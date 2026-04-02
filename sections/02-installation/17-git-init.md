---
status: complete
audience: both
chapter: 02
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 2.17 -- Initialiser le repo Git

## Contexte

Le code, les scripts et la configuration (hors secrets) doivent etre versionnes dans Git. Cette section cree le depot, configure le remote GitHub et met en place un .gitignore solide pour eviter de committer des secrets ou des fichiers inutiles.

## Etape 1 : Initialiser le depot

```bash
$ cd ~/
$ git init oa-system
$ cd oa-system
```

Ou si vous travaillez directement dans votre home :

```bash
$ cd ~/
$ git init
```

## Etape 2 : Configurer Git

```bash
$ git config user.name "Votre Nom"
$ git config user.email "votre-email@example.com"
$ git config init.defaultBranch main
```

## Etape 3 : Creer le .gitignore

Creez `.gitignore` a la racine du depot :

```gitignore
# === Secrets et credentials ===
.env
.env.*
*.key
*.pem
credentials.json
vault-keys.txt
unseal-keys.txt

# === Donnees Docker ===
docker/vault/data/
docker/postgres/data/

# === Sauvegardes ===
backups/

# === Logs ===
logs/
*.log

# === Node.js ===
node_modules/
npm-debug.log*
.npm

# === OpenClaw ===
.openclaw/credentials.json
.openclaw/logs/
.openclaw/workspace/sessions/

# === OS ===
.DS_Store
Thumbs.db
*~
*.swp
*.swo

# === IDE ===
.vscode/settings.json
.idea/
*.sublime-workspace
```

## Etape 4 : Copier les fichiers a versionner

Les fichiers qui DOIVENT etre dans Git :

```bash
# Scripts
$ cp ~/scripts/*.sh ./scripts/

# Docker compose (sans les donnees)
$ mkdir -p docker/vault docker/postgres
$ cp ~/docker/vault/docker-compose.yml ./docker/vault/
$ cp ~/docker/vault/config/vault.hcl ./docker/vault/config/
$ cp ~/docker/postgres/docker-compose.yml ./docker/postgres/

# Health check
$ cp ~/scripts/health-check.sh ./scripts/
```

Les fichiers qui NE DOIVENT PAS etre dans Git :
- Tout ce qui est dans `backups/`
- Les dossiers `data/` des conteneurs
- Les fichiers `.env` ou contenant des secrets
- Les unseal keys de Vault

## Etape 5 : Creer le remote GitHub

Creez un depot sur GitHub (prive recommande), puis :

```bash
$ git remote add origin git@github.com:VOTRE_USER/oa-system.git
```

Si vous utilisez HTTPS au lieu de SSH :

```bash
$ git remote add origin https://github.com/VOTRE_USER/oa-system.git
```

## Etape 6 : Premier commit

```bash
$ git add .
$ git status
```

Verifiez que AUCUN secret n'apparait dans la liste des fichiers a committer. Si un fichier sensible apparait, ajoutez-le au .gitignore et faites `git reset HEAD <fichier>`.

```bash
$ git commit -m "feat: initialisation du systeme OA - infrastructure et scripts"
$ git push -u origin main
```

## Etape 7 : Verifier sur GitHub

Allez sur votre depot GitHub et verifiez :
- Les fichiers sont presents
- Aucun secret n'est visible
- Le .gitignore fonctionne (pas de `data/`, pas de `backups/`)

## Erreurs courantes

- **Committer des secrets** : Si ca arrive, le secret est compromis meme si vous le supprimez du prochain commit (l'historique Git le conserve). Changez le secret immediatement. Utilisez `git-filter-repo` pour purger l'historique si necessaire.
- **"Permission denied (publickey)"** : Votre cle SSH n'est pas configuree sur GitHub. Ajoutez-la dans GitHub > Settings > SSH Keys.
- **Depot prive vs public** : Pour un systeme de production, utilisez un depot PRIVE. Les fichiers docker-compose.yml peuvent reveler votre architecture.
- **Oublier le .gitignore avant le premier commit** : Si `node_modules/` ou `data/` a ete committe, faites `git rm -r --cached node_modules/` puis re-committez.

## Verification

```bash
$ git status
$ git log --oneline
$ git remote -v
```

Resultats attendus :
- Working tree clean (rien a committer)
- Au moins un commit visible
- Remote pointe vers votre depot GitHub

## Temps estime

10 minutes.
