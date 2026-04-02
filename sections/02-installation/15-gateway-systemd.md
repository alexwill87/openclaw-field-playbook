---
status: complete
audience: both
chapter: 02
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 2.15 -- Gateway systemd

## Contexte

La gateway OpenClaw est le point d'entree HTTP du systeme. Elle doit tourner en permanence, redemarrer automatiquement en cas de crash et demarrer au boot du serveur. systemd est le gestionnaire de services standard de Linux -- c'est lui qui gere ca.

## Etape 1 : Creer le fichier de service

Creez `/etc/systemd/system/openclaw-gateway.service` :

```bash
$ sudo nano /etc/systemd/system/openclaw-gateway.service
```

Contenu :

D'abord, trouvez vos chemins exacts :

```bash
$ which node
$ which openclaw
```

Notez les resultats. Creez ensuite le fichier d'environnement pour les secrets :

```bash
$ sudo mkdir -p /etc/openclaw
$ sudo tee /etc/openclaw/gateway.env > /dev/null << 'EOF'
VAULT_ADDR=http://127.0.0.1:8200
VAULT_TOKEN=VOTRE_TOKEN_APPLICATIF_ICI
EOF
$ sudo chmod 600 /etc/openclaw/gateway.env
$ sudo chown root:root /etc/openclaw/gateway.env
```

> **SECURITE :** Le token Vault ne doit JAMAIS apparaitre en clair dans le fichier systemd. Utilisez `EnvironmentFile` pour le charger depuis un fichier protege (chmod 600, propriete root).

Creez le fichier service en remplacant `VOTRE_USER` et les chemins par vos valeurs :

```ini
[Unit]
Description=OpenClaw Gateway
Documentation=https://github.com/alexwill87/openclawfieldplaybook
After=network.target docker.service
Wants=docker.service

[Service]
Type=simple
User=VOTRE_USER
Group=VOTRE_USER
WorkingDirectory=/home/VOTRE_USER
Environment=NODE_ENV=production
EnvironmentFile=/etc/openclaw/gateway.env

ExecStart=/home/VOTRE_USER/.nvm/versions/node/VOTRE_VERSION/bin/node /home/VOTRE_USER/.nvm/versions/node/VOTRE_VERSION/bin/openclaw gateway start
ExecReload=/bin/kill -HUP $MAINPID
ExecStop=/bin/kill -TERM $MAINPID

Restart=always
RestartSec=10
StartLimitIntervalSec=300
StartLimitBurst=5

StandardOutput=journal
StandardError=journal
SyslogIdentifier=openclaw-gateway

# Securite
NoNewPrivileges=true
ProtectSystem=strict
ReadWritePaths=/home/VOTRE_USER

[Install]
WantedBy=multi-user.target
```

**IMPORTANT** : Remplacez les placeholders :
- `VOTRE_USER` : votre nom d'utilisateur (resultat de `whoami`)
- `VOTRE_VERSION` : votre version Node.js (resultat de `node --version`, ex: `v22.22.1`)
- Le token Vault dans `/etc/openclaw/gateway.env` : celui cree a la section 07

> **PM2 ou systemd ?** Si vous utilisez deja PM2 pour d'autres services Node.js, utilisez PM2. Sinon, systemd est recommande car il est natif a Ubuntu et ne necessite pas de dependance supplementaire. Ne melangez pas les deux pour le meme service.

## Etape 2 : Activer et demarrer le service

```bash
$ sudo systemctl daemon-reload
$ sudo systemctl enable openclaw-gateway
$ sudo systemctl start openclaw-gateway
```

## Etape 3 : Verifier le status

```bash
$ sudo systemctl status openclaw-gateway
```

Resultat attendu :

```
openclaw-gateway.service - OpenClaw Gateway
     Loaded: loaded (/etc/systemd/system/openclaw-gateway.service; enabled)
     Active: active (running) since ...
```

## Etape 4 : Consulter les logs

Logs en temps reel :

```bash
$ journalctl -u openclaw-gateway -f
```

Logs depuis le dernier demarrage :

```bash
$ journalctl -u openclaw-gateway -b
```

Logs des dernieres 100 lignes :

```bash
$ journalctl -u openclaw-gateway -n 100 --no-pager
```

## Etape 5 : Commandes de gestion courantes

| Action | Commande |
|--------|----------|
| Demarrer | `sudo systemctl start openclaw-gateway` |
| Arreter | `sudo systemctl stop openclaw-gateway` |
| Redemarrer | `sudo systemctl restart openclaw-gateway` |
| Recharger config | `sudo systemctl reload openclaw-gateway` |
| Status | `sudo systemctl status openclaw-gateway` |
| Desactiver au boot | `sudo systemctl disable openclaw-gateway` |
| Voir les logs | `journalctl -u openclaw-gateway -f` |

## Comportement de redemarrage automatique

La configuration prevoit :
- `Restart=always` : redemarre apres tout arret (crash, kill, etc.)
- `RestartSec=10` : attend 10 secondes avant de redemarrer
- `StartLimitBurst=5` et `StartLimitIntervalSec=300` : maximum 5 redemarrages en 5 minutes. Au-dela, systemd considere le service comme defaillant et arrete les tentatives.

Pour reinitialiser le compteur de tentatives :

```bash
$ sudo systemctl reset-failed openclaw-gateway
$ sudo systemctl start openclaw-gateway
```

## Erreurs courantes

- **"openclaw: command not found"** dans les logs : systemd ne charge pas `.bashrc`. Il faut utiliser le chemin ABSOLU vers node et openclaw. Pas de `nvm`, pas de `~`.
- **Permission denied** : L'utilisateur dans le fichier service n'a pas acces au dossier. Verifiez `User=` et `ReadWritePaths=`.
- **Service qui boucle (restart loop)** : Verifiez les logs (`journalctl`). Souvent un probleme de token Vault ou de connexion base de donnees.
- **"Start request repeated too quickly"** : Le service a crashe 5 fois en 5 minutes. Corrigez le probleme sous-jacent, puis `systemctl reset-failed`.

## Verification

```bash
$ sudo systemctl status openclaw-gateway
$ curl -s http://127.0.0.1:3000/health
$ journalctl -u openclaw-gateway -n 10 --no-pager
```

Resultats attendus :
- Status : active (running)
- Health endpoint retourne une reponse 200
- Pas d'erreur dans les 10 dernieres lignes de log

## Temps estime

10 minutes.
