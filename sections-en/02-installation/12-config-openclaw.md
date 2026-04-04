---
---
status: complete
audience: both
chapter: 02
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: en
---

# 2.12 -- OpenClaw Initial Configuration

## Context

The file `~/.openclaw/config.json` is the control center of OpenClaw. Each field affects system behavior. This section details a complete and annotated configuration file.

## Complete configuration file

Create or edit `~/.openclaw/config.json` :

```json
{
  // --- Identification ---
  "instance_name": "oa-paris",
  "environment": "production",

  // --- IA Model ---
  "model": {
    "provider": "openrouter",
    "default_model": "anthropic/claude-sonnet-4",
    "fallback_model": "anthropic/claude-haiku-4-5",
    "temperature": 0.3,
    "max_tokens": 8192
  },

  // --- Vault Connection ---
  "vault": {
    "enabled": true,
    "address": "http://127.0.0.1:8200",
    "token_env": "VAULT_TOKEN",
    "secret_prefix": "secret"
  },

  // --- Database ---
  "database": {
    "type": "postgresql",
    "vault_path": "secret/database",
    "pool_size": 10,
    "ssl": false
  },

  // --- Gateway ---
  "gateway": {
    "host": "127.0.0.1",
    "port": 3000,
    "cors_origins": []
  },

  // --- Notifications ---
  "notifications": {
    "telegram": {
      "enabled": true,
      "vault_path": "secret/telegram"
    }
  },

  // --- Logging ---
  "logging": {
    "level": "info",
    "file": "~/.openclaw/logs/openclaw.log",
    "max_size_mb": 50,
    "max_files": 5
  },

  // --- Workspace ---
  "workspace": {
    "path": "~/.openclaw/workspace",
    "auto_save_memory": true,
    "session_retention_days": 30
  },

  // --- Security ---
  "security": {
    "allowed_commands": ["git", "npm", "node", "docker", "docker compose"],
    "blocked_paths": ["/etc/shadow", "/root"],
    "require_confirmation_for": ["rm", "drop", "delete", "truncate"]
  }
}
```

> **OpenRouter model names change regularly.** Before configuring, verify the current names at [openrouter.ai/models](https://openrouter.ai/models). The names above were valid in April 2026.

**Note** : JSON does not support comments. Remove the `//` lines in the final file, or use a JSON5 preprocessor. The comments above are for documentation only.

## Field-by-field explanation

### instance_name

Unique identifier for this instance. Useful if you have multiple VPS. Appears in logs and notifications.

### model

| Field | Description |
|-------|-------------|
| `provider` | Service for accessing models. `openrouter` allows you to change models without changing providers. |
| `default_model` | Model used by default. Claude Sonnet 4 offers the best quality-to-price ratio. |
| `fallback_model` | Fallback model if the primary one is unavailable or too slow. Haiku is fast and inexpensive. |
| `temperature` | 0 = deterministic, 1 = creative. 0.3 is a good balance for code. |
| `max_tokens` | Maximum length of the response. 8192 is sufficient for most tasks. |

### vault

| Field | Description |
|-------|-------------|
| `enabled` | Enables secret retrieval from Vault. |
| `address` | Local URL of Vault. Do not change unless Vault is on another machine. |
| `token_env` | Environment variable containing the Vault token. Defined in the systemd file (section 15). |
| `secret_prefix` | Prefix of the KV path. `secret` corresponds to `vault kv get secret/...`. |

### database

| Field | Description |
|-------|-------------|
| `vault_path` | Vault path where PostgreSQL credentials are stored. |
| `pool_size` | Number of simultaneous connections. 10 is sufficient for moderate use. |
| `ssl` | Disabled because the connection is local (same machine, via 127.0.0.1). |

### security

| Field | Description |
|-------|-------------|
| `allowed_commands` | System commands the agent can execute. Add as needed. |
| `blocked_paths` | Paths the agent cannot read or write. |
| `require_confirmation_for` | Commands that require manual confirmation before execution. |

## Connecting to Vault

For the configuration to work, the Vault token must be available as an environment variable :

```bash
$ export VAULT_TOKEN="your-application-token"
```

To make this permanent, add to `~/.bashrc` :

```bash
export VAULT_TOKEN="your-application-token"
```

Or better : use the systemd file (section 15) to inject the variable.

## Model selection

| Model | Strengths | Weaknesses | Approx. cost |
|--------|--------|------------|--------------|
| Claude Sonnet 4 | Best reasoning, quality code | Slower, more expensive | ~3$/M input tokens |
| Claude Haiku 3.5 | Fast, inexpensive | Less accurate on complex tasks | ~0.25$/M tokens |
| Mistral Large | Good for French | Less capable at code | ~2$/M tokens |
| Gemini 2.0 Flash | Very fast, large window | Variable quality | ~0.10$/M tokens |

Recommendation : Claude Sonnet as default, Haiku as fallback.

## Registering models in `agents.defaults.models`

In addition to configuring the primary model, OpenClaw needs models to be registered in the `agents.defaults.models` section so agents can use them. Add this section to `~/.openclaw/config.json` :

```json
"agents": {
  "defaults": {
    "models": [
      {
        "id": "anthropic/claude-sonnet-4",
        "provider": "openrouter",
        "role": "primary"
      },
      {
        "id": "anthropic/claude-haiku-4-5",
        "provider": "openrouter",
        "role": "fallback"
      }
    ]
  }
}
```

Or via the CLI :

```bash
$ openclaw config set agents.defaults.models --strict-json '[{"id":"anthropic/claude-sonnet-4","provider":"openrouter","role":"primary"},{"id":"anthropic/claude-haiku-4-5","provider":"openrouter","role":"fallback"}]'
```

> **Without this step**, OpenClaw agents will not know which model to use and will fail with a "no model configured for agent" error.

## Syntax for `openclaw config set`

If you prefer to configure via the CLI rather than editing JSON manually, here is the syntax for `openclaw config set` :

**Strings** (quotes required for values containing spaces or special characters) :

```bash
$ openclaw config set instance_name "oa-paris"
$ openclaw config set model.default_model "anthropic/claude-sonnet-4"
```

**Booleans** :

```bash
$ openclaw config set vault.enabled true
$ openclaw config set database.ssl false
```

**Numbers** :

```bash
$ openclaw config set model.temperature 0.3
$ openclaw config set model.max_tokens 8192
```

**JSON objects** (use `--strict-json` to pass a complete object) :

```bash
$ openclaw config set model --strict-json '{"provider":"openrouter","default_model":"anthropic/claude-sonnet-4","fallback_model":"anthropic/claude-haiku-4-5","temperature":0.3,"max_tokens":8192}'
```

**List current configuration** :

```bash
$ openclaw config get
$ openclaw config get model.default_model
```

> **Common pitfall :** If you forget quotes around a string containing `/` (like `anthropic/claude-sonnet-4`), the shell may interpret it differently. Always wrap values in quotes.

## Common errors

- **Invalid JSON** : Remove the `//` comments from the file. Validate with `jq . ~/.openclaw/config.json`.
- **Missing Vault token** : The error appears when OpenClaw starts. Check `echo $VAULT_TOKEN`.
- **Model not found** : Verify the exact model name at openrouter.ai/models.
- **Pool size too large** : PostgreSQL has a limited number of connections (100 by default). 10 is reasonable.

## Verification

```bash
$ cat ~/.openclaw/config.json | python3 -m json.tool
$ openclaw doctor
```

Expected results :
- Valid JSON (no parsing errors)
- Doctor : valid configuration

## Estimated time

15 minutes.
