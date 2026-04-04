---
---
status: complete
audience: both
chapter: 03
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: en
---

# 3.4 -- AGENTS.md: the agent registry

## Context

When you have only one agent, AGENTS.md seems unnecessary. The moment you have two, it becomes essential.

AGENTS.md is the central registry. It answers three questions:
- Which agents exist?
- What does each one do?
- In what order do they start?

Even with a single agent, AGENTS.md clarifies the boot sequence: the order in which the agent reads its configuration files at startup.

## What AGENTS.md contains

- The list of agents with their roles
- The model used by each
- The permissions for each agent
- The boot sequence (order of file reading)
- Dependencies between agents (if multi-agent)

## Boot sequence: the order of reading

When the agent starts a session, it reads its configuration files in a precise order. This order matters: files read first carry more weight.

Recommended sequence:

```
1. SOUL.md        -- Who am I?
2. USER.md        -- Who do I work for?
3. CONSTITUTION.md -- What are my rules?
4. AGENTS.md      -- Who else exists? What is my specific role?
5. MEMORY.md      -- What happened recently?
6. knowledge/     -- What else should I know?
```

Why this order:
- Identity (SOUL.md) frames everything else
- User profile (USER.md) guides the responses
- Rules (CONSTITUTION.md) define the boundaries
- The registry (AGENTS.md) situates the agent within the whole
- Memory (MEMORY.md) provides recent context
- Knowledge (knowledge/) fills in as needed

## Step by step

### 1. List your agents

Even if you have only one, document it.

### 2. Define the role of each

One role = one sentence. If you need more, the agent is probably doing too many things.

### 3. Assign permissions

Each agent has its own levels in the permissions pyramid (section 3.1).

### 4. Document the boot sequence

List the order of file reading for each agent.

### 5. Define inter-agent communication channels

If you have multiple agents, how do they communicate? Via shared files? Via MEMORY.md? Via a message bus?

## AGENTS.md template

```markdown
# AGENTS.md

## Primary agent

| Field | Value |
|-------|-------|
| Name | [Name defined in SOUL.md] |
| Role | [Role in one sentence] |
| Model | [claude-opus-4 / claude-sonnet-4 / other] |
| Workspace | [workspace path] |
| Status | active |

### Permissions
- Read: everything
- Write: MEMORY.md, knowledge/, drafts
- External action: validation required

### Boot sequence
1. SOUL.md
2. USER.md
3. CONSTITUTION.md
4. AGENTS.md
5. MEMORY.md
6. knowledge/*.md

---

## Secondary agent (if applicable)

| Field | Value |
|-------|-------|
| Name | [Name] |
| Role | [Role in one sentence] |
| Model | [model] |
| Workspace | [workspace path] |
| Status | active / inactive |

### Permissions
- Read: [restricted scope]
- Write: [restricted scope]
- External action: [specific rules]

### Boot sequence
1. SOUL.md (specific to this agent)
2. USER.md (shared)
3. CONSTITUTION.md (specific to this agent)
4. AGENTS.md (shared)
5. MEMORY.md (shared or specific)

---

## Inter-agent communication

| From | To | Channel | Content |
|------|----|---------|---------| 
| [Agent 1] | [Agent 2] | [MEMORY.md / file / API] | [Type of information] |

## Notes
- [Additional rules, constraints, change history]
```

## Common mistakes

**No AGENTS.md with a single agent**: You think it's unnecessary. Then you add a second agent 3 months later and can't remember the boot sequence of the first one.

**Boot sequence not documented**: The agent reads files in a default order that may not match your intention. Be explicit.

**Identical permissions for all agents**: If two agents have the same permissions, they will probably get in each other's way. Differentiate.

**Forgetting the status**: An agent disabled but still in AGENTS.md can create confusion. Mark it "inactive" or remove it.

## Verification

- [ ] Each agent has an entry in AGENTS.md
- [ ] Role defined in one sentence per agent
- [ ] Model specified for each agent
- [ ] Explicit permissions (read, write, external action)
- [ ] Boot sequence documented
- [ ] If multi-agent: communication channels defined

---
