---
---
status: complete
audience: both
chapter: 06
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: en
---

# 01 -- Digital Agency (2 Partners + AI Agents)

**For whom:** duo of entrepreneurs running a digital agency with AI agents as primary workforce
**Setup time:** 2 to 4 weeks
**Difficulty:** Intermediate to Advanced

---

## Context

Two partners are launching a digital agency. Their particularity: the permanent team is limited to just the two of them. The rest of the workforce relies on AI agents configured to execute operational tasks — writing, research, communication, project management.

The challenge: create a central nervous system that coordinates humans and agents, without depending on a closed SaaS, and while maintaining complete control over data.

---

## Problem

- No centralized visibility over ongoing projects
- AI agents operate in silos (one per task, without shared memory)
- Communication between founders goes through too many different channels
- No system to track AI API usage costs
- Client files scattered between local machines and cloud services

---

## Configuration

### Infrastructure

| Component | Choice | Monthly Cost |
|-----------|--------|-------------|
| Server | VPS Hetzner (CPX21, Nuremberg or Helsinki) | 10.00 EUR |
| OS | Ubuntu 24.04 LTS | -- |
| Private network | Tailscale | free (personal plan) |
| Secrets | Vault (HashiCorp, dev mode then production) | -- |
| Database | PostgreSQL 16 | -- |
| Communication | Mattermost (self-hosted) | -- |
| Web cockpit | Next.js + API Routes | -- |

**Total infrastructure cost: approximately 10 EUR/month**

### Budget distribution by pillar (JD6 schema)

The JD6 schema organizes operational domains into numbered categories. For this agency, the monthly budget distribution is as follows:

| Pillar | Domain | Monthly Budget | Description |
|--------|--------|---------------|-------------|
| 10 | Infra | 10.00 EUR | VPS, domain, DNS |
| 30 | Agents | 30.00 EUR | Claude API, Mistral, LLM credits |
| 40 | Knowledge | 40.00 EUR | Embeddings, vector storage, RAG |
| 50 | Communication | 50.00 EUR | Mattermost, transactional email |
| 60 | Business | 60.00 EUR | Client tools, light CRM, billing |

**Total operational budget: approximately 190 EUR/month**

### Agent Architecture

The agency deploys one main agent and specialized agents:

**Main agent (orchestrator):**
- Runs on the VPS, accessible via the web cockpit
- Receives instructions from founders via Mattermost or the cockpit
- Delegates to specialized agents based on task type
- Maintains an activity log in PostgreSQL

**Specialized agents:**
- Writing Agent: business proposals, marketing content, client emails
- Research Agent: competitive intelligence, market analysis, technical documentation
- Ops Agent: server monitoring, alerts, cost reports

### JD6 Schema -- Domain Organization

```
10-19  Infrastructure    (servers, network, DNS, backups)
20-29  Security          (Vault, access, audit, GDPR)
30-39  AI Agents         (configuration, prompts, memory, costs)
40-49  Knowledge         (knowledge base, embeddings, RAG)
50-59  Communication     (Mattermost, email, notifications)
60-69  Business          (clients, projects, billing, CRM)
70-79  Reporting         (dashboards, metrics, KPIs)
```

Each domain has a corresponding folder in the knowledge base and a dedicated channel in Mattermost.

---

## Setup -- Key Steps

### Week 1: Infrastructure

1. Provision the Hetzner VPS
2. Install Ubuntu 24.04, harden SSH (keys only, non-standard port)
3. Install Tailscale on the VPS and founders' machines
4. Deploy PostgreSQL, create `openclaw_main` and `openclaw_knowledge` databases
5. Install Vault, configure secrets for API keys

### Week 2: Agents and Knowledge

1. Install OpenClaw on the VPS
2. Configure the main agent with the agency's system prompt
3. Connect the knowledge base (founder documents, templates, procedures)
4. Deploy specialized agents with their respective prompts
5. Test the pipeline: instruction -> agent -> result -> storage

### Week 3: Communication and Cockpit

1. Deploy Mattermost, create channels by JD6 domain
2. Configure webhooks between OpenClaw and Mattermost
3. Deploy the Next.js cockpit with authentication
4. Connect the cockpit to PostgreSQL for the dashboard
5. Test the complete flow: cockpit -> agent -> Mattermost -> founder

### Week 4: Stabilization

1. Configure automatic backups (PostgreSQL + files)
2. Set up API cost monitoring
3. Document internal procedures
4. Train the two founders on the cockpit
5. Move Vault to production mode

---

## Result

After one month of setup:

- **Operational cockpit**: founders see the status of all projects, real-time API costs, and agent activity from a single interface
- **Functional main agent**: it receives instructions in natural language, routes them to the specialized agent, and returns the result with a link to the produced document
- **Structured communication**: each JD6 domain has its Mattermost channel. Agents post their results in the corresponding channel. Founders no longer search for information
- **Controlled costs**: total monthly budget stays under 200 EUR, with complete visibility on the distribution
- **Data sovereignty**: everything runs on a European VPS. No client data passes through uncontrolled third-party services

---

## Lessons Learned

1. **Start with the main agent, not specialized agents.** The orchestrator is the entry point for the entire system. Without it, specialized agents are isolated tools.

2. **Vault from the start, not "later".** API keys in environment variables in `.env` files don't scale. Vault adds initial complexity but prevents secret leaks.

3. **One Mattermost channel per domain, not per project.** Projects come and go. Domains are stable. Organizing communication by JD6 domain prevents dead channel proliferation.

4. **The cockpit is an investment, not a luxury.** Without a visual interface, founders fall back to terminals and log files. The Next.js cockpit takes time to build but transforms operational quality of life.

5. **Document prompts like code.** Each agent prompt is versioned in Git, with a changelog. Changes are traced and reversible.

---

## Common Mistakes

| Mistake | Consequence | Solution |
|--------|-------------|----------|
| Deploy all agents at once | Debugging impossible, costs explode | Deploy one agent at a time, validate, then move to next |
| Ignore token limits | Truncated responses, lost context | Configure explicit limits and a chunking system |
| No PostgreSQL backup | Loss of knowledge base | Daily pg_dump cron job, copy off VPS |
| Mattermost without strong authentication | Unauthorized channel access | SSO or expiring access tokens |

---

## Template -- Main Agent System Prompt

```
You are the main agent of [AGENCY NAME].

Your role is to coordinate operations between the founders and specialized agents.

Rules:
- You always respond in French unless explicitly asked for English
- You post your results in the Mattermost channel corresponding to the JD6 domain
- You never make financial decisions without human validation
- You document each action in the PostgreSQL database
- You report any API cost anomalies immediately

JD6 Domains:
10-19 Infrastructure | 20-29 Security | 30-39 Agents | 40-49 Knowledge
50-59 Communication | 60-69 Business | 70-79 Reporting

When you receive an instruction:
1. Identify the concerned JD6 domain
2. Check if a specialized agent exists for this domain
3. If yes, delegate with necessary context
4. If no, handle directly and signal that a specialized agent would be useful
5. Post the result in the Mattermost channel of the domain
```

---

## Verification

- [ ] VPS responds on Tailscale from founders' machines
- [ ] Vault stores at least the LLM API keys
- [ ] Main agent responds to a simple instruction via the cockpit
- [ ] Results appear in the correct Mattermost channel
- [ ] PostgreSQL backup works and has been tested for restoration
- [ ] Month's API costs are visible in the cockpit

---

*This use case is inspired by a real implementation experience. Amounts and configurations are representative of a deployment in Europe in 2026.*

---
