---
---
status: complete
audience: both
chapter: 05
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: en
---

# 5. Maintenance

> Keep your OpenClaw setup performant, reliable, and trustworthy over time.

A well-installed and configured agent remains reliable only if it is maintained. This chapter covers daily operations (logs, backups, health checks), agent maintenance itself (prompt, memory, errors), infrastructure management (updates, secrets, monitoring), and medium-term evolution (multi-agents, model changes, ROI measurement). By the end, you will know how to diagnose a problem, prevent drift, and evolve your setup without breaking it.

For country-specific regulatory adaptations, see chapter 7 (Localization).

---

## Table of Contents

### Part A -- Daily Operations

- **5.1 -- [Daily health check](01-health-check.md)**
  Automate a complete infrastructure diagnosis with cron and Telegram alerts

- **5.2 -- [Log management](02-logs.md)**
  Locate logs, read them effectively, configure rotation and spot warning signals

- **5.3 -- [Backups](03-backups.md)**
  Set up pg_dump, Hetzner snapshots and critical file backups, then test restoration

### Part B -- Agent Maintenance

- **5.4 -- [Review the system prompt](04-revoir-system-prompt.md)**
  Know when and how to rewrite the prompt without losing what already works

- **5.5 -- [Memory drift](05-derive-memoire.md)**
  Detect and clean obsolete or contradictory information in the agent's memory

- **5.6 -- [When the agent makes mistakes](06-agent-se-trompe.md)**
  Apply the diagnostic, correction, prevention protocol for each error

- **5.7 -- [Update integrations](07-maj-integrations.md)**
  Adapt connections when an API changes, without breaking existing workflows

### Part C -- Infra Maintenance

- **5.8 -- [System updates](08-maj-systeme.md)**
  Plan Ubuntu, Docker, Node.js and Vault updates -- and know when not to do them

- **5.9 -- [Secrets rotation](09-rotation-secrets.md)**
  Renew credentials on a defined schedule, without service interruption

- **5.10 -- [Monitoring and alerts](10-monitoring.md)**
  Choose between three levels: cron+Telegram, Uptime Kuma, or Grafana depending on your needs

- **5.11 -- [In case of outage](11-en-cas-de-panne.md)**
  Consult the diagnostic table by symptom with for each case: cause, fix and prevention

### Part D -- Evolution

- **5.12 -- [When to add a second agent](12-deuxieme-agent.md)**
  Recognize the signs, structure isolation and define inter-agent communication

- **5.13 -- [Migrating to another model](13-migrer-modele.md)**
  Test a new model in A/B comparison without cutting off the production model

- **5.14 -- [Measuring ROI](14-mesurer-roi.md)**
  Quantify time saved, decisions improved and errors avoided

---

[Contribute to this chapter](https://github.com/alexwill87/openclawfieldplaybook/issues/new?template=suggestion.yml) -- [CONTRIBUTING.md](../../CONTRIBUTING.md)

---
