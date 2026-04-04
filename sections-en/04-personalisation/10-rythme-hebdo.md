---
---
status: complete
audience: both
chapter: 04
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: en
---

# 4.10 -- The Weekly Rhythm

## Context

An agent without rhythm is reactive: it responds when you ask. An agent with rhythm is proactive: it prepares what you need before you ask for it.

The basic rhythm according to Steinberg: preview on Monday, review on Friday. The agent prepares both. You decide and validate.

## Monday Preview

Monday morning, the agent presents the coming week to you.

### What the agent prepares

```
=== Preview week of March 31, 2026 ===

Tasks in progress: 4
Overdue tasks: 1 (S3 migration, 3 days late)
Deadlines this week: 2
  - Wednesday: API doc delivery
  - Friday: SSL certificate renewal

Suggested plan:
- Monday: finish S3 migration (catch up on delay)
- Tuesday-Wednesday: API doc
- Thursday: monthly secret rotation
- Friday: SSL certificate + review

Blockers detected: none.
Questions for you: has client X confirmed the spec?
```

### What you do

You read, you adjust. "Swap Tuesday and Monday." "Add the team's PR review." "Client hasn't confirmed, defer the doc."

5 minutes. Your week is framed.

### Prompt to configure

Add to the system prompt:

```
Every Monday morning, when I say "preview", generate:
- Tasks in progress and overdue
- Deadlines for the week
- Suggested plan day by day
- Blockers detected
- Questions for me
Format: bullet points, brief.
```

## Friday Review

On Friday, the agent does a recap of the week that has passed.

### What the agent prepares

```
=== Review week of March 31, 2026 ===

Completed: 5/7 planned tasks
  - S3 migration [DONE]
  - API /users doc [DONE]
  - Secret rotation [DONE]
  - Auto health check [DONE]
  - Team PR review [DONE]

Not completed: 2
  - SSL certificate: deferred (expires in 42 days, not urgent)
  - Auth refactoring: blocked (waiting for client spec)

Time saved by the agent: ~3h
  - Auto health checks: 5x10min = 50min
  - API doc generation: ~1h30
  - Automated secret rotation: ~40min

Points of attention for next week:
  - SSL certificate must be done next week.
  - 2 tasks dependent on client spec: follow up?
```

### What you do

You validate the recap. You note what went well and what got stuck. It's also the right time to adjust workflows or the system prompt if something didn't go smoothly during the week.

## Keep It Light and Reviewable

The trap of the weekly rhythm: it becomes heavy reporting that nobody reads.

Rules:

- **Monday preview**: maximum 15 lines. If it's longer, you have too many active tasks.
- **Friday review**: maximum 20 lines. Numbers and facts, no prose.
- **Reading time**: less than 2 minutes for each.
- **Decision time**: less than 5 minutes to adjust the plan.

If you spend more than 10 minutes on the Friday review, that's a signal the system is too complex.

## Adapt the Rhythm

Monday/Friday is a starting point. Adapt to your reality:

- **Solo freelancer**: Monday/Friday is enough.
- **Small team**: add a Wednesday check (mid-week check).
- **Intense project**: 5-line daily morning briefing.
- **Pure maintenance**: a review every two weeks may suffice.

What matters isn't the frequency, it's the regularity. A rhythm kept at 80% is better than an ideal rhythm kept at 20%.

## Common Mistakes

**Too much detail.** The preview is 50 lines with sub-tasks and hourly estimates. Nobody reads it. Stay macro.

**No decision.** You read the preview but decide nothing. The agent doesn't know what to prioritize. A preview without decision is noise.

**Abandoning after 2 weeks.** "It's redundant, I know what I have to do." You know it because the preview reminded you. Stop the preview and you'll forget within the week.

## Steps

1. Add the preview/review prompts to the system prompt.
2. Next Monday: say "preview" to your agent.
3. Spend 5 minutes adjusting the plan.
4. Friday: say "review".
5. Note if the format is useful or if it needs adjusting.
6. Keep the rhythm for 4 weeks before evaluating.

## Verification

- [ ] The preview and review prompts are in the system prompt.
- [ ] The preview fits in 15 lines max.
- [ ] The review fits in 20 lines max.
- [ ] You actually decide after each preview (not just read).
- [ ] The rhythm has been kept for at least 2 consecutive weeks.

---
