---
---
status: complete
audience: both
chapter: 03
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: en
---

# 3.15 -- Crons: scheduled automations

## Context

A reactive agent responds when you talk to it. A proactive agent acts without you asking, at defined times.

Crons are the mechanism for proactivity. A cron = a scheduled action that triggers at a fixed time. The morning briefing at 7am. The evening recap at 6pm. Email triage every 2 hours. The heartbeat that verifies everything is working.

## The 4 essential crons

### 1. Morning briefing

The most important. Full details in section 3.16.

```
openclaw cron add --name "briefing-matin" \
  --schedule "0 7 * * 1-5" \
  --prompt "Genere mon briefing du matin selon le format defini dans CONSTITUTION.md"
```

Trigger: Monday to Friday, 7:00am.

### 2. Evening recap

Summary of the day. What was done, what remains, what changed.

```
openclaw cron add --name "recap-soir" \
  --schedule "0 18 * * 1-5" \
  --prompt "Resume de la journee : decisions prises, taches completees, 
  points en attente. Mets a jour MEMORY.md avec ce qui doit etre retenu."
```

Trigger: Monday to Friday, 6:00pm.

The evening recap connects to the next day's briefing. What the recap captures in the evening, the briefing presents in the morning.

### 3. Email triage

Periodic classification of incoming emails.

```
openclaw cron add --name "triage-email" \
  --schedule "0 9,13,17 * * 1-5" \
  --prompt "Trie les emails recus depuis le dernier triage. 
  Classe en urgent/a-traiter/informatif. 
  Notifie-moi uniquement s'il y a des urgents."
```

Trigger: 3 times per day (9am, 1pm, 5pm).

Note: don't triage every 30 minutes. Email is not chat. 3 times per day is enough for the vast majority of contexts.

### 4. Heartbeat

Verification that the agent and its connections are working.

```
openclaw cron add --name "heartbeat" \
  --schedule "0 6 * * *" \
  --prompt "Verifie que toutes les connexions sont actives 
  (calendrier, email, taches). Signale uniquement les problemes."
```

Trigger: every day, 6:00am (before the briefing).

The heartbeat is silent when everything is working. It only notifies you if something is broken.

## Configuration

### Cron syntax

```
openclaw cron add --name "[nom]" \
  --schedule "[expression cron]" \
  --prompt "[instruction pour l'agent]"
```

Common cron expressions:

| Expression | Meaning |
|---|---|
| `0 7 * * 1-5` | Monday-Friday at 7am |
| `0 7 * * *` | Every day at 7am |
| `0 */2 * * 1-5` | Every 2 hours, Mon-Fri |
| `0 9,13,17 * * 1-5` | 9am, 1pm, 5pm, Mon-Fri |
| `30 8 * * 1` | Monday at 8:30am |

### Managing crons

```
openclaw cron list              # See all active crons
openclaw cron pause [nom]       # Pause
openclaw cron resume [nom]      # Reactivate
openclaw cron remove [nom]      # Delete
openclaw cron logs [nom]        # View execution logs
```

## Start with ONE cron only

Steinberg's rule applied to crons: start with one. The morning briefing.

Why:
- You validate that the cron mechanism works
- You verify that the prompt produces a useful result
- You adjust the time and content before adding others
- A misconfigured cron running 3 times per day is 3 times more noise than one

Recommended order of addition:

```
Week 1: morning briefing
Week 2: evening recap (if briefing is solid)
Week 3: email triage (if email is connected)
Week 4: heartbeat
```

## Step by step

1. Create the "briefing-matin" cron with the prompt from section 3.16
2. Verify the first briefing the next morning
3. Adjust the prompt if the result is not satisfactory
4. Live with it for 5 days
5. Add the next cron only when the first one is stable

## Common mistakes

**Too many crons from the start**: 8 crons on day one. You're drowning in notifications. Start with 1.

**Crons too frequent**: Email triage every 15 minutes. The agent consumes tokens for near-identical results. Reduce the frequency.

**Cron prompts too vague**: "Do a check-in." A check-in on what? From which sources? What format? Be as specific in a cron prompt as in a direct interaction.

**Not reading the logs**: A cron failing silently for 2 weeks. Check the logs regularly, at least in the beginning.

**No heartbeat**: Everything works until the day your API token expires and the briefing is empty. The heartbeat catches problems before they impact your work.

## Verification

- [ ] At least 1 active cron (morning briefing recommended)
- [ ] The cron prompt is precise and tested
- [ ] The trigger time matches your rhythm
- [ ] Logs are accessible and verified
- [ ] No more than 2 active crons in the first week
- [ ] Heartbeat planned (even if added later)

---
