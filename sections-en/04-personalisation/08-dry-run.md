---
---
status: complete
audience: both
chapter: 04
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: en
---

# 4.8 -- Dry run before trust

## Context

You've identified an automatable routine (section 4.7). Before letting it run autonomously, you test it. Not because you don't trust the agent — because you don't trust your own instructions.

The dry run reveals holes in your procedures. Better to discover them in test mode than in production.

## The 3 levels of trust

### Level 1: read-only ("show me")

The agent executes the routine but does nothing. It displays what it would do.

```
Prompt: "Do the health check in dry run mode. 
Show me each command you would run and what you would verify,
but don't execute anything."
```

Expected result:

```
Health check dry run:
1. I would run: docker ps --format "{{.Names}} {{.Status}}"
   I would verify: all containers are "Up"
2. I would run: curl -s -o /dev/null -w "%{http_code}" http://localhost:3000
   I would verify: code 200
3. I would run: df -h /
   I would verify: usage < 80%
4. If there's a problem, I would send a Telegram alert.

No action executed. Dry run mode.
```

You validate: are the commands correct? Are the thresholds good? Is something missing?

### Level 2: action + validation ("do and show")

The agent executes but asks for validation before each consequential action.

```
Prompt: "Do the health check. Execute the diagnostics.
If everything is OK, tell me. If something is not OK, show me 
what you would do but wait for my validation before acting."
```

This is the training mode. The agent does the diagnostic work (with no risk), but takes no corrective action without your approval.

### Level 3: autonomous ("do everything")

The agent executes the full routine, takes corrective actions if necessary, and reports afterward.

```
Prompt: "Daily health check. If a service is down, 
restart it. If disk exceeds 80%, clean up logs older than 30 days. 
Send me the summary via Telegram."
```

You only move to level 3 when levels 1 and 2 have worked without issues for at least one week.

## The trust escalation timeline

| Week | Level | What you do |
|---|---|---|
| 1 | Read-only | Verify each command. Fix procedures. |
| 2 | Action + validation | Let the agent diagnose. Validate corrections. |
| 3 | Autonomous with report | Agent acts alone but you read the report daily. |
| 4+ | Silent autonomous | Agent acts alone and only reports anomalies. |

This timeline is a minimum. For high-risk routines (deployment, data deletion), double each phase.

## Test prompt

To test a routine before automating it:

```
I want to automate this routine: [description].
Planned steps:
1. [step 1]
2. [step 2]
3. [step 3]

Execute in dry run mode. For each step:
- Show the exact command.
- Tell me what you verify.
- Tell me what you would do if the result is abnormal.
Don't execute anything.
```

## Common mistakes

**Jumping straight to level 3.** "This looks simple, no need to test." Then the agent restarts the wrong container or deletes the wrong logs. Always test.

**Getting stuck at level 1.** You've been doing dry runs for 3 months without ever taking action. Dry run is a transition tool, not a permanent mode.

**Not documenting findings.** The dry run reveals that your procedure is missing a step. You correct it verbally but not in the workflow. Next time, same error. Write corrections into WORKFLOWS.md (section 4.9).

## Steps

1. Choose a routine identified in section 4.7.
2. Request a dry run (level 1).
3. Verify: correct commands? Good thresholds? Missing steps?
4. Fix the procedure if necessary.
5. Move to level 2 for one week.
6. If all is OK, move to level 3.

## Verification

- [ ] Every new routine goes through level 1 before execution.
- [ ] Dry run findings are documented in WORKFLOWS.md.
- [ ] Moving to the next level is based on at least one week without issues.
- [ ] High-risk routines have a doubled trust escalation timeline.
