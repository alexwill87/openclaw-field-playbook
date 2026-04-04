---
---
status: complete
audience: both
chapter: 02
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: en
---

# 2.9 -- First health check

## Context

Before moving forward, we verify that all basic infrastructure is working. This script will be reused in the following sections, in monitoring crons, and in the deployment script.

## The complete script

Create the file:

```bash
$ mkdir -p ~/scripts
$ cat > ~/scripts/health-check.sh << 'HEALTHSCRIPT'
#!/bin/bash
# Health check infrastructure OA
# Usage : ./health-check.sh
# Exit codes : 0 = all OK, 1 = at least one failure

PASS=0
FAIL=0

check() {
  local name="$1"
  local cmd="$2"

  if eval "$cmd" > /dev/null 2>&1; then
    echo "[OK]    $name"
    ((PASS++))
  else
    echo "[ECHEC] $name"
    ((FAIL++))
  fi
}

echo "=== Health Check Infrastructure ==="
echo "Date : $(date)"
echo "---"

# Critical ports (verification before launching containers)
check "Port 8200 (Vault) in use" "ss -ltnp | grep -q :8200"
check "Port 5432 (PostgreSQL) in use" "ss -ltnp | grep -q :5432"

# Docker
check "Docker daemon" "docker info"
check "Docker Compose" "docker compose version"

# Vault
check "Vault container" "docker ps | grep vault | grep -q Up"
check "Vault unsealed" "docker exec vault vault status 2>&1 | grep -q 'Sealed.*false'"
check "Vault secret readable" "docker exec vault vault kv get secret/openrouter"

# PostgreSQL
check "PostgreSQL container" "docker ps | grep postgres | grep -q Up"
check "PostgreSQL connection" "docker exec postgres psql -U oa_admin -d oa_system -c 'SELECT 1;'"

# Tailscale
check "Tailscale active" "tailscale status"
check "Tailscale IP" "tailscale ip -4"

# System
check "Disk space > 10%" "test $(df / --output=pcent | tail -1 | tr -d '% ') -lt 90"
check "Available RAM > 1GB" "test $(free -m | awk '/Mem:/ {print \$7}') -gt 1024"

echo "---"
echo "Results : $PASS OK, $FAIL failure(s)"

if [ $FAIL -gt 0 ]; then
  exit 1
else
  echo "Infrastructure operational."
  exit 0
fi
HEALTHSCRIPT
$ chmod +x ~/scripts/health-check.sh
```

## Verification

Run the script:

```bash
$ ~/scripts/health-check.sh
```

## Expected output

```
=== Health Check Infrastructure ===
Date : Thu 02 Apr 2026 14:30:00 CEST
---
[OK]    Docker daemon
[OK]    Docker Compose
[OK]    Vault container
[OK]    Vault unsealed
[OK]    Vault secret readable
[OK]    PostgreSQL container
[OK]    PostgreSQL connection
[OK]    Tailscale active
[OK]    Tailscale IP
[OK]    Disk space > 10%
[OK]    Available RAM > 1GB
---
Results : 11 OK, 0 failure(s)
Infrastructure operational.
```

## Add to cron (optional)

For verification every 15 minutes with logging:

```bash
$ crontab -e
```

Add:

```
*/15 * * * * /home/deploy/scripts/health-check.sh >> /home/deploy/logs/health-check.log 2>&1
```

> **Note:** The port checks verify that the ports are in use (by the expected containers). If a port is free when a container should be running, that's an indicator of a problem. Before a `docker compose up`, you can also verify that a port is NOT already in use by another process with `ss -ltnp | grep :PORT`.

## Diagnostic by symptom

| Symptom | Probable cause | Action |
|----------|---------------|--------|
| Docker daemon FAILURE | Docker not started | `sudo systemctl start docker` |
| Vault container FAILURE | Container stopped | `cd ~/docker/vault && docker compose up -d` |
| Vault unsealed FAILURE | Vault sealed after restart | Run unseal (3 keys) |
| Vault secret FAILURE | KV engine not enabled or token expired | `vault secrets enable -path=secret kv-v2` |
| PostgreSQL FAILURE | Container stopped or crashed | `cd ~/docker/postgres && docker compose up -d` then check logs: `docker logs postgres` |
| Tailscale FAILURE | Service stopped | `sudo systemctl start tailscaled && sudo tailscale up` |
| Disk space FAILURE | Disk full | `docker system prune -a` and check logs/backups |
| RAM FAILURE | Memory saturated | `docker stats` to identify the heavy container |

## Common errors

- **The script fails on Vault secret**: Vault may be sealed. This is normal after a restart. Unseal first.
- **"free: command not found"**: Install `procps`: `sudo apt install -y procps`.
- **False positive on disk space**: The threshold is set to 90% used. Adjust if needed.

## Verification

The script IS the verification. If it exits with code 0, everything is good:

```bash
$ ~/scripts/health-check.sh && echo "Ready for next step"
```

## Estimated time

10 minutes.
