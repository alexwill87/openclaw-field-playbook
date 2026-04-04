---
---
status: complete
audience: both
chapter: 04
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: en
---

# 4.11 -- Trust is a configuration

## Context

Trust in your agent is not a feeling. It's a configuration. Every action has a risk level, and every risk level has rules. If you don't write them down, you'll swing between too much trust ("do everything") and not enough ("show me everything").

Steinberg proposes a pyramid: the riskier the action, the stricter the control.

## The rights pyramid

### Level 0: read-only

The agent can read but cannot modify anything.

Actions: consult files, read logs, display statuses, perform calculations.

Control: none necessary. Zero risk.

```
Examples:
- cat, ls, docker ps, git log
- SELECT on the database
- Read the documentation
```

### Level 1: reversible actions

The agent can act, but the action is easily undoable.

Actions: create files, write to a temporary file, create a git branch, add a task.

Control: the agent acts and reports back. You verify afterward.

```
Examples:
- git checkout -b feature/xxx
- Create a file in /tmp
- INSERT in the tasks table
- Write a draft
```

### Level 2: consequential actions

The agent can act but must request validation before.

Actions: modify config files, deploy a service, modify the database, send a message.

Control: the agent proposes the exact action and waits for an explicit "go".

```
Examples:
- docker compose restart
- UPDATE/DELETE on the database
- Modify .env or docker-compose.yml
- git push
- Send a Telegram message to a third party
```

### Level 3: forbidden actions

The agent can NEVER do this, even with validation.

Actions: delete unrecoverable production data, push --force to main, modify secrets without procedure, expose credentials.

Control: forbidden in the boundary prompt (section 4.12). The agent must refuse even if you ask.

```
Examples:
- DROP TABLE in production
- git push --force origin main
- Display a password in plain text in logs
- Modify firewall rules
- Delete a backup
```

## Write the levels in CONSTITUTION.md

Create a `CONSTITUTION.md` file that defines the levels explicitly:

```markdown
# CONSTITUTION.md — Trust levels

## Level 0: read-only (free)
- Read any project file
- Consult logs
- SELECT queries on the database
- Display statuses

## Level 1: reversible (act + report)
- Create non-critical files
- Create git branches
- Add tasks
- Generate drafts

## Level 2: consequential (ask before)
- Modify configuration files
- Deploy a service
- Modify the database (UPDATE, DELETE)
- Push to a branch
- Send communications

## Level 3: forbidden (always refuse)
- DROP TABLE / DELETE without WHERE
- Push --force to main
- Modify secrets outside procedure
- Expose credentials
- Delete backups
- Modify firewall rules
```

Add to the system prompt:

```
Read and respect CONSTITUTION.md for trust levels.
```

## Evolve the levels

The levels are not fixed. When a workflow has been tested and works well for a month, you can lower its control level:

- Cockpit deployment: level 2 -> level 1 (after 10 successful deployments).
- Secrets rotation: remains level 2 (inherent risk, no shortcuts).
- Health check: level 1 -> level 0 equivalent (automatic cron).

Document each level change with the date and reason in CONSTITUTION.md.

## Common mistakes

**No levels defined.** The agent improvises. Sometimes it asks, sometimes it acts. Inconsistent and stressful.

**Everything at level 2.** Every action requires validation. You spend your time validating things with no risk. Decision fatigue.

**Levels exist but are not applied.** CONSTITUTION.md exists but the system prompt doesn't reference it. The agent doesn't read it.

**Lower the level too quickly.** A workflow works 3 times and you make it autonomous. 3 successes don't prove reliability. Minimum 10 executions without problems.

## Steps

1. List the 10 most frequent actions of your agent.
2. Classify each one in a level (0, 1, 2, 3).
3. Create `CONSTITUTION.md` with this classification.
4. Add the reference in the system prompt.
5. Test for 2 weeks: does the agent respect the levels?
6. Adjust if necessary.

## Verification

- [ ] CONSTITUTION.md exists with the 4 levels defined.
- [ ] Each frequent action is classified in a level.
- [ ] The system prompt references CONSTITUTION.md.
- [ ] Level 3 contains at least 5 explicit prohibitions.
- [ ] Level changes are dated and justified.

---
