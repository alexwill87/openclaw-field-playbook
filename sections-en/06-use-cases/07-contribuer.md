---
---
status: complete
audience: both
chapter: 06
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: en
---

# 07 -- How to Submit Your Use Case

**For whom:** anyone or team using OpenClaw in a real-world situation
**Time required:** 30 minutes to 1 hour
**Difficulty:** Beginner

---

## Why contribute

Use cases are the most useful part of this playbook. Each new case helps other practitioners to:
- Evaluate whether OpenClaw fits their situation
- Save time by reusing a tested configuration
- Avoid mistakes others have already made

Your experience, even if partial, has value. A use case doesn't need to be perfect to be useful.

---

## Standard format

Each use case follows this structure. You can copy this template directly.

```markdown
---
status: draft
audience: both
chapter: 06
last_updated: YYYY-MM
contributors: [your-github-handle]
lang: fr
---

# XX -- [Use Case Title]

**For whom:** [one-line profile]
**Setup time:** [estimate]
**Difficulty:** Beginner / Intermediate / Advanced

---

## Context

Who you are, what your organization does, team size.

## Problem

What you needed to solve or automate. Be specific.

## Configuration

Your infrastructure (server, OS, tools).
Your agents (how many, what roles).
Your approximate budget.

## Setup

The steps you followed, in chronological order.

## Result

What changed concretely. Numbers if possible (time saved, success rate, costs).

## Lessons Learned

What you would do differently. What worked better than expected.

## Common Mistakes

The pitfalls you encountered and how to avoid them.

## Template

A prompt, configuration, or reusable snippet for others.

## Verification

A checklist to validate that the configuration works.
```

---

## Option 1: Submit via GitHub Issue

This is the simplest method. No Git knowledge required.

1. Go to [github.com/alexwill87/openclawfieldplaybook/issues](https://github.com/alexwill87/openclawfieldplaybook/issues)
2. Click **New Issue**
3. Choose the **suggestion** template
4. In the title, write: `use-case: [your title]`
5. In the body, paste the standard format above and fill it in
6. Add the `use-case` label
7. Submit

An AI agent will analyze your Issue and post a comment. A human maintainer will validate and integrate the case into the chapter.

---

## Option 2: Submit via Pull Request

If you're comfortable with GitHub:

1. Fork the repo [alexwill87/openclawfieldplaybook](https://github.com/alexwill87/openclawfieldplaybook)
2. Create your file in `sections/06-use-cases/`
3. Name it with the next available number: `XX-short-title.md`
4. Use the standard format above
5. Add the YAML frontmatter with `status: draft`
6. Commit with a clear message: `feat: add use case for [your title]`
7. Open a Pull Request to the main repo

### PR rules:

- One file per use case
- YAML frontmatter is mandatory
- Initial status is always `draft`
- No personal data (clients, employers) without consent
- Amounts and metrics can be approximate; indicate if they are

---

## What makes a use case useful

| Criterion | Good example | Bad example |
|-----------|--------------|-------------|
| Specificity | "We reduced triage time from 3h to 45min" | "It worked well" |
| Reproducibility | Complete configuration with system prompt | "We set up an agent" |
| Honesty | "The agent makes mistakes on 15% of cases, here's how we handle it" | "It works perfectly" |
| Template | Copy-paste ready prompt | Vague prompt description |

---

## What we're particularly looking for

The following use cases are most requested by the community. If you have experience in any of these areas, your contribution will be especially valued:

- Craft / manual trades (estimates, project tracking, client follow-up)
- Medical profession (appointment scheduling, patient follow-up, compliance)
- Association / NGO (volunteer management, communication, reporting)
- Education (lesson preparation, student tracking, administration)
- Legal profession (case triage, legal research, compliance)
- Real estate (rental management, landlord relations, work tracking)

---

## After submission

1. An AI agent analyzes your contribution and posts a comment
2. A human maintainer reviews the use case
3. If adjustments are needed, they are requested via comment
4. The case is merged with `draft` status, then moves to `review`, then `complete`
5. The case appears in the chapter 6 table of contents

Typical processing time: 1 to 2 weeks.

---

## Frequently asked questions

**Is my case too simple to be useful?**
Yes, it is. Simple cases are often the most useful because they're accessible to more people.

**I can't share the details of my company.**
Anonymize. Replace names, exact amounts, and sensitive details with generic values. The format and experience are what matter.

**My use case didn't work.**
Share it anyway. A documented failure is as useful as a success. Explain what didn't work and why.

**I don't speak French.**
Contributions in English are welcome. A contributor or agent will handle the translation.

---

*Every use case submitted makes this playbook more useful for the next practitioner. Your experience matters.*

*[Submit via Issue](https://github.com/alexwill87/openclawfieldplaybook/issues/new?template=suggestion.yml) -- [CONTRIBUTING.md](../../CONTRIBUTING.md)*

---
