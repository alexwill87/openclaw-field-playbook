---
status: complete
audience: both
chapter: 05
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 5.9 -- Rotation des secrets

## Contexte

Un secret qui ne change jamais est un secret qui attend d'etre compromis. La rotation des secrets -- changer regulierement les mots de passe, tokens, et cles API -- est une pratique de securite fondamentale. Pas parce que vous avez ete compromis, mais pour limiter les degats si vous l'etes un jour sans le savoir.

## Pourquoi tourner

- **Fuite silencieuse.** Un token a ete expose dans un log, un commit, un screenshot. Vous ne le savez pas. La rotation limite la fenetre d'exploitation.
- **Depart d'un collaborateur.** Il avait acces aux secrets. Rotation immediate.
- **Compliance.** Certains standards (SOC2, ISO 27001) exigent une rotation periodique.
- **Hygiene.** Un secret de 2 ans est un vecteur d'attaque dormant.

## Quoi tourner et quand

| Secret | Frequence | Priorite |
|---|---|---|
| Tokens API tiers (Telegram, GitHub) | Tous les 3 mois | Haute |
| Mots de passe base de donnees | Tous les 3 mois | Haute |
| Cles JWT / session secrets | Tous les mois | Haute |
| Mots de passe SSH (si password auth) | Desactiver, utiliser les cles | Critique |
| Cles SSH | Annuel | Moyenne |
| Vault unseal keys | Annuel ou apres incident | Haute |
| Tokens de service internes | Tous les 3 mois | Moyenne |

## Comment tourner : la procedure

### Le workflow en 5 etapes

1. **Generer** le nouveau secret.
2. **Stocker** dans Vault.
3. **Deployer** : mettre a jour le service qui utilise le secret.
4. **Tester** : verifier que le service fonctionne avec le nouveau secret.
5. **Logger** : documenter la rotation.

### Exemple complet : rotation d'un token API

```bash
#!/bin/bash
# rotate-secret.sh — Rotation d'un secret
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

# 1. Generer le nouveau secret
NEW_SECRET=$(openssl rand -hex 32)
log "Nouveau secret genere pour ${SERVICE}/${KEY}"

# 2. Sauvegarder l'ancien dans Vault (version precedente)
OLD_SECRET=$(vault kv get -field="$KEY" "secret/$SERVICE" 2>/dev/null)
log "Ancien secret sauvegarde (Vault versioning)"

# 3. Stocker le nouveau dans Vault
vault kv put "secret/$SERVICE" "$KEY=$NEW_SECRET"
log "Nouveau secret stocke dans Vault"

# 4. Redemarrer le service
log "Redemarrage de $SERVICE..."
cd /opt/"$SERVICE" && docker compose restart
sleep 5

# 5. Tester
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

### Rotation du mot de passe PostgreSQL

```bash
# 1. Generer
NEW_PASS=$(openssl rand -base64 24)

# 2. Changer dans PostgreSQL
sudo -u postgres psql -c "ALTER USER oa_admin PASSWORD '$NEW_PASS';"

# 3. Stocker dans Vault
vault kv put secret/postgresql password="$NEW_PASS"

# 4. Mettre a jour la connection string dans les services
# (via variable d'environnement ou .env)

# 5. Redemarrer les services qui utilisent la DB
docker compose restart

# 6. Tester
psql -U oa_admin -d cockpit -c "SELECT 1;" && echo "OK" || echo "ERREUR"

# 7. Logger
echo "$(date) PostgreSQL password rotated" >> /var/log/secret-rotation.log
```

## Frequence et planification

### Calendrier type

```
1er de chaque mois :
  - Rotation des cles JWT / session secrets

1er de chaque trimestre (janvier, avril, juillet, octobre) :
  - Rotation tokens API tiers
  - Rotation mot de passe PostgreSQL
  - Rotation tokens de service internes

1er janvier :
  - Rotation cles SSH
  - Review des Vault unseal keys
```

### Automatiser le rappel

```bash
# Cron : rappel le 1er de chaque mois
0 9 1 * * echo "Rappel : rotation des secrets mensuelle" | /opt/scripts/send-telegram.sh
```

## Erreurs courantes

**Ne jamais tourner.** Le meme token depuis 2 ans. Si (quand) il fuit, la fenetre d'exploitation est de 2 ans.

**Tourner sans tester.** Vous changez le secret, le service ne demarre plus, et c'est samedi. Testez toujours immediatement apres.

**Pas de rollback.** Le nouveau secret ne marche pas et vous avez ecrase l'ancien. Vault garde les versions -- utilisez-les.

**Secret en dur dans le code.** La rotation ne sert a rien si le secret est aussi dans un fichier de config non gere par Vault. Auditez (section 4.13).

**Oublier un service.** Vous tournez le mot de passe PostgreSQL mais un deuxieme service utilise aussi ce mot de passe et il n'est pas mis a jour.

## Etapes

1. Listez tous les secrets de votre infrastructure.
2. Classez-les par frequence de rotation.
3. Creez un calendrier de rotation.
4. Ecrivez le workflow de rotation dans WORKFLOWS.md.
5. Faites la premiere rotation manuellement.
6. Automatisez avec un script et un cron de rappel.

## Verification

- [ ] Tous les secrets sont inventories avec leur date de derniere rotation.
- [ ] Un calendrier de rotation existe.
- [ ] Le script de rotation inclut un test et un rollback.
- [ ] Chaque rotation est loggee dans /var/log/secret-rotation.log.
- [ ] Aucun secret n'a plus de 3 mois sans rotation.
