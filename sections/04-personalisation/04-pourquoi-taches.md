---
status: complete
audience: both
chapter: 04
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 4.4 -- Pourquoi un systeme de taches

## Contexte

Un agent sans systeme de taches est un conseiller. Vous lui posez des questions, il repond. Vous oubliez de demander, il oublie de faire. Rien ne persiste entre les sessions.

Un agent avec un systeme de taches est un partenaire. Il sait ce qui est en cours, ce qui est bloque, ce qui est termine. Il peut proposer la prochaine action sans que vous la formuliez.

La difference n'est pas technique. C'est une difference de relation.

## Agent conseiller vs agent partenaire

| | Conseiller | Partenaire |
|---|---|---|
| Memoire | Session uniquement | Persistante |
| Initiative | Repond aux questions | Propose des actions |
| Suivi | Aucun | Sait ou on en est |
| Valeur | Ponctuelle | Cumulative |
| Dependance | A votre memoire | A un systeme partage |

Le conseiller est utile. Le partenaire est indispensable.

## Commencer simple

N'installez pas PostgreSQL, un ORM, et un dashboard le premier jour. Commencez par une checklist.

### Niveau 1 : un fichier texte

```markdown
# TASKS.md

## En cours
- [ ] Migrer le backup vers S3 — deadline: 2026-04-05
- [ ] Ecrire la doc API endpoint /users

## En attente
- [ ] Renouveler le certificat SSL (expire 2026-05-15)

## Fait
- [x] Configurer le monitoring Telegram — 2026-03-28
```

Votre agent peut lire ce fichier, proposer des mises a jour, et vous rappeler les deadlines. Zero infrastructure.

### Niveau 2 : un fichier JSON/YAML structure

```yaml
tasks:
  - id: 1
    title: "Migrer backup S3"
    status: in_progress
    priority: high
    deadline: "2026-04-05"
    notes: "Tester restauration apres migration"
  - id: 2
    title: "Doc API /users"
    status: todo
    priority: medium
```

Plus facile a parser pour l'agent. Permet des requetes ("quelles taches high priority ?").

### Niveau 3 : base de donnees

Voir section 4.6. C'est le bon choix quand vous depassez 20 taches actives ou que vous avez besoin d'historique.

## Ce que le systeme de taches change concretement

**Sans taches :** "Ou en est-on avec le backup S3 ?"
Agent : "Je ne sais pas, je n'ai pas le contexte."

**Avec taches :** "Quoi de prevu aujourd'hui ?"
Agent : "3 taches prioritaires. La migration S3 est en retard de 2 jours. Le certificat SSL expire dans 6 semaines. Suggestion : finir S3 aujourd'hui."

C'est la difference entre piloter a vue et piloter avec un tableau de bord.

## Quand passer au niveau suivant

- **Fichier texte -> JSON** : quand vous avez plus de 10 taches et que vous voulez filtrer par priorite ou statut.
- **JSON -> Base de donnees** : quand vous voulez un historique, des requetes complexes, ou que plusieurs agents partagent les memes taches.

Ne sautez pas les etapes. Chaque niveau vous apprend ce dont vous avez vraiment besoin au niveau suivant.

## Erreurs courantes

**Trop de structure trop tot.** Installer Jira pour 5 taches. Un fichier TASKS.md suffit pour commencer.

**Pas de structure du tout.** "Je retiens tout dans ma tete." Non. Vous oubliez, l'agent aussi. Ecrivez.

**Deleguer le suivi sans le verifier.** L'agent met a jour les taches mais vous ne relisez jamais. Les statuts divergent de la realite. Voir section 4.5.

## Etapes

1. Creez un fichier `TASKS.md` dans votre projet.
2. Ajoutez vos 5 taches en cours les plus importantes.
3. Dites a votre agent : "Lis TASKS.md. Qu'est-ce qui est prioritaire ?"
4. Utilisez pendant une semaine.
5. Evaluez : est-ce que le format suffit ou faut-il passer au niveau 2 ?

## Verification

- [ ] Un fichier de taches existe et est accessible a l'agent.
- [ ] Les taches ont au minimum : titre, statut, priorite.
- [ ] L'agent sait ou trouver et lire ce fichier.
- [ ] Vous relisez les taches au moins une fois par semaine.
