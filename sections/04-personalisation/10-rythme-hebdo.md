---
status: complete
audience: both
chapter: 04
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 4.10 -- Le rythme hebdomadaire

## Contexte

Un agent sans rythme est reactif : il repond quand vous demandez. Un agent avec un rythme est proactif : il prepare ce dont vous avez besoin avant que vous le demandiez.

Le rythme de base selon Steinberg : preview le lundi, review le vendredi. L'agent prepare les deux. Vous decidez et validez.

## Preview du lundi

Le lundi matin, l'agent vous presente la semaine qui vient.

### Ce que l'agent prepare

```
=== Preview semaine du 31 mars 2026 ===

Taches en cours : 4
Taches en retard : 1 (migration S3, retard 3 jours)
Deadlines cette semaine : 2
  - Mercredi : livraison doc API
  - Vendredi : renouvellement certificat SSL

Suggestion de plan :
- Lundi : finir migration S3 (rattraper le retard)
- Mardi-mercredi : doc API
- Jeudi : rotation secrets mensuelle
- Vendredi : certificat SSL + review

Blocages detectes : aucun.
Questions pour vous : le client X a-t-il confirme la spec ?
```

### Ce que vous faites

Vous lisez, vous ajustez. "Inverse mardi et lundi." "Ajoute la review PR de l'equipe." "Le client n'a pas confirme, reporte la doc."

5 minutes. Votre semaine est cadree.

### Prompt pour configurer

Ajoutez dans le system prompt :

```
Chaque lundi matin, quand je te dis "preview", genere :
- Taches en cours et en retard
- Deadlines de la semaine
- Plan suggere jour par jour
- Blocages detectes
- Questions pour moi
Format : bullet points, court.
```

## Review du vendredi

Le vendredi, l'agent fait le bilan de la semaine ecoulee.

### Ce que l'agent prepare

```
=== Review semaine du 31 mars 2026 ===

Terminees : 5/7 taches planifiees
  - Migration S3 [DONE]
  - Doc API /users [DONE]
  - Rotation secrets [DONE]
  - Health check auto [DONE]
  - PR review equipe [DONE]

Non terminees : 2
  - Certificat SSL : reporte (expire dans 42 jours, pas urgent)
  - Refactoring auth : bloque (attente spec client)

Temps estime economise par l'agent : ~3h
  - Health checks auto : 5x10min = 50min
  - Generation doc API : ~1h30
  - Rotation secrets automatisee : ~40min

Points d'attention pour la semaine prochaine :
  - Le certificat SSL doit etre fait la semaine prochaine.
  - 2 taches dependant de la spec client : relancer ?
```

### Ce que vous faites

Vous validez le bilan. Vous notez ce qui a bien marche et ce qui a coince. C'est aussi le bon moment pour ajuster les workflows ou le system prompt si quelque chose a grince dans la semaine.

## Garder leger et reviewable

Le piege du rythme hebdomadaire : ca devient un reporting lourd que personne ne lit.

Regles :

- **Preview lundi** : maximum 15 lignes. Si c'est plus long, c'est qu'il y a trop de taches actives.
- **Review vendredi** : maximum 20 lignes. Chiffres et faits, pas de prose.
- **Temps de lecture** : moins de 2 minutes pour chacun.
- **Temps de decision** : moins de 5 minutes pour ajuster le plan.

Si vous passez plus de 10 minutes sur la review du vendredi, c'est un signal que le systeme est trop complexe.

## Adapter le rythme

Le lundi/vendredi est un point de depart. Adaptez selon votre realite :

- **Freelance solo** : lundi/vendredi suffit.
- **Equipe petite** : ajoutez un point mercredi (mid-week check).
- **Projet intense** : briefing quotidien de 5 lignes le matin.
- **Maintenance pure** : une review par quinzaine peut suffire.

L'important n'est pas la frequence, c'est la regularite. Un rythme tenu a 80% vaut mieux qu'un rythme ideal tenu a 20%.

## Erreurs courantes

**Trop de detail.** La preview fait 50 lignes avec des sous-taches et des estimations horaires. Personne ne lit. Restez macro.

**Pas de decision.** Vous lisez la preview mais ne decidez rien. L'agent ne sait pas quoi prioriser. La preview sans decision est du bruit.

**Abandonner apres 2 semaines.** "C'est redondant, je sais ce que j'ai a faire." Vous le savez parce que la preview vous l'a rappele. Arretez la preview et vous oublierez dans la semaine.

## Etapes

1. Ajoutez les prompts preview/review au system prompt.
2. Lundi prochain : dites "preview" a votre agent.
3. Passez 5 minutes a ajuster le plan.
4. Vendredi : dites "review".
5. Notez si le format est utile ou s'il faut ajuster.
6. Tenez le rythme pendant 4 semaines avant d'evaluer.

## Verification

- [ ] Les prompts preview et review sont dans le system prompt.
- [ ] La preview tient en 15 lignes max.
- [ ] La review tient en 20 lignes max.
- [ ] Vous decidez effectivement apres chaque preview (pas juste lire).
- [ ] Le rythme est tenu depuis au moins 2 semaines consecutives.
