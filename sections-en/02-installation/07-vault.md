---
---
status: complete
audience: both
chapter: 02
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: en
---

# 2.7 -- HashiCorp Vault

## Context

This is the most important section of the entire chapter. Vault centralizes ALL secrets: API keys, database passwords, Telegram tokens, etc.

**Why Vault and not .env files?**

| Criteria | .env files | Vault |
|----------|-----------|-------|
| Versioning | Risk of accidental commit | Secrets never in git |
| Rotation | Manual, forgotten | Programmable, automated |
| Audit | None | Log of every access |
| Granular access | All or nothing | Fine-grained policies by path |
| Encryption at rest | No | Yes (AES-256-GCM) |
| Multi-service | Copy .env everywhere | Centralized API |

In summary: .env files are technical debt. Vault is an investment.

## Step 1: Create the Docker Compose file

```bash
$ mkdir -p ~/docker/vault/config
$ mkdir -p ~/docker/vault/data
```

Create the file `~/docker/vault/docker-compose.yml`:

```yaml
version: "3.8"

services:
  vault:
    image: hashicorp/vault:1.17
    container_name: vault
    restart: unless-stopped
    ports:
      - "127.0.0.1:8200:8200"
    environment:
      VAULT_ADDR: "http://127.0.0.1:8200"
    cap_add:
      - IPC_LOCK
    volumes:
      - ./config:/vault/config:ro
      - ./data:/vault/data
    command: server -config=/vault/config/vault.hcl
    networks:
      - vault-net

networks:
  vault-net:
    driver: bridge
```

**IMPORTANT**: The port is bound to `127.0.0.1`, not `0.0.0.0`. Vault is only accessible locally (and via Tailscale if configured).

## Step 2: Create the Vault configuration

Create the file `~/docker/vault/config/vault.hcl`:

```hcl
storage "file" {
  path = "/vault/data"
}

listener "tcp" {
  address     = "0.0.0.0:8200"
  tls_disable = 1
}

api_addr = "http://127.0.0.1:8200"

ui = true

disable_mlock = true
```

Notes:
- `tls_disable = 1`: Acceptable because Vault is behind Tailscale (WireGuard encryption). In public production, enable TLS.
- `disable_mlock = true`: Necessary in Docker without additional privileges.
- `ui = true`: Web interface accessible at http://127.0.0.1:8200/ui.

## Step 3: Dev vs production mode

| Mode | Usage | Persistence | Security |
|------|-------|-------------|----------|
| Dev (`vault server -dev`) | Local tests | No (memory) | Root token known |
| Production (what we do here) | VPS | Yes (file/consul) | Secure initialization |

This playbook uses **production mode**. Do not use dev mode on a VPS.

## Step 4: Start Vault

```bash
$ cd ~/docker/vault
$ docker compose up -d
```

Fix the permissions on the data volume (the Vault container runs as the `vault` user, not `root`):

```bash
$ docker exec vault chown -R vault:vault /vault/data
```

> **Why?** Without this command, Vault can crash on startup with a permissions error on `/vault/data`. The volume mounted from the host belongs to root by default, but the Vault process inside the container runs as the `vault` user.

Verify that the container is running:

```bash
$ docker ps | grep vault
```

## Step 5: Initialize Vault

> **WARNING -- VAULT_ADDR and TLS:** Vault CLI uses HTTPS by default. If TLS is disabled (as in this configuration with `tls_disable = 1`), you must always pass `VAULT_ADDR=http://...` in each `docker exec vault` command. Without this, you will get errors like "http: server gave HTTP response to HTTPS client". All commands below already include `-e VAULT_ADDR=http://127.0.0.1:8200` for this reason.

Initialization happens only ONCE. It generates the decryption keys (unseal keys) and the root token.

```bash
$ docker exec -e VAULT_ADDR=http://127.0.0.1:8200 vault vault operator init -key-shares=5 -key-threshold=3
```

Result: 5 unseal keys and 1 root token. Example output:

```
Unseal Key 1: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
Unseal Key 2: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
Unseal Key 3: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
Unseal Key 4: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
Unseal Key 5: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Initial Root Token: hvs.XXXXXXXXXXXXXXXXXXXXXXXX
```

**SAVE THIS INFORMATION IMMEDIATELY.**

## Step 6: Back up the unseal keys OUTSIDE the VPS

The unseal keys must be stored **outside the VPS**. If someone compromises the VPS and has the unseal keys, they can decrypt all secrets.

Recommended method:
1. Copy each key into a password manager (1Password, Bitwarden, KeePass)
2. Distribute the keys: 2 for you, 2 for a co-admin, 1 in a physical safe
3. The threshold is 3: you need 3 keys out of 5 to decrypt. No single person can open everything alone.

**DO NOT STORE the unseal keys in a file on the VPS.**

## Step 7: Unseal Vault

After each restart, Vault starts in "sealed" (encrypted) state. You need 3 keys to open it:

```bash
$ docker exec -e VAULT_ADDR=http://127.0.0.1:8200 vault vault operator unseal KEY_1_HERE
$ docker exec -e VAULT_ADDR=http://127.0.0.1:8200 vault vault operator unseal KEY_2_HERE
$ docker exec -e VAULT_ADDR=http://127.0.0.1:8200 vault vault operator unseal KEY_3_HERE
```

Check the status:

```bash
$ docker exec -e VAULT_ADDR=http://127.0.0.1:8200 vault vault status
```

Expected result: `Sealed: false`

## Step 8: Log in with the root token

```bash
$ docker exec -e VAULT_ADDR=http://127.0.0.1:8200 vault vault login ROOT_TOKEN_HERE
```

Or via environment variable (more convenient for scripts):

```bash
$ export VAULT_TOKEN='ROOT_TOKEN_HERE'
```

## Step 9: Enable the KV v2 secrets engine

KV (Key-Value) v2 enables secret versioning:

```bash
$ docker exec -e VAULT_ADDR=http://127.0.0.1:8200 vault vault secrets enable -path=secret kv-v2
```

Verify:

```bash
$ docker exec -e VAULT_ADDR=http://127.0.0.1:8200 vault vault secrets list
```

You should see `secret/` in the list.

## Step 10: Store the first secrets

Store your secrets by category. Each command creates or updates a secret:

**OpenRouter API key:**

```bash
$ docker exec -e VAULT_ADDR=http://127.0.0.1:8200 vault vault kv put secret/openrouter api_key="sk-or-YOUR_KEY_HERE"
```

**Telegram token:**

```bash
$ docker exec -e VAULT_ADDR=http://127.0.0.1:8200 vault vault kv put secret/telegram bot_token="123456:ABC-DEF..." chat_id="YOUR_CHAT_ID"
```

**GitHub token:**

```bash
$ docker exec -e VAULT_ADDR=http://127.0.0.1:8200 vault vault kv put secret/github token="ghp_YOUR_TOKEN_HERE"
```

**Database credentials:**

```bash
$ docker exec -e VAULT_ADDR=http://127.0.0.1:8200 vault vault kv put secret/database \
  host="127.0.0.1" \
  port="5432" \
  name="oa_system" \
  user="oa_admin" \
  password="STRONG_PASSWORD_HERE"
```

**Cockpit secret:**

```bash
$ docker exec -e VAULT_ADDR=http://127.0.0.1:8200 vault vault kv put secret/cockpit \
  jwt_secret="GENERATE_WITH_openssl_rand_hex_32" \
  admin_password="ADMIN_PASSWORD"
```

## Step 11: Read a secret (verification)

```bash
$ docker exec -e VAULT_ADDR=http://127.0.0.1:8200 vault vault kv get secret/openrouter
```

Expected result: the `api_key` field with the stored value.

## Step 12: Create an application token (not the root token)

DO NOT use the root token in your applications. Create a dedicated token:

```bash
$ docker exec -e VAULT_ADDR=http://127.0.0.1:8200 vault vault token create \
  -display-name="openclaw-app" \
  -ttl=720h \
  -renewable=true \
  -policy=default
```

Note the generated token. This is the one you will use in the OpenClaw configuration.

## Step 13: Unseal after restart

After each VPS restart, Vault starts in sealed mode. You must unseal it manually:

```bash
$ docker exec -e VAULT_ADDR=http://127.0.0.1:8200 vault vault operator unseal
# Enter key 1 when prompted
$ docker exec -e VAULT_ADDR=http://127.0.0.1:8200 vault vault operator unseal
# Enter key 2
$ docker exec -e VAULT_ADDR=http://127.0.0.1:8200 vault vault operator unseal
# Enter key 3
```

> **SECURITY: Never store the unseal keys in a file on the server.** No `vault-unseal.sh` script with keys in plain text. The unseal keys must be kept outside the VPS (password manager, physical safe, or cloud KMS). An AI agent that has access to the unseal keys can compromise the entire system.

For production environments, consider Vault auto-unseal with a cloud KMS (AWS KMS, GCP Cloud KMS). It's more complex to set up but eliminates the need for manual unsealing.

**IMPORTANT**: This script contains unseal keys in plain text. It's a compromise between security and practicality. In a critical environment, prefer manual unsealing or Vault auto-unseal with a cloud KMS.

## Common errors

- **"server is not yet initialized"**: You didn't do step 5 (init). Initialization happens only once.
- **"Vault is sealed"**: After a container or VPS restart, Vault is always sealed. You must unseal it with 3 keys.
- **Losing the unseal keys**: If you lose 3+ keys, your secrets are unrecoverable. Back them up.
- **Using the root token in production**: The root token is all-powerful. Create dedicated tokens with restricted policies.
- **Vault crashing on startup**: Check permissions on `~/docker/vault/data/`. The folder must belong to your user.

## Verification

```bash
$ docker exec -e VAULT_ADDR=http://127.0.0.1:8200 vault vault status
$ docker exec -e VAULT_ADDR=http://127.0.0.1:8200 vault vault kv list secret/
$ docker exec -e VAULT_ADDR=http://127.0.0.1:8200 vault vault kv get secret/openrouter
```

Expected results:
- Status: Sealed = false, Initialized = true
- Secret list: openrouter, telegram, github, database, cockpit
- Reading a secret: value displayed correctly

## Estimated time

30 minutes (plus time to generate and back up the secrets).
