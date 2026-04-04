---
---
status: complete
audience: both
chapter: 04
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: en
---

# 4.13 -- Audit: what can your agent access?

## Context

You've configured your agent, defined the boundaries, written the system prompt. But do you really know what it can do? Does the reality of its access match your intention?

Audit answers that question. It's an inventory: what the agent can read, write, execute, and what it costs.

## The self-audit prompt

Ask your agent to audit itself:

```
Do a complete audit of your access. For each category,
list what you CAN do and what you CANNOT do.

Categories:
1. File system: which folders/files can you read? write? delete?
2. Database: which tables? SELECT/INSERT/UPDATE/DELETE?
3. Services: which containers can you start/stop/restart?
4. Network: which ports can you reach? which external APIs?
5. Git: which operations? on which branches?
6. Secrets: which secrets can you read? via Vault? in plain text?

For each access, tell me if it's intentional or if it should be restricted.
```

## Verify reality vs intention

The audit often reveals surprises:

| Intention | Reality | Action |
|---|---|---|
| Read-only on /opt | Read + write | Restrict permissions |
| No access to backups | Can read /var/backups | Change folder permissions |
| SELECT only on DB | User has all rights | Create PostgreSQL read-only role |
| No access to secrets | Can read .env | Move secrets to Vault |

### Manual verification

Don't rely solely on self-audit. The agent may not know all its permissions. Verify:

```bash
# Which files the agent can read (test with the user running the agent)
find /opt /home /var -readable -type f 2>/dev/null | head -50

# PostgreSQL rights
psql -c "\du" 
psql -c "\dp" # permissions on tables

# Accessible open ports
ss -tlnp

# Environment variables (potential secrets)
env | grep -i "key\|secret\|token\|pass\|api"
```

## Token budget and costs

Audit also means cost. Every request has a token cost. Track it.

### Calculate the cost

```
Cost per request = input tokens + output tokens

Input tokens = system prompt + context + memory + your message
Output tokens = agent response

Price (Claude Sonnet, April 2026):
- Input: ~$3 / million tokens
- Output: ~$15 / million tokens
```

### What costs a lot

| Element | Typical tokens | Cost/request (estimated) |
|---|---|---|
| Short system prompt (150 words) | ~200 | $0.0006 |
| Long system prompt (500 words) | ~700 | $0.0021 |
| Memory (10 context files) | ~3000 | $0.009 |
| File read in context | ~500-5000 | $0.0015-0.015 |
| Short response | ~200 | $0.003 |
| Long response (code) | ~2000 | $0.03 |

### Optimize costs

- Keep the system prompt under 200 words (section 4.3).
- Don't load all memory on every request.
- For large files, ask the agent to read the relevant part, not the whole file.
- Use bash scripts for repetitive operations instead of asking the agent.

### Monthly tracking

Track your costs each month:

```
March 2026:
- Requests: ~850
- Total cost: ~$12
- Average cost/request: ~$0.014
- Biggest cost: long file reads

Actions: condense system prompt, use tasks.sh instead 
of asking the agent to query the DB.
```

## Common mistakes

**Never audit.** The agent has access you forgot you gave it. One day it causes a problem.

**Audit once and forget.** Access changes when you add services, files, integrations. Audit at least once per quarter.

**Ignore costs.** "It's not expensive." Until the month you make 3000 requests with 5000-token files each. Track to avoid surprises.

**Trust self-audit.** The agent tells you what it thinks it can do. Manually verify what it actually can do.

## Steps

1. Run the self-audit prompt above.
2. Compare with manual verification (find, psql, ss, env).
3. Identify gaps between intention and reality.
4. Fix excessive permissions.
5. Calculate your average monthly cost.
6. Plan a quarterly audit.

## Verification

- [ ] A complete audit has been done (self-audit + manual verification).
- [ ] Gaps between intention/reality are identified and fixed.
- [ ] Excessive permissions are restricted.
- [ ] Monthly cost is known and tracked.
- [ ] A quarterly audit is planned.

---
