---
---
status: complete
audience: both
chapter: 03
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: en
---

# 3.10 -- Calendar First, Always (Steinberg Principle)

## Context

If you only connect one source, connect the calendar. It's the first connection, without exception.

Steinberg is emphatic: the calendar is the most honest signal of your professional life. Not what you say you do. Not what you'd like to do. What you ACTUALLY do.

## The 4 Reasons to Start with the Calendar

### 1. The Calendar Doesn't Lie

Your emails are noisy. Your tasks are incomplete. Your CRM is out of sync. But your calendar reflects your real commitments. If it's in the calendar, it's going to happen (or it should have).

### 2. The Calendar Sets the Pace

An agent that knows your calendar understands:
- That you're in a meeting from 10am to 11am (don't interrupt)
- That you have a client presentation at 2pm (prepare context)
- That your afternoon is free (ideal time for deep work)
- That tomorrow is packed (keep the briefing short)

### 3. The Calendar Connects People

Every calendar event involves people. The agent cross-references these people with USER.md (key contacts) and knowledge/ (client context). The briefing goes from "You have 4 meetings" to "You're seeing Marc from ClientAlpha at 2pm -- reminder: the pricing proposal has been pending since 03/25."

### 4. The Calendar Has Low Noise

Unlike emails (50/day) or messages (200/day), the calendar generates 5 to 15 events per day. Low volume, high relevance.

## Setup

### Via skill

```
openclaw skill add calendar
```

The agent will:
1. Ask you for the provider (Google Calendar, Outlook, CalDAV)
2. Configure authentication
3. Define the scope (read-only recommended at first)
4. Create the skill in your workspace

### Recommended Scope

| Right | Recommendation |
|-------|----------------|
| Read events | Yes |
| Read participants | Yes |
| Read descriptions | Yes |
| Create events | No (add later if needed) |
| Modify events | No |
| Delete events | No |

Start with read-only. Add write permissions after 2 weeks of use if necessary.

## Validation

The validation test is simple:

```
Show me my next 48 hours.
```

The agent should display:
- Events in chronological order
- Participants for each meeting
- Free slots
- Events that deserve preparation

If the display is correct and the cross-references are relevant (links to contacts in USER.md), the connection is validated.

### What Makes a Calendar Briefing USEFUL

```
WEDNESDAY, APRIL 2

09:00-09:30  Team standup
  > Nothing special -- weekly routine

10:00-11:00  Project Alpha check-in with Marc (ClientAlpha)
  > Preparation: the pricing proposal sent on 03/25
    hasn't received a response yet. Likely topic.

11:00-14:00  Free block
  > Suggestion: handle the 3 pending emails

14:00-15:00  Recruitment interview -- Lea Martin (backend dev position)
  > CV in knowledge/recruitment/lea-martin.md

15:30-16:00  Investor call -- Epsilon Fund
  > Context: second call. The first was on 03/18.
    Notes in MEMORY.md.
```

### What Makes a Calendar Briefing USELESS

```
You have 4 meetings tomorrow: standup, project check-in,
interview, call. Have a good day!
```

If your briefing looks like the second example, the problem isn't the calendar. It's that USER.md and knowledge/ are too empty for the agent to make cross-references.

## Step by Step

1. Connect the calendar in read-only
2. Test with "Show me my next 48 hours"
3. Verify that cross-references with USER.md work
4. Live with it for 5 days before adding another source
5. Add write permissions only if necessary

## Common Mistakes

**Connecting email before the calendar**: Email is noisy, the calendar is structured. Reverse the order and you'll debug email noise without the calendar as a reference point.

**Ignoring participants**: A calendar without cross-referencing key contacts is just a schedule. The value comes from the link between the event and the context.

**Giving write permissions immediately**: The agent creates an event by mistake, and you have a "Q3 Strategy Review" on a Saturday in your calendar. Start with read-only.

**Not filling out USER.md first**: Calendar without context = a list of events. Calendar with USER.md = an intelligent briefing.

## Checklist

- [ ] Calendar connected in read-only
- [ ] Test "Show me my next 48 hours" successful
- [ ] Participants are cross-referenced with key contacts in USER.md
- [ ] Free slots are identified
- [ ] Briefing is contextual (not just a simple list)
- [ ] 5 days of use before adding another source
