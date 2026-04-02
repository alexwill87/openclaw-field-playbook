---
status: complete
audience: both
chapter: 03
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 3.13 -- Construire un skill custom (methode Steinberg)

## Contexte

Les skills integres (calendrier, email, taches) couvrent les besoins generiques. Mais votre metier a des besoins specifiques. Un consultant veut interroger son CRM. Un e-commercant veut suivre ses commandes. Un dev veut monitorer ses deployments.

C'est la que les skills custom entrent en jeu. Un skill custom est un module que l'agent utilise pour interagir avec une source de donnees ou un service externe specifique a votre contexte.

## Les 4 parties d'un skill

Chaque skill custom contient exactement 4 parties :

### 1. Authentification

Comment l'agent se connecte au service.

```markdown
## Authentification
- Type : API key / OAuth / token
- Stockage : vault (jamais en clair dans le skill)
- Rotation : tous les 90 jours
- Fallback : si le token expire, notifier l'utilisateur
```

### 2. Requetes

Ce que l'agent peut demander au service.

```markdown
## Requetes autorisees
- GET /clients : liste des clients actifs
- GET /clients/{id}/historique : historique d'un client
- GET /factures/en-attente : factures impayees
- POST /notes : ajouter une note client (avec validation)
```

### 3. Perimetre

Les limites du skill : ce qu'il peut voir, ce qu'il ne peut pas voir.

```markdown
## Perimetre
- Donnees accessibles : clients actifs uniquement (pas les archives)
- Periode : 12 derniers mois
- Champs sensibles exclus : coordonnees bancaires, IBAN
- Volume max par requete : 50 resultats
```

### 4. Garde-fous

Les regles de securite et les limites d'usage.

```markdown
## Garde-fous
- Jamais de modification de donnees sans validation utilisateur
- Jamais d'export massif (plus de 100 enregistrements)
- Jamais d'acces aux donnees supprimees
- Rate limit : 10 requetes par minute max
- En cas d'erreur API : notifier, ne pas retenter automatiquement
```

## La regle d'or : lire le SKILL.md genere

Quand vous creez un skill avec le prompt generique (ci-dessous), l'agent genere un fichier SKILL.md dans votre workspace. LISEZ-LE.

L'agent interprete votre demande et la traduit en regles. Ces regles ne correspondent pas toujours a votre intention. Verifiez :

- Les requetes autorisees sont-elles completes ? (pas trop, pas trop peu)
- Le perimetre est-il correct ? (pas d'acces a des donnees sensibles)
- Les garde-fous sont-ils assez stricts ?

## Supprimer les regles de decision

Un skill ne doit PAS contenir de regles de decision. Un skill se connecte, recupere des donnees, et les presente. La decision appartient a CONSTITUTION.md.

Mauvais (dans le skill) :
```markdown
Si le client n'a pas paye depuis 30 jours, envoyer une relance.
```

Bon (dans CONSTITUTION.md) :
```markdown
Quand un client a une facture impayee depuis plus de 30 jours,
me signaler et proposer un brouillon de relance. Ne pas envoyer.
```

Le skill donne l'information. CONSTITUTION.md dit quoi en faire.

## Prompt generique pour creer un skill

```
Je veux creer un skill custom pour [nom du service].

Contexte :
- Service : [description du service, URL de l'API si disponible]
- Usage : [ce que je veux en faire, en 2-3 phrases]
- Frequence : [combien de fois par jour/semaine j'en ai besoin]

Contraintes :
- Authentification : [type d'auth disponible]
- Donnees sensibles : [ce qui ne doit jamais etre expose]
- Actions interdites : [ce que le skill ne doit jamais faire]

Genere le skill avec les 4 parties :
authentification, requetes, perimetre, garde-fous.

Montre-moi le SKILL.md avant de l'installer.
```

## Exemple complet : skill "client-pulse" (adapte de Steinberg)

Le "client-pulse" de Steinberg est un skill qui donne une vue rapide de la sante de la relation client. Voici une adaptation :

```markdown
# SKILL.md -- client-pulse

## Description
Donne un apercu rapide de la relation avec un client :
derniere interaction, factures en cours, satisfaction.

## Authentification
- Source : CRM via API REST
- Auth : Bearer token (stocke dans vault)
- Rotation : 90 jours

## Requetes
- GET /clients/{id}/derniere-interaction
  > Retourne : date, type (email/call/reunion), resume
- GET /clients/{id}/factures
  > Retourne : factures des 6 derniers mois, statut
- GET /clients/{id}/satisfaction
  > Retourne : dernier score NPS, tendance

## Perimetre
- Clients actifs uniquement
- 6 derniers mois d'historique
- Pas d'acces aux donnees financieres detaillees (montants oui, marges non)
- Pas d'acces aux notes internes marquees "confidentiel"

## Garde-fous
- Lecture seule (aucune modification du CRM)
- Maximum 5 clients interroges par session
- Pas de comparaison entre clients (donnees isolees)
- En cas d'indisponibilite API : signaler, ne pas inventer de donnees

## Usage type
"Donne-moi le pulse de ClientAlpha"
> Derniere interaction : call le 28/03, sujet devis
> Factures : 1 en attente (2 800 EUR, echeance 05/04)
> Satisfaction : NPS 8/10 (stable)
```

## Etape par etape

1. Identifiez le service que vous voulez connecter
2. Verifiez que l'API est disponible et documentee
3. Utilisez le prompt generique ci-dessus
4. Lisez le SKILL.md genere par l'agent
5. Verifiez les 4 parties (auth, requetes, perimetre, garde-fous)
6. Supprimez toute regle de decision (elles vont dans CONSTITUTION.md)
7. Testez le skill avec une requete simple
8. Validez pendant 3-5 jours avant de l'integrer au briefing quotidien

## Template de prompt avance

Pour les cas ou vous avez besoin de plus de controle :

```
Cree un skill custom avec ces specifications exactes :

NOM : [nom-du-skill]
SERVICE : [nom et URL]
AUTH : [methode d'authentification]

REQUETES AUTORISEES :
1. [methode] [endpoint] -- [description] -- [frequence d'usage]
2. [methode] [endpoint] -- [description] -- [frequence d'usage]

REQUETES INTERDITES :
- [methode] [endpoint] -- [raison de l'interdiction]

PERIMETRE :
- Donnees visibles : [liste]
- Donnees exclues : [liste]
- Periode : [duree]

GARDE-FOUS :
- [regle 1]
- [regle 2]

Genere le SKILL.md. Ne l'installe pas avant que je valide.
```

## Erreurs courantes

**Ne pas lire le SKILL.md genere** : L'agent a peut-etre ajoute des requetes que vous ne voulez pas, ou oublie des garde-fous. Lisez toujours.

**Mettre des regles de decision dans le skill** : Un skill recupere des donnees. Il ne decide pas quoi en faire. La decision va dans CONSTITUTION.md.

**Skill trop large** : Un skill qui fait 15 requetes differentes est probablement 3 skills. Decoupez.

**Pas de garde-fous** : Un skill sans garde-fous est un acces direct a un service externe. Definissez toujours les limites.

**Oublier la rotation des tokens** : Un token d'API qui n'expire jamais est un risque de securite. Planifiez la rotation.

## Verification

- [ ] Le service cible a une API documentee
- [ ] Le skill contient les 4 parties (auth, requetes, perimetre, garde-fous)
- [ ] Le SKILL.md genere a ete relu et valide
- [ ] Aucune regle de decision dans le skill
- [ ] Les garde-fous sont definis et explicites
- [ ] Le token est stocke dans le vault (pas en clair)
- [ ] Test avec une requete simple reussi
