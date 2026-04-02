---
status: complete
audience: both
chapter: 06
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 01 -- Agence digitale (2 associes + agents IA)

**Pour qui :** duo d'entrepreneurs gerant une agence digitale avec des agents IA comme force de travail principale
**Temps de mise en place :** 2 a 4 semaines
**Difficulte :** Intermediaire a Avance

---

## Contexte

Deux associes lancent une agence digitale. Leur particularite : l'equipe permanente se limite a eux deux. Le reste de la force de travail repose sur des agents IA configures pour executer des taches operationnelles -- redaction, recherche, communication, gestion de projet.

Le defi : creer un systeme nerveux central qui coordonne les humains et les agents, sans dependre d'un SaaS ferme, et en gardant le controle total sur les donnees.

---

## Probleme

- Pas de visibilite centralisee sur les projets en cours
- Les agents IA fonctionnent en silos (un par tache, sans memoire partagee)
- La communication entre les fondateurs passe par trop de canaux differents
- Aucun systeme de suivi des couts d'utilisation des API IA
- Les fichiers clients sont disperses entre machines locales et services cloud

---

## Configuration

### Infrastructure

| Composant | Choix | Cout mensuel |
|-----------|-------|-------------|
| Serveur | VPS Hetzner (CPX21, Nuremberg ou Helsinki) | 10.00 EUR |
| OS | Ubuntu 24.04 LTS | -- |
| Reseau prive | Tailscale | gratuit (plan personnel) |
| Secrets | Vault (HashiCorp, mode dev puis production) | -- |
| Base de donnees | PostgreSQL 16 | -- |
| Communication | Mattermost (self-hosted) | -- |
| Cockpit web | Next.js + API Routes | -- |

**Cout infrastructure total : environ 10 EUR/mois**

### Repartition budgetaire par pilier (schema JD6)

Le schema JD6 organise les domaines operationnels en categories numerotees. Pour cette agence, la repartition budgetaire mensuelle est la suivante :

| Pilier | Domaine | Budget mensuel | Description |
|--------|---------|---------------|-------------|
| 10 | Infra | 10.00 EUR | VPS, domaine, DNS |
| 30 | Agents | 30.00 EUR | API Claude, Mistral, credits LLM |
| 40 | Knowledge | 40.00 EUR | Embeddings, stockage vectoriel, RAG |
| 50 | Communication | 50.00 EUR | Mattermost, email transactionnel |
| 60 | Business | 60.00 EUR | Outils clients, CRM leger, facturation |

**Budget operationnel total : environ 190 EUR/mois**

### Architecture des agents

L'agence deploie un agent principal et des agents specialises :

**Agent principal (orchestrateur) :**
- Tourne sur le VPS, accessible via le cockpit web
- Recoit les instructions des fondateurs via Mattermost ou le cockpit
- Delegue aux agents specialises selon le type de tache
- Maintient un journal d'activite dans PostgreSQL

**Agents specialises :**
- Agent Redaction : propositions commerciales, contenus marketing, emails clients
- Agent Recherche : veille concurrentielle, analyse de marche, documentation technique
- Agent Ops : monitoring serveur, alertes, rapports de cout

### Schema JD6 -- Organisation des domaines

```
10-19  Infrastructure    (serveurs, reseau, DNS, backups)
20-29  Securite          (Vault, acces, audit, RGPD)
30-39  Agents IA         (configuration, prompts, memoire, couts)
40-49  Knowledge         (base de connaissances, embeddings, RAG)
50-59  Communication     (Mattermost, email, notifications)
60-69  Business          (clients, projets, facturation, CRM)
70-79  Reporting         (dashboards, metriques, KPIs)
```

Chaque domaine a un dossier correspondant dans la knowledge base et un canal dedie dans Mattermost.

---

## Mise en place -- Etapes cles

### Semaine 1 : Infrastructure

1. Provisionner le VPS Hetzner
2. Installer Ubuntu 24.04, durcir SSH (cles uniquement, port non standard)
3. Installer Tailscale sur le VPS et les machines des fondateurs
4. Deployer PostgreSQL, creer les bases `openclaw_main` et `openclaw_knowledge`
5. Installer Vault, configurer les secrets pour les cles API

### Semaine 2 : Agents et Knowledge

1. Installer OpenClaw sur le VPS
2. Configurer l'agent principal avec le system prompt de l'agence
3. Connecter la knowledge base (documents fondateurs, templates, procedures)
4. Deployer les agents specialises avec leurs prompts respectifs
5. Tester le pipeline : instruction -> agent -> resultat -> stockage

### Semaine 3 : Communication et cockpit

1. Deployer Mattermost, creer les canaux par domaine JD6
2. Configurer les webhooks entre OpenClaw et Mattermost
3. Deployer le cockpit Next.js avec authentification
4. Connecter le cockpit a PostgreSQL pour le tableau de bord
5. Tester le flux complet : cockpit -> agent -> Mattermost -> fondateur

### Semaine 4 : Stabilisation

1. Configurer les backups automatiques (PostgreSQL + fichiers)
2. Mettre en place le monitoring des couts API
3. Documenter les procedures internes
4. Former les deux fondateurs sur le cockpit
5. Passer Vault en mode production

---

## Resultat

Apres un mois de mise en place :

- **Cockpit operationnel** : les fondateurs voient l'etat de tous les projets, les couts API en temps reel, et l'activite des agents depuis une interface unique
- **Agent principal fonctionnel** : il recoit les instructions en langage naturel, les route vers l'agent specialise, et renvoie le resultat avec un lien vers le document produit
- **Communication structuree** : chaque domaine JD6 a son canal Mattermost. Les agents postent leurs resultats dans le canal correspondant. Les fondateurs ne cherchent plus l'information
- **Couts maitrises** : le budget mensuel total reste sous 200 EUR, avec une visibilite complete sur la repartition
- **Souverainete des donnees** : tout tourne sur un VPS europeen. Aucune donnee client ne transite par un service tiers non maitrise

---

## Lecons apprises

1. **Commencer par l'agent principal, pas par les agents specialises.** L'orchestrateur est le point d'entree de tout le systeme. Sans lui, les agents specialises sont des outils isoles.

2. **Vault des le debut, pas "plus tard".** Les cles API en variables d'environnement dans des fichiers `.env` ne passent pas a l'echelle. Vault ajoute de la complexite initiale mais evite les fuites de secrets.

3. **Un canal Mattermost par domaine, pas par projet.** Les projets vont et viennent. Les domaines sont stables. Organiser la communication par domaine JD6 evite la proliferation de canaux morts.

4. **Le cockpit est un investissement, pas un luxe.** Sans interface visuelle, les fondateurs retombent dans les terminaux et les fichiers de log. Le cockpit Next.js prend du temps a construire mais change la qualite de vie operationnelle.

5. **Documenter les prompts comme du code.** Chaque prompt d'agent est versionne dans Git, avec un changelog. Les modifications sont tracees et reversibles.

---

## Erreurs courantes

| Erreur | Consequence | Solution |
|--------|-------------|----------|
| Deployer tous les agents en meme temps | Debuggage impossible, couts qui explosent | Deployer un agent a la fois, valider, puis passer au suivant |
| Ignorer les limites de tokens | Reponses tronquees, contexte perdu | Configurer des limites explicites et un systeme de chunking |
| Pas de backup PostgreSQL | Perte de la knowledge base | Cron job pg_dump quotidien, copie hors VPS |
| Mattermost sans authentification forte | Acces non autorise aux canaux agents | SSO ou tokens d'acces avec expiration |

---

## Template -- System prompt de l'agent principal

```
Tu es l'agent principal de [NOM DE L'AGENCE].

Ton role est de coordonner les operations entre les fondateurs et les agents specialises.

Regles :
- Tu reponds toujours en francais sauf si on te demande explicitement l'anglais
- Tu postes tes resultats dans le canal Mattermost correspondant au domaine JD6
- Tu ne prends jamais de decision financiere sans validation humaine
- Tu documentes chaque action dans la base PostgreSQL
- Tu signales immediatement toute anomalie de cout API

Domaines JD6 :
10-19 Infrastructure | 20-29 Securite | 30-39 Agents | 40-49 Knowledge
50-59 Communication | 60-69 Business | 70-79 Reporting

Quand tu recois une instruction :
1. Identifie le domaine JD6 concerne
2. Verifie si un agent specialise existe pour ce domaine
3. Si oui, delegue avec le contexte necessaire
4. Si non, traite directement et signale qu'un agent specialise serait utile
5. Poste le resultat dans le canal Mattermost du domaine
```

---

## Verification

- [ ] Le VPS repond sur Tailscale depuis les machines des fondateurs
- [ ] Vault stocke au moins les cles API LLM
- [ ] L'agent principal repond a une instruction simple via le cockpit
- [ ] Les resultats apparaissent dans le bon canal Mattermost
- [ ] Le backup PostgreSQL fonctionne et a ete teste en restauration
- [ ] Les couts API du mois sont visibles dans le cockpit

---

*Ce cas d'usage est inspire d'une experience reelle de mise en place. Les montants et configurations sont representatifs d'un deploiement en Europe en 2026.*
