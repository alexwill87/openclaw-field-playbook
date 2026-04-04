---
---
status: complete
audience: both
chapter: 05
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: en
---

# 5.9 -- Secret Rotation

## Context

A secret that never changes is a secret waiting to be compromised. Secret rotation -- regularly changing passwords, tokens, and API keys -- is a fundamental security practice. Not because you've been compromised, but to limit the damage if you are one day without knowing it.

## Why rotate

- **Silent leak.** A token was exposed in a log, a commit, a screenshot. You don't know about it. Rotation limits the exploitation window.
- **Employee departure.** They had access to secrets. Immediate rotation.
- **Compliance.** Some standards (SOC2, ISO 27001) require periodic rotation.
- **Hygiene.** A secret from 2 years ago is a dormant attack vector.

## What to rotate and when

| Secret | Frequency | Priority |
|---|---|---|
| Third-party API tokens (Telegram, GitHub) | Every 3 months | High |
| Database passwords | Every 3 months | High |
| JWT keys / session secrets | Monthly | High |
| SSH passwords (if password auth) | Disable, use keys | Critical |
| SSH keys | Annual | Medium |
| Vault unseal keys | Annual or after incident | High |
| Internal service tokens | Every 3 months | Medium |

## How to rotate: the procedure

### The workflow in 5 steps

1. **Generate** the new secret.
2. **Store** in Vault.
3. **Deploy**: update the service that uses the secret.
4. **Test**: verify that the service works with the new secret.
5. **Log**: document the rotation.

### Complete example: rotating an API token

```bash
#!/bin/bash
# rotate-secret.sh — Secret rotation
# Usage : ./rotate-secret.sh <service_name> <secret_key>

SERVICE="$1"
KEY="$2"

if [ -z "$SERVICE" ] || [ -z "$KEY" ]; then
    echo "Usage : $0 <service_name> <secret_key>"
    exit 1
fi

LOG_FILE="/var/log/secret-rotation.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

log() {
    echo "$TIMESTAMP [ROTATION] $1" | tee -a "$LOG_FILE"
}

# 1. Generate the new secret
NEW_SECRET=$(openssl rand -hex 32)
log "Nouveau secret genere pour ${SERVICE}/${KEY}"

# 2. Save the old one in Vault (previous version)
OLD_SECRET=$(vault kv get -field="$KEY" "secret/$SERVICE" 2>/dev/null)
log "Ancien secret sauvegarde (Vault versioning)"

# 3. Store the new one in Vault
vault kv put "secret/$SERVICE" "$KEY=$NEW_SECRET"
log "Nouveau secret stocke dans Vault"

# 4. Restart the service
log "Redemarrage de $SERVICE..."
cd /opt/"$SERVICE" && docker compose restart
sleep 5

# 5. Test
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "http://localhost:3000/health" 2>/dev/null)
if [ "$HTTP_CODE" = "200" ]; then
    log "OK — Service $SERVICE repond correctement"
else
    log "ERREUR — Service $SERVICE ne repond pas (HTTP $HTTP_CODE)"
    log "ROLLBACK — Restauration de l'ancien secret"
    vault kv rollback -version=$(vault kv metadata get "secret/$SERVICE" | grep -c "version") "secret/$SERVICE"
    cd /opt/"$SERVICE" && docker compose restart
    exit 1
fi

log "Rotation terminee avec succes pour ${SERVICE}/${KEY}"
```

### PostgreSQL password rotation

```bash
# 1. Generate
NEW_PASS=$(openssl rand -base64 24)

# 2. Change in PostgreSQL
sudo -u postgres psql -c "ALTER USER oa_admin PASSWORD '$NEW_PASS';"

# 3. Store in Vault
vault kv put secret/postgresql password="$NEW_PASS"

# 4. Update the connection string in services
# (via environment variable or .env)

# 5. Restart services that use the DB
docker compose restart

# 6. Test
psql -U oa_admin -d cockpit -c "SELECT 1;" && echo "OK" || echo "ERREUR"

# 7. Log
echo "$(date) PostgreSQL password rotated" >> /var/log/secret-rotation.log
```

## Frequency and scheduling

### Typical calendar

```
1st of each month :
  - Rotation of JWT keys / session secrets

1st of each quarter (January, April, July, October) :
  - Rotation of third-party API tokens
  - Rotation of PostgreSQL password
  - Rotation of internal service tokens

January 1st :
  - Rotation of SSH keys
  - Review of Vault unseal keys
```

### Automate the reminder

```bash
# Cron: reminder on the 1st of each month
0 9 1 * * echo "Rappel : rotation des secrets mensuelle" | /opt/scripts/send-telegram.sh
```

## Common mistakes

**Never rotate.** The same token for 2 years. If (when) it leaks, the exploitation window is 2 years.

**Rotate without testing.** You change the secret, the service won't start, and it's Saturday. Always test immediately after.

**No rollback.** The new secret doesn't work and you've overwritten the old one. Vault keeps versions -- use them.

**Secret hardcoded in code.** Rotation is useless if the secret is also in a config file not managed by Vault. Audit it (section 4.13).

**Forget a service.** You rotate the PostgreSQL password but a second service also uses that password and it's not updated.

## Steps

1. List all secrets in your infrastructure.
2. Classify them by rotation frequency.
3. Create a rotation calendar.
4. Write the rotation workflow in WORKFLOWS.md.
5. Do the first rotation manually.
6. Automate with a script and a reminder cron job.

## Verification

- [ ] All secrets are inventoried with their last rotation date.
- [ ] A rotation calendar exists.
- [ ] The rotation script includes a test and a rollback.
- [ ] Each rotation is logged in /var/log/secret-rotation.log.
- [ ] No secret is older than 3 months without rotation.

---
