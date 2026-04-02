---
status: complete
audience: both
chapter: 02
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 2.5 -- Node.js et PM2

## Contexte

OpenClaw est ecrit en Node.js. PM2 est un gestionnaire de processus qui maintient OpenClaw en vie, gere les logs et redemarre automatiquement en cas de crash.

On installe Node.js via **nvm** (Node Version Manager), pas via apt. Pourquoi : apt fournit souvent une version obsolete, et nvm permet de changer de version facilement.

## Etape 1 : Installer nvm

```bash
$ curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/master/install.sh | bash
```

Rechargez le shell :

```bash
$ source ~/.bashrc
```

Verifiez :

```bash
$ nvm --version
```

## Etape 2 : Installer Node.js

Installez la version LTS (Long Term Support) :

```bash
$ nvm install --lts
$ nvm alias default lts/*
```

Verifiez :

```bash
$ node --version
$ npm --version
```

Version attendue : Node.js 22.x ou superieur (LTS au moment de l'ecriture).

## Etape 3 : Installer PM2

```bash
$ npm install -g pm2
```

Verifiez :

```bash
$ pm2 --version
```

## Etape 4 : Configurer PM2 pour le demarrage automatique

PM2 peut se relancer automatiquement au redemarrage du serveur :

```bash
$ pm2 startup
```

Cette commande affiche une ligne a copier-coller (elle commence par `sudo env PATH=...`). Executez-la.

Puis sauvegardez la liste actuelle des processus (vide pour l'instant) :

```bash
$ pm2 save
```

## Pourquoi PM2 et pas systemd directement ?

PM2 offre des fonctionnalites specifiques a Node.js :

- Redemarrage automatique en cas de crash avec backoff exponentiel
- Gestion des logs integree (`pm2 logs`)
- Monitoring memoire/CPU (`pm2 monit`)
- Mode cluster pour utiliser tous les CPU
- Rechargement sans interruption (`pm2 reload`)
- Ecosysteme de configuration via `ecosystem.config.js`

systemd sera utilise pour la gateway (section 15), mais PM2 gere les processus applicatifs Node.js.

## Erreurs courantes

- **Installer Node.js via apt** : La version sera trop vieille. Desinstallez (`sudo apt remove nodejs`) et utilisez nvm.
- **"nvm: command not found" apres installation** : Vous n'avez pas recharge le shell. Faites `source ~/.bashrc` ou ouvrez un nouveau terminal.
- **PM2 installe localement au lieu de globalement** : Assurez-vous d'utiliser `npm install -g pm2` (avec le `-g`).
- **PM2 startup ne fonctionne pas** : Executez bien la commande sudo affichee par `pm2 startup`, ne tapez pas juste `pm2 startup` avec sudo.

## Verification

```bash
$ node --version
$ npm --version
$ pm2 --version
$ pm2 list
```

Resultats attendus :
- Node.js v22.x+
- npm v10.x+
- PM2 v5.x+
- Liste PM2 vide (aucun processus encore)

## Temps estime

10 minutes.
