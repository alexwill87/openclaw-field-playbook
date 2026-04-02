---
status: complete
audience: both
chapter: 06
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 06 -- Startup early-stage

**Pour qui :** fondateurs de startup en phase de demarrage (pre-seed a seed), equipe de 2 a 8 personnes
**Temps de mise en place :** 3 a 5 jours
**Difficulte :** Intermediaire

---

## Contexte

Une startup early-stage a des ressources limitees et des besoins disproportionnes. Les fondateurs portent tous les roles : produit, commercial, technique, finance, RH. Ils doivent communiquer regulierement avec leurs investisseurs, surveiller le marche, recruter les premiers employes, et construire le produit -- le tout avec un budget serre.

OpenClaw peut devenir un multiplicateur de force en automatisant les taches a faible valeur ajoutee, liberant du temps pour les decisions strategiques.

---

## Probleme

- Les investor updates sont rediges a la derniere minute, souvent incomplets
- La veille concurrentielle est faite de facon sporadique et non structuree
- Le recrutement est lent : tri de CV manuel, suivi des candidatures dans des emails
- Les metriques cles (MRR, churn, runway) sont calculees manuellement dans des tableurs
- Les fondateurs passent plus de temps sur l'operationnel que sur la strategie

---

## Configuration

### Infrastructure

| Composant | Choix | Cout mensuel |
|-----------|-------|-------------|
| Serveur | VPS economique (Hetzner CX22) ou laptop local | 0-5 EUR |
| OpenClaw | Installation VPS ou locale | -- |
| Communication | Slack ou Mattermost (plan gratuit) | gratuit |
| Suivi | Notion, Linear ou fichiers Markdown | existant |
| Email | Service email existant | existant |

**Budget total : moins de 50 EUR/mois tout compris** (VPS + API LLM).

### Agents

**Agent Investor Relations :**
- Collecte les metriques cles depuis les outils de la startup (tableur, base de donnees, API)
- Genere un brouillon d'investor update mensuel au format standard
- Inclut : metriques cles, faits marquants, defis, besoins, prochaines etapes
- Le fondateur relit, ajuste le ton, et envoie

**Agent Veille :**
- Surveille les sources definies (blogs, newsletters, Product Hunt, reseaux sociaux)
- Genere un resume hebdomadaire des mouvements concurrentiels
- Signale les evenements critiques en temps reel (levee de fonds d'un concurrent, lancement produit)
- Classe par pertinence : impact direct / a surveiller / bruit de fond

**Agent Recrutement :**
- Trie les candidatures recues par adequation avec la fiche de poste
- Genere un resume de chaque CV avec points forts et points d'attention
- Propose un brouillon de reponse (acceptation pour entretien / refus courtois)
- Suit les candidatures en cours et relance les candidats en attente

---

## Mise en place

### Jour 1-2 : Infrastructure et agent Investor Relations

1. Installer OpenClaw (VPS ou local)
2. Configurer l'agent Investor Relations avec :
   - Le format d'investor update utilise par la startup
   - Les sources de metriques (tableur, API, base de donnees)
   - Le ton de communication avec les investisseurs
3. Tester en generant l'update du mois precedent
4. Comparer avec l'update reel et ajuster

### Jour 3 : Agent Veille

1. Definir les sources de veille (5 a 10 sources maximum au debut)
2. Definir les concurrents a surveiller
3. Configurer la frequence : resume hebdomadaire + alertes en temps reel
4. Tester sur la semaine ecoulee
5. Ajuster les filtres de pertinence

### Jour 4-5 : Agent Recrutement et stabilisation

1. Configurer l'agent Recrutement avec les fiches de poste actives
2. Definir les criteres de tri (competences requises, nice-to-have, red flags)
3. Tester sur un lot de 20 CV (reels ou anonymises)
4. Configurer les notifications pour l'ensemble des agents
5. Documenter les workflows pour l'equipe

---

## Resultat

Apres un mois d'utilisation :

- **Investor updates en 30 minutes au lieu de 3 heures** : l'agent collecte les metriques et genere le premier jet. Le fondateur ajuste le narratif et envoie. Les updates sortent a l'heure, chaque mois
- **Veille structuree** : le resume hebdomadaire remplace la surveillance sporadique. Deux alertes critiques ont ete detectees (lancement concurrent, changement reglementaire) qui auraient ete manquees autrement
- **Tri de CV accelere** : 80% du tri est fait par l'agent. Le fondateur ne passe du temps que sur les candidatures pre-selectionnees. Temps de recrutement reduit de 30%
- **Budget maitrise** : l'ensemble de la configuration coute moins de 50 EUR/mois, soit le prix d'un outil SaaS unique

---

## Lecons apprises

1. **L'investor update est le workflow a deployer en premier.** C'est regulier, structure, et chaque fondateur deteste le faire. L'impact sur la relation investisseur est immediat : les updates arrivent a l'heure et sont plus complets.

2. **La veille doit etre filtree agressivement.** 10 sources bien choisies valent mieux que 50 sources qui generent du bruit. L'agent doit etre configure pour ignorer le bruit, pas pour tout rapporter.

3. **Le tri de CV par IA a des biais.** L'agent peut eliminer des profils atypiques qui seraient de bons candidats. Le fondateur doit verifier un echantillon des candidatures refusees par l'agent pour calibrer.

4. **Pas de stack complexe en early-stage.** Si l'equipe a 3 personnes, un VPS a 5 EUR et des fichiers Markdown suffisent. PostgreSQL et Mattermost viendront quand l'equipe depassera 8 personnes.

5. **Documenter les prompts dans Git des le debut.** Meme en early-stage, les prompts sont du code. Les versionner permet de revenir en arriere quand un changement degrade les resultats.

---

## Erreurs courantes

| Erreur | Consequence | Solution |
|--------|-------------|----------|
| Investor update envoye sans relecture | Metriques incorrectes envoyees aux investisseurs | Toujours relire et valider les chiffres manuellement |
| Trop de sources de veille | Resume hebdomadaire trop long, non lu | Maximum 10 sources au debut, ajouter progressivement |
| Confiance aveugle dans le tri de CV | Bons candidats elimines par l'agent | Verifier un echantillon de candidatures refusees |
| Stack sur-dimensionnee | Temps passe a maintenir l'infra au lieu de construire le produit | Commencer minimal, evoluer avec l'equipe |

---

## Template -- System prompt de l'agent Investor Relations

```
Tu es l'assistant Investor Relations de [NOM DE LA STARTUP].

Contexte :
- [NOM] est une startup [SECTEUR] en phase [PHASE]
- Derniere levee : [MONTANT] en [DATE]
- Investisseurs : [LISTE]
- Metriques cles suivies : MRR, nombre d'utilisateurs, churn, runway

Format de l'investor update mensuel :

## [NOM] - Update [MOIS ANNEE]

### Metriques cles
| Metrique | Ce mois | Mois precedent | Variation |
|----------|---------|----------------|-----------|
| MRR | | | |
| Utilisateurs actifs | | | |
| Churn | | | |
| Runway (mois) | | | |

### Faits marquants
- [3 a 5 points positifs du mois]

### Defis
- [2 a 3 points de friction ou de risque]

### Comment vous pouvez aider
- [1 a 2 demandes concretes aux investisseurs]

### Prochaines etapes
- [3 a 5 objectifs pour le mois suivant]

Regles :
- Tu collectes les metriques depuis [SOURCE]
- Tu generes un brouillon, jamais un document final
- Tu ne specules pas sur les chiffres : si une donnee manque, tu le signales
- Tu gardes un ton professionnel et factuel, ni trop optimiste ni alarmiste
```

---

## Verification

- [ ] L'agent Investor Relations genere un update coherent avec les metriques disponibles
- [ ] Le format de l'update correspond a celui utilise habituellement par la startup
- [ ] L'agent Veille produit un resume hebdomadaire pertinent
- [ ] Les alertes critiques sont detectees et notifiees rapidement
- [ ] L'agent Recrutement classe correctement un lot de 20 CV test
- [ ] Le cout mensuel total reste sous 50 EUR

---

*Une startup early-stage n'a pas besoin d'une plateforme IA enterprise. Elle a besoin de 3 agents bien configures et d'un budget maitrise.*
