---
status: complete
audience: both
chapter: 06
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 03 -- E-commerce

**Pour qui :** vendeur en ligne gerant une boutique (Shopify, WooCommerce, PrestaShop ou equivalent)
**Temps de mise en place :** 3 a 5 jours
**Difficulte :** Intermediaire

---

## Contexte

Un vendeur en ligne gere une boutique avec quelques centaines de references. Il vend sur sa propre boutique et potentiellement sur des marketplaces. Il est seul ou avec un assistant a temps partiel. Son quotidien : commandes a traiter, questions clients a repondre, stock a surveiller, et des decisions d'approvisionnement a prendre.

Il cherche un systeme qui automatise les taches repetitives sans dependre d'un SaaS supplementaire a 200 EUR/mois.

---

## Probleme

- Les questions clients arrivent par email, formulaire de contact, et marketplaces -- reponses lentes ou oubliees
- Le suivi de stock est manuel : ruptures decouvertes trop tard, surstock sur d'autres references
- Les rapports de vente sont generes a la main dans des tableurs
- Aucune alerte proactive sur les tendances (produit qui decolle, produit qui stagne)
- Le temps passe sur l'operationnel empeche de travailler sur la strategie

---

## Configuration

### Infrastructure

| Composant | Choix | Cout mensuel |
|-----------|-------|-------------|
| Serveur | VPS leger (Hetzner CX22 ou equivalent) | 5.00 EUR |
| OpenClaw | Installation sur le VPS | -- |
| Boutique | Plateforme e-commerce existante (API) | existant |
| Notifications | Email + webhook vers Mattermost ou Slack | -- |

### Agents

**Agent Support Client :**
- Lit les messages clients entrants (via API ou export)
- Classe par categorie : suivi commande / question produit / reclamation / autre
- Genere un brouillon de reponse adapte
- Escalade les reclamations vers le vendeur avec un resume

**Agent Stock :**
- Interroge l'API de la boutique quotidiennement
- Alerte quand un produit passe sous le seuil de reapprovisionnement
- Detecte les produits a rotation lente (pas de vente depuis X jours)
- Genere une suggestion de commande fournisseur

**Agent Reporting :**
- Genere un rapport quotidien : ventes, panier moyen, produits les plus vendus
- Genere un rapport hebdomadaire avec tendances et comparaison semaine precedente
- Signale les anomalies (chute de ventes soudaine, pic inhabituel)

---

## Mise en place

### Jour 1-2 : Infrastructure et connexion boutique

1. Provisionner le VPS et installer OpenClaw
2. Configurer l'acces API a la plateforme e-commerce
3. Tester la lecture des commandes et du stock via l'API
4. Creer la structure de fichiers pour les templates de reponse

### Jour 3 : Agent Support Client

1. Rediger le system prompt avec le ton de la boutique et les FAQ courantes
2. Configurer la lecture des messages entrants
3. Definir les regles de classification (suivi / question / reclamation)
4. Tester sur 20 messages reels
5. Ajuster le prompt selon les resultats

### Jour 4 : Agent Stock et Reporting

1. Configurer les seuils de reapprovisionnement par categorie de produit
2. Mettre en place l'alerte quotidienne de stock
3. Configurer le rapport de ventes quotidien
4. Tester le rapport hebdomadaire sur les donnees de la semaine precedente

### Jour 5 : Stabilisation

1. Configurer les notifications (email ou webhook)
2. Tester le flux complet sur une journee reelle
3. Ajuster les seuils et les templates selon les retours
4. Documenter les procedures pour l'assistant eventuel

---

## Resultat

Apres deux semaines d'utilisation :

- **Temps de reponse client divise par 3** : les brouillons de reponse sont prets en quelques secondes. Le vendeur relit, ajuste si necessaire, et envoie
- **Zero rupture de stock surprise** : les alertes arrivent 5 a 7 jours avant la rupture, laissant le temps de commander
- **Reporting automatique** : le rapport quotidien arrive chaque matin. Plus besoin de manipuler des tableurs
- **Detection de tendances** : l'agent a signale un produit dont les ventes avaient triple en une semaine, permettant un reapprovisionnement anticipe
- **2 heures liberees par jour** : le temps recupere sur le support et le reporting est reinvesti dans la strategie produit

---

## Lecons apprises

1. **Les FAQ couvrent 80% des questions.** Investir du temps pour rediger 20 a 30 reponses types dans le system prompt elimine la majorite du travail de support.

2. **Les seuils de stock doivent etre par categorie, pas universels.** Un produit a forte rotation a besoin d'un seuil plus haut qu'un produit de niche.

3. **Le rapport quotidien doit etre court.** 5 lignes maximum. Si le rapport est trop long, il n'est pas lu. Les details doivent etre accessibles a la demande.

4. **Ne pas automatiser les reclamations.** Une reclamation mal geree coute un client. L'agent resume et escalade, le vendeur repond personnellement.

5. **Tester sur des donnees reelles, pas des donnees fictives.** Les cas limites (produits en rupture, commandes annulees, retours) ne se revelent qu'avec des donnees de production.

---

## Erreurs courantes

| Erreur | Consequence | Solution |
|--------|-------------|----------|
| Reponses automatiques sans relecture | Client qui recoit une reponse incorrecte ou froide | Toujours relire les brouillons avant envoi |
| Seuil de stock unique pour tout | Ruptures sur les best-sellers, surstock sur les niches | Seuils differencies par categorie |
| Ignorer les erreurs API | Donnees de stock obsoletes | Monitoring des appels API, alerte en cas d'echec |
| Rapport trop detaille | Le rapport n'est pas lu | Rapport court avec lien vers le detail |

---

## Template -- System prompt de l'agent support client

```
Tu es l'assistant support de [NOM DE LA BOUTIQUE].

Contexte :
- Boutique en ligne vendant [TYPE DE PRODUITS]
- Clientele principalement [PAYS/REGION]
- Ton : professionnel, chaleureux, concis

Regles :
- Tu generes des brouillons de reponse, jamais des reponses finales
- Tu vouvoies toujours le client
- Tu ne promets jamais de remboursement ou de geste commercial sans validation du vendeur
- Tu escalades toute reclamation avec un resume factuel
- Tu inclus le numero de commande dans chaque reponse

Classification des messages :
1. Suivi de commande -> verifier le statut, repondre avec le tracking
2. Question produit -> repondre a partir de la fiche produit et des FAQ
3. Reclamation -> resumer le probleme, escalader au vendeur
4. Autre -> classer et signaler

FAQ :
- Delai de livraison : [X jours ouvrables]
- Politique de retour : [conditions]
- Modes de paiement : [liste]
```

---

## Verification

- [ ] L'API de la boutique est accessible depuis le VPS
- [ ] L'agent support classe correctement un echantillon de 20 messages
- [ ] Les alertes stock se declenchent au bon seuil sur un produit test
- [ ] Le rapport quotidien est genere et envoye chaque matin
- [ ] Les reclamations sont escaladees et non repondues automatiquement
- [ ] Les notifications arrivent par le canal choisi (email ou webhook)

---

*Un vendeur en ligne n'a pas besoin d'une equipe support. Il a besoin d'un agent bien configure et d'une relecture humaine.*
