# CYBER SECURITY COUNCIL — SESSION LOG TEMPLATE
### For Audit, Organizational Learning, and Decision Tracking
### Version 3.0

---

## How to Use This Template

Complete one entry per Council session. File each completed log in the `sessions/` directory
as `sessions/YYYY-MM-DD-topic-slug.md` and add a row to `sessions/index.html`.

When using the orchestrator (`council_orchestrator.py`), this file is generated automatically.
When running a manual or conversational session, fill this template by hand.

**The Retrospective section should be left blank at session time** and updated later —
once the decision has been acted on and its quality can be assessed in hindsight.

**The full deliberation transcript must NOT be truncated.** It is the primary audit record.

---

## Session Record

**Date:** [YYYY-MM-DD]
**Session ID:** [YYYY-MM-DD-topic-slug — e.g., 2026-03-19-post-quantum-cryptography]
**Topic:** [One-line statement of the question deliberated]
**Invocation Mode:** [Full Template / Quick Summon / Informal / Orchestrator-Generated]
**Execution Mode:** [Sequential / Parallel (Best-Effort)]
**Parallel Compliance:** [N/A / Compliant — all expert prompts issued independently per round / Non-compliant — note gap]
**Tone Mode:** [Executive Brief / Analyst Roundtable / High-Conflict]
**Chair Voted:** [Yes / No]
**Management Review:** [Yes / No — if Yes, authorization status]

---

## Experts Seated

| Expert | Role | Why Selected |
|---|---|---|
| [ROSTER NAME] | [Role from roster] | [1-sentence rationale for selection] |
| [ROSTER NAME] | [Role from roster] | [1-sentence rationale for selection] |
| [ROSTER NAME] | [Role from roster] | [1-sentence rationale for selection] |

*If custom personas were used instead of roster personas, note names, domains, and bias profiles here.*

---

## Chair Framing (Round 0 Output)

*Copy the Chair's full Round 0 output here. This records the decision statement, missing context,
key assumptions, central tension, and expert selection rationale.*

```
DECISION_STATEMENT: [Precise rephrasing of the decision]

MISSING_CONTEXT:
- [item]

KEY_ASSUMPTIONS:
- [assumption]

CENTRAL_TENSION: [1–2 sentences]

EXPERT_1_NAME: [name]
EXPERT_1_ROLE: [role]
EXPERT_1_RATIONALE: [rationale]
[...repeat for all experts...]

SESSION_OPENING: [opening statement]
```

---

## Decision Record

*Copy the Chair's full Round 4 synthesis output here.*

```
VOTE TALLY:
- [Expert] — [Decision] — [Confidence]
- [Expert] — [Decision] — [Confidence]
- [Expert] — [Decision] — [Confidence]

OUTCOME TYPE: [Unanimous Consensus / Majority Decision / Split Decision / No-Confidence / Provisional Action]

DECISION:      [What the council recommends — 2–4 sentences]
OUTCOME RATIONALE: [Why this outcome won — 2–4 paragraphs]
DISSENT:       [Dissenting expert, their position, and key reasoning — or "None"]

AGGREGATE CONFIDENCE: [High / Medium / Low]
CONFIDENCE RATIONALE: [2–3 sentences]

KEY CROSS-EXAMINATION INSIGHTS:
- [Insight 1: claim, challenger, outcome]
- [Insight 2]

EVIDENCE GAPS:
- [Gap 1]
- [Gap 2]

ASSUMPTIONS THIS DECISION RESTS ON:
- [Assumption 1]
- [Assumption 2]

IMMEDIATE ACTIONS:
1. [Action] — Suggested Owner: [Role] — Timeline: [Timeframe]
2. [Action] — Suggested Owner: [Role] — Timeline: [Timeframe]

REVIEW TRIGGER CONDITIONS:
- [Condition 1]
- [Condition 2]

OPEN QUESTIONS:
1. [Question] — Resolved by: [Evidence needed]
2. [Question] — Resolved by: [Evidence needed]
```

---

## Full Deliberation Transcript (Audit Record)

*Paste the complete Round 1, Round 2, and Round 3 outputs here in full.*
*Do not truncate. This is the primary audit trail for why the decision was made.*

### Round 1 — Initial Assessments

[Full Round 1 outputs from all experts]

### Round 2 — Cross-Examination

[Full Round 2 outputs from all experts]

### Round 3 — Rebuttal and Final Votes

[Full Round 3 outputs from all experts]

---

## Retrospective *(complete after decision is acted on)*

**Date reviewed:** [YYYY-MM-DD]
**Decision acted on?** [Yes / No / Partially]
**Decision validated?** [Correct / Partially correct / Incorrect / Too early to assess]
**What happened:** [Brief description of outcomes after the recommendation was followed or not]
**What the council got right:** [Specific aspects of the analysis that proved accurate]
**What the council got wrong:** [Specific aspects that proved incorrect or overstated]
**Were the evidence gaps significant?** [Did the missing evidence named in the session turn out to matter?]
**Were the review triggers hit?** [Did any of the stated trigger conditions materialize?]
**Lessons for future sessions:** [Process, selection, or framing improvements identified]

---

## Index Entry (copy this row into sessions/index.html)

```html
<tr>
    <td>[YYYY-MM-DD]</td>
    <td><a href="./[session-id].md">[session-id].md</a></td>
    <td>[Topic — truncated to ~70 chars]</td>
    <td>[Expert 1 last name], [Expert 2 last name], [Expert 3 last name]</td>
    <td><span class="badge">[Outcome Type]</span></td>
    <td><span class="badge confidence-[High/Medium/Low]">[High/Medium/Low]</span></td>
</tr>
<!-- ROWS_END -->
```

---

*Session logged by: [Name / Role or "council_orchestrator.py v3.0"]*
*Template version: 3.0 — Cyber Security Council*
