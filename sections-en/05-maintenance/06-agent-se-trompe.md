---
---
status: complete
audience: both
chapter: 05
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: en
---

# 5.6 -- When the agent makes a mistake

## Context

Your agent will make mistakes. Not "maybe" -- will. LLMs hallucinate, over-interpret, apply the wrong context. This isn't a flaw, it's a property. The question isn't "how to prevent all errors" but "how to detect, correct, and prevent them."

## Types of errors

### Factual hallucination

The agent asserts something false with confidence.

```
Agent: "Your SSL certificate expires on May 15."
Reality: it expires on June 15.
```

### Over-interpretation

The agent interprets more than what you said.

```
You: "The deploy crashed."
Agent: "I identified the problem: the database ran out of memory,
        which caused an OOM kill of the container, probably linked to a memory
        leak in the latest commit."
Reality: it was a typo in the docker-compose.yml.
```

### Wrong context

The agent applies information from one context to another.

```
You're working on project A.
The agent applies the rules from project B.
```

### Incorrect execution

The agent does the right thing but wrong.

```
You: "Backup the database."
Agent: pg_dump without compression, in the wrong folder.
```

## Correction protocol

### 1. Diagnosis

Identify the type of error. Use this prompt:

```
You just made a mistake. Before correcting it, answer:
1. What was the exact error?
2. What type: hallucination, over-interpretation, wrong context, incorrect execution?
3. Why did the error happen (in your view)?
```

### 2. Correction

Fix the damage first, analyze later.

- If the agent modified a file: `git diff` to see what changed, `git checkout` if necessary.
- If the agent executed a command: check the impact (`docker ps`, `psql`, logs).
- If the agent gave wrong information: correct the fact in memory.

### 3. Prevention

After correcting, prevent it from happening again:

- **Hallucination**: add to the prompt -- "If you're not sure about a fact, say so. Don't make things up."
- **Over-interpretation**: use the Steinberg prompt (see below).
- **Wrong context**: clarify which project/context is active.
- **Incorrect execution**: update the workflow in WORKFLOWS.md.

## Steinberg's correction prompt

When the agent over-interprets, use this refocusing:

```
You're over-interpreting. Reframe your response with this format:
1. Signal: what did you observe factually?
2. Uncertainty: what do you NOT know?
3. Question for me: what would you need to know to conclude?
```

Example:

**Before (over-interpretation):**
```
"The deploy crashed because of an OOM kill linked to a memory leak
in the latest commit. I recommend profiling the code and
increasing the container memory."
```

**After (refocused):**
```
Signal: the cockpit container went from "Up" to "Exited" at 14:32.
Uncertainty: I don't know the cause. It could be OOM, config error,
or runtime issue.
Question: can you show me `docker logs cockpit --tail 50` and
`dmesg | tail -20` so I can diagnose?
```

The difference: refocusing separates what the agent knows from what it assumes. It prevents false leads.

## When the error is serious

If the agent caused damage (deleted data, broken service, sent information by mistake):

1. **Stop the agent.** Don't ask it to fix itself alone.
2. **Assess the damage.** Manually.
3. **Restore if possible.** Backups, git, snapshots.
4. **Document the incident.** What, when, why, how to prevent.
5. **Add to the boundary prompt.** The action that caused the problem joins the list of prohibitions.

## Common mistakes

**Blame the agent.** The error often comes from your instructions, not the model. Vague prompt = vague response. No boundary = no limits.

**Ignore the error.** "It's not serious, it basically understood." Small repeated errors become big errors.

**Correct without preventing.** You correct course but don't add a rule. The same error returns next week.

**Over-correct.** After an error, you add 10 restrictive rules. The agent becomes unusable. One targeted rule is enough.

## Steps

1. When the agent makes a mistake, identify the type of error.
2. Fix the damage (files, DB, services).
3. Use the refocusing prompt if it's over-interpretation.
4. Add a prevention rule (prompt, boundary, workflow).
5. Document the incident if it's a serious error.

## Checklist

- [ ] You can identify the type of error (hallucination, over-interpretation, etc.).
- [ ] Steinberg's refocusing prompt is in your notes/prompt.
- [ ] Serious errors are documented with prevention measures.
- [ ] The boundary prompt is updated after each incident.
- [ ] The agent has the rule "If you're not sure, say so" in its system prompt.
