---
status: complete
audience: both
chapter: 04
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 4.7 -- Reconnaitre une routine

## Contexte

Une routine, c'est une action que vous repetez avec le meme schema. Deployer un service, creer un backup, verifier les logs du matin. Quand vous faites la meme chose pour la 3eme fois, c'est un signal : ca pourrait etre automatise ou delegue a l'agent.

Mais pas tout. Certaines routines ont besoin de votre jugement humain. L'art, c'est de distinguer les deux.

## Les criteres d'une routine automatisable

Une tache est candidate a l'automatisation si elle remplit ces 3 conditions :

1. **Repetition.** Elle se produit 3+ fois avec le meme schema.
2. **Previsibilite.** Les etapes sont les memes a chaque fois, ou les variations sont connues a l'avance.
3. **Risque faible.** Si l'agent se trompe, les consequences sont reversibles ou mineures.

### Exemples de bonnes candidates

- Health check quotidien : memes commandes, meme interpretation, alerter si KO.
- Generer un resume hebdomadaire des taches : lecture seule, pas d'action.
- Rotation des logs : supprimer les fichiers > 30 jours, meme regle a chaque fois.
- Creer un commit avec un format standardise : meme structure, meme convention.

### Exemples de mauvaises candidates

- Repondre a un email client : chaque situation est differente, le ton importe.
- Decider de reporter une deadline : contexte humain necessaire (fatigue, priorites business, relations).
- Choisir entre deux architectures : trade-offs subtils, pas de bonne reponse universelle.
- Supprimer des donnees en production : irreversible, risque eleve.

## Comment detecter vos routines

### Methode 1 : le journal de bord

Pendant une semaine, notez chaque action que vous faites avec votre agent. Format :

```
Lundi :
- Health check VPS (5 min)
- Deploiement cockpit (10 min)
- Reponse email client X (15 min)
- Mise a jour TASKS.md (3 min)

Mardi :
- Health check VPS (5 min)
- Debug erreur API (30 min)
- Mise a jour TASKS.md (3 min)
```

Apres une semaine, les repetitions sautent aux yeux. Health check et TASKS.md reviennent chaque jour = routines.

### Methode 2 : demander a l'agent

```
Analyse mes 20 dernieres conversations avec toi.
Quelles actions reviennent 3+ fois ?
Pour chacune, dis-moi si elle suit un schema previsible.
```

L'agent voit des patterns que vous ne voyez pas parce que vous etes dedans.

## La zone grise : routines avec jugement

Certaines taches sont repetitives mais demandent du jugement a une etape :

- **Triage des taches** : repetitif, mais la priorisation demande du contexte humain.
- **Review de code** : le format est previsible, mais l'evaluation de la qualite est subjective.
- **Reporting** : la collecte de donnees est automatisable, l'interpretation non.

Pour celles-la, la bonne approche est de decouper : automatiser la partie mecanique, garder le jugement humain.

```
Routine "triage du matin" :
- [AGENT] Lister les taches actives, les trier par deadline.
- [AGENT] Signaler les retards et les blocages.
- [HUMAIN] Decider des priorites du jour.
- [AGENT] Mettre a jour les statuts selon la decision.
```

## Erreurs courantes

**Tout automatiser.** Parce que c'est possible ne veut pas dire que c'est souhaitable. Certaines routines vous gardent connecte a la realite de votre projet.

**Ne rien automatiser.** Par peur de perdre le controle. Commencez par les taches a risque zero (lecture seule, reporting) pour batir la confiance.

**Automatiser sans documenter.** L'agent fait la routine mais personne ne sait exactement ce qu'il fait. Si l'agent change ou si vous changez d'outil, la routine est perdue. Voir section 4.9.

## Etapes

1. Tenez un journal de bord pendant 5 jours.
2. Identifiez les actions qui reviennent 3+ fois.
3. Pour chacune, evaluez : previsible ? risque faible ?
4. Classez : automatisable / semi-automatisable / humain uniquement.
5. Commencez par la routine la plus simple et la moins risquee.

## Verification

- [ ] Au moins 3 routines identifiees.
- [ ] Chaque routine evaluee sur les 3 criteres (repetition, previsibilite, risque).
- [ ] Les routines avec jugement sont decoupees (partie agent / partie humain).
- [ ] La premiere routine automatisee est a risque zero.
