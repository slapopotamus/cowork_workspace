# Workspace Initialization

## First Time Setup

Copy the prompt below and paste it into Claude (Cowork mode) with this folder selected. Claude will read all governing documents, configure itself for the session, rebuild its memory, and confirm it is ready to operate.

You only need to do this once per session. A shorter returning session prompt is provided below for subsequent sessions.

---

## First Session Prompt

```
You are opening a structured cybersecurity operations workspace. Please do the following in order and confirm each step is complete before moving to the next.

1. Read all five files in 01_CONTEXT/ in this order:
   - PARTNERSHIP-AGREEMENT.md
   - TRUTH-PROTOCOL.md
   - SECURITY_SOP.md
   - RUNNING-DOCUMENT.md
   - QUICK-REFERENCE.md

   These documents define your role, communication standards, operating rules, standing commands, and the current state of the workspace. They govern all behavior from this point forward.

2. Read the invocation templates for both workers:
   - 04_WORKERS/CyberSecurityCouncil/invocation-template.md
   - 04_WORKERS/ThreatHunter/invocation-template.md

3. Rebuild session memory. Write the following to your memory system so this context persists across sessions:
   - Your role and operating scope as defined in PARTNERSHIP-AGREEMENT.md
   - The standing rules from RUNNING-DOCUMENT.md (output routing, backup procedure, ThreatHunter file format)
   - The location and purpose of each worker

4. Audit the workspace and confirm all six directories are present: 01_CONTEXT, 02_INBOX, 03_PROJECTS, 04_WORKERS, 05_OUTPUTS, 06_BACKUP.

5. Check 02_INBOX/ for any files waiting to be triaged. List them if present.

6. Report back with:
   - Confirmation all context documents have been read
   - A 2-3 sentence summary of your role and how you will operate
   - Workspace status: active projects, inbox items, anything that needs attention
   - Ready for first task

Adopt the communication style defined in PARTNERSHIP-AGREEMENT.md from this point forward, including BLUF formatting for all substantive responses.
```

---

## Returning Session Prompt

Use this at the start of any subsequent session to re-orient quickly.

```
Re-orienting for a new session. Please:

1. Read 01_CONTEXT/RUNNING-DOCUMENT.md to get current project status and standing rules.
2. Check 02_INBOX/ for anything new since last session.
3. Summarize where we left off and confirm ready for next task.
```

---

## Notes for New Users

**Customize the identity first.** Before your first session, open `01_CONTEXT/PARTNERSHIP-AGREEMENT.md` and edit the role description, scope, and tone to match your environment and preferences. This is what shapes how Claude communicates for every session.

**RUNNING-DOCUMENT.md is your session memory.** Claude does not retain memory between sessions automatically. This file carries context forward. Update it at the end of any session where meaningful work was done.

**All outputs go to 05_OUTPUTS/.** Nothing lands at workspace root or inside worker directories. Subdirectories are created per worker or project type.

**Backups are one word.** Say `backup` at any time and Claude will zip the full workspace and drop it in `06_BACKUP/` with today's date. Zip archives are excluded from git.

**Adding workers.** Drop a new worker folder into `04_WORKERS/` with a persona file (e.g. `hunter.md`) and an `invocation-template.md`. Reference it in `01_CONTEXT/QUICK-REFERENCE.md` and update `README.md`.

**The archive folder in CyberSecurityCouncil is intentional.** It holds prior implementation documents and is excluded from Claude's context via `.coworkignore` to keep sessions clean.
