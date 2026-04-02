---
status: complete
audience: both
chapter: 03
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 3.12 -- Email et messages

## Contexte

L'email est la source la plus volumineuse et la plus bruitee. C'est pour ca qu'elle vient en troisieme position, apres le calendrier et les taches. Connecter l'email a un agent mal configure, c'est lui donner un tuyau d'incendie quand il a besoin d'un verre d'eau.

## Connexion email

### Configuration

```
openclaw skill add email
```

L'agent va :
1. Demander le fournisseur (Gmail, Outlook, IMAP generique)
2. Configurer l'authentification (OAuth recommande, pas de mot de passe en clair)
3. Definir la portee initiale

### Portee recommandee au demarrage

| Droit | Recommandation |
|-------|----------------|
| Lecture des emails recus | Oui -- 48h glissantes |
| Lecture des emails envoyes | Oui -- pour le contexte des conversations |
| Brouillon de reponse | Oui -- l'agent prepare, vous envoyez |
| Envoi direct | Non -- ajoutez apres plusieurs semaines de confiance |
| Suppression | Non |
| Gestion des labels/dossiers | Non au debut |

La portee de 48h glissantes est importante : l'agent n'a pas besoin de vos emails d'il y a 6 mois. Il a besoin de ce qui est arrive recemment et attend une action.

## Triage : automatique vs assiste

Deux modes possibles :

### Triage assiste (recommande pour debuter)

L'agent classe vos emails et vous presente un resume. Vous decidez.

```
TRIAGE EMAIL -- 2 avril 2026, 08:15

URGENT (reponse aujourd'hui) :
- Marc (ClientAlpha) : Demande de modification du devis
  > Impact : le devis expire vendredi. Repondre avant jeudi.
- Lea Martin : Confirmation entretien 14h
  > Action : confirmer ou reporter

A TRAITER (cette semaine) :
- Fournisseur X : Nouvelle grille tarifaire
  > Pas urgent mais impacte le budget Q2
- Comptable : Documents manquants bilan
  > Deadline : 10 avril

INFORMATIF (pas d'action requise) :
- Newsletter secteur [archiver]
- Notification GitHub [archiver]
- Publicite [supprimer]

3 emails non classes -- voulez-vous que je les affiche ?
```

### Triage automatique (pour les agents matures)

L'agent agit selon des regles predefinies dans CONSTITUTION.md :

```markdown
## Regles de triage email
- Newsletter et notifications : archiver automatiquement
- Publicite et spam : supprimer automatiquement
- Email d'un interlocuteur cle (voir USER.md) : priorite haute
- Email avec deadline mentionnee : extraire la deadline, ajouter aux taches
- Tout le reste : classer en "a traiter" pour le prochain briefing
```

N'activez le triage automatique qu'apres 2-3 semaines de triage assiste valide.

## Brouillons de reponse

L'agent peut preparer des brouillons. C'est souvent la fonctionnalite la plus utile :

```
Prepare un brouillon de reponse pour l'email de Marc
sur la modification du devis. Ton professionnel mais ferme :
on peut ajuster la portee, pas le prix.
```

L'agent redige. Vous relisez. Vous envoyez (ou vous modifiez et envoyez).

Regle dans CONSTITUTION.md :

```markdown
## Emails
- Tu peux rediger des brouillons de reponse
- Tu ne peux JAMAIS envoyer un email sans ma validation explicite
- Chaque brouillon doit indiquer : destinataire, objet, ton utilise
```

## Le piege : ne pas tout connecter

L'email est la source ou le piege du "tout connecter" est le plus dangereux.

Ne connectez PAS :
- Les boites emails partagees (trop de bruit, contexte manquant)
- Les comptes personnels (separation pro/perso)
- Les listes de diffusion a haut volume (mailing lists techniques, etc.)

Connectez uniquement votre boite email professionnelle principale.

## Messages (Slack, Teams, etc.)

Les plateformes de messagerie instantanee sont encore plus bruitees que l'email. Si vous les connectez :

- Limitez a 2-3 channels pertinents, pas tout le workspace
- Mode lecture seule uniquement
- Pas de reponse automatique (jamais)
- Utilisez-les pour le contexte, pas pour l'action

```markdown
## Messaging
- Channels connectes : #general, #projet-alpha, #urgent
- Mode : lecture seule
- Usage : contexte pour le briefing, pas d'action directe
```

## Etape par etape

1. Connectez l'email en lecture seule (48h glissantes)
2. Activez le triage assiste pendant 2 semaines
3. Verifiez que le classement correspond a vos priorites
4. Ajoutez les brouillons de reponse
5. Si pertinent, passez au triage automatique apres validation
6. Les messages instantanes sont optionnels et viennent en dernier

## Erreurs courantes

**Connecter l'email en premier** : Sans calendrier et taches, l'agent ne peut pas prioriser vos emails. Il ne sait pas que vous etes en reunion toute la matinee ni que vous avez 5 taches urgentes.

**Donner le droit d'envoi immediatement** : Un email envoye par erreur a un client, ca ne se rattrape pas. Mode brouillon obligatoire au debut.

**Connecter toutes les boites** : 3 boites emails = 150 emails/jour dans le contexte. L'agent noie.

**Pas de regles de triage** : Sans regles explicites dans CONSTITUTION.md, l'agent trie selon son jugement. Son jugement ne connait pas vos priorites implicites.

**Oublier de deconnecter les sources bruitees** : Vous avez connecte la mailing list technique "au cas ou". 40 emails/jour de bruit pur.

## Verification

- [ ] Email connecte en lecture seule (48h glissantes)
- [ ] Triage assiste actif et valide
- [ ] Regles de triage documentees dans CONSTITUTION.md
- [ ] Brouillons de reponse fonctionnels
- [ ] Envoi direct desactive
- [ ] Aucune boite partagee ou personnelle connectee
- [ ] Si messaging connecte : 2-3 channels max, lecture seule
