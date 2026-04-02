---
status: complete
audience: both
chapter: 04
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# Chapitre 4 -- Personnalisation

> Faire de votre agent LE votre -- votre voix, vos regles, vos workflows, votre identite.

## Partie A -- Identite et voix

- **4.1** -- [Ecrire votre system prompt](01-system-prompt.md)
  Le texte le plus important que vous ecrirez pour votre agent.

- **4.2** -- [Personnalite et ton](02-personnalite-ton.md)
  Comment le faire parler comme vous -- et quand ne pas le faire.

- **4.3** -- [Iteration : la premiere version ne sera pas la bonne](03-iteration.md)
  Normal. Comment converger en 2-3 rounds vers un prompt qui sonne juste.

## Partie B -- Systeme de taches

- **4.4** -- [Pourquoi un systeme de taches](04-pourquoi-taches.md)
  Agent sans taches = conseiller. Agent avec taches = partenaire.

- **4.5** -- [Comment les taches se font](05-comment-taches.md)
  Workflow : l'agent propose, vous decidez.

- **4.6** -- [Base de donnees comme source de verite](06-db-source-verite.md)
  Schema PostgreSQL, scripts CLI, pourquoi DB > fichiers .md.

## Partie C -- Workflows et routines

- **4.7** -- [Reconnaitre une routine](07-reconnaitre-routine.md)
  Se repete 3+ fois, schema previsible = candidat a l'automatisation.

- **4.8** -- [Dry run avant confiance](08-dry-run.md)
  Tester en mode "montre-moi" avant de laisser l'agent agir seul.

- **4.9** -- [WORKFLOWS.md](09-workflows-md.md)
  Documenter chaque procedure. Format standardise.

- **4.10** -- [Le rythme hebdomadaire](10-rythme-hebdo.md)
  Preview lundi, review vendredi. L'agent prepare les deux.

## Partie D -- Securite et confiance

- **4.11** -- [La confiance est une configuration](11-confiance-configuration.md)
  Pyramide des droits. Chaque niveau a ses regles.

- **4.12** -- [Le boundary prompt](12-boundary-prompt.md)
  Ce que l'agent ne doit JAMAIS faire. Ecrit une fois, applique toujours.

- **4.13** -- [Audit : que peut acceder votre agent ?](13-audit-acces.md)
  Prompt auto-audit. Verifier realite vs intention.

- **4.14** -- [Configuration bilingue](14-config-bilingue.md)
  Francais, anglais, ou les deux. Quand basculer.

---

Specifications locales : voir `sections/07-localisation/`

---

[Contribuer a ce chapitre](https://github.com/alexwill87/openclawfieldplaybook/issues/new?template=suggestion.yml) -- [CONTRIBUTING.md](../../CONTRIBUTING.md)
