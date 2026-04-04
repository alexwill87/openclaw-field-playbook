---
---
status: complete
audience: both
chapter: 04
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: en
---

# 4.9 -- WORKFLOWS.md

## Context

A documented workflow is a routine that anyone (you, another dev, another agent) can execute without guessing the steps. If the procedure exists only in your head, it dies when you change tools or when you forget.

WORKFLOWS.md is the file that contains all your standardized procedures. The agent reads it, executes it, and updates it when a step changes.

## Standardized format

Each workflow follows the same structure:

```markdown
## [Workflow name]

**Trigger:** When this workflow runs (manually, cron, event).
**Confidence level:** 1 (dry run) / 2 (with validation) / 3 (autonomous)
**Last verification:** YYYY-MM-DD

### Prerequisites
- [What must be true before starting]
- [Necessary access]

### Steps
1. [Concrete action with exact command]
2. [Next action]
3. [Next action]

### Verification
- [ ] [How to know it worked]
- [ ] [Validation test]

### If error occurs
- If [error A] : [corrective action]
- If [error B] : [corrective action]
- If unknown : stop and report.
```

## Concrete examples

### Deploy cockpit

```markdown
## Deploy cockpit

**Trigger:** Manual, after merge to main.
**Confidence level:** 2 (with validation)
**Last verification:** 2026-03-28

### Prerequisites
- Branch main is up to date (git pull)
- Local tests passed
- No deployment in progress

### Steps
1. `cd /opt/cockpit && git pull origin main`
2. `docker compose build --no-cache`
3. `docker compose down && docker compose up -d`
4. Wait 10 seconds.
5. `curl -s -o /dev/null -w "%{http_code}" http://localhost:3000`
   Expected: 200

### Verification
- [ ] curl returns 200
- [ ] `docker ps` shows the container "Up"
- [ ] Logs contain no errors: `docker logs cockpit --tail 20`

### If error occurs
- If build fails: verify dependencies in package.json.
- If container doesn't start: `docker logs cockpit` for diagnosis.
- If curl returns 502: service is taking time to start, wait 30s and retry.
- If unknown: rollback with `git checkout HEAD~1 && docker compose up -d`
```

### Create a task

```markdown
## Create a task

**Trigger:** Manual.
**Confidence level:** 3 (autonomous)
**Last verification:** 2026-03-25

### Prerequisites
- PostgreSQL access

### Steps
1. `./tasks.sh add "Task title" [priority] [project] [deadline]`
2. Confirm creation: `./tasks.sh list todo`

### Verification
- [ ] The task appears in the list with the correct status and priority.

### If error occurs
- If PostgreSQL connection fails: verify the service is running (`systemctl status postgresql`).
```

### Secret rotation

```markdown
## Secret rotation

**Trigger:** Monthly (1st of the month) or after security incident.
**Confidence level:** 2 (with validation)
**Last verification:** 2026-03-01

### Prerequisites
- Vault access
- Root/sudo access
- Maintenance window (no deployment in progress)

### Steps
1. Generate new secret: `openssl rand -hex 32`
2. Store in Vault: `vault kv put secret/[service] key=[new_secret]`
3. Update service config.
4. Restart service: `docker compose restart [service]`
5. Test service: `curl -s http://localhost:[port]/health`
6. Log rotation: `echo "$(date) [service] secret rotated" >> /var/log/secret-rotation.log`

### Verification
- [ ] Service responds correctly with the new secret.
- [ ] Old secret no longer works.
- [ ] Rotation is logged.

### If error occurs
- If service doesn't start: restore old secret from Vault (previous version).
- If unknown: do not continue with other rotations, diagnose first.
```

## Organize the file

A single WORKFLOWS.md file with a table of contents:

```markdown
# WORKFLOWS.md

## Table of contents
1. [Deploy cockpit](#deploy-cockpit)
2. [Create a task](#create-a-task)
3. [Secret rotation](#secret-rotation)
4. [Daily health check](#daily-health-check)
5. [Database backup](#database-backup)
```

When the file exceeds 500 lines, split into separate files in a `workflows/` folder.

## Common mistakes

**No "If error occurs" section.** Everything works fine until the day it breaks. Without a rollback procedure, you improvise under stress.

**Approximate commands.** "Deploy the service" instead of the exact command. If the command isn't copy-pasteable, it's not precise enough.

**Never update.** The workflow is 6 months old, paths have changed, a step was added verbally. Verify each workflow at least once a month.

## Steps

1. Create `WORKFLOWS.md` at the project root.
2. Document your most frequent workflow (the one you do every day).
3. Test: give the workflow to the agent and ask it to execute it in dry run mode.
4. Fix missing or imprecise steps.
5. Add one workflow per week until your main routines are covered.

## Verification

- [ ] WORKFLOWS.md exists and contains at least 3 workflows.
- [ ] Each workflow follows the standardized format (prerequisites, steps, verification, error).
- [ ] Commands are exact and copy-pasteable.
- [ ] Each workflow has been tested in dry run mode by the agent.
- [ ] Last verification date is filled in and recent (< 1 month).

---
