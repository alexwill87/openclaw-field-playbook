---
status: complete
audience: both
chapter: 03
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 3.1 -- Definir le perimetre de l'agent

## Contexte

Un agent sans perimetre clair est un agent dangereux. Pas parce qu'il va "se rebeller" -- parce qu'il va faire des choses que vous n'aviez pas anticipees. Envoyer un email a un client avec un ton inapproprie. Modifier un fichier de production. Prendre une decision financiere.

Le perimetre n'est pas une liste de fonctionnalites. C'est un contrat de confiance entre vous et l'agent.

## La pyramide des droits

Trois niveaux, du plus permissif au plus restrictif :

```
        /\
       /  \
      / 3  \    ACTION EXTERNE
     / val. \   Validation requise a chaque fois
    /--------\
   /    2     \  ECRITURE
  /  autonome  \ L'agent agit seul dans un cadre defini
 /--------------\
/       1        \ LECTURE
/ toujours autorise\ L'agent lit tout ce qu'il a besoin
---------------------|
```

### Niveau 1 -- Lecture (toujours autorise)

L'agent peut lire sans restriction :
- Vos fichiers de configuration
- Votre calendrier
- Vos emails (en lecture seule)
- Vos taches
- Les documents dans knowledge/

Pourquoi sans restriction : un agent qui ne comprend pas le contexte produit des reponses generiques. La lecture est le carburant de la pertinence.

### Niveau 2 -- Ecriture (autonome, dans un cadre)

L'agent peut modifier SANS vous demander :
- MEMORY.md (ajout, compression, nettoyage)
- Fichiers dans knowledge/ (mise a jour)
- Brouillons d'emails (mais pas l'envoi)
- Rapports et syntheses
- Notes de session

Exemples concrets :

| L'agent PEUT | L'agent NE PEUT PAS |
|---|---|
| Ecrire un brouillon de reponse email | Envoyer l'email |
| Mettre a jour un fichier knowledge/ | Supprimer un fichier knowledge/ |
| Creer un resume de reunion | Publier le resume quelque part |
| Ajouter une entree dans MEMORY.md | Modifier CONSTITUTION.md |
| Modifier un fichier de code en dev | Deployer en production |

### Niveau 3 -- Action externe (validation requise)

L'agent DOIT vous demander avant :
- Envoyer un email ou message
- Publier quoi que ce soit
- Modifier une base de donnees de production
- Effectuer un paiement ou une transaction
- Contacter un tiers
- Supprimer des donnees

Formulation de la demande de validation :

```
[VALIDATION REQUISE]
Action : Envoyer un email a dupont@client.fr
Contenu : [resume du contenu]
Raison : Reponse a sa demande de devis du 28/03
Impact : Le client recevra votre proposition tarifaire

Valider ? (oui / non / modifier)
```

## Etape par etape

### 1. Lister les actions de votre semaine type

Passez en revue votre derniere semaine. Notez chaque action que vous aimeriez deleguer. Classez-la dans la pyramide.

### 2. Definir les interdictions explicites

Ce qui n'est PAS dans le perimetre est aussi important que ce qui y est. Exemples :

```
INTERDIT :
- Prendre des engagements financiers
- Repondre aux RH en mon nom
- Modifier les contrats clients
- Acceder aux donnees medicales
- Partager des informations confidentielles hors contexte
```

### 3. Ecrire le perimetre dans CONSTITUTION.md

Le perimetre se traduit directement dans votre fichier CONSTITUTION.md (voir section 3.5).

### 4. Tester le perimetre

Demandez a l'agent :

```
Montre-moi 3 situations ou tu me demanderais une validation
et 3 situations ou tu agirais seul.
```

Si ses exemples ne correspondent pas a votre intention, ajustez le perimetre.

## Erreurs courantes

**Perimetre trop large** : "Fais ce que tu juges necessaire." L'agent finira par faire quelque chose que vous n'aviez pas imagine. Garantie.

**Perimetre trop etroit** : "Demande-moi avant chaque action." Vous finissez par valider 50 demandes par jour. Autant ne pas avoir d'agent.

**Perimetre flou** : "Gere mes emails, mais pas les importants." Qu'est-ce qui est "important" ? Pour l'agent, sans criteres explicites, c'est arbitraire.

**Perimetre statique** : Ne jamais reviser le perimetre. Votre contexte evolue. Revoyez le perimetre chaque mois.

## Verification

- [ ] Vous avez liste les actions de votre semaine type
- [ ] Chaque action est classee dans un des 3 niveaux
- [ ] Les interdictions explicites sont ecrites
- [ ] Le perimetre est documente dans CONSTITUTION.md
- [ ] L'agent decrit correctement ses limites quand vous le testez
