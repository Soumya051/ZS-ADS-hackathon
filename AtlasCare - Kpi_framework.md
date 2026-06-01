# Project AtlasCare — KPI Framework

> **Context:** Acme Retail receives ~18,000 customer interactions per day. Tier-1 support is under pressure on three fronts: rising cost per contact, inconsistent CX across bot versions and agents, and slow multi-step resolution requiring multiple handoffs. AtlasCare is evaluated not just on happy-path accuracy, but on whether it is production-grade — observable, safe, scalable, and auditable.

---

## 1. Business KPIs
*Is AtlasCare reducing the pressure on Tier-1 support and delivering measurable value to Acme Retail?*

| KPI | Description | Why It Matters Here | Target |
|-----|-------------|----------------------|--------|
| **Self-serve resolution rate** | % of the ~18,000 daily interactions fully resolved by the agent without human fallback | Directly addresses the "human fallback rate too high" pain point | > 70% |
| **Human fallback rate** | % of queries escalated to a human agent | The inverse of self-serve rate; tracked separately for SRE alerting | < 30% |
| **Cost per contact** | Compute + LLM API cost per resolved query vs. baseline human agent cost | Core business case for AtlasCare — must show a downward trend vs. the hybrid model | Decreasing trend |
| **Multi-step resolution rate** | % of compound requests (J2-style: cancel + refund + reship) completed in a single interaction without handoff | Directly addresses the "slow multi-step resolution" pain point | > 90% |
| **Repeat contact rate** | % of customers who contact support again within 24 hrs on the same issue | Measures whether resolutions are actually correct, not just completed | < 10% |

---

## 2. Quality KPIs
*Is the agent doing the right thing, correctly and consistently — addressing the inconsistent CX pain point?*

| KPI | Description | Why It Matters Here | Target |
|-----|-------------|----------------------|--------|
| **Intent classification accuracy** | % of queries where the planner correctly identified all intents | Inconsistent classification = inconsistent CX, the same problem as mismatched bot versions | > 95% |
| **Entity extraction accuracy** | % of structured entities (order ID, phone, refund amount) correctly extracted | Errors here cascade into wrong tool calls and wrong resolutions | > 98% |
| **Response consistency score** | % of identical queries that receive a structurally equivalent response across sessions | Brand and compliance teams flagged inconsistency — this KPI directly tracks it | > 98% |
| **Hallucination rate** | % of responses containing order details not sourced from the OMS | With 150,000 SKUs, fabricated product or status details would erode customer trust rapidly | 0% |
| **Multi-ask completion rate** | % of compound queries where every sub-query was resolved in the same interaction | Measures the core J2 capability that replaces multi-handoff coordination | > 90% |
| **Incorrect escalation rate** | % of queries escalated that were within the agent's auto-resolve capability | Unnecessary escalations inflate cost and waste human agent time | < 5% |

---

## 3. Safety KPIs
*Is the agent staying within its guardrails and remaining auditable by Acme's Risk & Compliance team?*

| KPI | Description | Why It Matters Here | Target |
|-----|-------------|----------------------|--------|
| **Threshold breach — missed escalations** | Count of refund requests above ₹25,000 that were auto-processed instead of escalated | A single missed escalation is a compliance failure — Risk & Compliance will audit this | 0 |
| **Prompt injection block rate** | % of detected injection attempts blocked before any DB or tool call | 2M monthly active users means a non-trivial attack surface | 100% |
| **Malicious sub-query pass-through rate** | % of queries containing a malicious sub-query where the malicious part was executed | Gate 2 (intent tagging) must ensure no unrecognised operation ever reaches a tool | 0% |
| **Unauthorised tool call rate** | Count of tool calls triggered outside of a mapped, validated intent handler | Audit evidence that the system cannot be manipulated into arbitrary DB operations | 0 |
| **CRM case audit completeness** | % of escalated cases with a linked trace_id, structured summary, and created_at timestamp | Required for Risk & Compliance auditability — incomplete cases are an audit gap | 100% |

---

## 4. Operational KPIs
*Is the system healthy, observable, and operable by Acme's SRE team at 18,000 interactions/day scale?*

| KPI | Description | Why It Matters Here | Target |
|-----|-------------|----------------------|--------|
| **P50 / P95 end-to-end latency** | Median and 95th percentile response time across all queries | At 18,000 interactions/day, high tail latency directly impacts customer experience at scale | P50 < 2s, P95 < 5s |
| **J1 latency (Track Order)** | End-to-end latency for simple tracking queries — the highest volume query type | Hard requirement from the brief; simple queries must never be slow | < 3s |
| **API error rate** | % of `/query` requests returning a non-200 response | SRE alerting baseline — a spike here signals a systemic failure | < 1% |
| **Tool call failure rate** | % of OMS / CRM / Payments tool calls returning an error | Tool failures cause partial resolutions, which drive repeat contacts | < 3% |
| **LLM call latency** | Time taken by the Gemini classification call alone | Single point of latency risk — if this degrades, all journeys degrade | < 2s |
| **Daily API quota utilisation** | Gemini API calls consumed vs. available quota | Quota exhaustion = total service outage; must be monitored proactively | < 80% of quota |
| **DB write success rate** | % of query log `INSERT` operations that completed successfully | The query log is the audit trail — failed writes are silent compliance gaps | > 99.9% |
| **CRM case creation success rate** | % of escalations where a CRM case was successfully created and linked to a `trace_id` | A failed case creation means a customer is escalated with no record for the human agent | 100% |
