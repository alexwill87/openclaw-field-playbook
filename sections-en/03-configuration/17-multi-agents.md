---
---
status: complete
audience: both
chapter: 03
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: en
---

# 3.17 -- Multi-agent architecture

## Context

A single agent covers 90% of needs. This chapter is for the remaining 10%.

DO NOT START HERE. If you're reading this section before having a stable and useful primary agent for at least 4 weeks, close this page and come back later.

Multi-agent solves a specific problem: a single agent cannot do everything well. Not because of lack of capacity, but because different roles require different postures, permissions, and knowledge.

## When a single agent is no longer enough

Signs it's time to move to multi-agent:

- SOUL.md contains contradictory instructions ("be direct" AND "be diplomatic depending on context")
- CONSTITUTION.md has rules that apply to some tasks but not others
- knowledge/ mixes unrelated domains (technical infrastructure AND client communication)
- The agent changes "personality" depending on the subject, and the result is inconsistent

Signs it's NOT the right time:

- You don't yet have a stable morning briefing
- USER.md is incomplete
- You haven't connected any sources
- You use the agent less than 5 times per week

## Specialized agents

The recommended model: one primary agent (generalist) and specialized agents (experts in a domain).

### Architecture examples

**Technical freelancer**:
```
Primary agent: "Axel" -- daily management, briefing, triage
Dev agent: "K8" -- code, infrastructure, deployments
```

**SME owner**:
```
Primary agent: "Clara" -- briefing, email, agenda
Sales agent: "Hugo" -- CRM, pipeline, follow-ups
Ops agent: "Max" -- invoicing, suppliers, logistics
```

**Product team**:
```
Primary agent: "PM" -- prioritization, roadmap, communication
Technical agent: "Dev" -- code review, monitoring, alerts
Data agent: "Ana" -- metrics, reports, A/B tests
```

### When to add a specialized agent

Rule: add a specialized agent when a RECURRING ACTIVITY requires:
- A different tone from the primary agent
- Different permissions
- Specific knowledge that the primary agent doesn't need to load each session

If all three criteria are not met, a single agent with well-organized knowledge/ is sufficient.

## Workspace isolation

Each agent has its own workspace with its own configuration files:

```
workspaces/
  primary/
    SOUL.md              -- personality of the primary agent
    USER.md              -- shared (symlink)
    CONSTITUTION.md      -- rules of the primary agent
    MEMORY.md            -- memory of the primary agent
    knowledge/           -- general knowledge
  dev/
    SOUL.md              -- personality of the dev agent
    USER.md              -- shared (symlink)
    CONSTITUTION.md      -- rules of the dev agent
    MEMORY.md            -- memory of the dev agent
    knowledge/           -- technical knowledge
  commercial/
    SOUL.md              -- personality of the commercial agent
    USER.md              -- shared (symlink)
    CONSTITUTION.md      -- rules of the commercial agent
    MEMORY.md            -- memory of the commercial agent
    knowledge/           -- business knowledge
```

Isolation rules:

| File | Shared? | Reason |
|------|---------|--------|
| SOUL.md | No | Each agent has its own identity |
| USER.md | Yes (symlink) | You are the same person for everyone |
| CONSTITUTION.md | No | Each agent has its own rules |
| AGENTS.md | Yes (symlink) | Central registry of all agents |
| MEMORY.md | Case-by-case | Share if cross-context is needed |
| knowledge/ | No | Each agent has its own knowledge |

## Inter-agent communication

Agents don't talk to each other directly. They communicate via shared artifacts.

### Via shared MEMORY.md

The simplest approach. A single MEMORY.md read by all agents.

```
Primary agent notes in MEMORY.md:
"2026-04-01 -- Client Alpha requested a scope change. To evaluate."

Dev agent reads MEMORY.md at startup and sees the note.
```

Advantage: simple. Disadvantage: MEMORY.md grows quickly with multiple agents writing.

### Via liaison files

Each agent writes to an output file that others can read.

```
workspaces/shared/
  primary-output.md    -- what the primary agent wants to communicate
  dev-output.md        -- what the dev agent wants to communicate
  commercial-output.md -- what the commercial agent wants to communicate
```

Advantage: each agent controls what it shares. Disadvantage: more files to manage.

### Via AGENTS.md

The AGENTS.md registry defines communication channels:

```markdown
## Communication

| From | To | Channel | When |
|------|----|---------|----|
| Primary | Dev | shared/primary-output.md | When a technical topic emerges |
| Dev | Primary | shared/dev-output.md | After each deployment |
| Commercial | Primary | shared/commercial-output.md | When a deal moves forward/backward |
```

## Step by step

### 1. Validate that it's necessary

Review the criteria above. If your primary agent is working well, don't add complexity.

### 2. Identify the first specialized agent

Just one. Not three at once. Which domain would benefit most from a dedicated agent?

### 3. Create the workspace

Copy the structure. Create specific SOUL.md and CONSTITUTION.md. Link USER.md and AGENTS.md.

### 4. Define communication

How do agents exchange information? Shared MEMORY.md or liaison files?

### 5. Test for 2 weeks

Before adding a third agent, the second one must be stable.

### 6. Document in AGENTS.md

Update the central registry with the new agent.

## Common mistakes

**Starting with multi-agent**: You don't even have one agent that works and you're deploying three. Guaranteed results: confusion, wasted tokens, abandonment.

**Overlapping agents**: The primary agent and the sales agent both handle customer emails. Who's right? Define exclusive scopes.

**Too many agents**: 5 agents for a solo entrepreneur. Managing agents becomes a full-time job. 2-3 agents maximum for most contexts.

**No isolation**: All agents share everything. The dev agent has access to sales negotiations. The commercial agent can deploy code. Isolate workspaces.

**Communication undefined**: Agents don't know what others have done. No shared file, no common MEMORY.md. Each agent works in its own bubble.

**Forgetting to update AGENTS.md**: You add an agent but AGENTS.md isn't updated. Other agents don't know it exists.

## Checklist

- [ ] The primary agent has been stable for at least 4 weeks
- [ ] The multi-agent need is justified (all 3 criteria met)
- [ ] Maximum 1 specialized agent added at a time
- [ ] Each agent has its own isolated workspace
- [ ] USER.md and AGENTS.md are shared (symlinks)
- [ ] SOUL.md and CONSTITUTION.md are specific to each agent
- [ ] Inter-agent communication is defined and documented
- [ ] AGENTS.md is up to date with all agents
- [ ] 2 weeks of testing before adding another agent
