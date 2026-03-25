# API — Phase 2 Back-end

> **Status:** Planned — not deployed at launch.  
> Phase 1 is fully static (GitHub Pages).  
> This folder documents the back-end to be deployed on Hetzner post-meetup.

---

## Planned endpoints

### POST /api/newsletter
Subscribe to the weekly digest.

**Request:**
```json
{ "email": "user@example.com", "locale": "fr-FR" }
```

**Response:**
```json
{ "status": "subscribed", "digest_day": "Monday" }
```

### GET /api/search?q=
Full-text search across all sections.

**Response:**
```json
{
  "results": [
    { "chapter": 3, "section": "3.2", "title": "Connecting your tools", "excerpt": "..." }
  ]
}
```

### GET /api/scores
Returns current SECTIONS-SCORES data as JSON (for public dashboard).

---

## Stack (planned)
- Node.js or Python (FastAPI)
- Deployed on Hetzner VPS
- Secured with Tailscale or reverse proxy (Caddy)

## Timeline
See `ROADMAP.md` for Phase 2 milestones.
