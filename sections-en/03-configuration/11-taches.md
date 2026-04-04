---
---
status: complete
audience: both
chapter: 03
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: en
---

# 3.11 -- Tasks: the invisible pressure

## Context

The calendar shows what is PLANNED. Tasks show what is REAL but not yet planned.

This is the invisible pressure: the things you need to do but that have no time slot. The report to finish. The follow-up to send. The bug to fix. These items are not in the calendar, but they weigh on every prioritization decision.

An agent who sees your calendar but not your tasks believes your free slots are truly free. They are not.

## Calendar + tasks = complete picture

| Calendar | Tasks |
|---|---|
| What has a date and time | What has a deadline (or not) |
| Commitments with others | Commitments with yourself |
| Planned | Unplanned but real |
| Visible to others | Often private |

The agent needs both to produce a useful briefing. "You have 2 hours free this afternoon" is incomplete if you have 5 urgent tasks overdue.

## Connection

### Via database

```
openclaw skill add tasks --source db
```

The agent connects to your task database (Supabase, PostgreSQL, SQLite). Advantage: full control, no dependency on a third-party service.

### Via external tool

```
openclaw skill add tasks --source todoist
openclaw skill add tasks --source notion
openclaw skill add tasks --source linear
```

The agent connects to your existing task tool. Advantage: no need to migrate.

### Scope: this week, not the wishlist

Critical rule: the agent must only see tasks from THIS WEEK. Not the backlog of 200 items. Not the wishlist. Not the "maybe someday".

Why: an agent who sees 200 tasks treats them all as potentially relevant. It mentions low-priority tasks in the briefing. It suggests working on items that are 3 months old. Noise drowns out the signal.

Recommended configuration:

```markdown
## Task scope
- Tasks with deadline this week
- Tasks marked "urgent" or "high priority"
- Tasks assigned to me (not ones I've delegated)
- Maximum: 15 visible tasks at once
```

## Step by step

### 1. Identify your task source

Where are your tasks today? In a tool? Multiple places? On sticky notes? In a text file?

If they're scattered, consolidate them in a single place first before connecting the agent.

### 2. Connect in read-only

Like the calendar, start in read mode. The agent sees the tasks, mentions them in the briefing, but does not modify them.

### 3. Define the scope

Set the filter: this week + urgent only.

### 4. Validate the calendar + tasks integration

```
Show me my day with my pending tasks.
```

The agent must:
- Display the calendar (meetings, blocks)
- List relevant tasks
- Suggest when to handle tasks in free slots

### 5. Add write permissions (optional)

After validation, you can authorize the agent to:
- Mark a task as complete (after your confirmation)
- Add a task (from an email or meeting)
- Change priority (with notification)

## Common mistakes

**Connecting all tasks**: 200 tasks in context = useless briefing. Filter to this week.

**No priority**: If all tasks have the same priority, the agent can't sort them. Prioritize your tasks in your tool BEFORE connecting the agent.

**Tasks in MEMORY.md**: "Finish the report by Friday" in MEMORY.md instead of the task system. MEMORY.md is not a todo list. Tasks go in the task system.

**Duplicate tasks**: The same task in Notion AND in MEMORY.md. The agent counts it twice.

**Connecting tasks before calendar**: Tasks without calendar are a floating list. Connect the calendar first (section 3.10).

## Verification

- [ ] Task source identified and consolidated
- [ ] Read-only connection established
- [ ] Scope defined (this week + urgent)
- [ ] Maximum 15 visible tasks
- [ ] "My day with my tasks" test passed
- [ ] Calendar + tasks integration validated
- [ ] No tasks in MEMORY.md (they are in the task system)
