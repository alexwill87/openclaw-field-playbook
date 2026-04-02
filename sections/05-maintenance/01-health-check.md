---
status: complete
audience: both
chapter: 05
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 5.1 -- Health check quotidien

## Contexte

Un health check, c'est 30 secondes de diagnostic qui evitent 3 heures de panne. Vous verifiez que tout tourne, chaque jour, automatiquement. Si quelque chose tombe, vous le savez avant vos utilisateurs.

## Ce qu'il faut verifier

| Composant | Commande | Attendu |
|---|---|---|
| Containers Docker | `docker ps --format "{{.Names}} {{.Status}}"` | Tous "Up" |
| Services web | `curl -s -o /dev/null -w "%{http_code}" http://localhost:PORT` | 200 |
| Espace disque | `df -h / --output=pcent` | < 80% |
| PostgreSQL | `pg_isready` | Accepting connections |
| Memoire | `free -m` | Memoire libre > 20% |
| Certificats SSL | `openssl s_client -connect domain:443 2>/dev/null \| openssl x509 -noout -enddate` | > 30 jours |
| Vault | `vault status` | Sealed: false |

## Script complet : health-check.sh

```bash
#!/bin/bash
# health-check.sh — Diagnostic quotidien
# Usage : ./health-check.sh [--quiet]
# --quiet : n'affiche que les erreurs (pour cron)

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

# === Containers Docker ===
log "--- Docker ---"
if command -v docker &> /dev/null; then
    DOWN_CONTAINERS=$(docker ps -a --filter "status=exited" --format "{{.Names}}" 2>/dev/null)
    if [ -n "$DOWN_CONTAINERS" ]; then
        error "Containers down : $DOWN_CONTAINERS"
    else
        ok "Tous les containers sont up"
    fi
else
    error "Docker non installe"
fi

# === Services web ===
log "--- Services web ---"
SERVICES=("http://localhost:3000" "http://localhost:8080")
SERVICE_NAMES=("cockpit" "api")

for i in "${!SERVICES[@]}"; do
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 "${SERVICES[$i]}" 2>/dev/null)
    if [ "$HTTP_CODE" = "200" ]; then
        ok "${SERVICE_NAMES[$i]} repond (HTTP $HTTP_CODE)"
    else
        error "${SERVICE_NAMES[$i]} ne repond pas (HTTP $HTTP_CODE)"
    fi
done

# === Espace disque ===
log "--- Disque ---"
DISK_USAGE=$(df / --output=pcent | tail -1 | tr -d ' %')
if [ "$DISK_USAGE" -lt 80 ]; then
    ok "Disque : ${DISK_USAGE}% utilise"
elif [ "$DISK_USAGE" -lt 90 ]; then
    error "Disque : ${DISK_USAGE}% utilise (seuil 80%)"
else
    error "CRITIQUE — Disque : ${DISK_USAGE}% utilise"
fi

# === PostgreSQL ===
log "--- PostgreSQL ---"
if pg_isready -q 2>/dev/null; then
    ok "PostgreSQL OK"
else
    error "PostgreSQL ne repond pas"
fi

# === Memoire ===
log "--- Memoire ---"
MEM_TOTAL=$(free -m | awk '/Mem:/ {print $2}')
MEM_AVAIL=$(free -m | awk '/Mem:/ {print $7}')
MEM_PERCENT=$((MEM_AVAIL * 100 / MEM_TOTAL))
if [ "$MEM_PERCENT" -gt 20 ]; then
    ok "Memoire : ${MEM_PERCENT}% disponible (${MEM_AVAIL}M/${MEM_TOTAL}M)"
else
    error "Memoire faible : ${MEM_PERCENT}% disponible (${MEM_AVAIL}M/${MEM_TOTAL}M)"
fi

# === Vault ===
log "--- Vault ---"
if command -v vault &> /dev/null; then
    VAULT_STATUS=$(vault status -format=json 2>/dev/null | jq -r '.sealed' 2>/dev/null)
    if [ "$VAULT_STATUS" = "false" ]; then
        ok "Vault unsealed"
    else
        error "Vault sealed ou inaccessible"
    fi
else
    log "[SKIP] Vault non installe"
fi

# === Resume et alerte ===
log ""
if [ -n "$ERRORS" ]; then
    log "=== PROBLEMES DETECTES ==="
    echo -e "$ERRORS"
    
    # Alerte Telegram
    ALERT_MSG="*Health Check KO* — $(hostname) — $(date '+%Y-%m-%d %H:%M')"
    ALERT_MSG="${ALERT_MSG}$(echo -e "$ERRORS")"
    send_telegram "$ALERT_MSG"
    
    exit 1
else
    log "=== TOUT EST OK ==="
    exit 0
fi
```

## Automatiser avec cron

```bash
# Editer le crontab
crontab -e

# Health check tous les jours a 7h00
0 7 * * * /opt/scripts/health-check.sh --quiet >> /var/log/health-check.log 2>&1

# Health check toutes les 4 heures (pour les services critiques)
0 */4 * * * /opt/scripts/health-check.sh --quiet >> /var/log/health-check.log 2>&1
```

## Configurer les alertes Telegram

### 1. Creer un bot Telegram

1. Ouvrez Telegram, cherchez `@BotFather`.
2. Envoyez `/newbot`.
3. Donnez un nom et un username.
4. Copiez le token.

### 2. Obtenir votre chat ID

1. Envoyez un message a votre bot.
2. Ouvrez `https://api.telegram.org/bot<TOKEN>/getUpdates`.
3. Trouvez `chat.id` dans la reponse.

### 3. Stocker les credentials

```bash
# Dans Vault (recommande)
vault kv put secret/telegram bot_token="123456:ABC..." chat_id="987654321"

# Ou en variables d'environnement dans /etc/environment
TELEGRAM_BOT_TOKEN="123456:ABC..."
TELEGRAM_CHAT_ID="987654321"
```

## Erreurs courantes

**Pas de health check.** Vous decouvrez la panne quand un utilisateur vous ecrit. Toujours trop tard.

**Health check sans alerte.** Le script tourne, le log se remplit, mais personne ne le lit. Sans alerte, c'est inutile.

**Trop de checks.** 50 verifications avec des seuils trop sensibles. Vous recevez 10 alertes par jour et vous ignorez tout. Commencez avec 5-7 checks essentiels.

**Pas de test du script.** Le script a un bug, le cron tourne, mais il ne detecte rien. Testez manuellement en simulant une panne (arretez un container, remplissez le disque).

## Etapes

1. Copiez le script `health-check.sh` dans `/opt/scripts/`.
2. Adaptez les services et ports a votre setup.
3. Rendez executable : `chmod +x /opt/scripts/health-check.sh`.
4. Testez manuellement : `./health-check.sh`.
5. Configurez le bot Telegram et les variables.
6. Testez l'alerte : arretez un container, lancez le script.
7. Ajoutez au crontab.

## Verification

- [ ] Le script tourne sans erreur en mode normal et --quiet.
- [ ] Chaque composant critique est verifie.
- [ ] L'alerte Telegram fonctionne (testee avec une panne simulee).
- [ ] Le cron est configure et tourne.
- [ ] Le log est ecrit dans /var/log/health-check.log.
