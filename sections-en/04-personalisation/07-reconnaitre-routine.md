---
---
status: complete
audience: both
chapter: 04
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: en
---

# 4.7 -- Recognizing a routine

## Context

A routine is an action you repeat with the same pattern. Deploying a service, creating a backup, checking the morning logs. When you do the same thing for the 3rd time, that's a signal: it could be automated or delegated to the agent.

But not everything. Some routines need your human judgment. The art is distinguishing between the two.

## Criteria for an automatable routine

A task is a candidate for automation if it meets these 3 conditions:

1. **Repetition.** It occurs 3+ times with the same pattern.
2. **Predictability.** The steps are the same each time, or variations are known in advance.
3. **Low risk.** If the agent makes a mistake, the consequences are reversible or minor.

### Examples of good candidates

- Daily health check: same commands, same interpretation, alert if down.
- Generate a weekly summary of tasks: read-only, no action.
- Log rotation: delete files > 30 days old, same rule each time.
- Create a commit with standardized format: same structure, same convention.

### Examples of poor candidates

- Responding to a client email: each situation is different, tone matters.
- Deciding to postpone a deadline: human context required (fatigue, business priorities, relationships).
- Choosing between two architectures: subtle trade-offs, no universal right answer.
- Deleting production data: irreversible, high risk.

## How to detect your routines

### Method 1: the logbook

For one week, note every action you take with your agent. Format:

```
Monday:
- VPS health check (5 min)
- Cockpit deployment (10 min)
- Reply to client email X (15 min)
- Update TASKS.md (3 min)

Tuesday:
- VPS health check (5 min)
- Debug API error (30 min)
- Update TASKS.md (3 min)
```

After a week, the repetitions jump out at you. Health check and TASKS.md come back every day = routines.

### Method 2: ask the agent

```
Analyze my 20 most recent conversations with you.
Which actions come up 3+ times?
For each one, tell me if it follows a predictable pattern.
```

The agent sees patterns you don't see because you're in the middle of them.

## The gray zone: routines with judgment

Some tasks are repetitive but require judgment at one stage:

- **Task triage**: repetitive, but prioritization requires human context.
- **Code review**: the format is predictable, but quality evaluation is subjective.
- **Reporting**: data collection is automatable, interpretation is not.

For these, the right approach is to break it down: automate the mechanical part, keep the human judgment.

```
Routine "morning triage":
- [AGENT] List active tasks, sort by deadline.
- [AGENT] Flag delays and blockers.
- [HUMAN] Decide today's priorities.
- [AGENT] Update statuses according to the decision.
```

## Common mistakes

**Automate everything.** Just because it's possible doesn't mean it's desirable. Some routines keep you connected to the reality of your project.

**Automate nothing.** Out of fear of losing control. Start with zero-risk tasks (read-only, reporting) to build confidence.

**Automate without documenting.** The agent does the routine but no one knows exactly what it does. If the agent changes or you switch tools, the routine is lost. See section 4.9.

## Steps

1. Keep a logbook for 5 days.
2. Identify actions that come up 3+ times.
3. For each one, evaluate: predictable? low risk?
4. Classify: automatable / semi-automatable / human only.
5. Start with the simplest and least risky routine.

## Verification

- [ ] At least 3 routines identified.
- [ ] Each routine evaluated on the 3 criteria (repetition, predictability, risk).
- [ ] Routines with judgment are broken down (agent part / human part).
- [ ] The first automated routine is zero-risk.
