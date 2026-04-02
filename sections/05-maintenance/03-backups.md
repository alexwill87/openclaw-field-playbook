---
status: complete
audience: both
chapter: 05
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 5.3 -- Backups

## Contexte

Un backup qui n'a jamais ete teste n'est pas un backup. C'est un espoir. Et l'espoir n'est pas une strategie.

Ce qui compte : frequence adaptee, stockage separe, et test de restauration regulier.

## Quoi sauvegarder

| Element | Methode | Frequence |
|---|---|---|
| Base PostgreSQL | pg_dump | Quotidien |
| Fichiers de config | tar/rsync | Hebdomadaire |
| Docker volumes | docker cp / tar | Hebdomadaire |
| Secrets (Vault) | vault operator raft snapshot | Hebdomadaire |
| Code source | Git (deja sauvegarde si pousse) | A chaque push |
| VPS complet | Snapshot Hetzner | Mensuel |

## pg_dump : backup de la base

### Script complet : backup-db.sh

```bash
#!/bin/bash
# backup-db.sh — Backup PostgreSQL quotidien
# Usage : ./backup-db.sh

BACKUP_DIR="/var/backups/postgresql"
DB_NAME="${DB_NAME:-cockpit}"
DB_USER="${DB_USER:-oa_admin}"
RETENTION_DAYS=14
TIMESTAMP=$(date '+%Y%m%d_%H%M%S')
BACKUP_FILE="${BACKUP_DIR}/${DB_NAME}_${TIMESTAMP}.sql.gz"
LOG_FILE="/var/log/backup.log"

log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') [BACKUP-DB] $1" | tee -a "$LOG_FILE"
}

# Creer le dossier si necessaire
mkdir -p "$BACKUP_DIR"

# Backup
log "Debut backup ${DB_NAME}"
if pg_dump -U "$DB_USER" "$DB_NAME" | gzip > "$BACKUP_FILE"; then
    SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
    log "OK — ${BACKUP_FILE} (${SIZE})"
else
    log "ERREUR — pg_dump a echoue"
    exit 1
fi

# Verification : le fichier n'est pas vide
if [ ! -s "$BACKUP_FILE" ]; then
    log "ERREUR — Le fichier backup est vide"
    exit 1
fi

# Rotation : supprimer les backups de plus de N jours
DELETED=$(find "$BACKUP_DIR" -name "${DB_NAME}_*.sql.gz" -mtime +${RETENTION_DAYS} -delete -print | wc -l)
log "Rotation : ${DELETED} ancien(s) backup(s) supprime(s)"

log "Backup termine"
```

### Cron

```bash
# Backup quotidien a 2h du matin
0 2 * * * /opt/scripts/backup-db.sh >> /var/log/backup.log 2>&1
```

## Fichiers critiques

### Script : backup-files.sh

```bash
#!/bin/bash
# backup-files.sh — Backup des fichiers de configuration
# Usage : ./backup-files.sh

BACKUP_DIR="/var/backups/files"
TIMESTAMP=$(date '+%Y%m%d_%H%M%S')
BACKUP_FILE="${BACKUP_DIR}/config_${TIMESTAMP}.tar.gz"
LOG_FILE="/var/log/backup.log"

mkdir -p "$BACKUP_DIR"

log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') [BACKUP-FILES] $1" | tee -a "$LOG_FILE"
}

log "Debut backup fichiers"

# Liste des fichiers/dossiers a sauvegarder
FILES=(
    "/opt/cockpit/docker-compose.yml"
    "/opt/cockpit/.env"
    "/opt/scripts/"
    "/etc/nginx/sites-available/"
    "/etc/docker/daemon.json"
    "$HOME/.claude/"
    "$HOME/CONSTITUTION.md"
    "$HOME/BOUNDARIES.md"
    "$HOME/WORKFLOWS.md"
)

# Creer l'archive
tar -czf "$BACKUP_FILE" "${FILES[@]}" 2>/dev/null

if [ $? -eq 0 ]; then
    SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
    log "OK — ${BACKUP_FILE} (${SIZE})"
else
    log "ERREUR — tar a echoue"
    exit 1
fi

# Rotation : garder 4 semaines
find "$BACKUP_DIR" -name "config_*.tar.gz" -mtime +28 -delete

log "Backup fichiers termine"
```

## Snapshots Hetzner

Les snapshots Hetzner sauvegardent le VPS complet. C'est le dernier recours.

```bash
# Via hcloud CLI
hcloud server create-image --type snapshot --description "Snapshot mensuel $(date '+%Y-%m')" <server-id>

# Lister les snapshots existants
hcloud image list --type snapshot

# Supprimer un vieux snapshot
hcloud image delete <image-id>
```

Frequence : mensuelle ou avant une operation risquee (migration, mise a jour majeure).

Cout : les snapshots Hetzner sont factures au Go/mois. Un VPS de 40 Go = environ 0.80 EUR/mois par snapshot.

## TEST de restauration

Le test le plus important. Faites-le au moins une fois par mois.

### Tester la restauration PostgreSQL

```bash
# 1. Creer une base de test
createdb -U oa_admin cockpit_restore_test

# 2. Restaurer le dernier backup
gunzip -c /var/backups/postgresql/cockpit_$(ls -t /var/backups/postgresql/ | head -1) | psql -U oa_admin cockpit_restore_test

# 3. Verifier : compter les tables et les lignes
psql -U oa_admin cockpit_restore_test -c "\dt"
psql -U oa_admin cockpit_restore_test -c "SELECT 'tasks' AS tbl, COUNT(*) FROM tasks;"

# 4. Comparer avec la production
psql -U oa_admin cockpit -c "SELECT 'tasks' AS tbl, COUNT(*) FROM tasks;"

# 5. Nettoyer
dropdb -U oa_admin cockpit_restore_test
```

### Tester la restauration des fichiers

```bash
# 1. Extraire dans un dossier temporaire
mkdir -p /tmp/restore_test
tar -xzf /var/backups/files/config_$(ls -t /var/backups/files/ | head -1) -C /tmp/restore_test

# 2. Verifier que les fichiers critiques sont la
ls -la /tmp/restore_test/opt/cockpit/docker-compose.yml
ls -la /tmp/restore_test/opt/scripts/

# 3. Comparer avec les fichiers actuels
diff /opt/cockpit/docker-compose.yml /tmp/restore_test/opt/cockpit/docker-compose.yml

# 4. Nettoyer
rm -rf /tmp/restore_test
```

### Logger le test

```bash
echo "$(date '+%Y-%m-%d') Restauration testee : DB OK, fichiers OK" >> /var/log/backup-test.log
```

## Erreurs courantes

**Backup sans test.** Vous avez des fichiers .sql.gz depuis 6 mois. Jamais testes. Le jour ou vous en avez besoin, le fichier est corrompu ou incomplet.

**Backup sur le meme disque.** Le disque tombe, les backups aussi. Stockez au minimum sur un volume separe, idealement hors du serveur (S3, autre VPS).

**Pas de rotation.** Les backups s'accumulent et remplissent le disque. Ironie maximale : la panne causee par les backups.

**Backup sans log.** Le cron tourne mais vous ne savez pas si ca marche. Loggez chaque execution et verifiez le log une fois par semaine.

## Etapes

1. Installez `backup-db.sh` et `backup-files.sh` dans `/opt/scripts/`.
2. Testez manuellement les deux scripts.
3. Configurez les crons.
4. Testez la restauration (DB + fichiers).
5. Planifiez un test de restauration mensuel.
6. Configurez un snapshot Hetzner mensuel.

## Verification

- [ ] backup-db.sh tourne quotidiennement et produit des fichiers non-vides.
- [ ] backup-files.sh tourne hebdomadairement.
- [ ] La rotation supprime les vieux backups.
- [ ] Un test de restauration a ete fait dans le dernier mois.
- [ ] Les backups ne sont pas sur le meme disque que les donnees.
- [ ] Un snapshot Hetzner mensuel est planifie.
