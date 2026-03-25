# SECTIONS-SCORES.md — Quality Dashboard
## The OpenClaw Field Playbook

> **Automated.** Updated by the quality agent after each audit run.  
> Do not edit manually — scores are written by the agent following QUALITY.md protocol.  
> Source of truth for section readiness and publication decisions.

---

## Scoring scale reminder

| Score | Meaning |
|-------|---------|
| 1 | Absent or non-functional |
| 2 | Present but insufficient |
| 3 | Acceptable — publishable with minor fixes |
| 4 | Good — ready to publish |
| 5 | Reference quality |

**Thresholds:**
- Average ≥ 3.0 → eligible for `status: review`
- Average ≥ 4.0 → eligible for `status: complete`

---

## Dimensions key

| Code | Dimension |
|------|-----------|
| D1 | Scientific rigour |
| D2 | Exhaustiveness |
| D3 | Editorial form |
| D4 | Human readability |
| D5 | Agent readability |
| D6 | Bilingual coherence |

---

## Current scores

| Section | Status | D1 | D2 | D3 | D4 | D5 | D6 | Avg | Last audit | Audited by |
|---------|--------|----|----|----|----|----|----|-----|------------|------------|
| 00-reading-guide.md | draft | — | — | — | — | — | — | — | not run | — |
| 01-definition/README.md | draft | — | — | — | — | — | — | — | not run | — |
| 02-installation/README.md | draft | — | — | — | — | — | — | — | not run | — |
| 03-configuration/README.md | draft | — | — | — | — | — | — | — | not run | — |
| 04-personalisation/README.md | draft | — | — | — | — | — | — | — | not run | — |
| 05-maintenance/README.md | draft | — | — | — | — | — | — | — | not run | — |
| 06-use-cases/README.md | draft | — | — | — | — | — | — | — | not run | — |
| 07-localisation/fr-FR.md | — | — | — | — | — | — | — | — | not created | — |
| 07-localisation/en-US.md | — | — | — | — | — | — | — | — | not created | — |

---

## Audit history

*Entries are appended here after each agent audit run.*

---

### [No audits run yet]

*First audit will run when sections have content.*  
*To trigger: ask the quality agent to run QUALITY.md on a specific section file.*

---

## How to trigger an audit

**Manual (human):**
> "Run the quality audit on sections/01-definition/README.md and update SECTIONS-SCORES.md"

**Automatic (agent):**
The quality agent runs automatically when a PR changes a section file and the PR is labelled `quality-check`.

**Batch:**
> "Run the quality audit on all sections with status: draft and update the scores table"

---

## Interpretation guide

**For a section at `status: draft`:**
- Run audit to identify the highest-priority gaps
- Focus on D3 (form) and D1 (rigour) first — they unblock everything else

**For a section at `status: review`:**
- All dimensions should be ≥ 3
- D6 (bilingual coherence) must have fr-FR entry in progress

**For a section targeting `status: complete`:**
- All dimensions must be ≥ 4
- D6 fr-FR entry must exist and be complete
- A human maintainer must confirm the score independently
