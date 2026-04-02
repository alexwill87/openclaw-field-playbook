---
status: complete
audience: both
chapter: 06
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 05 -- Cabinet comptable

**Pour qui :** cabinet d'expertise comptable ou de gestion, de 3 a 20 collaborateurs
**Temps de mise en place :** 2 a 3 semaines
**Difficulte :** Avance (contraintes reglementaires)

---

## Contexte

Un cabinet comptable gere des dizaines de dossiers clients simultanement. Chaque dossier a ses echeances fiscales, ses documents a collecter, ses declarations a produire. Les collaborateurs passent un temps considerable sur le triage de documents, les rappels clients, et la verification de conformite.

Le cabinet veut utiliser OpenClaw pour automatiser les taches administratives repetitives tout en respectant strictement le RGPD et le secret professionnel.

---

## Probleme

- Le triage des documents recus (factures, releves, pieces justificatives) est manuel et chronophage
- Les echeances fiscales sont suivies dans des tableurs, avec des risques d'oubli
- Les rappels aux clients pour les pieces manquantes sont envoyes trop tard
- La verification de conformite (TVA, charges sociales) repose sur l'experience individuelle
- Les nouveaux collaborateurs n'ont pas acces a la jurisprudence et aux procedures internes de facon structuree

---

## Configuration

### Infrastructure

| Composant | Choix | Cout mensuel |
|-----------|-------|-------------|
| Serveur | VPS dedie en France (OVH, Scaleway) | 15-30 EUR |
| OS | Ubuntu 24.04 LTS | -- |
| OpenClaw | Installation on-premise | -- |
| Base de donnees | PostgreSQL (chiffrement au repos) | -- |
| Stockage documents | Systeme de fichiers chiffre (LUKS) | -- |
| Communication interne | Mattermost self-hosted | -- |

**Obligation : hebergement en France ou dans l'UE.** Le secret professionnel et le RGPD imposent que les donnees clients ne sortent pas de l'UE. Aucun appel API vers un LLM cloud ne doit contenir de donnees nominatives clients.

### Strategie d'anonymisation

Avant tout traitement par un LLM :
1. Les donnees nominatives (noms, SIRET, adresses, montants specifiques) sont remplacees par des placeholders
2. L'agent travaille sur les donnees anonymisees
3. Les placeholders sont restitues dans le resultat final
4. Les logs de l'agent ne contiennent jamais de donnees nominatives

### Agents

**Agent Triage :**
- Recoit les documents entrants (scan, email, upload)
- Classe par type : facture / releve bancaire / piece justificative / courrier fiscal / autre
- Associe au dossier client correspondant
- Signale les documents incomplets ou illisibles

**Agent Echeances :**
- Maintient le calendrier fiscal de chaque dossier
- Envoie des alertes aux collaborateurs : J-30, J-15, J-7, J-3
- Genere la liste des pieces manquantes pour chaque echeance
- Propose un brouillon de rappel client pour les pieces en retard

**Agent Conformite :**
- Verifie les declarations avant soumission
- Controle les taux de TVA appliques
- Detecte les incoherences entre les documents et les declarations
- Signale les points d'attention sans prendre de decision

---

## Mise en place

### Semaine 1 : Infrastructure securisee

1. Provisionner le VPS en France
2. Configurer le chiffrement du disque (LUKS)
3. Installer PostgreSQL avec chiffrement au repos
4. Installer OpenClaw
5. Configurer l'anonymisation des donnees (pipeline de pre-traitement)
6. Tester que les logs ne contiennent aucune donnee nominative

### Semaine 2 : Agents de triage et echeances

1. Deployer l'agent Triage avec les categories de documents du cabinet
2. Tester sur un echantillon de 50 documents reels (anonymises)
3. Configurer l'agent Echeances avec le calendrier fiscal en cours
4. Tester les alertes sur des echeances proches
5. Former 2 collaborateurs pilotes

### Semaine 3 : Conformite et deploiement

1. Deployer l'agent Conformite avec les regles fiscales de base
2. Tester sur 10 dossiers de declarations passees
3. Ajuster les regles selon les retours des experts-comptables
4. Deployer pour l'ensemble du cabinet
5. Documenter les procedures et les limites

---

## Resultat

Apres deux mois d'utilisation :

- **Triage automatise a 85%** : 85% des documents sont correctement classes et associes au bon dossier. Les 15% restants sont signales pour classification manuelle
- **Zero echeance oubliee** : les alertes progressives (J-30 a J-3) ont elimine les retards de declaration
- **Rappels clients en temps voulu** : les clients sont relances pour les pieces manquantes des que le seuil J-15 est atteint, au lieu du rappel de derniere minute habituel
- **Verification de conformite systematique** : chaque declaration passe par l'agent avant soumission. Il ne remplace pas l'expert-comptable mais detecte les erreurs mecaniques (mauvais taux, montant incoherent)
- **Confidentialite preservee** : l'audit des logs confirme l'absence de donnees nominatives dans les appels LLM

---

## Lecons apprises

1. **L'anonymisation est non negociable.** Ce n'est pas une option, c'est un prerequis. Le pipeline d'anonymisation doit etre teste et audite avant tout deploiement.

2. **L'agent Conformite assiste, il ne certifie pas.** L'expert-comptable reste responsable. L'agent detecte les anomalies, l'humain decide.

3. **Les categories de triage doivent correspondre aux categories du cabinet, pas a des categories generiques.** Chaque cabinet a sa propre nomenclature. Le prompt doit la refleter exactement.

4. **Hebergement en France, pas juste en UE.** Pour un cabinet comptable francais, l'hebergement en France simplifie la conformite et la communication avec les clients sur la securite de leurs donnees.

5. **Former les collaborateurs sur ce que l'agent ne fait pas.** La formation doit insister sur les limites : l'agent ne prend pas de decision fiscale, ne signe pas de declaration, ne communique pas directement avec les clients.

---

## Contraintes reglementaires

### RGPD

- Registre des traitements : documenter l'utilisation d'OpenClaw dans le registre RGPD du cabinet
- Base legale : interet legitime (amelioration de l'efficacite interne) ou consentement client selon les cas
- Droit d'acces : les clients doivent pouvoir demander quelles donnees sont traitees par l'agent
- Duree de conservation : aligner sur les obligations comptables (10 ans pour les pieces comptables)
- Sous-traitance : si un LLM cloud est utilise, le fournisseur est un sous-traitant au sens du RGPD

### Secret professionnel

- Aucune donnee nominative ne doit etre transmise a un service tiers sans anonymisation prealable
- Les acces a OpenClaw doivent etre traces et auditables
- Un collaborateur qui quitte le cabinet doit perdre immediatement ses acces

### Recommandations de l'Ordre des Experts-Comptables

- Documenter l'utilisation de l'IA dans les procedures internes
- Informer les clients de l'utilisation d'outils IA dans le traitement de leurs dossiers
- Maintenir la responsabilite humaine sur toute production fiscale ou comptable

---

## Erreurs courantes

| Erreur | Consequence | Solution |
|--------|-------------|----------|
| Envoyer des donnees nominatives au LLM | Violation du RGPD et du secret professionnel | Pipeline d'anonymisation obligatoire |
| Agent qui "decide" du taux de TVA | Erreur fiscale engageant la responsabilite du cabinet | L'agent propose, l'expert-comptable valide |
| Hebergement hors UE | Non-conformite RGPD | VPS en France, fournisseur UE uniquement |
| Pas de trace d'audit | Impossible de prouver la conformite | Logs complets et non modifiables |

---

## Template -- System prompt de l'agent Triage

```
Tu es l'assistant de triage documentaire du cabinet [NOM].

Ton role est de classer les documents recus et de les associer aux dossiers clients.

REGLE ABSOLUE : tu ne traites que des donnees anonymisees. Si tu detectes des
donnees nominatives non anonymisees dans un document, tu le signales immediatement
et tu ne le traites pas.

Categories de documents :
1. Facture d'achat
2. Facture de vente
3. Releve bancaire
4. Bulletin de salaire
5. Avis d'imposition
6. Piece justificative diverse
7. Courrier de l'administration fiscale
8. Document non classifiable -> signaler pour traitement manuel

Pour chaque document :
- Identifie la categorie
- Identifie le dossier client (via le placeholder client)
- Verifie la lisibilite et la completude
- Signale les anomalies (montant manquant, date illisible, document tronque)

Format de sortie :
Categorie : [categorie]
Dossier : [placeholder client]
Statut : complet / incomplet / illisible
Anomalies : [liste ou "aucune"]
```

---

## Verification

- [ ] Le VPS est heberge en France avec chiffrement du disque
- [ ] Le pipeline d'anonymisation fonctionne sur un echantillon de 20 documents
- [ ] Les logs ne contiennent aucune donnee nominative (audit)
- [ ] L'agent Triage classe correctement 80%+ d'un echantillon de 50 documents
- [ ] Les alertes d'echeances se declenchent aux bons seuils (J-30, J-15, J-7, J-3)
- [ ] L'agent Conformite detecte une erreur de taux de TVA inseree intentionnellement
- [ ] Le registre RGPD du cabinet mentionne le traitement OpenClaw

---

*Un cabinet comptable qui deploie de l'IA sans anonymisation prend un risque juridique disproportionne par rapport au gain operationnel. L'anonymisation est la premiere etape, pas la derniere.*
