# Website Roadmap
## openclawfieldplaybook.com

---

## Phase 1 — Static (launch Thursday March 26, 2026)

Hosted on GitHub Pages. Zero back-end.

- [x] `index.html` — single-page site with chapter navigation
- [x] `assets/style.css` — clean, readable typography
- [x] `assets/script.js` — search, anchor nav, PDF download link
- [x] `docs/CNAME` — custom domain configured
- [ ] DNS configured: `www.openclawfieldplaybook.com` → GitHub Pages
- [ ] DNS configured: `openclawfieldbook.com` → 301 redirect to main domain
- [ ] GitHub Pages activated in repo Settings
- [ ] PDF export GitHub Action deployed (generates PLAYBOOK.pdf on release)
- [ ] Test all chapter links and GitHub Issue links

---

## Phase 2 — Back-end minimal (post-meetup)

Deployed on Hetzner VPS.

- [ ] Newsletter signup endpoint (`/api/newsletter`)
- [ ] Full-text search across all sections (`/api/search`)
- [ ] Public SECTIONS-SCORES dashboard
- [ ] Contribution form (no GitHub account required)

---

## Phase 3 — Community features (v1.0+)

- [ ] User profiles for contributors
- [ ] Section-level comments
- [ ] Localisation request form
- [ ] "Clone starter" wizard (guided repo setup)
