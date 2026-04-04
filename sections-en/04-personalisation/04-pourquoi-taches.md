---
---
status: complete
audience: both
chapter: 04
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: en
---

# 4.4 -- Why a task system

## Context

An agent without a task system is an advisor. You ask it questions, it answers. You forget to ask, it forgets to do. Nothing persists between sessions.

An agent with a task system is a partner. It knows what's in progress, what's blocked, what's done. It can suggest the next action without you stating it.

The difference is not technical. It's a difference in relationship.

## Advisor agent vs partner agent

| | Advisor | Partner |
|---|---|---|
| Memory | Session only | Persistent |
| Initiative | Answers questions | Proposes actions |
| Follow-up | None | Knows where we stand |
| Value | One-off | Cumulative |
| Dependency | On your memory | On a shared system |

The advisor is useful. The partner is essential.

## Start simple

Don't install PostgreSQL, an ORM, and a dashboard on day one. Start with a checklist.

### Level 1: a text file

```markdown
# TASKS.md

## In progress
- [ ] Migrate backup to S3 — deadline: 2026-04-05
- [ ] Write API documentation endpoint /users

## Pending
- [ ] Renew SSL certificate (expires 2026-05-15)

## Done
- [x] Configure Telegram monitoring — 2026-03-28
```

Your agent can read this file, suggest updates, and remind you of deadlines. Zero infrastructure.

### Level 2: a structured JSON/YAML file

```yaml
tasks:
  - id: 1
    title: "Migrate backup to S3"
    status: in_progress
    priority: high
    deadline: "2026-04-05"
    notes: "Test restoration after migration"
  - id: 2
    title: "API documentation /users"
    status: todo
    priority: medium
```

Easier for the agent to parse. Allows queries ("what high priority tasks?").

### Level 3: database

See section 4.6. This is the right choice when you exceed 20 active tasks or need history.

## What the task system concretely changes

**Without tasks:** "Where are we with the S3 backup?"
Agent: "I don't know, I don't have the context."

**With tasks:** "What's scheduled for today?"
Agent: "3 priority tasks. The S3 migration is 2 days behind. The SSL certificate expires in 6 weeks. Suggestion: finish S3 today."

It's the difference between flying by the seat of your pants and flying with a dashboard.

## When to move to the next level

- **Text file -> JSON**: when you have more than 10 tasks and want to filter by priority or status.
- **JSON -> Database**: when you want history, complex queries, or multiple agents sharing the same tasks.

Don't skip steps. Each level teaches you what you actually need at the next level.

## Common mistakes

**Too much structure too soon.** Install Jira for 5 tasks. A TASKS.md file is enough to start.

**No structure at all.** "I keep it all in my head." No. You forget, the agent forgets too. Write it down.

**Delegate follow-up without verifying it.** The agent updates the tasks but you never review them. Statuses diverge from reality. See section 4.5.

## Steps

1. Create a `TASKS.md` file in your project.
2. Add your 5 most important tasks in progress.
3. Tell your agent: "Read TASKS.md. What's the priority?"
4. Use for a week.
5. Evaluate: is the format enough or do we need to move to level 2?

## Checklist

- [ ] A task file exists and is accessible to the agent.
- [ ] Tasks have at minimum: title, status, priority.
- [ ] The agent knows where to find and read this file.
- [ ] You review the tasks at least once a week.

---
