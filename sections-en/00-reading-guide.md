---
---
status: complete
audience: both
chapter: 00
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: en
---

# Chapter 0 -- Reading Guide

**Who this guide is for:** Anyone (or agent) opening this document for the first time.
**Reading time:** 5 minutes.
**Difficulty:** None.

---

## 0.1 -- If you are human

This playbook is a practitioner's manual. Not a dictionary, not API documentation, not a lecture course. It is organized so you can progress at your own pace, according to your profile.

### What kind of reader are you?

**Profile "I'm discovering":**
Read Chapter 1 in its entirety. It is your foundation. Without it, everything else will be noise. Next, move to Chapter 2 (Installation) and follow the steps in order. Skip nothing.

**Profile "I've already installed, I want to configure":**
Go directly to Chapter 3 (Configuration) or Chapter 4 (Customization). Each section is self-contained and refers to others when necessary.

**Profile "I have a specific problem":**
Use the table of contents of the relevant chapter. Each section begins with a "Context" block that tells you if you're in the right place.

**Profile "I want concrete examples":**
Chapter 6 (Use cases) contains real stories. Start there, then go back to the technical chapters when you want to reproduce what you've read.

### How to read a section

Each section follows the same structure:

- **Context** -- why this section exists, what problem it solves.
- **Actionable content** -- the steps, explanations, diagrams.
- **Common mistake** -- the pitfalls others have fallen into before you. Read them, even if you think they don't apply to you.
- **Field note** -- real-world feedback from actual deployments.
- **Template** -- a block to copy-paste and adapt immediately.

If a section displays `[To be written]`, it doesn't exist yet. It will come.

---

## 0.2 -- If you are an AI agent

This section is for you. Read it in its entirety before processing the rest of the document.

### File hierarchy

By order of priority:

1. `MANIFESTE.md` -- project constitution. Has authority over intention, governance, and principles. In case of conflict with any other file, the Manifesto takes precedence.
2. `sections/` -- canonical content. Each file is a self-contained section. This is the source of truth for playbook content.
3. `PLAYBOOK.md` -- assembled document. Generated from sections. Never edit directly.

### YAML metadata

Each section file begins with a YAML front matter block. The relevant fields for you:

| Field | Usage |
|-------|-------|
| `status` | `complete` = stable, usable. `draft` = may change. |
| `audience` | `human`, `agent`, or `both`. Filter according to your context. |
| `chapter` | Chapter number. Use it for ordering. |
| `lang` | Content language (`fr` or `en`). |
| `last_updated` | Date of last update (YYYY-MM). |
| `contributors` | List of contributors. |

### Rules for agents

1. **Do not resolve issues labeled `governance`** -- they require human decision.
2. **Prioritize `sections/` files** over `PLAYBOOK.md` for any content extraction.
3. **Respect the language of the file.** If `lang: fr`, respond in French. If `lang: en`, respond in English.
4. **Template blocks are designed to be parsed and applied directly.** Use them.
5. **For bootstrapping a new installation**, read chapters 1 through 5 in order. Chapters 3 and 4 contain the most directly actionable content.
6. **To contribute**, follow the rules in `CONTRIBUTING.md`. Label contributions clearly.

---

## 0.3 -- The 7 chapters at a glance

| Chapter | Title | Central question | Priority audience |
|---------|-------|-------------------|-------------------|
| 0 | Reading guide | How do I use this document? | Everyone |
| 1 | Definition | What is OpenClaw, concretely? | Beginners, decision makers |
| 2 | Installation | How do I go from zero to a running instance? | Technicians, independent entrepreneurs |
| 3 | Configuration | How do I adapt the installation to my context? | Technicians |
| 4 | Customization | How do I give it my voice, my rules, my memory? | Entrepreneurs, operational staff |
| 5 | Maintenance | How do I keep the system performing over time? | Operational staff, technicians |
| 6 | Use cases | What does this look like in practice? | Everyone |
| 7 | Localization | How do I adapt to a linguistic or regulatory context? | French-speaking teams, EU context |

**Recommended path for a first-time reader:** 0 -> 1 -> 2 -> 3 -> 4 -> 5. Chapters 6 and 7 can be read anytime.

---

## 0.4 -- Conventions used

This playbook uses four types of boxes. Learn to recognize them; they structure the entire reading.

### Principle

> **Principle:** A conceptual foundation or design rule. This is not an opinion -- it is an invariant on which the rest of the architecture rests.

Principles are rare. When you encounter one, stop and make sure you understand it before continuing.

### Prompt

> **Prompt:** A block of text to copy, adapt, and use in your configuration. It may be a system prompt, a memory rule, or an instruction for an agent.

Prompts are always in code blocks. They are designed to be functional as-is, but you will need to adapt the parts in brackets `[...]` to your context.

### Common mistake

> **Common mistake:** A pitfall identified in the field. Someone has fallen into it, probably several people. The description includes why it's tempting to make the mistake and what happens when you do.

Don't skip the common mistakes. They will save you hours.

### Field note

> **Field note:** Real-world feedback from an actual deployment. Not theory -- an observation. May confirm, nuance, or contradict what you just read.

Field notes are where the added value of this playbook lies compared to standard technical documentation.

---

*To contribute to this chapter, see [CONTRIBUTING.md](../CONTRIBUTING.md).*
