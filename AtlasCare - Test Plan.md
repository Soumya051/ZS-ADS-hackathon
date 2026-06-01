# Project AtlasCare — Test Plan

## What Is Covered

**Journey validation (J1, J2, J3)**
Agent capable of carrying out all three mandatory journeys with multi-step queries being broken into smaller queries (yet to be tested end-to-end due to code being WIP)

**Relevance classifier correctness**
The planner is tested against a set of hand-labelled queries covering: single-intent queries, multi-intent compound queries, fully irrelevant queries, and mixed queries containing one legitimate and one malicious sub-query. Expected output is a PlannerResponse with correct relevance tags, intents, and extracted entities.

**Gate-level rejection**
Injection-pattern queries and off-topic queries are tested to confirm they are dropped at Gate 1 or Gate 2 and never reach a tool call.

**API contract**
POST /query and GET /health are tested to confirm they return the exact response schema specified in the brief, including trace_id, session_id, latency_ms, and tool_calls.

---

## Deliberately Out of Scope for This Submission

- **PII masking** — not yet implemented; no tests written for masking behaviour
- **Session continuity** — multi-turn conversations across requests are not tested; each request is treated as stateless
- **Load and stress testing** — no tests at the 18,000 interactions/day scale
- **Voice and email channels** — only the chat/API interface is tested
- **Failure recovery** — partial failures mid-J2 (e.g. cancellation succeeds but address update fails) are not yet handled or tested

---

## Before Go-Live

**Regression suite on the classifier**
As new intents are added, automated regression tests will confirm existing intent classification is not degraded — critical given the finite-intent architecture where adding a handler must not disturb existing ones.

**PII masking validation**
Tests to confirm no raw phone number, email, or address appears in any Gemini prompt, query log entry, or CRM case summary.

**Latency benchmarking under load**
Simulate peak traffic (18,000 interactions/day ≈ ~13 requests/second) to validate P95 latency stays within the 5-second budget and identify bottlenecks in the LLM call or tool layer.

**Adversarial prompt testing**
A structured red-teaming exercise with injection attempts, boundary-probing refund amounts (e.g. exactly ₹25,000, ₹25,001), and multi-language queries to stress-test Gate 1 and Gate 2 rejection.

**Shadow mode evaluation**
Run AtlasCare in parallel with the existing rule-based bot on live traffic, comparing resolution rates and escalation decisions without exposing the agent's responses to customers — allows real-world accuracy measurement before full cutover.

**Hallucination detection layer**
Automated checks that cross-reference every order detail in an agent response against the OMS record for that query, flagging any response that contains a field value not present in the source data.