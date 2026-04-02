---
status: complete
audience: both
chapter: 05
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 5.14 -- Mesurer le ROI

## Contexte

"L'agent me fait gagner du temps." OK, combien ? Si vous ne mesurez pas, vous ne savez pas. Et si vous ne savez pas, vous ne pouvez pas justifier le cout, ni optimiser l'usage, ni decider si ca vaut le coup de continuer.

Mesurer le ROI d'un agent AI, c'est concret. Pas de la philosophie.

## Les trois axes du ROI

### 1. Temps gagne

Le plus tangible. Comparez le temps avec et sans agent.

#### Comment mesurer

Pendant 2 semaines, tracez :

```markdown
# Journal ROI — Semaine du [date]

| Tache | Sans agent (estime) | Avec agent (reel) | Gagne |
|---|---|---|---|
| Health check quotidien | 10 min | 0 min (automatise) | 10 min |
| Deploiement cockpit | 15 min | 5 min | 10 min |
| Ecrire un commit message | 3 min | 30 sec | 2.5 min |
| Debug erreur Docker | 30 min | 10 min | 20 min |
| Generer doc API | 2h | 30 min | 1h30 |
| Rotation secrets | 20 min | 5 min | 15 min |

**Total semaine : ~3h30 gagnees**
```

#### Calcul financier

```
Temps gagne/semaine : 3.5 heures
Taux horaire : [votre taux] EUR/h

Valeur mensuelle du temps gagne : 3.5h * 4 semaines * taux = X EUR
Cout agent/mois : Y EUR (API + infra)

ROI = (X - Y) / Y * 100
```

Exemple concret :

```
Temps gagne : 14h/mois
Taux : 80 EUR/h
Valeur : 1120 EUR/mois

Cout agent : ~50 EUR/mois (API ~30 EUR + VPS ~20 EUR)

ROI : (1120 - 50) / 50 = 2140%
```

Meme avec des estimations conservatrices, le ROI est generalement massif. Le probleme n'est pas le ROI, c'est de le mesurer pour savoir ou optimiser.

### 2. Decisions ameliorees

Plus difficile a quantifier, mais reel. L'agent vous aide a prendre de meilleures decisions parce qu'il :

- Analyse des donnees que vous n'auriez pas regardees.
- Detecte des patterns que vous n'auriez pas vus.
- Propose des alternatives que vous n'auriez pas considerees.

#### Comment mesurer

Tracez les decisions ou l'agent a apporte une valeur :

```markdown
# Decisions assistees — [mois]

1. L'agent a detecte que le certificat SSL expirait dans 15 jours.
   Sans agent : j'aurais probablement oublie. Impact potentiel : site down.

2. L'agent a suggere de condenser le system prompt (480 -> 150 mots).
   Resultat : cout tokens reduit de 40%.

3. L'agent a identifie un pattern de deplacement de taches doc.
   Resultat : j'ai bloque 2h/jeudi pour la doc. Les taches doc ne trainent plus.
```

Pas besoin de chiffrer chaque decision. Le simple fait de les noter montre la valeur.

### 3. Erreurs evitees

Chaque erreur evitee a un cout fantome : le temps de correction, l'impact sur les utilisateurs, le stress.

#### Comment mesurer

Tracez les situations ou l'agent a empeche une erreur :

```markdown
# Erreurs evitees — [mois]

1. J'ai demande un push --force sur main. L'agent a refuse (boundary prompt).
   Cout evite : potentiellement des heures de recovery + perte de commits.

2. Le health check a detecte un disque a 85% avant que ca cause une panne.
   Cout evite : downtime non planifie.

3. L'agent a detecte une incoherence dans la config avant deploiement.
   Cout evite : deploiement d'une version buggee.
```

## Dashboard mensuel

Chaque mois, compilez un resume :

```markdown
# ROI Agent — [Mois YYYY]

## Temps
- Heures gagnees : XX h
- Valeur : XX EUR
- Top 3 taches automatisees :
  1. [tache] — [temps gagne]
  2. [tache] — [temps gagne]
  3. [tache] — [temps gagne]

## Cout
- API : XX EUR
- Infra : XX EUR
- Total : XX EUR

## ROI
- Net : XX EUR
- Pourcentage : XX%

## Decisions
- X decisions assistees notables

## Erreurs evitees
- X erreurs evitees

## Actions
- [Ce qu'on peut ameliorer le mois prochain]
```

## Quand le ROI est negatif

Ca arrive. Signes :

- Vous passez plus de temps a corriger l'agent qu'a faire le travail vous-meme.
- Le cout API depasse la valeur du temps gagne.
- L'agent introduit des erreurs que vous devez debugger.

Dans ce cas, le probleme n'est generalement pas l'agent. C'est :

1. **Le system prompt** : mal configure, donc l'agent ne fait pas ce que vous voulez.
2. **Le workflow** : pas adapte, donc friction inutile.
3. **Le mauvais usage** : vous utilisez l'agent pour des taches ou il n'apporte pas de valeur.

Avant d'abandonner, revisez ces trois points. Si le ROI reste negatif apres optimisation, reduisez l'usage aux taches ou l'agent est clairement utile.

## Erreurs courantes

**Ne jamais mesurer.** "Ca va plus vite, je le sens." Les sensations ne suffisent pas. Mesurez au moins une fois pour avoir une baseline.

**Mesurer uniquement le temps.** Le temps gagne est le plus visible mais pas le seul. Les decisions ameliorees et les erreurs evitees comptent aussi.

**Comparer avec zero.** "Sans agent, je ferais la meme chose manuellement." Pas toujours. Certaines taches (analyse de patterns, monitoring automatise) ne seraient tout simplement pas faites sans agent.

**Oublier le cout d'apprentissage.** Le premier mois, le ROI est negatif parce que vous apprenez a configurer. C'est normal. Mesurez a partir du mois 2.

## Etapes

1. Tracez votre usage pendant 2 semaines (journal ROI).
2. Calculez le temps gagne et sa valeur.
3. Calculez le cout mensuel (API + infra).
4. Notez les decisions assistees et les erreurs evitees.
5. Compilez le dashboard mensuel.
6. Identifiez les optimisations pour le mois suivant.

## Verification

- [ ] Un journal ROI existe avec au moins 2 semaines de donnees.
- [ ] Le temps gagne est chiffre en heures et en euros.
- [ ] Le cout mensuel est connu (API + infra).
- [ ] Le ROI est positif (ou les raisons du negatif sont identifiees).
- [ ] Un dashboard mensuel est compile.
