---
status: complete
audience: both
chapter: 05
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: en
---

# 5.7 -- Update integrations

## Context

APIs change. Tools evolve. An endpoint that worked yesterday returns a 404 error tomorrow. Your agent uses integrations (Telegram, Vault, PostgreSQL, Docker, GitHub) and each one can break independently.

The challenge: adapt without breaking everything.

## When an API changes

### Warning signals

- The agent receives 4xx/5xx errors on an endpoint it was using.
- An email from the vendor announces a change (deprecation notice).
- A CLI command no longer works after an update.
- Results have changed format (JSON with different fields).

### Update process

1. **Identify**: which endpoint/command has changed.
2. **Read the docs**: changelog, migration guide, new API.
3. **Test in isolation**: call the new version manually before integrating it.
4. **Update the workflow**: modify WORKFLOWS.md with the new command/endpoint.
5. **Test the complete workflow**: dry run with the agent.
6. **Deploy**: update in production.

### Update template

```markdown
## Update integration: [name]

Date: YYYY-MM-DD
Reason: [deprecation / bug / new feature]

### Before
- Endpoint: [old]
- Command: [old]
- Format: [old]

### After
- Endpoint: [new]
- Command: [new]
- Format: [new]

### Impact
- Affected workflows: [list]
- Scripts to modify: [list]

### Test
- [ ] Manual call OK
- [ ] Agent dry run OK
- [ ] Production OK
```

## Adapt without breaking

### Rule 1: never in production first

Always test in isolation. A manual `curl`, a test script, a staging environment. Never directly in the production workflow.

### Rule 2: keep the old one as fallback

Don't remove the old integration until the new one is validated in production for at least one week.

```bash
# Example: new Telegram endpoint
NEW_URL="https://api.telegram.org/bot${TOKEN}/sendMessage"
OLD_URL="https://api.telegram.org/bot${TOKEN}/sendMessage"  # same in this case

# Test the new one
if ! curl -s -f "$NEW_URL" -d "chat_id=$CHAT_ID&text=test" > /dev/null; then
    echo "New endpoint failed, falling back to old one"
    curl -s "$OLD_URL" -d "chat_id=$CHAT_ID&text=test"
fi
```

### Rule 3: one change at a time

Don't update Telegram, Docker, and the GitHub API on the same day. If something breaks, you won't know what. One change, one test, one validation.

## Skills up to date

If your agent uses skills (MCP, plugins, extensions):

### Check available skills

```
List all your skills/tools available.
For each one, tell me:
- Name
- Last used
- Is it still working? (test it)
```

### Update a skill

1. Check the current version.
2. Read the changelog for the new version.
3. Update in a test environment.
4. Test the features you use.
5. Deploy in production.

### Remove unused skills

Each skill is a maintenance point. If you haven't used it for 2 months, disable it. This reduces the attack surface and simplifies debugging.

## Common mistakes

**Ignoring deprecation notices.** "It still works, I'll see later." Then the API cuts off the old endpoint on a Sunday evening.

**Updating blindly.** `pip install --upgrade` or `npm update` without reading the changelog. Breaking change surprise.

**No fallback.** The old one is removed, the new one doesn't work. You're stuck.

**Forgetting to update workflows.** The integration is updated but WORKFLOWS.md still references the old command. The agent uses the old workflow and it crashes.

## Steps

1. List all integrations of your agent.
2. For each one, note the current version and date of last verification.
3. Subscribe to changelogs/release notes for critical tools.
4. When an update is necessary, follow the process above.
5. Update WORKFLOWS.md after each integration change.

## Verification

- [ ] The list of integrations is documented with versions.
- [ ] Each integration has been tested in the last month.
- [ ] Deprecation notices are being tracked.
- [ ] WORKFLOWS.md is up to date after each integration change.
- [ ] A fallback exists for critical integrations.

---
