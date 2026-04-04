---
---
status: complete
audience: both
chapter: 03
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: en
---

# 3.7 -- MEMORY.md : the collective memory

## Context

MEMORY.md is the most living file in your configuration. It changes every day. It compresses every week. It is read at every session startup.

This is warm memory: what happened recently and still matters. Not the distant past (knowledge/). Not the immediate present (session). The in-between.

## The 80-line rule

Steinberg is categorical: MEMORY.md must never exceed 80 lines.

Why 80:
- Below 80, the agent treats each line as important
- Above 80, the agent starts to "skim" and misses information
- 80 lines = approximately 2 minutes of reading for the agent at startup

This is not a suggestion. This is a hard constraint. If MEMORY.md exceeds 80 lines, you must compress or move content to knowledge/.

## Recommended structure

```markdown
# MEMORY.md

## Current context
- [Important fact 1 -- date]
- [Important fact 2 -- date]
- [Ongoing situation]

## Recent decisions
- [Decision 1 -- date -- reason]
- [Decision 2 -- date -- reason]

## Pending
- [What is waiting for a response or action]
- [What is blocked and why]

## Session notes
- [Last notable fact from the last session]
```

Four sections. No more. If you need more sections, it means content should migrate to knowledge/.

## Night consolidation (Steinberg method)

Every evening (or every morning before the briefing), the agent consolidates MEMORY.md:

1. **Delete** what is no longer relevant (decision executed, event passed)
2. **Compress** what can be (3 lines on the same subject = 1 line)
3. **Migrate** what has become stable knowledge to knowledge/
4. **Add** what emerged during the day

Consolidation prompt:

```
Consolidate MEMORY.md:
1. Delete what is no longer relevant (more than 2 weeks old, already processed)
2. Compress related entries into a single line
3. If information has become stable, migrate it to knowledge/
4. Verify that the total does not exceed 80 lines
Show me the diff before saving.
```

## Voluntary forgetting

Forgetting is a feature, not a bug. An agent that remembers everything is an agent that doesn't know what matters.

When to delete from MEMORY.md:
- The decision was executed and no longer has impact
- The event has passed and no longer influences the present
- The information was migrated to knowledge/
- The fact became obsolete (price changed, person left, project cancelled)

When NOT to delete:
- The decision still impacts the current week
- The information is necessary for the next briefing
- The context is still active (ongoing negotiation, project in critical phase)

## Collective vs individual memory

If you have multiple agents (section 3.17), MEMORY.md can be:
- **Shared**: all agents read the same file. Simpler. Risk of noise.
- **Separate**: each agent has its own MEMORY.md. Cleaner. Risk of desynchronization.

Recommendation: start shared. Separate when noise becomes a problem.

## MEMORY.md template

```markdown
# MEMORY.md
Last consolidation: [date]

## Current context
- [3-5 lines max on the general situation]

## Recent decisions
- [YYYY-MM-DD] [Decision] -- [Reason in 5 words]
- [YYYY-MM-DD] [Decision] -- [Reason in 5 words]

## Pending
- [What] -- pending [who/what] -- since [date]

## Notes
- [Notable fact from the last session]
```

## Common mistakes

**MEMORY.md never cleaned**: The file grows to 300 lines. The agent loses the signal. Consolidate at least once a week.

**Keep everything "just in case"**: If information hasn't been useful for 2 weeks, it's probably no longer relevant. Delete or migrate.

**No dates**: Without dates, impossible to know what is recent. Each entry must have a date.

**Duplicates with knowledge/**: "Deployment process -- updated 15/03" in MEMORY.md when the process is already in knowledge/infra/. MEMORY.md points to knowledge/, it doesn't duplicate.

**Too many sections**: 8 sections in MEMORY.md = too much structure. 4 sections are enough. If you need more, it means content belongs elsewhere.

## Verification

- [ ] MEMORY.md exists and is under 80 lines
- [ ] Each entry has a date
- [ ] The structure has a maximum of 4 sections
- [ ] No duplicates with knowledge/
- [ ] The consolidation prompt is ready (or automated via cron)
- [ ] You know what should be deleted and what should be kept

---
