---
status: complete
audience: both
chapter: 01
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 1.5 -- L'architecture mentale avant de commencer

**A qui s'adresse cette section :** Toute personne qui va installer et configurer OpenClaw. Lisez ceci avant de toucher au terminal.
**Temps de lecture :** 12 minutes.
**Difficulte :** Intermediaire.

### Contexte

Avant de lancer le moindre `docker compose up`, vous avez besoin d'un modele mental clair de ce que vous construisez. Sans ce modele, chaque decision de configuration sera un coup dans le noir.

### Les 3 couches

Toute installation OpenClaw s'organise en trois couches superposees :

```
+------------------------------------------+
|            3. ACTION                      |
|  Ce que vos agents font concretement     |
|  (envoyer, creer, modifier, alerter)     |
+------------------------------------------+
|            2. VISIBILITE                  |
|  Ce que vos agents savent                |
|  (memoire, contexte, outils, donnees)    |
+------------------------------------------+
|            1. IDENTITE                    |
|  Qui sont vos agents                     |
|  (roles, regles, limites, personnalite)  |
+------------------------------------------+
```

**Couche 1 -- Identite.** C'est le socle. Avant de donner des outils a un agent, definissez qui il est. Quel est son role ? Quelles sont ses limites ? Qu'a-t-il le droit de faire et de ne pas faire ? Un agent sans identite claire est un agent dangereux -- pas parce qu'il est malveillant, mais parce qu'il est imprevisible.

**Couche 2 -- Visibilite.** Une fois l'identite posee, definissez ce que l'agent sait. A quelles donnees a-t-il acces ? Quelle est sa memoire ? Quels outils peut-il utiliser ? Un agent qui a une identite claire mais pas de visibilite est un agent impuissant.

**Couche 3 -- Action.** Enfin, definissez ce que l'agent fait. Quelles actions concretes peut-il prendre ? Dans quelles conditions ? Avec quelles validations ? Un agent qui a identite + visibilite + capacite d'action est un agent operationnel.

> **Principe :** Toujours construire de bas en haut. Identite d'abord, visibilite ensuite, action en dernier. Inverser cet ordre est la source la plus frequente de problemes.

### Le concept de "piliers"

Un pilier est un **bloc fonctionnel** qui structure une installation OpenClaw. Pensez-y comme un domaine de responsabilite.

Il existe deux categories :

**Piliers universels** -- presents dans toute installation, quel que soit le metier :

| Pilier | Responsabilite |
|--------|---------------|
| **Infra** | L'infrastructure technique. Serveur, Docker, reverse proxy, certificats SSL, sauvegardes. C'est le sol sur lequel tout repose. |
| **Agents** | Les agents eux-memes. Leur configuration, leur orchestration, leurs interactions. |
| **Knowledge** | La base de connaissances. Memoire, contexte, documents de reference, regles metier. |

**Piliers metier** -- specifiques a votre activite :

Ces piliers dependent de ce que vous faites. Exemples :

| Metier | Piliers metier possibles |
|--------|------------------------|
| Consultant independant | Prospection, Livrables, Facturation |
| E-commerce | Catalogue, Commandes, Service client |
| Agence | Projets, Clients, Production |
| Formateur | Contenu, Apprenants, Planning |

Vous n'avez pas besoin de definir tous vos piliers metier avant de commencer. Commencez par les piliers universels. Les piliers metier emergeront naturellement au fur et a mesure que vous utilisez le systeme.

> **Erreur courante :** Vouloir definir l'architecture complete avant de commencer. Vous ne pouvez pas tout prevoir. Posez les piliers universels, construisez un premier agent fonctionnel, et laissez l'architecture evoluer avec l'usage.

> **Note de terrain :** Sur les installations que nous avons accompagnees, les piliers metier se stabilisent generalement apres 2 a 4 semaines d'usage reel. Pas avant. Toute tentative de les figer en amont produit une architecture qui ne correspond pas a la realite.
