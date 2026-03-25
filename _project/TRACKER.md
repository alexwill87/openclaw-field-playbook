# TRACKER — The OpenClaw Field Playbook
## Live task status · github.com/alexwill87/openclawfieldplaybook

> Legend: `[x]` done · `[-]` in progress · `[ ]` to do · `[!]` blocked

---

## Session March 23-24, 2026 — Completed

### Foundation files
- [x] MANIFESTE.md — complete rewrite, real story, precise vocabulary
- [x] README.md — rewrite with 3 CTAs, real story, tech stack
- [x] PLAYBOOK.md — assembled playbook with Chapter 7
- [x] CONTRIBUTING.md
- [x] ROADMAP.md
- [x] CODE_OF_CONDUCT.md
- [x] LICENSE (CC-BY 4.0)

### Sections
- [x] sections/00-reading-guide.md — complete (human + agent)
- [x] sections/01-definition/README.md — section 1.1 written, structure complete
- [x] sections/02-installation/README.md — subsections listed
- [x] sections/03-configuration/README.md — subsections listed
- [x] sections/04-personalisation/README.md — subsections listed
- [x] sections/05-maintenance/README.md — subsections listed
- [x] sections/06-use-cases/README.md — format + wanted profiles listed
- [x] sections/07-localisation/README.md — chapter index
- [x] sections/07-localisation/fr-FR.md — first complete locale
- [x] sections/07-localisation/en-US.md — baseline locale

### Resources
- [x] resources/prompt-templates/en-US/README.md — 5 templates
- [x] resources/prompt-templates/fr-FR/README.md — 4 templates
- [x] resources/agent-instructions/README.md — complete agent guide
- [x] resources/tech-stack.md — Alex's full stack documented
- [x] resources/REFERENCES.md — 7 sources analysed

### Internal project docs
- [x] _project/PROJECT.md — master reference
- [x] _project/TODO.md — 17 blocs, 135 tasks
- [x] _project/QUALITY.md — 6 dimensions, 18 tests, agent-ready
- [x] _project/SECTIONS-SCORES.md — scoring dashboard
- [x] _project/RULES.md — working agreement
- [x] _project/setup.sh — one-command GitHub deploy

### GitHub automation
- [x] .github/workflows/ai-review.yml — AI review on Issues + PRs
- [x] .github/workflows/weekly-digest.yml — Monday digest
- [x] .github/workflows/pdf-export.yml — PDF on release
- [x] .github/ISSUE_TEMPLATE/suggestion.yml
- [x] .github/ISSUE_TEMPLATE/correction.yml
- [x] .github/PULL_REQUEST_TEMPLATE.md

### Website
- [x] website/index.html — single-page site
- [x] website/assets/style.css — clean typography
- [x] website/assets/script.js — search + nav + PDF
- [x] website/api/README.md — Phase 2 documented
- [x] website/ROADMAP.md — phases 1/2/3
- [x] website/docs/CNAME — www.openclawfieldplaybook.com

---

## Remaining for Thursday (Alex actions)

### GitHub
- [ ] Create repo: github.com/alexwill87/openclawfieldplaybook
- [ ] Push all files (run `bash _project/setup.sh` or manual upload)
- [ ] Add secret: `ANTHROPIC_API_KEY` in Settings → Secrets
- [ ] Activate GitHub Actions in Actions tab
- [ ] Test: open a dummy Issue → AI should respond within 2 min
- [ ] Create first release tag `v0.1` → triggers PDF export

### DNS (on your domain registrar)
- [ ] `www.openclawfieldplaybook.com` CNAME → `alexwill87.github.io`
- [ ] Apex A records → 185.199.108.153 / .109.153 / .110.153 / .111.153
- [ ] `openclawfieldbook.com` → 301 redirect to `openclawfieldplaybook.com`

### GitHub Pages
- [ ] Settings → Pages → Source: `/website/docs`
- [ ] Custom domain: `www.openclawfieldplaybook.com`

### LinkedIn post
- [ ] Write post (Tuesday) — 3 failed attempts angle
- [ ] Schedule for Thursday 07:30

### Meetup prep
- [ ] QR code → www.openclawfieldplaybook.com
- [ ] Linktree updated: site + GitHub + LinkedIn
- [ ] 2-min pitch rehearsed
- [ ] 1-1 questions ready: "Tu utilises OpenClaw en prod ?"

---

## Backlog (post-meetup)

- [ ] sections/01-definition/ — sections 1.2, 1.3, 1.4
- [ ] sections/02-installation/ — first section written
- [ ] sections/03-configuration/ — first section written
- [ ] Quality audit run (QUALITY.md) on existing sections
- [ ] Aurel/OpenClaw integrated as GitHub agent
- [ ] REFERENCES.md — standardised fiches for all 7 refs + REF-08 (LeanPub sample)
- [ ] website Phase 2 — newsletter endpoint on Hetzner
- [ ] GitHub Projects board configured
