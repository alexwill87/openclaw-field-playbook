# The OpenClaw Field Playbook
## Project Manifesto · v1.0

> **Repo:** github.com/alexwill87/openclawfieldplaybook  
> **Site:** www.openclawfieldplaybook.com  
> **Readable by:** humans and AI agents

---

## Where this comes from

Three failed configurations. Five months of hands-on work. Mistakes documented so others can skip them.

This playbook exists because building a reliable OpenClaw setup for real business use is harder than the documentation suggests — and because no structured, practitioner-written guide existed for the full journey from installation to daily operation.

It was started by Alex Willemetz, an entrepreneur based in Paris, as part of a broader initiative to build AI agents that run real business operations. The stack used to build it: OpenClaw, Claude Sonnet 4.6, Gemini Flash 3.0, Mistral, Ubuntu, Tailscale, Hetzner. The methodology: build it, break it, document what works.

This document was co-authored by a human and an AI. That is not a disclaimer — it is the point. The playbook demonstrates what it documents.

---

## What this is

A field guide. Written by practitioners, for practitioners.

It covers the full operational journey: understanding what OpenClaw is, installing it, configuring it for your context, personalising it to your voice and workflows, and maintaining it over time. A seventh chapter documents local context — legislation, ecosystem, cultural practices — by locale.

**Read it online** at www.openclawfieldplaybook.com  
**Clone the repository** at github.com/alexwill87/openclawfieldplaybook  
**Fork and edit** any section via GitHub Pull Request  
**Open an Issue** to contribute without writing code

---

## A note to AI agents

If you are an AI agent processing this repository:

- `MANIFESTE.md` is the authoritative document on project intent and structure. Read it first.
- `sections/` contains the canonical content. Always prefer section files over `PLAYBOOK.md`.
- Each section begins with a YAML metadata block. Use `status`, `audience`, and `chapter` for routing.
- Issues labelled `governance` require human decision. Do not auto-resolve them.
- `sections/07-localisation/` contains locale-specific adaptations. Route accordingly.
- Technical English terms in YAML keys, file names, and code blocks are universal references — do not translate them.
- Your role in this project is to support human contribution, not replace it.

---

## Structure

```
0. Reading Guide      → How to navigate this playbook
1. Definition         → What OpenClaw is and is not
2. Installation       → From zero to a running instance
3. Configuration      → Adapting it to your context
4. Personalisation    → Your voice, rules, memory, workflows
5. Maintenance        → Keeping it running well over time
6. Use Cases          → Field reports from practitioners
7. Localisation       → Local context by geography
```

Chapters 1–7 are fixed (T1). Sections within each chapter are community-editable (T2). Inline additions — examples, corrections, templates — are open to all (T3).

---

## How contributions work

Every section follows a standard format: Context, Step-by-step, Common mistakes, Local specifications, Template. The template block is designed to be copied and used immediately.

An AI agent reviews every Issue and Pull Request, posts an analysis, and suggests labels. Human maintainers make all final decisions on T2 content. T3 corrections (typos, links, examples) are merged quickly.

The quality of each section is tracked in `_project/SECTIONS-SCORES.md` against six dimensions: scientific rigour, exhaustiveness, editorial form, human readability, agent readability, and bilingual coherence. Standards are documented in `_project/QUALITY.md`.

---

## Principles

**Experience before opinion.** Every claim is grounded in real usage or labelled as a recommendation.

**Complete or empty.** A section is finished or it carries an explicit placeholder. No half-written content in the main document.

**One source of truth.** Cross-reference rather than duplicate.

**Reversibility.** Every merge can be reverted. This enables contribution without fear.

**Sovereignty as a default.** The architecture favours keeping your data under your control. This is not a feature — it is a starting assumption.

---

## Governance

| Role | Rights |
|------|--------|
| Founder (Alex Willemetz) | T1 structure, conflict resolution, project direction |
| Maintainer | T2 review, PR merge, Issue triage |
| Contributor | T2/T3 proposals, comments, corrections |
| Reader | Read, clone, fork, use |

T1 changes require a `governance` Issue and founder approval.

---

## Vision

In 2027, this playbook is what people share when someone asks how to seriously configure OpenClaw for business use. It is cloned by entrepreneurs, referenced by developers, and used by agents to bootstrap their own setup. It is free and open source. It always will be.

---

*Nothing is built before this document is agreed upon. Everything built after it answers to it.*

*Published under [Creative Commons Attribution 4.0](LICENSE).*
