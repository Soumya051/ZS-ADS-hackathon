# Project AtlasCare — Architecture Document

---

## Key Architectural Decisions

### 1. Relational DB over Document-Oriented Mock Schema

The provided schemas are document-oriented, with nested objects (addresses inside customers, items inside orders) optimised for static mock data. The implemented design normalises every entity that needs to be independently queried, updated, or audited at runtime — matching what a production enterprise system requires.

**Key normalisation decisions:**

- **`shipping_address_id` as a foreign key** on orders rather than an inline object, preserving address individuality and enabling easy querying via IDs. Addresses are referenced using simplified IDs (e.g. 1–10, where 10 is the max saved per user), making future address updates clean and predictable.
- **`addresses` as a standalone table**, enabling label-based lookup (e.g. "office address") without runtime JSON parsing.
- **`cases` promoted to a first-class table** with proper foreign keys, making runtime case creation a clean, atomic `INSERT`.

---

### 2. Query Logging at the DB Layer

A dedicated `queries` table in the Orders DB links every user interaction to a `customer_id`, `order_id`, structured `intent`, and `intent_details`.

> Interaction history is queryable directly from the DB — a Risk & Compliance team does not need to dig through application logs or distributed traces to audit what a customer asked and what the agent classified it as.

---

### 3. Single LLM Call for Classification

Relevance check, intent classification, entity extraction, and malicious sub-query detection are consolidated into **one Gemini call** with a structured Pydantic response schema.

- Avoids sequential LLM round-trips
- Keeps classification latency tight — critical for the J1 under-3-second constraint

---

### 4. Structured Output with Typed Discriminated Union *(implementation incomplete)*

The planner response uses a Pydantic discriminated union (`AnyDetails`) for the `details` field, keyed on a `detail_type` literal.

- Guarantees downstream workflow handlers receive a fully typed, validated payload
- Eliminates dict key errors or missing field surprises at execution time
- Reduces query processing errors introduced by model interpretation

---

### 5. No Direct AI-to-DB Access

Every user query goes through a structured classification layer before anything touches the database. The pipeline enforces this in **three successive gates**:

| Gate | Name | What it does |
|------|------|--------------|
| **Gate 1** | Relevance Filter | Gemini classifies only order-related queries as relevant. Anything off-topic or suspicious is rejected before any intent is resolved. |
| **Gate 2** | Intent Tagging | Relevant queries are mapped to a strict, finite set of supported intents. No query can trigger an unrecognised operation. Adding a new capability requires explicitly building a new intent and its handler. |
| **Gate 3** | Detail Extraction | Each intent carries a scoped detail payload containing only what that specific operation requires. Structured entities — order IDs, phone numbers, refund amounts — are extracted via regex, reducing LLM load and ensuring critical fields are never left to model interpretation. No freeform user input is passed to any downstream system. |

**Net result:** A prompt injection attempt either fails at Gate 1, or produces an intent with no handler and is silently dropped at Gate 2. The database only ever receives clean, validated, intent-scoped inputs — never raw user text.

---

## Planned — To Be Implemented Before Go-Live

### 6. PII Masking 
All customer PII must be masked at the earliest possible point in the pipeline: **before the raw user message is passed to Gemini or any other model**. No LLM, no tool, and no downstream system should ever see unmasked PII. The masking step sits between raw input ingestion and the classification call, replacing identified PII with anonymised tokens (e.g. `+91-98765XXXXX`, `p*****@email.com`) using regex - consistent with the same extraction patterns already planned for entity extraction. The original values are to be held in a short-lived, request-scoped map and re-substituted only at the point where a tool call will genuinely require them (e.g. the OMS address update), and are never to be writteninto  the query log or CRM case summaries.

### 7. Refund Guardrail & Human Agent Handover

The auto-refund limit is read dynamically from the `payment_config` table at runtime, so it can be updated **without a code change**.

**If a refund request exceeds the threshold:**
- The payments tool is **never called**
- A CRM case is created with a structured summary covering:
  - The user's original query
  - What the agent already resolved
  - What remains pending for the human agent
- The case is linked to the originating `trace_id` for full traceability
- The customer receives a holding message with the expected SLA, sourced from the KB


### 8. Hybrid Pre-filter Before the LLM

A regex keyword pre-filter running before the LLM call. Obvious off-topic or injection-pattern queries are rejected instantly at zero cost, preserving API quota for genuine customer interactions.

### 9. Dependency-Aware Multi-Ask Execution

Multi-step compound requests handled by a `depends_on_previous` flag returned by the planner:

- **Independent asks** → batched and executed in parallel via `asyncio.gather`
- **Dependent asks** → batch is flushed and execution proceeds sequentially

This gives the fastest possible resolution time without compromising correctness on ordered operations such as cancel-then-refund.
