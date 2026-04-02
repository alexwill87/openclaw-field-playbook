---
status: complete
audience: both
chapter: 02
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 2.19 -- Script de deploiement

## Contexte

Le script `deploy.sh` automatise le deploiement complet : pull du code, installation des dependances, build et redemarrage des services. Il doit etre **idempotent** : executable plusieurs fois de suite sans effet de bord. Que le systeme soit a jour ou non, le resultat final est le meme.

## Le script complet

Creez `~/scripts/deploy.sh` :

```bash
#!/bin/bash
set -euo pipefail

# === Configuration ===
PROJECT_DIR="$HOME/oa-system"
LOG_FILE="$HOME/logs/deploy.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# === Fonctions ===
log() {
  echo "[${TIMESTAMP}] $1" | tee -a "$LOG_FILE"
}

notify() {
  if [ -f "$HOME/scripts/notify-telegram.sh" ]; then
    "$HOME/scripts/notify-telegram.sh" "$1" 2>/dev/null || true
  fi
}

fail() {
  log "ECHEC : $1"
  notify "[OA Deploy] ECHEC : $1"
  exit 1
}

# === Pre-checks ===
log "=== Debut deploiement ==="

# Verifier que le repertoire existe
[ -d "$PROJECT_DIR" ] || fail "Repertoire $PROJECT_DIR introuvable"

# Verifier que Docker tourne
docker info > /dev/null 2>&1 || fail "Docker n'est pas demarre"

# Verifier que Vault est unseal
docker exec vault vault status 2>&1 | grep -q "Sealed.*false" || fail "Vault est sealed"

cd "$PROJECT_DIR"

# === Etape 1 : Git pull ===
log "Git pull..."
BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "$BRANCH" != "main" ]; then
  log "ATTENTION : branche actuelle = $BRANCH (pas main)"
fi

git fetch origin
LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/$BRANCH)

if [ "$LOCAL" = "$REMOTE" ]; then
  log "Deja a jour (commit: ${LOCAL:0:8}). Rien a deployer."
  exit 0
fi

git pull origin "$BRANCH" || fail "git pull a echoue"
NEW_COMMIT=$(git rev-parse --short HEAD)
log "Nouveau commit : $NEW_COMMIT"

# === Etape 2 : Installation des dependances ===
log "Installation des dependances npm..."
if [ -f "package.json" ]; then
  npm ci --production 2>&1 | tail -1 | tee -a "$LOG_FILE"
else
  log "Pas de package.json, etape ignoree"
fi

# === Etape 3 : Build ===
log "Build..."
if [ -f "package.json" ] && grep -q '"build"' package.json; then
  npm run build 2>&1 | tail -5 | tee -a "$LOG_FILE"
else
  log "Pas de script build, etape ignoree"
fi

# === Etape 4 : Mise a jour Docker Compose (si necessaire) ===
log "Verification des conteneurs Docker..."
for service_dir in docker/vault docker/postgres; do
  if [ -f "$HOME/$service_dir/docker-compose.yml" ]; then
    cd "$HOME/$service_dir"
    docker compose pull 2>/dev/null || true
    docker compose up -d 2>&1 | tee -a "$LOG_FILE"
    cd "$PROJECT_DIR"
  fi
done

# === Etape 5 : Redemarrage gateway ===
# Le playbook recommande systemd (section 2.15).
# Si vous utilisez PM2, remplacez cette section par : pm2 reload all --update-env
log "Redemarrage gateway (systemd)..."
if sudo systemctl restart openclaw-gateway 2>&1; then
  log "Gateway redemarree"
else
  log "ATTENTION : restart gateway echoue"
  notify "[OA Deploy] ECHEC restart gateway sur $NEW_COMMIT"
  exit 1
fi

# === Etape 6 : Health check ===
log "Health check post-deploiement..."
sleep 5  # Laisser le temps aux services de demarrer

if "$HOME/scripts/health-check.sh" >> "$LOG_FILE" 2>&1; then
  log "Health check : OK"
  log "=== Deploiement termine avec succes ($NEW_COMMIT) ==="
  notify "[OA Deploy] Deploiement reussi : $NEW_COMMIT sur $BRANCH"
else
  log "ATTENTION : health check a des echecs"
  notify "[OA Deploy] WARNING : $NEW_COMMIT deploye mais health check en echec"
  exit 1
fi
```

## Installation

```bash
$ chmod +x ~/scripts/deploy.sh
```

## Utilisation

```bash
$ ~/scripts/deploy.sh
```

Le script :
1. Verifie les prerequis (Docker, Vault)
2. Pull le code depuis Git
3. S'arrete si rien n'a change (idempotent)
4. Installe les dependances (`npm ci`)
5. Build le projet si un script build existe
6. Met a jour les conteneurs Docker si necessaire
7. Recharge les processus PM2
8. Redemarre la gateway
9. Lance le health check
10. Notifie via Telegram

## Proprietes du script

| Propriete | Detail |
|-----------|--------|
| Idempotent | Si le code est deja a jour, le script s'arrete proprement |
| Echec rapide | `set -euo pipefail` arrete le script a la premiere erreur |
| Logging | Chaque etape est logguee dans `~/logs/deploy.log` |
| Notification | Telegram est notifie en cas de succes ou d'echec |
| Adaptable | Les etapes optionnelles (build, PM2) sont ignorees si non applicables |

## Deploiement automatique via Git hook (optionnel)

Pour declencher le deploiement automatiquement a chaque push :

Creez `.git/hooks/post-receive` sur le VPS (si vous utilisez un bare repo) :

```bash
#!/bin/bash
~/scripts/deploy.sh
```

Ou utilisez GitHub Actions pour declencher le script via SSH.

## Erreurs courantes

- **"npm ci" echoue** : Le fichier `package-lock.json` est absent ou desynchronise. Faites `npm install` puis committez le lock file.
- **Gateway qui ne redemarre pas** : Verifiez les logs : `journalctl -u openclaw-gateway -n 20`. Souvent un token Vault expire.
- **Script qui echoue au premier lancement** : Le depot Git n'existe peut-etre pas encore dans `~/oa-system`. Creez-le d'abord (section 17).
- **Permissions** : Le script doit etre execute par l'utilisateur `deploy`, pas par root. Les commandes sudo internes (restart gateway) fonctionnent grace aux droits sudo du user.

## Verification

```bash
$ ~/scripts/deploy.sh
$ cat ~/logs/deploy.log | tail -20
```

Resultats attendus :
- Script s'execute sans erreur (ou s'arrete avec "Deja a jour")
- Log montre les etapes completees
- Notification Telegram recue (si configuree)

## Temps estime

15 minutes (creation et premier test).
