# OpenClaw Install Tracker

Cockpit minimal pour suivre une installation OpenClaw etape par etape.

**Cet outil est optionnel.** Le playbook fonctionne sans. Mais si vous voulez tracer votre progression, vos decisions et l'etat de vos services en temps reel, ce tracker est fait pour ca.

## Fonctionnalites

- **Checklist live** des 11 phases d'installation avec statuts et timestamps
- **Registre des decisions** (Vault ou .env ? PM2 ou systemd ?)
- **Registre des services** (ports, statuts, acces)
- **Log des actions** (succes, echecs, warnings)
- **Export JSON** de l'etat complet
- **API REST** pour alimenter le tracker depuis des scripts
- **Dark mode** automatique
- **Zero dependance externe** (SQLite embarque, pas besoin de PostgreSQL)

## Installation rapide

### Option A : Docker (recommande)

```bash
cd tools/install-tracker
docker compose up -d
```

Accessible sur `http://localhost:3007`

### Option B : Node.js direct

```bash
cd tools/install-tracker
npm install
npm start
```

### Option C : Depuis le repo playbook

Si vous avez clone le playbook complet :

```bash
cd openclaw-field-playbook/tools/install-tracker
docker compose up -d
```

## API

Tous les endpoints retournent du JSON.

| Methode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/api/phases` | Liste des phases |
| PATCH | `/api/phases/:id` | Mettre a jour statut/notes |
| GET | `/api/decisions` | Liste des decisions |
| POST | `/api/decisions` | Ajouter une decision |
| GET | `/api/services` | Liste des services |
| PUT | `/api/services/:id` | Ajouter/modifier un service |
| GET | `/api/actions` | Log des actions |
| POST | `/api/actions` | Logger une action |
| GET | `/api/state` | Export complet |
| POST | `/api/state` | Import complet |

### Exemples curl

```bash
# Marquer une phase comme en cours
curl -X PATCH http://localhost:3007/api/phases/phase-02 \
  -H 'Content-Type: application/json' \
  -d '{"status": "en_cours"}'

# Logger une action
curl -X POST http://localhost:3007/api/actions \
  -H 'Content-Type: application/json' \
  -d '{"action": "Docker installe", "result": "success", "phase_id": "phase-01"}'

# Enregistrer un service
curl -X PUT http://localhost:3007/api/services/vault \
  -H 'Content-Type: application/json' \
  -d '{"name": "Vault", "port": 8200, "status": "running", "access_type": "localhost"}'

# Enregistrer une decision
curl -X POST http://localhost:3007/api/decisions \
  -H 'Content-Type: application/json' \
  -d '{"question": "Vault ou .env ?", "choice": "Vault", "reason": "Multi-utilisateurs prevu", "phase_id": "phase-02"}'

# Exporter l'etat complet
curl http://localhost:3007/api/state > install-state.json
```

## Configuration nginx (optionnel)

Si vous voulez exposer le tracker sur un domaine :

```nginx
server {
    server_name mission.votre-domaine.com;
    location / {
        proxy_pass http://127.0.0.1:3007;
        proxy_set_header Host $host;
    }
}
```

## Stack technique

- Express.js (serveur HTTP)
- better-sqlite3 (base de donnees embarquee)
- HTML/CSS/JS vanilla (pas de build, pas de framework frontend)
- Docker optionnel

## Licence

Meme licence que le playbook : CC-BY 4.0
