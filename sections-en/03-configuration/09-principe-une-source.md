---
---
status: complete
audience: both
chapter: 03
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: en
---

# 3.9 -- One source at a time (Steinberg principle)

## Context

You've configured the agent. SOUL.md, USER.md, CONSTITUTION.md, MEMORY.md, knowledge/ -- everything is in place. Now you want to connect your tools: calendar, email, CRM, Notion, Slack, database, business API...

Stop. One source at a time.

This is the most counter-intuitive principle of Steinberg. Instinct says "connect everything so the agent has a complete view." Experience says "each source added increases noise faster than signal."

## Why only one source at a time

Each new connection increases three things:

**1. Token cost.** Each source injected into the context consumes window space. Calendar + emails + tasks + CRM = a context that explodes before you even ask your question.

**2. Interpretation risk.** The more sources the agent has, the more connections it makes. Some are relevant. Others are phantom correlations. "You have a meeting with X and an unread email from X, so I deduce that..." -- not necessarily.

**3. Noise.** 50 unread emails, 30 tasks, 15 calendar events. The agent drowns important information in the mass.

## The method

### Connect

Add ONE source. Calendar first (see section 3.10).

### Validate

Live with this source for 3 to 5 days. Ask the question:

```
What has changed since yesterday in [source] ?
```

If the answer is useful and precise, the source adds value. If the answer is vague or noisy, the source configuration needs refinement before adding another.

### Keep or remove

Decision rule: **does this source improve a decision I need to make THIS WEEK?**

- Yes: keep
- "It could be useful someday": remove
- "It's interesting": remove

Interesting is the enemy of relevant.

## The anti-pattern: the connection weekend

Classic scenario:

```
Friday evening: "This weekend, I'll connect everything!"
Saturday: calendar, email, Notion, CRM, Slack, database
Sunday: "It's amazing, the agent sees everything!"
Monday morning: 45-line briefing, 3 false connections,
  2 suggested actions completely off base
Monday noon: "This tool doesn't work."
```

The problem isn't the tool. It's that 6 sources connected in 48 hours weren't validated individually. Impossible to know which one is causing the noise.

## Recommended connection order

| Order | Source | Why now |
|-------|--------|---------|
| 1 | Calendar | Most reliable signal (section 3.10) |
| 2 | Tasks | Completes calendar with unplanned items (section 3.11) |
| 3 | Email | Most voluminous source, add after mastering first 2 (section 3.12) |
| 4 | Business tools | CRM, Notion, database -- based on your specific need |
| 5 | Messaging | Slack, Teams -- last, most noisy |

Delay between each addition: minimum 3 days, ideally 1 week.

## Step by step

1. Identify the source that would have the most impact on your week
2. Connect it (see following sections for each type)
3. Use it for 3-5 days
4. Evaluate with the question "What has changed?"
5. If valid, move to the next one. Otherwise, refine first.

## Common mistakes

**Connecting everything at once**: See the anti-pattern above. Noise drowns signal.

**Keeping a useless source**: "I connected Slack but I never use it in my briefings." Disconnect. Each useless source consumes tokens and adds noise.

**Connecting before configuring**: Adding email before having solid USER.md and CONSTITUTION.md. The agent will process your emails without understanding your priorities or knowing your rules.

**Confusing "possible" and "useful"**: The agent CAN connect to 15 sources. That doesn't mean it SHOULD.

## Verification

- [ ] You've identified your first source to connect
- [ ] You have a plan for progressive addition (one source at a time)
- [ ] You know the validation question ("What has changed?")
- [ ] You have the decision criterion (improves a decision THIS WEEK)
- [ ] The base files (SOUL.md, USER.md, CONSTITUTION.md) are in place BEFORE the first connection

---
