---
status: complete
audience: both
chapter: 02
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 2.9 -- Premier health check

## Contexte

Avant d'aller plus loin, on verifie que toute l'infrastructure de base fonctionne. Ce script sera reutilise dans les sections suivantes, dans les crons de surveillance et dans le script de deploiement.

## Le script complet

Creez le fichier :

```bash
$ mkdir -p ~/scripts
$ cat > ~/scripts/health-check.sh << 'HEALTHSCRIPT'
#!/bin/bash
# Health check infrastructure OA
# Usage : ./health-check.sh
# Codes de sortie : 0 = tout OK, 1 = au moins un echec

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

# Ports critiques (verification avant lancement de conteneurs)
check "Port 8200 (Vault) occupe" "ss -ltnp | grep -q :8200"
check "Port 5432 (PostgreSQL) occupe" "ss -ltnp | grep -q :5432"

# Docker
check "Docker daemon" "docker info"
check "Docker Compose" "docker compose version"

# Vault
check "Vault conteneur" "docker ps | grep vault | grep -q Up"
check "Vault unsealed" "docker exec vault vault status 2>&1 | grep -q 'Sealed.*false'"
check "Vault secret lisible" "docker exec vault vault kv get secret/openrouter"

# PostgreSQL
check "PostgreSQL conteneur" "docker ps | grep postgres | grep -q Up"
check "PostgreSQL connexion" "docker exec postgres psql -U oa_admin -d oa_system -c 'SELECT 1;'"

# Tailscale
check "Tailscale actif" "tailscale status"
check "Tailscale IP" "tailscale ip -4"

# Systeme
check "Espace disque > 10%" "test $(df / --output=pcent | tail -1 | tr -d '% ') -lt 90"
check "RAM disponible > 1Go" "test $(free -m | awk '/Mem:/ {print \$7}') -gt 1024"

echo "---"
echo "Resultats : $PASS OK, $FAIL echec(s)"

if [ $FAIL -gt 0 ]; then
  exit 1
else
  echo "Infrastructure operationnelle."
  exit 0
fi
HEALTHSCRIPT
$ chmod +x ~/scripts/health-check.sh
```

## Verification

Lancez le script :

```bash
$ ~/scripts/health-check.sh
```

## Sortie attendue

```
=== Health Check Infrastructure ===
Date : jeu. 02 avril 2026 14:30:00 CEST
---
[OK]    Docker daemon
[OK]    Docker Compose
[OK]    Vault conteneur
[OK]    Vault unsealed
[OK]    Vault secret lisible
[OK]    PostgreSQL conteneur
[OK]    PostgreSQL connexion
[OK]    Tailscale actif
[OK]    Tailscale IP
[OK]    Espace disque > 10%
[OK]    RAM disponible > 1Go
---
Resultats : 11 OK, 0 echec(s)
Infrastructure operationnelle.
```

## Ajouter au cron (optionnel)

Pour une verification toutes les 15 minutes avec log :

```bash
$ crontab -e
```

Ajoutez :

```
*/15 * * * * /home/deploy/scripts/health-check.sh >> /home/deploy/logs/health-check.log 2>&1
```

> **Note :** Les checks de ports verifient que les ports sont bien utilises (par les conteneurs attendus). Si un port est libre alors qu'un conteneur devrait tourner, c'est un indicateur de probleme. Avant un `docker compose up`, vous pouvez aussi verifier qu'un port n'est PAS deja occupe par un autre processus avec `ss -ltnp | grep :PORT`.

## Diagnostic par symptome

| Symptome | Cause probable | Action |
|----------|---------------|--------|
| Docker daemon ECHEC | Docker pas demarre | `sudo systemctl start docker` |
| Vault conteneur ECHEC | Conteneur arrete | `cd ~/docker/vault && docker compose up -d` |
| Vault unsealed ECHEC | Vault sealed apres redemarrage | Executer l'unseal (3 cles) |
| Vault secret ECHEC | Moteur KV pas active ou token expire | `vault secrets enable -path=secret kv-v2` |
| PostgreSQL ECHEC | Conteneur arrete ou crash | `cd ~/docker/postgres && docker compose up -d` puis verifier les logs : `docker logs postgres` |
| Tailscale ECHEC | Service arrete | `sudo systemctl start tailscaled && sudo tailscale up` |
| Espace disque ECHEC | Disque plein | `docker system prune -a` et verifier les logs/backups |
| RAM ECHEC | Memoire saturee | `docker stats` pour identifier le conteneur gourmand |

## Erreurs courantes

- **Le script echoue sur Vault secret** : Vault est peut-etre sealed. C'est normal apres un redemarrage. Unsealez d'abord.
- **"free: command not found"** : Installez `procps` : `sudo apt install -y procps`.
- **Faux positif sur l'espace disque** : Le seuil est fixe a 90% utilise. Ajustez si necessaire.

## Verification

Le script EST la verification. S'il sort avec le code 0, tout est bon :

```bash
$ ~/scripts/health-check.sh && echo "Pret pour la suite"
```

## Temps estime

10 minutes.
