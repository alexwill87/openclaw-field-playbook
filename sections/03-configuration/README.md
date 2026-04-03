---
status: complete
audience: both
chapter: 03
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 3. Configuration

> Configurer OpenClaw pour votre contexte specifique : votre metier, vos outils, vos contraintes.

L'installation (chapitre 2) vous donne un agent generique. La configuration en fait VOTRE agent. Ce chapitre couvre quatre axes : definir l'identite et les regles de l'agent, organiser sa memoire, le connecter a vos sources de donnees, et automatiser ses declenchements. A la fin, vous aurez un agent qui connait votre metier, respecte vos limites, et se reveille tout seul le matin.

**Debutant** : commencez par 3.1, 3.2, 3.3, 3.5, 3.6, 3.10, 3.16. Le reste viendra apres. **Presse** : 3.1 (5 min), 3.5 (5 min), 3.16 (5 min) -- un agent fonctionnel en 15 minutes. **Praticien** : lisez dans l'ordre, chaque section construit sur la precedente.

---

## Sommaire

### Partie A -- L'agent

- **3.1 -- [Perimetre de l'agent](01-perimetre-agent.md)**
  Definir explicitement ce que l'agent doit faire, peut faire, et ne doit jamais faire

- **3.2 -- [SOUL.md](02-soul-md.md)**
  Ecrire le document qui donne a l'agent son identite, ses valeurs et sa posture

- **3.3 -- [USER.md](03-user-md.md)**
  Decrire votre profil, vos preferences et votre contexte pour que l'agent s'adapte a vous

- **3.4 -- [AGENTS.md](04-agents-md.md)**
  Tenir le registre de tous les agents actifs, leur role et leurs permissions

- **3.5 -- [CONSTITUTION.md](05-constitution-md.md)**
  Fixer les regles du jeu : ce qui est negoociable, ce qui ne l'est pas

### Partie B -- La memoire

- **3.6 -- [Trois zones de memoire](06-trois-zones-memoire.md)**
  Comprendre l'architecture chaude/tiede/froide et ou stocker chaque type d'information

- **3.7 -- [MEMORY.md](07-memory-md.md)**
  Alimenter la memoire collective que tous les agents partagent entre les sessions

- **3.8 -- [knowledge/](08-knowledge.md)**
  Organiser le dossier de connaissances metier que l'agent consulte en contexte

### Partie C -- Les connexions

- **3.9 -- [Une source a la fois](09-principe-une-source.md)**
  Pourquoi connecter progressivement plutot que tout brancher d'un coup

- **3.10 -- [Calendrier](10-calendrier.md)**
  Brancher le calendrier en premier -- la connexion la plus simple et la plus utile

- **3.11 -- [Taches](11-taches.md)**
  Connecter le gestionnaire de taches et gerer la pression invisible des listes

- **3.12 -- [Email et messages](12-email-messages.md)**
  Configurer le triage automatique des emails et messages entrants

- **3.13 -- [Skill custom](13-skill-custom.md)**
  Construire vos propres skills pour etendre les capacites de l'agent a votre metier

- **3.14 -- [Souverainete des donnees](14-souverainete-donnees.md)**
  Savoir exactement ou vivent vos donnees et qui y a acces

### Partie D -- Triggers et automatisations

- **3.15 -- [Les crons](15-crons.md)**
  Planifier des declenchements automatiques a heures fixes ou sur evenement

- **3.16 -- [Le briefing du matin](16-briefing-matin.md)**
  Configurer le test ultime : l'agent qui vous prepare un resume chaque matin

- **3.17 -- [Multi-agents](17-multi-agents.md)**
  Orchestrer plusieurs agents specialises qui collaborent sur des taches complexes

---

[Contribuer a ce chapitre](https://github.com/alexwill87/openclawfieldplaybook/issues/new?template=suggestion.yml) -- [CONTRIBUTING.md](../../CONTRIBUTING.md)
