---
---
status: complete
audience: both
chapter: 04
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: en
---

# 4. Personalization

> Make your agent truly YOURS -- your voice, your rules, your workflows, your identity.

Configuration (chapter 3) makes the agent functional. Personalization makes it indispensable. This chapter covers shaping the agent's voice and tone, setting up a task system, automating recurring routines, and establishing trust and security boundaries. By the end, you'll have an agent that speaks like you, executes your workflows, and knows exactly where its authority ends.

For country-specific adaptations (regulations, local ecosystem), see chapter 7 (Localization).

---

## Contents

### Part A -- Identity and Voice

- **4.1 -- [Write your system prompt](01-system-prompt.md)**
  Draft the foundational text that determines how the agent thinks, responds, and behaves

- **4.2 -- [Personality and tone](02-personnalite-ton.md)**
  Calibrate register, formality level, and cases where the agent should not imitate you

- **4.3 -- [Iteration: your first version won't be right](03-iteration.md)**
  Method to converge in 2-3 rounds toward a prompt that sounds just right

### Part B -- Task System

- **4.4 -- [Why a task system](04-pourquoi-taches.md)**
  Move from an agent that advises to an agent that acts and reports

- **4.5 -- [How tasks get done](05-comment-taches.md)**
  The concrete workflow: agent proposes, you validate, it executes, it reports

- **4.6 -- [Database as source of truth](06-db-source-verite.md)**
  Use PostgreSQL instead of Markdown files to store tasks and their status

### Part C -- Workflows and Routines

- **4.7 -- [Recognize a routine](07-reconnaitre-routine.md)**
  Identify repetitive tasks (3+ occurrences, predictable pattern) that are candidates for automation

- **4.8 -- [Dry run before trust](08-dry-run.md)**
  Test each automation in "show me" mode before letting the agent act alone

- **4.9 -- [WORKFLOWS.md](09-workflows-md.md)**
  Document each procedure in a standardized format the agent can follow to the letter

- **4.10 -- [The weekly rhythm](10-rythme-hebdo.md)**
  Establish the preview Monday / review Friday cycle, prepared automatically by the agent

### Part D -- Security and Trust

- **4.11 -- [Trust is a configuration](11-confiance-configuration.md)**
  Define the rights pyramid: read-only, proposal, supervised execution, autonomy

- **4.12 -- [The boundary prompt](12-boundary-prompt.md)**
  Write the definitive list of what the agent must never do, under any circumstances

- **4.13 -- [Audit: what can your agent access?](13-audit-acces.md)**
  Run a self-audit to verify that actual access matches your intentions

- **4.14 -- [Bilingual configuration](14-config-bilingue.md)**
  Manage French, English, or both, and define the switching rules

---

[Contribute to this chapter](https://github.com/alexwill87/openclawfieldplaybook/issues/new?template=suggestion.yml) -- [CONTRIBUTING.md](../../CONTRIBUTING.md)

---
