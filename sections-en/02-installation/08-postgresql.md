---
---
status: complete
audience: both
chapter: 02
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: en
---

# 2.8 -- PostgreSQL

## Context

PostgreSQL stores the system's persistent data: sessions, agent history, metrics, states. We run it in Docker for isolation and portability. The password will be stored in Vault (previous section).

## Step 1: Retrieve the password from Vault

If you followed section 07, the password is already in Vault:

```bash
$ docker exec vault vault kv get -field=password secret/database
```

Note this password to use in the docker-compose.

## Step 2: Create the Docker Compose file

Create `~/docker/postgres/docker-compose.yml`:

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

Create the `.env` file with credentials (never commit this to git):

```bash
$ cat > ~/docker/postgres/.env << 'EOF'
POSTGRES_USER=oa_admin
POSTGRES_PASSWORD=YOUR_STRONG_PASSWORD
POSTGRES_DB=oa_system
EOF
$ chmod 600 ~/docker/postgres/.env
```

> **SECURITY:** The `.env` file contains the password in plaintext. Protect it (`chmod 600`) and add `.env` to your `.gitignore`. Ideally, retrieve the password from Vault: `vault kv get -field=password secret/database > ~/docker/postgres/.env`

## Step 3: Start PostgreSQL

```bash
$ cd ~/docker/postgres
$ docker compose up -d
```

Verify:

```bash
$ docker ps | grep postgres
```

## Step 4: Test the connection

```bash
$ docker exec -it postgres psql -U oa_admin -d oa_system -c "SELECT version();"
```

Expected result: PostgreSQL version 16.x.

## Step 5: Create initial tables (if necessary)

OpenClaw will create its own tables on first launch. But you can verify that the database is empty and ready:

```bash
$ docker exec -it postgres psql -U oa_admin -d oa_system -c "\dt"
```

Expected result: "Did not find any relations." (normal, the database is empty).

## Step 6: Configure automatic backups

Create the backup script `~/scripts/backup-postgres.sh`:

```bash
#!/bin/bash
# Daily PostgreSQL backup
# Add to cron: 0 3 * * * /home/deploy/scripts/backup-postgres.sh

BACKUP_DIR="$HOME/backups/postgres"
DATE=$(date +%Y%m%d_%H%M%S)
FILENAME="oa_system_${DATE}.sql.gz"

# Compressed dump
docker exec postgres pg_dump -U oa_admin oa_system | gzip > "${BACKUP_DIR}/${FILENAME}"

# Keep the last 7 days
find "${BACKUP_DIR}" -name "*.sql.gz" -mtime +7 -delete

echo "[$(date)] Backup complete: ${FILENAME}"
```

Make it executable:

```bash
$ chmod +x ~/scripts/backup-postgres.sh
```

Test it:

```bash
$ ~/scripts/backup-postgres.sh
$ ls -la ~/backups/postgres/
```

## Step 7: Add to cron

```bash
$ crontab -e
```

Add this line (backup every day at 3 AM):

```
0 3 * * * /home/deploy/scripts/backup-postgres.sh >> /home/deploy/logs/backup-postgres.log 2>&1
```

## Common errors

- **"password authentication failed"**: The password in docker-compose.yml does not match the one stored in Vault. Align the two.
- **"port 5432 already in use"**: PostgreSQL is already running (installed via apt?). Stop it: `sudo systemctl stop postgresql && sudo systemctl disable postgresql`.
- **Data lost after container recreation**: The `./data` volume persists the data. Do not delete this folder. If you run `docker compose down -v`, the volumes are deleted.
- **Permissions on the data folder**: If PostgreSQL does not start, verify: `ls -la ~/docker/postgres/data/`. The folder must be accessible.

## Verification

```bash
$ docker ps | grep postgres
$ docker exec -it postgres psql -U oa_admin -d oa_system -c "SELECT 1;"
$ ls ~/backups/postgres/
```

Expected results:
- postgres container in "Up" state
- The query returns 1
- At least one backup file present (if the test was run)

## Estimated time

15 minutes.
