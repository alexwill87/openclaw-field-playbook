---
status: complete
audience: both
chapter: 02
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 2.8 -- PostgreSQL

## Contexte

PostgreSQL stocke les donnees persistantes du systeme : sessions, historique des agents, metriques, etats. On le fait tourner dans Docker pour l'isolation et la portabilite. Le mot de passe sera stocke dans Vault (section precedente).

## Etape 1 : Recuperer le mot de passe depuis Vault

Si vous avez suivi la section 07, le mot de passe est deja dans Vault :

```bash
$ docker exec vault vault kv get -field=password secret/database
```

Notez ce mot de passe pour l'utiliser dans le docker-compose.

## Etape 2 : Creer le fichier Docker Compose

Creez `~/docker/postgres/docker-compose.yml` :

```yaml
version: "3.8"

services:
  postgres:
    image: postgres:16-alpine
    container_name: postgres
    restart: unless-stopped
    ports:
      - "127.0.0.1:5432:5432"
    env_file:
      - .env
    environment:
      PGDATA: /var/lib/postgresql/data/pgdata
    volumes:
      - ./data:/var/lib/postgresql/data
    shm_size: 256mb
    networks:
      - postgres-net

networks:
  postgres-net:
    driver: bridge
```

Creez le fichier `.env` avec les identifiants (ne jamais le committer dans git) :

```bash
$ cat > ~/docker/postgres/.env << 'EOF'
POSTGRES_USER=oa_admin
POSTGRES_PASSWORD=VOTRE_MOT_DE_PASSE_FORT
POSTGRES_DB=oa_system
EOF
$ chmod 600 ~/docker/postgres/.env
```

> **SECURITE :** Le fichier `.env` contient le mot de passe en clair. Protegez-le (`chmod 600`) et ajoutez `.env` a votre `.gitignore`. Idealement, recuperez le mot de passe depuis Vault : `vault kv get -field=password secret/database > ~/docker/postgres/.env`

## Etape 3 : Demarrer PostgreSQL

```bash
$ cd ~/docker/postgres
$ docker compose up -d
```

Verifiez :

```bash
$ docker ps | grep postgres
```

## Etape 4 : Tester la connexion

```bash
$ docker exec -it postgres psql -U oa_admin -d oa_system -c "SELECT version();"
```

Resultat attendu : version PostgreSQL 16.x.

## Etape 5 : Creer les tables initiales (si necessaire)

OpenClaw creera ses propres tables au premier lancement. Mais vous pouvez verifier que la base est vide et prete :

```bash
$ docker exec -it postgres psql -U oa_admin -d oa_system -c "\dt"
```

Resultat attendu : "Did not find any relations." (normal, la base est vide).

## Etape 6 : Configurer la sauvegarde automatique

Creez le script de backup `~/scripts/backup-postgres.sh` :

```bash
#!/bin/bash
# Sauvegarde quotidienne PostgreSQL
# A mettre dans cron : 0 3 * * * /home/deploy/scripts/backup-postgres.sh

BACKUP_DIR="$HOME/backups/postgres"
DATE=$(date +%Y%m%d_%H%M%S)
FILENAME="oa_system_${DATE}.sql.gz"

# Dump compresse
docker exec postgres pg_dump -U oa_admin oa_system | gzip > "${BACKUP_DIR}/${FILENAME}"

# Garder les 7 derniers jours
find "${BACKUP_DIR}" -name "*.sql.gz" -mtime +7 -delete

echo "[$(date)] Backup termine : ${FILENAME}"
```

Rendez-le executable :

```bash
$ chmod +x ~/scripts/backup-postgres.sh
```

Testez :

```bash
$ ~/scripts/backup-postgres.sh
$ ls -la ~/backups/postgres/
```

## Etape 7 : Ajouter au cron

```bash
$ crontab -e
```

Ajoutez cette ligne (backup tous les jours a 3h du matin) :

```
0 3 * * * /home/deploy/scripts/backup-postgres.sh >> /home/deploy/logs/backup-postgres.log 2>&1
```

## Erreurs courantes

- **"password authentication failed"** : Le mot de passe dans docker-compose.yml ne correspond pas a celui stocke dans Vault. Alignez les deux.
- **"port 5432 already in use"** : Un PostgreSQL tourne deja (installe via apt ?). Arretez-le : `sudo systemctl stop postgresql && sudo systemctl disable postgresql`.
- **Donnees perdues apres recreation du conteneur** : Le volume `./data` persiste les donnees. Ne supprimez pas ce dossier. Si vous faites `docker compose down -v`, les volumes sont supprimes.
- **Permissions sur le dossier data** : Si PostgreSQL ne demarre pas, verifiez : `ls -la ~/docker/postgres/data/`. Le dossier doit etre accessible.

## Verification

```bash
$ docker ps | grep postgres
$ docker exec -it postgres psql -U oa_admin -d oa_system -c "SELECT 1;"
$ ls ~/backups/postgres/
```

Resultats attendus :
- Conteneur postgres en etat "Up"
- La requete retourne 1
- Au moins un fichier de backup present (si le test a ete lance)

## Temps estime

15 minutes.
