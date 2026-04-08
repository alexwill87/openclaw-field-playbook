---
status: complete
audience: both
chapter: 03
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 3.19 -- Le terminal : votre interface quotidienne

> Le terminal n'est pas un outil de developpeur. C'est votre poste de pilotage. Cette section explique comment l'utiliser efficacement, comment le configurer, et pourquoi c'est la meilleure facon d'interagir avec OpenClaw.

**Pour qui :** tout le monde
**Prerequis :** installation terminee (chapitre 2), gateway fonctionnel
**Difficulte :** Debutant
**Temps de lecture :** 20 minutes

---

## Contexte

OpenClaw est un systeme qui vit dans le terminal. Pas dans un navigateur web, pas dans une application desktop — dans un terminal. C'est un choix delibere : le terminal est rapide, direct, et ne necessite aucune infrastructure supplementaire.

Si vous venez d'un monde ou tout passe par des interfaces graphiques, ca peut sembler intimidant. Cette section est la pour vous montrer que le terminal est en realite **plus simple** qu'un dashboard — pas plus complique.

---

## Pourquoi le terminal et pas une interface graphique

| Interface graphique | Terminal |
|---------------------|---------|
| Il faut un serveur web, un framework, du CSS | Il est deja la |
| Il faut le maintenir, le mettre a jour | Rien a maintenir |
| Il peut tomber en panne independamment | Si le serveur tourne, le terminal aussi |
| Il montre ce que quelqu'un a decide de montrer | Il montre tout ce que vous demandez |
| Il faut cliquer, naviguer, chercher | Une commande, une reponse |

Le terminal n'est pas une interface degradee. C'est l'interface **la plus directe** vers votre systeme.

---

## Comment acceder a votre terminal

### Option 1 : SSH direct (le plus simple)

Depuis n'importe quelle machine :

```bash
$ ssh votre-user@votre-ip-tailscale
```

Avantages :
- Fonctionne depuis n'importe ou (Mac, Linux, Windows, telephone)
- Zero installation supplementaire
- Connexion chiffree via Tailscale

### Option 2 : VS Code Remote SSH (recommande pour le travail quotidien)

VS Code peut se connecter directement a votre VPS et vous donner un terminal integre, un explorateur de fichiers, et un editeur — le tout dans une seule fenetre.

**Installation :**

1. Installez [VS Code](https://code.visualstudio.com/) sur votre machine locale.
2. Installez l'extension **Remote - SSH** (identifiant : `ms-vscode-remote.remote-ssh`).
3. Appuyez sur `F1` > tapez "Remote-SSH: Connect to Host..." > entrez `votre-user@votre-ip-tailscale`.
4. VS Code se connecte. Ouvrez un terminal integre avec `` Ctrl+` ``.

**Configuration SSH pour eviter de retaper l'adresse :**

Sur votre machine locale, editez `~/.ssh/config` :

```
Host mon-vps
    HostName 100.x.x.x
    User votre-user
    IdentityFile ~/.ssh/id_ed25519
```

Ensuite dans VS Code : `F1` > "Remote-SSH: Connect to Host..." > selectionnez `mon-vps`.

**Pourquoi VS Code Remote est recommande :**

| Fonctionnalite | SSH seul | VS Code Remote |
|----------------|----------|----------------|
| Terminal | Oui | Oui (integre, multiple) |
| Editer des fichiers | `nano` ou `vim` | Editeur complet avec coloration |
| Naviguer dans les fichiers | `ls`, `cd` | Explorateur visuel |
| Copier-coller | Selon le terminal | Natif |
| Plusieurs terminaux | `tmux` ou `screen` | Onglets integres |
| Extensions (git, markdown) | Non | Oui |

> **Vous n'etes PAS oblige d'utiliser VS Code.** SSH direct fonctionne parfaitement. VS Code ajoute du confort, pas de la fonctionnalite. Si vous etes a l'aise dans un terminal SSH, restez-y.

### Option 3 : Terminal local (si OpenClaw est sur votre machine)

Si vous avez installe OpenClaw directement sur votre machine (pas sur un VPS), ouvrez simplement votre terminal habituel :

- **macOS** : Terminal.app ou iTerm2
- **Linux** : le terminal de votre distribution
- **Windows** : Windows Terminal + WSL2

### Option 4 : Application mobile (acces d'urgence)

Pour un acces rapide depuis un telephone :

- **iOS** : Termius, Prompt
- **Android** : Termux, JuiceSSH

Ce n'est pas confortable pour travailler longtemps, mais utile pour un `openclaw health` rapide quand vous n'etes pas devant votre ordinateur.

---

## Configurer votre terminal pour OpenClaw

### Aliases utiles

Ajoutez ces raccourcis a votre `~/.bashrc` ou `~/.zshrc` sur le VPS :

```bash
# OpenClaw - raccourcis quotidiens
alias ocs='openclaw gateway status'
alias och='openclaw health'
alias ocd='openclaw status --deep'
alias ocl='journalctl -u openclaw-gateway -f'
alias oclogs='journalctl -u openclaw-gateway -n 100 --no-pager'
alias ocr='sudo systemctl restart openclaw-gateway'
alias ocsess='openclaw sessions'
```

Rechargez :

```bash
$ source ~/.bashrc
```

Maintenant au lieu de taper `openclaw gateway status`, tapez `ocs`. Au lieu de `journalctl -u openclaw-gateway -f`, tapez `ocl`.

### Prompt personnalise (optionnel)

Pour voir d'un coup d'oeil si le gateway tourne, ajoutez un indicateur dans votre prompt bash :

```bash
# Dans ~/.bashrc
openclaw_status() {
  if systemctl is-active --quiet openclaw-gateway 2>/dev/null; then
    echo "●"
  else
    echo "○"
  fi
}
export PS1='$(openclaw_status) \u@\h:\w\$ '
```

Resultat : `● omar@vps:~$` quand le gateway tourne, `○ omar@vps:~$` quand il est arrete.

### Configuration VS Code pour OpenClaw

Si vous utilisez VS Code Remote, ajoutez ces parametres pour une meilleure experience :

1. Ouvrez les Settings (`Ctrl+,`)
2. Cherchez "terminal" et ajustez :

| Parametre | Valeur recommandee | Pourquoi |
|-----------|-------------------|----------|
| `terminal.integrated.scrollback` | `5000` | Plus d'historique visible |
| `terminal.integrated.fontSize` | `14` | Lisibilite |
| `files.autoSave` | `afterDelay` | Sauvegarde auto quand vous editez des configs |

3. Extensions VS Code utiles pour OpenClaw :

| Extension | Ce qu'elle apporte |
|-----------|-------------------|
| **YAML** (Red Hat) | Coloration du frontmatter des sections |
| **Markdown All in One** | Preview des fichiers .md |
| **Docker** (Microsoft) | Voir les containers depuis VS Code |
| **GitLens** | Historique des modifications |

> Ces extensions sont **optionnelles**. Elles ajoutent du confort, pas de la fonctionnalite.

---

## Les commandes du quotidien

### Le matin (2 minutes)

```bash
# Etat general
$ ocs        # alias pour openclaw gateway status

# Si quelque chose est rouge :
$ och        # alias pour openclaw health
$ oclogs     # alias pour les 100 dernieres lignes de log
```

### Pendant la journee

```bash
# Voir les sessions actives
$ ocsess     # alias pour openclaw sessions

# Parler a un agent
$ openclaw chat

# Voir ce qu'un agent a fait
$ openclaw sessions --last

# Executer une commande via l'agent
$ openclaw run "verifie les backups"
```

### En cas de probleme

```bash
# Logs en temps reel
$ ocl        # alias pour journalctl -f

# Diagnostic complet
$ ocd        # alias pour openclaw status --deep

# Redemarrer le gateway
$ ocr        # alias pour systemctl restart

# Verifier les secrets
$ openclaw gateway token list
```

### En fin de journee (1 minute)

```bash
# Resume de la journee
$ openclaw sessions --today

# Etat avant de partir
$ ocs
```

---

## Travailler avec plusieurs terminaux

Quand vous travaillez sur votre VPS, vous aurez souvent besoin de plusieurs terminaux en parallele. Par exemple :

- Terminal 1 : les logs du gateway en temps reel (`ocl`)
- Terminal 2 : vos commandes habituelles
- Terminal 3 : un `openclaw chat` en cours

### Avec VS Code

Cliquez sur le `+` dans le panneau terminal pour ouvrir un nouvel onglet. Nommez-les pour vous y retrouver (clic droit > "Rename").

### Avec tmux (SSH seul)

```bash
# Demarrer tmux
$ tmux new -s openclaw

# Diviser l'ecran horizontalement
Ctrl+b puis "

# Diviser verticalement
Ctrl+b puis %

# Naviguer entre les panneaux
Ctrl+b puis fleches

# Detacher (la session continue en arriere-plan)
Ctrl+b puis d

# Revenir plus tard
$ tmux attach -t openclaw
```

tmux est particulierement utile en SSH : si votre connexion coupe, les processus continuent et vous les retrouvez en vous reconnectant.

---

## Erreurs courantes

**Ne pas utiliser d'aliases.** Taper `journalctl -u openclaw-gateway -n 100 --no-pager` a chaque fois est penible. Les aliases existent pour ca.

**Ouvrir un seul terminal.** Gardez toujours un terminal avec les logs en temps reel (`ocl`). Quand quelque chose ne fonctionne pas, la reponse est souvent dans les logs.

**Ignorer le terminal pour un dashboard.** Le dashboard est une commodite, pas un remplacement. Les informations les plus precises et les plus a jour sont dans le terminal.

**Se connecter en root.** Utilisez toujours votre utilisateur (`ssh votre-user@...`), jamais root directement. C'est une regle de securite de base (section 2.2).

---

## Verification

- [ ] Vous pouvez vous connecter a votre VPS en SSH.
- [ ] Les aliases `ocs`, `och`, `ocl` sont configures et fonctionnent.
- [ ] Vous savez ouvrir plusieurs terminaux (VS Code ou tmux).
- [ ] `ocs` retourne un resultat propre.
- [ ] Vous avez teste `openclaw chat` au moins une fois.

---

## Temps estime

20 minutes (configuration des aliases + test des commandes).
