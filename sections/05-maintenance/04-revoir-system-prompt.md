---
status: complete
audience: both
chapter: 05
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 5.4 -- Revoir le system prompt

## Contexte

Un system prompt n'est pas un texte sacre. Votre contexte change, vos projets evoluent, vos besoins se precisent. Un prompt ecrit il y a 3 mois ne reflete plus votre realite d'aujourd'hui. Si vous ne le revoyez pas, il accumule des instructions obsoletes et l'agent degrade progressivement.

## Frequence

- **Review complete** : tous les mois.
- **Ajustements ponctuels** : quand un declencheur se manifeste (voir ci-dessous).
- **Condensation** : tous les 3 mois (le prompt grossit naturellement, il faut le comprimer).

## Declencheurs d'une revision

Vous devez revoir le prompt quand :

1. **Un projet se termine.** Les instructions liees a ce projet polluent le prompt.
2. **Un outil change.** Vous migrez de X vers Y mais le prompt mentionne encore X.
3. **Vous corrigez l'agent regulierement sur le meme point.** Signal que le prompt ne couvre pas ce cas.
4. **Le prompt depasse 300 mots.** Il est temps de condenser.
5. **Vous changez de modele.** Chaque modele interprete differemment. Testez et ajustez.
6. **Un incident s'est produit.** L'agent a fait quelque chose qu'il n'aurait pas du. Ajoutez une regle ou clarifiez.

## Quoi preserver

Certaines parties du prompt sont stables. Ne les touchez pas sauf raison forte :

- **La mission** (qui est l'agent, pour qui).
- **Le ton et le format** (une fois calibre, ca tient).
- **Les boundaries** (les interdictions ne changent pas).
- **La langue** (stable une fois definie).

## Quoi reecrire

Ce qui change le plus souvent :

- **Le contexte** : projets actifs, stack, outils.
- **Les regles operationnelles** : workflows, priorites, processus.
- **Les acces** : quels outils l'agent peut utiliser.

## Methode de revision

### 1. Relire le prompt actuel

Lisez-le comme si c'etait la premiere fois. Marquez :
- [OBSOLETE] : ce qui n'est plus vrai.
- [VAGUE] : ce qui pourrait etre plus precis.
- [MANQUE] : ce qui devrait etre la mais n'y est pas.
- [OK] : ce qui est bon.

### 2. Supprimer avant d'ajouter

La regle : pour chaque ligne ajoutee, cherchez une ligne a supprimer. Le prompt doit rester court.

### 3. Tester

Apres la revision, testez avec 5 requetes typiques. Comparez les reponses avec les reponses d'avant. Si la qualite baisse, revenez en arriere.

### 4. Versionner

Gardez les versions precedentes. Un simple fichier :

```
system-prompt-v1.md    (2026-01-15)
system-prompt-v2.md    (2026-02-20)
system-prompt-v3.md    (2026-04-01)  <- actuel
```

Si une revision degrade les performances, vous pouvez revenir a la version precedente.

## Erreurs courantes

**Ne jamais reviser.** Le prompt de janvier 2026 est toujours actif en decembre. Il mentionne des projets termines, des outils remplaces, des regles obsoletes.

**Reviser trop souvent.** Chaque jour vous changez un truc. L'agent n'a jamais le temps de "se stabiliser" et vous ne pouvez pas evaluer l'impact d'un changement.

**Ajouter sans supprimer.** Le prompt passe de 150 a 500 mots en 3 mois. Performance en baisse, cout en hausse.

**Pas de versioning.** Vous modifiez le prompt et vous ne savez plus ce qu'il y avait avant. Impossible de revenir en arriere.

## Etapes

1. Planifiez une review mensuelle (mettez un rappel).
2. Relisez le prompt avec le systeme OBSOLETE/VAGUE/MANQUE/OK.
3. Supprimez ce qui est obsolete.
4. Precisez ce qui est vague.
5. Ajoutez ce qui manque.
6. Condensez si > 300 mots.
7. Testez avec 5 requetes.
8. Sauvegardez l'ancienne version.

## Verification

- [ ] La derniere review du prompt date de moins d'un mois.
- [ ] Le prompt fait moins de 300 mots.
- [ ] Aucune instruction ne fait reference a un projet termine ou un outil remplace.
- [ ] Les versions precedentes sont sauvegardees.
- [ ] 5 requetes test donnent des reponses correctes apres la revision.
