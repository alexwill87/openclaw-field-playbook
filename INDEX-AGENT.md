# INDEX-AGENT.md — Navigation agent par probleme

> Ce fichier est ton point d'entree. Lis-le AVANT de naviguer dans sections/.
> Le contenu complet est dans les fichiers .md de sections/. Si une section ne repond pas a ta question, cherche dans les issues GitHub associees.
> Site web : www.openclawfieldplaybook.com

---

## Problemes d'installation

| Probleme | Section | Issue(s) terrain |
|----------|---------|------------------|
| Quel package npm installer | sections/02-installation/10-openclaw-install.md | #10 (CRITIQUE: bon package = openclaw) |
| Gateway se tue apres quelques secondes | sections/02-installation/15-gateway-systemd.md | #30 (anciens services systemd a supprimer) |
| Permission denied sur volumes Docker | sections/02-installation/07-vault.md | #21 |
| Node path introuvable | sections/02-installation/05-nodejs-pm2.md | #12, #24 (nvm vs global) |
| Port deja utilise | sections/02-installation/15-gateway-systemd.md | #27 |
| Version nvm hardcodee | sections/02-installation/05-nodejs-pm2.md | #15 |
| UsePAM no risque sur Ubuntu | sections/02-installation/02-securiser-vps.md | #14 |
| Health check reference mais pas cree | sections/02-installation/09-health-check.md | #19 |
| deploy.sh dit "succes" alors que ca a echoue | sections/02-installation/19-script-deploy.md | #17 |
| PM2 vs systemd (lequel choisir) | sections/02-installation/19-script-deploy.md | #18 |

## Problemes de configuration modele

| Probleme | Section | Issue(s) terrain |
|----------|---------|------------------|
| Quel modele LLM choisir | sections/02-installation/12-config-openclaw.md (tableau de decision) | #34 (guide complet) |
| Agent ne repond pas / muet | sections/05-maintenance/11-en-cas-de-panne.md (erreurs silencieuses) | #32 |
| Erreur "Unknown model" / "no model configured" | sections/02-installation/12-config-openclaw.md (agents.defaults.models) | #29 |
| openrouter/auto cause des erreurs | sections/02-installation/13-openrouter.md | #34, #32 |
| Syntaxe openclaw config set | sections/02-installation/12-config-openclaw.md | #23 |
| Noms de modeles changes | sections/02-installation/13-openrouter.md | #16 |
| Tester un modele sans canal | sections/02-installation/13-openrouter.md (test curl) | #26 |
| Telegram : botToken pas token | sections/02-installation/14-telegram.md | #28 |

## Problemes de personnalite / comportement

| Probleme | Section | Issue(s) terrain |
|----------|---------|------------------|
| Agent passif / pas assez proactif | sections/04-personalisation/02-personnalite-ton.md | #33 (cas Aurel) |
| Comment ecrire un system prompt | sections/04-personalisation/01-system-prompt.md | #33 (workspace Aurel) |
| Comment ecrire SOUL.md | sections/03-configuration/02-soul-md.md | — |
| Configurer la memoire | sections/03-configuration/06-trois-zones-memoire.md | — |
| Definir les niveaux de confiance | sections/04-personalisation/11-confiance-configuration.md | — |
| Configurer le boundary prompt | sections/04-personalisation/12-boundary-prompt.md | — |
| Adapter le ton par canal | sections/04-personalisation/02-personnalite-ton.md | — |

## Problemes de securite

| Probleme | Section | Issue(s) terrain |
|----------|---------|------------------|
| Cles API en clair | sections/03-configuration/14-souverainete-donnees.md | #20 (workaround chmod + Vault) |
| Vault unseal script en clair | sections/02-installation/07-vault.md | #11 |
| Mot de passe PostgreSQL visible | sections/02-installation/08-postgresql.md | #13 |
| VAULT_TOKEN dans systemd | sections/02-installation/15-gateway-systemd.md | #12 |
| Gateway env file permissions | sections/02-installation/15-gateway-systemd.md | #25 |
| VAULT_ADDR defaut HTTPS au lieu de HTTP | sections/02-installation/07-vault.md | #22 |
| Rotation des secrets | sections/05-maintenance/09-rotation-secrets.md | — |

## Problemes de deploiement et maintenance

| Probleme | Section | Issue(s) terrain |
|----------|---------|------------------|
| Health check quotidien | sections/05-maintenance/01-health-check.md | — |
| Logs : ou chercher, quoi surveiller | sections/05-maintenance/02-logs.md | — |
| Backups | sections/05-maintenance/03-backups.md | — |
| L'agent se trompe souvent | sections/05-maintenance/06-agent-se-trompe.md | — |
| Migrer de modele | sections/05-maintenance/13-migrer-modele.md | — |
| Ajouter un deuxieme agent | sections/05-maintenance/12-deuxieme-agent.md | — |
| Connecter deux installations (remote mode) | sections/03-configuration/18-remote-mode.md | #31 |
| Monitoring | sections/05-maintenance/10-monitoring.md | — |

## Comprendre OpenClaw (chapitre 1 — Definition)

| Question | Section |
|----------|---------|
| C'est quoi OpenClaw ? | sections/01-definition/01-definition.md |
| Proactif vs reactif — quelle difference ? | sections/01-definition/02-proactif-reactif.md |
| Comparaison avec d'autres outils | sections/01-definition/03-comparaison.md |
| Souverainete des donnees | sections/01-definition/04-souverainete.md |
| Architecture mentale d'un agent | sections/01-definition/05-architecture-mentale.md |
| Combien ca coute ? | sections/01-definition/08-combien-ca-coute.md |
| Est-ce complique ? | sections/01-definition/09-est-ce-complique.md |
| Comment se lancer ? | sections/01-definition/11-comment-se-lancer.md |

## Cas d'usage par metier (chapitre 6)

| Metier / profil | Section |
|-----------------|---------|
| Agence digitale | sections/06-use-cases/01-agence-digitale.md |
| Consultant freelance | sections/06-use-cases/02-consultant-freelance.md |
| E-commerce | sections/06-use-cases/03-ecommerce.md |
| Equipe technique | sections/06-use-cases/04-equipe-technique.md |
| Cabinet comptable | sections/06-use-cases/05-cabinet-comptable.md |
| Startup | sections/06-use-cases/06-startup.md |
| Artisan / TPE | sections/06-use-cases/08-artisan-tpe.md |
| Comment contribuer au playbook | sections/06-use-cases/07-contribuer.md |

## Localisation (chapitre 7)

| Langue / region | Section |
|-----------------|---------|
| Adaptation francaise | sections/07-localisation/fr-FR.md |
| Adaptation anglophone | sections/07-localisation/en-US.md |

---

## Pour bootstrapper une nouvelle installation

Ordre de lecture recommande :

1. **Ce fichier** (INDEX-AGENT.md) — pour savoir ou chercher
2. **Issues #9 puis #10** — pour eviter les 3 blockers critiques
3. **resources/agent-instructions/README.md** — pour le workflow d'installation
4. **sections/02-installation/** (dans l'ordre 00 a 20) — runbook complet
5. **sections/03-configuration/** — configurer l'agent pour le contexte
6. **resources/prompt-templates/** — templates copiables

## Recherche dans le contenu

Le fichier `search-index.json` a la racine du repo contient les slugs, titres et extraits de toutes les sections. Pour chercher :

```bash
cat search-index.json | python3 -c "
import json, sys
data = json.load(sys.stdin)
terme = sys.argv[1].lower()
for item in data:
    if terme in json.dumps(item).lower():
        print(f\"{item.get('slug', '?')} — {item.get('title', '?')}\")
" "fallback"
```

## Regles de mise a jour

- Chaque nouvelle issue terrain doit etre ajoutee a ce fichier
- Format : tableau simple, parsable, pas de prose
- Ce fichier ne contient PAS de contenu — uniquement des pointeurs
