---
---
status: complete
audience: both
chapter: 03
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: en
---

# 3.1 -- Define the agent's scope

## Context

An agent without clear scope is a dangerous agent. Not because it will "rebel" -- because it will do things you didn't anticipate. Send an email to a client with an inappropriate tone. Modify a production file. Make a financial decision.

Scope is not a list of features. It's a trust contract between you and the agent.

## The rights pyramid

Three levels, from most permissive to most restrictive:

```
        /\
       /  \
      / 3  \    EXTERNAL ACTION
     / val. \   Validation required each time
    /--------\
   /    2     \  WRITE
  /  autonomous \ The agent acts alone within a defined framework
 /--------------\
/       1        \ READ
/ always allowed  \ The agent reads everything it needs
---------------------|
```

### Level 1 -- Read (always allowed)

The agent can read without restriction:
- Your configuration files
- Your calendar
- Your emails (read-only)
- Your tasks
- Documents in knowledge/

Why without restriction: an agent that doesn't understand context produces generic responses. Reading is the fuel of relevance.

### Level 2 -- Write (autonomous, within a framework)

The agent can modify WITHOUT asking you:
- MEMORY.md (addition, compression, cleanup)
- Files in knowledge/ (updates)
- Email drafts (but not sending)
- Reports and summaries
- Session notes

Concrete examples:

| The agent CAN | The agent CANNOT |
|---|---|
| Write a draft email response | Send the email |
| Update a knowledge/ file | Delete a knowledge/ file |
| Create a meeting summary | Publish the summary somewhere |
| Add an entry to MEMORY.md | Modify CONSTITUTION.md |
| Modify a code file in dev | Deploy to production |

### Level 3 -- External action (validation required)

The agent MUST ask you before:
- Sending an email or message
- Publishing anything
- Modifying a production database
- Making a payment or transaction
- Contacting a third party
- Deleting data

Validation request format:

```
[VALIDATION REQUIRED]
Action: Send email to dupont@client.fr
Content: [content summary]
Reason: Response to their quote request from 28/03
Impact: The client will receive your pricing proposal

Validate? (yes / no / modify)
```

## Step by step

### 1. List the actions of your typical week

Review your last week. Note each action you'd like to delegate. Classify it in the pyramid.

### 2. Define explicit prohibitions

What is NOT in scope is just as important as what is. Examples:

```
PROHIBITED:
- Making financial commitments
- Responding to HR on my behalf
- Modifying client contracts
- Accessing medical data
- Sharing confidential information out of context
```

### 3. Write the scope in CONSTITUTION.md

The scope translates directly into your CONSTITUTION.md file (see section 3.5).

### 4. Test the scope

Ask the agent:

```
Show me 3 situations where you'd ask me for validation
and 3 situations where you'd act alone.
```

If its examples don't match your intention, adjust the scope.

## Common mistakes

**Scope too broad**: "Do what you think is necessary." The agent will end up doing something you didn't imagine. Guaranteed.

**Scope too narrow**: "Ask me before each action." You end up validating 50 requests a day. Might as well not have an agent.

**Scope too vague**: "Manage my emails, but not the important ones." What is "important"? For the agent, without explicit criteria, it's arbitrary.

**Static scope**: Never revise the scope. Your context evolves. Review the scope each month.

## Verification

- [ ] You have listed the actions of your typical week
- [ ] Each action is classified in one of the 3 levels
- [ ] Explicit prohibitions are written down
- [ ] The scope is documented in CONSTITUTION.md
- [ ] The agent correctly describes its limits when you test it

---
