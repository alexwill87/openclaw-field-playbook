---
status: complete
audience: both
chapter: 04
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: en
---

# 4.3 -- Iteration: your first version won't be the right one

## Context

Your first system prompt will be bad. Not because you're bad — because nobody knows what they want from an agent until they've used it. That's normal. The prompt reveals itself through use, not through thinking about it.

Plan for 2-3 rounds of iteration before you have a prompt that feels right. After that, occasional tweaks when your needs change.

## The iteration process

### Round 1: the rough version

Write your first prompt (see section 4.1). Use it for 2-3 days. Note every friction point:

- "It responds too long"
- "It forgets I want informal speech"
- "It suggests Windows solutions when I'm on Linux"
- "It asks for context every time"

### Round 2: the correction prompt

Use this pattern to fix it:

```
Here's my current system prompt:
[paste the prompt]

Problems observed:
1. [friction 1]
2. [friction 2]
3. [friction 3]

Rewrite the prompt fixing these issues.
Keep the structure. Don't exceed 250 words.
```

Review the suggestion. Manually edit whatever doesn't fit. Test for 2-3 more days.

### Round 3: condense

After round 2, your prompt probably runs 400-500 words. That's too much. Every token counts.

Condensation prompt:

```
Here's my system prompt (480 words).
Condense it to 150 words maximum.
Keep ALL the rules and restrictions.
Remove explanations -- the agent doesn't need to understand why.
```

The rule: 150 words > 500 words. A short, precise prompt beats a long, detailed one. The model doesn't need your justifications — it needs your instructions.

## Why condensing works

A long prompt creates noise. The model has to sort what matters from what's filler. The shorter it is, the more weight each word carries.

Comparison:

**Before (68 words):**
```
When you suggest technical solutions to me, I'd like you to take into
account the fact that I work primarily on Linux Ubuntu environments, and
that I generally don't need solutions specific to Windows or macOS, unless
you're explicitly asked for them in my question.
```

**After (12 words):**
```
Environment: Linux Ubuntu. No Windows/macOS solutions unless requested.
```

Same information. 5x fewer tokens.

## When to stop iterating

Stop when:

- You're no longer correcting the agent on tone or format.
- Responses are useful on the first try in 80%+ of cases.
- Your corrections are about substance (knowledge) not form (behavior).

If you're still iterating after 5 rounds, the problem probably isn't the prompt. It might be the model, the tool, or your expectations.

## Common mistakes

**Never iterate.** The first draft stays in place for months. The prompt accumulates obsolete instructions and the agent gradually degrades.

**Iterate without noting.** You change the prompt "from memory" without having written down the friction points. You fix one problem and create another.

**Add without removing.** Every iteration adds rules but never removes any. After 5 rounds, the prompt is 800 words and contradicts itself.

## Steps

1. Use your current prompt for 2-3 days.
2. Note every friction point in a file `prompt-feedback.md`.
3. Apply the correction prompt (round 2).
4. Test for 2-3 days.
5. Condense to 150 words (round 3).
6. Test. If it holds, you're done.

## Checklist

- [ ] The current prompt has been tested in real conditions (not just reread).
- [ ] Friction points are written down, not from memory.
- [ ] The final prompt is under 200 words.
- [ ] No instruction contradicts another.
- [ ] 80%+ of responses are useful without correction.
