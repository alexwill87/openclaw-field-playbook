---
status: complete
audience: both
chapter: 06
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 04 -- Equipe technique (5-15 personnes)

**Pour qui :** equipe de developpement ou d'operations de taille moyenne
**Temps de mise en place :** 1 a 2 semaines
**Difficulte :** Intermediaire

---

## Contexte

Une equipe technique de 5 a 15 personnes travaille sur un ou plusieurs produits logiciels. Le code est sur GitHub ou GitLab. La documentation existe mais est rarement a jour. Les code reviews prennent du temps. Les nouveaux arrivants mettent des semaines a etre autonomes.

L'equipe veut utiliser OpenClaw pour accelerer les taches repetitives sans remplacer le jugement humain sur les decisions d'architecture.

---

## Probleme

- La documentation technique est obsolete ou incomplete
- Les code reviews sont un goulot d'etranglement
- L'onboarding des nouveaux developpeurs est lent et informel
- Les decisions d'architecture sont prises en reunion mais mal documentees
- Les incidents en production sont resolus mais les post-mortems ne sont pas rediges

---

## Configuration

### Infrastructure

| Composant | Choix | Cout mensuel |
|-----------|-------|-------------|
| Serveur | VPS dedie ou instance cloud existante | variable |
| OpenClaw | Installation sur le serveur de l'equipe | -- |
| Code | GitHub ou GitLab (existant) | existant |
| Communication | Slack, Mattermost ou Teams (existant) | existant |
| Knowledge base | Wiki existant ou Markdown dans le repo | existant |

### Agents

**Agent Documentation :**
- Surveille les Pull Requests mergees
- Detecte les changements qui impactent la documentation existante
- Genere un brouillon de mise a jour de la documentation
- Poste le brouillon en commentaire sur la PR ou dans le canal documentation

**Agent Code Review :**
- Effectue une premiere passe sur les Pull Requests ouvertes
- Verifie : style, conventions de nommage, couverture de tests, patterns connus
- Poste un commentaire structure avec les points d'attention
- Ne bloque jamais une PR : ses commentaires sont informatifs, pas bloquants

**Agent Onboarding :**
- Maintient un guide d'onboarding a jour a partir de la knowledge base
- Repond aux questions des nouveaux arrivants sur le canal dedie
- Pointe vers la documentation existante plutot que de repondre directement
- Signale les questions recurrentes non couvertes par la documentation

**Agent Post-mortem :**
- Apres un incident, collecte les messages du canal incident
- Genere un brouillon de post-mortem structure (timeline, cause racine, actions)
- Le soumet a l'equipe pour validation et enrichissement

---

## Mise en place

### Semaine 1 : Fondations

1. Installer OpenClaw sur le serveur de l'equipe
2. Connecter l'API GitHub/GitLab
3. Deployer l'agent Code Review sur un repo pilote
4. Configurer les conventions de l'equipe dans le system prompt (style guide, patterns interdits, regles de nommage)
5. Tester sur 5 Pull Requests existantes
6. Ajuster le prompt selon les retours de l'equipe

### Semaine 2 : Agents complementaires

1. Deployer l'agent Documentation
2. Deployer l'agent Onboarding avec la knowledge base existante
3. Configurer l'agent Post-mortem avec le template de l'equipe
4. Former l'equipe sur l'utilisation et les limites de chaque agent
5. Definir les regles : l'agent informe, l'humain decide

---

## Resultat

Apres un mois d'utilisation :

- **Documentation a jour** : les brouillons de mise a jour sont generes automatiquement. Le taux de documentation obsolete baisse de 60% a 15%
- **Code reviews plus rapides** : la premiere passe de l'agent detecte les problemes mecaniques (style, nommage, tests manquants). Les reviewers humains se concentrent sur la logique et l'architecture. Temps moyen de review reduit de 40%
- **Onboarding structure** : les nouveaux arrivants ont un interlocuteur disponible 24h/24 pour les questions de base. Temps d'autonomie reduit de 3 semaines a 10 jours
- **Post-mortems systematiques** : chaque incident a son post-mortem redige dans les 24h, au lieu de "on le fera plus tard" (c'est-a-dire jamais)
- **Multi-agents coordonnes** : les agents partagent la knowledge base. Une mise a jour de documentation par l'agent Documentation est immediatement disponible pour l'agent Onboarding

---

## Lecons apprises

1. **Commencer par le Code Review, pas par la documentation.** L'agent Code Review a un impact visible immediatement et cree de l'adhesion dans l'equipe.

2. **Les conventions doivent etre explicites dans le prompt.** L'agent ne peut pas deviner le style guide de l'equipe. Si les regles ne sont pas ecrites, il applique des conventions generiques qui frustrent les developpeurs.

3. **L'agent ne doit jamais bloquer un workflow.** Ses commentaires sont informatifs. Le jour ou l'agent bloque une PR par erreur, l'equipe perd confiance et desactive tout.

4. **Les post-mortems automatiques sont le meilleur rapport effort/valeur.** Personne n'aime rediger un post-mortem. L'agent genere un premier jet a partir des messages du canal incident. L'equipe corrige et complete en 15 minutes.

5. **Prevoir un canal "feedback-agent" pour l'equipe.** Les developpeurs doivent pouvoir signaler quand l'agent se trompe. Ce feedback ameliore les prompts et maintient la confiance.

---

## Erreurs courantes

| Erreur | Consequence | Solution |
|--------|-------------|----------|
| Agent Code Review trop strict | Developpeurs qui ignorent tous ses commentaires | Ton informatif, jamais imperatif. Pas de faux positifs |
| Documentation generee sans relecture | Erreurs factuelles dans la knowledge base | Brouillon + validation humaine obligatoire |
| Pas de limite de scope pour l'agent Onboarding | Reponses hors sujet ou inventees | Limiter au contenu de la knowledge base existante |
| Deployer sur tous les repos en meme temps | Bruit excessif, rejet par l'equipe | Un repo pilote, puis extension progressive |

---

## Template -- System prompt de l'agent Code Review

```
Tu es l'assistant de code review de l'equipe [NOM].

Ton role est de faire une premiere passe sur les Pull Requests pour detecter
les problemes mecaniques. Tu ne remplaces pas le reviewer humain.

Regles :
- Tes commentaires sont informatifs, jamais bloquants
- Tu utilises le ton "suggestion" : "Considerez..." plutot que "Vous devez..."
- Tu ne commentes pas l'architecture ou les choix de design
- Tu pointes vers la documentation existante quand c'est pertinent

Ce que tu verifies :
1. Respect du style guide : [LIEN VERS LE STYLE GUIDE]
2. Conventions de nommage : [REGLES]
3. Couverture de tests : chaque nouvelle fonction doit avoir un test
4. Patterns interdits : [LISTE]
5. Fichiers de configuration modifies : signaler pour attention particuliere

Ce que tu ne fais pas :
- Evaluer la pertinence fonctionnelle du changement
- Suggerer des refactorings majeurs
- Commenter les choix d'architecture
- Bloquer ou approuver la PR

Format de ton commentaire :
## Premiere passe automatique

**Style :** [OK / X points a verifier]
**Tests :** [OK / tests manquants pour les fonctions X, Y]
**Attention :** [fichiers sensibles modifies, le cas echeant]

_Ce commentaire est genere par l'agent Code Review. Il ne remplace pas
la review humaine._
```

---

## Verification

- [ ] L'agent Code Review commente les PR du repo pilote
- [ ] Les commentaires respectent le ton informatif (pas de faux positifs bloquants)
- [ ] L'agent Documentation detecte les PR impactant la documentation
- [ ] L'agent Onboarding repond correctement a 10 questions types
- [ ] L'agent Post-mortem genere un brouillon coherent a partir d'un canal incident test
- [ ] Le canal feedback-agent est cree et l'equipe sait comment l'utiliser

---

*Les agents IA dans une equipe technique fonctionnent quand ils reduisent le bruit, pas quand ils en ajoutent.*
