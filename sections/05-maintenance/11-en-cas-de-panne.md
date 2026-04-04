---
status: complete
audience: both
chapter: 05
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 5.11 -- En cas de panne

## Contexte

Une panne, ca arrive. Le reflexe : ne pas paniquer, diagnostiquer, corriger, prevenir. Ce guide vous donne un tableau de diagnostic par symptome pour les pannes les plus courantes.

## Reflexe en cas de panne

1. **Ne pas toucher a tout en meme temps.** Un diagnostic a la fois.
2. **Noter l'heure.** Quand ca a commence. Pour correler les logs.
3. **Verifier le plus simple d'abord.** Le serveur est-il up ? Le service tourne-t-il ? L'espace disque est-il plein ?

## Tableau diagnostic

### Le site/service ne repond pas

| Diagnostic | Commande | Fix |
|---|---|---|
| Le container est arrete | `docker ps -a` | `docker compose up -d` |
| Le port n'est pas expose | `ss -tlnp \| grep PORT` | Verifier docker-compose.yml ports |
| Nginx ne proxy pas | `nginx -t && systemctl status nginx` | Corriger la config, `systemctl restart nginx` |
| Le service crash au demarrage | `docker logs CONTAINER --tail 50` | Lire l'erreur, corriger, rebuild |
| DNS ne pointe pas | `dig votre-domaine.com` | Verifier la config DNS |

**Prevention :** health check automatise (section 5.1) + monitoring (section 5.10).

### Le serveur est inaccessible en SSH

| Diagnostic | Commande | Fix |
|---|---|---|
| Le serveur est down | Console Hetzner Cloud | Reboot depuis la console |
| SSH est bloque par le firewall | Console Hetzner > rescue mode | `ufw allow 22` |
| Disque plein (SSH ne peut pas creer de session) | Console Hetzner | Rescue mode, monter le disque, liberer de l'espace |
| Mauvaise cle SSH | Depuis votre machine : `ssh -vvv user@ip` | Verifier authorized_keys |

**Prevention :** ne jamais modifier ufw/iptables sans regle SSH confirmee. Snapshot avant modification reseau.

### La base de donnees ne repond pas

| Diagnostic | Commande | Fix |
|---|---|---|
| PostgreSQL est arrete | `systemctl status postgresql` | `systemctl start postgresql` |
| Trop de connexions | `psql -c "SELECT count(*) FROM pg_stat_activity;"` | Identifier les connexions fantomes, augmenter max_connections |
| Disque plein | `df -h /var/lib/postgresql` | Liberer de l'espace (logs, tmp) |
| Corruption | Logs PostgreSQL | Restaurer depuis le dernier backup (section 5.3) |
| Mauvais mot de passe (apres rotation) | `psql -U oa_admin -d cockpit` | Verifier le secret dans Vault, corriger |

**Prevention :** monitoring PostgreSQL + backup quotidien teste.

### Le disque est plein

| Diagnostic | Commande | Fix |
|---|---|---|
| Identifier quoi prend de la place | `du -sh /* \| sort -rh \| head -10` | Voir ci-dessous |
| Logs Docker | `du -sh /var/lib/docker/containers/` | Configurer la rotation (section 5.2) |
| Logs systeme | `journalctl --disk-usage` | `journalctl --vacuum-size=200M` |
| Vieux backups | `du -sh /var/backups/` | Supprimer les plus vieux, garder 7 jours |
| Images Docker inutilisees | `docker system df` | `docker system prune -a --filter "until=720h"` |
| Fichiers temporaires | `du -sh /tmp/` | `rm -rf /tmp/old-*` (avec discernement) |

**Prevention :** alerte a 80% d'utilisation disque dans le health check. Rotation des logs configuree.

### Un container redemarrerait en boucle

| Diagnostic | Commande | Fix |
|---|---|---|
| Erreur au demarrage | `docker logs CONTAINER --tail 100` | Lire l'erreur, corriger |
| Dependance manquante | `docker logs CONTAINER 2>&1 \| grep -i "error\|fatal"` | npm install, pip install, etc. |
| Variable d'environnement manquante | `docker inspect CONTAINER \| jq '.[0].Config.Env'` | Ajouter dans .env ou docker-compose.yml |
| Port deja utilise | `ss -tlnp \| grep PORT` | Arreter l'autre service ou changer le port |
| OOM Kill | `dmesg \| grep -i oom` | Augmenter la memoire ou optimiser l'app |

**Prevention :** `restart: unless-stopped` dans docker-compose.yml + health check + logs.

### L'agent ne fonctionne plus

| Diagnostic | Commande | Fix |
|---|---|---|
| API key invalide/expiree | Tester un appel API direct | Renouveler la cle |
| Rate limit atteint | Verifier les headers de reponse | Attendre ou changer de plan |
| Service API down | Verifier status.anthropic.com (ou equivalent) | Attendre |
| Configuration cassee | Lire .claude/ ou equivalent | Restaurer depuis backup |
| Modele deprece | Lire les logs d'erreur | Changer le modele dans la config |

**Prevention :** fallback sur un autre modele configure (section 5.13). Budget et rate limits surveilles.

### L'agent ne repond pas (muet) — erreurs LLM silencieuses

L'agent semble "endormi" : il recoit les messages mais ne repond pas, ou repond apres 5-6 tentatives. Ce n'est pas un bug OpenClaw, c'est un probleme de modele.

| Diagnostic | Commande | Fix |
|---|---|---|
| Erreur modele silencieuse (400/422) | Chercher `stopReason: "error"` dans les sessions JSONL : `grep -c '"stopReason":"error"' ~/.openclaw/sessions/*.jsonl` | Changer de modele primaire (voir section 2.12) |
| `openrouter/auto` route vers un modele incompatible | Verifier les sessions : `grep '"model"' ~/.openclaw/sessions/*.jsonl \| tail -20` | Remplacer `openrouter/auto` par un modele explicite |
| Erreur "Reasoning is mandatory" | `grep -i "reasoning" ~/.openclaw/sessions/*.jsonl` | Le modele exige `reasoning: true`. Changer de modele ou activer le parametre |
| Fallback fonctionne mais lent | Compter les erreurs primaires vs fallback dans les sessions | Le modele primaire echoue en silence, le fallback prend le relais apres timeout |
| Taux d'erreur eleve (>5%) | `grep -c "error" ~/.openclaw/sessions/SESSION.jsonl` | Changer de modele. Un bon setup a <1% d'erreurs |

**Cas terrain (Aurel, avril 2026)** : `openrouter/auto` a cause 11.6% d'erreurs silencieuses (erreur 400 "Reasoning is mandatory"). L'agent paraissait endormi pendant que le fallback Gemini Flash prenait le relais apres timeout. Solution : remplacer `openrouter/auto` par un modele explicite (`anthropic/claude-sonnet-4`).

**Prevention :**
- **Ne jamais utiliser `openrouter/auto` en production** — le routage automatique cause des incompatibilites (voir section 2.13).
- Verifier periodiquement les sessions JSONL pour detecter les erreurs silencieuses.
- Configurer au moins 2 modeles fallback de providers differents.
- Apres chaque changement de modele, envoyer un message test et verifier la reponse.

## Apres la panne

1. **Documenter.** Quoi, quand, cause, fix, duree.
2. **Prevenir.** Ajouter un check dans le health check, une regle dans le boundary prompt, un workflow dans WORKFLOWS.md.
3. **Tester la prevention.** Simuler la panne a nouveau et verifier que le monitoring la detecte.

### Template post-mortem

```markdown
## Incident — YYYY-MM-DD

**Symptome :** [ce qui a ete observe]
**Debut :** HH:MM — **Fin :** HH:MM — **Duree :** X min
**Cause :** [cause racine]
**Fix :** [ce qui a ete fait]
**Impact :** [qui/quoi a ete affecte]
**Prevention :** [mesure ajoutee pour eviter la recidive]
```

## Erreurs courantes

**Paniquer et toucher a tout.** Vous changez 3 configs en meme temps. Maintenant vous avez 4 problemes au lieu d'un.

**Pas de backup recent.** La restauration est impossible ou trop vieille. Voir section 5.3.

**Ne pas documenter.** La meme panne revient 3 mois plus tard et vous avez oublie le fix.

**Corriger sans comprendre.** "J'ai redemarre et ca marche." Jusqu'a la prochaine fois. Identifiez la cause racine.

## Verification

- [ ] Vous savez diagnostiquer les 7 scenarios ci-dessus.
- [ ] Les commandes de diagnostic sont testees et fonctionnent sur votre setup.
- [ ] Un template post-mortem existe.
- [ ] Les pannes passees sont documentees.
- [ ] Chaque panne a genere une mesure de prevention.
