---
---
status: complete
audience: both
chapter: 02
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: en
---

# 2.10 -- OpenClaw Installation

## Context

OpenClaw is the central tool of the system. This section covers the installation of the CLI and runtime. The infrastructure (Docker, Vault, PostgreSQL) must be in place before this step.

## Step 1: Verify Prerequisites

```bash
$ node --version   # v22.x+ required
$ npm --version    # v10.x+ required
$ docker --version # Docker 28.x+ required
```

If any version is insufficient, return to the corresponding section.

## Step 2: Install OpenClaw via npm

Recommended method (global installation):

```bash
$ npm install -g openclaw@latest
```

> **Warning:** The package is called `openclaw`, not `openclaw@latest` (which is Claude Code, another tool). Verify that the `openclaw` command is available after installation.

Verify:

```bash
$ openclaw --version
```

## Step 3: First Run

Launch OpenClaw for the first time to generate the workspace structure:

```bash
$ openclaw
```

Follow the initial configuration wizard. It will ask you for:
- The API key or authentication method
- The default model
- The workspace directory

## Step 4: Verify Installation

```bash
$ openclaw doctor
```

This command verifies all dependencies and configuration. Everything should be green.

## Common Errors

### Permission denied during global npm installation

```
Error: EACCES: permission denied, mkdir '/usr/local/lib/node_modules'
```

Solution: You are probably using Node.js installed via apt instead of nvm. With nvm, global installations go to `~/.nvm/` and do not require sudo.

```bash
$ nvm use --lts
$ npm install -g openclaw@latest
```

Do NOT do `sudo npm install -g`. This creates cascading permission issues.

### Wrong Node.js version

```
Error: openclaw requires Node.js >= 22.0.0
```

Solution:

```bash
$ nvm install --lts
$ nvm alias default lts/*
$ npm install -g openclaw@latest
```

### "openclaw: command not found" after installation

The binary is not in the PATH. With nvm, it should work automatically. Verify:

```bash
$ which openclaw
$ echo $PATH | tr ':' '\n' | grep nvm
```

If the nvm path is not in the PATH, reload the shell:

```bash
$ source ~/.bashrc
```

### Connectivity Issues

If npm installation fails with network errors:

```bash
$ npm config set registry https://registry.npmjs.org/
$ npm cache clean --force
$ npm install -g openclaw@latest
```

## Verification

```bash
$ openclaw --version
$ which openclaw
$ openclaw doctor
```

Expected results:
- Version displayed
- Path in `~/.nvm/versions/node/...`
- Doctor: all checks green

## Estimated Time

15 minutes.
