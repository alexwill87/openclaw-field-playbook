---
---
status: complete
audience: both
chapter: 02
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: en
---

# 2.15 -- Gateway systemd

## Context

The OpenClaw gateway is the HTTP entry point of the system. It must run continuously, restart automatically in case of crash, and start at server boot. systemd is the standard Linux service manager — it handles this.

## Step 0: Check for old services (CRITICAL)

Before creating a new service, verify that there is no old OpenClaw service that could conflict:

```bash
$ systemctl --user list-units --all | grep openclaw
$ sudo systemctl list-units --all | grep openclaw
```

If an old service exists (for example `openclaw.service`, `openclaw-gateway.service` from a previous installation), disable and remove it:

```bash
# For a user service:
$ systemctl --user stop openclaw-gateway
$ systemctl --user disable openclaw-gateway
$ rm ~/.config/systemd/user/openclaw-gateway.service
$ systemctl --user daemon-reload

# For a system service:
$ sudo systemctl stop openclaw-gateway
$ sudo systemctl disable openclaw-gateway
$ sudo rm /etc/systemd/system/openclaw-gateway.service
$ sudo systemctl daemon-reload
```

> **Why?** Two systemd services with the same name or pointing to the same binary will fight over the same port. The symptom: the gateway crashes in a loop with "EADDRINUSE" or "port already in use". This problem is very difficult to diagnose if you don't think to check for old services.

## Step 1: Create the service file

Create `/etc/systemd/system/openclaw-gateway.service`:

```bash
$ sudo nano /etc/systemd/system/openclaw-gateway.service
```

Content:

First, find your exact paths:

```bash
$ which node
$ which openclaw
```

Note the results. Then create the environment file for secrets:

```bash
$ sudo mkdir -p /etc/openclaw
$ sudo tee /etc/openclaw/gateway.env > /dev/null << 'EOF'
VAULT_ADDR=http://127.0.0.1:8200
VAULT_TOKEN=YOUR_APPLICATION_TOKEN_HERE
EOF
$ sudo chmod 600 /etc/openclaw/gateway.env
$ sudo chown YOUR_USER:YOUR_USER /etc/openclaw/gateway.env
```

> **SECURITY:** The Vault token must NEVER appear in plain text in the systemd file. Use `EnvironmentFile` to load it from a protected file (chmod 600). The file must be owned by the user who executes the service (YOUR_USER), otherwise systemd will not be able to read it and the service will fail silently with empty environment variables.

Create the service file by replacing `YOUR_USER` and paths with your values:

```ini
[Unit]
Description=OpenClaw Gateway
Documentation=https://github.com/alexwill87/openclawfieldplaybook
After=network.target docker.service
Wants=docker.service

[Service]
Type=simple
User=YOUR_USER
Group=YOUR_USER
WorkingDirectory=/home/YOUR_USER
Environment=NODE_ENV=production
EnvironmentFile=/etc/openclaw/gateway.env

ExecStart=/home/YOUR_USER/scripts/openclaw-gateway.sh
ExecReload=/bin/kill -HUP $MAINPID
ExecStop=/bin/kill -TERM $MAINPID

Restart=always
RestartSec=10
StartLimitIntervalSec=300
StartLimitBurst=5

StandardOutput=journal
StandardError=journal
SyslogIdentifier=openclaw-gateway

# Security
NoNewPrivileges=true
ProtectSystem=strict
ReadWritePaths=/home/YOUR_USER

[Install]
WantedBy=multi-user.target
```

Create the wrapper script that loads nvm correctly (systemd does not load `.bashrc`):

```bash
$ cat > ~/scripts/openclaw-gateway.sh << 'SCRIPT'
#!/bin/bash
# Load nvm if present, otherwise use global node
if [ -f "$HOME/.nvm/nvm.sh" ]; then
  export NVM_DIR="$HOME/.nvm"
  source "$NVM_DIR/nvm.sh"
fi
exec openclaw gateway start
SCRIPT
$ chmod +x ~/scripts/openclaw-gateway.sh
```

> **Why this detection?** If nvm is not installed (for example if node was installed via apt or another package manager), the script will crash on the `source` of a non-existent file. With this detection, the script works in both cases.

**IMPORTANT**: Replace the placeholders in the service file:
- `YOUR_USER`: your username (result of `whoami`)
- The Vault token in `/etc/openclaw/gateway.env`: the one created in section 07

> **PM2 or systemd?** If you already use PM2 for other Node.js services, use PM2. Otherwise, systemd is recommended because it is native to Ubuntu and does not require additional dependencies. Do not mix the two for the same service.

## Step 2: Enable and start the service

```bash
$ sudo systemctl daemon-reload
$ sudo systemctl enable openclaw-gateway
$ sudo systemctl start openclaw-gateway
```

## Step 3: Check the status

```bash
$ sudo systemctl status openclaw-gateway
```

Expected result:

```
openclaw-gateway.service - OpenClaw Gateway
     Loaded: loaded (/etc/systemd/system/openclaw-gateway.service; enabled)
     Active: active (running) since ...
```

## Step 4: View the logs

Real-time logs:

```bash
$ journalctl -u openclaw-gateway -f
```

Logs since last boot:

```bash
$ journalctl -u openclaw-gateway -b
```

Logs from the last 100 lines:

```bash
$ journalctl -u openclaw-gateway -n 100 --no-pager
```

## Step 5: Common management commands

| Action | Command |
|--------|---------|
| Start | `sudo systemctl start openclaw-gateway` |
| Stop | `sudo systemctl stop openclaw-gateway` |
| Restart | `sudo systemctl restart openclaw-gateway` |
| Reload config | `sudo systemctl reload openclaw-gateway` |
| Status | `sudo systemctl status openclaw-gateway` |
| Disable at boot | `sudo systemctl disable openclaw-gateway` |
| View logs | `journalctl -u openclaw-gateway -f` |

## Automatic restart behavior

The configuration provides:
- `Restart=always`: restarts after any stop (crash, kill, etc.)
- `RestartSec=10`: waits 10 seconds before restarting
- `StartLimitBurst=5` and `StartLimitIntervalSec=300`: maximum 5 restarts in 5 minutes. Beyond that, systemd considers the service as failing and stops attempts.

To reset the attempt counter:

```bash
$ sudo systemctl reset-failed openclaw-gateway
$ sudo systemctl start openclaw-gateway
```

## Common errors

- **"openclaw: command not found"** in logs: systemd does not load `.bashrc`. You must use the ABSOLUTE path to node and openclaw. No `nvm`, no `~`.
- **Permission denied**: The user in the service file does not have access to the folder. Check `User=` and `ReadWritePaths=`.
- **Service looping (restart loop)**: Check the logs (`journalctl`). Often a problem with Vault token or database connection.
- **"Start request repeated too quickly"**: The service crashed 5 times in 5 minutes. Fix the underlying problem, then `systemctl reset-failed`.

## Verification

```bash
$ sudo systemctl status openclaw-gateway
$ curl -s http://127.0.0.1:3000/health
$ journalctl -u openclaw-gateway -n 10 --no-pager
```

Expected results:
- Status: active (running)
- Health endpoint returns a 200 response
- No errors in the last 10 lines of log

## Estimated time

10 minutes.
