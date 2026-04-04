---
---
status: complete
audience: both
chapter: 04
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: en
---

# 4.5 -- How Tasks Get Done

## Context

Having a task system isn't enough. What matters is the workflow: who proposes what, who decides, who executes. If you don't define this workflow, the agent will either do everything without asking (dangerous) or do nothing without being told (useless).

The right balance, according to the Steinberg model: the agent proposes, you decide.

## The propose/decide workflow

### 1. The agent proposes

The agent analyzes current tasks, deadlines, context. It proposes:

```
Hello. 3 priority tasks today:

1. [URGENT] S3 Migration — 2 days overdue. 
   Proposal: finish the transfer script, test, deploy.

2. [NORMAL] API /users documentation — no deadline, but blocking dev onboarding.
   Proposal: generate skeleton from code, you complete it.

3. [INFO] SSL certificate expires in 43 days.
   Proposal: schedule renewal for next week.

What first?
```

### 2. You decide

You don't validate everything at once. You triage:

- "1: yes, start with the script."
- "2: not today."
- "3: add to next week's planning."

This is triage. The agent does the prep work (analyze, prioritize, formulate). You keep the judgment (decide, prioritize according to your real constraints).

### 3. The agent executes and reports

After validation, the agent executes and updates the status:

```
S3 Migration: transfer script complete. 
Restore test: OK (3 files, 12s).
Status updated: in_progress -> done.

Next task?
```

## Triage without delegating judgment

The trap: letting the agent decide priority. It doesn't have your full context. It doesn't know client X is calling tomorrow, that you're tired, that the budget is tight.

What the agent can do:
- Order by deadline.
- Flag delays.
- Identify dependencies.
- Propose a plan.

What you must do:
- Validate or reorder.
- Decide to defer or cancel.
- Judge the real urgency (not the theoretical deadline).

## Tasks feed the briefing

Each completed task enriches the context. After a week, your agent can say:

```
This week: 8 tasks completed, 2 deferred, 1 blocked.
The pattern: infra tasks finish quickly, doc tasks drag on.
Suggestion: block 2h for docs on Thursday.
```

This feedback is only possible if tasks are tracked with their status and dates. A text file without dates doesn't allow this.

## Minimal task format

For the workflow to work, each task needs:

```
- Title (what)
- Status (todo / in_progress / done / blocked)
- Priority (high / medium / low)
- Creation date
- Deadline (optional)
- Notes (optional — context, blockers, decisions)
```

No need for more at the start. Add fields when the need arises, not before.

## Common mistakes

**The agent decides alone.** It closes a task, opens another, changes priorities. You discover the changes after the fact. Solution: rule in the system prompt -- "Never change a task's status without validation."

**You micro-manage.** Every sub-step needs validation. The agent spends more time waiting than executing. Solution: define confidence levels (see section 4.11).

**No reporting.** The agent executes but doesn't say what it did. You don't know where things stand. Solution: require a summary after each completed task.

## Steps

1. Add this rule to your system prompt: "Propose tasks, don't execute them without validation."
2. Ask for a daily briefing: "What are the priority tasks today?"
3. Practice triage: validate, defer, or cancel each proposal.
4. After each execution, verify the status is updated.
5. At week's end, ask for a summary.

## Checklist

- [ ] The agent proposes without executing automatically.
- [ ] You validate each task before execution.
- [ ] Statuses are updated after each action.
- [ ] A weekly summary is possible from the data.
- [ ] The agent never changes a priority without your approval.

---
