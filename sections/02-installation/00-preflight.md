---
status: complete
audience: both
chapter: 02
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit, claude-aurel]
lang: fr
---

# Checklist pre-vol -- Tout preparer avant de commencer

Cette page existe parce qu'on en a marre de decouvrir un prerequis a la section 13 alors qu'on aurait pu le preparer avant de commencer. Tout ce qui suit doit etre pret AVANT de lancer la premiere commande du chapitre 2.

Temps total de preparation : environ 30 minutes.

---

## 1. Comptes a creer

Creez ces comptes maintenant. Pas "plus tard". Maintenant.

| # | Service | URL d'inscription | Ce qu'il faut noter | Temps estime |
|---|---------|-------------------|---------------------|-------------|
| 1 | **Hetzner** ou **OVH** (VPS) | [hetzner.com/cloud](https://www.hetzner.com/cloud) / [ovh.com/vps](https://www.ovhcloud.com/fr/vps/) | Identifiants du compte, IP du serveur une fois commande | 10 min |
| 2 | **Tailscale** | [login.tailscale.com/start](https://login.tailscale.com/start) | Compte cree (connexion via Google, GitHub ou Microsoft) | 2 min |
| 3 | **OpenRouter** | [openrouter.ai](https://openrouter.ai) | Cle API (format `sk-or-v1-...`). Allez dans Settings > API Keys apres inscription | 5 min |
| 4 | **Telegram** (bot) | Dans l'app Telegram, cherchez `@BotFather` et envoyez `/newbot` | Token du bot (format `123456789:ABCDef...`), username du bot | 5 min |
| 5 | **GitHub** | [github.com/signup](https://github.com/signup) | Identifiants. Generez aussi un Personal Access Token (Settings > Developer settings > Tokens) | 5 min |

**Astuce Telegram** : Apres avoir cree le bot, envoyez-lui un message dans Telegram. Vous en aurez besoin plus tard pour recuperer votre `chat_id`.

---

## 2. Informations a collecter

Avant de toucher au serveur, rassemblez ces elements :

### Votre IP publique actuelle

```bash
$ curl -4 ifconfig.me
```

Notez-la. Vous en aurez besoin pour configurer le pare-feu du VPS.

### Votre cle SSH publique

Verifiez si vous en avez deja une :

```bash
$ cat ~/.ssh/id_ed25519.pub
```

Si le fichier n'existe pas, creez une cle :

```bash
$ ssh-keygen -t ed25519 -C "votre-email@example.com"
```

Acceptez le chemin par defaut, mettez une passphrase. Copiez le contenu de `~/.ssh/id_ed25519.pub`.

### Un mot de passe fort pour PostgreSQL

Generez-en un avec :

```bash
$ openssl rand -base64 24
```

Notez-le dans un gestionnaire de mots de passe (1Password, Bitwarden, KeePass). Vous le stockerez dans Vault a la section 07.

### Un nom pour votre agent

C'est le nom qui apparaitra dans `SOUL.md` -- l'identite de votre agent IA. Exemples : `Atlas`, `Vigil`, `Sentinel`. Choisissez quelque chose de court et memorable.

### L'adresse email de l'utilisateur principal

Elle sera utilisee dans `USER.md` pour identifier le proprietaire de l'instance. Utilisez une adresse que vous consultez vraiment.

---

## 3. Decisions a prendre AVANT de commencer

Ne decouvrez pas ces choix en plein milieu de l'installation. Decidez maintenant.

| Decision | Options | Recommandation |
|----------|---------|----------------|
| Vault ou fichiers .env ? | Vault (production) / .env (prototype) | Vault si multi-utilisateurs, .env si solo |
| PM2 ou systemd ? | PM2 (si deja utilise) / systemd (natif Ubuntu) | systemd pour les nouveaux |
| Quel modele LLM par defaut ? | Claude Sonnet / Haiku / Mistral / Gemini | Claude Sonnet 4 via OpenRouter |
| PostgreSQL ou SQLite ? | PostgreSQL (recommande) / SQLite (leger) | PostgreSQL |
| Mattermost ou pas ? | Oui (communication structuree) / Non (email/Telegram suffit) | Pas obligatoire au depart |

**Vault vs .env** : Si vous etes seul et que c'est un prototype, `.env` suffit pour demarrer. Mais si d'autres personnes ou agents accedent aux secrets, Vault est l'investissement qui evite la dette technique. Le playbook documente les deux approches, mais les sections suivantes utilisent Vault par defaut.

**PM2 vs systemd** : PM2 est pratique si vous venez du monde Node.js. systemd est natif a Ubuntu, ne necessite aucune installation supplementaire, et s'integre mieux avec les logs systeme. Si vous n'avez pas d'avis, prenez systemd.

**Modele LLM** : Claude Sonnet 4 offre le meilleur equilibre precision/cout pour des taches complexes. Haiku 3.5 est le fallback rapide et economique. Vous pourrez changer a tout moment via OpenRouter.

---

## 4. Budget estime

| Poste | Cout mensuel | Notes |
|-------|-------------|-------|
| VPS (Hetzner CPX21) | ~5-8 EUR/mois | 4 CPU, 8 Go RAM, 80 Go SSD |
| Cle API OpenRouter | ~10-30 EUR/mois | Depend de l'usage. Configurez une alerte a 10 EUR et une limite a 30 EUR |
| Domaine (optionnel) | ~10 EUR/an | Si vous voulez un domaine custom |
| **Total** | **~15-40 EUR/mois** | |

Le poste le plus variable est OpenRouter. Un agent actif qui utilise Claude Sonnet consomme plus qu'un agent en veille sur Haiku. Surveillez votre dashboard OpenRouter les premieres semaines.

---

## 5. Temps estime

| Phase | Duree |
|-------|-------|
| Creation des comptes (cette page) | 30 minutes |
| Installation complete (chapitre 2, sections 01-19) | 3-5 heures |
| Configuration (chapitre 3) | 2-3 heures |
| Personnalisation (chapitre 4) | Continu |

Prevoyez une demi-journee pour les chapitres 2 et 3. Ne commencez pas a 23h un dimanche soir.

---

## Checklist rapide

Cochez chaque point avant de passer a la section 01 :

- [ ] Compte VPS cree et serveur commande
- [ ] Compte Tailscale cree
- [ ] Compte OpenRouter cree et cle API notee
- [ ] Bot Telegram cree et token note
- [ ] Compte GitHub cree
- [ ] Cle SSH generee (ou existante localisee)
- [ ] Mot de passe PostgreSQL genere
- [ ] Decision Vault vs .env prise
- [ ] Decision PM2 vs systemd prise
- [ ] Budget mensuel estime et valide

Tout est coche ? Passez a **[2.1 -- Prerequis](01-prerequis.md)**.
