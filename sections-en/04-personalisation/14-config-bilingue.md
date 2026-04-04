---
status: complete
audience: both
chapter: 04
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: en
---

# 4.14 -- Bilingual Configuration

## Context

If you work in French and English -- French-speaking clients, English documentation, English code, French communications -- your agent needs to know when to use which language. Without clear instructions, it will switch unpredictably.

## The Three Modes

### Mode 1: French only

```
Language: French. Always.
Technical terms in English when there's no common equivalent 
(deploy, commit, merge, container, endpoint).
Command and code names in English (it's code, not translation).
```

When to use it: personal use, French-speaking team, no English-speaking clients.

### Mode 2: English only

```
Language: English. Always.
```

When to use it: international team, open source documentation, English-speaking clients.

### Mode 3: Contextual bilingual

```
Default language: French.
Switch to English when:
- I'm writing technical documentation (README, API docs)
- I'm preparing a message for an English-speaking client
- I tell you "in English"
Return to French automatically at the next conversation.
```

When to use it: mixed context, international freelance, open source project with local team.

## Switching Rules

The switch must be predictable. Define the triggers:

| Trigger | Language |
|---|---|
| Direct conversation | French |
| Write a commit message | English |
| Write code documentation | English |
| Write a French client email | French |
| Write an English client email | English |
| Comment code | English |
| Explain a concept | French |
| Name variables/functions | English |

### Switching Prompt

```
To switch language:
- "En anglais" or "in English" -> switch to English for this task
- "En francais" -> return to French
- When I write in English, respond in English
- When I write in French, respond in French
- Default: French
```

## Recommended Models by Language

All major models (Claude, GPT-4, Gemini) handle French and English well. A few nuances:

### French

- **Claude**: excellent in French. Understands nuances, formal/informal speech, register.
- **GPT-4**: good in French, sometimes slightly Anglicized phrasing.
- **Open source models (Mistral, LLaMA)**: Mistral, being French, is strong in French. LLaMA is variable.

### English

All models are excellent in English. No significant difference for professional use.

### Bilingual

The key factor: consistency of switching. Claude and GPT-4 handle bilingual context well if the rules are clear in the system prompt. Smaller models tend to mix.

## Bilingual Pitfalls

### Unintentional Mixing

The agent starts in French, adds an English term, then continues in English. Or vice versa. Solution: explicit rule in the system prompt.

```
If you switch language mid-response, signal it.
One response = one language (except technical terms).
```

### Unsolicited Translation

You write in French, the agent translates to English "to be more precise". Solution:

```
Never translate my request. Respond in the language I use.
```

### Forced Technical Terms

The agent translates "container" to "conteneur", "deploy" to "déployer" (instead of "deploy", which is acceptable in technical French). Solution:

```
Technical terms kept in English: deploy, commit, merge, push, pull, 
container, endpoint, token, API, CLI, pipeline, build, runtime.
```

## Common Mistakes

**No language rule.** The agent chooses based on the model's mood. Inconsistent.

**Force 100% technical French.** "Use 'conteneur' instead of 'container'." Nobody talks like that. Keep the terms your team uses daily.

**Switch without context.** You say "in English" but forget to return to French. The agent continues in English for the next 10 requests.

## Steps

1. Decide your mode (1, 2, or 3).
2. List technical terms to keep in English.
3. Define switching triggers.
4. Add rules to the system prompt.
5. Test with 5 requests in each language.

## Verification

- [ ] The language mode is defined in the system prompt.
- [ ] Technical terms to keep in English are listed.
- [ ] Switching triggers are explicit.
- [ ] The agent respects the expected language (tested in both languages).
- [ ] No unintentional mixing in responses.
