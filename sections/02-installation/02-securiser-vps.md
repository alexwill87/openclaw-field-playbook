---
status: complete
audience: both
chapter: 02
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 2.2 -- Securiser le VPS

## Contexte

Un VPS neuf est expose a Internet avec un acces root par mot de passe. C'est une cible facile. Cette section blinde le serveur AVANT d'installer quoi que ce soit. Chaque commande est a executer dans l'ordre.

## Etape 1 : Premiere connexion en root

Depuis votre poste local :

```bash
$ ssh root@VOTRE_IP_VPS
```

Acceptez l'empreinte SSH si c'est la premiere connexion.

## Etape 2 : Mettre a jour le systeme

```bash
# apt update && apt upgrade -y
# apt install -y curl wget git ufw fail2ban unattended-upgrades
```

## Etape 3 : Creer un utilisateur non-root

Ne travaillez JAMAIS en root au quotidien. Creez un utilisateur dedie :

```bash
# adduser deploy
```

Repondez aux questions (mot de passe fort, le reste peut etre vide).

Donnez-lui les droits sudo :

```bash
# usermod -aG sudo deploy
```

## Etape 4 : Configurer l'authentification par cle SSH

Sur votre machine LOCALE (pas le VPS), generez une cle si vous n'en avez pas :

```bash
$ ssh-keygen -t ed25519 -C "votre-email@example.com"
```

Copiez la cle publique sur le VPS :

```bash
$ ssh-copy-id deploy@VOTRE_IP_VPS
```

Testez la connexion sans mot de passe :

```bash
$ ssh deploy@VOTRE_IP_VPS
```

Si ca marche, passez a l'etape suivante. Si non, ne desactivez PAS le mot de passe.

## Etape 5 : Desactiver l'authentification par mot de passe

**IMPORTANT** : Ne faites cette etape QUE si la connexion par cle SSH fonctionne. Sinon vous serez bloque hors du serveur.

Editez la configuration SSH :

```bash
$ sudo nano /etc/ssh/sshd_config
```

Modifiez (ou ajoutez) ces lignes :

```
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
```

Redemarrez SSH :

```bash
$ sudo systemctl restart sshd
```

**Gardez votre session actuelle ouverte** et testez dans un NOUVEAU terminal :

```bash
$ ssh deploy@VOTRE_IP_VPS
```

## Etape 6 : Configurer le pare-feu UFW

Politique par defaut : tout bloquer en entree, tout autoriser en sortie.

```bash
$ sudo ufw default deny incoming
$ sudo ufw default allow outgoing
```

Autoriser SSH (sinon vous perdez l'acces) :

```bash
$ sudo ufw allow ssh
```

Activer le pare-feu :

```bash
$ sudo ufw enable
```

Verifier l'etat :

```bash
$ sudo ufw status verbose
```

Resultat attendu :

```
Status: active

To                         Action      From
--                         ------      ----
22/tcp                     ALLOW IN    Anywhere
```

**IMPORTANT** : N'ouvrez PAS d'autres ports. Tous les services (Vault, PostgreSQL, OpenClaw) seront accessibles uniquement via Tailscale, pas via l'IP publique.

## Etape 7 : Configurer fail2ban

fail2ban bloque les IP qui tentent trop de connexions SSH :

```bash
$ sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
$ sudo nano /etc/fail2ban/jail.local
```

Trouvez la section `[sshd]` et assurez-vous qu'elle contient :

```ini
[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
bantime = 3600
findtime = 600
```

Redemarrez fail2ban :

```bash
$ sudo systemctl restart fail2ban
$ sudo systemctl enable fail2ban
```

## Etape 8 : Mises a jour automatiques de securite

```bash
$ sudo dpkg-reconfigure -plow unattended-upgrades
```

Selectionnez "Yes" pour activer les mises a jour automatiques.

Verifiez la configuration :

```bash
$ cat /etc/apt/apt.conf.d/20auto-upgrades
```

Resultat attendu :

```
APT::Periodic::Update-Package-Lists "1";
APT::Periodic::Unattended-Upgrade "1";
```

## Etape 9 : Configurer le fuseau horaire

```bash
$ sudo timedatectl set-timezone Europe/Paris
$ timedatectl
```

## Erreurs courantes

- **Se bloquer hors du serveur** : Toujours tester la connexion SSH par cle AVANT de desactiver le mot de passe. Gardez une session ouverte pendant les changements SSH.
- **Oublier d'autoriser SSH dans UFW avant de l'activer** : Vous perdez l'acces. La plupart des fournisseurs offrent une console VNC de secours.
- **Ne pas installer fail2ban** : Les bots scannent en permanence. Sans fail2ban, vous verrez des milliers de tentatives de connexion par jour.

## Verification

```bash
$ sudo ufw status
$ sudo systemctl status fail2ban
$ sudo systemctl status sshd
$ cat /etc/ssh/sshd_config | grep -E "PermitRoot|PasswordAuth"
```

Resultats attendus :
- UFW actif, seul le port 22 ouvert
- fail2ban actif
- sshd actif
- PermitRootLogin no, PasswordAuthentication no

## Temps estime

20 minutes.
