---
---
status: complete
audience: both
chapter: 05
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: en
---

# 5.3 -- Backups

## Context

A backup that has never been tested is not a backup. It's hope. And hope is not a strategy.

What matters: appropriate frequency, separate storage, and regular restoration testing.

## What to back up

| Element | Method | Frequency |
|---|---|---|
| PostgreSQL database | pg_dump | Daily |
| Config files | tar/rsync | Weekly |
| Docker volumes | docker cp / tar | Weekly |
| Secrets (Vault) | vault operator raft snapshot | Weekly |
| Source code | Git (already backed up if pushed) | On each push |
| Complete VPS | Hetzner snapshot | Monthly |

## pg_dump: database backup

### Complete script: backup-db.sh

```bash
#!/bin/bash
# backup-db.sh — Daily PostgreSQL backup
# Usage: ./backup-db.sh

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

# Create directory if necessary
mkdir -p "$BACKUP_DIR"

# Backup
log "Starting backup of ${DB_NAME}"
if pg_dump -U "$DB_USER" "$DB_NAME" | gzip > "$BACKUP_FILE"; then
    SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
    log "OK — ${BACKUP_FILE} (${SIZE})"
else
    log "ERROR — pg_dump failed"
    exit 1
fi

# Verification: file is not empty
if [ ! -s "$BACKUP_FILE" ]; then
    log "ERROR — Backup file is empty"
    exit 1
fi

# Rotation: delete backups older than N days
DELETED=$(find "$BACKUP_DIR" -name "${DB_NAME}_*.sql.gz" -mtime +${RETENTION_DAYS} -delete -print | wc -l)
log "Rotation: ${DELETED} old backup(s) deleted"

log "Backup completed"
```

### Cron

```bash
# Daily backup at 2 AM
0 2 * * * /opt/scripts/backup-db.sh >> /var/log/backup.log 2>&1
```

## Critical files

### Script: backup-files.sh

```bash
#!/bin/bash
# backup-files.sh — Backup of configuration files
# Usage: ./backup-files.sh

BACKUP_DIR="/var/backups/files"
TIMESTAMP=$(date '+%Y%m%d_%H%M%S')
BACKUP_FILE="${BACKUP_DIR}/config_${TIMESTAMP}.tar.gz"
LOG_FILE="/var/log/backup.log"

mkdir -p "$BACKUP_DIR"

log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') [BACKUP-FILES] $1" | tee -a "$LOG_FILE"
}

log "Starting backup of files"

# List of files/folders to back up
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

# Create archive
tar -czf "$BACKUP_FILE" "${FILES[@]}" 2>/dev/null

if [ $? -eq 0 ]; then
    SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
    log "OK — ${BACKUP_FILE} (${SIZE})"
else
    log "ERROR — tar failed"
    exit 1
fi

# Rotation: keep 4 weeks
find "$BACKUP_DIR" -name "config_*.tar.gz" -mtime +28 -delete

log "File backup completed"
```

## Hetzner snapshots

Hetzner snapshots back up the complete VPS. It's the last resort.

```bash
# Via hcloud CLI
hcloud server create-image --type snapshot --description "Monthly snapshot $(date '+%Y-%m')" <server-id>

# List existing snapshots
hcloud image list --type snapshot

# Delete an old snapshot
hcloud image delete <image-id>
```

Frequency: monthly or before a risky operation (migration, major update).

Cost: Hetzner snapshots are charged per GB/month. A 40 GB VPS costs approximately 0.80 EUR/month per snapshot.

## RESTORATION testing

The most important test. Do it at least once a month.

### Test PostgreSQL restoration

```bash
# 1. Create a test database
createdb -U oa_admin cockpit_restore_test

# 2. Restore the latest backup
gunzip -c /var/backups/postgresql/cockpit_$(ls -t /var/backups/postgresql/ | head -1) | psql -U oa_admin cockpit_restore_test

# 3. Verify: count tables and rows
psql -U oa_admin cockpit_restore_test -c "\dt"
psql -U oa_admin cockpit_restore_test -c "SELECT 'tasks' AS tbl, COUNT(*) FROM tasks;"

# 4. Compare with production
psql -U oa_admin cockpit -c "SELECT 'tasks' AS tbl, COUNT(*) FROM tasks;"

# 5. Clean up
dropdb -U oa_admin cockpit_restore_test
```

### Test file restoration

```bash
# 1. Extract to a temporary folder
mkdir -p /tmp/restore_test
tar -xzf /var/backups/files/config_$(ls -t /var/backups/files/ | head -1) -C /tmp/restore_test

# 2. Verify that critical files are there
ls -la /tmp/restore_test/opt/cockpit/docker-compose.yml
ls -la /tmp/restore_test/opt/scripts/

# 3. Compare with current files
diff /opt/cockpit/docker-compose.yml /tmp/restore_test/opt/cockpit/docker-compose.yml

# 4. Clean up
rm -rf /tmp/restore_test
```

### Log the test

```bash
echo "$(date '+%Y-%m-%d') Restoration tested: DB OK, files OK" >> /var/log/backup-test.log
```

## Common errors

**Backup without testing.** You have .sql.gz files from 6 months ago. Never tested. When you need them, the file is corrupted or incomplete.

**Backup on the same disk.** The disk fails, and so do the backups. Store on a separate volume at minimum, ideally off the server (S3, another VPS).

**No rotation.** Backups accumulate and fill the disk. Maximum irony: the failure caused by the backups themselves.

**Backup without logging.** The cron runs but you don't know if it works. Log each execution and check the log once a week.

## Steps

1. Install `backup-db.sh` and `backup-files.sh` in `/opt/scripts/`.
2. Manually test both scripts.
3. Configure the crons.
4. Test restoration (DB + files).
5. Schedule a monthly restoration test.
6. Configure a monthly Hetzner snapshot.

## Verification

- [ ] backup-db.sh runs daily and produces non-empty files.
- [ ] backup-files.sh runs weekly.
- [ ] Rotation deletes old backups.
- [ ] A restoration test was performed in the last month.
- [ ] Backups are not on the same disk as the data.
- [ ] A monthly Hetzner snapshot is scheduled.

---
