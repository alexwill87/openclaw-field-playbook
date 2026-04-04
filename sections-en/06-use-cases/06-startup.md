---
---
status: complete
audience: both
chapter: 06
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: en
---

# 06 -- Startup early-stage

**For whom:** startup founders in early stage (pre-seed to seed), team of 2 to 8 people
**Implementation time:** 3 to 5 days
**Difficulty:** Intermediate

---

## Context

An early-stage startup has limited resources and disproportionate needs. Founders wear every hat: product, sales, technology, finance, HR. They must communicate regularly with investors, monitor the market, hire their first employees, and build the product -- all with a tight budget.

OpenClaw can become a force multiplier by automating low-value-added tasks, freeing up time for strategic decisions.

---

## Problem

- Investor updates are written at the last minute, often incomplete
- Competitive intelligence is done sporadically and unstructured
- Recruiting is slow: manual CV sorting, candidate follow-up scattered across emails
- Key metrics (MRR, churn, runway) are calculated manually in spreadsheets
- Founders spend more time on operations than on strategy

---

## Configuration

### Infrastructure

| Component | Choice | Monthly cost |
|-----------|--------|-------------|
| Server | Budget VPS (Hetzner CX22) or local laptop | 0-5 EUR |
| OpenClaw | VPS or local installation | -- |
| Communication | Slack or Mattermost (free plan) | free |
| Tracking | Notion, Linear, or Markdown files | existing |
| Email | Existing email service | existing |

**Total budget: less than 50 EUR/month all-in** (VPS + LLM API).

### Agents

**Investor Relations Agent:**
- Collects key metrics from the startup's tools (spreadsheet, database, API)
- Generates a monthly investor update draft in standard format
- Includes: key metrics, highlights, challenges, needs, next steps
- Founder reviews, adjusts tone, and sends

**Intelligence Agent:**
- Monitors defined sources (blogs, newsletters, Product Hunt, social media)
- Generates a weekly summary of competitive movements
- Flags critical events in real-time (competitor funding, product launch)
- Categorizes by relevance: direct impact / monitor / background noise

**Recruitment Agent:**
- Sorts incoming applications by alignment with job description
- Generates a summary of each CV with strengths and points of concern
- Proposes a draft response (acceptance for interview / polite rejection)
- Tracks ongoing applications and follows up on pending candidates

---

## Implementation

### Day 1-2: Infrastructure and Investor Relations Agent

1. Install OpenClaw (VPS or local)
2. Configure the Investor Relations Agent with:
   - The investor update format used by the startup
   - Metric sources (spreadsheet, API, database)
   - Communication tone with investors
3. Test by generating last month's update
4. Compare with the actual update and adjust

### Day 3: Intelligence Agent

1. Define intelligence sources (5 to 10 sources maximum to start)
2. Define competitors to monitor
3. Configure frequency: weekly summary + real-time alerts
4. Test on the previous week
5. Adjust relevance filters

### Day 4-5: Recruitment Agent and stabilization

1. Configure the Recruitment Agent with active job descriptions
2. Define sorting criteria (required skills, nice-to-have, red flags)
3. Test on a batch of 20 CVs (real or anonymized)
4. Set up notifications for all agents
5. Document workflows for the team

---

## Results

After one month of use:

- **Investor updates in 30 minutes instead of 3 hours:** the agent collects metrics and generates the first draft. The founder adjusts the narrative and sends. Updates go out on time, every month
- **Structured intelligence:** the weekly summary replaces sporadic monitoring. Two critical alerts were detected (competitor launch, regulatory change) that would have been missed otherwise
- **Accelerated CV sorting:** 80% of sorting is done by the agent. The founder only spends time on pre-selected applications. Recruitment time reduced by 30%
- **Budget controlled:** the entire setup costs less than 50 EUR/month, the price of a single SaaS tool

---

## Lessons learned

1. **The investor update is the workflow to deploy first.** It's regular, structured, and every founder hates doing it. The impact on investor relationships is immediate: updates arrive on time and are more complete.

2. **Intelligence must be filtered aggressively.** 10 well-chosen sources are better than 50 sources that generate noise. The agent must be configured to ignore noise, not report everything.

3. **AI-based CV sorting has biases.** The agent can eliminate atypical profiles that would be good candidates. The founder must verify a sample of applications rejected by the agent to calibrate.

4. **No complex stack in early-stage.** If the team has 3 people, a 5 EUR VPS and Markdown files are enough. PostgreSQL and Mattermost will come when the team exceeds 8 people.

5. **Document prompts in Git from the start.** Even in early-stage, prompts are code. Versioning them allows you to revert when a change degrades results.

---

## Common mistakes

| Mistake | Consequence | Solution |
|---------|-------------|----------|
| Investor update sent without review | Incorrect metrics sent to investors | Always review and manually validate figures |
| Too many intelligence sources | Weekly summary too long, not read | Maximum 10 sources to start, add progressively |
| Blind trust in CV sorting | Good candidates eliminated by agent | Verify a sample of applications rejected |
| Over-sized stack | Time spent maintaining infrastructure instead of building product | Start minimal, evolve with team |

---

## Template -- System prompt for the Investor Relations Agent

```
You are the Investor Relations assistant for [STARTUP NAME].

Context:
- [NAME] is a [SECTOR] startup in [PHASE]
- Last funding: [AMOUNT] in [DATE]
- Investors: [LIST]
- Key metrics tracked: MRR, number of users, churn, runway

Format of the monthly investor update:

## [NAME] - Update [MONTH YEAR]

### Key metrics
| Metric | This month | Last month | Change |
|--------|-----------|-----------|---------|
| MRR | | | |
| Active users | | | |
| Churn | | | |
| Runway (months) | | | |

### Highlights
- [3 to 5 positive points from the month]

### Challenges
- [2 to 3 friction points or risks]

### How you can help
- [1 to 2 concrete requests to investors]

### Next steps
- [3 to 5 objectives for next month]

Rules:
- You collect metrics from [SOURCE]
- You generate a draft, never a final document
- You do not speculate on figures: if data is missing, flag it
- You maintain a professional and factual tone, neither too optimistic nor alarming
```

---

## Checklist

- [ ] The Investor Relations Agent generates a coherent update with available metrics
- [ ] The update format matches the format normally used by the startup
- [ ] The Intelligence Agent produces a relevant weekly summary
- [ ] Critical alerts are detected and notified quickly
- [ ] The Recruitment Agent correctly sorts a batch of 20 test CVs
- [ ] Total monthly cost remains under 50 EUR

---

*An early-stage startup doesn't need an enterprise AI platform. It needs 3 well-configured agents and a controlled budget.*

---
