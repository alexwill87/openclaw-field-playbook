---
---
status: complete
audience: both
chapter: 03
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: en
---

# 3.3 -- USER.md : your profile for the agent

## Context

SOUL.md defines who the agent is. USER.md defines who YOU are.

Without USER.md, the agent operates in a vacuum. It doesn't know that you hate long emails. That you're in a fundraising phase. That you never work Friday afternoons. That your main contact is named Marc and he's the CTO at your biggest client.

USER.md is the most underestimated file in the configuration. It's also the one that makes the biggest difference.

## The onboarding interview (Steinberg method)

Steinberg recommends starting with an "onboarding interview": 20 questions the agent asks you to build your profile. Here's the adapted list:

### Identity and role
1. What is your current role? How long have you been in it?
2. Who do you report to? Who reports to you?
3. What are your 3 main objectives this quarter?
4. What is your distinctive expertise (what you do better than average)?

### Work style
5. How do you prefer to receive information? (lists, paragraphs, tables, visuals)
6. What is your work rhythm? (morning/evening, focus blocks, availability)
7. What irritates you in written communication?
8. Casual or formal tone with the agent?

### Business context
9. What is your industry?
10. What is your organization's size?
11. What are your main tools daily?
12. What are the 3 subjects you spend the most time on?

### Agent preferences
13. What should the agent do when it doesn't know? (guess, ask, flag)
14. Do you prefer a fast and imperfect response or slow and precise?
15. Should the agent challenge you or execute?
16. What level of detail do you expect by default?

### Key relationships
17. Who are your 5 most frequent contacts? (name, role, context)
18. Are there any sensitive relationships where the agent should be extra careful?
19. Who are the people whose messages deserve priority response?

### Limits
20. What should the agent NEVER do on your behalf?

## What belongs in USER.md

USER.md contains what is STABLE in your profile. The rule:

**If it changes more than once a month, it doesn't go in USER.md.**

| Belongs in USER.md | Does NOT belong in USER.md |
|---|---|
| Your role and responsibilities | Your weekly schedule |
| Your communication preferences | Your current tasks |
| Your key contacts | Pending decisions |
| Your expertise | Recent facts (goes in MEMORY.md) |
| Your quarterly objectives | Your mood today |
| Your work tools | Specific deadlines |
| Your limits and prohibitions | Meeting content |

Where excluded information goes:
- Schedule: calendar connection (section 3.10)
- Current tasks: task system (section 3.11)
- Recent facts: MEMORY.md (section 3.7)
- Pending decisions: active session

## Step by step

### 1. Launch the onboarding interview

```
I want you to ask me the 20 onboarding questions
one by one. Wait for my answer before moving to the next.
At the end, generate my USER.md.
```

### 2. Review and adjust

The agent will generate a USER.md. Review it. Remove what's too volatile. Add what's missing.

### 3. Validate with the 5-sentence test

```
Describe me in 5 sentences.
```

Verify that:
- The 5 sentences are factual (no flattery)
- They cover role, style, context
- Nothing important is missing
- Nothing false appears

If the description is generic ("You are a motivated professional who..."), USER.md is too vague.

### 4. Update quarterly

Block 15 minutes each quarter to review USER.md. Your objectives change. Your contacts evolve. Your role may have shifted.

## Complete USER.md template

```markdown
# USER.md

## Identity
- Name: [your name]
- Role: [your current role]
- Organization: [name, sector, size]
- Main responsibilities: [3-5 lines max]

## Objectives this quarter
1. [Objective 1]
2. [Objective 2]
3. [Objective 3]

## Work style
- Preferred format: [lists / paragraphs / tables]
- Response length: [concise / detailed / depends -- specify]
- Rhythm: [early morning / standard day / evening]
- Focus: [2-hour blocks / multitasking / variable]
- Working language: [French / English / both depending on context]

## Communication
- Casual or formal tone: [choice]
- What irritates me: [concrete examples]
- What I appreciate: [concrete examples]
- When I say "[recurring expression]", I mean [translation]

## Key contacts
| Name | Role | Context | Priority |
|-----|------|----------|----------|
| [Name 1] | [Role] | [Relationship context] | High |
| [Name 2] | [Role] | [Relationship context] | Medium |
| [Name 3] | [Role] | [Relationship context] | Normal |

## Agent preferences
- When you don't know: [ask / flag / propose a hypothesis]
- Speed vs precision: [fast and imperfect / slow and precise]
- Challenge vs execute: [challenge / execute / both]
- Default detail level: [minimum / standard / maximum]

## Prohibitions
- Never [prohibition 1]
- Never [prohibition 2]
- Never [prohibition 3]
```

## Common mistakes

**USER.md too short**: "I'm a dev, I code in Python." The agent doesn't know you. It will give generic answers to a generic "Python dev".

**USER.md too long**: 200 lines of biography. The agent loses the signal in the noise. Aim for 40-60 lines.

**Putting tasks in USER.md**: "I need to finish the report by Friday." That changes every week. It goes in the task system or MEMORY.md.

**Never updating it**: You changed roles 3 months ago but USER.md still says the old one. The agent works with outdated information.

**Forgetting contacts**: The agent can't know that "Marc" in your emails is your main client if you don't tell it.

## Verification checklist

- [ ] Onboarding interview completed (or answers to 20 questions)
- [ ] USER.md generated and reviewed
- [ ] "Describe me in 5 sentences" test passed
- [ ] No volatile information in the file
- [ ] Key contacts documented
- [ ] Agent preferences explicit
- [ ] Next review date noted (in 3 months)
