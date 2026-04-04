---
---
status: complete
audience: both
chapter: 05
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: en
---

# 5.1 -- Daily Health Check

## Context

A health check is 30 seconds of diagnosis that prevents 3 hours of downtime. You verify that everything is running, every day, automatically. If something goes down, you know about it before your users do.

## What to Check

| Component | Command | Expected |
|---|---|---|
| Docker Containers | `docker ps --format "{{.Names}} {{.Status}}"` | All "Up" |
| Web Services | `curl -s -o /dev/null -w "%{http_code}" http://localhost:PORT` | 200 |
| Disk Space | `df -h / --output=pcent` | < 80% |
| PostgreSQL | `pg_isready` | Accepting connections |
| Memory | `free -m` | Free memory > 20% |
| SSL Certificates | `openssl s_client -connect domain:443 2>/dev/null \| openssl x509 -noout -enddate` | > 30 days |
| Vault | `vault status` | Sealed: false |

## Complete Script: health-check.sh

```bash
#!/bin/bash
# health-check.sh — Daily diagnostic
# Usage : ./health-check.sh [--quiet]
# --quiet : only display errors (for cron)

TELEGRAM_BOT_TOKEN="${TELEGRAM_BOT_TOKEN:-}"
TELEGRAM_CHAT_ID="${TELEGRAM_CHAT_ID:-}"
QUIET="${1:-}"
ERRORS=""

log() {
    if [ "$QUIET" != "--quiet" ]; then
        echo "$1"
    fi
}

error() {
    ERRORS="${ERRORS}\n[KO] $1"
    echo "[KO] $1" >&2
}

ok() {
    log "[OK] $1"
}

send_telegram() {
    if [ -n "$TELEGRAM_BOT_TOKEN" ] && [ -n "$TELEGRAM_CHAT_ID" ]; then
        local message="$1"
        curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
            -d chat_id="$TELEGRAM_CHAT_ID" \
            -d text="$message" \
            -d parse_mode="Markdown" > /dev/null
    fi
}

# === Docker Containers ===
log "--- Docker ---"
if command -v docker &> /dev/null; then
    DOWN_CONTAINERS=$(docker ps -a --filter "status=exited" --format "{{.Names}}" 2>/dev/null)
    if [ -n "$DOWN_CONTAINERS" ]; then
        error "Containers down : $DOWN_CONTAINERS"
    else
        ok "All containers are up"
    fi
else
    error "Docker not installed"
fi

# === Web Services ===
log "--- Web Services ---"
SERVICES=("http://localhost:3000" "http://localhost:8080")
SERVICE_NAMES=("cockpit" "api")

for i in "${!SERVICES[@]}"; do
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 "${SERVICES[$i]}" 2>/dev/null)
    if [ "$HTTP_CODE" = "200" ]; then
        ok "${SERVICE_NAMES[$i]} responding (HTTP $HTTP_CODE)"
    else
        error "${SERVICE_NAMES[$i]} not responding (HTTP $HTTP_CODE)"
    fi
done

# === Disk Space ===
log "--- Disk ---"
DISK_USAGE=$(df / --output=pcent | tail -1 | tr -d ' %')
if [ "$DISK_USAGE" -lt 80 ]; then
    ok "Disk : ${DISK_USAGE}% used"
elif [ "$DISK_USAGE" -lt 90 ]; then
    error "Disk : ${DISK_USAGE}% used (threshold 80%)"
else
    error "CRITICAL — Disk : ${DISK_USAGE}% used"
fi

# === PostgreSQL ===
log "--- PostgreSQL ---"
if pg_isready -q 2>/dev/null; then
    ok "PostgreSQL OK"
else
    error "PostgreSQL not responding"
fi

# === Memory ===
log "--- Memory ---"
MEM_TOTAL=$(free -m | awk '/Mem:/ {print $2}')
MEM_AVAIL=$(free -m | awk '/Mem:/ {print $7}')
MEM_PERCENT=$((MEM_AVAIL * 100 / MEM_TOTAL))
if [ "$MEM_PERCENT" -gt 20 ]; then
    ok "Memory : ${MEM_PERCENT}% available (${MEM_AVAIL}M/${MEM_TOTAL}M)"
else
    error "Low memory : ${MEM_PERCENT}% available (${MEM_AVAIL}M/${MEM_TOTAL}M)"
fi

# === Vault ===
log "--- Vault ---"
if command -v vault &> /dev/null; then
    VAULT_STATUS=$(vault status -format=json 2>/dev/null | jq -r '.sealed' 2>/dev/null)
    if [ "$VAULT_STATUS" = "false" ]; then
        ok "Vault unsealed"
    else
        error "Vault sealed or inaccessible"
    fi
else
    log "[SKIP] Vault not installed"
fi

# === Summary and Alert ===
log ""
if [ -n "$ERRORS" ]; then
    log "=== PROBLEMS DETECTED ==="
    echo -e "$ERRORS"
    
    # Telegram Alert
    ALERT_MSG="*Health Check KO* — $(hostname) — $(date '+%Y-%m-%d %H:%M')"
    ALERT_MSG="${ALERT_MSG}$(echo -e "$ERRORS")"
    send_telegram "$ALERT_MSG"
    
    exit 1
else
    log "=== EVERYTHING OK ==="
    exit 0
fi
```

## Automate with Cron

```bash
# Edit crontab
crontab -e

# Health check every day at 7:00 AM
0 7 * * * /opt/scripts/health-check.sh --quiet >> /var/log/health-check.log 2>&1

# Health check every 4 hours (for critical services)
0 */4 * * * /opt/scripts/health-check.sh --quiet >> /var/log/health-check.log 2>&1
```

## Configure Telegram Alerts

### 1. Create a Telegram Bot

1. Open Telegram, search for `@BotFather`.
2. Send `/newbot`.
3. Give it a name and username.
4. Copy the token.

### 2. Get Your Chat ID

1. Send a message to your bot.
2. Open `https://api.telegram.org/bot<TOKEN>/getUpdates`.
3. Find `chat.id` in the response.

### 3. Store Credentials

```bash
# In Vault (recommended)
vault kv put secret/telegram bot_token="123456:ABC..." chat_id="987654321"

# Or as environment variables in /etc/environment
TELEGRAM_BOT_TOKEN="123456:ABC..."
TELEGRAM_CHAT_ID="987654321"
```

## Common Mistakes

**No health check.** You discover the outage when a user contacts you. Always too late.

**Health check without alerts.** The script runs, the log fills up, but nobody reads it. Without alerts, it's useless.

**Too many checks.** 50 verifications with overly sensitive thresholds. You receive 10 alerts per day and ignore everything. Start with 5-7 essential checks.

**Script not tested.** The script has a bug, cron runs it, but it detects nothing. Test manually by simulating a failure (stop a container, fill the disk).

## Steps

1. Copy the `health-check.sh` script to `/opt/scripts/`.
2. Adapt the services and ports to your setup.
3. Make executable: `chmod +x /opt/scripts/health-check.sh`.
4. Test manually: `./health-check.sh`.
5. Configure the Telegram bot and variables.
6. Test the alert: stop a container, run the script.
7. Add to crontab.

## Checklist

- [ ] The script runs without error in normal and --quiet mode.
- [ ] Each critical component is checked.
- [ ] Telegram alert works (tested with a simulated failure).
- [ ] Cron is configured and running.
- [ ] Log is written to /var/log/health-check.log.

---
