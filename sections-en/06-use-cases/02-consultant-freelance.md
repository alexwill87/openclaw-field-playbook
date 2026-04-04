---
---
status: complete
audience: both
chapter: 06
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: en
---

# 02 -- Freelance consultant

**For whom:** independent consultant working solo, without a technical team
**Setup time:** 1 to 2 days
**Difficulty:** Beginner

---

## Context

A freelance consultant manages around ten clients in parallel. Their daily routine: meetings, commercial proposals, project tracking, invoicing, and lots of emails. They don't have a VPS, no technical team, and no desire to maintain server infrastructure.

They want an AI assistant to help structure their day, write faster, and not forget anything.

---

## Problem

- Client emails accumulate without prioritization
- Commercial proposals take too long to write
- Client tracking relies on memory and scattered notes
- No consolidated view of time spent per client
- Invoice reminders are forgotten or sent too late

---

## Configuration

### Infrastructure

| Component | Choice | Monthly cost |
|-----------|--------|-------------|
| Machine | Personal laptop (macOS or Linux) | -- |
| OpenClaw | Local installation | -- |
| Calendar | Google Calendar or Nextcloud | free or existing |
| Email | Existing email client (Gmail, ProtonMail) | existing |
| Storage | Local folder + existing cloud sync | existing |

**No VPS. No database. No Mattermost.** Everything runs locally on the consultant's laptop.

### Single agent

One OpenClaw agent, configured with:
- The consultant's system prompt (tone, domain of expertise, list of clients)
- Read access to local files (proposals, notes, templates)
- Calendar connection for morning briefings

---

## Setup

### Day 1: Installation and basic configuration

1. Install OpenClaw on the laptop
2. Create the system prompt with the consultant's context:
   - Domain of expertise
   - List of active clients with short context
   - Preferred communication tone
   - Proposal templates and sample emails
3. Configure access to local files (folder `~/clients/`)
4. Test with a first task: "Summarize my notes from the last meeting with [client X]"

### Day 2: Daily workflows

1. Configure the morning briefing:
   - The agent reads today's calendar
   - It lists pending tasks by client
   - It flags overdue invoices
   - It suggests a priority order for the day
2. Configure email triage:
   - The agent reads received emails (via export or integration)
   - It classifies by urgency: action required / information / can wait
   - It proposes draft responses for urgent emails
3. Configure client tracking:
   - After each interaction, the agent updates the client file
   - It generates a weekly summary per client

---

## Results

After one week of use:

- **Morning briefing in 2 minutes**: the consultant starts each day with a clear view of their priorities, without opening 5 applications
- **Email triage**: emails are classified automatically. Draft responses save 30 to 45 minutes per day
- **Automated client tracking**: each client has an up-to-date file with interaction history, decisions made, and next steps
- **Commercial proposals in 15 minutes instead of 2 hours**: the agent generates a first draft from the template and client context. The consultant adjusts and sends
- **Zero forgotten follow-ups**: the agent flags overdue invoices in the morning briefing

---

## Lessons learned

1. **The system prompt is the heart of the system.** A vague prompt produces generic results. The consultant must invest time describing their context, tone, and business rules.

2. **One file per client, not a database.** For a freelancer, Markdown files in a `~/clients/` folder are simpler and more portable than a database.

3. **The morning briefing changes everything.** It's the simplest workflow to set up and the one with the most impact. Start there.

4. **Don't automate client relationships.** The agent drafts messages. The consultant reviews, adjusts, and sends. The client should never receive an unreviewed email.

5. **Back up the agent context.** The system prompt and client files must be in a synchronized folder (cloud or Git). Losing the laptop shouldn't mean losing the agent's memory.

---

## Common mistakes

| Mistake | Consequence | Solution |
|---------|-------------|----------|
| Prompt too generic | Generic, unusable responses | Add specific context: clients, domain, tone |
| No file structure | Agent can't find information | One folder per client, consistent file names |
| Trusting the first draft | Factual errors sent to client | Always review before sending |
| No backup | Loss of context if device fails | Cloud sync or Git for the work folder |

---

## Template -- Consultant's system prompt

```
You are the professional assistant for [NAME], a consultant in [DOMAIN].

Context:
- [NAME] has worked independently since [YEAR]
- Their clients are primarily [CLIENT TYPE]
- Their tone is professional but direct, no unnecessary jargon

Active clients:
- [Client A]: [short context, current project]
- [Client B]: [short context, current project]
- [Client C]: [short context, current project]

Rules:
- You always draft messages, never final communications
- You flag if information is missing rather than making it up
- You use formal address in client emails
- You record decisions and next steps after each interaction
- You remind about unpaid invoices over 30 days old in the morning briefing

Workflows:
1. Morning briefing: calendar + tasks + invoices + priorities
2. Email triage: urgent / info / can wait + drafts
3. Commercial proposal: template + client context + first draft
4. Client tracking: update client file after each interaction
```

---

## Checklist

- [ ] OpenClaw is installed and responds on the laptop
- [ ] The system prompt contains the list of active clients
- [ ] The morning briefing displays today's appointments
- [ ] Email triage correctly classifies a sample of 10 emails
- [ ] A test commercial proposal is generated in under 5 minutes
- [ ] Client files are in a synchronized folder

---

*Minimal configuration, zero infrastructure to maintain. Ideal for a first contact with OpenClaw.*
