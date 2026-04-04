---
---
status: complete
audience: both
chapter: 02
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: en
---

# 2.13 -- OpenRouter Connection

## Context

OpenRouter is an API gateway that provides access to multiple AI models (Claude, Gemini, Mistral, Llama, etc.) via a single API key and unified format. Main advantage: if one model becomes unavailable, you switch to another without changing your code.

## Step 1: Get the API Key

1. Log in to [openrouter.ai](https://openrouter.ai)
2. Go to Settings > API Keys
3. Create a new key
4. Copy the key (format: `sk-or-v1-...`)

## Step 2: Store the Key in Vault

If not already done (section 07):

```bash
$ docker exec vault vault kv put secret/openrouter api_key="sk-or-v1-YOUR_KEY_HERE"
```

Verify:

```bash
$ docker exec vault vault kv get -field=api_key secret/openrouter
```

## Step 3: Test an API Call

Quick test with curl to verify that the key works:

```bash
$ API_KEY=$(docker exec vault vault kv get -field=api_key secret/openrouter)

$ curl -s https://openrouter.ai/api/v1/chat/completions \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "anthropic/claude-haiku-3.5",
    "messages": [{"role": "user", "content": "Reply just OK"}]
  }' | python3 -m json.tool
```

Expected result: a JSON response containing "OK" (or equivalent) in `choices[0].message.content`.

## Step 4: Check Credit

```bash
$ curl -s https://openrouter.ai/api/v1/auth/key \
  -H "Authorization: Bearer $API_KEY" | python3 -m json.tool
```

This endpoint returns your balance and limits.

## Available Models Comparison

| Model | Use Case | Speed | Code Quality | Relative Cost |
|-------|----------|-------|-------------|---------------|
| `anthropic/claude-sonnet-4-20250514` | Complex tasks, reasoning, code | Medium | Excellent | $$$ |
| `anthropic/claude-haiku-3.5` | Quick tasks, classification, sorting | Fast | Good | $ |
| `mistral/mistral-large-latest` | French text, analysis | Medium | Good | $$ |
| `google/gemini-2.0-flash-001` | Volume, large context window | Very fast | Correct | $ |
| `meta-llama/llama-3.3-70b-instruct` | Open source, no filter | Medium | Correct | $ |

### Recommended Strategy

- **Default model**: Claude Sonnet 4 for precision
- **Fallback model**: Claude Haiku 3.5 for speed and cost
- **Experimentation model**: Gemini Flash for large volumes

## Configuration in OpenClaw

The connection is configured in `~/.openclaw/config.json` (section 12). The `model.provider` field must be `"openrouter"` and the key is automatically read from Vault.

## Budget Alerts

OpenRouter allows you to set spending limits in the dashboard. Configure:
- Alert at 10 EUR/month
- Hard limit at 30 EUR/month

This prevents surprises if an agent loops.

## Common Errors

- **"Invalid API key"**: The key is miscopied or expired. Regenerate it on openrouter.ai.
- **"Insufficient credits"**: Recharge your account on openrouter.ai.
- **"Model not found"**: The model name has changed. Check the exact name on openrouter.ai/models.
- **Timeout on calls**: Some models are slow under load. The fallback (Haiku) takes over automatically if configured.

## Verification

```bash
$ docker exec vault vault kv get -field=api_key secret/openrouter
$ curl -s https://openrouter.ai/api/v1/auth/key \
  -H "Authorization: Bearer $(docker exec vault vault kv get -field=api_key secret/openrouter)" \
  | python3 -m json.tool
```

Expected results:
- The key is readable from Vault
- The API returns account info (balance, limits)

## Estimated Time

10 minutes.
