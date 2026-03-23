# Cyber Security Council

A structured multi-agent deliberation framework that simulates a panel of senior cybersecurity professionals analyzing, debating, and reaching decisions on complex security topics.

---

## What It Does

The Cyber Security Council seats 3–5 fictional expert personas — each with distinct domain expertise, biases, and priorities — and runs them through a structured four-round deliberation:

- **Round 0 (Chair):** Frames the question, identifies missing context, selects experts, names assumptions
- **Round 1:** Each expert gives their independent initial assessment
- **Round 2:** Cross-examination — experts challenge each other's claims
- **Round 3:** Rebuttals and final votes
- **Round 4 (Chair):** Synthesizes the decision record with confidence level, dissent, and open questions

The result is a decision that surfaces genuine tradeoffs, competing priorities, and explicit uncertainty — rather than a single-voice recommendation.

---

## Files

| File | Purpose |
|---|---|
| `council.md` | Operating charter, expert roster (25 personas), deliberation protocol, voting mechanics |
| `roster.md` | Quick-reference selection guide — domain, lean, best-use-case for each expert |
| `invocation-template.md` | Copy-paste prompt template for summoning the Council, with filled examples |
| `report-templates.md` | Output templates: Executive Summary, Technical Decision Record, Action Tracking Record |
| `session-log-template.md` | Template for logging completed sessions for audit and retrospective review |
| `council_orchestrator.py` | Python orchestrator for file-drop parallel execution mode (see below) |
| `sessions/index.html` | Session index viewer for your `sessions/` directory |

---

## Quick Start

### Option 1 — Paste into any Claude session

Copy the invocation block from `invocation-template.md`, fill in your topic and evidence, and submit. No setup required.

```
Summon the Cyber Security Council.
Topic: [Your question here]
Context: [Key facts, constraints, or evidence]
Mode: [Executive Brief / Analyst Roundtable / High-Conflict]
```

### Option 2 — Agentic environment (Claude Cowork / Claude Code)

Point the agent at this directory and invoke using file references. The agent reads `council.md` and `roster.md` as its operating instructions and can reference evidence files without pasting their contents directly.

### Option 3 — Parallel execution with orchestrator

Use `council_orchestrator.py` to issue each expert's Round 1 and Round 2 prompts as structurally independent calls, then feed outputs back into the next round. See `council.md` Section 15 for the parallel execution model.

---

## Expert Roster (v3.0 — 25 Personas)

The council includes standing experts across these domains:

SOC Operations · Threat Intelligence · Incident Response · Vulnerability Management · Security Architecture · Red Team · Cloud Security · Identity & Access Management · GRC & Compliance · Malware Analysis · Application Security · CISO Advisory · Cryptography & Post-Quantum · OT/ICS Security · Supply Chain Security · Privacy Engineering · AI/ML Security · Insider Threat & DLP · Cyber Legal Counsel · Security Culture & Human Risk · SRE/DevOps · Threat Hunting · Risk Quantification & Insurance · Digital Forensics & e-Discovery · Physical Security

Full persona definitions — biases, persuasion triggers, challenge patterns — are in `council.md` Section 5.

---

## Session Logs

Session logs belong in a `sessions/` directory alongside this repository. They are excluded from this repo by `.gitignore` because they may contain organizational context. The `sessions/index.html` file provides a browser-based index for navigating your local sessions.

---

## Charter Version

Current charter: **v3.0** | Roster: **v3.0 (25 personas)**
