---
status: complete
audience: both
chapter: 04
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 4. Personnalisation

> Faire de votre agent LE votre -- votre voix, vos regles, vos workflows, votre identite.

La configuration (chapitre 3) rend l'agent fonctionnel. La personnalisation le rend indispensable. Ce chapitre couvre le travail sur la voix et le ton de l'agent, la mise en place d'un systeme de taches, l'automatisation des routines recurrentes, et le cadrage de la confiance et de la securite. A la fin, vous aurez un agent qui parle comme vous, execute vos workflows, et sait exactement ou s'arretent ses droits.

Pour les adaptations par pays (reglementation, ecosysteme local), voir le chapitre 7 (Localisation).

---

## Sommaire

### Partie A -- Identite et voix

- **4.1 -- [Ecrire votre system prompt](01-system-prompt.md)**
  Rediger le texte fondateur qui determine comment l'agent pense, repond et se comporte

- **4.2 -- [Personnalite et ton](02-personnalite-ton.md)**
  Calibrer le registre de langue, le niveau de formalite, et les cas ou l'agent ne doit pas vous imiter

- **4.3 -- [Iteration : la premiere version ne sera pas la bonne](03-iteration.md)**
  Methode pour converger en 2-3 rounds vers un prompt qui sonne juste

### Partie B -- Systeme de taches

- **4.4 -- [Pourquoi un systeme de taches](04-pourquoi-taches.md)**
  Passer d'un agent qui conseille a un agent qui agit et rend des comptes

- **4.5 -- [Comment les taches se font](05-comment-taches.md)**
  Le workflow concret : l'agent propose, vous validez, il execute, il rapporte

- **4.6 -- [Base de donnees comme source de verite](06-db-source-verite.md)**
  Utiliser PostgreSQL plutot que des fichiers Markdown pour stocker les taches et leur etat

### Partie C -- Workflows et routines

- **4.7 -- [Reconnaitre une routine](07-reconnaitre-routine.md)**
  Identifier les taches repetitives (3+ occurrences, schema previsible) candidates a l'automatisation

- **4.8 -- [Dry run avant confiance](08-dry-run.md)**
  Tester chaque automatisation en mode "montre-moi" avant de laisser l'agent agir seul

- **4.9 -- [WORKFLOWS.md](09-workflows-md.md)**
  Documenter chaque procedure dans un format standardise que l'agent peut suivre a la lettre

- **4.10 -- [Le rythme hebdomadaire](10-rythme-hebdo.md)**
  Instaurer le cycle preview lundi / review vendredi, prepare automatiquement par l'agent

### Partie D -- Securite et confiance

- **4.11 -- [La confiance est une configuration](11-confiance-configuration.md)**
  Definir la pyramide des droits : lecture seule, proposition, execution supervisee, autonomie

- **4.12 -- [Le boundary prompt](12-boundary-prompt.md)**
  Ecrire la liste definitive de ce que l'agent ne doit jamais faire, quelles que soient les circonstances

- **4.13 -- [Audit : que peut acceder votre agent ?](13-audit-acces.md)**
  Lancer un auto-audit pour verifier que les acces reels correspondent a vos intentions

- **4.14 -- [Configuration bilingue](14-config-bilingue.md)**
  Gerer le francais, l'anglais ou les deux, et definir les regles de bascule

---

[Contribuer a ce chapitre](https://github.com/alexwill87/openclawfieldplaybook/issues/new?template=suggestion.yml) -- [CONTRIBUTING.md](../../CONTRIBUTING.md)
