---
---
status: complete
audience: both
chapter: 03
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: en
---

# 3.14 -- Data Sovereignty

## Context

Your agent handles your emails, calendar, tasks, customer data. The question is not IF this data is sensitive, but WHERE it lives and WHO has access to it.

Data sovereignty is not a theoretical topic. It's an architectural decision that impacts your legal compliance, customer trust, and your ability to switch providers.

## Where Your Data Lives

Three models:

### Local

All data stays on your machine or server.

```
+----------------------------+
|  YOUR MACHINE / VPS        |
|                            |
|  SOUL.md                   |
|  USER.md                   |
|  CONSTITUTION.md           |
|  MEMORY.md                 |
|  knowledge/                |
|  skills/                   |
|  local database            |
|                            |
+----------------------------+
      |
      | API calls (prompts)
      v
+----------------------------+
|  LLM PROVIDER              |
|  (prompts transit,         |
|   not files)               |
+----------------------------+
```

Advantages:
- Full control
- No dependency on a third-party service for storage
- Simplified GDPR compliance

Disadvantages:
- Maintenance is your responsibility (backup, security, updates)
- Limited access to your machine / network

### Cloud

Data lives with a cloud provider.

Advantages:
- No infrastructure maintenance
- Access from anywhere
- Automatic backup

Disadvantages:
- Your data is with a third party
- Vendor dependency (lock-in)
- More complex GDPR compliance (depending on server location)

### Hybrid (Recommended)

Configuration and memory locally. External services for what requires it.

```
+----------------------------+    +---------------------------+
|  LOCAL                     |    |  CLOUD                    |
|                            |    |                           |
|  SOUL.md                   |    |  Calendar (Google/O365)   |
|  USER.md                   |    |  Email (provider)         |
|  CONSTITUTION.md           |    |  CRM (if SaaS)            |
|  MEMORY.md                 |    |                           |
|  knowledge/                |    +---------------------------+
|  skills/                   |
|  vault (secrets)           |
|  logs                      |
|                            |
+----------------------------+
```

The rule: your configuration files, your memory, and your secrets stay local. External services are accessed via API with minimum necessary permissions.

## GDPR: What You Need to Know

If you are in Europe or process data of European residents, GDPR applies.

### Key Points for Your Agent

**Legal basis**: You must have a legal basis for processing data through the agent (legitimate interest, consent, contract execution).

**Minimization**: The agent should only access strictly necessary data. Don't "connect everything just in case."

**Location**: Prioritize providers whose servers are in Europe. If the LLM provider is outside the EU, prompts transit outside the EU -- make sure personal data is anonymized in prompts.

**Right to erasure**: If a customer requests deletion of their data, it must also disappear from knowledge/, MEMORY.md, and any agent files.

**Processing register**: Document what data the agent processes, why, and where it is stored. A knowledge/legal/gdpr.md file is a good place.

### Minimal GDPR Checklist

```markdown
## Processing Register -- OpenClaw Agent

| Data | Purpose | Legal basis | Storage | Duration |
|------|---------|-------------|---------|----------|
| Customer emails | Sorting and drafts | Legitimate interest | Local (48h cache) | 48h |
| Calendar | Daily briefing | Legitimate interest | API (no copy) | Session |
| Customer contacts | Relationship context | Contract execution | knowledge/ | Contract duration |
| Meeting notes | Agent memory | Legitimate interest | MEMORY.md | 2 weeks |
```

## Recommended European Hosting

For VPS or local server:
- OVH (France)
- Hetzner (Germany)
- Scaleway (France)
- Infomaniak (Switzerland)

For cloud services:
- Prioritize options with datacenters in the EU
- Verify transfer conditions outside the EU
- Read the DPA (Data Processing Agreements)

## Step by Step

1. Map where your data currently lives
2. Decide on the model (local / cloud / hybrid)
3. Make sure configuration files are local
4. Store secrets in a vault, never in plain text
5. If GDPR applicable: create the processing register
6. Choose European hosting if possible
7. Document your choices in knowledge/legal/ or knowledge/infra/

## Common Mistakes

**Ignoring the question**: "It's just an agent, not a public service." Your agent potentially processes personal data of your customers. GDPR applies.

**Secrets in plain text in files**: An API token in SOUL.md or in a skill. Use a vault.

**No backup**: Your configuration and knowledge/ represent weeks of work. Back them up.

**Everything in cloud without thinking**: Convenient, but your data is with a third party. Make sure you understand the implications.

**Forgetting the right to erasure**: A customer requests deletion of their data. You delete it from the CRM but it remains in knowledge/clients/client-x.md and in MEMORY.md.

## Verification

- [ ] You know where each of your data lives
- [ ] Configuration files are local
- [ ] Secrets are in a vault
- [ ] If GDPR applicable: processing register created
- [ ] European hosting chosen (or documented justification if not)
- [ ] Data deletion procedure documented
- [ ] Backup in place for configuration and knowledge/

---
