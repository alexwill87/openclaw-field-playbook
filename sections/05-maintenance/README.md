---
status: complete
audience: both
chapter: 05
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# Chapitre 5 -- Maintenance

> Garder votre setup OpenClaw performant, fiable et digne de confiance dans la duree.

## Partie A -- Operations quotidiennes

- **5.1** -- [Health check quotidien](01-health-check.md)
  Script diagnostic. Automatiser avec cron. Alertes Telegram.

- **5.2** -- [Gestion des logs](02-logs.md)
  Ou les trouver, comment les lire, rotation, quoi surveiller.

- **5.3** -- [Backups](03-backups.md)
  pg_dump, snapshots Hetzner, fichiers critiques. Test de restauration.

## Partie B -- Maintenance agent

- **5.4** -- [Revoir le system prompt](04-revoir-system-prompt.md)
  Frequence, declencheurs, quoi preserver vs reecrire.

- **5.5** -- [Derive de la memoire](05-derive-memoire.md)
  Memoire obsolete ou contradictoire. Nettoyage periodique.

- **5.6** -- [Quand l'agent se trompe](06-agent-se-trompe.md)
  Protocole : diagnostic, correction, prevention.

- **5.7** -- [Mettre a jour les integrations](07-maj-integrations.md)
  API qui change. Adapter sans casser.

## Partie C -- Maintenance infra

- **5.8** -- [Mises a jour systeme](08-maj-systeme.md)
  Ubuntu, Docker, Node.js, Vault. Quand NE PAS mettre a jour.

- **5.9** -- [Rotation des secrets](09-rotation-secrets.md)
  Pourquoi, comment, frequence.

- **5.10** -- [Monitoring et alertes](10-monitoring.md)
  Simple (cron+Telegram), intermediaire (Uptime Kuma), avance (Grafana).

- **5.11** -- [En cas de panne](11-en-cas-de-panne.md)
  Tableau diagnostic par symptome. Pour chaque : diagnostic, fix, prevention.

## Partie D -- Evolution

- **5.12** -- [Quand ajouter un deuxieme agent](12-deuxieme-agent.md)
  Signes, structure, isolation, communication.

- **5.13** -- [Migrer vers un autre modele](13-migrer-modele.md)
  Comment tester sans casser. Comparaison A/B. Garder le fallback.

- **5.14** -- [Mesurer le ROI](14-mesurer-roi.md)
  Temps gagne, decisions ameliorees, erreurs evitees.

---

Specifications locales : voir `sections/07-localisation/`

---

[Contribuer a ce chapitre](https://github.com/alexwill87/openclawfieldplaybook/issues/new?template=suggestion.yml) -- [CONTRIBUTING.md](../../CONTRIBUTING.md)
