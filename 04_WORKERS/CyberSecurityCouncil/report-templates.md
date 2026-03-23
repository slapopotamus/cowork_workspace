# CYBER SECURITY COUNCIL — REPORT TEMPLATES
### Standardized Output Formats for Different Audiences
### Version 3.0

---

## How to Use This File

After a Council session concludes, select the template that matches your audience and
populate it from the session's decision record. Three templates are provided:

- **Template A — Executive Summary:** One page. Decision-focused. For boards, C-suite,
  and non-technical leadership. Minimize jargon. Emphasize risk, consequence, and action.

- **Template B — Technical Decision Record:** Full deliberation summary. For security
  teams, architects, auditors, and compliance functions. Preserve full reasoning,
  dissent, evidence gaps, and open questions.

- **Template C — Action Tracking Record:** Distills recommendations into a trackable
  action list for operations, program management, or ticket systems.

All templates draw from the decision record produced by the Chair in Round 4
(see council.md Section 10 for the decision record format specification).

---

## Template A — Executive Summary

*Target audience: Board, C-suite, executive leadership, non-technical stakeholders*
*Target length: One page / 300–500 words*
*Source fields: DECISION, OUTCOME TYPE, AGGREGATE CONFIDENCE, OUTCOME RATIONALE, IMMEDIATE ACTIONS, REVIEW TRIGGER CONDITIONS, DISSENT, OPEN QUESTIONS*

---

```
CYBER SECURITY COUNCIL — EXECUTIVE BRIEF
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Date:            [YYYY-MM-DD]
Topic:           [One-line topic description]
Session ID:      [YYYY-MM-DD-topic-slug]
Prepared by:     [Name / Role]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RECOMMENDATION
[1–2 sentences: what the council recommends and the core reason why.
Use plain language. Avoid jargon. State what should happen, not what was discussed.]

CONFIDENCE LEVEL: [High / Medium / Low]
OUTCOME TYPE:     [Unanimous Consensus / Majority Decision / Split / No-Confidence / Provisional]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

THE QUESTION
[1 sentence: the specific decision or question the council addressed.]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

KEY CONSIDERATIONS
[3–5 bullet points — the most important factors the council weighed.
Non-technical language. Focus on risk, cost, time, and consequence.]

• [Consideration 1]
• [Consideration 2]
• [Consideration 3]
• [Consideration 4 — optional]
• [Consideration 5 — optional]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RISK IF NOT ACTED ON
[1–2 sentences: likely consequence if this recommendation is not followed,
and the timeframe in which that risk materializes.]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

IMMEDIATE NEXT STEPS
1. [Action] — Owner: [Role/Team] — By: [Date or timeframe]
2. [Action] — Owner: [Role/Team] — By: [Date or timeframe]
3. [Action — optional] — Owner: [Role/Team] — By: [Date or timeframe]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

WHEN THIS DECISION EXPIRES
[State the specific event or date that triggers re-evaluation of this recommendation.
E.g., "If exploitation in the wild is confirmed," "at the 30-day mark," or
"if vendor patches the dependency."]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

WHAT THE COUNCIL COULD NOT DETERMINE
[1–2 sentences: what the council lacked confidence about, and what information would resolve it.
Being explicit about uncertainty builds credibility with leadership.]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DISSENTING VIEW [include only if Majority Decision — omit if Unanimous Consensus]
[1–2 sentences: summarize the minority position and its core reasoning.
Preserving dissent demonstrates intellectual rigor and helps leadership
assess the robustness of the recommendation.]
```

---

## Template B — Technical Decision Record

*Target audience: Security team, architects, GRC/compliance, internal audit*
*Target length: 500–2,000 words depending on deliberation complexity*
*Source fields: all fields from the Chair's Round 4 synthesis*

---

```
CYBER SECURITY COUNCIL — TECHNICAL DECISION RECORD
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Date:             [YYYY-MM-DD]
Session ID:       [YYYY-MM-DD-topic-slug]
Topic:            [Full question statement as posed to the council]
Experts Seated:   [ROSTER_NAME (Role), ROSTER_NAME (Role), ROSTER_NAME (Role)]
Execution Mode:   [Sequential / Parallel (Best-Effort)]
Tone Mode:        [Executive Brief / Analyst Roundtable / High-Conflict]
Chair Voted:      [Yes / No]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

VOTE TALLY
[List each expert's final vote: Name — Decision — Confidence]
• [Expert 1] — [Decision] — [High/Medium/Low]
• [Expert 2] — [Decision] — [High/Medium/Low]
• [Expert 3] — [Decision] — [High/Medium/Low]
[If Chair voted: Chair — [Decision] — [High/Medium/Low]]

OUTCOME TYPE: [Unanimous Consensus / Majority Decision / Split Decision / No-Confidence / Provisional Action]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DECISION
[Full decision statement — what the council recommends or concludes. 2–4 sentences.]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

OUTCOME RATIONALE
[Why this outcome won. Summarize the argument chain from evidence to conclusion.
Include the strongest arguments on both sides. 2–4 paragraphs. This section is the
primary audit trail for why this decision was made — do not summarize it away.]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DISSENT
[If Majority or Split: name the dissenting expert(s), state their full position,
and record their key reasoning. Do not summarize the dissent into meaninglessness —
a dissent that survives the decision may prove correct later.
If Unanimous Consensus: "None." Then note: "Strongest counterargument raised: [brief statement]"]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

AGGREGATE CONFIDENCE
Level: [High / Medium / Low]
Rationale: [What drives or limits aggregate confidence — 2–3 sentences]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

KEY CROSS-EXAMINATION INSIGHTS
[The 2–3 most important challenges or position shifts from Round 2 and Round 3.
For each: name the claim, who challenged it, and what changed as a result.]

• [Insight 1]
• [Insight 2]
• [Insight 3 — optional]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EVIDENCE CONSIDERED

Present:
• [Evidence item]
• [Evidence item]

Noted as missing (evidence gaps):
• [Gap 1 — what it was and how it would have changed confidence or the decision]
• [Gap 2]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ASSUMPTIONS THIS DECISION RESTS ON
[These are the working premises. If any of these prove false, the decision should be revisited.]

• [Assumption 1]
• [Assumption 2]
• [Assumption 3]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TRADEOFFS ACCEPTED
[What is being sacrificed, deprioritized, or risked by this recommendation.
No recommendation is cost-free. Name the tradeoffs explicitly.]

• [Tradeoff 1]
• [Tradeoff 2]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

IMMEDIATE ACTIONS
[For each: action, suggested owner (role not name), and timeline]

1. [Action] — Suggested Owner: [Role/Team] — Timeline: [Date or relative]
2. [Action] — Suggested Owner: [Role/Team] — Timeline: [Date or relative]
3. [Action] — Suggested Owner: [Role/Team] — Timeline: [Date or relative]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

REVIEW TRIGGER CONDITIONS
[Specific, concrete conditions that would invalidate this decision or require it to be revisited.
Vague caveats ("if conditions change") provide no governance value.]

This decision should be revisited if:
• [Trigger 1 — specific and actionable]
• [Trigger 2]
• [Trigger 3]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

OPEN QUESTIONS
[What the council could not determine, and what evidence would resolve each question.]

1. [Question] — Would be resolved by: [Evidence needed]
2. [Question] — Would be resolved by: [Evidence needed]
3. [Question — optional] — Would be resolved by: [Evidence needed]
```

---

## Template C — Action Tracking Record

*Target audience: SOC, engineering teams, program/project management, ticket systems*
*Target length: 100–300 words*
*Source fields: IMMEDIATE ACTIONS, REVIEW TRIGGER CONDITIONS, DECISION*
*Purpose: Create tickets, assign owners, and track follow-through*

---

```
CYBER SECURITY COUNCIL — ACTION TRACKING RECORD
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Session ID:   [YYYY-MM-DD-topic-slug]
Date:         [YYYY-MM-DD]
Decision:     [One-sentence summary of what was decided]
Confidence:   [High / Medium / Low]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ACTIONS

[ ] Action 1: [Description]
    Owner: [Role/Team]        Due: [Date]       Status: [ ] Open [ ] In Progress [ ] Done

[ ] Action 2: [Description]
    Owner: [Role/Team]        Due: [Date]       Status: [ ] Open [ ] In Progress [ ] Done

[ ] Action 3: [Description]
    Owner: [Role/Team]        Due: [Date]       Status: [ ] Open [ ] In Progress [ ] Done

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RE-EVALUATION TRIGGERS

This decision expires / requires re-evaluation if:
[ ] [Trigger 1]
[ ] [Trigger 2]

Scheduled review date: [YYYY-MM-DD or "When trigger fires"]
Review owner: [Role/Team]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NOTES / BLOCKERS
[Any impediments to action completion, dependencies, or escalation notes]
```

---

*Cyber Security Council Report Templates — Version 3.0*
*For session logging, see session-log-template.md.*
*For operating instructions, see council.md.*
*For the decision record format specification, see council.md Section 10.*
