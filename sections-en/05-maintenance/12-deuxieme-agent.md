---
---
status: complete
audience: both
chapter: 05
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: en
---

# 5.12 -- When to add a second agent

## Context

One agent works well for a single context. When the context grows too large — too many projects, too many responsibilities, too much context to maintain — response quality drops. This is the signal that it might be time to add a second agent.

## Signs it's time

1. **The system prompt exceeds 500 words** and you can't condense it without losing critical context.

2. **The domains are disjoint.** Your agent handles both infrastructure and client communication. These are two different skill sets with different rules.

3. **Context errors are increasing.** The agent applies project A rules to project B. It confuses clients. It mixes workflows.

4. **Token cost is exploding.** Too much memory, too much context loaded per request.

5. **You spend time recalibrating.** "No, this is project X, not Y." If this happens several times a week, the context is too broad.

## How to structure it

### Option 1: by domain

```
Agent 1: Infrastructure / DevOps
  - Manages: VPS, Docker, PostgreSQL, Vault, backups, monitoring
  - System prompt: technical, commands, procedures

Agent 2: Business / Communication
  - Manages: client emails, documentation, planning, billing
  - System prompt: professional tone, templates, business rules
```

### Option 2: by project

```
Agent 1: Cockpit Project
  - Manages: everything related to cockpit (code, deploy, tasks)
  - Context: cockpit stack, cockpit workflows

Agent 2: OpenClaw Project
  - Manages: writing, structure, review
  - Context: playbook plan, style guide
```

### Option 3: by trust level

```
Agent 1: Operations (level 1-2)
  - Can act (within limits)
  - Access to bash, Docker, PostgreSQL

Agent 2: Advisory (level 0)
  - Read-only
  - Analysis, recommendations, writing
  - No infrastructure access
```

## Isolation

Each agent has its own scope. Don't share everything.

### What should be separated

- **System prompt**: each agent has its own, tailored to its domain.
- **Memory**: each agent has its own memory. The infrastructure agent's memory doesn't contain client context.
- **Access**: the business agent doesn't have bash access. The infrastructure agent doesn't have access to emails.
- **Boundaries**: adapted to each agent's domain.

### What can be shared

- **Tasks**: if both agents work on the same tasks (shared PostgreSQL table).
- **Cross-cutting workflows**: deployments involving both code and infrastructure.
- **Reference files**: CONSTITUTION.md, BOUNDARIES.md (with sections per agent).

### File structure

```
~/.claude/
  agent-infra/
    system-prompt.md
    memory/
    boundaries.md
  agent-business/
    system-prompt.md
    memory/
    boundaries.md
  shared/
    CONSTITUTION.md
    TASKS (shared PostgreSQL table)
```

## Communication between agents

Agents don't talk directly to each other. You are the link.

### Recommended pattern

```
1. Infrastructure agent detects a problem: "The cockpit container is restarting in a loop."
2. You diagnose with Agent Infra.
3. If the fix involves code, you move to Agent Business/Code.
4. You return to Agent Infra to deploy the fix.
```

### What NOT to do

- Pass messages from one agent to another without reviewing them. ("Agent 1 says X, tell Agent 2.") You lose control.
- Give both agents access to the same communication channel. Confusion guaranteed.

## Common mistakes

**Adding an agent too early.** You have 3 tasks and 1 project. A single agent is more than enough. Only add an agent when the first one is saturated.

**No isolation.** Both agents have the same access and the same memory. They step on each other's toes.

**Too many agents.** 4 specialized agents for a solo setup. Time spent coordinating exceeds time saved. For most setups: 1 is enough, 2 at most.

**No naming convention.** You no longer know which agent does what. Name them clearly: "agent-infra", "agent-content", not "agent-1", "agent-2".

## Steps

1. Identify the disjoint domains in your current usage.
2. Evaluate: does the separation solve a real problem?
3. If yes, create the second agent with a minimal system prompt.
4. Define the isolation (access, memory, boundaries).
5. Test for 2 weeks with both agents.
6. Evaluate: has response quality improved?

## Checklist

- [ ] The need for a second agent is justified (at least 2 signs from the list).
- [ ] Each agent has its own system prompt and its own memory.
- [ ] Access is separated (the business agent doesn't have bash access, etc.).
- [ ] Communication goes through you, not between agents.
- [ ] The total number of agents is less than or equal to 2 (unless demonstrated need).

---
