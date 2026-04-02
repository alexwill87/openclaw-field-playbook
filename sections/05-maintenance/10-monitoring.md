---
status: complete
audience: both
chapter: 05
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 5.10 -- Monitoring et alertes

## Contexte

Le monitoring repond a une question simple : est-ce que tout tourne ? Et si non, depuis quand et pourquoi ? Sans monitoring, vous decouvrez les pannes quand vos utilisateurs vous ecrivent. Avec monitoring, vous les decouvrez avant eux.

Trois niveaux. Commencez par le premier. Montez quand le besoin se manifeste.

## Niveau 1 : simple (cron + Telegram)

C'est le health check de la section 5.1 sur un cron, avec alerte Telegram. Zero infrastructure supplementaire.

### Ce que ca couvre

- Services up/down.
- Espace disque.
- PostgreSQL accessible.
- Certificats SSL valides.

### Ce que ca ne couvre pas

- Historique des metriques (pas de graphes).
- Temps de reponse.
- Metriques applicatives (requetes/seconde, erreurs).
- Monitoring depuis l'exterieur (si le serveur tombe completement, le cron ne s'execute pas).

### Mise en place

Voir section 5.1. Resume :

```bash
# Cron toutes les 4 heures
0 */4 * * * /opt/scripts/health-check.sh --quiet

# Alerte Telegram si KO
```

Temps de mise en place : 30 minutes.
Cout : 0 EUR.

## Niveau 2 : intermediaire (Uptime Kuma)

Uptime Kuma est un outil de monitoring self-hosted. Interface web, historique, notifications multiples.

### Installation

```bash
# Via Docker (la methode recommandee)
docker run -d \
  --name uptime-kuma \
  --restart unless-stopped \
  -p 3001:3001 \
  -v uptime-kuma-data:/app/data \
  louislam/uptime-kuma:1

# Ou dans docker-compose.yml
services:
  uptime-kuma:
    image: louislam/uptime-kuma:1
    container_name: uptime-kuma
    restart: unless-stopped
    ports:
      - "3001:3001"
    volumes:
      - uptime-kuma-data:/app/data

volumes:
  uptime-kuma-data:
```

### Configuration

1. Ouvrez `http://votre-ip:3001`.
2. Creez un compte admin.
3. Ajoutez des moniteurs :

| Type | URL/Commande | Intervalle |
|---|---|---|
| HTTP | `http://localhost:3000` (cockpit) | 60s |
| HTTP | `http://localhost:8080` (API) | 60s |
| TCP | `localhost:5432` (PostgreSQL) | 120s |
| HTTP Keyword | `https://votre-domaine.com` + mot-cle attendu | 300s |

4. Configurez les notifications : Telegram, email, ou Slack.

### Ce que ca ajoute

- Historique d'uptime (graphes).
- Temps de reponse moyen.
- Notifications flexibles (multi-canal).
- Page de statut publique (optionnel).
- Monitoring depuis le meme serveur (limitation : si le serveur tombe, Uptime Kuma tombe aussi).

Temps de mise en place : 1 heure.
Cout : 0 EUR (self-hosted).

## Niveau 3 : avance (Grafana + Prometheus)

Pour ceux qui ont besoin de metriques detaillees, de dashboards personnalises, et de monitoring distribue.

### Stack

```
Prometheus : collecte les metriques (CPU, RAM, disque, requetes).
Node Exporter : expose les metriques systeme pour Prometheus.
Grafana : affiche les dashboards.
AlertManager : gere les alertes.
```

### Installation (Docker Compose)

```yaml
services:
  prometheus:
    image: prom/prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus-data:/prometheus
    ports:
      - "9090:9090"

  node-exporter:
    image: prom/node-exporter
    ports:
      - "9100:9100"
    pid: host
    volumes:
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro

  grafana:
    image: grafana/grafana
    ports:
      - "3002:3000"
    volumes:
      - grafana-data:/var/lib/grafana
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=changeme

volumes:
  prometheus-data:
  grafana-data:
```

### Quand c'est justifie

- Vous gerez 3+ services avec des SLA.
- Vous avez besoin de correler CPU/memoire/reseau avec les performances applicatives.
- Vous avez une equipe qui consulte les dashboards.
- Vous facturez de l'uptime a vos clients.

### Quand c'est du over-engineering

- Vous etes seul avec 2 containers.
- Personne ne regarde les dashboards.
- Un cron + Telegram suffit pour votre usage.

Temps de mise en place : 4-8 heures.
Cout : 0 EUR (self-hosted) + temps de maintenance.

## Recommandation

**Commencez par le niveau 1.** Toujours. Ca prend 30 minutes et ca couvre 80% des besoins.

Passez au niveau 2 quand :
- Vous voulez un historique d'uptime.
- Vous avez 5+ services a surveiller.
- Vous voulez une page de statut.

Passez au niveau 3 quand :
- Vous avez des SLA a respecter.
- Vous avez besoin de metriques fines (latence p99, throughput).
- Vous gerez plusieurs serveurs.

La plupart des setups solo n'auront jamais besoin du niveau 3.

## Erreurs courantes

**Installer Grafana + Prometheus pour 2 containers.** Over-engineering. Vous passez plus de temps a maintenir le monitoring qu'a maintenir l'application.

**Pas de monitoring externe.** Tout votre monitoring tourne sur le meme serveur. Si le serveur tombe, le monitoring aussi. Solution niveau 1 : un service externe gratuit (UptimeRobot, Hetrixtools) pour le ping basique.

**Trop d'alertes.** Vous recevez 20 alertes par jour. Vous les ignorez toutes. Finissez par ignorer la vraie panne. Reglez les seuils pour n'alerter que sur les vrais problemes.

**Pas d'alerte du tout.** Le monitoring tourne, les logs se remplissent, mais personne n'est notifie. Un monitoring sans alerte est un monitoring sans valeur.

## Etapes

1. Installez le niveau 1 (section 5.1 : health-check.sh + cron + Telegram).
2. Utilisez pendant 2 semaines.
3. Evaluez : est-ce suffisant ?
4. Si non, installez Uptime Kuma (niveau 2).
5. Ajoutez un ping externe gratuit pour couvrir la panne complete du serveur.

## Verification

- [ ] Un monitoring est actif (au minimum niveau 1).
- [ ] Les alertes fonctionnent (testees avec une panne simulee).
- [ ] Le nombre d'alertes par jour est raisonnable (< 3 en temps normal).
- [ ] Un monitoring externe ping votre serveur.
- [ ] Vous savez en moins de 5 minutes si un service est down.
