---
status: complete
audience: both
chapter: 05
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: en
---

# 5.2 -- Log Management

## Context

Logs are your black box. When everything works, nobody looks at them. When something breaks, it's the first thing you open. If you don't know where they are and how to read them, you waste time at the worst possible moment.

## Where are the logs

### System logs (journalctl)

```bash
# All logs since last boot
journalctl -b

# Logs for a specific service
journalctl -u postgresql
journalctl -u docker

# Logs from the last 30 minutes
journalctl --since "30 min ago"

# Logs from today
journalctl --since today

# Follow in real time
journalctl -f

# Filter by priority (errors and above)
journalctl -p err
```

### Docker logs

```bash
# Logs from a container
docker logs cockpit

# Last 50 lines
docker logs cockpit --tail 50

# Follow in real time
docker logs cockpit -f

# Since a specific date
docker logs cockpit --since "2026-04-01T10:00:00"

# All containers with recent logs
for c in $(docker ps --format "{{.Names}}"); do
    echo "=== $c ==="
    docker logs "$c" --tail 5 2>&1
    echo ""
done
```

### Application logs

Depending on your stack:

| Application | Typical location |
|---|---|
| Node.js | stdout (captured by Docker) or `/var/log/app/` |
| PostgreSQL | `/var/log/postgresql/` or journalctl |
| Nginx | `/var/log/nginx/access.log`, `/var/log/nginx/error.log` |
| Vault | journalctl -u vault |
| Custom scripts | `/var/log/` (or wherever you directed them) |
| Health check | `/var/log/health-check.log` |

### Agent session logs

If your agent has a session log:

```bash
# Claude Code sessions
ls ~/.claude/sessions/

# Command execution history
cat ~/.bash_history | tail -50
```

## How to read logs

### The reflex: end of file first

The most recent logs are the most useful. Always start from the end:

```bash
# Last 100 lines
tail -100 /var/log/nginx/error.log

# Or with journalctl
journalctl -u postgresql -n 100
```

### Filter the noise

```bash
# Look for errors
journalctl -p err --since today

# Grep on a pattern
docker logs cockpit 2>&1 | grep -i "error\|fail\|exception"

# Exclude known noise
docker logs cockpit 2>&1 | grep -iv "healthcheck\|GET /favicon"
```

### Correlate by timestamp

When a problem occurs, note the time. Then search all logs around that time:

```bash
# All system logs around 14:30
journalctl --since "14:25" --until "14:35"

# Docker logs around the same time
docker logs cockpit --since "2026-04-01T14:25:00" --until "2026-04-01T14:35:00"
```

## Log rotation

Logs grow indefinitely if you don't manage them. A full disk because of logs is a preventable outage.

### journalctl (systemd)

```bash
# Current size of system logs
journalctl --disk-usage

# Keep only the last 7 days
sudo journalctl --vacuum-time=7d

# Limit to 500M
sudo journalctl --vacuum-size=500M

# Permanent configuration in /etc/systemd/journald.conf
# SystemMaxUse=500M
# MaxRetentionSec=7d
```

### Docker

```bash
# Configure rotation in /etc/docker/daemon.json
{
    "log-driver": "json-file",
    "log-opts": {
        "max-size": "10m",
        "max-file": "3"
    }
}

# Then restart Docker
sudo systemctl restart docker
```

### Logrotate (standard files)

```bash
# Create /etc/logrotate.d/openclaw
/var/log/health-check.log
/var/log/backup.log
{
    daily
    rotate 14
    compress
    delaycompress
    missingok
    notifempty
}
```

## What to monitor

Don't monitor everything. Monitor what signals a problem:

| Signal | Where to find it | Action |
|---|---|---|
| "OOM" or "Out of memory" | journalctl, docker logs | Increase memory or optimize |
| "Connection refused" | Docker logs | Service down, restart it |
| "Disk full" | journalctl | Clean up logs, temp files |
| "SSL certificate expired" | Nginx error log | Renew the certificate |
| "Too many connections" | PostgreSQL logs | Increase max_connections or fix connection leak |
| "Permission denied" | Any log | Check user permissions |
| Spikes in 5xx errors | Nginx access log | Investigate the backend service |

## Common mistakes

**Never looking at logs.** You only open them when something is broken. At that point, you don't know how to read them and you waste time.

**No rotation.** Logs fill the disk. The server crashes. The irony: it's the easiest outage to prevent.

**Too many logs.** Debug mode is enabled in production. Every request generates 50 lines. The signal is drowned in noise. Use INFO level in production, DEBUG only to diagnose.

**Logs without timestamps.** Your scripts write logs without dates. Impossible to correlate with other logs. Always: `echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] message"`.

## Steps

1. Identify where your logs are (journalctl, Docker, files).
2. Configure rotation (journald.conf, daemon.json, logrotate).
3. Test that you know how to find an error: simulate a problem, find it in the logs.
4. Add timestamps to your scripts if not already done.
5. Define the 5 signals to monitor for your setup.

## Verification

- [ ] You know where to find logs for each component.
- [ ] Rotation is configured for all logs.
- [ ] Total log size is known (`journalctl --disk-usage`, `du -sh /var/log`).
- [ ] You know how to filter logs by error and timestamp.
- [ ] Debug mode is disabled in production.
