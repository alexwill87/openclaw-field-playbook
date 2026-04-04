---
---
status: complete
audience: both
chapter: 06
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: en
---

# 04 -- Technical Team (5-15 people)

**For whom:** mid-sized development or operations team
**Setup time:** 1 to 2 weeks
**Difficulty:** Intermediate

---

## Context

A technical team of 5 to 15 people works on one or more software products. Code is on GitHub or GitLab. Documentation exists but is rarely up to date. Code reviews take time. New hires take weeks to become autonomous.

The team wants to use OpenClaw to speed up repetitive tasks without replacing human judgment on architectural decisions.

---

## Problem

- Technical documentation is obsolete or incomplete
- Code reviews are a bottleneck
- Onboarding new developers is slow and informal
- Architectural decisions are made in meetings but poorly documented
- Production incidents are resolved but post-mortems are not written

---

## Configuration

### Infrastructure

| Component | Choice | Monthly cost |
|-----------|--------|-------------|
| Server | Dedicated VPS or existing cloud instance | variable |
| OpenClaw | Installation on the team's server | -- |
| Code | GitHub or GitLab (existing) | existing |
| Communication | Slack, Mattermost or Teams (existing) | existing |
| Knowledge base | Existing wiki or Markdown in the repo | existing |

### Agents

**Documentation Agent:**
- Monitors merged Pull Requests
- Detects changes that impact existing documentation
- Generates a draft documentation update
- Posts the draft as a comment on the PR or in the documentation channel

**Code Review Agent:**
- Performs an initial pass on open Pull Requests
- Verifies: style, naming conventions, test coverage, known patterns
- Posts a structured comment with attention points
- Never blocks a PR: its comments are informational, not blocking

**Onboarding Agent:**
- Maintains an up-to-date onboarding guide from the knowledge base
- Answers questions from new hires on the dedicated channel
- Points to existing documentation rather than answering directly
- Flags recurring questions not covered by the documentation

**Post-mortem Agent:**
- After an incident, collects messages from the incident channel
- Generates a structured post-mortem draft (timeline, root cause, actions)
- Submits it to the team for validation and enrichment

---

## Setup

### Week 1: Foundations

1. Install OpenClaw on the team's server
2. Connect the GitHub/GitLab API
3. Deploy the Code Review agent on a pilot repo
4. Configure the team's conventions in the system prompt (style guide, forbidden patterns, naming rules)
5. Test on 5 existing Pull Requests
6. Adjust the prompt based on team feedback

### Week 2: Complementary agents

1. Deploy the Documentation Agent
2. Deploy the Onboarding Agent with the existing knowledge base
3. Configure the Post-mortem Agent with the team's template
4. Train the team on the use and limitations of each agent
5. Define the rules: the agent informs, humans decide

---

## Result

After one month of use:

- **Documentation up to date:** update drafts are generated automatically. The rate of obsolete documentation drops from 60% to 15%
- **Faster code reviews:** the agent's initial pass detects mechanical issues (style, naming, missing tests). Human reviewers focus on logic and architecture. Average review time reduced by 40%
- **Structured onboarding:** new hires have a contact available 24/7 for basic questions. Time to autonomy reduced from 3 weeks to 10 days
- **Systematic post-mortems:** each incident has its post-mortem written within 24 hours, instead of "we'll do it later" (meaning never)
- **Coordinated multi-agents:** agents share the knowledge base. A documentation update by the Documentation Agent is immediately available to the Onboarding Agent

---

## Lessons Learned

1. **Start with Code Review, not documentation.** The Code Review Agent has visible impact immediately and builds buy-in within the team.

2. **Conventions must be explicit in the prompt.** The agent cannot guess the team's style guide. If the rules are not written, it applies generic conventions that frustrate developers.

3. **The agent must never block a workflow.** Its comments are informational. The day the agent blocks a PR by mistake, the team loses confidence and disables everything.

4. **Automatic post-mortems are the best effort-to-value ratio.** Nobody likes writing a post-mortem. The agent generates a first draft from incident channel messages. The team corrects and completes it in 15 minutes.

5. **Plan an "agent-feedback" channel for the team.** Developers must be able to report when the agent is wrong. This feedback improves prompts and maintains trust.

---

## Common Mistakes

| Mistake | Consequence | Solution |
|---------|-------------|----------|
| Code Review Agent too strict | Developers who ignore all its comments | Informational tone, never imperative. No false positives |
| Documentation generated without review | Factual errors in the knowledge base | Draft + mandatory human validation |
| No scope limit for the Onboarding Agent | Off-topic or made-up answers | Limit to existing knowledge base content |
| Deploying to all repos at once | Excessive noise, rejection by the team | One pilot repo, then progressive expansion |

---

## Template -- Code Review Agent System Prompt

```
You are the code review assistant for the [NAME] team.

Your role is to perform an initial pass on Pull Requests to detect
mechanical issues. You do not replace the human reviewer.

Rules:
- Your comments are informational, never blocking
- You use a "suggestion" tone: "Consider..." rather than "You must..."
- You do not comment on architecture or design choices
- You point to existing documentation when relevant

What you verify:
1. Compliance with style guide: [LINK TO STYLE GUIDE]
2. Naming conventions: [RULES]
3. Test coverage: each new function must have a test
4. Forbidden patterns: [LIST]
5. Modified configuration files: flag for special attention

What you do not do:
- Evaluate the functional relevance of the change
- Suggest major refactorings
- Comment on architectural choices
- Block or approve the PR

Format of your comment:
## Automated initial pass

**Style:** [OK / X points to check]
**Tests:** [OK / tests missing for functions X, Y]
**Attention:** [sensitive files modified, if any]

_This comment is generated by the Code Review Agent. It does not replace
human review._
```

---

## Checklist

- [ ] The Code Review Agent comments on PRs from the pilot repo
- [ ] Comments respect the informational tone (no blocking false positives)
- [ ] The Documentation Agent detects PRs impacting documentation
- [ ] The Onboarding Agent correctly answers 10 typical questions
- [ ] The Post-mortem Agent generates a coherent draft from a test incident channel
- [ ] The agent-feedback channel is created and the team knows how to use it

---

*AI agents in a technical team work when they reduce noise, not when they add to it.*

---
