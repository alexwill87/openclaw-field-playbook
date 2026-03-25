# PROJECT.md — The OpenClaw Field Playbook
## Master Reference Document

> **Scope:** March 24–26, 2026 — from empty repo to contributor-ready at the AI Tinkerers meetup  
> **Location:** `_project/PROJECT.md` — internal, ephemeral after launch  
> **Maintained by:** Alex Willemetz + Claude (Anthropic)

---

## Table of Contents

1. [Project overview](#1-project-overview)
2. [Repository map](#2-repository-map)
3. [Document registry](#3-document-registry)
4. [Agents and roles](#4-agents-and-roles)
5. [Working rules (until Thursday)](#5-working-rules-until-thursday)
6. [Workflow: creation](#6-workflow-creation)
7. [Workflow: validation and deployment](#7-workflow-validation-and-deployment)
8. [Planning](#8-planning)
9. [Definition of done](#9-definition-of-done)

---

## 1. Project overview

### What we are building
An open source playbook — `github.com/alexwill87/openclawfieldplaybook` — designed to be the global reference for configuring OpenClaw as a proactive, multimodal, multi-function, sovereign and secure AI assistant for entrepreneurship.

### Why now
No structured, practitioner-written guide exists. The AI Tinkerers Paris meetup on March 26 (École 42 × HEC Vibe × AI Tinkerers, ~100 participants) is a launch window. The room will contain ideal early contributors.

### The dual audience
Every document serves two readers simultaneously:
- **Humans** — entrepreneurs from solo freelancers to enterprise teams, especially French-speaking
- **AI agents** — an OpenClaw instance can ingest this playbook to complete its own configuration

This dual readership is a strategic differentiator. It is built into every structural decision.

### Strategic objective
Visibility + credibility + high-quality encounters. This playbook establishes Alex as a trusted, useful practitioner in the OpenClaw community — and creates a foundation for future services (not documented here).

---

## 2. Repository map

```
openclaw-field-playbook/
│
├── MANIFESTE.md              ← Constitution. Read first. Never edit lightly.
├── README.md                 ← Front door for new visitors
├── PLAYBOOK.md             ← Assembled document (auto-generated from sections/)
├── CONTRIBUTING.md           ← Onboarding for contributors
├── ROADMAP.md                ← Direction and milestones
├── CODE_OF_CONDUCT.md        ← Community rules
├── LICENSE                   ← CC-BY 4.0
│
├── sections/                 ← THE CONTENT (canonical source)
│   ├── 00-reading-guide.md   ← How to use this playbook
│   ├── 01-definition/        ← Chapter 1: What is OpenClaw?
│   ├── 02-installation/      ← Chapter 2: Getting started
│   ├── 03-configuration/     ← Chapter 3: Your context
│   ├── 04-personalisation/   ← Chapter 4: Your identity
│   ├── 05-maintenance/       ← Chapter 5: Long-term operation
│   └── 06-use-cases/         ← Chapter 6: Field reports
│
├── resources/
│   ├── prompt-templates/
│   │   ├── en/               ← English prompt templates
│   │   └── fr/               ← French prompt templates
│   └── agent-instructions/   ← Structured guidance for AI agents
│
├── _project/                 ← INTERNAL CHANTIER (ephemeral, not part of playbook)
│   ├── PROJECT.md            ← This file
│   ├── TRACKER.md            ← Live status of all tasks
│   ├── RULES.md              ← Working rules Alex + Claude
│   └── setup.sh              ← One-command GitHub repo creation script
│
└── .github/
    ├── ISSUE_TEMPLATE/
    │   ├── suggestion.yml
    │   └── correction.yml
    ├── PULL_REQUEST_TEMPLATE.md
    └── workflows/
        ├── ai-review.yml     ← AI agent analyses every Issue and PR
        └── weekly-digest.yml ← Monday morning activity summary
```

---

## 3. Document registry

Every document in this repo has an explicit purpose and owner.

| Document | Purpose | Audience | Editable by | Status |
|----------|---------|----------|-------------|--------|
| `MANIFESTE.md` | Constitution — project intent, structure, principles | Human + Agent | Founder only (governance Issue) | Stable |
| `README.md` | Front door — what is it, who is it for, how to start | Human + Agent | Maintainer | Stable |
| `PLAYBOOK.md` | Assembled playbook — full read | Human + Agent | Auto-assembled | Living |
| `CONTRIBUTING.md` | Contribution guide — process, templates, rules | Human | Maintainer | Stable |
| `ROADMAP.md` | Direction — milestones, discussion items | Human | Community | Living |
| `CODE_OF_CONDUCT.md` | Community rules — tone, conflict, safety | Human | Founder | Stable |
| `sections/00-reading-guide.md` | How to read and navigate this playbook | Human + Agent | Maintainer | Priority |
| `sections/01-definition/` | What OpenClaw is — concepts, positioning | Human + Agent | Community T2/T3 | Priority |
| `sections/02-installation/` | Setup from scratch | Human | Community T2/T3 | Open |
| `sections/03-configuration/` | Context-specific configuration | Human + Agent | Community T2/T3 | Open |
| `sections/04-personalisation/` | Voice, memory, workflows | Human + Agent | Community T2/T3 | Open |
| `sections/05-maintenance/` | Long-term operation | Human | Community T2/T3 | Open |
| `sections/06-use-cases/` | Field reports — real usage | Human | Community T2/T3 | Open |
| `resources/prompt-templates/` | Ready-to-use prompts EN + FR | Human + Agent | Community | Open |
| `resources/agent-instructions/` | Agent-specific guidance | Agent | Founder + Maintainer | Priority |
| `_project/TRACKER.md` | Live task status | Internal | Alex + Claude | Active |
| `_project/RULES.md` | Working rules Alex + Claude | Internal | Alex + Claude | Active |
| `.github/workflows/ai-review.yml` | AI moderation on Issues/PRs | System | Maintainer | Active |
| `.github/workflows/weekly-digest.yml` | Weekly activity summary | System | Maintainer | Active |

---

## 4. Agents and roles

### Alex Willemetz — Founder and Decision Maker
- Validates all strategic decisions
- Approves T1 structure changes
- Represents the project in public (meetup, LinkedIn, etc.)
- Reviews weekly digest and acts on flagged items

### Claude (Anthropic) — Creation Agent (active until Thursday)
- Writes and structures all documents
- Generates GitHub automation files
- Reviews drafts and applies devil's advocate analysis
- Does not push to GitHub directly — delivers files for Alex to upload

### Aurel — OpenClaw Agent (integration planned post-Thursday)
- Will handle GitHub Issue triage and PR first-response
- Will run the `ai-review.yml` workflow logic natively
- Will generate weekly digests from repo activity
- Onboarding: after March 26 meetup

---

## 5. Working rules (until Thursday)

These rules govern the Alex + Claude collaboration from March 24 to March 26, 18:45.

**R1 — Nothing is produced without a validated brief.**  
Before any document is written, intent and structure are agreed in conversation.

**R2 — Manifesto is the constitution.**  
Every document produced answers to `MANIFESTE.md`. If there is a conflict, the Manifesto wins.

**R3 — Complete or placeholder.**  
No half-written sections in public documents. Either the content is there, or a clear placeholder with an Issue number marks its absence.

**R4 — One pass, then review.**  
Claude writes a full draft in one pass. Alex reviews and requests specific changes. No iterative word-by-word editing — it wastes time.

**R5 — Thursday goal is contributor-ready, not content-complete.**  
The repo must be clean, welcoming, and functional by 18:45 Thursday. Content completeness is a community goal, not a launch blocker.

**R6 — _project/ is internal.**  
Nothing in `_project/` is written for the public. It can be raw, direct, and operational.

**R7 — Validate before deploy.**  
Before any file is pushed to GitHub, Alex confirms: "this is good to push." Claude does not assume.

---

## 6. Workflow: creation

```
BRIEF         Alex describes what he needs
     ↓
STRUCTURE     Claude proposes structure + intent
     ↓
VALIDATION    Alex approves or adjusts (one exchange max)
     ↓
PRODUCTION    Claude writes full draft in one pass
     ↓
REVIEW        Alex reads, flags specific issues
     ↓
ADJUSTMENT    Claude makes targeted changes
     ↓
SIGN-OFF      Alex says "good to push"
     ↓
DELIVERY      Claude outputs file(s) for upload
```

---

## 7. Workflow: validation and deployment

### How files reach GitHub (until Aurel is integrated)

**Option A — Manual upload (current method)**
1. Claude delivers files via `present_files`
2. Alex goes to `github.com/alexwill87/openclawfieldplaybook`
3. `Add file → Upload files` → drag and drop
4. Commit message: `[type]: description` (e.g. `docs: add MANIFESTE and README`)
5. Push to `main`

**Option B — Setup script (when Alex is ready)**
Claude generates a `setup.sh` script.  
Alex runs it once from terminal.  
It creates the repo structure and pushes all files in one command.

### GitHub Actions activation
After first push:
1. Go to `Settings → Secrets and variables → Actions`
2. Add secret: `ANTHROPIC_API_KEY` = your Anthropic API key
3. Go to `Actions` tab → confirm workflow activation
4. Test: open a dummy Issue → AI comment should appear within 2 minutes

---

## 8. Planning

### Monday March 24 — Foundation
- [x] Repo name decided: `openclaw-field-playbook`
- [x] Manifesto finalized
- [ ] README finalized
- [ ] PROJECT.md finalized
- [ ] Full repo structure generated
- [ ] All files delivered to Alex
- [ ] **Alex creates repo and pushes first files**

### Tuesday March 25 — Content
- [ ] `sections/00-reading-guide.md` written
- [ ] `sections/01-definition/` — intro section written
- [ ] `sections/03-configuration/` — first practical section
- [ ] Prompt templates (EN + FR) — minimum 3 per language
- [ ] `resources/agent-instructions/` — agent bootstrap guide
- [ ] GitHub Actions tested and operational

### Wednesday March 26 — Polish
- [ ] All placeholder sections have clean Issue numbers
- [ ] GitHub Projects board configured
- [ ] TRACKER.md up to date
- [ ] LinkedIn post written and scheduled (07:30)
- [ ] QR code + Linktree ready
- [ ] Pitch rehearsed (2 min stage + 1-1 version)

### Thursday March 26 — Launch
- [ ] LinkedIn post published 07:30
- [ ] Repo final check 17:00
- [ ] Meetup 18:45 — AI Tinkerers × HEC Vibe × École 42

---

## 9. Definition of done

The repo is **contributor-ready** when:

- [ ] `MANIFESTE.md` — final, clean, under 2 pages
- [ ] `README.md` — clear, welcoming, all links functional
- [ ] `CONTRIBUTING.md` — step-by-step for a GitHub beginner
- [ ] All 6 chapter folders exist with at minimum a `README.md` placeholder
- [ ] `sections/00-reading-guide.md` — complete
- [ ] `sections/01-definition/` — at least one complete section
- [ ] At least 2 prompt templates available (EN + FR)
- [ ] `agent-instructions/` — complete enough for a fresh OpenClaw to parse
- [ ] `ai-review.yml` — deployed and tested (one dummy Issue confirms it works)
- [ ] GitHub Projects board — columns and first cards created
- [ ] Zero broken links in README and MANIFESTE
- [ ] AI agent responds to a test Issue within 2 minutes
