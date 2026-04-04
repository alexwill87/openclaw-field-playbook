---
---
status: complete
audience: both
chapter: 03
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: en
---

# 3.16 -- The Morning Briefing (Steinberg Method)

## Context

The morning briefing is the ultimate test of your configuration. If the briefing is good, your configuration is good. If it's generic, flat, or off-topic, the problem is upstream: incomplete USER.md, disconnected calendar, empty MEMORY.md.

Steinberg uses the briefing as a diagnostic tool: "Show me your briefing, and I'll tell you what's missing from your config."

## The Exact Prompt

```
Morning briefing.

Sources:
- Calendar: next 24 hours
- Tasks: this week, not completed
- Email: received since last evening
- MEMORY.md: current context

Format:
1. TODAY'S FOCUS: the most important thing today (1 sentence)
2. AGENDA: events of the day with context
3. TO HANDLE: what awaits action from me
4. SIGNALS: what I might have missed
5. SUGGESTION: a concrete action you recommend

Maximum 30 lines. No pleasantries.
```

## If It's Generic, the Problem Is Upstream

A generic briefing looks like this:

```
Hello! Here's your briefing.
You have 4 meetings and 8 tasks. Have a great day!
```

That's not a briefing. That's a counter. Possible causes:

| Symptom | Likely Cause | Solution |
|---|---|---|
| No context on meetings | USER.md without key contacts | Complete USER.md |
| Tasks listed without priority | Non-prioritized task system | Prioritize tasks |
| Emails mentioned without sorting | No triage rules | Define rules in CONSTITUTION.md |
| No relevant suggestions | Empty knowledge/ | Document recurring topics |
| No context reminders | Empty MEMORY.md | End-of-session routine |

## Examples of GOOD Briefings

### Alex -- Independent Consultant

```
TODAY'S FOCUS
Preparation for ClientAlpha steering committee at 2 PM.

AGENDA
09:00  Team standup (routine, 15 min)
10:00-12:00  Free block
  > Suggestion: finalize steering committee slides
14:00-15:30  Steering Committee ClientAlpha -- Marc, Sophie, Technical Director
  > Context: phase 2 of project approved 03/18.
    Budget remaining: 45%. Sophie flagged a scheduling risk
    in her 03/30 email. Needs to be addressed.
16:00  Quick call with accountant -- financial statements

TO HANDLE
- Reply to Sophie (03/30 email): she's waiting for clarifications
  on phase 2 scheduling BEFORE the steering committee
- March invoice ClientBeta: send before Friday

SIGNALS
- Marc hasn't replied to last email (sent 5 days ago).
  Unusual. Worth monitoring at the steering committee.

SUGGESTION
Reply to Sophie this morning. Her scheduling point will
likely come up at the steering committee. Better to have
the answer ready.
```

Why it's good: the focus is clear, the steering committee context is complete (with budget and risk reminders), actions are concrete and prioritized, the signal about Marc is relevant.

### Sam -- CTO Startup

```
TODAY'S FOCUS
Release v2.4 scheduled for 4 PM. Last window before the weekend.

AGENDA
09:00  Dev standup (routine)
09:30-12:00  Code block -- finish fix #847
  > Fix is 80% done (yesterday's session note). Remaining: integration tests.
12:30  Lunch with investor (informal, no prep required)
14:00  Code review PR #312 with Lea
  > PR open for 3 days. Lea waiting for feedback.
16:00  Release window v2.4
  > Checklist: fix #847 merge, tests green, staging OK

TO HANDLE
- Validate PR #312 (blocking Lea for 3 days)
- Reply to backend candidate (response deadline: tomorrow)

SIGNALS
- CI pipeline had 2 flaky tests last night (monitoring).
  Not blocking but worth monitoring before release.

SUGGESTION
Do code review #312 first this morning.
Lea is blocked and it only takes 30 min.
Fix #847 can wait until 10 AM.
```

### Mira -- SME CEO

```
TODAY'S FOCUS
Sign SupplierY contract. Last day offer is valid.

AGENDA
08:30  HR meeting with Julie -- hiring commercial role
  > 3 candidates shortlisted. Julie waiting for your approval
    to move to final interviews.
10:00  Weekly commercial team meeting
  > Pipeline: 2 hot prospects (see knowledge/business/pipeline.md)
11:30-14:00  Free
14:00  Sign SupplierY contract (video call)
  > Amount: 24,000 EUR/year. Negotiated 03/20.
    Terms validated by legal 03/27.
15:30  Bank call -- monthly cash position update

TO HANDLE
- Review SupplierY contract one last time before signing
- Validate 3 HR candidates (Julie waiting for 2 days)

SIGNALS
- Prospect Gamma hasn't followed up since proposal sent 03/22 (10 days).
  Consider a follow-up.

SUGGESTION
Review the contract this morning during the free block.
Validate the HR candidates before Julie's meeting at 08:30
(5-minute email, she'll have the info in hand for the meeting).
```

### Jordan -- Freelance Developer

```
TODAY'S FOCUS
Deliver authentication module for ClientDelta (deadline tomorrow).

AGENDA
09:00-12:00  Dev -- ClientDelta auth module
  > Progress: 70%. Remaining: unit tests + API documentation.
  > Session note yesterday: OAuth flow working, tests in progress.
14:00  Call with ClientDelta -- progress update
  > Lea (project manager) wants status. Have tests passing
    BEFORE the call if possible.
15:00-18:00  Dev -- continue if necessary

TO HANDLE
- ClientEpsilon invoice: 45 days overdue.
  Follow-up sent 03/25, no response.
- ClientZeta quote: request received yesterday, respond by Friday.

SIGNALS
- ClientDelta repo has a dependency (auth-lib) with a CVE
  published yesterday. Medium severity. Needs evaluation.

SUGGESTION
Run unit tests first thing this morning.
If they pass, you'll have concrete updates for the 2 PM call.
Documentation can be done after.
```

## Examples of BAD Briefings

### Too Generic

```
Hello! You have a busy day with 5 meetings
and 12 pending tasks. Have a productive day!
```

Problem: no context, no prioritization, no concrete action. The agent doesn't know the context well enough (USER.md, knowledge/, MEMORY.md empty or insufficient).

### Too Long

```
[45 lines detailing every email received, every task,
every event with 5 lines of context each]
```

Problem: the briefing is a report, not a briefing. If it takes 5 minutes to read, it's too long. Maximum 30 lines.

### False Context

```
FOCUS: Prepare presentation for the board.
[You don't have a board. The agent invented it.]
```

Problem: the agent "fills the gaps" by inventing facts. CONSTITUTION.md must explicitly forbid inventing facts.

## Step by Step

1. Configure the morning-briefing cron (section 3.15)
2. Use the exact prompt above
3. Read the first briefing and evaluate:
   - Is the focus correct?
   - Is the meeting context relevant?
   - Are the actions concrete?
   - Is the suggestion useful?
4. If not, identify the upstream cause (USER.md? MEMORY.md? sources?)
5. Adjust the config, not the prompt
6. Iterate for 5 days before considering the briefing stable

## Common Mistakes

**Adjusting the prompt instead of the config**: The briefing is flat so you rewrite the prompt 10 times. The problem isn't the prompt. It's that the sources are empty.

**Briefing on weekends**: If you don't work weekends, disable the cron. An empty Saturday briefing creates noise.

**No SIGNALS section**: Signals are the agent's added value. What YOU would have missed because it's buried in an email or calendar. Without this section, the agent is just a schedule reader.

**Pleasantries**: "Hello, I hope you're doing well." Wasted space. The briefing is a tool, not a conversation.

## Verification

- [ ] Morning-briefing cron active
- [ ] Precise prompt with 5 sections (focus, agenda, to handle, signals, suggestion)
- [ ] Maximum 30 lines
- [ ] Focus is specific (not generic)
- [ ] Meeting context crosses USER.md and knowledge/
- [ ] Suggestions are concrete and actionable
- [ ] No pleasantries
- [ ] If briefing is flat: upstream diagnosis (USER.md, MEMORY.md, sources)
