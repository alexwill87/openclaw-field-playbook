---
---
status: complete
audience: both
chapter: 03
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: en
---

# 3.8 -- The knowledge/ folder

## Context

knowledge/ is the cold memory of the agent. The knowledge that doesn't change every week. References, processes, durable business information.

Unlike MEMORY.md (80 lines, volatile), knowledge/ has no global size limit. But each file must remain readable and focused: one file per topic, 200 lines max per file.

## Organization by domain

Recommended structure:

```
knowledge/
  infra/
    stack-technique.md
    deploiement.md
    monitoring.md
  business/
    clients-principaux.md
    tarification.md
    processus-vente.md
  guides/
    onboarding-nouveau-client.md
    procedure-incident.md
    checklist-livraison.md
  contacts/
    equipe.md
    partenaires.md
```

Three to four top-level folders. No more. If you need more, you're probably trying to document too much.

## Organization rules

### One file per topic

Bad:
```
knowledge/tout-sur-le-business.md  (300 lines, 15 topics)
```

Good:
```
knowledge/business/tarification.md     (60 lines)
knowledge/business/clients-principaux.md  (80 lines)
knowledge/business/processus-vente.md     (70 lines)
```

### Cross-reference instead of duplication

If the deployment process mentions monitoring, don't copy the monitoring section. Make a reference:

```markdown
## Deployment
[...]
For post-deployment monitoring, see [monitoring.md](../infra/monitoring.md).
```

Duplication creates contradictory information from the first forgotten update.

### 200 lines max per file

Beyond 200 lines, the file probably covers multiple topics. Break it up.

### Explicit file names

The file name should be enough to understand its content. No `notes.md`, `misc.md`, `temp.md`.

## Examples of good organization

### Freelancer / consultant

```
knowledge/
  clients/
    client-alpha.md        -- context, contacts, history
    client-beta.md
  metier/
    tarifs-2026.md          -- current pricing grid
    modele-proposition.md   -- structure of business proposals
  guides/
    onboarding-client.md    -- checklist from first contact to delivery
    facturation.md          -- invoicing process
```

### Technical startup

```
knowledge/
  infra/
    architecture.md         -- infrastructure diagram
    runbooks.md             -- emergency procedures
    secrets-management.md   -- where secrets are, how to access them
  produit/
    roadmap-q2-2026.md      -- quarterly product priorities
    metriques.md            -- tracked KPIs, alert thresholds
  equipe/
    roles.md                -- who does what
    rituels.md              -- meetings, standups, retros
```

### SME manager

```
knowledge/
  business/
    offre-services.md       -- service offering description
    clients-top-10.md       -- top 10 clients, context
    pipeline-commercial.md  -- ongoing opportunities
  operations/
    processus-recrutement.md
    processus-achat.md
  legal/
    contrats-types.md       -- standard clauses, points of attention
    rgpd.md                 -- obligations, processing register
```

## Step by step

### 1. Create the folder structure

Start with 3 folders maximum. You can always add more later.

### 2. Migrate from MEMORY.md

Review MEMORY.md. Anything that has been stable for more than 2 weeks should migrate to knowledge/. Replace the entry in MEMORY.md with a reference:

```
Before (MEMORY.md):
- Deployment process: build > test > staging > validation > prod

After (MEMORY.md):
- Deployment process documented in knowledge/infra/deploiement.md
```

### 3. Document your 5 most frequent topics

What are the 5 topics you explain the same way at every session? Document them in knowledge/.

### 4. Set up quarterly review

Every quarter, go through knowledge/:
- Delete obsolete files
- Update outdated information
- Merge files that are too small, split files that are too large

## Common mistakes

**Empty knowledge/** : The agent starts from scratch on core topics at every session. Massive waste of time.

**One large file** : `knowledge/everything.md` with 800 lines. Impossible to maintain, impossible to read efficiently.

**Duplication** : The same information in 3 files. At the first update, 2 out of 3 files are obsolete.

**Orphaned files** : Files that nobody reads and nobody maintains. If a file hasn't been useful in 3 months, delete it or archive it.

**Vague names** : `notes.md`, `idees.md`, `a-traiter.md`. Names that say nothing about the content.

## Checklist

- [ ] The knowledge/ folder exists with a domain-based structure
- [ ] Each file covers a single topic
- [ ] No file exceeds 200 lines
- [ ] No duplication between files (cross-references instead)
- [ ] File names are explicit
- [ ] Your 5 most frequent topics are documented
- [ ] A quarterly review date is scheduled
