---
---
status: complete
audience: human
chapter: 06
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: en
---

# 6.8 -- Craftspeople and Small Businesses: An AI Assistant for Solo Operators

> You are a plumber, electrician, consultant, photographer, or coach. You work alone or almost alone. You handle everything: clients, quotes, accounting, marketing. Here's how OpenClaw can help you.

**For whom:** craftspeople or small business owner managing their activity solo
**Time to set up:** 3 hours (with an installer)
**Difficulty:** Beginner

---

## Context

Jean is a plumbing contractor in Montreuil. He works alone. His days: 7 hours on job sites, then in the evening he responds to clients, prepares quotes, chases unpaid invoices, updates his website. He sleeps 5 hours a night. He heard about "AI" from his accountant.

---

## Problem

- He loses clients because he responds to requests 48 hours later
- Each quote takes 30 minutes even though they follow the same format every time
- He forgets to follow up on unpaid invoices
- He doesn't know which prospects are hot and which have abandoned him

---

## Configuration

### What Jean installed (with an installer's help)

| Component | Detail | Cost |
|-----------|--------|------|
| VPS | Hetzner CPX11 (2 CPU, 4 GB RAM) | 4.50 EUR/month |
| OpenClaw | Via OpenRouter (Claude Haiku) | ~10 EUR/month |
| Channel | Telegram (@JeanPlomberieBot) | Free |
| Email | Gmail connected via Himalaya skill | Free |

**Total cost: ~15 EUR/month** -- cheaper than a Netflix subscription.

### What the agent does for Jean

**Every morning at 7 AM (cron briefing):**
- "3 new client messages last night. 2 quote requests, 1 question about an ongoing project."
- "Invoice #2024-089 unpaid for 15 days. Would you like me to send a follow-up?"
- "Weather: rain tomorrow, plan to cover the job site on Rue de la Paix."

**When a client sends an email:**
- The agent categorizes the message (quote request / question / complaint / spam)
- For quote requests: it prepares a draft based on similar previous quotes
- For questions: it responds with information from the knowledge base (hours, service areas, rates)

**Every Friday evening (cron summary):**
- "This week: 5 new contacts, 3 quotes sent, 1 project completed. Estimated revenue: 2,400 EUR."

### Jean's system prompt (simplified)

```
You are Jean's assistant, a plumbing contractor in Montreuil.

You manage:
- Incoming email triage
- Quote draft preparation
- Unpaid invoice follow-ups
- Daily briefing

You NEVER:
- Send an email without Jean's validation
- Modify a quote that has already been sent
- Respond to an unhappy customer (escalate to Jean)

Your tone: professional, simple, no technical jargon.
Language: French only.
```

---

## Results after 2 months

- Client response time: 48h -> 4h (agent prepares, Jean validates via Telegram)
- Quotes sent per week: 3 -> 8 (pre-filled drafts)
- Unpaid invoices: 5 -> 1 (automatic follow-ups)
- Jean sleeps 7 hours per night instead of 5

---

## Lessons learned

1. **Start with ONE use case only.** Jean started with email triage. He added quotes 3 weeks later, follow-ups after that.

2. **The agent doesn't replace Jean.** It prepares. Jean validates. Trust builds step by step.

3. **The highest cost isn't the server.** It's the initial setup time (3 hours with an installer). After that, it's 15 EUR/month.

4. **Telegram is the right channel.** Jean is on his phone all day. A Telegram message, he sees it in 30 seconds. An email, he sees it in the evening.

---

## Common mistakes

| Mistake | Consequence | Solution |
|---------|-------------|----------|
| Automate everything at once | The craftsperson loses trust, disables everything | Start with one use case, validate it, then expand |
| Let the agent respond without validation | Inappropriate response to an unhappy customer | Keep human validation on everything during the first month |
| Ignore the notification channel | The craftsperson doesn't see alerts | Use Telegram, not email -- the craftsperson is on their phone |
| Don't populate the knowledge base | The agent invents rates or hours | Spend 30 minutes entering basic information at startup |

---

## Reusable template

Checklist for a craftsperson/small business:

- [ ] Choose a channel (Telegram recommended)
- [ ] Identify THE most painful use case (often: responding to clients)
- [ ] Install OpenClaw (alone or with an installer)
- [ ] Set up email triage
- [ ] Test for 1 week with manual validation on everything
- [ ] Add a second use case after 2-3 weeks

---

## Verification

- [ ] The agent sends the morning briefing on Telegram
- [ ] A test email is correctly categorized and a response draft is generated
- [ ] Jean can validate or reject an action from Telegram
- [ ] The weekly summary arrives Friday evening

---

*This use case is inspired by a real implementation experience. The amounts and configurations are representative of a deployment in Europe in 2026.*
