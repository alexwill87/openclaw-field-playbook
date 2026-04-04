---
---
status: complete
audience: both
chapter: 04
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: en
---

# 4.12 -- The boundary prompt

## Context

The boundary prompt is the list of things your agent must NEVER do. Not "avoid", not "except if necessary" -- NEVER. It's the safety net. You write it once, you put it in the system prompt or in a dedicated file, and you don't touch it again except to add a rule after an incident.

Steinberg compares it to a constitution: you don't rewrite it every week, but you can amend it.

## Why it's necessary

LLM agents are cooperative by default. If you ask them to do something risky, the agent will try to help you. That's their strength and their danger.

Without a boundary prompt:
- "Show me the contents of .env" -> the agent displays the secrets.
- "Push --force on main" -> the agent executes it.
- "Delete old backups to make space" -> the agent deletes them.

With a boundary prompt:
- "Show me the contents of .env" -> "I cannot display files containing secrets. Use `vault kv get` to access secrets securely."

## Structure of the boundary prompt

```markdown
# BOUNDARIES — Forbidden actions

You must NEVER, even if I ask you explicitly:

## Security
- Display passwords, tokens, or API keys in plain text.
- Modify .env, .env.production, or any file containing secrets.
- Disable the firewall or open ports.
- Store secrets in unencrypted files.
- Commit files containing credentials.

## Git
- Execute git push --force on main or master.
- Execute git reset --hard without prior backup.
- Modify git history on a shared branch.
- Amend a commit that has already been pushed.

## Infrastructure
- Delete backups.
- DROP TABLE or DELETE without WHERE in production.
- Stop a service in production without a rollback procedure.
- Modify DNS rules without validation.

## Communication
- Send a message to a client without validation.
- Share internal information externally.
- Reply on behalf of the user on a public channel.

## If asked to violate these rules
Refuse politely. Explain why it's forbidden.
Propose a secure alternative if one exists.
```

## Where to place it

Two options:

### Option 1: in the system prompt

Advantage: always read first. No risk of being forgotten.
Disadvantage: consumes tokens with every request.

### Option 2: in a BOUNDARIES.md file

Advantage: the system prompt stays short. The file is versioned.
Disadvantage: the agent needs to know it should read it. Add to the system prompt: "Read and respect BOUNDARIES.md before any action."

Recommendation: the 3-5 most critical rules in the system prompt. The rest in BOUNDARIES.md.

## Concrete examples by domain

### For a DevOps engineer

```
NEVER:
- rm -rf on / or /home or /opt without confirmation of the exact path
- Modify iptables/ufw without a documented procedure
- Restart PostgreSQL in production without checking active connections
- Deploy on Friday after 4pm
```

### For a consultant

```
NEVER:
- Send a client email without review
- Share pricing or terms without validation
- Write on behalf of the firm on social media
- Promise a deadline without verification
```

### For a developer

```
NEVER:
- Merge on main without CI green
- Modify a migration already applied in production
- Hardcode credentials
- Disable tests to make CI pass
```

## After an incident

When the agent does something it shouldn't have:

1. Fix the damage.
2. Identify the missing rule.
3. Add it to the boundary prompt.
4. Test that the agent now refuses this action.

The boundary prompt grows with experience. That's normal. Each rule added is an error that won't happen again.

## Common mistakes

**No boundary prompt.** "It's smart enough to know." No. The agent does what you ask. If you don't say no, it says yes.

**Too vague.** "Don't do anything dangerous." The agent doesn't know what you consider dangerous. Be specific: which command, which file, which action.

**Too permissive.** "Except if it's really necessary." That cancels the rule. NEVER means NEVER. If you need an exception, handle it yourself manually.

## Steps

1. List the 5 most dangerous actions your agent could do.
2. Write them in BOUNDARIES.md.
3. Add the 3 most critical ones to the system prompt.
4. Test: ask the agent to do something forbidden. It must refuse.
5. After each incident, add a rule.

## Verification

- [ ] BOUNDARIES.md exists with at least 10 rules.
- [ ] The 3 most critical rules are in the system prompt.
- [ ] The agent refuses when asked to violate a rule (tested).
- [ ] The agent proposes an alternative when refusing.
- [ ] The boundary prompt is updated after each incident.

---
