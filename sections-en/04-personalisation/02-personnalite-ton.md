---
---
status: complete
audience: both
chapter: 04
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: en
---

# 4.2 -- Personality and Tone

## Context

Your agent's tone is not a cosmetic detail. It's what makes the difference between a tool you enjoy using and one you tolerate. An agent that's too verbose, you stop reading. Too dry, you lack context. Too formal, it sounds off.

The goal: the agent's response should sound like what a competent colleague would tell you.

## Personality Axes

### Direct vs Diplomatic

**Direct**: "This script has a bug on line 12. The fix: [code]."
**Diplomatic**: "I noticed a point of attention on line 12 that could potentially cause an issue..."

For daily technical use, direct wins. Always.

### Humorous vs Professional

Humor in a technical agent is a trap. It works the first time, it gets tiring by the hundredth. If you want it, measure it: a light remark when things go well, zero humor when things break.

### Short vs Detailed

The golden rule: short by default, detailed on demand.

Bad: `"detailed communication"`
Good: `"3 sentences max unless I ask for more"`
Even better: `"1 line for the answer, code block if necessary, explanation only if I say 'explain'"`

### Informal vs Formal

Your agent, your choice. But be explicit:

```
Use informal language with me. No "you", no politeness formulas.
```

or

```
Formal tone. Professional but not distant.
```

If you don't specify, the agent will alternate and it sounds inconsistent.

## Write in Actionable Terms

The problem with vague instructions is that the model interprets them its own way. And each model interprets them differently.

| Vague (useless) | Actionable (effective) |
|---|---|
| "Be concise" | "3 sentences max unless explicitly asked otherwise" |
| "Direct communication" | "No politeness formulas. Start with the answer." |
| "Professional tone" | "No emojis. No exclamation marks. Standard English." |
| "Be helpful" | (write nothing -- it's the default behavior) |
| "Adapt to my style" | "Short sentences. Bullet points for lists. Inline code for commands." |

## Concrete Configuration Examples

### Tech / DevOps Profile

```
Tone: direct, technical. No politeness formulas.
Short response by default (1-3 sentences + code if applicable).
If I ask a yes/no question, answer yes or no first, then justify.
Use informal language with me.
No emojis.
```

### Consultant / Client-Facing Profile

```
Formal tone. Professional but accessible.
When I'm preparing a client email, suggest a diplomatic version.
For internal work, direct and short response.
```

### Creative Profile

```
Use informal language with me. Relaxed tone.
Suggest alternatives when I ask for your opinion.
If an idea is bad, say it frankly with a better suggestion.
```

## Common Mistakes

**Stacking adjectives.** "Be professional, warm, concise, detailed when needed, humorous but not too much." The model doesn't know how to prioritize. Choose 2-3 traits, not 7.

**Copying someone else's tone.** Someone else's prompt won't sound right for you. Start from your own conversations: how do you talk to a trusted colleague? That's your tone.

**Forgetting format.** Tone isn't just words. It's also: bullet points vs prose, code blocks vs inline, headers vs continuous text. Specify the format as much as the vocabulary.

## Steps

1. Review your last 10 conversations with your agent.
2. Note each time the tone bothered you (too long, too formal, too vague).
3. Write 3-5 actionable instructions that fix these issues.
4. Add them to your system prompt, Tone section.
5. Test on 5 requests. Adjust.

## Verification

- [ ] Tone is defined in actionable instructions, not adjectives.
- [ ] The choice of formal/informal language is explicit.
- [ ] The default length of responses is specified.
- [ ] The format (bullets, prose, code) is precise.
- [ ] Tested on 5 requests -- the tone is consistent.
