# SESSION LOG — POST-QUANTUM CRYPTOGRAPHY READINESS
### Cyber Security Council | 2026-03-19

---

## Session Record

**Date:** 2026-03-19
**Session ID:** 2026-03-19-post-quantum-cryptography
**Topic:** Should our organization begin planning and implementing quantum-resistant encryption now, or should we wait until standards, vendor support, and enterprise adoption mature further?
**Invocation Mode:** Informal (Quick Summon — full template not used)
**Execution Mode:** Parallel Agents (partial — see compliance note below)
**Parallel Compliance:** Non-compliant. Two of three experts (VORONOV, THIEL) ran as independent agents. ANAND's positions were written as context text by the orchestrator and fed to the other agents' prompts in Rounds 1 and 3. Rule P2 (Symmetric Instantiation) was not fully satisfied. Session output is high quality but cannot be declared fully parallel-compliant.
**Tone Mode:** Analyst Roundtable
**Chair Voted:** No

---

## Experts Seated

*Note: This session pre-dated V2.0 roster. All three experts were custom personas not drawn from the standing roster. The cryptography persona (VORONOV) has since been canonicalized in the V2.0 roster.*

| Expert | Role | Why Selected |
|---|---|---|
| VORONOV, Aleksei (custom) | Applied Cryptographer / Quantum Security Strategist | Primary domain expertise — PQC standards, ML-KEM/ML-DSA, harvest-now-decrypt-later threat modeling |
| ANAND, Priya (custom) | VP Enterprise Risk & Compliance | Business/risk/compliance representation required per Section 4, criterion 3 |
| THIEL, Marcus (custom) | Principal Enterprise Architect | Infrastructure migration reality — HSM constraints, PKI dependency mapping, operational risk of premature deployment |

**Chair:** Dr. Miriam Osei-Bonsu (custom) — synthesized and moderated final session record.

---

## Decision Record

```
DECISION:      Begin now with structured, phased implementation. Immediate action on
               software-backed PKI and subordinate CAs where vendor support exists.
               Extract vendor HSM roadmap commitments contractually by Q3 2026.
               Defer root CA migration until HSM vendor delivery is confirmed.

OUTCOME TYPE:  Consensus (3–0)

CONFIDENCE:    High on direction and phasing. Moderate on execution timelines,
               pending HSM vendor delivery commitments.

RATIONALE:     All three experts converged on immediate structured action after
               cross-examination resolved apparent tension between urgency (VORONOV),
               compliance/risk pressure (ANAND), and operational readiness (THIEL).
               The debate reframed from "act now vs. wait" to "what must we do to
               remain capable of migrating when it matters?" CRQC timeline uncertainty
               does not neutralize the harvest-now-decrypt-later threat. Vendor
               procurement lead times do not compress on demand — delay in beginning
               vendor conversations translates directly into delay in migration capability.

DISSENT:       None. All three experts voted for immediate structured action with
               phased, conditional deployment. THIEL registered a process dissent:
               the recommendation must carry equal weight for "act with rigor" as
               for "act with urgency" — premature deployment without inventory is
               worse than a careful staged approach.

CAVEATS:       Decision rests on: (1) HSM vendors shipping ML-DSA support on
               committed timelines; (2) CRQC not arriving materially earlier than
               the 2030–2035 range most assessments cite; (3) organization having
               capacity to execute inventory and vendor engagement in parallel.

OPEN QUESTIONS:
               1. When will HSM vendors (Thales, YubiKey, Entrust) ship field-deployable
                  ML-DSA for root CA and OCSP signing? → Resolved by Q3 2026 vendor RFI responses.
               2. Will certificate chain length overflow require architectural changes
                  in existing TLS infrastructure? → Resolved by Q3 2026 pilot data.
               3. Will cyber liability carriers begin formally excluding PQC readiness?
                  → Monitor renewal cycles; not yet documented as of session date.

NEXT STEPS:
               1. Cryptographic asset inventory — map all key material, CA hierarchies,
                  HSM dependencies. Owner: Security Architecture. Timeline: Q2 2026.
               2. Issue RFIs to all PKI/HSM vendors requiring ML-DSA/ML-KEM delivery
                  timelines per component type. Owner: Procurement + Security. Timeline: Q2 2026.
               3. Make PQC roadmap maturity a hard procurement criterion by Q3 2026.
                  Owner: Procurement. Timeline: Q3 2026.
               4. Pilot hybrid ML-DSA signing on one low-risk software-backed subordinate CA.
                  Owner: PKI team. Timeline: Q3 2026.
               5. Publish quarterly crypto-agility metrics to security and compliance.
                  Owner: GRC. Timeline: Q3 2026 baseline, then quarterly.
```

---

## Key Cross-Examination Insights

- **CRQC timeline uncertainty does not neutralize urgency.** VORONOV's initial claim of high urgency was challenged by ANAND (who demanded a specific intelligence assessment) and THIEL (who challenged the "manageable" framing of HSM constraints). VORONOV correctly rebutted: the asymmetry between migration lead time and threat emergence timeline means timeline uncertainty is itself an argument for beginning sooner, not later.

- **Priya's insurance argument was dismantled — and she conceded it.** ANAND initially cited cyber liability carriers as a driver of urgency. THIEL challenged her to name a single renewal exclusion for PQC readiness. She could not. She dropped the argument and pivoted to documented risk drivers. This was the most important position revision in the session — a risk-based argument built on anticipated rather than observed risk was correctly pruned.

- **Marcus's "12–18 months" sequencing was exposed as potentially indistinct from waiting.** VORONOV challenged THIEL's "prepare then deploy" framing by pointing out that if vendor conversations are deferred to Q4 2027 and the vendor then says "support ships in 2029," the organization has made a binding migration decision by inaction. THIEL accepted this and revised to "prepare while extracting vendor commitments as a condition of continued procurement" — a meaningful shift.

---

## Evidence Gaps Identified

- No declassified intelligence assessment naming a specific threat actor with CRQC capability on a defined planning horizon. Absence of specific evidence is not absence of threat, but it limits board-level urgency arguments.
- No documented cyber liability exclusions for PQC readiness as of session date. This argument should be revisited at each renewal cycle.
- HSM vendor delivery timelines unconfirmed — this is the binding operational constraint. Q3 2026 RFI responses will resolve it.

---

## Retrospective *(to be completed after implementation)*

**Date reviewed:** [TBD]
**Decision acted on?** [TBD]
**Decision validated?** [TBD]
**What happened:** [TBD]
**What the council got right:** [TBD]
**What the council got wrong:** [TBD]
**Lessons for future sessions:** Parallel agent execution was requested mid-session rather than specified at invocation. This created orchestration ambiguity that resulted in partial non-compliance with Rule P2. Future parallel sessions should use the full invocation template with Execution Mode: Parallel Agents specified upfront.

---

*Session logged by: Council Chair (Dr. Miriam Osei-Bonsu, custom)*
*Retroactively logged 2026-03-19 as first entry in council session registry*
*Template version: 2.0 — Cyber Security Council*
