---
status: complete
audience: both
chapter: 05
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 5.15 -- Diagnostiquer et monitorer le gateway

> Le gateway est le premier composant a verifier quand quelque chose ne fonctionne pas. Cette section vous donne les reflexes, les commandes, et les scenarios de diagnostic specifiques au gateway.

**Pour qui :** tout le monde
**Prerequis :** gateway fonctionnel (section 2.15), terminal configure (section 3.19)
**Difficulte :** Debutant a intermediaire
**Temps de lecture :** 15 minutes

---

## Contexte

La section 5.11 (En cas de panne) couvre les diagnostics generaux. Mais le gateway merite sa propre section de diagnostic, pour une raison simple : **quand le gateway ne fonctionne pas, rien ne fonctionne.**

Le gateway est comme le standard telephonique d'une entreprise. Si le standard tombe, personne ne peut appeler personne — meme si les telephones individuels marchent parfaitement. Diagnostiquer le gateway est donc toujours la **premiere etape**, pas la derniere.

---

## Le reflexe : gateway d'abord

Quand quelque chose ne fonctionne pas, votre premier reflexe doit etre :

```bash
$ openclaw gateway status
```

Si le gateway repond :
- Le probleme est ailleurs (base de donnees, modele IA, configuration). Passez aux diagnostics specifiques.

Si le gateway ne repond pas :
- Tout le reste est en suspens. Concentrez-vous sur le gateway.

```bash
# Etape 1 : le service tourne-t-il ?
$ sudo systemctl status openclaw-gateway

# Etape 2 : les logs disent quoi ?
$ journalctl -u openclaw-gateway -n 50 --no-pager

# Etape 3 : le port est-il occupe par autre chose ?
$ ss -tlnp | grep :3000

# Etape 4 : redemarrer proprement
$ sudo systemctl restart openclaw-gateway
$ sleep 5
$ openclaw gateway status
```

---

## Les 7 scenarios de panne gateway

### 1. Le gateway ne demarre pas

**Symptome :** `systemctl status` montre "failed" ou "activating (auto-restart)"

| Cause probable | Commande de diagnostic | Fix |
|----------------|----------------------|-----|
| Port deja utilise | `ss -tlnp \| grep :3000` | Tuer le processus qui occupe le port, ou changer le port dans config.json |
| Node.js introuvable | `journalctl -u openclaw-gateway \| grep "not found"` | Verifier le wrapper script (section 2.15) : chemin nvm/node |
| Token Vault invalide | `journalctl -u openclaw-gateway \| grep -i "vault\|token\|auth"` | Verifier `/etc/openclaw/gateway.env` |
| Config JSON invalide | `cat ~/.openclaw/config.json \| python3 -m json.tool` | Corriger la syntaxe JSON |
| Ancien service en conflit | `systemctl --user list-units \| grep openclaw` | Desactiver l'ancien service (section 2.15, etape 0) |

### 2. Le gateway demarre mais crash en boucle

**Symptome :** Le service alterne entre "active" et "activating", les logs montrent des erreurs repetees.

```bash
# Voir la boucle dans les logs
$ journalctl -u openclaw-gateway --since "10 min ago" | grep -c "Started\|Stopped"
```

Si le compteur depasse 5, systemd va arreter les tentatives. Corrigez la cause racine, puis :

```bash
$ sudo systemctl reset-failed openclaw-gateway
$ sudo systemctl start openclaw-gateway
```

### 3. Le gateway tourne mais ne repond pas

**Symptome :** `systemctl status` montre "active (running)" mais `openclaw gateway status` timeout.

| Cause probable | Diagnostic | Fix |
|----------------|-----------|-----|
| Le gateway ecoute sur la mauvaise interface | `ss -tlnp \| grep :3000` — verifier l'IP | Corriger `gateway.host` dans config.json |
| Firewall bloque le port | `sudo ufw status` | `sudo ufw allow 3000/tcp` (si necessaire) |
| Le gateway est bloque (deadlock) | Les logs s'arretent a un moment precis | Redemarrer : `sudo systemctl restart openclaw-gateway` |
| Trop de connexions | `ss -tn \| grep :3000 \| wc -l` | Redemarrer, investiguer les clients |

### 4. Le health check echoue

**Symptome :** `openclaw health` montre des composants en rouge.

Le gateway fait le health check de tous les composants. Quand un composant est rouge, ce n'est pas le gateway qui est en panne — c'est le composant qu'il surveille.

```bash
# Health check detaille
$ openclaw health

# Verifier chaque composant individuellement
$ docker exec supabase_db psql -U oa_admin -d oa_system -c "SELECT 1;"     # PostgreSQL
$ docker exec vault vault status                                            # Vault
$ curl -s https://openrouter.ai/api/v1/models | head -1                    # OpenRouter
```

### 5. Les sessions ne fonctionnent plus

**Symptome :** `openclaw chat` ne repond pas, ou les sessions sont vides.

```bash
# Verifier les sessions
$ openclaw sessions

# Verifier la connexion au modele IA
$ openclaw model test

# Verifier les logs pour des erreurs modele
$ journalctl -u openclaw-gateway | grep -i "error\|failed\|timeout" | tail -20
```

Cause frequente : un changement de modele IA ou une cle API expiree (voir section 5.11, "L'agent ne repond pas").

### 6. Le mode remote ne se connecte plus

**Symptome :** Le client remote affiche "Connection refused" ou "Authentication failed".

```bash
# Cote maitre : verifier que le gateway ecoute sur le bon port
$ ss -tlnp | grep :18789

# Cote maitre : verifier les tokens
$ openclaw gateway token list

# Cote client : verifier la configuration remote
$ cat ~/.openclaw/gateway.json

# Tester la connectivite reseau
$ tailscale ping ip-du-maitre      # Si Tailscale
$ nc -zv ip-du-maitre 18789        # Test TCP direct
```

Voir section 3.18 pour les erreurs courantes du mode remote.

### 7. Les performances se degradent

**Symptome :** Le gateway repond lentement, les commandes prennent plus de temps que d'habitude.

```bash
# Verifier l'utilisation des ressources
$ top -p $(pgrep -f "openclaw gateway")

# Verifier l'espace disque (les logs peuvent saturer)
$ df -h /
$ journalctl --disk-usage

# Verifier le nombre de sessions actives
$ openclaw sessions | wc -l

# Si trop de logs
$ sudo journalctl --vacuum-size=200M
```

---

## Monitoring natif du gateway

Avant d'installer des outils de monitoring supplementaires, exploitez ce que le gateway offre nativement.

### Endpoint health

```bash
# Health check simple
$ curl -s http://127.0.0.1:3000/health

# Health check depuis un script (retour 0 = OK, 1 = KO)
$ curl -sf http://127.0.0.1:3000/health > /dev/null && echo "OK" || echo "KO"
```

### Cron de surveillance (niveau 1 — zero outil supplementaire)

```bash
# Ajouter au crontab : surveillance toutes les 5 minutes
$ crontab -e
```

```cron
*/5 * * * * curl -sf http://127.0.0.1:3000/health > /dev/null || /chemin/vers/alerte-telegram.sh "Gateway KO"
```

C'est le monitoring le plus simple et le plus fiable. Pas de container supplementaire, pas d'interface web, pas de configuration. Si le gateway ne repond pas au health check, vous recevez un message Telegram.

### Commandes de monitoring quotidien

| Commande | Ce qu'elle montre | Frequence |
|----------|------------------|-----------|
| `openclaw gateway status` | Etat general, uptime, connexions | 1x/jour (matin) |
| `openclaw health` | Sante de tous les composants | 1x/jour ou apres un doute |
| `openclaw sessions --today` | Activite de la journee | 1x/jour (soir) |
| `journalctl -u openclaw-gateway -n 50 --no-pager` | Derniers evenements | Quand quelque chose semble lent |

### Quand ajouter un outil de monitoring

Le monitoring natif suffit si :
- Vous etes seul ou en petite equipe
- Vous avez moins de 5 services
- Vous n'avez pas besoin d'historique graphique

Passez a Uptime Kuma (section 5.10, niveau 2) quand :
- Vous voulez un historique d'uptime
- Vous voulez une page de statut publique
- Vous avez 5+ services a surveiller

Passez a Prometheus + Grafana (section 5.10, niveau 3) quand :
- Vous avez des SLA contractuels
- Vous avez une equipe ops dediee
- Vous gerez 10+ services sur plusieurs serveurs

---

## Cascade : quand le gateway tombe, que se passe-t-il

Comprendre la cascade aide a diagnostiquer :

```
Le gateway tombe
     │
     ├── Les commandes CLI ne repondent plus
     │   (openclaw status, openclaw chat, openclaw health)
     │
     ├── Les agents s'arretent
     │   (pas de routing vers le modele IA)
     │
     ├── Les crons echouent
     │   (les taches planifiees utilisent le gateway)
     │
     ├── Le mode remote se deconnecte
     │   (les clients perdent la connexion WebSocket)
     │
     └── Les notifications continuent
         (Telegram est independant du gateway)
```

**Point important :** Telegram est le seul canal qui fonctionne quand le gateway est down. C'est pourquoi le cron de surveillance doit envoyer ses alertes via Telegram, pas via le gateway.

---

## Template de diagnostic rapide

Copiez et executez ce bloc quand quelque chose ne fonctionne pas :

```bash
echo "=== DIAGNOSTIC GATEWAY ==="
echo "1. Service systemd :"
sudo systemctl is-active openclaw-gateway
echo ""
echo "2. Port 3000 :"
ss -tlnp | grep :3000
echo ""
echo "3. Health check :"
curl -sf http://127.0.0.1:3000/health && echo "OK" || echo "KO"
echo ""
echo "4. Derniers logs :"
journalctl -u openclaw-gateway -n 10 --no-pager
echo ""
echo "5. Ressources :"
echo "Disque : $(df -h / | tail -1 | awk '{print $5}') utilise"
echo "RAM : $(free -h | grep Mem | awk '{print $3}') / $(free -h | grep Mem | awk '{print $2}')"
echo "=== FIN ==="
```

Enregistrez-le dans `~/scripts/diag-gateway.sh` pour l'avoir sous la main :

```bash
$ chmod +x ~/scripts/diag-gateway.sh
$ ~/scripts/diag-gateway.sh
```

---

## Erreurs courantes

**Chercher ailleurs avant de verifier le gateway.** Le gateway est le premier check, toujours. Si `openclaw gateway status` ne repond pas, inutile de debugger la base de donnees ou le modele IA.

**Redemarrer sans lire les logs.** `sudo systemctl restart openclaw-gateway` est tentant. Mais si vous ne lisez pas les logs d'abord, le meme probleme reviendra.

**Pas de cron de surveillance.** Si le gateway tombe a 3h du matin, personne ne le saura avant le lendemain. Un cron + Telegram coute 5 minutes a configurer et vous previent immediatement.

**Confondre "le gateway est down" et "un composant est down".** Si `openclaw gateway status` repond mais `openclaw health` montre un composant rouge, c'est le composant qui a un probleme — pas le gateway.

---

## Verification

- [ ] Vous savez que le premier reflexe est `openclaw gateway status`.
- [ ] Le script `diag-gateway.sh` est installe et fonctionne.
- [ ] Un cron de surveillance du gateway est en place (ou prevu).
- [ ] Vous comprenez la cascade : gateway down = tout down sauf Telegram.
- [ ] Vous connaissez la difference entre "gateway down" et "composant down".

---

## Temps estime

15 minutes (lecture + installation du script de diagnostic).
