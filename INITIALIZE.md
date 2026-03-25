# Workspace Initialization

Initialization is handled automatically by the **workspace-initialize** skill.

Say **"initialize"** at any time to configure or reconfigure the workspace.

---

## What the Skill Does

On **first use** (no prior `CLAUDE.md`), the skill runs a full initialization:

1. Reads all five governing documents in `01_CONTEXT/`
2. Discovers all workers in `04_WORKERS/` dynamically (any folder with an `invocation-template.md`)
3. Writes session memory (`CLAUDE.md` hot cache and `memory/context/workspace.md` deep storage)
4. Audits workspace directories and creates any that are missing
5. Checks `02_INBOX/` for items to triage
6. Updates `.gitignore` and `.coworkignore` to exclude generated memory files
7. Auto-updates `QUICK-REFERENCE.md` with any new workers
8. Reports status in BLUF format

On **returning sessions** (when `CLAUDE.md` already exists), the skill runs a lighter re-orientation: loads the hot cache, re-reads all governing documents to catch edits, re-scans workers for additions or removals, checks inbox, and syncs memory only if changes are detected.

---

## Adding a New Worker

Drop a folder into `04_WORKERS/` with at minimum an `invocation-template.md`. Then say "initialize" to pick it up immediately, or it will be discovered on the next session automatically.

## Skill Location

`.claude/skills/workspace-initialize/SKILL.md`
