---
status: complete
audience: both
chapter: 06
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 02 -- Consultant freelance

**Pour qui :** consultant independant travaillant seul, sans equipe technique
**Temps de mise en place :** 1 a 2 jours
**Difficulte :** Debutant

---

## Contexte

Un consultant freelance gere une dizaine de clients en parallele. Son quotidien : reunions, propositions commerciales, suivi de projets, facturation, et beaucoup d'emails. Il n'a pas de VPS, pas d'equipe technique, et pas envie de maintenir une infrastructure serveur.

Il veut un assistant IA qui l'aide a structurer sa journee, rediger plus vite, et ne rien oublier.

---

## Probleme

- Les emails clients s'accumulent sans priorisation
- Les propositions commerciales prennent trop de temps a rediger
- Le suivi client repose sur la memoire et des notes dispersees
- Pas de vision consolidee du temps passe par client
- Les relances de factures sont oubliees ou faites trop tard

---

## Configuration

### Infrastructure

| Composant | Choix | Cout mensuel |
|-----------|-------|-------------|
| Machine | Laptop personnel (macOS ou Linux) | -- |
| OpenClaw | Installation locale | -- |
| Calendrier | Google Calendar ou Nextcloud | gratuit ou existant |
| Email | Client email existant (Gmail, ProtonMail) | existant |
| Stockage | Dossier local + sync cloud existant | existant |

**Pas de VPS. Pas de base de donnees. Pas de Mattermost.** Tout tourne en local sur le laptop du consultant.

### Agent unique

Un seul agent OpenClaw, configure avec :
- Le system prompt du consultant (ton, domaine d'expertise, liste de clients)
- Acces en lecture aux fichiers locaux (propositions, notes, templates)
- Connexion au calendrier pour les briefings du matin

---

## Mise en place

### Jour 1 : Installation et configuration de base

1. Installer OpenClaw sur le laptop
2. Creer le system prompt avec le contexte du consultant :
   - Domaine d'expertise
   - Liste des clients actifs avec contexte court
   - Ton de communication prefere
   - Templates de propositions et emails types
3. Configurer l'acces aux fichiers locaux (dossier `~/clients/`)
4. Tester avec une premiere tache : "Resume mes notes du dernier rendez-vous avec [client X]"

### Jour 2 : Workflows quotidiens

1. Configurer le morning briefing :
   - L'agent lit le calendrier du jour
   - Il liste les taches en attente par client
   - Il signale les factures en retard
   - Il propose un ordre de priorite pour la journee
2. Configurer le triage email :
   - L'agent lit les emails recus (via export ou integration)
   - Il classe par urgence : action requise / information / peut attendre
   - Il propose des brouillons de reponse pour les emails urgents
3. Configurer le suivi client :
   - Apres chaque interaction, l'agent met a jour le fichier client
   - Il genere un resume hebdomadaire par client

---

## Resultat

Apres une semaine d'utilisation :

- **Morning briefing en 2 minutes** : le consultant commence chaque journee avec une vue claire de ses priorites, sans ouvrir 5 applications
- **Triage email** : les emails sont classes automatiquement. Les brouillons de reponse font gagner 30 a 45 minutes par jour
- **Suivi client automatise** : chaque client a un fichier a jour avec l'historique des interactions, les decisions prises, et les prochaines etapes
- **Propositions commerciales en 15 minutes au lieu de 2 heures** : l'agent genere un premier jet a partir du template et du contexte client. Le consultant ajuste et envoie
- **Zero relance oubliee** : l'agent signale les factures en retard dans le briefing du matin

---

## Lecons apprises

1. **Le system prompt est le coeur du systeme.** Un prompt vague donne des resultats generiques. Le consultant doit investir du temps pour decrire son contexte, son ton, et ses regles metier.

2. **Un fichier par client, pas une base de donnees.** Pour un freelance, des fichiers Markdown dans un dossier `~/clients/` sont plus simples et plus portables qu'une base de donnees.

3. **Le morning briefing change tout.** C'est le workflow le plus simple a mettre en place et celui qui a le plus d'impact. Commencer par la.

4. **Ne pas automatiser la relation client.** L'agent redige des brouillons. Le consultant relit, ajuste, et envoie. Le client ne doit jamais recevoir un email non relu.

5. **Sauvegarder le contexte agent.** Le system prompt et les fichiers clients doivent etre dans un dossier synchronise (cloud ou Git). Perdre le laptop ne doit pas signifier perdre la memoire de l'agent.

---

## Erreurs courantes

| Erreur | Consequence | Solution |
|--------|-------------|----------|
| Prompt trop generique | Reponses passe-partout, inutilisables | Ajouter le contexte specifique : clients, domaine, ton |
| Pas de structure de fichiers | L'agent ne retrouve pas les informations | Un dossier par client, des noms de fichiers coherents |
| Faire confiance au premier jet | Erreurs factuelles envoyees au client | Toujours relire avant envoi |
| Pas de backup | Perte du contexte en cas de panne | Sync cloud ou Git pour le dossier de travail |

---

## Template -- System prompt du consultant

```
Tu es l'assistant professionnel de [NOM], consultant en [DOMAINE].

Contexte :
- [NOM] travaille en independant depuis [ANNEE]
- Ses clients sont principalement des [TYPE DE CLIENTS]
- Son ton est professionnel mais direct, pas de jargon inutile

Clients actifs :
- [Client A] : [contexte court, projet en cours]
- [Client B] : [contexte court, projet en cours]
- [Client C] : [contexte court, projet en cours]

Regles :
- Tu rediges toujours des brouillons, jamais des messages finaux
- Tu signales si une information te manque plutot que d'inventer
- Tu utilises le vouvoiement dans les emails clients
- Tu notes les decisions et les prochaines etapes apres chaque interaction
- Tu rappelles les factures impayees de plus de 30 jours dans le briefing du matin

Workflows :
1. Morning briefing : calendrier + taches + factures + priorites
2. Triage email : urgent / info / peut attendre + brouillons
3. Proposition commerciale : template + contexte client + premier jet
4. Suivi client : mise a jour du fichier client apres chaque interaction
```

---

## Verification

- [ ] OpenClaw est installe et repond sur le laptop
- [ ] Le system prompt contient la liste des clients actifs
- [ ] Le morning briefing affiche les rendez-vous du jour
- [ ] Le triage email classe correctement un echantillon de 10 emails
- [ ] Une proposition commerciale test est generee en moins de 5 minutes
- [ ] Les fichiers clients sont dans un dossier synchronise

---

*Configuration minimaliste, zero infrastructure a maintenir. Ideal pour un premier contact avec OpenClaw.*
