---
status: complete
audience: both
chapter: 03
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 3.20 -- Choisir sa stack : du minimum viable au setup complet

> Vous n'avez pas besoin de tout. Cette section vous aide a choisir les bons outils pour votre situation — et a comprendre ce que chacun apporte avant de l'installer.

**Pour qui :** tout le monde
**Prerequis :** installation de base terminee (chapitre 2)
**Difficulte :** Debutant a intermediaire
**Temps de lecture :** 15 minutes

---

## Contexte

Quand on decouvre OpenClaw et son ecosysteme, il est tentant de tout installer : monitoring, dashboards, multi-agents, remote mode, bot Telegram, base de donnees, pipeline CI/CD...

**C'est une erreur.**

Chaque outil ajoute de la complexite. Chaque service supplementaire est un service a maintenir, a surveiller, a debugger. L'objectif n'est pas d'avoir la stack la plus complete — c'est d'avoir la stack **la plus adaptee a votre besoin actuel**.

---

## Les 3 niveaux de stack

### Niveau 1 : Essentiel (1 jour d'installation)

C'est le minimum pour avoir un OpenClaw fonctionnel. C'est la ou **tout le monde doit commencer**.

| Composant | Role | Obligatoire ? |
|-----------|------|:------------:|
| **VPS + Ubuntu** | Le serveur | Oui |
| **Docker** | Isolation des services | Oui |
| **Node.js** | Runtime OpenClaw | Oui |
| **OpenClaw + Gateway** | Le coeur du systeme | Oui |
| **Vault** | Gestion des secrets | Oui |
| **Tailscale** | Acces securise au VPS | Oui |
| **PostgreSQL** | Base de donnees | Oui |

**Ce que vous pouvez faire avec le niveau 1 :**
- Parler a un agent IA via le terminal
- Stocker vos secrets de maniere securisee
- Avoir une base de donnees pour la memoire et les taches
- Acceder a votre VPS de n'importe ou via Tailscale
- Verifier la sante du systeme (`openclaw health`)

**Ce que vous ne pouvez PAS faire :**
- Recevoir des notifications (il faut Telegram)
- Avoir un agent autonome (il faut les crons)
- Connecter un deuxieme VPS (il faut le remote mode)
- Avoir un dashboard visuel

> **Recommandation :** Restez au niveau 1 pendant au moins 2 semaines. Apprenez a maitriser le gateway, le terminal, et les commandes de base. N'ajoutez rien tant que vous n'avez pas un besoin reel.

### Niveau 2 : Operationnel (1 semaine)

Ajoutez ces composants quand vous sentez des limites concretes avec le niveau 1.

| Composant | Ce qu'il apporte | Quand l'ajouter |
|-----------|-----------------|-----------------|
| **Telegram Bot** | Notifications, alertes, commandes rapides | Quand vous voulez etre prevenu sans etre devant le terminal |
| **Crons** | Taches planifiees (briefing matin, health check) | Quand vous voulez de l'automatisation |
| **Git + script deploy** | Versionning de vos configs, deploiement reproductible | Quand vous modifiez souvent les configs |
| **Health check cron** | Alerte Telegram si un service tombe | Des que vous avez Telegram |
| **Mattermost** | Communication entre agents et humains | Quand vous avez 2+ agents ou une equipe |

**Ce que le niveau 2 ajoute :**
- Votre agent peut vous prevenir quand quelque chose se passe
- Des taches tournent automatiquement (briefing matin, checks)
- Vos configurations sont versionnees et recuperables
- Vous pouvez communiquer avec vos agents depuis votre telephone

### Niveau 3 : Avance (quand le besoin se manifeste)

**N'installez ces composants QUE si vous avez un besoin explicite.**

| Composant | Ce qu'il apporte | Quand c'est justifie | Quand c'est du over-engineering |
|-----------|-----------------|---------------------|-------------------------------|
| **Remote mode** | Connexion multi-VPS | Vous gerez 2+ VPS ou un VPS client | Vous avez un seul VPS |
| **Multi-agents** | Plusieurs agents specialises | Vous avez des domaines separes (finance, clients, technique) | Vous etes seul avec un besoin simple |
| **Uptime Kuma** | Monitoring avec historique et graphes | Vous avez 5+ services a surveiller | Vous avez 2 containers |
| **ClawHub** | Marketplace de skills et configurations | Vous cherchez des integrations pretes a l'emploi | Vous avez des besoins tres specifiques |
| **Dashboard custom** | Interface visuelle pour non-techniques | Vous avez une equipe qui ne touche pas au terminal | Vous etes seul et a l'aise avec le terminal |
| **Prometheus + Grafana** | Metriques fines, dashboards detailles | Vous avez des SLA, 10+ services, une equipe ops | Tout le reste |

---

## Tableau de decision par profil

| Vous etes... | Stack recommandee | Ce que vous pouvez ignorer |
|-------------|-------------------|---------------------------|
| **Solo, debutant** | Niveau 1 | Tout le reste pendant 2 semaines |
| **Solo, a l'aise** | Niveau 1 + Telegram + Crons | Dashboard, multi-agents, monitoring avance |
| **Equipe de 2-3** | Niveau 2 + Mattermost | Prometheus, Grafana, dashboard custom |
| **Integrateur / consultant** | Niveau 2 + Remote mode | Dashboard custom |
| **Equipe technique (5+)** | Niveau 2 + Uptime Kuma + multi-agents | Prometheus (sauf si SLA) |
| **Entreprise avec SLA** | Niveau 3 complet | Rien — tout est justifie |

---

## ClawHub : l'ecosysteme OpenClaw

ClawHub est le marketplace d'OpenClaw. C'est l'endroit ou vous trouvez des skills, des configurations, et des integrations creees par la communaute.

### Ce que vous y trouvez

| Type | Exemples | Pour qui |
|------|----------|---------|
| **Skills** | CRM connector, invoice generator, email parser | Ceux qui veulent des integrations pretes |
| **Templates de config** | Config type agence, config type e-commerce | Ceux qui demarrent et veulent un point de depart |
| **Agents pre-configures** | Agent support client, agent comptable | Ceux qui veulent un agent operationnel rapidement |

### Quand utiliser ClawHub

- **Oui :** Vous cherchez une integration avec un outil specifique (Pennylane, Sellsy, etc.) et quelqu'un l'a deja faite.
- **Oui :** Vous demarrez et voulez un template de configuration pour votre metier.
- **Non :** Vous avez des besoins tres specifiques qui ne correspondent a aucun template.
- **Non :** Vous preferez tout construire vous-meme pour comprendre.

> **Note :** ClawHub est encore jeune. Le catalogue grandit avec la communaute. Si vous ne trouvez pas ce que vous cherchez, c'est normal — et c'est une opportunite de contribuer.

### Comment y acceder

```bash
# Rechercher un skill
$ openclaw hub search "crm"

# Installer un skill depuis ClawHub
$ openclaw hub install skill-crm-pulse

# Voir ce qui est installe
$ openclaw hub list
```

---

## Les outils un par un : ce que chacun apporte

Plutot que de lister des outils dans un tableau abstrait, voici ce que chacun resout concretement.

### Telegram Bot

**Le probleme qu'il resout :** "Je ne suis pas devant mon terminal mais je veux savoir si quelque chose a casse."

**Ce qu'il fait :**
- Envoie des alertes quand un health check echoue
- Permet d'envoyer des commandes rapides a l'agent depuis votre telephone
- Notifie quand une tache planifiee est terminee

**Installation :** Section 2.14
**Prerequis :** Rien de special
**Complexite ajoutee :** Faible (un token, un chat ID)

### Mattermost

**Le probleme qu'il resout :** "J'ai plusieurs agents et/ou une equipe. Je veux un canal de communication structure."

**Ce qu'il fait :**
- Canaux par sujet (technique, clients, finance...)
- Les agents postent leurs bilans et decisions
- Les humains peuvent commenter et valider
- Historique recherchable

**Installation :** Section 2.8 (PostgreSQL requis)
**Prerequis :** Niveau 1 complet
**Complexite ajoutee :** Moyenne (Docker container, configuration des canaux)

### Uptime Kuma

**Le probleme qu'il resout :** "Je veux savoir depuis combien de temps chaque service tourne et voir l'historique."

**Ce qu'il fait :**
- Monitore chaque service (HTTP, TCP, ping)
- Graphe d'uptime dans le temps
- Notifications multi-canal (Telegram, email, Slack)
- Page de statut publique (optionnel)

**Installation :** Section 5.10
**Prerequis :** Docker
**Complexite ajoutee :** Faible (un container, interface web)

### Prometheus + Grafana

**Le probleme qu'il resout :** "J'ai besoin de metriques fines (CPU, memoire, latence p99) et de dashboards pour une equipe ops."

**Ce qu'il fait :**
- Collecte des metriques systeme et applicatives
- Dashboards personnalisables
- Alertes sur seuils
- Correlation entre metriques

**Quand c'est justifie :**
- Vous gerez 10+ services
- Vous avez des SLA a respecter
- Vous avez une equipe qui consulte les dashboards

**Quand c'est du over-engineering :**
- Vous etes seul avec 3 containers
- Personne ne regarde les dashboards
- Un `openclaw health` + Telegram suffit

**Installation :** Section 5.10 (niveau 3)
**Prerequis :** Niveau 2 complet, Docker
**Complexite ajoutee :** Elevee (3 containers, configuration YAML, dashboards a creer)

> **Conseil :** Si vous hesitez entre Uptime Kuma et Prometheus+Grafana, prenez Uptime Kuma. Il couvre 90% des besoins de monitoring avec 10% de la complexite.

---

## La regle d'or

**N'installez un outil que quand vous ressentez un manque.** Si vous ne ressentez pas le manque, l'outil ne vous apportera rien — il ajoutera seulement de la maintenance.

La progression naturelle :

```
Semaine 1-2 : Niveau 1 (gateway + terminal + commandes de base)
         │
         ▼  "J'aimerais etre prevenu quand ca casse"
Semaine 3-4 : + Telegram + Health check cron
         │
         ▼  "Je veux automatiser le briefing du matin"
Mois 2 :     + Crons + Git deploy
         │
         ▼  "On est deux, on a besoin de se coordonner"
Mois 3+ :    + Mattermost + Multi-agents
         │
         ▼  "Je veux voir l'historique d'uptime"
Quand ca vient : + Uptime Kuma
```

Chaque ajout repond a un besoin que vous avez **reellement vecu**, pas a un besoin que vous imaginez.

---

## Erreurs courantes

**Tout installer le premier jour.** Vous passez 3 jours a configurer Grafana, Prometheus, Mattermost, un dashboard custom... et vous n'avez toujours pas parle a votre agent. Commencez par le niveau 1. Le reste viendra.

**Installer un outil "au cas ou".** Si vous n'avez pas un probleme concret que l'outil resout, ne l'installez pas. Vous pourrez toujours l'ajouter plus tard.

**Copier la stack d'un autre.** Ce qui fonctionne pour une equipe de 10 personnes avec des SLA ne fonctionne pas pour un solo entrepreneur. Construisez votre stack a votre rythme.

**Confondre outils et fonctionnalites.** Grafana n'est pas une fonctionnalite. C'est un outil qui affiche des metriques. Si `openclaw health` et Telegram vous suffisent, Grafana ne vous apportera rien de plus — juste de la maintenance.

---

## Verification

- [ ] Vous savez a quel niveau de stack vous etes actuellement.
- [ ] Vous pouvez expliquer pourquoi chaque composant installe est la.
- [ ] Vous n'avez pas d'outil installe "au cas ou".
- [ ] Vous avez un plan pour le prochain outil a ajouter (ou pas).
- [ ] Vous connaissez ClawHub et savez comment y chercher un skill.

---

## Temps estime

15 minutes de lecture. L'installation depend des composants choisis (voir les sections dediees pour chacun).
