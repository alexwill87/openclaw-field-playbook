---
---
status: complete
audience: both
chapter: 03
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit, claude-aurel]
lang: en
---

# 3.18 -- Connect Two OpenClaw Installations (Remote Mode)

> You have two VPS with OpenClaw, or you manage a client's installation. Here's how to connect them to monitor, debug, or collaborate remotely.

**For whom:** integrator, multi-site teams, or agent supervising another agent
**Prerequisites:** two functional OpenClaw installations, ideally on the same Tailscale network
**Difficulty:** Intermediate

---

## Context

OpenClaw supports a `gateway.mode: "remote"` mode that allows a client to connect to a remote gateway via WebSocket. It's a client-server architecture, not a federation: one VPS is the master (it hosts the gateway), the other is the client (it connects remotely).

### When to Connect Two Installations

| Use Case | Example |
|----------|---------|
| **Learning** | Observe how a more mature agent works on another VPS |
| **Debugging** | Diagnose a problem remotely without SSH access |
| **Supervision** | A central VPS monitors the health of multiple installations |
| **Inter-agent Collaboration** | Two agents on separate VPS share a communication channel |

---

## Architecture

```
VPS A (master gateway)              VPS B (remote client)
   gateway.mode: "server"              gateway.mode: "remote"
   port 18789 (WebSocket)              gateway.remote.url
          ^                                    |
          |_________ Tailscale / SSH __________|
```

The remote client does NOT launch its own gateway. It connects to the master's gateway and uses its CLI commands remotely.

---

## Steps

### 1. Master Gateway Side (VPS A)

Create a dedicated authentication token for the remote connection. **Never** reuse the root token.

```bash
# Generate a dedicated token
openclaw gateway token create --name "remote-vps-b" --scope read
```

Note the generated token. Verify that the gateway is listening on the correct port:

```bash
# Verify the configuration
cat ~/.openclaw/gateway.json
```

The configuration should include:

```json
{
  "mode": "server",
  "port": 18789,
  "auth": {
    "tokens": [
      {
        "name": "remote-vps-b",
        "token": "ocgw_xxxxxxxxxxxxxxxxxx",
        "scope": "read"
      }
    ]
  }
}
```

### 2. Transport Configuration

Three options, from simplest to most complex:

#### Option A: Direct Tailscale (Recommended)

If both VPS are on the same Tailscale network, this is the simplest. Traffic is already encrypted point-to-point.

```bash
# On VPS B, verify connectivity
tailscale ping vps-a
```

The remote URL will be: `ws://100.x.x.x:18789` (Tailscale IP of VPS A).

#### Option B: SSH Tunnel

If you don't have Tailscale, an SSH tunnel does the job:

```bash
# On VPS B, create the tunnel
ssh -N -L 18789:localhost:18789 user@vps-a-ip
```

The remote URL will be: `ws://localhost:18789`.

To make the tunnel persistent, add it to a systemd service or use `autossh`:

```bash
# Install autossh
sudo apt install autossh

# Persistent tunnel
autossh -M 0 -N -L 18789:localhost:18789 user@vps-a-ip \
  -o "ServerAliveInterval 30" -o "ServerAliveCountMax 3"
```

#### Option C: WebSocket over Internet (Advanced)

If you need to pass through the Internet without a tunnel, **always** use TLS:

```bash
# Behind a reverse proxy (Caddy, Nginx) with TLS certificate
# The URL will be: wss://gateway.your-domain.com
```

Never expose `ws://` on a public IP without TLS.

### 3. Remote Client Side (VPS B)

Configure the client to connect to the remote gateway:

```bash
# Edit the configuration
nano ~/.openclaw/gateway.json
```

```json
{
  "mode": "remote",
  "remote": {
    "url": "ws://100.x.x.x:18789",
    "token": "ocgw_xxxxxxxxxxxxxxxxxx"
  }
}
```

Replace the URL and token with the values from your installation.

### 4. Verification

```bash
# On VPS B -- test the connection
openclaw gateway status

# Should display: Connected to remote gateway at ws://100.x.x.x:18789

# Verify the health of the remote installation
openclaw health

# See detailed status
openclaw status --deep
```

---

## Security

| Rule | Why |
|------|-----|
| **Dedicated token** (not the root token) | Limit damage in case of leak |
| **`read` scope by default** | Client observes but does not modify |
| **Tailscale or SSH tunnel** | Transport encryption is mandatory |
| **Never `ws://` on public IP** | Plain WebSocket = credentials in plain text |
| **Regular token rotation** | Best practice, especially for client installations |

---

## Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `Connection refused` | Master gateway not listening on the correct port or IP | Check `gateway.json` on master side and network connectivity |
| `Authentication failed` | Incorrect or expired token | Regenerate token on master side, update on client side |
| `ws:// blocked on non-loopback` | OpenClaw refuses non-TLS WebSocket to a remote IP | Use Tailscale (considered loopback) or SSH tunnel |
| Client launches its own gateway | `mode` is still on `server` instead of `remote` | Check `gateway.json` on client side: `"mode": "remote"` |
| `gateway.auth` vs `gateway.remote` | Confusion between server and client config | `auth` = master side (receiving), `remote` = client side (connecting) |

---

## Reusable Template

### Master Configuration (VPS A)

```json
{
  "mode": "server",
  "port": 18789,
  "auth": {
    "tokens": [
      {
        "name": "remote-vps-b",
        "token": "REPLACE_WITH_YOUR_TOKEN",
        "scope": "read"
      }
    ]
  }
}
```

### Client Configuration (VPS B)

```json
{
  "mode": "remote",
  "remote": {
    "url": "ws://TAILSCALE_IP_VPS_A:18789",
    "token": "REPLACE_WITH_YOUR_TOKEN"
  }
}
```

### SSH Tunnel Command (if no Tailscale)

```bash
autossh -M 0 -N -L 18789:localhost:18789 user@VPS_A_IP \
  -o "ServerAliveInterval 30" -o "ServerAliveCountMax 3"
```

### Verification Commands

```bash
# From VPS B
openclaw gateway status         # Connection state
openclaw health                 # Health of remote installation
openclaw status --deep          # Detailed status
```

---

## Checklist

- [ ] Dedicated token created on master VPS (not the root token)
- [ ] Transport is encrypted (Tailscale, SSH tunnel, or TLS)
- [ ] `openclaw gateway status` displays "Connected" on client
- [ ] `openclaw health` returns a result from client
- [ ] `ws://` is NOT exposed on a public IP

---

*This section was written based on the experience of connecting VPS-Omar and VPS-Aurel (Pantheos). Issue [#31](https://github.com/alexwill87/openclaw-field-playbook/issues/31).*
