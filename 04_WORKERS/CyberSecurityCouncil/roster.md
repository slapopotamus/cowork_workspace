# CYBER SECURITY COUNCIL — EXPERT ROSTER
### Quick-Reference Selection Guide | Version 2.0

---

## How to Use This File

This file is a quick-reference companion to `council.md`. Use it when selecting experts for a session. Each entry summarizes a roster member's domain, their core lean, and the tension they bring. Full persona definitions with complete bias profiles are in `council.md` Section 5.

**Canonical source:** Full persona definitions (biases, challenge patterns, persuasion triggers, mistake-catching) are maintained exclusively in `council.md` Section 5. This file is a derived quick-reference. When any discrepancy exists between the two files, `council.md` is authoritative.

---

## Full Roster — At a Glance

| Name | Role | Domain | Lean | Best Used When |
|---|---|---|---|---|
| **CALLOWAY, Marcus** | SOC Operations Lead / Detection Engineering | Detection, alert triage, SIEM | Operational realist; skeptical of unvalidated coverage claims | Detection coverage is in question; SOC workload is a factor |
| **VANCE, Priya** | Threat Intelligence Analyst | TI, attribution, TTP mapping | Cautious attributer; actor-context focused | Attribution is in play; TTPs need adversary context |
| **OKAFOR, Demi** | Incident Response Lead | IR, forensics, containment | Action-biased; impatient with over-deliberation | Active or suspected compromise; containment decisions |
| **BRENNAN, Cole** | Vulnerability Management & Exposure Engineering | Vuln triage, EPSS, patch strategy | Risk-contextualist; pushes back on CVSS fixation | Patching priority; exploit likelihood; attack surface decisions |
| **HARTLEY, Simone** | Security Architect | Architecture, segmentation, ZT design | Structural over tactical; framework-oriented | Control design; long-term risk reduction; systemic gaps |
| **CROSS, Eliot** | Red Team Lead / Adversary Simulation | Offensive research, control validation | Chronically pessimistic; kills false confidence | Validating defensive assumptions; stress-testing coverage |
| **NAKAMURA, Yuki** | Cloud Security Engineer | Cloud IAM, CSPM, cloud-native detection | Cloud-native purist; skeptical of on-prem security models | Cloud environment decisions; misconfiguration risk; cloud IR |
| **ABARA, Kwame** | Identity & Access Management Architect | IAM, PAM, MFA, identity threat detection | Identity-as-perimeter; excessive privilege hawk | Credential attacks; identity-based lateral movement; IAM strategy |
| **CHEN, Margaret** | Governance, Risk & Compliance Director | GRC, regulatory frameworks, audit readiness | Compliance-framed; liability-conscious | Regulatory exposure; risk documentation; audit defensibility |
| **FROST, Daniel** | Malware Analyst / Reverse Engineer | RE, sandbox analysis, C2 infrastructure | Completionist; delays action for full characterization | Malware classification; eradication confidence; implant analysis |
| **VASQUEZ, Renata** | Application Security Lead / Product Security | AppSec, SDLC, supply chain, API security | Shift-left advocate; skeptical of perimeter mitigations | Application-layer vulnerabilities; SDLC; third-party library risk |
| **OSEI, Nana** | CISO Advisor / Enterprise Security Risk | Executive risk, security investment, M&A | Business-impact translator; organizational realist | Executive communication; investment decisions; board-level risk |
| **VORONOV, Aleksei** | Applied Cryptographer / Quantum Security Strategist | Cryptography, PQC, PKI, HSM strategy, crypto-agility | Urgency-biased on crypto risk; dismissive of operational complexity as a reason to delay | Cryptographic migration; post-quantum readiness; PKI architecture; algorithm selection; harvest-now-decrypt-later risk |
| **IBRAHIM, Tariq** | OT/ICS Security Engineer | OT/SCADA, ICS safety, IEC 62443, IT/OT convergence | Safety-first; resistant to IT-centric security approaches in OT environments | OT/ICS incidents; IT/OT convergence decisions; industrial control system architecture |
| **NAVARRO, Lucia** | Supply Chain Security & Third-Party Risk Manager | Vendor risk, SBOM, supply chain integrity, CI/CD pipeline | Sees supply chain risk everywhere; slow to trust vendors without verification | Vendor compromise; supply chain attacks; third-party risk decisions; software composition risk |
| **LINDSTRÖM, Maja** | Privacy Engineer / Data Protection Officer | GDPR, CCPA, privacy-by-design, breach notification, data classification | Privacy-first framer; skeptical of security monitoring that creates surveillance risk | Breach notification; data protection decisions; privacy-vs-security tradeoffs; cross-border data handling |
| **VALDEZ, Sofia** | AI/ML Security Strategist | LLM security, prompt injection, ML pipeline integrity, AI data governance | Views unvetted AI integration as data exfiltration risk; skeptical of wrapper-based security | AI service adoption; custom LLM deployment; securing AI features; prompt injection risk |
| **HOLLOWAY, Jackson** | Insider Threat & Data Loss Prevention Lead | UBA, DLP architecture, IP protection, employee investigations | Suspicious of "trusted" users; prioritizes data restriction over frictionless productivity | Data exfiltration; employee offboarding risk; unauthorized access by authorized users |
| **AL-FASSI, Nura** | Cyber Legal Counsel & Incident Response Attorney | SEC materiality, attorney-client privilege, breach notification law, regulatory defense | Views security through legal defensibility; risk-averse about written statements | Regulatory defense; incident liability; breach notification; public communications |
| **GALLAGHER, Finn** | Security Culture & Human Risk Lead | Behavioral nudges, usability vs. security, anti-phishing, security champion programs | Defends user experience; rejects controls requiring perfect human behavior | Security awareness; friction reduction; shadow IT drivers; policy usability |
| **CHANG, David** | Site Reliability Engineer / DevOps | Uptime, CI/CD pipeline stability, infrastructure-as-code, deployment velocity | Prioritizes availability and speed; rejects high-latency security tools | Emergency patching impact; CI/CD security friction; prod-breaking changes |
| **KASONGO, Elise** | Threat Hunter / Detection Researcher | Hypothesis-driven hunting, behavioral analytics, ATT&CK coverage, telemetry gap analysis | Assumes compromise until disproven; dismissive of purely reactive detection | Detection validation; hunt-driven gap analysis; adversary persistence discovery |
| **MORAN, Patrick** | Cyber Risk Quantification & Insurance Strategist | FAIR methodology, ALE modeling, cyber insurance analysis, Monte Carlo risk modeling | Demands dollar figures; skeptical of qualitative risk ratings | Security budget justification; insurance coverage gaps; risk transfer decisions |
| **DRAPER, Keiko** | Digital Forensics & e-Discovery Specialist | Disk/memory forensics, chain of custody, court-admissible analysis, forensic imaging | Will delay containment to preserve evidence; treats every incident as potentially litigated | Evidence preservation; forensic imaging; e-discovery; litigation support |
| **REEVES, Anton** | Physical Security & Convergence Specialist | Badge systems, CCTV, social engineering defense, physical pentesting, IT/physical convergence | Believes physical security is massively underinvested; skeptical of cloud-only strategies | Facility access; social engineering defense; physical-cyber convergence |

---

## Expert Selection Matrix

Use this matrix to quickly identify which experts are most relevant by topic category. Select 2–3 from the most relevant row, ensuring viewpoint diversity.

### Incident Response / Active Compromise
**Primary:** OKAFOR, FROST, CALLOWAY
**Add for tension:** VANCE (attribution caution), CHEN (regulatory exposure), OSEI (business impact)

### Threat Intelligence / Attribution
**Primary:** VANCE, FROST, CROSS
**Add for tension:** CALLOWAY (actionability), OKAFOR (containment urgency), CHEN (attribution documentation risk)

### Detection Engineering / SOC Optimization
**Primary:** CALLOWAY, CROSS, VANCE
**Add for tension:** HARTLEY (architecture gaps), NAKAMURA (cloud telemetry), OSEI (investment context)

### Vulnerability Triage / Patch Prioritization
**Primary:** BRENNAN, CALLOWAY, CROSS
**Add for tension:** HARTLEY (systemic control gaps), CHEN (compliance deadlines), OKAFOR (active exploitation risk)

### Security Architecture / Zero Trust Design
**Primary:** HARTLEY, ABARA, NAKAMURA
**Add for tension:** CROSS (will it actually work?), CALLOWAY (operational feasibility), OSEI (cost and org reality)

### Cloud Security
**Primary:** NAKAMURA, ABARA, HARTLEY
**Add for tension:** CROSS (cloud attack surface), CHEN (compliance in cloud), BRENNAN (cloud misconfiguration exposure)

### Identity / IAM / Credential Attacks
**Primary:** ABARA, NAKAMURA, CROSS
**Add for tension:** OKAFOR (active identity compromise), CALLOWAY (detection of identity attacks), CHEN (access governance)

### Malware Analysis
**Primary:** FROST, VANCE, OKAFOR
**Add for tension:** CALLOWAY (detection operationalization), CROSS (evasion assumptions), BRENNAN (vulnerability context)

### GRC / Compliance / Regulatory
**Primary:** CHEN, OSEI, HARTLEY
**Add for tension:** CALLOWAY (compliance vs. operational reality), VASQUEZ (product security obligations), BRENNAN (risk quantification)

### Application / Product Security
**Primary:** VASQUEZ, HARTLEY, BRENNAN
**Add for tension:** CROSS (exploitability validation), CHEN (regulatory obligations), CALLOWAY (runtime detection gaps)

### Red Team / Purple Team / Control Validation
**Primary:** CROSS, CALLOWAY, HARTLEY
**Add for tension:** VANCE (threat context), OKAFOR (IR readiness), OSEI (business risk of findings)

### Strategic Security Investment / Vendor Decisions
**Primary:** OSEI, CHEN, HARTLEY
**Add for tension:** CALLOWAY (operational reality), CROSS (will it stop an attacker?), NAKAMURA (technology fit)

### Cryptography / PKI / Post-Quantum Readiness
**Primary:** VORONOV, HARTLEY, CHEN
**Add for tension:** OSEI (business feasibility and migration cost), CROSS (cryptographic control validation), NAKAMURA (cloud PKI and key management)

### OT/ICS Security / Industrial Control Systems
**Primary:** IBRAHIM, HARTLEY, CALLOWAY
**Add for tension:** CROSS (OT attack simulation and exploitation reality), CHEN (IEC 62443 compliance), OSEI (safety vs. security investment tradeoffs)

### Supply Chain Security / Third-Party Risk
**Primary:** NAVARRO, VASQUEZ, CHEN
**Add for tension:** CROSS (supply chain attack validation), BRENNAN (dependency vulnerability and patch exposure), OSEI (vendor relationship management and contract leverage)

### Privacy & Data Protection
**Primary:** LINDSTRÖM, CHEN, ABARA
**Add for tension:** OKAFOR (breach response urgency vs. notification timing), CALLOWAY (monitoring effectiveness vs. privacy constraints), OSEI (regulatory cost and reputational risk)

### AI/ML Security & Generative AI Risks
**Primary:** VALDEZ, VASQUEZ, CHEN
**Add for tension:** CROSS (prompt injection attack validation), HARTLEY (AI architecture integration), LINDSTRÖM (AI data privacy and model training compliance)

### Insider Threat & Data Exfiltration
**Primary:** HOLLOWAY, ABARA, CALLOWAY
**Add for tension:** LINDSTRÖM (employee privacy vs. monitoring), OSEI (HR friction and business impact), OKAFOR (speed of response to authorized user exfil)

### Executive, Legal & Organizational Risk
**Primary:** OSEI, AL-FASSI, CHEN
**Add for tension:** OKAFOR (IR speed vs. legal caution), HARTLEY (architectural cost vs. budget), GALLAGHER (usability vs. policy rigor)

### Application Security & DevOps Friction
**Primary:** VASQUEZ, CHANG, NAVARRO
**Add for tension:** OSEI (time-to-market business pressure), CROSS (proving exploitability of findings), CHEN (compliance blocking deployments)

### Proactive Threat Hunting & Detection Validation
**Primary:** KASONGO, CALLOWAY, VANCE
**Add for tension:** CROSS (red team TTPs vs. hunt hypotheses), FROST (malware indicators as hunt seeds), NAKAMURA (cloud telemetry gaps and cloud-native logging coverage)

### Digital Forensics, Litigation & Evidence
**Primary:** DRAPER, AL-FASSI, OKAFOR
**Add for tension:** FROST (malware RE methodology), HOLLOWAY (insider investigation evidence), LINDSTRÖM (privacy constraints on forensic collection)

### Risk Quantification & Insurance
**Primary:** MORAN, OSEI, CHEN
**Add for tension:** AL-FASSI (legal liability framing vs. financial modeling), HARTLEY (architectural cost justification), NAKAMURA (cloud cost modeling and cloud-specific risk quantification)

### Physical Security & Social Engineering
**Primary:** REEVES, HOLLOWAY, GALLAGHER
**Add for tension:** ABARA (physical badge vs. logical access convergence), CROSS (physical penetration testing), OKAFOR (physical breach incident response)

---

## Adversarial Pairing Guide

Use these pairings when you want guaranteed productive conflict:

| Pairing | Nature of Tension |
|---|---|
| OKAFOR + VANCE | Speed vs. context — IR wants to move; TI wants attribution first |
| CROSS + HARTLEY | Does it actually work vs. is it architecturally sound? |
| CHEN + OKAFOR | Compliance documentation vs. incident speed |
| CALLOWAY + HARTLEY | Operational workload vs. structural correctness |
| BRENNAN + OKAFOR | Measured patching pace vs. IR urgency |
| FROST + OKAFOR | Complete analysis vs. get it contained now |
| CROSS + OSEI | Adversarial reality vs. business communication |
| ABARA + CALLOWAY | Identity-as-perimeter vs. detection-first operations |
| VORONOV + OSEI | Cryptographic urgency vs. business feasibility and migration cost |
| IBRAHIM + OKAFOR | OT safety-first caution vs. IR containment speed |
| NAVARRO + BRENNAN | Supply chain risk maximalism vs. risk-based prioritization |
| LINDSTRÖM + CALLOWAY | Privacy constraints on monitoring vs. security visibility needs |
| LINDSTRÖM + OKAFOR | Breach notification compliance obligations vs. incident containment speed |
| VORONOV + CROSS | Theoretical cryptographic risk horizon vs. empirical exploitation reality |

---

## Roster Growth Log

| Version | Change |
|---|---|
| 1.0 | Initial roster (12): CALLOWAY, VANCE, OKAFOR, BRENNAN, HARTLEY, CROSS, NAKAMURA, ABARA, CHEN, FROST, VASQUEZ, OSEI |
| 2.0 | Added 4 personas: VORONOV (Cryptography/PQC), IBRAHIM (OT/ICS), NAVARRO (Supply Chain), LINDSTRÖM (Privacy/DPO). Added topic categories: Cryptography/PKI/PQC, OT/ICS, Supply Chain, Privacy. Added 6 adversarial pairings. Established council.md as canonical persona source. |
| 2.1 | Added 12 personas: VALDEZ (AI/ML Security), HOLLOWAY (Insider Threat/DLP), AL-FASSI (Cyber Legal), GALLAGHER (Security Culture/Human Risk), CHANG (SRE/DevOps), KASONGO (Threat Hunter), MORAN (Risk Quantification/Insurance), DRAPER (Digital Forensics/e-Discovery), REEVES (Physical Security). Added topic categories: AI/ML Security, Insider Threat, Executive/Legal/Org Risk, DevOps Friction, Threat Hunting, Digital Forensics, Risk Quantification, Physical Security. Added adversarial pairings. |
| 3.0 | Fixed stale THIEL references (replaced with NAKAMURA in selection matrix). Corrected role titles for AL-FASSI, GALLAGHER, CHANG, KASONGO, MORAN, DRAPER, REEVES for consistency with council.md. Updated charter reference to v3.0. |

---

*Cyber Security Council Expert Roster — Version 3.0*
*For full persona definitions, see council.md Section 5.*
*For session invocation instructions, see invocation-template.md.*
*For operating charter, see council.md (v3.0).*
