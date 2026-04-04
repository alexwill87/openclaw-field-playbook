---
---
status: complete
audience: both
chapter: 02
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: en
---

# 2.4 -- Docker and Docker Compose

## Context

Docker runs Vault, PostgreSQL, and potentially other services in isolated containers. Docker Compose orchestrates these containers with a simple YAML file.

## Step 1: Install dependencies

```bash
$ sudo apt update
$ sudo apt install -y ca-certificates curl gnupg
```

## Step 2: Add the official Docker repository

```bash
$ sudo install -m 0755 -d /etc/apt/keyrings
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
$ sudo chmod a+r /etc/apt/keyrings/docker.gpg
```

```bash
$ echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

## Step 3: Install Docker Engine

```bash
$ sudo apt update
$ sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

## Step 4: Add the user to the docker group

To avoid typing `sudo` before each docker command:

```bash
$ sudo usermod -aG docker $USER
$ newgrp docker
```

## Step 5: Verify the installation

```bash
$ docker --version
$ docker compose version
$ docker run hello-world
```

Expected result: "Hello from Docker!" in the output.

## Note on docker-compose vs docker compose

There are two syntaxes:

| Command | Version | Status |
|----------|---------|--------|
| `docker-compose` (with hyphen) | v1, separate Python binary | **Obsolete** |
| `docker compose` (with space) | v2, native Docker plugin | **Use this** |

This playbook uses exclusively `docker compose` (with space). If you find tutorials using `docker-compose`, replace it with `docker compose`.

## Step 6: Configure automatic startup

```bash
$ sudo systemctl enable docker
$ sudo systemctl enable containerd
```

## Common errors

- **"permission denied" on the Docker socket**: You did not add the user to the docker group, or you did not run `newgrp docker`. Log out and log back in.
- **"docker-compose: command not found"**: You installed Docker from the official repository (good), but you are using the old syntax. Use `docker compose` (with space).
- **Docker installed via snap**: Uninstall it (`sudo snap remove docker`) and reinstall from the official repository. The snap version causes permission issues.

## Verification

```bash
$ docker ps
$ docker compose version
$ id | grep docker
```

Expected results:
- `docker ps` runs without error (empty list is normal)
- `docker compose version` displays v2.x.x
- The `docker` group appears in the output of `id`

## Estimated time

10 minutes.
