# TODO.md — Master Task List
## The OpenClaw Field Playbook · github.com/alexwill87/openclawfieldplaybook

> **Rule:** This file is the single source of truth for all pending changes.  
> No modification is made without being listed here first.  
> This file ships in the public repo — it documents the project's build process.  
> Mark tasks `[x]` as they are completed.

---

## Table of Contents

- [Decisions log](#decisions-log)
- [BLOC 1 — Rename PLAYBOOK → PLAYBOOK](#bloc-1--rename-playbook--playbook)
- [BLOC 2 — Chapter number consistency](#bloc-2--chapter-number-consistency)
- [BLOC 3 — Link corrections](#bloc-3--link-corrections)
- [BLOC 4 — Missing files](#bloc-4--missing-files)
- [BLOC 5 — New Chapter 7: Localisation](#bloc-5--new-chapter-7-localisation)
- [BLOC 6 — Language strategy](#bloc-6--language-strategy)
- [BLOC 7 — Content standards](#bloc-7--content-standards)
- [BLOC 8 — Version management](#bloc-8--version-management)
- [BLOC 9 — Update PROJECT.md](#bloc-9--update-projectmd)
- [BLOC 10 — Update TRACKER.md](#bloc-10--update-trackermd)
- [BLOC 11 — MANIFESTE.md rewrite](#bloc-11--manifestemd-rewrite)
- [BLOC 12 — README.md rewrite](#bloc-12--readmemd-rewrite)
- [BLOC 13 — REFERENCES.md standardisation](#bloc-13--referencesmd-standardisation)
- [BLOC 14 — website/ subfolder](#bloc-14--website-subfolder)
- [BLOC 15 — Domain and brand consistency](#bloc-15--domain-and-brand-consistency)
- [BLOC 16 — Integrate references into content](#bloc-16--integrate-references-into-content)
- [BLOC 17 — Final checks before ZIP](#bloc-17--final-checks-before-zip)

---

## Decisions log

All strategic decisions made during the build session (March 23-24, 2026).

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-03-23 | Rename PLAYBOOK → PLAYBOOK everywhere | Coherence with repo name and project title |
| 2026-03-23 | Language strategy: EN-US universal + Chapter 7 Localisation | Glossary EN-US only, local specs in ch.7 |
| 2026-03-23 | First locale: fr-FR. Planned: fr-CA, en-GB | Auto-localisation workflow in v1.5 |
| 2026-03-23 | QUALITY: 6 dimensions validated, scores 1–5 | See _project/QUALITY.md |
| 2026-03-23 | _project/ fully public on GitHub | Transparency as a trust signal |
| 2026-03-24 | Domain purchased: openclawfieldplaybook.com | Redirect to main domain |
| 2026-03-24 | Main domain: openclawfieldplaybook.com | Coherent with project title |
| 2026-03-24 | Repo name: openclaw-field-playbook | Stays unchanged — coherent with title |
| 2026-03-24 | website/ subfolder in repo | Front (Phase 1 jeudi) + back minimal (Phase 1) |
| 2026-03-24 | About section at launch: minimal | First name, city, one line per project |
| 2026-03-24 | REFERENCES.md: public, standardised fiche format | Community can add notes via Issues |
| 2026-03-24 | Do NOT claim "first repo designed for agents" | Cannot be verified — remove from Manifeste |
| 2026-03-24 | Site vocabulary: "read online", "clone", "fork and edit", "open an Issue" | Precise, no invented jargon |

---

## BLOC 1 — Rename PLAYBOOK → PLAYBOOK

### File to rename
- [ ] `PLAYBOOK.md` → `PLAYBOOK.md`

### Occurrences to fix in each file

- [ ] `README.md` — all occurrences + link updated to `PLAYBOOK.md`
- [ ] `MANIFESTE.md` — all occurrences
- [ ] `CONTRIBUTING.md` — all occurrences
- [ ] `_project/PROJECT.md` — repository map + document registry
- [ ] `resources/agent-instructions/README.md` — reference to `PLAYBOOK.md`
- [ ] `sections/00-reading-guide.md` — any occurrence
- [ ] `.github/workflows/ai-review.yml` — any occurrence in system prompts
- [ ] `.github/workflows/weekly-digest.yml` — any occurrence

### Verify after rename
- [ ] Grep entire repo for "PLAYBOOK" — must return zero results

---

## BLOC 2 — Chapter number consistency

Remove zero-padding from chapter numbers in section READMEs.

- [ ] `sections/02-installation/README.md` — `Chapter 02` → `Chapter 2`
- [ ] `sections/03-configuration/README.md` — `Chapter 03` → `Chapter 3`
- [ ] `sections/04-personalisation/README.md` — `Chapter 04` → `Chapter 4`
- [ ] `sections/05-maintenance/README.md` — `Chapter 05` → `Chapter 5`
- [ ] `sections/06-use-cases/README.md` — `Chapter 06` → `Chapter 6`

---

## BLOC 3 — Link corrections

- [ ] `PLAYBOOK.md` — all relative `https://github.com/alexwill87/openclawfieldplaybook/issues/new` links → absolute GitHub URLs
- [ ] `README.md` — Issue template links → absolute GitHub URLs
- [ ] `sections/02` to `06/README.md` — Issue template links → absolute GitHub URLs
- [ ] Verify all `sections/` links after PLAYBOOK rename
- [ ] Add link to `www.openclawfieldplaybook.com` in `README.md` once DNS is live

---

## BLOC 4 — Missing files to create or rename

- [ ] `resources/prompt-templates/en/` → rename to `resources/prompt-templates/en-US/`
- [ ] Verify `_project/QUALITY.md` present *(created this session)*
- [ ] Verify `_project/SECTIONS-SCORES.md` present *(created this session)*
- [ ] Verify `resources/REFERENCES.md` present *(created this session)*
- [ ] Create `resources/tech-stack.md` — Alex's full stack documented (see BLOC 11)

---

## BLOC 5 — New Chapter 7: Localisation

### Principle
Playbook content is universal (EN-US). Chapter 7 documents what changes per local context — legislation, ecosystem, tools, cultural practices.

### Files to create
- [ ] `sections/07-localisation/` — create folder
- [ ] `sections/07-localisation/README.md` — chapter index
- [ ] `sections/07-localisation/fr-FR.md` — first locale, priority
- [ ] `sections/07-localisation/en-US.md` — reference locale

### Section format for each locale file
```markdown
---
status: draft
locale: [code]
last_updated: YYYY-MM
contributors: []
---

# Locale: [code] — [full name]

## Regulatory context
## Local ecosystem
## Language specifics
## Cultural business context
## Known differences from en-US baseline
```

### Associated updates
- [ ] Add Chapter 7 to `PLAYBOOK.md` with link to `sections/07-localisation/README.md`
- [ ] Add to `_project/PROJECT.md` — repository map + document registry
- [ ] Add to `ROADMAP.md` — "v1.5: Auto-localisation workflow"

### Auto-localisation workflow (document, do not deploy at launch)
- [ ] Describe in ROADMAP v1.5: when a section reaches `status: complete`, agent produces fr-FR entry automatically
- [ ] Planned locales: `fr-FR` (priority), `fr-CA`, `en-GB`

---

## BLOC 6 — Language strategy

### Language contract to add to `sections/00-reading-guide.md`
- [ ] Add section "Language contract":

```
Untouchable — never translated, all locales:
  → YAML keys: status, audience, chapter, last_updated
  → File and folder names
  → GitHub labels
  → Technical commands in code blocks
  → Glossary (EN-US only — see Chapter 1)

Universal content (EN-US, applies everywhere):
  → Section body, Step-by-step, Common mistakes, Templates
  → This content does not change per locale

Local content (Chapter 7 only):
  → Legislation and regulation
  → Local tool ecosystem
  → Cultural business practices
  → Differences from EN-US baseline

For agents operating in non-US contexts:
  "Technical English terms in YAML keys and commands are
  universal references — do not translate.
  For local adaptations, see sections/07-localisation/[locale].md"
```

### Rename existing blocks across all sections
- [ ] `## 🇫🇷 French context` → `## 🌍 Local specifications`
- [ ] Block content → `*[See sections/07-localisation/ for local adaptations]*`

---

## BLOC 7 — Content standards

Add to `_project/RULES.md` a "Content standards" section.

- [ ] Criteria for `draft` → `review`:
  - Full standard format present
  - Template is copy-paste ready
  - Metadata block complete
  - Every claim based on real experience or verifiable source
  - Section limits explicitly stated

- [ ] Criteria for `review` → `complete`:
  - Validated by a human maintainer
  - QUALITY score ≥ 3/5 on all 6 dimensions
  - Entry created in `07-localisation/fr-FR.md`

---

## BLOC 8 — Version management

- [ ] Add versioning convention to `ROADMAP.md`:
  - `v0.x` — in construction, no `complete` sections yet
  - `v1.0` — every chapter has at least one `status: complete` section
  - `v1.x` — additions without T1 structure change
  - `v2.0` — T1 structure change (governance Issue required)

- [ ] Add to `_project/PROJECT.md` — who decides version bumps:
  - `v0.x → v1.0` — Founder
  - `v1.x → v1.x+1` — Maintainer after merging a complete section
  - `v1.x → v2.0` — governance Issue + community vote

---

## BLOC 9 — Update PROJECT.md

After all blocs above are applied:

- [ ] Repository map: add `PLAYBOOK.md`, `07-localisation/`, `QUALITY.md`, `SECTIONS-SCORES.md`, `REFERENCES.md`, `tech-stack.md`, `website/`, `en-US/`
- [ ] Document registry: all new files with purpose + audience + editability
- [ ] Definition of done: add QUALITY score threshold (≥ 3/5)
- [ ] Add domain: `www.openclawfieldplaybook.com`

---

## BLOC 10 — Update TRACKER.md

- [ ] Mark `[x]` all files produced in this session
- [ ] Add: `QUALITY.md created`
- [ ] Add: `SECTIONS-SCORES.md created`
- [ ] Add: `REFERENCES.md created`
- [ ] Add Tuesday tasks: `07-localisation/fr-FR.md`, `07-localisation/en-US.md`, `website/` front
- [ ] Add: domain `openclawfieldplaybook.com` purchased and DNS to configure

---

## BLOC 11 — MANIFESTE.md rewrite

Full rewrite based on session decisions. Key changes:

### Remove
- [ ] Claim of being "first repo designed to be ingested by agents" — unverifiable
- [ ] Any language implying superiority over existing resources

### Add or strengthen
- [ ] Opening line: lead with the real story — failed attempts, months of R&D, not a marketing pitch
- [ ] "Clone-and-deploy" as the central promise — not just "read and apply"
- [ ] Co-authorship by humans and AI stated as a deliberate philosophical choice
- [ ] Sovereignty as a non-negotiable value, not a feature
- [ ] Reference to `www.openclawfieldplaybook.com` as the human-readable entry point
- [ ] Reference to GitHub repo as the place to clone, fork, and edit

### Vocabulary to use precisely
- "read online" — for the website
- "clone the repository" — for local use
- "fork and edit" — for contributing via code
- "open an Issue" — for contributing via discussion
- Never: "playbook", "first of its kind", "revolutionary"

### New `resources/tech-stack.md` to create
Documenting Alex's stack (referenced from Manifeste and README):
- Agents: OpenClaw + Aurel (sub-agents planned)
- LLMs used: Sonnet 4.6, Gemini Flash 3.0, Claude, Mistral, OpenAI
- Infrastructure: Ubuntu, Tailscale, Hetzner VPS
- Collaboration: GitHub Actions, Notion
- This file: reference for contributors who want to replicate the environment

---

## BLOC 12 — README.md rewrite

### Fix the pitch title
- [ ] Current: "Building, sharing and editing my clone and deploy OpenClaw Business oriented Playbook" (typo + too long)
- [ ] Replace with: `"Building the OpenClaw Field Playbook — a clone-and-deploy guide for entrepreneurs and builders"`

### Add to README
- [ ] Link to `www.openclawfieldplaybook.com` (once live)
- [ ] Real story: 3 failed attempts, 5 months R&D, AI superagent initiative as context
- [ ] Tech stack reference → `resources/tech-stack.md`
- [ ] Three clear calls to action:
  - "Read online → www.openclawfieldplaybook.com"
  - "Clone the repository → github.com/alexwill87/openclawfieldplaybook"
  - "Open an Issue → contribute without code"

### About section (minimal for launch)
- [ ] Alex Willemetz — Paris
- [ ] One line per project: LADB, Adhectif, Panthéos, Omar&Paris
- [ ] No detail — to be enriched post-meetup

---

## BLOC 13 — REFERENCES.md standardisation

### Standard fiche format (validated)
Apply this format to all 7 existing references and all future additions:

```markdown
## REF-XX — [Title]

- **URL:**
- **Author:**
- **Format:** book / repo / website / guide / article / official-doc / API
- **Access:** free / paid / on-request
- **Language:** EN / FR / other
- **Date:**
- **Target audience:**
- **Summary:** (3 lines max)
- **Table of contents:** (if available)
- **Strengths:**
- **Gaps vs our playbook:**
- **Community note:** *[Add via GitHub Issue — label: reference-note]*
- **Tags:** #installation #configuration #business #personal #technical #official #api

---
```

### Tasks
- [ ] Apply standard fiche format to REF-01 through REF-07
- [ ] Add REF-08 — LeanPub sample (read from public URL, extract depth and topics)
- [ ] Add REF-09 — OpenClaw official documentation (docs.openclaw.ai)
- [ ] Add REF-10 — ClawHub (community skills marketplace)
- [ ] Add REF-11 — OpenClaw GitHub repo (main repo, star count, activity)
- [ ] Add instructions at top of file: "To add a reference, open an Issue with label `new-reference`"
- [ ] Add to `CONTRIBUTING.md`: how to contribute a reference

---

## BLOC 14 — website/ subfolder

### Architecture
`website/` is a subfolder in the repo containing the full site source.  
Phase 1 (jeudi): front-end static site served via GitHub Pages.  
Phase 2 (post-meetup): back-end minimal on Hetzner.

### Folder structure to create
```
website/
├── ROADMAP.md          ← site-specific roadmap (features, phases)
├── index.html          ← single-page site, renders playbook content
├── assets/
│   ├── style.css       ← clean, readable typography
│   └── script.js       ← search, anchor nav, PDF export trigger
├── api/                ← Phase 2 back-end (Node.js or Python)
│   ├── README.md       ← API documentation
│   ├── newsletter.js   ← newsletter signup endpoint
│   └── search.js       ← full-text search endpoint
└── docs/               ← GitHub Pages source
    └── CNAME           ← www.openclawfieldplaybook.com
```

### Phase 1 features (jeudi — static)
- [ ] Fixed top navigation: chapters 0–7 as anchor links + "Download PDF" button
- [ ] Full playbook content rendered with readable typography
- [ ] "Read on GitHub" button — links to repo
- [ ] "Clone" button — links to `git clone` instructions
- [ ] "Open an Issue" button — links to GitHub Issues
- [ ] "Fork and edit" button — links to GitHub fork
- [ ] About section: Alex, Paris, one line per project
- [ ] Footer: licence CC-BY 4.0, GitHub link, domain

### Phase 2 features (post-meetup — back-end minimal)
- [ ] Full-text search across all sections
- [ ] Newsletter signup → weekly digest
- [ ] PDF export on demand (server-side generation)
- [ ] Public SECTIONS-SCORES dashboard
- [ ] Contribution form (simplified — no GitHub account required)

### GitHub Pages configuration
- [ ] `docs/CNAME` — contains `www.openclawfieldplaybook.com`
- [ ] Settings → Pages → Source: `/website/docs`
- [ ] Settings → Pages → Custom domain: `www.openclawfieldplaybook.com`

### DNS configuration (on registrar)
- [ ] CNAME `www` → `alexwill87.github.io`
- [ ] A records apex → 185.199.108.153 / .109.153 / .110.153 / .111.153
- [ ] Configure `openclawfieldplaybook.com` as redirect → `openclawfieldplaybook.com`

### PDF export GitHub Action
- [ ] Create `.github/workflows/pdf-export.yml`
- [ ] Triggers on: new release tag
- [ ] Output: `PLAYBOOK.pdf` attached to release

---

## BLOC 15 — Domain and brand consistency

The official brand is: **The OpenClaw Field Playbook**

### Verify consistency everywhere
- [ ] `MANIFESTE.md` — title uses exact brand name
- [ ] `README.md` — H1 uses exact brand name
- [ ] `PLAYBOOK.md` — H1 uses exact brand name
- [ ] `website/index.html` — title tag and H1 use exact brand name
- [ ] `_project/setup.sh` — repo URL correct: `github.com/alexwill87/openclawfieldplaybook`
- [ ] All GitHub Actions — repo URL correct
- [ ] `resources/agent-instructions/README.md` — repo URL correct

### Domains
- [ ] `openclawfieldplaybook.com` — main domain (to purchase + configure)
- [ ] `openclawfieldplaybook.com` — already purchased, configure as 301 redirect

---

## BLOC 16 — Integrate references into content

Based on `resources/REFERENCES.md` analysis.

### `MANIFESTE.md`
- [ ] Add: no existing resource covers the full journey (installation → maintenance) for entrepreneurs — this is the gap we fill
- [ ] Add: positioning vs hype marketing (contrast with "earn while you sleep" approach)

### `sections/01-definition/README.md`
- [ ] Section 1.3: use REFERENCES.md as source for OpenClaw vs alternatives
- [ ] Add REF-07 (Wikipedia FR) for OpenClaw history: Clawdbot → Moltbot → OpenClaw
- [ ] Mention ClawHub security issue (300+ malicious extensions 2026) in sovereignty section

### `sections/03-configuration/README.md`
- [ ] Section 3.5: reference REF-04 benchmark data (skill graphs: +20% accuracy, −70% tokens)

### `sections/06-use-cases/README.md`
- [ ] Reference REF-06 (dropshipping) as example of vertical-specific playbook
- [ ] Reference REF-01 personas (Alex, Sam, Mira, Jordan) as inspiration for use case format

### `ROADMAP.md`
- [ ] Add: ongoing REFERENCES.md maintenance as community task
- [ ] Add label `new-reference` to GitHub Issue templates

### `CONTRIBUTING.md`
- [ ] Add section: "Before writing, check REFERENCES.md — build on what exists, don't reproduce it"

---

## BLOC 17 — Final checks before ZIP

Run these checks in order. All must pass before generating the ZIP.

### Automated checks (agent can run)
- [ ] Grep global: zero occurrence of `PLAYBOOK`
- [ ] Grep global: zero relative link `https://github.com/alexwill87/openclawfieldplaybook/issues/new`
- [ ] All section metadata blocks have 5 required keys
- [ ] All `status` values are valid: `draft | review | complete`
- [ ] `sections/07-localisation/fr-FR.md` exists
- [ ] `sections/07-localisation/en-US.md` exists
- [ ] `resources/prompt-templates/en-US/` exists (renamed from `en/`)
- [ ] `website/` folder exists with `index.html` and `assets/`
- [ ] `_project/setup.sh` contains `github.com/alexwill87/openclawfieldplaybook`
- [ ] `docs/CNAME` contains `www.openclawfieldplaybook.com`

### Manual checks (human)
- [ ] Read MANIFESTE.md — real story is there, no unverifiable claims
- [ ] Read README.md — three calls to action are clear
- [ ] Read `sections/00-reading-guide.md` — language contract is complete
- [ ] Check website locally: navigation, PDF button, GitHub links work
- [ ] Verify About section: minimal but honest

### Generate ZIP
- [ ] ZIP generated cleanly — no parasitic folders
- [ ] ZIP tested: unzip and verify structure matches PROJECT.md map
- [ ] This TODO.md stays in ZIP (it's public, it documents the build process)
