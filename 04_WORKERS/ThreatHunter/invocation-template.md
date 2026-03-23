# THREAT HUNTER — INVOCATION TEMPLATE
### Reusable Prompt Template for Engaging REYES, Nikolai | Version 1.1

---

## How to Use This Template

Copy the invocation block below, fill in the required fields, and submit it as your prompt. REYES will open the engagement by restating the hypothesis, confirming scope, and working through the relevant hunt phases.

Leave the Operating Charter reference at the top so the model can locate its persona and methodology.

---

## What Each Field Contributes

| Field | What It Adds | What's Lost Without It |
|---|---|---|
| **Hypothesis / Objective** | Defines what behavior is being hunted | REQUIRED — hunt cannot proceed |
| **Available Evidence / Context** | Grounds the hunt in real telemetry, TI, or observations | Hunt operates from general TTP knowledge only; less targeted |
| **Platform** | Ensures queries are written for the right data source | REYES defaults to CrowdStrike CQL; may not match your environment |
| **Hunt Mode** | Controls which phases REYES executes; Query + Test adds a full test suite | REYES runs a full hunt by default; no test cases unless requested |
| **Tone** | Controls output verbosity | REYES defaults to Detailed mode |
| **ATT&CK Depth** | Controls depth of technique mapping and actor association | Surface mapping is applied by default |
| **Confidence Floor** | Raises the evidence bar for Confirmed/Probable ratings | Standard confidence thresholds apply |
| **Special Instructions** | Adds focus constraints, assumptions, or scope adjustments | REYES uses its own judgment |

---

## Invocation Block

```
## THREAT HUNTER — ENGAGEMENT INVOCATION

**Operating Charter:** hunter.md (Threat Hunter — REYES, Nikolai v1.0)

---

### [REQUIRED] Hypothesis / Objective

[State the hunt hypothesis or objective clearly. A well-formed hypothesis names:
 - The adversary behavior or TTP being hunted
 - The expected evidence if the behavior is present
 - The conditions under which the hunt can be closed

 If you are providing raw IOCs or behaviors for analysis rather than a structured
 hypothesis, state that here and REYES will construct the hypothesis from the input.

 Examples:
 - "Hunt for scheduled task abuse (T1053.005) used for persistence following initial access."
 - "We observed encoded PowerShell execution from an Office process. Determine scope."
 - "Threat intel indicates this actor uses WMI for lateral movement. Hunt for presence."
 - "Analyze these IOCs and recommend a hunt strategy."]

---

### [OPTIONAL] Available Evidence / Context

[Paste or summarize any relevant evidence REYES should treat as working material.
 This can include:
 - Raw IOCs (IPs, domains, hashes, URLs)
 - Log snippets or observed behaviors
 - Threat intelligence reports or TTP descriptions
 - MITRE ATT&CK techniques of interest
 - Organizational context (environment type, known tools, baseline behaviors)
 - Prior hunt results or detection gaps

 If no evidence is provided, REYES will hunt from general TTP knowledge and will
 explicitly note what evidence would strengthen the hunt.]

---

### [OPTIONAL] Platform

Select one or more:
- [ ] CrowdStrike LogScale (CQL)  — default; endpoint, identity, and process telemetry
- [ ] Microsoft Sentinel (KQL)    — cloud, Azure AD, Office 365, multi-source
- [ ] Splunk (SPL)                — Splunk-primary environments
- [ ] Multi-platform              — deliver queries for all applicable platforms with gap notes

[If not specified, REYES defaults to CrowdStrike LogScale CQL.]

---

### [OPTIONAL] Hunt Mode

Select one:
- [ ] Full Hunt (default)   — complete five-phase engagement: hypothesis, scope, queries, analysis, report
- [ ] Full Hunt + Test      — full hunt with a test suite produced for every query developed
- [ ] Query-Only            — deliver hunt queries only; skip analysis and report phases
- [ ] Query + Test          — deliver hunt queries with a full test suite (TP, TN, edge cases) for each
- [ ] Analysis-Only         — analyze provided IOCs, TTPs, or findings; no query development
- [ ] Report-Only           — produce a hunt report from findings already provided

[If not specified, REYES runs a Full Hunt without test cases. Test cases can also be requested
 for any existing query by asking REYES to "test" or "validate" a specific query.]

---

### [OPTIONAL] Tone

Select one:
- [ ] Detailed (default)  — full reasoning shown; hypothesis logic, query annotations, and confidence rationale included
- [ ] Operational         — concise output; findings and queries without extended reasoning; suitable for time-pressured hunts

---

### [OPTIONAL] ATT&CK Depth

Select one:
- [ ] Surface Mapping (default)  — primary technique and sub-technique identified; tactic stated
- [ ] Deep Mapping               — full technique analysis including procedure variants, sub-technique
                                   behavioral distinctions, and known actor associations

---

### [OPTIONAL] Confidence Floor

Select one:
- [ ] Standard (default)  — REYES applies normal confidence thresholds
- [ ] Strict              — Confirmed and Probable ratings require stronger corroborating evidence;
                            REYES will more readily return Insufficient Evidence rather than force a finding

---

### [OPTIONAL] Special Instructions

[Any additional constraints, scope definitions, or focus areas for this engagement.
 Examples:
 - "Focus on cloud identity telemetry only — endpoint is out of scope for this hunt."
 - "Assume the adversary has been present for 30+ days; extend the time window accordingly."
 - "Flag any detection engineering gaps you identify but do not include remediation."
 - "The environment uses a non-standard naming convention for service accounts — note this in scope."
 - "This hunt may be handed off to IR; produce the report assuming an IR audience."
 - "Do not escalate — produce findings only; IR decision will be made separately."]

---

### HUNT BEGIN

[REYES will open by restating the hypothesis, confirming scope and platform, identifying
 any evidence gaps, and proceeding through the relevant hunt phases per hunter.md.]
```

---

## Lightweight Quick Summon

For time-pressured engagements where the full template is not warranted:

```
Invoke the Threat Hunter.
Hypothesis: [What adversary behavior are you hunting?]
Evidence: [Any IOCs, observed behaviors, or TI to work from]
Platform: [CQL / KQL / SPL]
Mode: [Full Hunt / Query-Only / Analysis-Only]
```

REYES will apply defaults for all unspecified fields and flag any missing context that would meaningfully affect hunt confidence.

---

## Filled Example — Scheduled Task Abuse Hunt

```
## THREAT HUNTER — ENGAGEMENT INVOCATION

**Operating Charter:** hunter.md (Threat Hunter — REYES, Nikolai v1.0)

---

### Hypothesis / Objective

Hunt for scheduled task abuse (T1053.005) as a persistence mechanism following a suspected
initial access event. The triggering event was a phishing email opened by a user in the
finance team 72 hours ago. We have not confirmed a payload was executed, but we want to
rule out persistence before closing the ticket.

Expected behavior if present: schtasks.exe spawned by an unusual parent (e.g., Office process,
cmd spawned by browser), task creation with encoded or obfuscated command-line arguments, or
tasks pointing to user-writable paths or temp directories.

---

### Available Evidence / Context

- Phishing email received 2026-03-20 at 09:14 UTC; opened by user jdoe@corp.com
- Email contained a macro-enabled .xlsm attachment; macro execution is unconfirmed
- No AV or EDR alert fired on the endpoint (CORP-WRK-4421)
- No outbound C2 indicators identified in proxy logs as of 2026-03-22
- Environment uses CrowdStrike Falcon; full process telemetry is available

---

### Platform

- [x] CrowdStrike LogScale (CQL)

---

### Hunt Mode

- [x] Full Hunt

---

### Tone

- [x] Detailed

---

### ATT&CK Depth

- [x] Deep Mapping

---

### Special Instructions

Scope the hunt to CORP-WRK-4421 first. If findings are present on that host,
broaden to the full finance team endpoint group. Flag any additional TTPs
you would recommend hunting based on this access pattern.

---

### HUNT BEGIN
```

---

## Filled Example — IOC Analysis and Hunt Strategy

```
## THREAT HUNTER — ENGAGEMENT INVOCATION

**Operating Charter:** hunter.md (Threat Hunter — REYES, Nikolai v1.0)

---

### Hypothesis / Objective

We received the following IOCs from a threat sharing partner. Analyze them, assess
their hunt value and likely staleness, and recommend a hunt strategy. Build queries
for any IOCs or TTPs worth hunting in the environment.

---

### Available Evidence / Context

IOCs received 2026-03-21 from ISAC partner (financial sector sharing):

Domains:
- update-svc[.]net
- cdn-telemetry[.]io
- microsoftupdate-cdn[.]com

IPs:
- 185.234.219.47
- 91.108.56.201

File hashes (SHA-256):
- 3a7bd3e2360a3d29eea436fcfb7e44c735d117c42d1c1835420b6b9942dd4f1b
- c1c6e4b3f8a30f5a2b1d7c0e9f4e3a2b1c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2

Context: These indicators are associated with a campaign targeting financial sector
organizations using spear-phishing followed by LOLBin-based lateral movement.
Actor suspected to be FIN-category financially motivated group. No confirmed
presence in our environment but overlap with sector targeting is high.

---

### Platform

- [x] Multi-platform

---

### Hunt Mode

- [x] Analysis-Only (IOC analysis first, then recommend queries)

---

### ATT&CK Depth

- [x] Deep Mapping

---

### Confidence Floor

- [x] Strict

---

### HUNT BEGIN
```

---

## Filled Example — Query-Only (Lateral Movement via WMI)

```
## THREAT HUNTER — ENGAGEMENT INVOCATION

**Operating Charter:** hunter.md (Threat Hunter — REYES, Nikolai v1.0)

---

### Hypothesis / Objective

Build hunt queries for lateral movement via WMI (T1021.006). Focus on WMI-based
remote execution patterns — specifically wmiprvse.exe spawning child processes
on remote hosts and WMI subscriptions used for persistence.

---

### Platform

- [x] CrowdStrike LogScale (CQL)
- [x] Microsoft Sentinel (KQL)

---

### Hunt Mode

- [x] Query-Only

---

### Tone

- [x] Operational

---

### HUNT BEGIN
```

---

## Filled Example — Query + Test (Credential Dumping via LSASS)

```
## THREAT HUNTER — ENGAGEMENT INVOCATION

**Operating Charter:** hunter.md (Threat Hunter — REYES, Nikolai v1.1)

---

### Hypothesis / Objective

Build hunt queries targeting credential dumping via LSASS memory access (T1003.001).
Focus on process access patterns where a non-system process opens a handle to lsass.exe
with permissions consistent with memory reading. These queries will be considered for
promotion to standing detection rules — full test cases required.

---

### Platform

- [x] CrowdStrike LogScale (CQL)

---

### Hunt Mode

- [x] Query + Test

---

### Tone

- [x] Detailed

---

### ATT&CK Depth

- [x] Deep Mapping

---

### Special Instructions

Include edge cases for known legitimate tools that access LSASS (e.g., AV agents,
backup software, certain EDR components). Flag any logic that would require
environment-specific tuning before deployment as a detection rule.
Also include the promotion assessment (tuning, triage guidance, response action)
per the Query Testing Framework in hunter.md.

---

### HUNT BEGIN
```

---

*Threat Hunter Invocation Template — Version 1.1*
*For persona definition and full methodology, see hunter.md.*
