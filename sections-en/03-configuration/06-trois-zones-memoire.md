---
---
status: complete
audience: both
chapter: 03
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: en
---

# 3.6 -- The three memory zones

## Context

An agent without memory is an amnesiac agent. Each session starts from scratch. You repeat the same things. It asks the same questions.

An agent with too much memory is a drowning agent. It mixes context from 6 months ago with today's. It cites obsolete decisions. It treats what is no longer current as if it were.

Steinberg's solution: three memory zones, each with its own scope and rules.

## The three zones

```
+--------------------------------------------------+
|                                                  |
|  HOT MEMORY (session)                            |
|  Duration: this conversation                     |
|  Size: unlimited (within context window)         |
|  Content: everything being said right now        |
|  Disappears: at end of session                   |
|                                                  |
+--------------------------------------------------+
          |
          | What deserves to be retained
          v
+--------------------------------------------------+
|                                                  |
|  WARM MEMORY (MEMORY.md)                         |
|  Duration: days to weeks                         |
|  Size: 80 lines max                              |
|  Content: recent facts, decisions, context       |
|  Cleanup: regular compression                    |
|                                                  |
+--------------------------------------------------+
          |
          | What is lasting and structured
          v
+--------------------------------------------------+
|                                                  |
|  COLD MEMORY (knowledge/)                        |
|  Duration: months to indefinite                  |
|  Size: unlimited (one file per topic)            |
|  Content: stable knowledge, references, guides   |
|  Cleanup: quarterly review                       |
|                                                  |
+--------------------------------------------------+
```

## Hot memory: the session

This is the ongoing conversation. Everything you say, everything the agent responds with, remains accessible during the session.

**What goes in**: everything. Questions, answers, reflections, attempts, errors.

**What comes out**: nothing automatically. At the end of the session, everything disappears EXCEPT what you or the agent decide to save in MEMORY.md or knowledge/.

**Pitfall**: thinking that the agent will "remember" tomorrow what you said today. Without explicit save, hot memory is volatile.

Good practice at end of session:

```
What deserves to be retained from this session?
Update MEMORY.md.
```

## Warm memory: MEMORY.md

The buffer between the present and the lasting. 80 lines maximum (Steinberg's rule). Contains the recent context necessary for the agent to be relevant when opening the next session.

**What goes in**:
- Decisions made this week
- Important recent facts
- Current context (project, negotiation, event)
- Temporary notes not to forget

**What does NOT go in**:
- Stable knowledge (goes in knowledge/)
- Permanent personal information (goes in USER.md)
- Agent operating rules (goes in CONSTITUTION.md)
- Tasks (goes in the task system)

Details in section 3.7.

## Cold memory: knowledge/

Lasting knowledge. Structured by domain. One file per topic. No global size limit, but each file should remain readable (200 lines max per file recommended).

**What goes in**:
- Documented processes
- Stable business information
- Technical references
- Guides and procedures
- Profiles of durable clients or partners

**What does NOT go in**:
- Temporary context (goes in MEMORY.md)
- Opinions or preferences (goes in USER.md)
- Agent rules (goes in CONSTITUTION.md)

Details in section 3.8.

## Why separate

**Reason 1: token cost.** Everything the agent reads at startup consumes tokens. MEMORY.md (80 lines) is read every session. knowledge/ is read on demand or according to boot sequence. Mixing the two = loading 500 lines of stable knowledge every session, even when not relevant.

**Reason 2: noise.** An agent reading 200 lines of context at startup will lose the signal. Recent information (MEMORY.md) must be separated from background knowledge (knowledge/) so the agent knows what is CURRENT.

**Reason 3: maintenance.** MEMORY.md compresses every week. knowledge/ is reviewed every quarter. Two different rhythms for two different types of information.

**Reason 4: relevance.** When the agent reads "Decision 03/28: launching postponed to April" in MEMORY.md, it knows it's recent and actionable. When it reads "Product launch process" in knowledge/, it knows it's a stable reference.

## Decision diagram

```
Information arrives. Where to store it?

Does it concern ONLY this session?
  YES --> Do nothing. Hot memory.
  NO --> continue

Will it change in the next 2 weeks?
  YES --> MEMORY.md (warm memory)
  NO --> continue

Is it stable, reusable knowledge?
  YES --> knowledge/ (cold memory)
  NO --> continue

Is it information about ME that doesn't change often?
  YES --> USER.md
  NO --> continue

Is it an agent operating rule?
  YES --> CONSTITUTION.md
  NO --> Probably not necessary to store it.
```

## Common mistakes

**Everything in MEMORY.md**: The file grows, exceeds 80 lines, the agent loses the signal. MEMORY.md is a buffer, not a database.

**Nothing in knowledge/**: You repeat the same explanations every session because the agent has no lasting reference.

**No cleanup**: MEMORY.md contains notes from 3 months ago. knowledge/ contains obsolete files. Unmaintained memory is worse than no memory.

**Confusing hot and warm memory**: "I told you that earlier" -- yes, in session. But without saving in MEMORY.md, tomorrow it's forgotten.

## Verification

- [ ] You understand the difference between the 3 zones
- [ ] MEMORY.md exists and is under 80 lines
- [ ] The knowledge/ folder is created with at least one file
- [ ] You have an end-of-session routine ("Update MEMORY.md")
- [ ] Information is in the right zone (no tasks in USER.md, no stable knowledge in MEMORY.md)

---
