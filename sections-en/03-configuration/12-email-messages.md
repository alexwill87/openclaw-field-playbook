---
---
status: complete
audience: both
chapter: 03
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: en
---

# 3.12 -- Email and messages

## Context

Email is the noisiest and most voluminous source. That's why it comes in third place, after calendar and tasks. Connecting email to a poorly configured agent is like giving them a fire hose when they need a glass of water.

## Email connection

### Configuration

```
openclaw skill add email
```

The agent will:
1. Ask for the provider (Gmail, Outlook, generic IMAP)
2. Set up authentication (OAuth recommended, no plain-text passwords)
3. Define the initial scope

### Recommended scope at startup

| Permission | Recommendation |
|-----------|-----------------|
| Read received emails | Yes -- 48h rolling window |
| Read sent emails | Yes -- for conversation context |
| Draft responses | Yes -- agent prepares, you send |
| Direct sending | No -- add after several weeks of trust |
| Deletion | No |
| Label/folder management | No at the start |

The 48-hour rolling window scope is important: the agent doesn't need your emails from 6 months ago. It needs what arrived recently and is waiting for action.

## Triage: automatic vs assisted

Two modes possible:

### Assisted triage (recommended to start)

The agent classifies your emails and presents you with a summary. You decide.

```
EMAIL TRIAGE -- April 2, 2026, 08:15

URGENT (response today):
- Marc (ClientAlpha): Request for quote modification
  > Impact: quote expires Friday. Respond by Thursday.
- Lea Martin: Interview confirmation 2pm
  > Action: confirm or reschedule

TO HANDLE (this week):
- Supplier X: New pricing schedule
  > Not urgent but impacts Q2 budget
- Accountant: Missing balance sheet documents
  > Deadline: April 10

INFORMATIONAL (no action required):
- Industry newsletter [archive]
- GitHub notification [archive]
- Advertisement [delete]

3 unclassified emails -- would you like me to display them?
```

### Automatic triage (for mature agents)

The agent acts according to predefined rules in CONSTITUTION.md:

```markdown
## Email triage rules
- Newsletters and notifications: archive automatically
- Advertisements and spam: delete automatically
- Email from key contact (see USER.md): high priority
- Email with deadline mentioned: extract deadline, add to tasks
- Everything else: classify as "to handle" for next briefing
```

Only enable automatic triage after 2-3 weeks of validated assisted triage.

## Response drafts

The agent can prepare drafts. This is often the most useful feature:

```
Prepare a response draft for Marc's email
about the quote modification. Professional but firm tone:
we can adjust scope, not price.
```

The agent drafts. You review. You send (or edit and send).

Rule in CONSTITUTION.md:

```markdown
## Emails
- You can draft response emails
- You can NEVER send an email without my explicit validation
- Each draft must indicate: recipient, subject, tone used
```

## The trap: don't connect everything

Email is the source where the "connect everything" trap is most dangerous.

Do NOT connect:
- Shared mailboxes (too much noise, missing context)
- Personal accounts (work/personal separation)
- High-volume mailing lists (technical mailing lists, etc.)

Connect only your primary professional email inbox.

## Messages (Slack, Teams, etc.)

Instant messaging platforms are even noisier than email. If you connect them:

- Limit to 2-3 relevant channels, not the whole workspace
- Read-only mode only
- No automatic replies (never)
- Use them for context, not for action

```markdown
## Messaging
- Connected channels: #general, #project-alpha, #urgent
- Mode: read-only
- Usage: context for briefing, no direct action
```

## Step by step

1. Connect email in read-only mode (48h rolling window)
2. Enable assisted triage for 2 weeks
3. Verify that classification matches your priorities
4. Add response drafts
5. If relevant, switch to automatic triage after validation
6. Instant messages are optional and come last

## Common mistakes

**Connecting email first**: Without calendar and tasks, the agent can't prioritize your emails. It doesn't know you're in meetings all morning or that you have 5 urgent tasks.

**Giving send permission immediately**: An email sent by mistake to a client can't be undone. Draft mode is mandatory at the start.

**Connecting all mailboxes**: 3 email accounts = 150 emails/day in context. The agent drowns.

**No triage rules**: Without explicit rules in CONSTITUTION.md, the agent sorts by its own judgment. Its judgment doesn't know your implicit priorities.

**Forgetting to disconnect noisy sources**: You connected the technical mailing list "just in case". 40 emails/day of pure noise.

## Verification

- [ ] Email connected in read-only mode (48h rolling window)
- [ ] Assisted triage active and validated
- [ ] Triage rules documented in CONSTITUTION.md
- [ ] Response drafts functional
- [ ] Direct sending disabled
- [ ] No shared or personal mailboxes connected
- [ ] If messaging connected: 2-3 channels max, read-only

---
