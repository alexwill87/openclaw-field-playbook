---
---
status: complete
audience: both
chapter: 03
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: en
---

# 3.5 -- CONSTITUTION.md : the rules of the game

## Context

SOUL.md says who the agent is. CONSTITUTION.md says what it is ALLOWED to do.

This is the contract between you and the agent. Not a suggestion, not a preference: a contract. The agent must comply with it for every action.

CONSTITUTION.md is the file you will reread most often, because your rules evolve with trust. A freshly configured agent has strict rules. An agent that has proven itself over 3 months gets more autonomy.

## The 3 levels of autonomy

### Level 1 -- Autonomous execution

The agent acts without notifying you. Use this level for low-risk, high-frequency actions.

```markdown
## Full autonomy
You can without validation :
- Read all configuration files and knowledge/
- Update MEMORY.md (additions, compression)
- Create drafts in drafts/
- Generate summaries and reports
- Rephrase and correct existing texts
- Answer factual questions in session
```

### Level 2 -- Execution with notification

The agent acts, then notifies you. For moderate-risk actions you want to monitor without blocking.

```markdown
## Autonomy with notification
You can act then notify me :
- Modify a file in knowledge/ (tell me which one and why)
- Reorganize the structure of MEMORY.md (show me the diff)
- Create a new file in the workspace (alert me)
- Update an existing draft (flag the changes)
```

### Level 3 -- Prior validation

The agent proposes, you validate. For any action with external impact or that is irreversible.

```markdown
## Validation required
You must ask me BEFORE :
- Send an email or message to anyone
- Publish content (blog, social media, public documentation)
- Modify a database
- Delete a file or data
- Make a commitment (date, price, deliverable)
- Contact a third party on my behalf
```

## Explicit prohibitions

Prohibitions are not levels of autonomy. They are absolute red lines.

```markdown
## Prohibitions
NEVER, even if I explicitly ask you to :
- Invent facts or figures
- Pretend you did something you didn't do
- Ignore an error to move faster
- Store passwords in plain text
- Send personal data to an unapproved third-party service
- Modify CONSTITUTION.md without discussing it first
```

The "even if I ask you to" clause is intentional. It protects against poor judgment under pressure. You can always modify CONSTITUTION.md thoughtfully, but the agent should not simply obey a contradictory instruction given in urgency.

## Validation conditions

When the agent requests validation, the request must be structured :

```markdown
## Validation format
When you request validation, use this format :

[ACTION] : What you want to do
[CONTENT] : Summary of the content or change
[REASON] : Why this action
[IMPACT] : Foreseeable consequences
[RISK] : What could go wrong

Wait for my explicit response (yes/no/modify) before acting.
```

## Step by step

### 1. Start with the 3 levels

Copy the structure above. Adapt the lists to your context.

### 2. Add prohibitions

List 5-10 things the agent should never do. Be specific.

### 3. Define the validation format

Adapt the format above if needed. The essential thing is that each validation request contains : action, reason, impact.

### 4. Add clauses specific to your profession

Examples by context :

**Consultant** :
```
- Never share one client's data with another client
- Always anonymize examples taken from previous projects
```

**E-commerce** :
```
- Never modify a price without validation
- Always check stock before confirming an order
```

**Developer** :
```
- Never push to main without validation
- Always run tests before proposing a merge
```

### 5. Test the constitution

```
I want you to send an email to my main client
to cancel our meeting tomorrow.
```

The agent must :
1. Identify that this is an external action (level 3)
2. Request validation with the defined format
3. Wait for your response

If it acts directly, CONSTITUTION.md is not clear enough.

## Complete CONSTITUTION.md template

```markdown
# CONSTITUTION.md

Version : 1.0
Last updated : [date]
Next review : [date + 1 month]

---

## Full autonomy
You can without validation :
- [List of low-risk actions]

## Autonomy with notification
You can act then notify me :
- [List of moderate-risk actions]

## Validation required
You must ask me BEFORE :
- [List of actions with external impact or irreversible]

## Prohibitions
NEVER, even if I explicitly ask you to :
- [List of absolute red lines]

## Validation format
When you request validation :
- [ACTION] : what you want to do
- [CONTENT] : summary
- [REASON] : why
- [IMPACT] : consequences
- [RISK] : what could go wrong
Wait for my explicit response before acting.

## Business rules
- [Rule specific to your context 1]
- [Rule specific to your context 2]
- [Rule specific to your context 3]

## Evolution of this constitution
- Modifications are made through discussion, never through direct instruction in session
- Each modification is dated and justified
- Scheduled monthly review
```

## Common mistakes

**Constitution too permissive** : "Do whatever you want as long as it's reasonable." The definition of "reasonable" differs between you and the agent.

**Constitution too restrictive** : Everything at level 3. You spend your day validating. Start strict, then gradually increase the level of autonomy.

**No explicit prohibitions** : Implicit prohibitions don't exist for an agent. If you don't write it, it doesn't know it.

**Constitution never reviewed** : You trust the agent after 2 months, but its constitution is still the one from day 1. Review every month.

**Confusing CONSTITUTION.md and SOUL.md** : "Be careful" is a personality trait (SOUL.md). "Never modify production database without validation" is a rule (CONSTITUTION.md).

## Verification

- [ ] The 3 levels of autonomy are defined with concrete actions
- [ ] Prohibitions are listed explicitly
- [ ] The validation format is documented
- [ ] Profession-specific rules are added
- [ ] The external action test works (the agent properly requests validation)
- [ ] The date of next review is noted

---
