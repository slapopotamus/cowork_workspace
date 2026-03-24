# Workspace Initialize Skill

**Description:** Initialize or re-orient the cybersecurity operations workspace. Triggers on: "initialize", "init", "start session", "new session", "re-orient", "returning session", "load context", "set up the workspace", "configure workspace", or any task where the workspace has not yet been initialized in the current session.

---

## Auto-Detection Logic

Before executing, determine which flow to run:

1. Check if `CLAUDE.md` exists at the workspace root.
2. Check if the user explicitly requested initialization (said "initialize", "init", "start session", "new session", "re-orient", "set up the workspace", "configure workspace", or similar).

| Condition | Flow |
|---|---|
| `CLAUDE.md` does NOT exist | **Full Initialization** |
| `CLAUDE.md` exists AND user explicitly requests initialization | **Full Initialization** (user-requested reconfigure) |
| `CLAUDE.md` exists AND user did NOT request initialization | **Returning Session** |

---

## Full Initialization Flow

Execute these six steps in order. Confirm each step completes before proceeding.

### Step 1 — Read Governing Documents

Read all five files in `01_CONTEXT/` in this exact order:

1. `01_CONTEXT/PARTNERSHIP-AGREEMENT.md` — identity, role, communication tone, scope of authority
2. `01_CONTEXT/TRUTH-PROTOCOL.md` — anti-sycophancy directive, technical accuracy rules
3. `01_CONTEXT/SECURITY_SOP.md` — scripting standards, audit checklists, query standards
4. `01_CONTEXT/RUNNING-DOCUMENT.md` — live project log, standing rules, session memory
5. `01_CONTEXT/QUICK-REFERENCE.md` — command cheat sheet for workers and workspace actions

These documents govern all behavior from this point forward. Internalize their contents fully.

### Step 2 — Discover Workers Dynamically

Scan `04_WORKERS/` for all subdirectories that contain an `invocation-template.md` file:

```bash
find 04_WORKERS/ -maxdepth 2 -name "invocation-template.md"
```

For each discovered worker:

1. Read the `invocation-template.md` file.
2. Identify persona files in the same directory — any `.md` file that is NOT `invocation-template.md` and NOT `README.md`.
3. Record for each worker:
   - **Worker name** = subdirectory name (e.g., `CyberSecurityCouncil`)
   - **Path** = `04_WORKERS/[name]/`
   - **Invocation template** = `04_WORKERS/[name]/invocation-template.md`
   - **Persona files** = list of other `.md` files found

This is convention-based discovery. Adding a new worker requires only dropping a folder into `04_WORKERS/` with an `invocation-template.md`. No skill edits required.

### Step 3 — Write Memory

Create or overwrite two memory artifacts. Use the template in `references/memory-template.md` as the structure for `CLAUDE.md`.

#### 3a. CLAUDE.md (Hot Cache) — workspace root

A compact file (~60–80 lines) containing:

- **Identity** — Hootz identity and communication style from `PARTNERSHIP-AGREEMENT.md`
- **Workspace** — table of all 6 directories and their purposes
- **Workers** — table of all discovered workers with path and quick summon syntax
- **Standing Rules** — key rules extracted from `RUNNING-DOCUMENT.md`, with pointer to full doc
- **Active Projects** — extracted from `RUNNING-DOCUMENT.md` active task section
- **Terms** — key terms table (BLUF, CQL, KQL, SPL) with pointer to `QUICK-REFERENCE.md`
- **Governing Documents** — table of all 5 docs with one-line content summary

#### 3b. memory/context/workspace.md (Deep Storage)

Create `memory/context/` directory if it doesn't exist. Write a richer file containing:

- Complete list of standing rules from `RUNNING-DOCUMENT.md`
- Full worker registry: all discovered workers with persona file paths, invocation patterns, and any supporting files
- Completed milestones history from `RUNNING-DOCUMENT.md`
- SOP section status — which sections of `SECURITY_SOP.md` are populated vs. placeholder
- Any inbox items found during initialization

Do NOT write to `memory/glossary.md`, `memory/people/`, or `memory/projects/` — those are for organic workplace knowledge. Workspace initialization context stays in `memory/context/workspace.md`.

### Step 4 — Audit Workspace Structure

Confirm all six required directories exist:

- `01_CONTEXT/`
- `02_INBOX/`
- `03_PROJECTS/`
- `04_WORKERS/`
- `05_OUTPUTS/`
- `06_BACKUP/`

If any are missing, create them and note the action in the status report.

### Step 5 — Check Inbox

List all files in `02_INBOX/` excluding `.gitkeep`. If items are present, flag them for triage.

### Step 6 — Handle .gitignore and .coworkignore

**First-time initialization only** (when `CLAUDE.md` did not previously exist):

Append the following to `.gitignore` if not already present:

```
# Session-generated memory (created by workspace-initialize skill)
CLAUDE.md
memory/
```

Append the following to `.coworkignore` if not already present:

```
# Session-generated memory
CLAUDE.md
memory/
```

This ensures memory artifacts are not committed to git and are excluded from Claude's automatic context loading (the skill loads them explicitly at the right time).

### Step 7 — Auto-Update QUICK-REFERENCE.md

Compare the list of discovered workers against the sections in `01_CONTEXT/QUICK-REFERENCE.md`:

- **New workers** (discovered but not in QUICK-REFERENCE.md): Append a new section for each using this template:

```markdown
## [Worker Name]

[One-line description extracted from invocation template header or persona file.]

**Quick Summon:**
```
[Extracted from the "Lightweight Quick Summon" or similar section of the invocation template.
If no quick summon section exists, generate a minimal one from the template's required fields.]
```

Full template: `04_WORKERS/[WorkerName]/invocation-template.md`
```

- **Removed workers** (in QUICK-REFERENCE.md but directory no longer exists in `04_WORKERS/`): Add `(REMOVED)` to the worker's heading. Do NOT delete the section — this preserves history.

### Step 8 — Report Status

Output a BLUF-formatted status report:

```
BLUF: Workspace initialized. [N] governing documents loaded, [N] workers discovered, [inbox status]. Ready for tasking.

Identity: Hootz — Cybersecurity Operations Chief of Staff
Workers:
  - [Worker 1]: [quick summon syntax]
  - [Worker 2]: [quick summon syntax]
Active task: [from RUNNING-DOCUMENT.md or "None — standing by"]
Inbox: [count and summary, or "Empty"]
Workspace integrity: [all directories present / issues noted]
```

**From this point forward, adopt the communication style defined in `PARTNERSHIP-AGREEMENT.md`:** BLUF-first, technical, direct, no preamble, no pleasantries before the BLUF.

---

## Returning Session Flow

Execute when `CLAUDE.md` exists and the user has NOT explicitly requested initialization.

### Step 1 — Load Hot Cache

Read `CLAUDE.md` for immediate context restoration.

### Step 2 — Re-read All Governing Documents

Read all five files in `01_CONTEXT/` in order:

1. `01_CONTEXT/PARTNERSHIP-AGREEMENT.md`
2. `01_CONTEXT/TRUTH-PROTOCOL.md`
3. `01_CONTEXT/SECURITY_SOP.md`
4. `01_CONTEXT/RUNNING-DOCUMENT.md`
5. `01_CONTEXT/QUICK-REFERENCE.md`

This ensures edits made between sessions are always picked up. The returning-session flow pays the same context-loading cost as full initialization — the difference is it does not overwrite memory unless changes are detected.

### Step 3 — Re-scan Workers

Run the same dynamic worker discovery from Step 2 of Full Initialization. Compare discovered workers against what is listed in `CLAUDE.md`:

- If workers have been **added**: read their invocation templates, update `CLAUDE.md`, update `QUICK-REFERENCE.md` (append new section).
- If workers have been **removed**: annotate their heading in `QUICK-REFERENCE.md` with `(REMOVED)`, update `CLAUDE.md`.

### Step 4 — Check Inbox

List any new files in `02_INBOX/` (excluding `.gitkeep`). Flag for triage if present.

### Step 5 — Sync Memory If Needed

If ANY changes were detected in Steps 2–4:

- Governing document edits (content differs from what's in current memory)
- Worker additions or removals
- Standing rule changes
- New inbox items

Then update both `CLAUDE.md` and `memory/context/workspace.md` to reflect the current state.

If nothing changed, leave memory files untouched.

### Step 6 — Report

Output a BLUF-formatted status report:

```
BLUF: Re-oriented for new session. [Summary of where we left off].

Last session: [date and milestone from RUNNING-DOCUMENT.md]
Active task: [current or "None — standing by"]
Inbox: [status]
Worker changes: [any additions/removals since last init, or "None"]
Governing doc changes: [any detected edits, or "None"]
Ready for next task.
```

**Adopt the communication style defined in `PARTNERSHIP-AGREEMENT.md` from this point forward.**

---

## Important Notes

- **Adding a new worker** requires only a new folder in `04_WORKERS/` with an `invocation-template.md`. Say "initialize" to pick it up immediately, or it is discovered automatically on the next session.
- **User-triggered reinitialization** (saying "initialize" when `CLAUDE.md` already exists) runs the Full Initialization flow from scratch. Use this after editing `PARTNERSHIP-AGREEMENT.md`, adding workers, or anytime a full reset is desired.
- **Memory is two-tier**: `CLAUDE.md` is the hot cache (~60–80 lines, fast to load), `memory/context/workspace.md` is deep storage (full details). The skill writes both; the hot cache is what gets loaded first on returning sessions.
- **All outputs go to `05_OUTPUTS/`.** This rule from `RUNNING-DOCUMENT.md` applies at all times. Nothing lands at workspace root or inside worker directories.
