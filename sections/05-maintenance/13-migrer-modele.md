---
status: complete
audience: both
chapter: 05
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 5.13 -- Migrer vers un autre modele

## Contexte

Le monde des LLM bouge vite. Un nouveau modele sort, les prix changent, les performances evoluent. Vous allez peut-etre vouloir migrer de Claude vers GPT (ou l'inverse), ou tester un modele open source. Le risque : casser ce qui marchait.

## Quand migrer

Bonnes raisons :

- **Cout.** Le nouveau modele est significativement moins cher pour des performances equivalentes.
- **Performance.** Meilleure qualite de reponse pour votre cas d'usage specifique.
- **Feature.** Le nouveau modele supporte quelque chose dont vous avez besoin (vision, plus de contexte, outils specifiques).
- **Disponibilite.** Votre modele actuel a des problemes de fiabilite ou de rate limiting.

Mauvaises raisons :

- "C'est nouveau, ca doit etre mieux." Pas toujours.
- "Tout le monde migre." Votre cas d'usage est unique.
- "Le benchmark dit que c'est meilleur." Les benchmarks ne mesurent pas votre usage specifique.

## Comment tester sans casser

### Phase 1 : test en parallele

Gardez votre modele actuel en production. Testez le nouveau sur le cote.

```
Semaine 1-2 : envoyez les memes requetes aux deux modeles.
Comparez :
- Qualite des reponses
- Respect du system prompt
- Ton et format
- Temps de reponse
- Cout
```

### Grille de comparaison

Creez un fichier `model-comparison.md` :

```markdown
# Comparaison : [Modele A] vs [Modele B]

Date : YYYY-MM-DD
Requetes testees : 20

| Critere | Modele A | Modele B | Gagnant |
|---|---|---|---|
| Respect du system prompt | 9/10 | 7/10 | A |
| Qualite technique | 8/10 | 9/10 | B |
| Respect du ton | 9/10 | 6/10 | A |
| Respect du francais | 9/10 | 8/10 | A |
| Temps de reponse moyen | 2.1s | 1.8s | B |
| Cout moyen/requete | $0.015 | $0.008 | B |
| Hallucinations | 1/20 | 3/20 | A |
| Suivi du boundary prompt | 10/10 | 8/10 | A |

Verdict : [decision]
Raison : [justification]
```

### Phase 2 : migration progressive

Si le nouveau modele est meilleur, migrez progressivement :

1. **Semaine 1** : utilisez le nouveau modele pour les taches a faible risque (questions, recherche, redaction).
2. **Semaine 2** : utilisez-le pour les taches operationnelles (mais avec validation).
3. **Semaine 3** : utilisez-le comme modele principal.
4. **Semaine 4** : evaluez. Gardez ou revenez en arriere.

### Phase 3 : couper l'ancien

Ne desactivez l'ancien modele qu'apres 1 mois de fonctionnement satisfaisant du nouveau. Gardez la configuration de l'ancien en backup.

## Adapter le system prompt

Chaque modele interprete le system prompt differemment. Ce qui fonctionne avec Claude peut ne pas fonctionner avec GPT-4.

### Points d'attention

| Aspect | Claude | GPT-4 | Modeles open source |
|---|---|---|---|
| Longueur du prompt | Tolere les longs prompts | Prefere les prompts structures | Court = mieux |
| Ton en francais | Naturel | Parfois anglicise | Variable |
| Boundaries | Respecte bien | Respecte bien | Moins fiable |
| Format XML dans le prompt | Excellent | Moyen | Faible |
| Bullet points vs prose | Les deux | Prefere les bullets | Bullets |

### Adapter sans reecrire

1. Copiez votre system prompt actuel.
2. Testez 5 requetes.
3. Notez les differences de comportement.
4. Ajustez les parties qui ne fonctionnent pas.
5. Ne reecrivez pas tout -- ajustez chirurgicalement.

## Garder le fallback

Toujours avoir un plan B.

```bash
# Configuration avec fallback
PRIMARY_MODEL="claude-sonnet-4-20250514"
FALLBACK_MODEL="claude-3-5-sonnet-20241022"

# Si le modele principal echoue, basculer
if ! call_model "$PRIMARY_MODEL" "$PROMPT"; then
    echo "Fallback sur $FALLBACK_MODEL"
    call_model "$FALLBACK_MODEL" "$PROMPT"
fi
```

### Ce qu'il faut sauvegarder

- System prompt de l'ancien modele (versionne).
- Configuration de connexion (API key, endpoint).
- Notes sur les ajustements specifiques au modele.

## Erreurs courantes

**Migrer en un jour.** Lundi Claude, mardi GPT-4. Vous ne savez pas si les problemes viennent du modele ou de la transition. Migrez progressivement.

**Ne pas adapter le prompt.** Le meme prompt verbatim sur deux modeles donnera des resultats differents. Testez et ajustez.

**Jeter l'ancien.** Vous supprimez la config de l'ancien modele. Le nouveau a un probleme le week-end. Pas de fallback.

**Se fier aux benchmarks.** "GPT-4 a un meilleur score MMLU." Les benchmarks generiques ne predisent pas la performance sur votre cas d'usage precis. Seul votre test A/B compte.

## Etapes

1. Identifiez pourquoi vous voulez migrer (raison concrete).
2. Testez le nouveau modele en parallele pendant 2 semaines.
3. Remplissez la grille de comparaison avec 20 requetes reelles.
4. Si le nouveau gagne, migrez progressivement (3 semaines).
5. Gardez le fallback actif pendant 1 mois.
6. Documentez les ajustements de prompt specifiques au modele.

## Verification

- [ ] La raison de la migration est concrete (pas juste "c'est nouveau").
- [ ] Un test A/B a ete fait avec au moins 20 requetes.
- [ ] La grille de comparaison est remplie.
- [ ] Le system prompt a ete adapte au nouveau modele.
- [ ] Un fallback est configure et fonctionnel.
- [ ] L'ancienne configuration est sauvegardee.
