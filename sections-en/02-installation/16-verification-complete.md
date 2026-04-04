---
---
status: complete
audience: both
chapter: 02
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: en
---

# 2.16 -- Post-installation verification

## Context

All the building blocks are in place. Before moving to the next chapter, verify EVERYTHING at once. If any item is red, the symptom-based diagnosis will tell you what to do.

## Checklist of 11 points

Execute each command. Everything must succeed.

### 1. Docker is working

```bash
$ docker ps
```

Expected: at least 2 containers (vault, postgres) in "Up" state.

### 2. Vault is unsealed and accessible

```bash
$ docker exec vault vault status | grep Sealed
```

Expected: `Sealed          false`

### 3. Secrets are readable

```bash
$ docker exec vault vault kv get secret/openrouter
$ docker exec vault vault kv get secret/telegram
$ docker exec vault vault kv get secret/database
```

Expected: each command returns the stored fields.

### 4. PostgreSQL responds

```bash
$ docker exec postgres psql -U oa_admin -d oa_system -c "SELECT 'pg_ok';"
```

Expected: `pg_ok`

### 5. Tailscale is connected

```bash
$ tailscale status
```

Expected: your machine appears as connected.

### 6. Node.js is the correct version

```bash
$ node --version
```

Expected: v22.x or higher.

### 7. OpenClaw is installed

```bash
$ openclaw --version
```

Expected: version number displayed.

### 8. The gateway is running

```bash
$ sudo systemctl status openclaw-gateway | grep Active
```

Expected: `active (running)`

### 9. The health check passes

```bash
$ ~/scripts/health-check.sh
```

Expected: 0 failures.

### 10. Test the AI model

Verify that the connection to the AI provider works with a simple call:

```bash
$ openclaw model test
```

If `openclaw model test` is not available, test directly via OpenRouter:

```bash
$ OPENROUTER_KEY=$(docker exec -e VAULT_ADDR=http://127.0.0.1:8200 vault vault kv get -field=api_key secret/openrouter)
$ curl -s https://openrouter.ai/api/v1/chat/completions \
  -H "Authorization: Bearer ${OPENROUTER_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"model":"anthropic/claude-haiku-4-5","messages":[{"role":"user","content":"Reponds juste OK"}],"max_tokens":10}' \
  | python3 -m json.tool
```

Expected: a JSON response containing the text "OK" (or similar) in `choices[0].message.content`.

### 11. openclaw doctor

```bash
$ openclaw doctor
```

Expected: all checks green.

## Quick verification script

To verify everything in one command:

```bash
$ check() { echo -n "$1: "; if eval "$2" > /dev/null 2>&1; then echo "OK"; else echo "FAILED"; fi; }
$ echo "=== COMPLETE VERIFICATION ==="
$ check "1. Docker"      "docker ps"
$ check "2. Vault unseal" "docker exec vault vault status 2>/dev/null | grep 'Sealed.*false'"
$ check "3. Vault secret" "docker exec vault vault kv get -field=api_key secret/openrouter"
$ check "4. PostgreSQL"   "docker exec postgres psql -U oa_admin -d oa_system -c 'SELECT 1;'"
$ check "5. Tailscale"    "tailscale status"
$ echo -n "6. Node: "    && node --version
$ check "7. OpenClaw"     "openclaw --version"
$ check "8. Gateway"      "sudo systemctl is-active openclaw-gateway"
$ echo "=== END ==="
```

## Diagnosis by symptom

If any point fails, here's what to do:

| Point | Symptom | Diagnosis |
|-------|----------|------------|
| 1 | Docker ps error | `sudo systemctl start docker`. If error persists: `journalctl -u docker -n 50`. |
| 2 | Vault sealed | Normal after restart. Unseal with 3 keys (section 07, step 7). |
| 3 | Secret unreadable | Token expired? `docker exec vault vault token lookup`. Recreate if necessary. |
| 4 | PostgreSQL not responding | `docker logs postgres` to see the error. Often a permissions issue on `data/`. |
| 5 | Tailscale disconnected | `sudo tailscale up`. If error: `sudo systemctl restart tailscaled`. |
| 6 | Node version too old | `nvm install --lts && nvm alias default lts/*`. |
| 7 | OpenClaw not installed | `npm install -g @anthropic-ai/claude-code`. Verify the nvm PATH. |
| 8 | Gateway inactive | `journalctl -u openclaw-gateway -n 50`. Often an incorrect path in the service file. |
| 9 | Health check failed | The script indicates which point failed. Fix that specific point. |
| 10 | Doctor failed | Follow the instructions displayed by `openclaw doctor`. |

## If everything is green

Congratulations. Your infrastructure is operational. Move on to the following sections (17, 18, 19) to finalize the development workflow, then to chapter 3.

## If any point stays red

Do not move to the next chapter with a red point. Each building block depends on the previous ones. An unresolved issue here will become a bigger problem later.

## Estimated time

10 minutes (verification only, without corrections).
