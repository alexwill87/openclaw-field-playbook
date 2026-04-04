---
---
status: complete
audience: both
chapter: 02
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: en
---

# 2.3 -- Tailscale Private Network

## Context

Tailscale creates a private network (VPN mesh) between your machines. Each machine receives a private IP (in the 100.x.x.x range). The fundamental principle: **no service is exposed on the VPS's public IP**. Vault, PostgreSQL, OpenClaw -- everything goes through Tailscale.

Advantages:
- Zero complex network configuration
- End-to-end encryption (WireGuard)
- Works even behind NAT
- Free up to 100 machines

## Step 1: Install Tailscale on the VPS

```bash
$ curl -fsSL https://tailscale.com/install.sh | sh
```

## Step 2: Start and Authenticate

```bash
$ sudo tailscale up
```

This command displays an authentication link. Open this link in your browser and sign in with your Tailscale account.

## Step 3: Get Your Tailscale IP

```bash
$ tailscale ip -4
```

Note this IP (format 100.x.x.x). This is the address you'll use for all services.

## Step 4: Verify the Connection

```bash
$ tailscale status
```

You should see your VPS in the list of connected machines.

## Step 5: Install Tailscale on Your Local Machine

Install Tailscale on your workstation as well:
- **Mac**: `brew install tailscale` or from the Mac App Store
- **Linux**: `curl -fsSL https://tailscale.com/install.sh | sh`
- **Windows**: Download from tailscale.com

Then `tailscale up` and authenticate.

## Step 6: Test Connectivity

From your local machine:

```bash
$ ping YOUR_VPS_TAILSCALE_IP
$ ssh deploy@YOUR_VPS_TAILSCALE_IP
```

From now on, always use the Tailscale IP to connect to the VPS, not the public IP.

## Step 7 (Optional): Disable SSH on the Public IP

If you're confident that Tailscale is working, you can restrict SSH to Tailscale only:

```bash
$ sudo ufw delete allow ssh
$ sudo ufw allow in on tailscale0 to any port 22
```

**IMPORTANT**: Only do this if you've confirmed that SSH via Tailscale works. Keep your provider's VNC console as a backup plan.

## Architecture Principle

From this step forward, the rule is:

```
Public IP: NOTHING exposed (except SSH if necessary)
Tailscale IP: EVERYTHING goes through here
```

PostgreSQL listens on 100.x.x.x:5432, not on 0.0.0.0.
Vault listens on 100.x.x.x:8200, not on 0.0.0.0.
The OpenClaw gateway listens on 100.x.x.x:3000, not on 0.0.0.0.

## Common Mistakes

- **Forgetting to install Tailscale on your local machine**: Without Tailscale on both sides, there's no private network.
- **Using the public IP for services**: The whole point of Tailscale is to avoid this. If a service listens on 0.0.0.0, fix it to listen on the Tailscale IP only.
- **Tailscale disconnecting**: Add `--ssh` to `tailscale up` to maintain the connection, and enable autostart: `sudo systemctl enable tailscaled`.

## Verification

```bash
$ tailscale status
$ tailscale ip -4
$ ping -c 3 $(tailscale ip -4)
```

Expected results:
- Status shows the machine as "active"
- IP in the 100.x.x.x range
- Ping responds without packet loss

## Estimated Time

10 minutes.
