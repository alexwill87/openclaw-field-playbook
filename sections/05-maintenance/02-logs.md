---
status: complete
audience: both
chapter: 05
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 5.2 -- Gestion des logs

## Contexte

Les logs sont votre boite noire. Quand tout va bien, personne ne les regarde. Quand ca casse, c'est la premiere chose qu'on ouvre. Si vous ne savez pas ou ils sont et comment les lire, vous perdez du temps au pire moment.

## Ou sont les logs

### Logs systeme (journalctl)

```bash
# Tous les logs depuis le dernier boot
journalctl -b

# Logs d'un service specifique
journalctl -u postgresql
journalctl -u docker

# Logs des 30 dernieres minutes
journalctl --since "30 min ago"

# Logs d'aujourd'hui
journalctl --since today

# Suivre en temps reel
journalctl -f

# Filtrer par priorite (erreurs et plus grave)
journalctl -p err
```

### Logs Docker

```bash
# Logs d'un container
docker logs cockpit

# Les 50 dernieres lignes
docker logs cockpit --tail 50

# Suivre en temps reel
docker logs cockpit -f

# Depuis une date
docker logs cockpit --since "2026-04-01T10:00:00"

# Tous les containers avec leurs logs recents
for c in $(docker ps --format "{{.Names}}"); do
    echo "=== $c ==="
    docker logs "$c" --tail 5 2>&1
    echo ""
done
```

### Logs applicatifs

Selon votre stack :

| Application | Emplacement typique |
|---|---|
| Node.js | stdout (capte par Docker) ou `/var/log/app/` |
| PostgreSQL | `/var/log/postgresql/` ou journalctl |
| Nginx | `/var/log/nginx/access.log`, `/var/log/nginx/error.log` |
| Vault | journalctl -u vault |
| Scripts perso | `/var/log/` (ou vous les avez diriges) |
| Health check | `/var/log/health-check.log` |

### Logs des sessions agent

Si votre agent a un log de session :

```bash
# Claude Code sessions
ls ~/.claude/sessions/

# Historique des commandes executees
cat ~/.bash_history | tail -50
```

## Comment lire les logs

### Le reflexe : fin du fichier d'abord

Les logs les plus recents sont les plus utiles. Toujours commencer par la fin :

```bash
# Les 100 dernieres lignes
tail -100 /var/log/nginx/error.log

# Ou avec journalctl
journalctl -u postgresql -n 100
```

### Filtrer le bruit

```bash
# Chercher les erreurs
journalctl -p err --since today

# Grep sur un pattern
docker logs cockpit 2>&1 | grep -i "error\|fail\|exception"

# Exclure le bruit connu
docker logs cockpit 2>&1 | grep -iv "healthcheck\|GET /favicon"
```

### Correler par timestamp

Quand un probleme survient, notez l'heure. Puis cherchez dans tous les logs autour de cette heure :

```bash
# Tous les logs systeme autour de 14h30
journalctl --since "14:25" --until "14:35"

# Docker logs autour du meme moment
docker logs cockpit --since "2026-04-01T14:25:00" --until "2026-04-01T14:35:00"
```

## Rotation des logs

Les logs grandissent indefiniment si vous ne les gerez pas. Un disque plein a cause des logs est une panne evitable.

### journalctl (systemd)

```bash
# Taille actuelle des logs systeme
journalctl --disk-usage

# Garder seulement les 7 derniers jours
sudo journalctl --vacuum-time=7d

# Limiter a 500M
sudo journalctl --vacuum-size=500M

# Configuration permanente dans /etc/systemd/journald.conf
# SystemMaxUse=500M
# MaxRetentionSec=7d
```

### Docker

```bash
# Configurer la rotation dans /etc/docker/daemon.json
{
    "log-driver": "json-file",
    "log-opts": {
        "max-size": "10m",
        "max-file": "3"
    }
}

# Puis redemarrer Docker
sudo systemctl restart docker
```

### Logrotate (fichiers classiques)

```bash
# Creer /etc/logrotate.d/openclaw
/var/log/health-check.log
/var/log/backup.log
{
    daily
    rotate 14
    compress
    delaycompress
    missingok
    notifempty
}
```

## Quoi surveiller

Ne surveillez pas tout. Surveillez ce qui annonce un probleme :

| Signal | Ou le trouver | Action |
|---|---|---|
| "OOM" ou "Out of memory" | journalctl, docker logs | Augmenter la memoire ou optimiser |
| "Connection refused" | Docker logs | Service down, redemarrer |
| "Disk full" | journalctl | Nettoyer les logs, les tmp |
| "SSL certificate expired" | Nginx error log | Renouveler le certificat |
| "Too many connections" | PostgreSQL logs | Augmenter max_connections ou fix connection leak |
| "Permission denied" | Tout log | Verifier les droits utilisateur |
| Pics d'erreurs 5xx | Nginx access log | Investiguer le service backend |

## Erreurs courantes

**Ne jamais regarder les logs.** Vous ne les ouvrez que quand c'est casse. A ce moment, vous ne savez pas les lire et vous perdez du temps.

**Pas de rotation.** Les logs remplissent le disque. Le serveur plante. Ironie : c'est la panne la plus facile a prevenir.

**Trop de logs.** Le mode debug est active en production. Chaque requete genere 50 lignes. Le signal est noye dans le bruit. Utilisez le niveau INFO en production, DEBUG uniquement pour diagnostiquer.

**Logs sans timestamp.** Vos scripts ecrivent des logs sans date. Impossible de correler avec les autres logs. Toujours : `echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] message"`.

## Etapes

1. Identifiez ou sont vos logs (journalctl, Docker, fichiers).
2. Configurez la rotation (journald.conf, daemon.json, logrotate).
3. Testez que vous savez chercher une erreur : simulez un probleme, trouvez-le dans les logs.
4. Ajoutez des timestamps a vos scripts si ce n'est pas fait.
5. Definissez les 5 signaux a surveiller pour votre setup.

## Verification

- [ ] Vous savez ou trouver les logs de chaque composant.
- [ ] La rotation est configuree pour tous les logs.
- [ ] La taille totale des logs est connue (`journalctl --disk-usage`, `du -sh /var/log`).
- [ ] Vous savez filtrer les logs par erreur et par timestamp.
- [ ] Le mode debug est desactive en production.
