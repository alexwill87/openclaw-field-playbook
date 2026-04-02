---
status: complete
audience: both
chapter: 02
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 2.10 -- Installation OpenClaw

## Contexte

OpenClaw est l'outil central du systeme. Cette section couvre l'installation de la CLI et du runtime. L'infrastructure (Docker, Vault, PostgreSQL) doit etre en place avant cette etape.

## Etape 1 : Verifier les prerequis

```bash
$ node --version   # v22.x+ requis
$ npm --version    # v10.x+ requis
$ docker --version # Docker 28.x+ requis
```

Si une version est insuffisante, retournez a la section correspondante.

## Etape 2 : Installer OpenClaw via npm

Methode recommandee (installation globale) :

```bash
$ npm install -g openclaw@latest
```

> **Attention :** Le package s'appelle `openclaw`, pas `openclaw@latest` (qui est Claude Code, un autre outil). Verifiez que la commande `openclaw` est disponible apres installation.

Verifiez :

```bash
$ openclaw --version
```

## Etape 3 : Premiere execution

Lancez OpenClaw une premiere fois pour generer la structure du workspace :

```bash
$ openclaw
```

Suivez l'assistant de configuration initiale. Il vous demandera :
- La cle API ou la methode d'authentification
- Le modele par defaut
- Le repertoire workspace

## Etape 4 : Verifier l'installation

```bash
$ openclaw doctor
```

Cette commande verifie toutes les dependances et la configuration. Tout doit etre vert.

## Erreurs classiques

### Permission denied lors de l'installation globale npm

```
Error: EACCES: permission denied, mkdir '/usr/local/lib/node_modules'
```

Solution : Vous utilisez probablement Node.js installe via apt au lieu de nvm. Avec nvm, les installations globales vont dans `~/.nvm/` et ne necessitent pas sudo.

```bash
$ nvm use --lts
$ npm install -g openclaw@latest
```

Ne faites PAS `sudo npm install -g`. Ca cree des problemes de permissions en cascade.

### Mauvaise version de Node.js

```
Error: openclaw requires Node.js >= 22.0.0
```

Solution :

```bash
$ nvm install --lts
$ nvm alias default lts/*
$ npm install -g openclaw@latest
```

### "openclaw: command not found" apres installation

Le binaire n'est pas dans le PATH. Avec nvm, ca devrait fonctionner automatiquement. Verifiez :

```bash
$ which openclaw
$ echo $PATH | tr ':' '\n' | grep nvm
```

Si le chemin nvm n'est pas dans le PATH, rechargez le shell :

```bash
$ source ~/.bashrc
```

### Problemes de connectivite

Si l'installation npm echoue avec des erreurs reseau :

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

Resultats attendus :
- Version affichee
- Chemin dans `~/.nvm/versions/node/...`
- Doctor : tous les checks verts

## Temps estime

15 minutes.
