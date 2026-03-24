---
status: draft
locale: fr-FR
last_updated: 2026-03
contributors: [alexwill87]
---

# Locale: fr-FR — France

> This file documents what is specific to France when using OpenClaw in a business context.
> Universal content is in chapters 1–6. Only the differences are here.

---

## Regulatory context

### RGPD (GDPR)
OpenClaw processes personal data — emails, calendar, contacts. In France, this falls under RGPD (Règlement Général sur la Protection des Données).

Key implications for your configuration:
- Data stored locally on your machine or VPS = RGPD-compliant by default
- Cloud integrations (Gmail, Google Calendar) = check your data processing agreements
- If you deploy OpenClaw for clients or employees: you are the data controller — a privacy policy is required
- Recommended: self-host on French infrastructure (OVHcloud, Scaleway) for maximum compliance

### AI Act (EU)
As of 2026, the EU AI Act applies to AI systems deployed in professional contexts. OpenClaw as a personal assistant in low-risk use cases is likely in the minimal-risk category. Monitor for updates as regulatory guidance evolves.

### Labour law considerations
If OpenClaw is used to monitor employee activity (emails, schedules), French labour law applies. Consult a legal advisor before deploying in HR contexts.

---

## Local ecosystem

### Recommended French infrastructure
- **Hosting:** OVHcloud, Scaleway, Infomaniak (Swiss-French)
- **VPS:** Hetzner (German — GDPR-compliant), OVHcloud
- **Domain registrar:** Gandi.net, OVHcloud
- **Email:** ProtonMail (Swiss), Infomaniak Mail

### French business tools OpenClaw integrates well with
- **Accounting:** Pennylane, Indy, QuickBooks FR
- **CRM:** Sellsy, Pipedrive FR
- **Invoicing:** Facture.net, Tiime
- **HR:** Payfit, Lucca
- **Communication:** Slack, Teams (widely used in French enterprise)

### Tools that may require custom integration
Standard OpenClaw skills are built for anglophone tools. French-specific tools (Pennylane, Sellsy, etc.) may require custom skill development via ClawHub or manual configuration.

---

## Language specifics

### Prompt language
Write your system prompt in French if your business operates in French. OpenClaw passes your prompts to the underlying LLM — French prompts work well with Claude, GPT-4, and Mistral (which has strong French-language performance).

### Recommended models for French content
- **Mistral** (French company) — excellent French, strong cultural understanding
- **Claude Sonnet** — high quality in French, consistent tone
- **GPT-4o** — good French but occasionally anglophone cultural assumptions

### Tone conventions
- French business communication defaults to **vouvoiement** (formal "vous")
- Configure your agent accordingly in the system prompt: *"Tu utilises le vouvoiement dans toutes les communications externes."*
- Internal notes and personal briefings can use **tutoiement**

---

## Cultural business context

### French business rhythm
- August is largely dead — configure reduced agent activity in August
- Lunch (12h–14h) is protected time in most French companies — avoid scheduling automations that send external communications during this window
- "Rentrée" (September) is the real new year for French business — plan your major automations resets then

### Invoice and accounting specifics
- French invoices require: SIRET number, TVA number, mentions légales
- Configure your invoice templates accordingly before letting OpenClaw generate them
- Auto-entrepreneur regime has specific invoice requirements — different from SARL/SAS

### Working hours and legal compliance
- French law limits certain types of communication outside working hours
- "Droit à la déconnexion" (right to disconnect) — OpenClaw should not send work communications after 18h30 by default in employee-facing contexts

---

## Known differences from en-US baseline

| Topic | en-US baseline | fr-FR specifics |
|-------|---------------|-----------------|
| Data hosting | AWS/GCP common | OVHcloud/Scaleway preferred for RGPD |
| Invoice tools | QuickBooks, FreshBooks | Pennylane, Indy, Tiime |
| Business hours | 9am–5pm | 9h–18h30, lunch 12h–14h protected |
| Recommended LLM for local language | GPT-4o | Mistral or Claude |
| Formal/informal tone | Generally informal | Vouvoiement for external comms |
| Peak business calendar | Jan restart | Rentrée (September) = real new year |

---

*[Improve this locale](https://github.com/alexwill87/openclawfieldplaybook/issues/new?template=suggestion.yml) · [CONTRIBUTING.md](../../../CONTRIBUTING.md)*
