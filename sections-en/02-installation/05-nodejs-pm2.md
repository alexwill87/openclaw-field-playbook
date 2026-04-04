---
status: complete
audience: both
chapter: 02
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: en
---

# 2.5 -- Node.js and PM2

## Context

OpenClaw is written in Node.js. PM2 is a process manager that keeps OpenClaw running, manages logs, and automatically restarts on crash.

Install Node.js via **nvm** (Node Version Manager), not via apt. Why: apt often provides an outdated version, and nvm allows you to switch versions easily.

## Step 1: Install nvm

```bash
$ curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/master/install.sh | bash
```

Reload the shell:

```bash
$ source ~/.bashrc
```

Verify:

```bash
$ nvm --version
```

## Step 2: Install Node.js

Install the LTS (Long Term Support) version:

```bash
$ nvm install --lts
$ nvm alias default lts/*
```

Verify:

```bash
$ node --version
$ npm --version
```

Expected version: Node.js 22.x or higher (LTS at the time of writing).

## Step 3: Install PM2

```bash
$ npm install -g pm2
```

Verify:

```bash
$ pm2 --version
```

## Step 4: Configure PM2 for automatic startup

PM2 can restart automatically when the server reboots:

```bash
$ pm2 startup
```

This command displays a line to copy and paste (it starts with `sudo env PATH=...`). Execute it.

Then save the current list of processes (empty for now):

```bash
$ pm2 save
```

## Why PM2 and not systemd directly?

PM2 provides features specific to Node.js:

- Automatic restart on crash with exponential backoff
- Built-in log management (`pm2 logs`)
- Memory/CPU monitoring (`pm2 monit`)
- Cluster mode to use all CPUs
- Zero-downtime reload (`pm2 reload`)
- Configuration ecosystem via `ecosystem.config.js`

systemd will be used for the gateway (section 15), but PM2 manages Node.js application processes.

## Common errors

- **Installing Node.js via apt**: The version will be too old. Uninstall it (`sudo apt remove nodejs`) and use nvm.
- **"nvm: command not found" after installation**: You didn't reload the shell. Run `source ~/.bashrc` or open a new terminal.
- **PM2 installed locally instead of globally**: Make sure you use `npm install -g pm2` (with the `-g`).
- **PM2 startup doesn't work**: Make sure to execute the sudo command displayed by `pm2 startup`, don't just run `pm2 startup` with sudo.

## Verification

```bash
$ node --version
$ npm --version
$ pm2 --version
$ pm2 list
```

Expected results:
- Node.js v22.x+
- npm v10.x+
- PM2 v5.x+
- PM2 list empty (no processes yet)

## Estimated time

10 minutes.
