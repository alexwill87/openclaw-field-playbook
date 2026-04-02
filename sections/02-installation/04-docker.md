---
status: complete
audience: both
chapter: 02
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 2.4 -- Docker et Docker Compose

## Contexte

Docker fait tourner Vault, PostgreSQL et potentiellement d'autres services dans des conteneurs isoles. Docker Compose orchestre ces conteneurs avec un simple fichier YAML.

## Etape 1 : Installer les dependances

```bash
$ sudo apt update
$ sudo apt install -y ca-certificates curl gnupg
```

## Etape 2 : Ajouter le depot officiel Docker

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

## Etape 3 : Installer Docker Engine

```bash
$ sudo apt update
$ sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

## Etape 4 : Ajouter l'utilisateur au groupe docker

Pour eviter de taper `sudo` devant chaque commande docker :

```bash
$ sudo usermod -aG docker $USER
$ newgrp docker
```

## Etape 5 : Verifier l'installation

```bash
$ docker --version
$ docker compose version
$ docker run hello-world
```

Resultat attendu : "Hello from Docker!" dans la sortie.

## Note sur docker-compose vs docker compose

Il existe deux syntaxes :

| Commande | Version | Status |
|----------|---------|--------|
| `docker-compose` (avec tiret) | v1, binaire Python separe | **Obsolete** |
| `docker compose` (avec espace) | v2, plugin Docker natif | **A utiliser** |

Ce playbook utilise exclusivement `docker compose` (avec espace). Si vous trouvez des tutoriels avec `docker-compose`, remplacez par `docker compose`.

## Etape 6 : Configurer le demarrage automatique

```bash
$ sudo systemctl enable docker
$ sudo systemctl enable containerd
```

## Erreurs courantes

- **"permission denied" sur le socket Docker** : Vous n'avez pas ajoute l'utilisateur au groupe docker, ou vous n'avez pas fait `newgrp docker`. Deconnectez-vous et reconnectez-vous.
- **"docker-compose: command not found"** : Vous avez installe Docker via le depot officiel (bien), mais vous utilisez la vieille syntaxe. Utilisez `docker compose` (avec espace).
- **Docker installe via snap** : Desinstallez-le (`sudo snap remove docker`) et reinstallez depuis le depot officiel. La version snap pose des problemes de permissions.

## Verification

```bash
$ docker ps
$ docker compose version
$ id | grep docker
```

Resultats attendus :
- `docker ps` s'execute sans erreur (liste vide, c'est normal)
- `docker compose version` affiche v2.x.x
- Le groupe `docker` apparait dans la sortie de `id`

## Temps estime

10 minutes.
