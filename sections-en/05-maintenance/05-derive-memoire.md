---
---
status: complete
audience: both
chapter: 05
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: en
---

# 5.5 -- Memory Drift

## Context

Your agent's memory accumulates information over time. Some becomes obsolete, some contradicts itself, some has become false without anyone noticing. This is memory drift.

Steinberg compares it to a desk: if you never organize, important documents get lost under expired papers.

## Symptoms of Drift

You have a drift problem when:

- The agent mentions a project you finished 2 months ago.
- The agent uses an old workflow that has been replaced.
- The agent gives contradictory information in two close responses.
- The agent "remembers" a decision that was canceled.
- The agent repeats information, phrasing it differently each time (sign of redundancy).

## Types of Drift

### Obsolescence

The information was true but no longer is.

```
Memory: "The cockpit project uses Express.js"
Reality: you migrated to Fastify 3 weeks ago.
```

### Contradiction

Two pieces of information contradict each other.

```
Memory file A: "Backups are daily"
Memory file B: "Backups are weekly"
```

### Inflation

The same information is stored in 5 different forms. The agent no longer knows which one to use.

```
File 1: "The user prefers informal speech"
File 2: "Use informal speech, not formal"
File 3: "Informal communication, use tu"
```

### Memorized Hallucination

The agent once "invented" information and stored it as fact.

```
Memory: "The server has 16 GB of RAM"
Reality: it has 8.
```

## Periodic Cleanup

### Frequency

- **Monthly**: quick scan (15 minutes).
- **Quarterly**: deep cleanup (1 hour).
- **After each completed project**: remove project context.

### Scan Prompt

```
Read all your memory and context files.
For each factual piece of information, indicate:
- [OK]: still true and useful
- [OBSOLETE]: no longer true
- [DOUBT]: you're not sure, needs verification with me
- [REDUNDANT]: says the same thing as another entry

List the results. We'll clean up together.
```

### Cleanup Process

1. Run the scan prompt.
2. Review the results with the agent.
3. Delete the [OBSOLETE] entries.
4. Merge [REDUNDANT] entries into a single one.
5. Verify the [DOUBT] entries — correct or delete.
6. Save the cleaned version.

## Night Consolidation

Steinberg's concept: at the end of each day (or week), the agent consolidates what it learned.

```
Summary of the day:
- What new information did you learn today?
- Does it contradict anything in your memory?
- What information in memory was confirmed by today?

Propose the necessary memory updates.
```

It doesn't take long. 2 minutes at the end of the day. But it prevents drift from accumulating.

## Voluntary Forgetting

Sometimes the right action is to delete from memory. Not because it's false, but because it's no longer useful.

Candidates for forgetting:

- Details of a completed project (keep only lessons learned).
- Intermediate decisions that were replaced by the final decision.
- Temporary context ("this week I'm working on X").
- Documented trials and errors that are no longer relevant.

Voluntary forgetting reduces noise and token cost. Less memory = faster reads = more accurate responses.

## Common Mistakes

**Never clean up.** Memory grows, contradictions accumulate, response quality drops. You blame the agent when it's actually polluted memory.

**Delete everything.** Radical cleanup: you erase all memory. The agent starts from scratch and loses all useful context. Clean surgically.

**Trust the scan without verifying.** The agent marks [OK] on obsolete information because it doesn't know it changed. Verify critical facts yourself.

**No memory versioning.** You delete information and need it 2 weeks later. Keep a backup before each cleanup.

## Steps

1. Run the scan prompt on your memory.
2. Review the results: OBSOLETE, DOUBT, REDUNDANT.
3. Save the current version of memory (backup).
4. Clean up: delete, merge, correct.
5. Test: does the agent give more accurate responses?
6. Schedule the next cleanup (monthly).

## Verification

- [ ] A memory scan has been done in the last month.
- [ ] Obsolete information is deleted.
- [ ] Redundancies are merged into a single entry.
- [ ] A memory backup exists before each cleanup.
- [ ] Night consolidation is practiced (daily or weekly).

---
