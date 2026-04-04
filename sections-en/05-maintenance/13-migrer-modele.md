---
---
status: complete
audience: both
chapter: 05
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: en
---

# 5.13 -- Migrating to Another Model

## Context

The LLM world moves fast. A new model launches, prices change, performance evolves. You might want to migrate from Claude to GPT (or vice versa), or test an open source model. The risk: breaking what already works.

## When to Migrate

Good reasons:

- **Cost.** The new model is significantly cheaper for equivalent performance.
- **Performance.** Better response quality for your specific use case.
- **Features.** The new model supports something you need (vision, more context, specific tools).
- **Availability.** Your current model has reliability issues or rate limiting problems.

Bad reasons:

- "It's new, it must be better." Not always.
- "Everyone's migrating." Your use case is unique.
- "The benchmark says it's better." Benchmarks don't measure your specific usage.

## How to Test Without Breaking Things

### Phase 1: parallel testing

Keep your current model in production. Test the new one on the side.

```
Weeks 1-2: send the same requests to both models.
Compare:
- Response quality
- System prompt adherence
- Tone and format
- Response time
- Cost
```

### Comparison Grid

Create a file `model-comparison.md`:

```markdown
# Comparison: [Model A] vs [Model B]

Date: YYYY-MM-DD
Requests tested: 20

| Criterion | Model A | Model B | Winner |
|---|---|---|---|
| System prompt adherence | 9/10 | 7/10 | A |
| Technical quality | 8/10 | 9/10 | B |
| Tone adherence | 9/10 | 6/10 | A |
| French language quality | 9/10 | 8/10 | A |
| Average response time | 2.1s | 1.8s | B |
| Average cost/request | $0.015 | $0.008 | B |
| Hallucinations | 1/20 | 3/20 | A |
| Boundary prompt adherence | 10/10 | 8/10 | A |

Verdict: [decision]
Reason: [justification]
```

### Phase 2: progressive migration

If the new model is better, migrate progressively:

1. **Week 1**: use the new model for low-risk tasks (questions, research, writing).
2. **Week 2**: use it for operational tasks (but with validation).
3. **Week 3**: use it as the primary model.
4. **Week 4**: evaluate. Keep or roll back.

### Phase 3: deactivate the old one

Only deactivate the old model after 1 month of satisfactory performance from the new one. Keep the old configuration as a backup.

## Adapt the System Prompt

Each model interprets the system prompt differently. What works with Claude may not work with GPT-4.

### Points of Attention

| Aspect | Claude | GPT-4 | Open Source Models |
|---|---|---|---|
| Prompt length | Tolerates long prompts | Prefers structured prompts | Short = better |
| French tone | Natural | Sometimes anglicized | Variable |
| Boundaries | Good adherence | Good adherence | Less reliable |
| XML format in prompt | Excellent | Average | Weak |
| Bullet points vs prose | Both work | Prefers bullets | Bullets |

### Adapt Without Rewriting

1. Copy your current system prompt.
2. Test 5 requests.
3. Note differences in behavior.
4. Adjust the parts that don't work.
5. Don't rewrite everything -- adjust surgically.

## Keep a Fallback

Always have a plan B.

```bash
# Configuration with fallback
PRIMARY_MODEL="claude-sonnet-4-20250514"
FALLBACK_MODEL="claude-3-5-sonnet-20241022"

# If primary model fails, switch over
if ! call_model "$PRIMARY_MODEL" "$PROMPT"; then
    echo "Falling back to $FALLBACK_MODEL"
    call_model "$FALLBACK_MODEL" "$PROMPT"
fi
```

### What to Back Up

- System prompt of the old model (versioned).
- Connection configuration (API key, endpoint).
- Notes on model-specific adjustments.

## Common Mistakes

**Migrating in one day.** Monday Claude, Tuesday GPT-4. You don't know if issues come from the model or the transition. Migrate progressively.

**Not adapting the prompt.** The same prompt verbatim on two models will give different results. Test and adjust.

**Throwing out the old one.** You delete the old model's config. The new one has an issue on the weekend. No fallback.

**Trusting benchmarks.** "GPT-4 has a better MMLU score." Generic benchmarks don't predict performance on your specific use case. Only your A/B test matters.

## Steps

1. Identify why you want to migrate (concrete reason).
2. Test the new model in parallel for 2 weeks.
3. Fill in the comparison grid with 20 real requests.
4. If the new one wins, migrate progressively (3 weeks).
5. Keep fallback active for 1 month.
6. Document model-specific prompt adjustments.

## Checklist

- [ ] The migration reason is concrete (not just "it's new").
- [ ] An A/B test was done with at least 20 requests.
- [ ] The comparison grid is filled in.
- [ ] The system prompt has been adapted to the new model.
- [ ] A fallback is configured and functional.
- [ ] The old configuration is backed up.
