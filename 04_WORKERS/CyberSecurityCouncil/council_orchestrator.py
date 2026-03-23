"""
Cyber Security Council — Orchestrator v3.0
==========================================
File-drop orchestration model: this script writes prompt files to queue/prompts/
and waits for corresponding output files to appear in queue/outputs/.
The consuming agent (Claude Cowork, Claude Code CLI, or any tool watching the queue)
is responsible for reading each prompt, running it against the LLM, and writing the
result back to queue/outputs/ with the same filename.

Session outputs are written to sessions/YYYY-MM-DD-topic-slug.md and the
sessions/index.html file is updated automatically.

Usage:
    python council_orchestrator.py <path_to_invocation.md>
    python council_orchestrator.py <path_to_invocation.md> --tone analyst
    python council_orchestrator.py <path_to_invocation.md> --experts 4
"""

import os
import sys
import time
import re
from datetime import datetime

# ---------------------------------------------------------------------------
# Directory layout
# ---------------------------------------------------------------------------
BASE_DIR      = os.path.dirname(os.path.abspath(__file__))
PROMPTS_DIR   = os.path.join(BASE_DIR, "queue", "prompts")
OUTPUTS_DIR   = os.path.join(BASE_DIR, "queue", "outputs")
SESSIONS_DIR  = os.path.join(BASE_DIR, "sessions")

# ---------------------------------------------------------------------------
# Filesystem helpers
# ---------------------------------------------------------------------------

def setup_directories():
    os.makedirs(PROMPTS_DIR, exist_ok=True)
    os.makedirs(OUTPUTS_DIR, exist_ok=True)
    os.makedirs(SESSIONS_DIR, exist_ok=True)


def read_file(filepath: str) -> str:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"[!] Required file not found: {filepath}")
        sys.exit(1)


def write_file(filepath: str, content: str):
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)


def write_prompt(filename: str, content: str):
    """Write a prompt file to the drop-folder for the agent to pick up."""
    filepath = os.path.join(PROMPTS_DIR, filename)
    write_file(filepath, content)
    print(f"  [>] Prompt written: {filename}")


def wait_for_output(filename: str, timeout_seconds: int = 600) -> str:
    """
    Block until the agent writes the corresponding output file.
    Returns the file content once it exists and is non-empty.
    Raises SystemExit on timeout.
    """
    filepath = os.path.join(OUTPUTS_DIR, filename)
    print(f"  [~] Waiting for: {filename} ...", end="", flush=True)
    deadline = time.time() + timeout_seconds
    while True:
        if os.path.exists(filepath):
            time.sleep(0.5)          # brief pause to ensure write is complete
            content = read_file(filepath)
            if content:
                print(f" done.")
                return content
        if time.time() > deadline:
            print(f"\n[!] Timeout after {timeout_seconds}s waiting for {filename}.")
            sys.exit(1)
        time.sleep(2)
        print(".", end="", flush=True)


# ---------------------------------------------------------------------------
# Invocation parsing helpers
# ---------------------------------------------------------------------------

def extract_section(text: str, *headers) -> str:
    """
    Try each header variant in order; return the first match.
    Supports both [REQUIRED]/[OPTIONAL] prefixed headers and plain headers.
    """
    for header in headers:
        pattern = rf"###\s+(?:\[(?:REQUIRED|OPTIONAL)\]\s+)?{re.escape(header)}(.*?)(?=###\s|---\s*$|$)"
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return ""


def parse_invocation(invocation_md: str) -> dict:
    """Extract all user-specified fields from the invocation document."""
    return {
        "topic":           extract_section(invocation_md, "Topic / Question", "Topic"),
        "context":         extract_section(invocation_md, "Available Evidence / Context",
                                           "Available Evidence", "Context"),
        "tone":            extract_section(invocation_md, "Tone Mode"),
        "execution_mode":  extract_section(invocation_md, "Execution Mode"),
        "chair_vote":      extract_section(invocation_md, "Chair Voting Behavior"),
        "domain_emphasis": extract_section(invocation_md, "Domain Emphasis"),
        "output_length":   extract_section(invocation_md, "Output Length Preference", "Output Length"),
        "expert_override": extract_section(invocation_md, "Expert Override"),
        "panel_size":      extract_section(invocation_md, "Expert Panel Size"),
        "exec_review":     extract_section(invocation_md, "Management/Executive Review Required",
                                           "Management Review Required"),
        "special":         extract_section(invocation_md, "Special Instructions"),
    }


def resolve_expert_count(parsed: dict) -> int:
    raw = parsed.get("panel_size", "")
    m = re.search(r'\d+', raw) if raw else None
    count = int(m.group()) if m else 3
    return max(2, min(count, 6))


def resolve_execution_mode(parsed: dict) -> str:
    raw = (parsed.get("execution_mode") or "").lower()
    if "parallel" in raw:
        return "Parallel (Best-Effort)"
    return "Sequential"


def resolve_tone(parsed: dict) -> str:
    raw = (parsed.get("tone") or "").lower()
    if "executive" in raw:
        return "Executive Brief"
    if "conflict" in raw or "adversarial" in raw:
        return "High-Conflict"
    return "Analyst Roundtable"   # safe default


def resolve_exec_review(parsed: dict) -> bool:
    raw = (parsed.get("exec_review") or "").lower()
    return "yes" in raw


# ---------------------------------------------------------------------------
# Prompt builders
# ---------------------------------------------------------------------------

STRUCTURED_EXPERT_FORMAT = """\
Respond using EXACTLY this structured format (use these exact section headers):

POSITION:
[Your clear recommendation or conclusion — 2–4 sentences. No hedge words without explanation.]

ASSUMPTIONS:
[List the assumptions your position depends on. Number each one. Be explicit about what you are taking for granted.]

FACTS VS. INFERENCES:
Facts (evidence we have): [list]
Inferences (what I am reading into the evidence): [list]
Unknowns (what we need but do not have): [list]

MAIN CONCERN:
[The single most important risk, gap, or problem you see in this situation — from your domain perspective.]

CHALLENGE TO ANOTHER EXPERT:
[Name the expert you are challenging, state the specific claim you dispute, explain why it is weak, and state what a stronger position would require. Be direct. "I would push back on [NAME]'s claim that..." is the expected opening.]

CONFIDENCE: [High / Medium / Low]
CONFIDENCE RATIONALE: [1–2 sentences explaining what drives or limits your confidence.]

WHAT WOULD CHANGE MY MIND:
[State the single most important piece of evidence or argument that would shift your position.]
"""

ROUND1_SUFFIX = """
NOTE: This is Round 1 (Initial Assessment). You have NOT seen other experts' positions.
Develop your position entirely from your own domain expertise and the evidence provided.
Do not be diplomatic. Do not try to balance all perspectives. State your honest assessment.
Avoid generic best-practice language ("implement defense in depth," "follow NIST guidelines")
unless you can apply it specifically to the evidence at hand.
"""

ROUND2_SUFFIX = """
NOTE: This is Round 2 (Cross-Examination). You have now seen all Round 1 positions.
Your job is to challenge, probe, and expose weaknesses — not to agree.
Your CHALLENGE TO ANOTHER EXPERT section is the most important part of this round.
Name the specific expert, name the specific claim, explain precisely why it is weak.
You may also revise your own position if a Round 1 argument genuinely persuaded you
— but you must explicitly state what changed and why.
"""

ROUND3_FORMAT = """\
Respond using EXACTLY this structured format:

REBUTTAL:
[Respond directly to the challenge(s) leveled against your position in Round 2. Accept, counter, or modify each challenge explicitly. Do not pretend challenges did not happen.]

STRONGEST ARGUMENT AGAINST MY OWN POSITION:
[Name the best argument the opposition has made. Acknowledge its strength honestly before explaining why you still hold your position — or why it has changed your view.]

REVISED POSITION (if changed):
[If your position changed from Round 1, state the new position and what specifically caused the change. If unchanged, write "Unchanged."]

FINAL VOTE:
Decision: [Your clear vote — what should be done or concluded]
Confidence: [High / Medium / Low]
Rationale: [1-sentence explanation of your final stance]
"""

ROUND3_SUFFIX = """
NOTE: This is Round 3 (Rebuttal and Final Vote). This is your final opportunity to
respond to challenges, acknowledge where opponents were right, and cast your vote.
Intellectual honesty here — admitting a good point while defending your core position —
is more credible than unconditional defense of everything you said in Round 1.
"""


def build_persona_context(council_text: str, expert_name: str) -> str:
    """
    Extract the persona block for a specific expert from council.md.
    Falls back to the full personas section if not found.
    """
    # Try to extract just that expert's block
    name_last = expert_name.split(",")[0].strip().upper() if "," in expert_name else expert_name.split()[0].upper()
    pattern = rf"### {name_last}.*?(?=---\s*\n### |---\s*\n## |\Z)"
    match = re.search(pattern, council_text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(0).strip()
    # Fallback: return the whole Section 5
    section_match = re.search(r"## 5\. Expert Roster(.*?)(?=## 6\.|\Z)", council_text, re.DOTALL)
    return section_match.group(1).strip() if section_match else council_text


def generate_round1_prompt(expert: dict, council_text: str, topic: str, context: str, special: str) -> str:
    persona = build_persona_context(council_text, expert['name'])
    special_block = f"\n\nSPECIAL INSTRUCTIONS FROM INVOKER:\n{special}" if special.strip() else ""
    return f"""\
## CYBER SECURITY COUNCIL — ROUND 1 (INITIAL ASSESSMENT)

### YOUR IDENTITY
You are {expert['name']}, {expert['role']}.
Act strictly as this persona. Your domain biases, priorities, and rhetorical style are defined below.
Do not perform balance. Do not soften your perspective to reach false middle ground.

### YOUR PERSONA DEFINITION
{persona}

### THE QUESTION BEFORE THE COUNCIL
{topic}

### AVAILABLE EVIDENCE AND CONTEXT
{context if context.strip() else "[No evidence provided. Deliberate from general domain knowledge and state explicitly what you are assuming about the environment.]"}
{special_block}

### WHAT YOU MUST DO
Provide your initial independent assessment of the question above.
{STRUCTURED_EXPERT_FORMAT}
{ROUND1_SUFFIX}
"""


def generate_round2_prompt(expert: dict, council_text: str, topic: str, context: str,
                            r1_combined: str, special: str) -> str:
    persona = build_persona_context(council_text, expert['name'])
    special_block = f"\n\nSPECIAL INSTRUCTIONS FROM INVOKER:\n{special}" if special.strip() else ""
    return f"""\
## CYBER SECURITY COUNCIL — ROUND 2 (CROSS-EXAMINATION)

### YOUR IDENTITY
You are {expert['name']}, {expert['role']}.
Act strictly as this persona. Your biases and priorities are defined below.

### YOUR PERSONA DEFINITION
{persona}

### THE QUESTION (UNCHANGED)
{topic}

### AVAILABLE EVIDENCE AND CONTEXT (UNCHANGED)
{context if context.strip() else "[No evidence provided.]"}
{special_block}

### ALL ROUND 1 POSITIONS (READ CAREFULLY BEFORE RESPONDING)
{r1_combined}

### WHAT YOU MUST DO
You have read all Round 1 positions. Now challenge, probe, and defend.
{STRUCTURED_EXPERT_FORMAT}
{ROUND2_SUFFIX}
"""


def generate_round3_prompt(expert: dict, council_text: str, topic: str, context: str,
                            r1_combined: str, r2_combined: str, special: str) -> str:
    persona = build_persona_context(council_text, expert['name'])
    special_block = f"\n\nSPECIAL INSTRUCTIONS FROM INVOKER:\n{special}" if special.strip() else ""
    return f"""\
## CYBER SECURITY COUNCIL — ROUND 3 (REBUTTAL AND FINAL VOTE)

### YOUR IDENTITY
You are {expert['name']}, {expert['role']}.
Your persona definition is below.

### YOUR PERSONA DEFINITION
{persona}

### THE QUESTION (UNCHANGED)
{topic}

### AVAILABLE EVIDENCE AND CONTEXT (UNCHANGED)
{context if context.strip() else "[No evidence provided.]"}
{special_block}

### ROUND 1 POSITIONS (REFERENCE)
{r1_combined}

### ROUND 2 CROSS-EXAMINATION (READ CAREFULLY — RESPOND TO CHALLENGES DIRECTED AT YOU)
{r2_combined}

### WHAT YOU MUST DO
{ROUND3_FORMAT}
{ROUND3_SUFFIX}
"""


def generate_chair_framing_prompt(topic: str, context: str, personas_text: str,
                                   expert_count: int, domain_emphasis: str,
                                   expert_override: str, tone: str, special: str) -> str:
    override_note = ""
    if expert_override.strip():
        override_note = f"""
### EXPERT OVERRIDE
The invoker has requested these specific experts: {expert_override}
You MUST select these experts unless they are not found in the roster.
You still owe a brief rationale for why each is appropriate for this question.
"""
    emphasis_note = ""
    if domain_emphasis.strip():
        emphasis_note = f"""
### DOMAIN EMPHASIS REQUESTED BY INVOKER
{domain_emphasis}
Factor this into your expert selection and framing.
"""
    special_block = f"\n### SPECIAL INSTRUCTIONS\n{special}" if special.strip() else ""

    expert_rows = "\n".join([f"EXPERT_{i+1}_NAME: [Last name, First name from roster]" for i in range(expert_count)])
    expert_roles = "\n".join([f"EXPERT_{i+1}_ROLE: [Exact role title from roster]" for i in range(expert_count)])

    return f"""\
## CYBER SECURITY COUNCIL — CHAIR FRAMING (ROUND 0)

You are the Chair of the Cyber Security Council.
Your role is to frame the deliberation, not to advocate for a position.
Tone mode for this session: {tone}

### THE QUESTION AS POSED
{topic}

### AVAILABLE EVIDENCE AND CONTEXT
{context if context.strip() else "[No evidence provided by invoker. Note this explicitly in your framing.]"}
{emphasis_note}{override_note}{special_block}

### FULL EXPERT ROSTER (for selection)
{personas_text}

### YOUR MANDATORY TASKS

**Task 1 — Restate the decision precisely.**
Convert the topic above into a precise decision statement: what specific question must the council
answer, and in what form (yes/no, recommended action, risk rating, prioritized options, etc.)?
If the question is ambiguous, name the ambiguity and state how you are resolving it.

**Task 2 — Identify missing context.**
List any context that would materially improve the council's confidence but was NOT provided.
Be specific (e.g., "No asset inventory provided — experts will need to assume exposure scope").

**Task 3 — Name key assumptions.**
List the assumptions the council must operate under given the available evidence.
These are not guesses — they are the working premises that define the decision space.

**Task 4 — Identify the central tension.**
In 1–2 sentences, name the core tradeoff or conflict this decision forces.
(e.g., "Speed of containment versus evidence preservation," or "Business continuity versus compliance deadline.")

**Task 5 — Select experts with explicit rationale.**
Select exactly {expert_count} experts from the roster.
For each, state: (a) their name and role, (b) why they are relevant to this specific question,
and (c) the specific type of friction or contrasting viewpoint they will contribute.
At least one expert must represent a non-technical perspective (business, risk, legal, compliance)
unless the question is purely technical and scope-limited.

**Task 6 — Open the session.**
Write 1–3 sentences formally opening the session and posing the question to the panel.

### OUTPUT FORMAT (use EXACTLY these labels)

DECISION_STATEMENT: [Precise rephrasing of the decision to be made]

MISSING_CONTEXT:
- [item]
- [item]

KEY_ASSUMPTIONS:
- [assumption]
- [assumption]

CENTRAL_TENSION: [1–2 sentence statement of the core tradeoff]

{expert_rows}
{expert_roles}
EXPERT_1_RATIONALE: [Why selected + what friction they bring]
EXPERT_2_RATIONALE: [Why selected + what friction they bring]
{"EXPERT_3_RATIONALE: [Why selected + what friction they bring]" if expert_count >= 3 else ""}
{"EXPERT_4_RATIONALE: [Why selected + what friction they bring]" if expert_count >= 4 else ""}
{"EXPERT_5_RATIONALE: [Why selected + what friction they bring]" if expert_count >= 5 else ""}
{"EXPERT_6_RATIONALE: [Why selected + what friction they bring]" if expert_count >= 6 else ""}

SESSION_OPENING: [1–3 sentences opening the session]
"""


def generate_chair_synthesis_prompt(topic: str, context: str, execution_mode: str, tone: str,
                                     experts: list, full_transcript: str, chair_vote: str) -> str:
    expert_list = ", ".join([f"{e['name']} ({e['role']})" for e in experts])
    chair_votes_note = ""
    if "yes" in chair_vote.lower() or "vote" in chair_vote.lower():
        chair_votes_note = """
### CHAIR VOTE
The invoker has configured the Chair to cast a vote in addition to moderating.
After reviewing the transcript, cast your own vote in the same format as the experts:
CHAIR_VOTE_DECISION: [Your recommendation]
CHAIR_VOTE_CONFIDENCE: [High / Medium / Low]
CHAIR_VOTE_RATIONALE: [1-sentence justification]
Include this in the decision record below.
"""

    return f"""\
## CYBER SECURITY COUNCIL — CHAIR SYNTHESIS (ROUND 4)

You are the Chair of the Cyber Security Council.
Your role now is to synthesize the full deliberation into a formal, auditable decision record.
You do NOT invent expert positions. You synthesize what was actually argued.
{chair_votes_note}
### SESSION METADATA
Topic: {topic}
Experts: {expert_list}
Execution Mode: {execution_mode}
Tone Mode: {tone}

### ORIGINAL QUESTION
{topic}

### ORIGINAL EVIDENCE AND CONTEXT
{context if context.strip() else "[No evidence was provided.]"}

### FULL DELIBERATION TRANSCRIPT
{full_transcript}

### YOUR MANDATORY TASKS

**Task 1 — Tally the votes from Round 3.**
Extract each expert's FINAL VOTE from the transcript. Record each vote.

**Task 2 — Determine the outcome type.**
- Unanimous Consensus: all experts voted the same way
- Majority Decision: majority agree, minority dissents (record the dissent fully)
- Split Decision: no majority; present options with their rationales
- No-Confidence: evidence was insufficient to support a defensible conclusion
- Provisional Action Under Uncertainty: risk is high, deferral is not viable,
  but confidence is limited — state what would trigger reassessment

**Task 3 — Summarize what the cross-examination changed.**
Identify 2–3 specific insights that emerged from Round 2 or Round 3 that meaningfully
shaped or challenged the final decision. Name the specific claims and counter-claims.

**Task 4 — Name the strongest dissenting argument.**
Even in a consensus outcome, name the strongest argument that was raised against the
majority position. Future decision-makers should know what was considered and why it lost.

**Task 5 — Produce the formal decision record.**

### REQUIRED OUTPUT FORMAT (use EXACTLY these section headers)

## CYBER SECURITY COUNCIL — DECISION RECORD

**Date:** {datetime.now().strftime("%Y-%m-%d")}
**Topic:** {topic}
**Experts Seated:** {expert_list}
**Execution Mode:** {execution_mode}
**Tone Mode:** {tone}

---

### VOTE TALLY
[List each expert's final vote: Name — Decision — Confidence]

### OUTCOME TYPE
[Unanimous Consensus / Majority Decision / Split Decision / No-Confidence / Provisional Action]

---

### DECISION
[Full decision statement — what the council recommends or concludes. 2–4 sentences.]

### OUTCOME RATIONALE
[Why this outcome won. Summarize the argument chain from evidence to conclusion.
Include the strongest arguments on both sides. 2–4 paragraphs.]

### DISSENT
[If Majority or Split: full statement of the minority position, its reasoning, and why it matters.
If Consensus: "None. Note the strongest counterargument raised: [brief statement]"]

### AGGREGATE CONFIDENCE
Level: [High / Medium / Low]
Rationale: [What drives or limits aggregate confidence — 2–3 sentences]

### KEY CROSS-EXAMINATION INSIGHTS
- [Insight 1: specific claim, who challenged it, and what changed as a result]
- [Insight 2]
- [Insight 3 — optional]

### EVIDENCE GAPS
[What the council lacked and would have changed confidence or the decision itself]
- [Gap 1]
- [Gap 2]

### ASSUMPTIONS THIS DECISION RESTS ON
- [Assumption 1]
- [Assumption 2]

### IMMEDIATE ACTIONS
1. [Action] — Suggested Owner: [Role] — Timeline: [Timeframe]
2. [Action] — Suggested Owner: [Role] — Timeline: [Timeframe]
3. [Action] — Suggested Owner: [Role] — Timeline: [Timeframe]

### REVIEW TRIGGER CONDITIONS
This decision should be revisited if:
- [Condition 1]
- [Condition 2]
- [Condition 3]

### OPEN QUESTIONS
[What could not be determined. For each: the question and what evidence would resolve it.]
1. [Question] — Resolved by: [Evidence needed]
2. [Question] — Resolved by: [Evidence needed]
"""


def generate_exec_review_prompt(final_decision: str, topic: str) -> str:
    return f"""\
## CYBER SECURITY COUNCIL — MANAGEMENT / EXECUTIVE REVIEW (ROUND 5)

You are the Enterprise Chief Information Security Officer (CISO) and chair of the IT Risk Committee.
You represent the management layer. Your role is not to re-litigate the technical analysis —
the Council's technical experts have done that work. Your role is to evaluate:
- Whether the recommendation is business-feasible given budget, staffing, and timeline
- Whether the risk posture it creates is acceptable to the organization
- Whether the recommendation aligns with regulatory obligations and board risk appetite
- What conditions or constraints must accompany approval

### COUNCIL TECHNICAL DECISION RECORD
{final_decision}

### TOPIC
{topic}

### YOUR OUTPUT (use EXACTLY these section headers)

## MANAGEMENT REVIEW — EXECUTIVE AUTHORIZATION

**AUTHORIZATION:** [Approved / Rejected / Accepted Risk / Approved with Conditions]

**EXECUTIVE RATIONALE:**
[2–3 paragraphs. Explain the business reasoning behind your authorization decision.
Include: what risk is being accepted, what budget/timeline implications exist,
what you are conditionally requiring if "Approved with Conditions," and
what the organization communicates to the board or to regulators about this decision.]

**CONDITIONS (if applicable):**
- [Condition 1 — specific and actionable]
- [Condition 2]

**ESCALATION THRESHOLD:**
[State the specific condition that would require this decision to be escalated to the board
or to an external advisor — e.g., "If a second incident occurs within 30 days" or
"If remediation cost exceeds $X or timeline exceeds Y weeks."]
"""


# ---------------------------------------------------------------------------
# Parsing helpers for Chair output
# ---------------------------------------------------------------------------

def parse_chair_selection(selection_output: str, expert_count: int) -> list:
    """
    Extract expert names and roles from Chair framing output.
    Returns list of {"name": str, "role": str} dicts.
    """
    experts = []
    for i in range(1, expert_count + 1):
        name_match = re.search(rf"EXPERT_{i}_NAME:\s*(.+)", selection_output, re.IGNORECASE)
        role_match = re.search(rf"EXPERT_{i}_ROLE:\s*(.+)", selection_output, re.IGNORECASE)
        if name_match and role_match:
            experts.append({
                "name": name_match.group(1).strip(),
                "role": role_match.group(1).strip(),
            })

    # Fallback: try legacy "EXPERT N: Name - Role" format
    if len(experts) != expert_count:
        experts = []
        for line in selection_output.split('\n'):
            m = re.match(r"EXPERT[\s_]?\d+\s*:\s*(.+?)\s*[-–]\s*(.+)", line)
            if m:
                experts.append({"name": m.group(1).strip(), "role": m.group(2).strip()})

    return experts


def extract_field(text: str, *field_names) -> str:
    """Extract a labeled field value from structured output."""
    for field in field_names:
        pattern = rf"(?:^|\n){re.escape(field)}\s*[:：]\s*(.+?)(?=\n[A-Z_]+[:：]|\n##|\Z)"
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return ""


# ---------------------------------------------------------------------------
# Session log writer
# ---------------------------------------------------------------------------

def write_session_log(filepath: str, topic: str, date_str: str, execution_mode: str,
                       tone: str, chair_vote_str: str, experts: list,
                       chair_framing: str, full_transcript: str, final_decision: str):
    """
    Write a complete session log file. The full transcript is NOT truncated —
    it is the primary audit record.
    """
    expert_table = "\n".join([
        f"| {e['name']} | {e['role']} | (see Chair framing for rationale) |"
        for e in experts
    ])

    content = f"""\
# CYBER SECURITY COUNCIL — SESSION LOG
**Session ID:** {os.path.basename(filepath).replace('.md', '')}
**Date:** {date_str}
**Topic:** {topic}
**Execution Mode:** {execution_mode}
**Tone Mode:** {tone}
**Chair Voted:** {"Yes" if "yes" in chair_vote_str.lower() else "No"}

---

## Experts Seated

| Expert | Role | Selection Rationale |
|---|---|---|
{expert_table}

---

## Chair Framing (Round 0)

{chair_framing}

---

## Decision Record

{final_decision}

---

## Full Deliberation Transcript (Audit Record)

{full_transcript}

---

## Retrospective *(complete after decision is acted on)*

**Date reviewed:** [YYYY-MM-DD]
**Decision acted on?** [Yes / No / Partially]
**Decision validated?** [Correct / Partially correct / Incorrect / Too early to assess]
**What happened:** [Brief description of outcomes]
**What the council got right:** [Aspects that proved accurate]
**What the council got wrong:** [Aspects that proved incorrect or overstated]
**Lessons for future sessions:** [Process, selection, or framing improvements]

---

*Session logged automatically by council_orchestrator.py v3.0*
*Template version: 3.0 — Cyber Security Council*
"""
    write_file(filepath, content)


# ---------------------------------------------------------------------------
# HTML index updater
# ---------------------------------------------------------------------------

def update_html_index(index_html_path: str, date_str: str, filename: str,
                       topic: str, experts: list, outcome: str, confidence: str):
    """Append a new row to sessions/index.html."""
    if not os.path.exists(index_html_path):
        print(f"  [!] index.html not found at {index_html_path} — skipping index update.")
        return

    html_content = read_file(index_html_path)
    if "<!-- ROWS_END -->" not in html_content:
        print(f"  [!] index.html missing <!-- ROWS_END --> marker — skipping index update.")
        return

    # Confidence badge CSS class
    conf_class = ""
    cl = confidence.lower()
    if "high"   in cl: conf_class = "confidence-High"
    elif "medium" in cl: conf_class = "confidence-Medium"
    elif "low"  in cl: conf_class = "confidence-Low"

    expert_names = ", ".join([e['name'].split(",")[0] for e in experts])
    topic_short  = (topic[:70] + "...") if len(topic) > 70 else topic

    new_row = f"""                <tr>
                    <td>{date_str}</td>
                    <td><a href="./{filename}">{filename}</a></td>
                    <td>{topic_short}</td>
                    <td>{expert_names}</td>
                    <td><span class="badge">{outcome}</span></td>
                    <td><span class="badge {conf_class}">{confidence}</span></td>
                </tr>
                <!-- ROWS_END -->"""

    updated_html = html_content.replace("<!-- ROWS_END -->", new_row)
    write_file(index_html_path, updated_html)
    print(f"  [*] index.html updated.")


# ---------------------------------------------------------------------------
# Main orchestration loop
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("\nUsage: python council_orchestrator.py <path_to_invocation.md>")
        sys.exit(1)

    setup_directories()
    invocation_file = sys.argv[1]

    # Load core framework files
    council_md  = read_file(os.path.join(BASE_DIR, "council.md"))
    roster_md   = read_file(os.path.join(BASE_DIR, "roster.md"))
    invocation_md = read_file(invocation_file)

    # Parse invocation
    parsed = parse_invocation(invocation_md)
    topic           = parsed["topic"]
    context         = parsed["context"]
    expert_count    = resolve_expert_count(parsed)
    execution_mode  = resolve_execution_mode(parsed)
    tone            = resolve_tone(parsed)
    exec_review_req = resolve_exec_review(parsed)
    chair_vote_str  = parsed.get("chair_vote", "")
    special         = parsed.get("special", "")
    domain_emphasis = parsed.get("domain_emphasis", "")
    expert_override = parsed.get("expert_override", "")

    if not topic:
        print("[!] Could not parse a Topic from the invocation file. "
              "Ensure the file has a '### Topic / Question' or '### [REQUIRED] Topic / Question' section.")
        sys.exit(1)

    # Extract the roster / personas section from council.md
    section5_match = re.search(r"## 5\. Expert Roster(.*?)(?=## 6\.|\Z)", council_md, re.DOTALL)
    personas_text  = section5_match.group(1).strip() if section5_match else council_md

    print(f"\n{'='*60}")
    print(f"  CYBER SECURITY COUNCIL — SESSION START")
    print(f"{'='*60}")
    print(f"  Topic   : {topic[:80]}{'...' if len(topic)>80 else ''}")
    print(f"  Experts : {expert_count}")
    print(f"  Mode    : {execution_mode}  |  Tone: {tone}")
    print(f"  Exec Rev: {'Yes' if exec_review_req else 'No'}")
    print(f"{'='*60}\n")

    # ------------------------------------------------------------------
    # Round 0 — Chair Framing + Expert Selection
    # ------------------------------------------------------------------
    print("[ROUND 0] Chair framing and expert selection...")
    chair_framing_prompt = generate_chair_framing_prompt(
        topic=topic, context=context, personas_text=personas_text,
        expert_count=expert_count, domain_emphasis=domain_emphasis,
        expert_override=expert_override, tone=tone, special=special
    )
    write_prompt("00_chair_framing.md", chair_framing_prompt)
    chair_framing_output = wait_for_output("00_chair_framing.md")

    experts = parse_chair_selection(chair_framing_output, expert_count)
    if len(experts) != expert_count:
        print(f"\n[!] Could not parse {expert_count} experts from Chair output.")
        print(f"    Parsed {len(experts)}: {experts}")
        print(f"    Check 00_chair_framing.md output for correct EXPERT_N_NAME / EXPERT_N_ROLE labels.")
        sys.exit(1)

    print(f"\n  Experts selected:")
    for e in experts:
        print(f"    • {e['name']} — {e['role']}")
    print()

    # ------------------------------------------------------------------
    # Round 1 — Independent Initial Assessments
    # ------------------------------------------------------------------
    print("[ROUND 1] Independent initial assessments...")
    for i, exp in enumerate(experts):
        p = generate_round1_prompt(exp, council_md, topic, context, special)
        write_prompt(f"01_expert{i+1}_round1.md", p)

    r1_outputs = []
    for i, exp in enumerate(experts):
        out = wait_for_output(f"01_expert{i+1}_round1.md")
        r1_outputs.append(f"=== {exp['name'].upper()} — ROUND 1 ===\n{out}")
    r1_combined = "\n\n".join(r1_outputs)

    # ------------------------------------------------------------------
    # Round 2 — Cross-Examination
    # ------------------------------------------------------------------
    print("\n[ROUND 2] Cross-examination...")
    for i, exp in enumerate(experts):
        p = generate_round2_prompt(exp, council_md, topic, context, r1_combined, special)
        write_prompt(f"02_expert{i+1}_round2.md", p)

    r2_outputs = []
    for i, exp in enumerate(experts):
        out = wait_for_output(f"02_expert{i+1}_round2.md")
        r2_outputs.append(f"=== {exp['name'].upper()} — ROUND 2 ===\n{out}")
    r2_combined = "\n\n".join(r2_outputs)

    # ------------------------------------------------------------------
    # Round 3 — Rebuttal + Final Vote
    # ------------------------------------------------------------------
    print("\n[ROUND 3] Rebuttal and final votes...")
    for i, exp in enumerate(experts):
        p = generate_round3_prompt(exp, council_md, topic, context,
                                    r1_combined, r2_combined, special)
        write_prompt(f"03_expert{i+1}_round3.md", p)

    r3_outputs = []
    for i, exp in enumerate(experts):
        out = wait_for_output(f"03_expert{i+1}_round3.md")
        r3_outputs.append(f"=== {exp['name'].upper()} — ROUND 3 / FINAL VOTE ===\n{out}")
    r3_combined = "\n\n".join(r3_outputs)

    # Full transcript (not truncated — this is the audit record)
    full_transcript = (
        f"## ROUND 1 — INITIAL ASSESSMENTS\n\n{r1_combined}\n\n"
        f"## ROUND 2 — CROSS-EXAMINATION\n\n{r2_combined}\n\n"
        f"## ROUND 3 — REBUTTAL AND FINAL VOTES\n\n{r3_combined}"
    )

    # ------------------------------------------------------------------
    # Round 4 — Chair Synthesis
    # ------------------------------------------------------------------
    print("\n[ROUND 4] Chair synthesis...")
    synth_prompt = generate_chair_synthesis_prompt(
        topic=topic, context=context, execution_mode=execution_mode,
        tone=tone, experts=experts, full_transcript=full_transcript,
        chair_vote=chair_vote_str
    )
    write_prompt("04_chair_synthesis.md", synth_prompt)
    final_decision = wait_for_output("04_chair_synthesis.md")

    # ------------------------------------------------------------------
    # Round 5 — Management / Executive Review (optional)
    # ------------------------------------------------------------------
    if exec_review_req:
        print("\n[ROUND 5] Management / executive review...")
        exec_prompt = generate_exec_review_prompt(final_decision, topic)
        write_prompt("05_management_review.md", exec_prompt)
        mgmt_decision = wait_for_output("05_management_review.md")
        final_decision += f"\n\n---\n\n{mgmt_decision}"

    # ------------------------------------------------------------------
    # Write session log
    # ------------------------------------------------------------------
    date_str = datetime.now().strftime("%Y-%m-%d")
    # Build a URL-safe slug from the topic
    slug_raw = re.sub(r'[^a-zA-Z0-9\s]', '', topic[:40]).strip()
    slug = re.sub(r'\s+', '-', slug_raw).lower().strip('-')
    filename = f"{date_str}-{slug}.md"
    filepath = os.path.join(SESSIONS_DIR, filename)

    write_session_log(
        filepath=filepath, topic=topic, date_str=date_str,
        execution_mode=execution_mode, tone=tone, chair_vote_str=chair_vote_str,
        experts=experts, chair_framing=chair_framing_output,
        full_transcript=full_transcript, final_decision=final_decision
    )
    print(f"\n  [+] Session log written: sessions/{filename}")

    # ------------------------------------------------------------------
    # Update HTML index
    # ------------------------------------------------------------------
    # Best-effort extraction of outcome and confidence for the index row
    outcome    = extract_field(final_decision, "OUTCOME TYPE")  or "Unknown"
    confidence = extract_field(final_decision, "Level")         or \
                 extract_field(final_decision, "AGGREGATE CONFIDENCE", "CONFIDENCE") or "Unknown"
    # Strip markdown bold markers if present
    outcome    = re.sub(r'\*+', '', outcome).strip()
    confidence = re.sub(r'\*+', '', confidence).strip()

    index_html_path = os.path.join(SESSIONS_DIR, "index.html")
    update_html_index(index_html_path, date_str, filename, topic, experts, outcome, confidence)

    print(f"\n{'='*60}")
    print(f"  SESSION COMPLETE")
    print(f"  Decision record: sessions/{filename}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
