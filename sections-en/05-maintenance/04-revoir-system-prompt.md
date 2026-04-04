---
status: complete
audience: both
chapter: 05
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: en
---

# 5.4 -- Review the system prompt

## Context

A system prompt is not sacred text. Your context changes, your projects evolve, your needs become clearer. A prompt written 3 months ago no longer reflects your reality today. If you don't review it, it accumulates obsolete instructions and the agent gradually degrades.

## Frequency

- **Complete review**: every month.
- **Spot adjustments**: when a trigger appears (see below).
- **Condensation**: every 3 months (the prompt naturally grows, you need to compress it).

## Triggers for a review

You should review the prompt when:

1. **A project ends.** Instructions tied to that project clutter the prompt.
2. **A tool changes.** You migrate from X to Y but the prompt still mentions X.
3. **You correct the agent regularly on the same point.** A signal that the prompt doesn't cover this case.
4. **The prompt exceeds 300 words.** Time to condense.
5. **You change models.** Each model interprets differently. Test and adjust.
6. **An incident occurred.** The agent did something it shouldn't have. Add a rule or clarify.

## What to preserve

Certain parts of the prompt are stable. Don't touch them unless there's a strong reason:

- **The mission** (who the agent is, who it's for).
- **Tone and format** (once calibrated, it holds).
- **Boundaries** (prohibitions don't change).
- **Language** (stable once defined).

## What to rewrite

What changes most often:

- **Context**: active projects, stack, tools.
- **Operational rules**: workflows, priorities, processes.
- **Access**: which tools the agent can use.

## Review method

### 1. Reread the current prompt

Read it as if for the first time. Mark:
- [OBSOLETE]: what is no longer true.
- [VAGUE]: what could be more precise.
- [MISSING]: what should be there but isn't.
- [OK]: what is good.

### 2. Delete before adding

The rule: for every line added, find a line to remove. The prompt must stay short.

### 3. Test

After the review, test with 5 typical requests. Compare the responses with responses from before. If quality drops, roll back.

### 4. Version control

Keep previous versions. A simple file:

```
system-prompt-v1.md    (2026-01-15)
system-prompt-v2.md    (2026-02-20)
system-prompt-v3.md    (2026-04-01)  <- current
```

If a revision degrades performance, you can revert to the previous version.

## Common mistakes

**Never reviewing.** The prompt from January 2026 is still active in December. It mentions finished projects, replaced tools, obsolete rules.

**Reviewing too often.** Every day you change something. The agent never has time to "stabilize" and you can't evaluate the impact of a change.

**Adding without deleting.** The prompt grows from 150 to 500 words in 3 months. Performance drops, cost increases.

**No version control.** You modify the prompt and no longer know what was there before. Impossible to roll back.

## Steps

1. Schedule a monthly review (set a reminder).
2. Reread the prompt using the OBSOLETE/VAGUE/MISSING/OK system.
3. Delete what is obsolete.
4. Clarify what is vague.
5. Add what is missing.
6. Condense if > 300 words.
7. Test with 5 requests.
8. Save the old version.

## Checklist

- [ ] The prompt's last review was less than a month ago.
- [ ] The prompt is under 300 words.
- [ ] No instruction references a finished project or replaced tool.
- [ ] Previous versions are saved.
- [ ] 5 test requests produce correct responses after the review.
