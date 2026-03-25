# Contributing to the OpenClaw Field Playbook

Welcome. Every contribution improves a resource used by entrepreneurs and AI agents worldwide.  
This guide explains how to contribute — whatever your level.

---

## Before you start

Read `MANIFESTE.md`. It is two pages. It explains what this project is, what it is not, and how it is governed. Understanding it will save you time.

---

## Three levels of contribution

### T3 — Open to everyone, merged quickly
Typos, broken links, outdated information, reformulations, example additions.  
→ Open an Issue with the `correction` template, or submit a Pull Request directly.  
→ The AI agent reviews and the maintainer merges quickly if non-controversial.

### T2 — Community editable, reviewed by maintainer
New subsections, rewritten sections, new use cases, translated content.  
→ Open an Issue first (use the `suggestion` template) or fork + PR directly.  
→ The AI agent analyses your PR. A maintainer reviews and merges.

### T1 — Fixed structure, founder decision only
The five chapter titles (Definition, Installation, Configuration, Personalisation, Maintenance).  
→ Open an Issue labelled `governance` to propose changes.  
→ These decisions are made by the founder after community discussion.

---

## How to open an Issue

1. Go to the **Issues** tab
2. Click **New Issue**
3. Choose a template: `suggestion` or `correction`
4. Fill in the template — be specific
5. Submit

The AI agent will post an analysis within minutes. No action needed from you after that.

---

## How to submit a Pull Request

**If you have never used GitHub:**

1. **Fork** this repository (button top-right)
2. Edit the file you want to change in `sections/`
3. **Commit** with a clear message:
   - `fix: typo in section 02-installation`
   - `feat: add use case for freelance invoice workflow`
   - `refactor: rewrite section 03 intro for clarity`
4. Open a **Pull Request** from your fork to this repo
5. Fill in the PR template
6. The AI agent comments. The maintainer reviews.

**One PR = one change.** Do not bundle multiple unrelated changes.

---

## Section format

Every T2 section follows this structure:

```markdown
---
status: draft | review | complete
audience: human | agent | both
chapter: 01 | 02 | 03 | 04 | 05 | 06
last_updated: YYYY-MM
contributors: [names or GitHub handles]
---

## [Section title]

**Who this is for:** one line  
**Time required:** estimate  
**Difficulty:** Beginner / Intermediate / Advanced

### Context
Why this matters. What problem it solves.

### Step-by-step
The actual content.

### Common mistakes
What goes wrong and how to avoid it.

### 🇫🇷 French context
Adaptations for French-speaking organisations or teams.

### Template
```
Copy-paste ready prompt or configuration block.
```
```

---

## Content standards

- Write from experience. Label speculation explicitly.
- Be direct. Remove words that do not add meaning.
- No half-written sections. Complete it or leave a placeholder.
- One source of truth. Cross-reference instead of duplicating.

---

## Language

Write in English or French — both are welcome.  
If you write in French, the AI agent will flag it for a French-context block if one does not exist.

---

## Questions

Open an Issue labelled `question`. No question is too basic.
