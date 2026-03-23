# CYBER SECURITY COUNCIL — INVOCATION TEMPLATE
### Reusable Prompt Template for Summoning the Council
### Version 3.0

---

## How to Use This Template

Copy the invocation block below, fill in the fields, and submit it as your prompt.
Fields marked `[REQUIRED]` must be completed. Fields marked `[OPTIONAL]` may be omitted —
the Chair will apply sensible defaults.

**Keep the Operating Charter reference at the top** so the model can locate its operating instructions.

**Claude Cowork / agentic environment note:** You do not need to paste large files directly
into the invocation block. Use the evidence guidance below to supply file paths, commands,
or repository locations instead. See the "Cowork / Agent Evidence Guide" section for details.

---

## Pre-Flight Checklist

Before invoking the Council, review this list. The more you provide, the better the deliberation.

- [ ] **Is the question specific enough to produce a decision?** Vague questions produce vague councils.
      Reframe "Should we improve our security?" to "Should we prioritize patching CVE-X or deploying
      MFA across the VPN fleet first, given our current exposure?"
- [ ] **Have you provided the most important evidence?** Log snippets, CVE details, architecture notes,
      recent incidents, and organizational constraints are all valuable.
- [ ] **Do you want a specific expert composition?** If so, fill in Expert Override.
- [ ] **Is this time-sensitive?** If yes, note it in Special Instructions — it changes expert behavior.
- [ ] **Who is the audience for the output?** If executives, use Executive Brief mode.
      If your security team, use Analyst Roundtable.
- [ ] **Do you need management sign-off?** If yes, enable Management/Executive Review.

---

## What Each Field Contributes to Deliberation Quality

| Field | What It Adds | What's Lost Without It |
|---|---|---|
| **Topic / Question** | Precise framing prevents scope drift | REQUIRED — session cannot proceed |
| **Available Evidence** | Grounds expert positions in specifics | Experts argue from general domain knowledge only |
| **Tone Mode** | Controls depth and adversarial intensity | Chair defaults to Analyst Roundtable |
| **Chair Voting** | Enables tiebreaking | Split decisions possible with no tiebreak |
| **Domain Emphasis** | Steers expert selection toward your priority angle | Chair selects from topic alone |
| **Output Length** | Matches output to your audience | Follows tone mode default |
| **Expert Override** | Guarantees specific expertise is present | Dynamic selection may miss a domain you need |
| **Execution Mode** | Structural round isolation for each expert prompt | Sequential single-session execution |
| **Special Instructions** | Adds constraints, assumptions, and focus areas | Experts use their own judgment |

**Quick rule:** If the decision matters enough to invoke the Council, it matters enough to fill in at least the Topic, Evidence, and Tone Mode fields.

---

## Invocation Block

```
## CYBER SECURITY COUNCIL — SESSION INVOCATION

**Operating Charter:** council.md (Cyber Security Council v3.0)
**Roster Reference:** roster.md

---

### [REQUIRED] Topic / Question

[State the cybersecurity topic, decision, question, or scenario the Council should deliberate on.
Be as specific as possible. If this is a yes/no decision, frame it as such.
If this is an open analytical question, state what output you need — e.g., a risk assessment,
a prioritization decision, a recommended course of action, a threat assessment, etc.

GOOD: "Should we emergency-patch CVE-2025-XXXXX within 24 hours, or implement a WAF rule
as a compensating control and patch during the next scheduled maintenance window in 9 days?"

WEAK: "What should we do about the new vulnerability?"]

---

### [OPTIONAL] Available Evidence / Context

[Paste or summarize relevant evidence, artifacts, logs, findings, threat intel,
organizational context, or background the Council should treat as working material.

**Cowork / Agentic Environment — File and Tool References:**
If you are running this Council in Claude Cowork or a Claude Code / agent environment,
you do not need to paste file contents directly. Instead, use one of these approaches:

1. FILE PATH: Provide absolute or workspace-relative paths to files the agent can read.
   Example: "Read /workspace/logs/auth-failure-2026-03-18.log before deliberating."

2. DIRECTORY CONTEXT: Point to a repository or folder.
   Example: "The application source is at /workspace/myapp/. Review the auth module at
   /workspace/myapp/src/auth/ before the session begins."

3. COMMANDS TO RUN: Ask the agent to run a command and use the output as evidence.
   Example: "Run: git log --oneline -20 in /workspace/myapp and use the output as context."

4. THREAT INTEL BUNDLE: Reference a saved threat report or IOC file.
   Example: "Evidence file: /workspace/intel/apt-campaign-brief.md"

5. SCREENSHOTS / ATTACHMENTS: Reference image files for the agent to read.
   Example: "See the Splunk screenshot at /workspace/screenshots/alert-cluster-2026-03-18.png"

If no evidence is provided, the Council will deliberate from general domain knowledge
and will explicitly note what evidence is missing.]

---

### [OPTIONAL] Tone Mode

Select one:
- [ ] Executive Brief Mode     — condensed; decision-focused; suitable for leadership
                                  Output: ~400–800 words
- [ ] Analyst Roundtable Mode  — full deliberation; deep reasoning; complete output [DEFAULT]
                                  Output: ~1,000–2,500 words
- [ ] High-Conflict Mode       — adversarial selection; extended challenge; stress-test focus
                                  Output: ~1,500–3,000+ words

[If not specified, the Chair uses Analyst Roundtable Mode.]

---

### [OPTIONAL] Execution Mode

Select one:
- [ ] Sequential (default)  — single-context deliberation; experts speak in turn
- [ ] Parallel (Best-Effort) — each expert prompt is dispatched as a structurally isolated call
                               per round; Round 1 outputs are not shared between experts
                               until Round 2 begins. Provides stronger prompt-level separation.
                               NOTE: This uses the same underlying model for all calls.
                               Independence is structural (prompt isolation), not model-level.
                               See council.md Section 15 for honest capabilities and limits.

[Parallel mode is recommended for high-stakes decisions where prompt-level independence matters.
It requires an orchestrator or agent environment that supports file-drop prompt dispatch
(see council_orchestrator.py).]

---

### [OPTIONAL] Chair Voting Behavior

Select one:
- [ ] Chair moderates only (default) — Chair does not cast a vote
- [ ] Chair votes                    — Chair casts a tiebreaking or full vote

[If Chair votes: majority requires 3 of 4 when 3 experts are seated.]

---

### [OPTIONAL] Domain Emphasis

[If you want expert selection to prioritize a specific domain or angle, state it here.
Examples:
- "Prioritize cloud security perspective — our environment is AWS-heavy."
- "Ensure GRC voice is present — this decision has regulatory implications."
- "Weight toward incident response over architecture — we have an active situation."
- "Include adversary simulation perspective to stress-test our assumptions."]

---

### [OPTIONAL] Output Length Preference

Select one:
- [ ] Short    — decision and key rationale only (~300–500 words)
- [ ] Standard — full deliberation with summary output (~800–1,500 words)
- [ ] Full     — complete roundtable with all cross-examination and extended dissent (2,000+ words)

[If not specified, output length follows the Tone Mode default.]

---

### [OPTIONAL] Expert Override

[Manually specify which experts are seated rather than allowing the Chair to select.
Use roster last names: e.g., "Seat: CALLOWAY, VANCE, CHEN"
Leave blank for dynamic selection.]

---

### [OPTIONAL] Expert Panel Size

[Number of experts the Chair should select. Default: 3. Recommended: 3–5.
Higher counts increase diversity but also increase processing time and may reduce consensus speed.]

---

### [OPTIONAL] Management/Executive Review Required

- [ ] Yes — require final business authorization layer after technical decision
- [ ] No  — stop at technical decision (default)

[If Yes, the final technical decision is passed to a Management Persona (Enterprise CISO / Risk Committee)
for a final business sign-off. Produces an AUTHORIZATION field and executive commentary.]

---

### [OPTIONAL] Special Instructions

[Any additional constraints, focus areas, assumptions, or behavioral instructions.
Examples:
- "Focus the deliberation on detection feasibility, not just threat severity."
- "Assume the organization has a mature SOC but limited cloud security tooling."
- "The decision must be defensible to an external auditor."
- "Treat this as an active incident — prioritize speed over completeness."
- "The council should declare no-confidence if evidence does not support a conclusion."
- "Each expert must name the strongest argument against their own position."
- "The environment has no EDR on OT systems — factor this into detection recommendations."
- "Budget ceiling for any recommendation is $200K for this fiscal year."]

---

### SESSION BEGIN

[The Chair will now open the session, identify assumptions, select the specified number of
experts (default three), and begin the deliberation according to the Operating Charter (v3.0).]
```

---

## Lightweight Quick Summon

For time-sensitive sessions where the full template is not warranted. The Chair applies defaults for all unspecified fields.

```
Summon the Cyber Security Council.
Topic: [Your question here]
Context: [Key facts, constraints, or evidence]
Mode: [Executive Brief / Analyst Roundtable / High-Conflict]
```

**Note:** Quick Summon omits expert selection control, execution mode, and output length preferences.
Use the full template for decisions that require auditability, specific expert composition, or executive output.

---

## Cowork / Agent Evidence Guide

When running the Council in Claude Cowork or a Claude Code / agent environment, you can supply evidence as tool instructions rather than pasting content directly. Insert these as the first instruction under "Available Evidence / Context":

### Supply a single file
```
Before deliberating, read the following file and treat its contents as evidence:
File: /path/to/evidence.md
```

### Supply a directory or repository
```
Before deliberating, explore the following directory to understand the context:
Directory: /workspace/my-project/
Focus on: [specific subdirectories or file types]
```

### Run a command and use its output
```
Before deliberating, run the following command and treat the output as evidence:
Command: [command here]
Working directory: [path]
```

### Supply multiple artifacts
```
Before deliberating, read these files in order and treat all contents as evidence:
1. /workspace/intel/threat-brief.md
2. /workspace/logs/auth-events-2026-03-18.txt
3. /workspace/architecture/network-diagram.md
```

### Reference screenshots or images
```
Before deliberating, view the following screenshot and treat it as evidence:
Image: /workspace/screenshots/siem-dashboard.png
```

---

## Filled Examples

### Example 1 — Vulnerability Triage

```
## CYBER SECURITY COUNCIL — SESSION INVOCATION

**Operating Charter:** council.md (Cyber Security Council v3.0)
**Roster Reference:** roster.md

---

### Topic / Question

CVE-2025-XXXXX has been identified in our internally deployed web framework (RCE via
deserialization, CVSS 9.1). A public PoC exists. The application is internal-only, serves
11 teams including Finance, HR, and Executive Support. Patch requires a 4-hour maintenance
window; next scheduled window is 9 days out.

Should we emergency-patch within 24 hours, deploy a compensating WAF rule and patch
in 9 days, or accept risk and monitor until the scheduled window?

---

### Available Evidence / Context

- CVE published 6 days ago; PoC available on GitHub since day 2
- No confirmed exploitation in the wild against this CVE as of today
- Application is not internet-facing; accessible from corporate network only
- Network segmentation exists between app server and production databases
- WAF in place but not configured to block deserialization payloads specifically
- 3 of 11 teams using the application are high-sensitivity (Finance, HR, Executive)
- Patch has been tested in staging; no regressions found

---

### Tone Mode

- [x] Analyst Roundtable Mode

---

### Domain Emphasis

Ensure vulnerability management and detection engineering perspectives are represented.
Include at least one voice that will push back on emergency patching urgency.

---

### Output Length Preference

- [x] Standard

---

### SESSION BEGIN
```

---

### Example 2 — Active Incident Attribution

```
## CYBER SECURITY COUNCIL — SESSION INVOCATION

**Operating Charter:** council.md (Cyber Security Council v3.0)
**Roster Reference:** roster.md

---

### Topic / Question

We are observing lateral movement in our environment using WMI, PsExec, and Cobalt Strike
beacon variants. TTPs partially overlap with a tracked nation-state financial sector threat
actor. We cannot rule out a financially motivated criminal group using similar tooling.

Should we attribute this to a nation-state actor for purposes of our IR strategy and
executive briefing, or treat this as unattributed and respond to behavior rather than actor?

---

### Available Evidence / Context

- Cobalt Strike beacon with malleable C2 profile matching known infrastructure cluster
- WMI persistence consistent with APT behavior but also used by crimeware groups
- Exfiltration of financial projection documents (not PII, not customer data)
- C2 domain registered 3 weeks ago; no prior threat intel match
- Compromised accounts belong to Treasury and M&A teams
- No ransomware deployed; lateral spread confirmed to 3 hosts so far
- Dwell time estimated at 11–17 days based on log retention

---

### Tone Mode

- [x] High-Conflict Mode

---

### Chair Voting Behavior

- [x] Chair votes

---

### Special Instructions

The council must explicitly address whether attribution confidence is sufficient to justify
executive-level communication about a nation-state actor. Dissenting views on attribution
confidence must be preserved in the final record.

---

### SESSION BEGIN
```

---

### Example 3 — Cowork File-Based Evidence

```
## CYBER SECURITY COUNCIL — SESSION INVOCATION

**Operating Charter:** council.md (Cyber Security Council v3.0)
**Roster Reference:** roster.md

---

### Topic / Question

We have received a security assessment report for a third-party vendor we are evaluating
for access to our production data pipeline. Should we approve, conditionally approve,
or reject the vendor based on their security posture?

---

### Available Evidence / Context

Before deliberating, read the following files:
1. /workspace/vendor-assessments/acme-corp-soc2-report-2025.pdf — vendor's SOC 2 Type II report
2. /workspace/vendor-assessments/acme-corp-pentest-2025.md — summary of their pentest findings
3. /workspace/architecture/data-pipeline-diagram.md — our pipeline architecture and data sensitivity

Use the contents of all three files as the council's evidence base.

---

### Tone Mode

- [x] Analyst Roundtable Mode

---

### Expert Override

Seat: NAVARRO, CHEN, CALLOWAY

---

### Management/Executive Review Required

- [x] Yes

---

### SESSION BEGIN
```

---

### Example 4 — Post-Quantum Readiness (Parallel Execution)

```
## CYBER SECURITY COUNCIL — SESSION INVOCATION

**Operating Charter:** council.md (Cyber Security Council v3.0)
**Roster Reference:** roster.md

---

### Topic / Question

Should our organization begin planning and implementing quantum-resistant cryptography now,
or should we wait until standards, vendor support, and enterprise adoption mature further?

---

### Available Evidence / Context

- Mid-to-large enterprise with cloud services, on-prem systems, VPNs, PKI/certificates,
  internal applications, third-party SaaS, and legacy systems
- NIST finalized ML-KEM (FIPS 203), ML-DSA (FIPS 204), SLH-DSA (FIPS 205) in August 2024
- NSA CNSA 2.0 guidance issued 2022 with explicit migration timelines for national security systems
- HSM vendor support for ML-DSA is limited as of early 2026 — Thales Luna 7.x partial, others roadmap-only
- Organization holds data with 10–15 year confidentiality requirements (M&A, R&D, legal)
- Full enterprise migration estimated at 5–7 years across heterogeneous infrastructure

---

### Tone Mode

- [x] Analyst Roundtable Mode

---

### Execution Mode

- [x] Parallel (Best-Effort)

---

### Expert Override

Seat: VORONOV, HARTLEY, OSEI

---

### Output Length Preference

- [x] Full

---

### Special Instructions

- Require aggressive cross-examination of assumptions about CRQC timelines
- Each expert must name the strongest argument against their own position
- Address harvest-now-decrypt-later as a specific threat vector
- End with a practical 12-month roadmap and named triggers for accelerating implementation

---

### SESSION BEGIN
```

---

*Cyber Security Council Invocation Template — Version 3.0*
*For operating instructions, see council.md. For the full expert roster, see roster.md.*
