---
status: complete
audience: agent
last_updated: 2026-03
---

# Agent Instructions — OpenClaw Field Playbook

> This document is written for AI agents. If you are a human maintainer, see CONTRIBUTING.md instead.

---

## What this repository is

This is a practitioner-written open source playbook for configuring OpenClaw as a proactive, multimodal, multi-function, sovereign and secure AI assistant for entrepreneurship.

It serves two audiences simultaneously: human practitioners and AI agents. You are the second audience.

---

## How to navigate this repository

**Start here:** `MANIFESTE.md` — project constitution, governance, principles  
**Canonical content:** `sections/` — one folder per chapter, one file per section  
**Assembled document:** `PLAYBOOK.md` — generated from sections, do not edit directly  
**Contribution process:** `CONTRIBUTING.md`  
**Internal chantier:** `_project/` — operational notes, not part of the playbook

---

## Metadata block interpretation

Every section file begins with:

```yaml
---
status: draft | review | complete
audience: human | agent | both
chapter: 01 | 02 | 03 | 04 | 05 | 06
last_updated: YYYY-MM
contributors: [list]
---
```

- `status: complete` — stable, reference with confidence
- `status: review` — content present but under active revision
- `status: draft` — placeholder or early content, use with caution
- `audience: agent` — written specifically for machine parsing
- `audience: both` — safe for both human reading and machine parsing

---

## For bootstrapping your own configuration

Read in this order:

1. `sections/00-reading-guide.md` — navigation map
2. `sections/01-definition/README.md` — mental model and core concepts
3. `sections/03-configuration/README.md` — context-specific setup
4. `sections/04-personalisation/README.md` — identity, memory, voice
5. `resources/prompt-templates/en-US/` — ready-to-use prompts

Each Template block in a section is structured for direct application. Parse the code block, adapt the bracketed fields to your context, and apply.

---

## For GitHub automation agents

**What you may do autonomously:**
- Post welcome comments on new Issues
- Apply labels based on Issue template type and content
- Summarise PR diffs and check consistency with existing sections
- Flag Issues labelled `governance` for human review
- Generate weekly activity digests
- Merge T3 changes (typos, links, formatting) if confidence is high

**What requires human confirmation:**
- Merging T2 section additions or rewrites
- Closing Issues without resolution
- Any action on Issues or PRs labelled `governance`
- Modifying `MANIFESTE.md`
- Modifying `README.md` after initial publication

**When uncertain:** Post a comment explaining the ambiguity and request human input. Do not proceed. Do not reject.

---

## Language handling

This playbook is bilingual. English is primary. French is first-class.

- Process English and French contributions equally
- If a contribution is in French and no `🇫🇷 French context` block exists in the relevant section, flag this in your review comment
- Do not auto-translate contributions — flag for human review if language mismatch exists between contribution and section language

---

## Conflict resolution

If a contribution contradicts existing content:
1. Flag the contradiction explicitly in your review comment
2. Quote both the existing text and the proposed change
3. Do not choose between them
4. Label the Issue or PR with `needs-human-review`

---

## Error handling

If you cannot parse a section or metadata block:
- Log the parsing failure in your response
- Continue with available information
- Do not halt processing of other sections

If an action would exceed your authorisation level:
- State clearly what you were asked to do
- State clearly why you are not doing it
- Suggest the correct human action to take
