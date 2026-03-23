# Workspace Initialization

## First Time Setup

Copy the prompt below and paste it into Claude with this workspace folder selected. Claude will read all governing documents, configure itself for the session, and confirm it is ready to operate.

You only need to do this once per session. At the start of future sessions, a shorter re-orientation prompt is provided below.

---

## First Session Prompt

```
You are opening a structured cybersecurity operations workspace for the first time.

Please do the following in order:

1. Read all files in 01_CONTEXT/ — specifically PARTNERSHIP-AGREEMENT.md, TRUTH-PROTOCOL.md, SECURITY_SOP.md, RUNNING-DOCUMENT.md, and QUICK-REFERENCE.md. These documents define your role, communication standards, operating rules, and the current state of the workspace.

2. Read 04_WORKERS/CyberSecurityCouncil/invocation-template.md and 04_WORKERS/ThreatHunter/invocation-template.md so you understand how to invoke each worker.

3. Audit the workspace structure and confirm all expected directories are present: 01_CONTEXT, 02_INBOX, 03_PROJECTS, 04_WORKERS, 05_OUTPUTS, 06_BACKUP.

4. Check 02_INBOX/ for any files waiting to be triaged. If files are present, list them. If empty, note that.

5. Report back with:
   - A confirmation that all context documents have been read
   - Your understanding of your role and operating standards in 2-3 sentences
   - Current workspace status (active projects, inbox items, any anomalies)
   - Standing by for first task

Adopt the communication style defined in PARTNERSHIP-AGREEMENT.md from this point forward, including BLUF formatting for all substantive responses.
```

---

## Returning Session Prompt

Use this at the start of any subsequent session to re-orient quickly without a full re-read.

```
Re-orienting for a new session. Please:

1. Read RUNNING-DOCUMENT.md in 01_CONTEXT/ to get current project status and standing rules.
2. Check 02_INBOX/ for anything new.
3. Confirm you are ready and summarize where we left off.
```

---

## Notes for New Users

**Customizing the identity.** The `PARTNERSHIP-AGREEMENT.md` file defines how Claude communicates and what it focuses on. Edit the role description, tone, and scope sections to match your environment and preferences before your first session.

**The RUNNING-DOCUMENT.md is your session memory.** Claude does not automatically remember previous sessions. The running document carries context forward. Update it at the end of any session where meaningful work was done.

**Output routing.** Everything Claude produces goes into `05_OUTPUTS/`. Subdirectories are created per worker or project. Do not save deliverables anywhere else.

**Backups.** Say `backup` at any time and Claude will zip the workspace and save it to `06_BACKUP/` with today's date. Backup archives are excluded from git.

**Adding workers.** Drop a new worker folder into `04_WORKERS/` with a `hunter.md` or equivalent persona file and an `invocation-template.md`. Reference it in `QUICK-REFERENCE.md` and update `README.md`.
