---
---
status: complete
audience: both
chapter: 02
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: en
---

# 2.2 -- Securing the VPS

## Context

A new VPS is exposed to the Internet with root access via password. It's an easy target. This section hardens the server BEFORE installing anything. Each command must be executed in order.

## Step 1: First root connection

From your local machine:

```bash
$ ssh root@YOUR_VPS_IP
```

Accept the SSH fingerprint if this is your first connection.

## Step 2: Update the system

```bash
# apt update && apt upgrade -y
# apt install -y curl wget git ufw fail2ban unattended-upgrades
```

## Step 3: Create a non-root user

NEVER work as root on a daily basis. Create a dedicated user:

```bash
# adduser deploy
```

Answer the prompts (strong password, the rest can be empty).

Grant sudo privileges:

```bash
# usermod -aG sudo deploy
```

## Step 4: Configure SSH key authentication

On your LOCAL machine (not the VPS), generate a key if you don't have one:

```bash
$ ssh-keygen -t ed25519 -C "your-email@example.com"
```

Copy the public key to the VPS:

```bash
$ ssh-copy-id deploy@YOUR_VPS_IP
```

Test the connection without a password:

```bash
$ ssh deploy@YOUR_VPS_IP
```

If it works, move to the next step. If not, do NOT disable password authentication.

## Step 5: Disable password authentication

**IMPORTANT**: Only do this step if SSH key connection works. Otherwise you will be locked out of the server.

Edit the SSH configuration:

```bash
$ sudo nano /etc/ssh/sshd_config
```

Modify (or add) these lines:

```
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
```

Restart SSH:

```bash
$ sudo systemctl restart sshd
```

**Keep your current session open** and test in a NEW terminal:

```bash
$ ssh deploy@YOUR_VPS_IP
```

## Step 6: Configure the UFW firewall

Default policy: block all incoming, allow all outgoing.

```bash
$ sudo ufw default deny incoming
$ sudo ufw default allow outgoing
```

Allow SSH (otherwise you lose access):

```bash
$ sudo ufw allow ssh
```

Enable the firewall:

```bash
$ sudo ufw enable
```

Check the status:

```bash
$ sudo ufw status verbose
```

Expected result:

```
Status: active

To                         Action      From
--                         ------      ----
22/tcp                     ALLOW IN    Anywhere
```

**IMPORTANT**: Do NOT open any other ports. All services (Vault, PostgreSQL, OpenClaw) will be accessible only via Tailscale, not via the public IP.

## Step 7: Configure fail2ban

fail2ban blocks IPs that attempt too many SSH connections:

```bash
$ sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
$ sudo nano /etc/fail2ban/jail.local
```

Find the `[sshd]` section and make sure it contains:

```ini
[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
bantime = 3600
findtime = 600
```

Restart fail2ban:

```bash
$ sudo systemctl restart fail2ban
$ sudo systemctl enable fail2ban
```

## Step 8: Automatic security updates

```bash
$ sudo dpkg-reconfigure -plow unattended-upgrades
```

Select "Yes" to enable automatic updates.

Verify the configuration:

```bash
$ cat /etc/apt/apt.conf.d/20auto-upgrades
```

Expected result:

```
APT::Periodic::Update-Package-Lists "1";
APT::Periodic::Unattended-Upgrade "1";
```

## Step 9: Configure the timezone

```bash
$ sudo timedatectl set-timezone Europe/Paris
$ timedatectl
```

## Common errors

- **Locking yourself out of the server**: Always test SSH key connection BEFORE disabling password authentication. Keep a session open during SSH changes.
- **Forgetting to allow SSH in UFW before enabling it**: You lose access. Most providers offer a rescue VNC console.
- **Not installing fail2ban**: Bots scan continuously. Without fail2ban, you'll see thousands of login attempts per day.

## Verification

```bash
$ sudo ufw status
$ sudo systemctl status fail2ban
$ sudo systemctl status sshd
$ cat /etc/ssh/sshd_config | grep -E "PermitRoot|PasswordAuth"
```

Expected results:
- UFW active, only port 22 open
- fail2ban active
- sshd active
- PermitRootLogin no, PasswordAuthentication no

## Estimated time

20 minutes.
