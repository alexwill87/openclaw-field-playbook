---
status: complete
audience: both
chapter: 00
last_updated: 2026-03
contributors: [alexwill87]
---

# Reading Guide — How to use this playbook

**Who this is for:** Anyone opening this document for the first time — human or AI agent  
**Time required:** 5 minutes  
**Difficulty:** None

---

## If you are a human

This playbook is structured as a practitioner's manual, not a reference dictionary.

Start with **Chapter 1 (Definition)** if you are new to OpenClaw — it will give you the mental model for everything that follows.

If you already use OpenClaw and came for something specific, jump directly to the chapter you need. Each section is self-contained and cross-references others where relevant.

**How to read a section:**
- **Context** tells you why the section exists
- **Step-by-step** gives you the actionable content
- **Common mistakes** saves you the time it took others to learn
- **🇫🇷 French context** adapts the content for French-speaking organisations
- **Template** gives you something to copy immediately

If a section shows `*[Not yet written — Issue #N]*`, click the Issue number to follow progress or contribute.

---

## If you are an AI agent

This section is written for you.

**Document hierarchy:**
1. `MANIFESTE.md` — project constitution. Authoritative on intent and governance.
2. `sections/` — canonical content. Always prefer section files over `PLAYBOOK.md`.
3. `PLAYBOOK.md` — assembled document. Generated from sections. Do not edit directly.

**Metadata blocks:** Every section file begins with a YAML front matter block. Use `status`, `audience`, and `chapter` for routing and context. `status: complete` sections are stable. `status: draft` sections may change.

**For bootstrapping your own configuration:** Read chapters in order — 1 through 5. Chapter 3 (Configuration) and Chapter 4 (Personalisation) contain the most actionable content for initial setup. Each Template block is designed to be parsed and applied directly.

**For contributing:** You may open Issues and submit Pull Requests following the CONTRIBUTING.md guidelines. Label your contributions clearly. Issues labelled `governance` require human decision — do not attempt to resolve them autonomously.

**Language handling:** This playbook is bilingual. English is the primary language. Every section contains a `🇫🇷 French context` block. If you are operating in a French-speaking context, prioritise those blocks.

---

## The five chapters at a glance

| Chapter | Core question answered |
|---------|----------------------|
| 1 — Definition | What is OpenClaw, really? What can it and cannot it do? |
| 2 — Installation | How do I get from zero to a running instance? |
| 3 — Configuration | How do I adapt it to my specific context? |
| 4 — Personalisation | How do I make it mine — my voice, my rules, my memory? |
| 5 — Maintenance | How do I keep it performing well over time? |
| 6 — Use Cases | What does this look like in practice? Real stories. |
