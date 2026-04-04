---
status: complete
audience: both
chapter: 01
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: en
---

# 1.5 -- The mental architecture before you start

**This section is for:** Anyone who will install and configure OpenClaw. Read this before touching the terminal.
**Reading time:** 12 minutes.
**Difficulty:** Intermediate.

### Context

Before you run a single `docker compose up`, you need a clear mental model of what you're building. Without this model, every configuration decision will be a shot in the dark.

### The 3 layers

Every OpenClaw installation is organized into three stacked layers:

```
+------------------------------------------+
|            3. ACTION                      |
|  What your agents do concretely          |
|  (send, create, modify, alert)           |
+------------------------------------------+
|            2. VISIBILITY                  |
|  What your agents know                   |
|  (memory, context, tools, data)          |
+------------------------------------------+
|            1. IDENTITY                    |
|  Who your agents are                     |
|  (roles, rules, limits, personality)     |
+------------------------------------------+
```

**Layer 1 -- Identity.** This is the foundation. Before you give tools to an agent, define who it is. What is its role? What are its limits? What is it allowed to do and not do? An agent without clear identity is a dangerous agent -- not because it's malicious, but because it's unpredictable.

**Layer 2 -- Visibility.** Once identity is set, define what the agent knows. What data does it have access to? What is its memory? Which tools can it use? An agent with clear identity but no visibility is a powerless agent.

**Layer 3 -- Action.** Finally, define what the agent does. What concrete actions can it take? Under what conditions? With what validations? An agent with identity + visibility + capacity for action is an operational agent.

> **Principle:** Always build from the bottom up. Identity first, visibility next, action last. Reversing this order is the most frequent source of problems.

### The concept of "pillars"

A pillar is a **functional block** that structures an OpenClaw installation. Think of it as a domain of responsibility.

There are two categories:

**Universal pillars** -- present in every installation, regardless of your field:

| Pillar | Responsibility |
|--------|---------------|
| **Infra** | The technical infrastructure. Server, Docker, reverse proxy, SSL certificates, backups. It's the ground on which everything rests. |
| **Agents** | The agents themselves. Their configuration, orchestration, interactions. |
| **Knowledge** | The knowledge base. Memory, context, reference documents, business rules. |

**Business pillars** -- specific to your activity:

These pillars depend on what you do. Examples:

| Business | Possible business pillars |
|----------|------------------------|
| Independent consultant | Prospecting, Deliverables, Billing |
| E-commerce | Catalog, Orders, Customer service |
| Agency | Projects, Clients, Production |
| Trainer | Content, Learners, Scheduling |

You don't need to define all your business pillars before you start. Begin with the universal pillars. The business pillars will emerge naturally as you use the system.

> **Common mistake:** Trying to define the complete architecture before you begin. You can't foresee everything. Lay down the universal pillars, build your first functional agent, and let the architecture evolve with usage.

> **Field note:** In the installations we've supported, business pillars generally stabilize after 2 to 4 weeks of real-world usage. Not before. Any attempt to lock them in beforehand produces an architecture that doesn't match reality.
