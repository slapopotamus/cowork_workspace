# ThreatHunter — Document Repository Index
### docs/ | Knowledge Base for REYES, Nikolai

This folder contains reference documentation used by the Threat Hunter persona when building queries, analyzing TTPs, and conducting hunt operations. When invoked, REYES draws on these documents as the authoritative knowledge base for query craft and platform specifics.

---

## Contents

| File | Topic | Status | Source |
|---|---|---|---|
| `cql-syntax.md` | CrowdStrike LogScale CQL — syntax, operators, field assignment, expressions, user parameters, saved searches, relative time, regex engine V1/V2, event types, field names, query templates, performance guide | v1.1 — updated 2026-03-23 | LogScale Skill + LogScale Docs v1.229–1.232 |
| `cql-query-examples.md` | 11 real-world CQL queries with MITRE ATT&CK context — credential dumping, brute force thresholding, base64 decode, LOLBins, lateral movement, Tor exit nodes, recon clustering, DNS staging, hidden scheduled tasks, file size analysis, impossible travel | Current | ByteRay-Labs/Query-Hub + LogScale Docs |

---

## Adding Documents

Drop new reference files into this folder and add an entry to the table above. Useful additions:

- Additional CQL function deep-dives (e.g., `cql-joins.md`, `cql-aggregations.md`)
- Platform-specific guides (e.g., `kql-sentinel.md`, `spl-splunk.md`)
- Hunt playbooks for specific adversary groups or campaigns
- IOC and TTP reference sheets
- Detection engineering standards and tuning guidelines

---

*ThreatHunter Document Repository — docs/index.md*
