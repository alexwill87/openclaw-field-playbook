---
---
status: complete
audience: both
chapter: 04
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: en
---

# 4.1 -- Writing your system prompt

## Context

The system prompt is the most important text in your setup. It's the first thing the agent reads at the start of every conversation. It defines who it is, what it can do, and how it should behave.

A good system prompt = a useful agent from the first response.
A bad system prompt = constant corrections.

## Recommended structure

An effective system prompt follows this order:

### 1. Mission (2-3 sentences)

Who the agent is, who it works for, what its main role is.

```
You are the technical assistant of [your name], freelance devops.
You manage VPS infrastructure, deployments, and task tracking.
You communicate in French, technical terms in English.
```

### 2. Context (what it needs to know)

Permanent facts. Not details that change every week -- those go in memory.

```
Stack: Ubuntu 24.04, Docker, PostgreSQL, Node.js, Vault.
VPS: Hetzner Paris, static IP.
Active projects: cockpit, openclaw-playbook.
```

### 3. Tools and access

What the agent can use. Not the complete documentation -- just the list and limitations.

```
You have access to: bash, local files, git, Docker, PostgreSQL, Vault.
You do NOT have access to: email, Stripe, DNS.
```

### 4. Rules of behavior

Non-negotiable constraints.

```
- Never push --force on main.
- Never modify .env without explicit validation.
- Always create a separate commit, never amend except on explicit request.
- No markdown files except on explicit request.
```

### 5. Tone and format

How it speaks. Short and precise. See section 4.2 for details.

```
- French. Technical terms in English.
- Short responses unless I ask for detail.
- No emojis.
```

## Common mistakes

**Too long.** Every token of the system prompt is sent with every request. 500 words = ~700 tokens. At 1000 requests/month, it adds up. Aim for 150-300 words.

**Too vague.** "Be helpful and professional" says nothing. "Answer in 3 sentences max unless I ask for more" says everything.

**Too much volatile context.** The system prompt is for permanent rules. Current projects, deadlines, statuses -- those go in memory or context files.

**No negative rules.** Saying what the agent should NOT do is as important as saying what it should do. Otherwise it improvises, and improvisation is expensive.

## Complete template

```markdown
# System Prompt — [Your name / project]

## Mission
You are [role] of [who]. You [main responsibility].

## Context
- Stack: [technologies]
- Infra: [provider, location]
- Projects: [list]

## Tools
You have access to: [list].
You do NOT have access to: [list].

## Rules
- [Rule 1 — the most critical]
- [Rule 2]
- [Rule 3]
- NEVER [critical prohibition].

## Tone
- [Language]. Technical terms in English.
- [Style: short/long, formal/direct]
- [Preferred format: bullet points, prose, code]
```

## Steps

1. Write a first version following the structure above.
2. Test with 5 typical requests from your daily usage.
3. Note where the agent responds poorly -- that's a gap in the prompt.
4. Adjust. See section 4.3 for the iteration process.

## Checklist

- [ ] The prompt is under 300 words.
- [ ] The mission is clear in 2 sentences.
- [ ] The rules include at least 2 explicit prohibitions.
- [ ] The tone is defined in an actionable way (not "be professional").
- [ ] Tested with 5 real requests -- responses are correct without correction.

---
