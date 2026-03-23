# Quick Reference — Workspace Commands
**Last Updated:** 2026-03-23

A fast-access cheat sheet for all available commands and invocations.

---

## Workspace Commands

| Say this... | What happens |
|---|---|
| `backup` | Zips the full workspace and drops it in `06_BACKUP/` with today's date |

---

## Cyber Security Council

Summons a panel of cybersecurity experts to deliberate on a question or decision.

**Quick Summon** (minimal input, sensible defaults):
```
Summon the Cyber Security Council.
Topic: [Your question]
Context: [Key facts, constraints, or evidence]
Mode: [Executive Brief / Analyst Roundtable / High-Conflict]
```

**Modes:**
- `Executive Brief` — condensed, decision-focused (~400–800 words)
- `Analyst Roundtable` — full deliberation, deep reasoning (~1,000–2,500 words) *(default)*
- `High-Conflict` — adversarial, stress-test focused (~1,500–3,000+ words)

**Execution Modes:**
- `Sequential` — experts deliberate in a single session *(default)*
- `Parallel` — each expert is prompted in isolation per round; stronger independence

**Optional controls:** expert override by last name (e.g., `Seat: CALLOWAY, VANCE, CHEN`), chair voting, management/executive review layer, output length (Short / Standard / Full).

Full template: `04_WORKERS/CyberSecurityCouncil/invocation-template.md`
Roster: `04_WORKERS/CyberSecurityCouncil/roster.md`
Session outputs: `05_OUTPUTS/CybersecurityCouncilSessions/`

---

## Threat Hunter (REYES, Nikolai)

Engages the Threat Hunter for hypothesis-driven hunts, IOC analysis, and query development.

**Quick Summon:**
```
Invoke the Threat Hunter.
Hypothesis: [What adversary behavior are you hunting?]
Evidence: [IOCs, observed behaviors, or threat intel]
Platform: [CQL / KQL / SPL]
Mode: [Full Hunt / Query-Only / Analysis-Only]
```

**Hunt Modes:**
- `Full Hunt` — complete five-phase engagement *(default)*
- `Full Hunt + Test` — full hunt with a test suite for every query
- `Query-Only` — queries only, no analysis or report
- `Query + Test` — queries with full TP/TN/edge case test suite
- `Analysis-Only` — analyze IOCs/TTPs, no query development
- `Report-Only` — produce a hunt report from findings already provided

**Platforms:** CrowdStrike LogScale (CQL) *(default)*, Microsoft Sentinel (KQL), Splunk (SPL), Multi-platform

**Output format:** All ThreatHunter outputs are delivered as `.md` + `.html` file pairs in `05_OUTPUTS/ThreatHunter/`

Full template: `04_WORKERS/ThreatHunter/invocation-template.md`

---

## Output Routing

All deliverables go to `05_OUTPUTS/`. Never at workspace root or inside worker directories.

| Output Type | Destination |
|---|---|
| Council session logs | `05_OUTPUTS/CybersecurityCouncilSessions/` |
| ThreatHunter outputs | `05_OUTPUTS/ThreatHunter/` *(`.md` + `.html` pairs)* |
| Backups | `06_BACKUP/` |
