# Cowork Workspace — Cybersecurity Operations

A structured AI-powered workspace for cybersecurity operations, threat hunting, detection engineering, and security advisory work. Built to run with Claude (Cowork mode) as a persistent, context-aware operations partner.

---

## What This Is

This workspace gives Claude a defined role, operating standards, and a set of specialized workers to execute cybersecurity tasks with precision and consistency. Once initialized, Claude reads the governing documents in `01_CONTEXT/` and operates as a dedicated cybersecurity operations partner for the session.

The workspace is scoped to:
- Threat hunting and detection engineering
- Security advisory and risk prioritization
- Query development (CQL, KQL, SPL)
- Scripting (PowerShell, Python, Bash)
- Audit and compliance work
- Incident response support

All behavior is governed by the documents in `01_CONTEXT/`.

---

## Getting Started

See `INITIALIZE.md` at the root of this workspace. Copy the initialization prompt, paste it into Claude (Cowork mode) with this folder selected, and the session will bootstrap itself automatically.

---

## Folder Structure

```
01_CONTEXT/         Governing documents, SOPs, and session memory
02_INBOX/           Incoming tasks, briefs, and raw intelligence to be triaged
03_PROJECTS/        Active project tracking and work in progress
04_WORKERS/         AI worker agents and their supporting files
05_OUTPUTS/         All deliverables, reports, session logs, and artifacts
06_BACKUP/          Workspace snapshots (zip archives, not committed to git)
```

---

## Workers

### Cyber Security Council
A structured multi-expert deliberation framework for high-stakes security decisions. The Council seats domain experts drawn from a standing roster, deliberates through structured rounds, and delivers a reasoned decision with dissent preserved.

Use it for: vulnerability triage, architecture decisions, incident attribution, risk prioritization, threat assessment, and any decision that benefits from adversarial challenge before you commit.

Invocation template: `04_WORKERS/CyberSecurityCouncil/invocation-template.md`
Session outputs: `05_OUTPUTS/CybersecurityCouncilSessions/`

### Threat Hunter (REYES, Nikolai)
A hypothesis-driven threat hunting agent with full ATT&CK methodology, multi-platform query development (CQL, KQL, SPL), and built-in test case generation. REYES works from IOCs, behavioral observations, or threat intelligence and delivers hunt packages ready for analyst review or promotion to standing detections.

Outputs are delivered as paired `.md` and `.html` files.

Invocation template: `04_WORKERS/ThreatHunter/invocation-template.md`
Hunt outputs: `05_OUTPUTS/ThreatHunter/`

---

## Quick Commands

| Command | What it does |
|---|---|
| `backup` | Zips the workspace and saves it to `06_BACKUP/` with today's date |
| `Summon the Cyber Security Council` | Opens a Council session with your topic and context |
| `Invoke the Threat Hunter` | Engages REYES for a hypothesis-driven hunt or query build |

Full quick reference: `01_CONTEXT/QUICK-REFERENCE.md`

---

## Governing Documents

| Document | Purpose |
|---|---|
| `PARTNERSHIP-AGREEMENT.md` | Defines the operating relationship, scope, and communication standards |
| `TRUTH-PROTOCOL.md` | Anti-sycophancy directive; accuracy over agreeableness |
| `SECURITY_SOP.md` | PowerShell scripting standards, CrowdStrike audit checklists, query and reporting standards |
| `RUNNING-DOCUMENT.md` | Live project log and session memory; updated after every major task |
| `QUICK-REFERENCE.md` | Command cheat sheet for all workers and workspace actions |

---

## Output Routing

All deliverables go to `05_OUTPUTS/`. Nothing lands at workspace root or inside worker directories.

Backup archives go to `06_BACKUP/` and are excluded from git. The folder structure is tracked; the zip files are not.
