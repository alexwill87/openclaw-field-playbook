---
status: complete
audience: both
chapter: 03
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 3.3 -- USER.md : votre profil pour l'agent

## Contexte

SOUL.md definit qui est l'agent. USER.md definit qui VOUS etes.

Sans USER.md, l'agent repond dans le vide. Il ne sait pas que vous detestez les longs emails. Que vous etes en phase de levee de fonds. Que vous ne travaillez jamais le vendredi apres-midi. Que votre interlocuteur principal s'appelle Marc et qu'il est directeur technique chez votre plus gros client.

USER.md est le fichier le plus sous-estime de la configuration. C'est aussi celui qui fait la plus grande difference.

## L'onboarding interview (methode Steinberg)

Steinberg recommande de commencer par une "interview d'onboarding" : 20 questions que l'agent vous pose pour construire votre profil. Voici la liste adaptee :

### Identite et role
1. Quel est votre role actuel ? Depuis combien de temps ?
2. A qui rendez-vous des comptes ? Qui vous rend des comptes ?
3. Quels sont vos 3 objectifs principaux ce trimestre ?
4. Quelle est votre expertise distinctive (ce que vous faites mieux que la moyenne) ?

### Style de travail
5. Comment preferez-vous recevoir de l'information ? (listes, paragraphes, tableaux, visuels)
6. Quel est votre rythme de travail ? (matin/soir, blocs de focus, disponibilite)
7. Qu'est-ce qui vous irrite dans la communication ecrite ?
8. Tutoiement ou vouvoiement avec l'agent ?

### Contexte metier
9. Quel est votre secteur d'activite ?
10. Quelle est la taille de votre organisation ?
11. Quels sont vos outils principaux au quotidien ?
12. Quels sont les 3 sujets sur lesquels vous passez le plus de temps ?

### Preferences de l'agent
13. Que doit faire l'agent quand il ne sait pas ? (deviner, demander, signaler)
14. Preferez-vous une reponse rapide et imparfaite ou lente et precise ?
15. L'agent doit-il vous challenger ou executer ?
16. Quel niveau de detail attendez-vous par defaut ?

### Relations cles
17. Quels sont vos 5 interlocuteurs les plus frequents ? (nom, role, contexte)
18. Y a-t-il des relations sensibles ou l'agent doit etre particulierement prudent ?
19. Qui sont les personnes dont les messages meritent une reponse prioritaire ?

### Limites
20. Qu'est-ce que l'agent ne doit JAMAIS faire en votre nom ?

## Ce qui appartient a USER.md

USER.md contient ce qui est STABLE dans votre profil. La regle :

**Si ca change plus d'une fois par mois, ca ne va pas dans USER.md.**

| Appartient a USER.md | N'appartient PAS a USER.md |
|---|---|
| Votre role et vos responsabilites | Votre emploi du temps de la semaine |
| Vos preferences de communication | Vos taches en cours |
| Vos interlocuteurs cles | Les decisions en attente |
| Votre expertise | Les faits recents (ca va dans MEMORY.md) |
| Vos objectifs trimestriels | Votre humeur du jour |
| Vos outils de travail | Les deadlines specifiques |
| Vos limites et interdictions | Le contenu d'une reunion |

Ou vont les informations exclues :
- Emploi du temps : connexion calendrier (section 3.10)
- Taches en cours : systeme de taches (section 3.11)
- Faits recents : MEMORY.md (section 3.7)
- Decisions en attente : session active

## Etape par etape

### 1. Lancer l'onboarding interview

```
Je veux que tu me poses les 20 questions d'onboarding
une par une. Attends ma reponse avant de passer a la suivante.
A la fin, genere mon USER.md.
```

### 2. Relire et ajuster

L'agent va generer un USER.md. Relisez-le. Supprimez ce qui est trop volatile. Ajoutez ce qui manque.

### 3. Valider avec le test des 5 phrases

```
Decris-moi en 5 phrases.
```

Verifiez que :
- Les 5 phrases sont factuelles (pas de flatterie)
- Elles couvrent role, style, contexte
- Rien d'important ne manque
- Rien de faux n'apparait

Si la description est generique ("Vous etes un professionnel motive qui..."), USER.md est trop vague.

### 4. Mettre a jour trimestriellement

Bloquez 15 minutes chaque trimestre pour relire USER.md. Vos objectifs changent. Vos interlocuteurs evoluent. Votre role peut avoir bouge.

## Template USER.md complet

```markdown
# USER.md

## Identite
- Nom : [votre nom]
- Role : [votre role actuel]
- Organisation : [nom, secteur, taille]
- Responsabilites principales : [3-5 lignes max]

## Objectifs ce trimestre
1. [Objectif 1]
2. [Objectif 2]
3. [Objectif 3]

## Style de travail
- Format prefere : [listes / paragraphes / tableaux]
- Longueur des reponses : [concis / detaille / ca depend -- preciser]
- Rythme : [matin tot / journee standard / soir]
- Focus : [blocs de 2h / multitache / variable]
- Langue de travail : [francais / anglais / les deux selon contexte]

## Communication
- Tutoiement / Vouvoiement : [choix]
- Ce qui m'irrite : [exemples concrets]
- Ce que j'apprecie : [exemples concrets]
- Quand je dis "[expression recurrente]", je veux dire [traduction]

## Interlocuteurs cles
| Nom | Role | Contexte | Priorite |
|-----|------|----------|----------|
| [Nom 1] | [Role] | [Contexte de la relation] | Haute |
| [Nom 2] | [Role] | [Contexte de la relation] | Moyenne |
| [Nom 3] | [Role] | [Contexte de la relation] | Normale |

## Preferences agent
- Quand tu ne sais pas : [demander / signaler / proposer une hypothese]
- Rapidite vs precision : [rapide et imparfait / lent et precis]
- Challenger vs executer : [challenger / executer / les deux]
- Niveau de detail par defaut : [minimum / standard / maximum]

## Interdictions
- Ne jamais [interdit 1]
- Ne jamais [interdit 2]
- Ne jamais [interdit 3]
```

## Erreurs courantes

**USER.md trop court** : "Je suis dev, je code en Python." L'agent ne vous connait pas. Il donnera des reponses generiques a un "dev Python" generique.

**USER.md trop long** : 200 lignes de biographie. L'agent perd le signal dans le bruit. Visez 40-60 lignes.

**Mettre des taches dans USER.md** : "Je dois finir le rapport pour vendredi." Ca change chaque semaine. Ca va dans le systeme de taches ou dans MEMORY.md.

**Ne jamais mettre a jour** : Vous avez change de role il y a 3 mois mais USER.md dit encore l'ancien. L'agent travaille avec des informations obsoletes.

**Oublier les interlocuteurs** : L'agent ne peut pas savoir que "Marc" dans vos emails est votre client principal si vous ne le lui dites pas.

## Verification

- [ ] Onboarding interview completee (ou reponses aux 20 questions)
- [ ] USER.md genere et relu
- [ ] Test "Decris-moi en 5 phrases" reussi
- [ ] Aucune information volatile dans le fichier
- [ ] Interlocuteurs cles documentes
- [ ] Preferences agent explicites
- [ ] Date de prochaine revision notee (dans 3 mois)
