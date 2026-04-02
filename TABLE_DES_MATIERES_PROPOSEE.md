# Table des matieres proposee — OpenClaw Field Playbook
### Version francaise complete
### Proposee le 2 avril 2026 — A valider par Omar et Alex

---

## Principes de cette structure

1. **Respecte le T1 existant** : les 7 chapitres d'Alex restent (0-7). On enrichit massivement les sous-sections.
2. **Fusionne technique et conceptuel** : chaque chapitre melange le "comment faire" (commandes, config) et le "pourquoi" (concepts de Steinberg, retours terrain).
3. **En francais** : tout le contenu est en francais. Les termes techniques anglais sont gardes quand il n'y a pas d'equivalent clair.
4. **Chaque section est autonome** : on peut lire une section sans avoir lu les precedentes (cross-references plutot que dependances).
5. **Format standard** par section : Contexte / Etape par etape / Erreurs courantes / Template / Verification

---

## Chapitre 0 — Guide de lecture

> Comment naviguer dans ce playbook — pour les humains et les agents IA.

- **0.1 — Si vous etes un humain**
  Comment lire ce guide, dans quel ordre, selon votre profil (debutant, intermediaire, expert)

- **0.2 — Si vous etes un agent IA**
  Hierarchie des fichiers, metadata YAML, regles de routing, permissions

- **0.3 — Les 7 chapitres en un coup d'oeil**
  Tableau synthetique : chapitre / question centrale / temps estime / difficulte

- **0.4 — Conventions utilisees dans ce guide**
  Encadres (Principe, Prompt, Erreur courante, Note de terrain), format des commandes, icones

---

## Chapitre 1 — Definition

> Qu'est-ce qu'OpenClaw ? Ce que c'est, ce que ce n'est pas, et pourquoi ca compte maintenant.

- **1.1 — Ce qu'OpenClaw est (et n'est pas)** *(existe deja — a enrichir)*
  Framework d'agents, pas un chatbot. Composabilite, souverainete, proactivite programmable.

- **1.2 — La distinction proactif vs reactif**
  Pourquoi un agent qui attend vos questions ne sert qu'a 20%. Le concept de "spirale" (Steinberg) : comprendre → automatiser → decider → reflechir.

- **1.3 — OpenClaw vs les autres assistants IA**
  Comparaison honnete : ChatGPT, Claude.ai, Copilot, AutoGPT, CrewAI. Forces et faiblesses reelles d'OpenClaw.

- **1.4 — Pourquoi la souverainete compte pour un entrepreneur**
  RGPD, controle des donnees, independance vis-a-vis des plateformes. Cas concret : que se passe-t-il si OpenAI change ses conditions demain ?

- **1.5 — L'architecture mentale avant de commencer**
  Les 3 couches : identite (qui est l'agent), visibilite (ce qu'il voit), action (ce qu'il fait). Le concept de "piliers" : blocs fonctionnels qui structurent une installation.

- **1.6 — Ce que vous allez construire dans ce guide**
  Vue d'ensemble du resultat final : un agent operationnel avec workspace, memoire, connexions, et routines. Schema visuel de l'architecture cible.

---

## Chapitre 2 — Installation

> De zero a une instance qui tourne. Pas a pas, sans suppositions.

### Partie A — Preparer le terrain

- **2.1 — Prerequis materiel et logiciel**
  Minimum requis : VPS (specs), OS (Ubuntu 24.04 recommande), acces SSH, comptes necessaires (Hetzner/OVH, Tailscale, GitHub, OpenRouter). Estimation budget mensuel.

- **2.2 — Securiser le VPS avant tout**
  Utilisateur non-root, cle SSH, desactiver mot de passe, UFW, mises a jour auto. C'est la base. Si cette etape est mal faite, rien d'autre ne compte.

- **2.3 — Reseau prive : Tailscale**
  Pourquoi un VPN mesh (pas un VPN classique). Installation, connexion, IP Tailscale. Principe : aucun service expose publiquement sauf SSH.

### Partie B — Infrastructure

- **2.4 — Docker et Docker Compose**
  Installation, ajout au groupe docker, verification. Pourquoi Docker (isolation, reproductibilite, nettoyage facile).

- **2.5 — Node.js, npm, PM2**
  Installation via nvm (pas apt). PM2 pour le process management. Pourquoi PM2 plutot que systemd pour les apps Node.

- **2.6 — Structure de dossiers**
  Convention proposee : ~/docker/, ~/scripts/, ~/backups/. Pourquoi cette structure (chaque chose a sa place, reproductible).

### Partie C — Services socle

- **2.7 — HashiCorp Vault : le coffre-fort des secrets**
  Pourquoi Vault (pas un .env, pas en clair). Installation Docker. Mode dev vs production. Initialisation, unseal, premier login. Stockage des premiers secrets (API keys, mots de passe DB). Script d'unseal automatique (optionnel, avec les risques). Sauvegarde des unseal keys HORS du VPS.

- **2.8 — PostgreSQL : la source de verite**
  Pourquoi une vraie DB (pas des fichiers .md comme source de verite). Installation Docker, creation de la DB oa_system, utilisateur, test de connexion. Backup automatique (pg_dump cron).

- **2.9 — Premier health check**
  Script de diagnostic rapide : Docker tourne ? Vault unseal ? Postgres repond ? Tailscale connecte ? Ce script sera reutilise tout au long du guide.

### Partie D — OpenClaw

- **2.10 — Installation propre d'OpenClaw**
  Methode recommandee (npm global ou script). Les erreurs classiques d'installation (permissions, version Node incompatible, path manquant).

- **2.11 — Structure du workspace**
  Les fichiers crees par defaut. Ce qu'il faut garder, ce qu'il faut personnaliser. Arborescence cible commentee.

- **2.12 — Configuration initiale (openclaw.json / config)**
  Fichier de config principal. Chaque champ explique. Connection a Vault pour les secrets (pas de cle API en clair). Choix du modele par defaut.

- **2.13 — Connexion a OpenRouter**
  Pourquoi OpenRouter (multi-modeles, un seul compte). Creation du compte, generation de la cle, stockage dans Vault. Test d'appel API. Choix du modele (Claude Sonnet vs Haiku vs Mistral vs Gemini — comparaison pragmatique).

- **2.14 — Connexion a Telegram**
  Creation du bot via @BotFather. Stockage du token dans Vault. Configuration dans OpenClaw. Recuperation du chat_id. Test d'envoi de message. Pourquoi Telegram (simple, mobile, notifications push, pas besoin d'app custom).

- **2.15 — Le gateway : service systemd**
  Creation du service, activation, demarrage. Logs (journalctl). Auto-restart. Verification que le gateway repond.

- **2.16 — Verification complete post-installation**
  `openclaw doctor` (ou equivalent). Checklist de 10 points. Si tout est vert, passer au chapitre suivant. Si non, diagnostic par symptome.

### Partie E — Git et versionning

- **2.17 — Initialiser le repo Git**
  git init, remote GitHub, .gitignore rigoureux (secrets, node_modules, .next, .env). Premier commit.

- **2.18 — CLAUDE.md : le fichier que tout agent IA doit lire**
  Conventions du repo, stack, commandes utiles, regles. Ce fichier permet a n'importe quel Claude Code d'etre operationnel sur le projet en 30 secondes.

- **2.19 — Script de deploiement**
  deploy.sh : git pull, npm ci, npm run build, pm2 restart. Idempotent, rapide, fiable.

---

## Chapitre 3 — Configuration

> Adapter OpenClaw a votre contexte — votre metier, vos outils, vos contraintes.

### Partie A — L'agent

- **3.1 — Definir le perimetre de votre agent**
  Ce qu'il doit faire vs ce qu'il ne doit jamais faire. La "pyramide des droits" (Steinberg) : lecture (toujours), ecriture (autonome), action externe (validation requise).

- **3.2 — SOUL.md : l'identite de votre agent**
  Ce fichier definit QUI est votre agent. Exemples commentes (agent direct, agent diplomatique, agent technique). Erreur classique : passer des heures sur SOUL.md et negliger USER.md.

- **3.3 — USER.md : votre profil pour l'agent**
  Ce fichier definit QUI VOUS ETES. L'onboarding interview (Steinberg) : 20 questions pour que l'agent vous comprenne vraiment. Validation : "Decris-moi en 5 phrases" — si c'est generique, c'est a refaire.

- **3.4 — AGENTS.md : le registre**
  Liste de tous les agents, leurs roles, leurs modeles, leurs permissions. Boot sequence : l'ordre dans lequel l'agent lit ses fichiers au demarrage.

- **3.5 — CONSTITUTION.md : les regles du jeu**
  Les 3 niveaux d'autonomie. Les interdictions explicites. Les conditions de validation. Ce fichier est le contrat entre vous et votre agent.

### Partie B — La memoire

- **3.6 — Les trois zones de memoire (Steinberg)**
  Memoire chaude (contexte de session), memoire tiede (MEMORY.md, 80 lignes max), memoire froide (fichiers thematiques dans knowledge/). Principe : ce qui change souvent ne vit pas au meme endroit que ce qui est stable.

- **3.7 — MEMORY.md : la memoire collective**
  Structure recommandee. Regle des 80 lignes. Nettoyage automatique ("Night consolidation" — Steinberg). Oubli volontaire : quand et pourquoi supprimer des souvenirs.

- **3.8 — Le dossier knowledge/ : la base de connaissances**
  Organisation par domaine (infra/, business/, guides/). Un fichier par sujet. Cross-references plutot que duplication.

### Partie C — Les connexions

- **3.9 — Principe : une source a la fois, pas en vrac (Steinberg)**
  Chaque nouvelle source augmente le cout en tokens, le risque d'interpretation, et le bruit. Connecter, valider ("qu'est-ce qui a change ?"), garder seulement si ca ameliore une decision cette semaine.

- **3.10 — Calendrier d'abord, toujours (Steinberg)**
  Le calendrier est le signal le plus honnete. Configuration via skill (Gog, Google Calendar). Validation : "Montre-moi mes prochaines 48h."

- **3.11 — Taches : la pression invisible**
  Le calendrier dit ce qui est planifie. Les taches disent ce qui ne l'est pas mais qui est reel. Connexion a la DB PostgreSQL ou a un outil externe.

- **3.12 — Email et messages**
  Connexion email (Himalaya ou autre). Triage automatique vs triage assiste. Pieges : ne pas tout connecter, filtrer par pertinence.

- **3.13 — Construire un skill custom (Steinberg)**
  Quand il n'y a pas de skill pre-fait. Prompt generique pour demander a l'agent de creer un skill. Les 4 parties d'un bon skill : authentification, requetes, perimetre, garde-fous. Lire le SKILL.md que l'agent a cree (toujours). Supprimer les regles de decision (elles n'ont pas leur place dans un skill).

- **3.14 — Souverainete des donnees**
  Ou vivent vos donnees ? Local, cloud, hybride. RGPD et implications. Recommandation : heberger en Europe (Hetzner, OVH, Scaleway).

### Partie D — Triggers et automatisations

- **3.15 — Les crons : automatisations planifiees**
  Briefing du matin, recap du soir, triage email, heartbeat. Comment configurer (`openclaw cron add`). Commencer par un seul cron, valider, puis ajouter.

- **3.16 — Le briefing du matin (Steinberg)**
  Le test ultime de votre configuration. Prompt : "Donne-moi un briefing du matin avec les sources connectees." Si c'est generique, le probleme est en amont (USER.md trop mince, pas assez de sources). Exemples de bons vs mauvais briefings.

- **3.17 — Architecture multi-agents**
  Quand un seul agent ne suffit plus. Agents specialises (contenu, vente, support). Isolation des workspaces. Communication inter-agents. Attention : ne pas commencer par la avant d'avoir un agent principal solide.

---

## Chapitre 4 — Personnalisation

> Faire d'OpenClaw le votre — votre voix, vos regles, vos workflows, votre rythme.

### Partie A — Identite et voix

- **4.1 — Ecrire votre system prompt**
  Le texte le plus important que vous ecrirez pour votre agent. Structure recommandee : mission, contexte, outils, regles, ton. Erreur classique : trop long (cout en tokens a chaque session).

- **4.2 — Definir la personnalite et le ton**
  Direct ou diplomatique ? Humoristique ou professionnel ? Comment le formuler de facon actionnable ("3 phrases max sauf si je demande plus" plutot que "communication directe"). Tutoiement vs vouvoiement selon le contexte.

- **4.3 — Iteration : votre premiere version ne sera pas la bonne**
  C'est normal. Prompt de correction : "Ta description de moi est trop [generique/pro/casual]. Voici ce qui manque : [...]." Compter 2-3 iterations pour une USER.md qui sonne juste. Puis condenser (150 mots > 500 mots pour le meme resultat).

### Partie B — Systeme de taches

- **4.4 — Pourquoi un systeme de taches dans l'agent (Steinberg)**
  L'agent sans taches est un conseiller. L'agent avec taches est un partenaire. Commencer simple (checklist), evoluer vers des sections.

- **4.5 — Comment les taches se font (Steinberg)**
  Le workflow : l'agent propose, vous decidez, l'agent execute (ou vous executez). Triage sans deleguer le jugement. Les taches nourrissent le briefing du matin.

- **4.6 — Base de donnees comme source de verite**
  Schema PostgreSQL pour les taches (id, titre, statut, priorite, owner, node, deadline). Pourquoi la DB plutot que des fichiers .md. Requetes utiles. Scripts CLI.

### Partie C — Workflows et routines

- **4.7 — Reconnaitre une routine (Steinberg)**
  Tout ce qui se repete au moins 3 fois et suit un schema previsible est candidat a l'automatisation. Mais pas tout : certaines routines ont besoin de votre jugement.

- **4.8 — Dry run avant confiance (Steinberg)**
  Toujours tester une automatisation en mode "montre-moi ce que tu ferais" avant de la laisser agir. Premier essai = lecture seule. Deuxieme essai = action avec validation. Troisieme essai = autonome (si les deux premiers etaient bons).

- **4.9 — WORKFLOWS.md : documenter vos procedures**
  Comment creer une tache, mettre a jour un projet, deployer le cockpit, faire une rotation de secrets. Chaque workflow = prerequis, etapes, verification.

- **4.10 — Le rythme hebdomadaire (Steinberg)**
  Deux ancres : preview du lundi (qu'est-ce qui arrive cette semaine ?) et review du vendredi (qu'est-ce qui s'est passe ?). L'agent prepare les deux. Garder ca leger et reviewable.

### Partie D — Securite et confiance

- **4.11 — La confiance est une configuration, pas un sentiment (Steinberg)**
  La pyramide des droits : lecture / ecriture / action externe. Chaque niveau a ses regles. Les ecrire explicitement dans CONSTITUTION.md.

- **4.12 — Le boundary prompt (Steinberg)**
  Un prompt que vous ecrivez une fois et qui definit ce que l'agent ne doit JAMAIS faire. Exemples : jamais envoyer un email sans validation, jamais modifier les fichiers identitaires, jamais depenser de l'argent.

- **4.13 — Audit : que peut reellement acceder votre agent ?**
  Prompt d'auto-audit : "Liste tout ce a quoi tu as acces en ce moment." Verifier que la realite correspond a vos intentions. Budget tokens et couts.

- **4.14 — Configuration bilingue**
  Travailler en francais, en anglais, ou les deux. Quand basculer et comment. Recommandation de modeles par langue (Mistral pour le francais, Claude pour le bilingue).

---

## Chapitre 5 — Maintenance

> Garder votre installation OpenClaw performante, precise, et digne de confiance dans le temps.

### Partie A — Operations quotidiennes

- **5.1 — Le health check quotidien**
  Script de diagnostic : services Docker, Vault, DB, gateway, Tailscale. Automatiser avec un cron. Alerte Telegram si un service tombe.

- **5.2 — Gestion des logs**
  Ou sont les logs (journalctl, docker logs, sessions OpenClaw). Comment les lire. Rotation automatique. Ce qu'il faut surveiller.

- **5.3 — Backups**
  pg_dump pour la DB. Snapshots Hetzner. Backup des fichiers critiques (Vault, config, workspace). Frequence recommandee. Test de restauration (le backup qu'on ne teste jamais est un faux backup).

### Partie B — Maintenance de l'agent

- **5.4 — Revoir et mettre a jour le system prompt**
  A quelle frequence ? Quels declencheurs (changement de metier, nouveau client, nouvel outil) ? Quoi preserver vs quoi rewriter.

- **5.5 — Gerer la derive de la memoire (Steinberg)**
  Quand la memoire de l'agent devient obsolete ou contradictoire. Nettoyage periodique. "Night consolidation" : l'agent resumerise et compresse sa propre memoire. Oubli volontaire.

- **5.6 — Quand l'agent se trompe**
  Protocole : diagnostic (pourquoi ?), correction (comment ?), prevention (que changer pour que ca n'arrive plus ?). Le prompt de correction : "Tu surinterpretes ces donnees. Reformule : signal, incertitude, et une question pour moi avant de recommander."

- **5.7 — Mettre a jour les integrations**
  Quand une API change, quand un outil evolue. Comment adapter sans tout casser. Garder les skills a jour.

### Partie C — Maintenance de l'infrastructure

- **5.8 — Mises a jour systeme**
  Ubuntu : apt update regulier. Docker : mise a jour des images. Node.js : mise a jour via nvm. Vault : mise a jour du binaire. Quand NE PAS mettre a jour (avant un deploy critique).

- **5.9 — Rotation des secrets**
  Pourquoi (securite). Comment (generer nouveau secret, stocker dans Vault, restart le service, tester, logger). Frequence recommandee.

- **5.10 — Monitoring et alertes**
  Options : simple (script cron + Telegram), intermediaire (Uptime Kuma), avance (Grafana + Prometheus). Recommandation pour commencer : le script cron suffit.

- **5.11 — En cas de panne**
  Tableau diagnostic par symptome : cockpit inaccessible, DB connexion refused, Vault sealed, gateway down, plus de RAM. Pour chaque symptome : diagnostic, fix, prevention.

### Partie D — Evolution

- **5.12 — Quand ajouter un deuxieme agent**
  Signes qu'un seul agent ne suffit plus. Comment structurer le deuxieme. Isolation des workspaces. Communication inter-agents.

- **5.13 — Quand migrer vers un autre modele**
  Les modeles evoluent. Comment tester un nouveau modele sans tout casser. Comparaison A/B sur les memes prompts. Garder le fallback.

- **5.14 — Mesurer le ROI de votre installation**
  Temps gagne, decisions ameliorees, erreurs evitees. Comment le mesurer concretement (pas du feeling, des donnees).

---

## Chapitre 6 — Cas d'usage

> Retours de terrain de vrais praticiens. Comment ils utilisent OpenClaw, ce qu'ils ont configure, ce qui a change.

### Partie A — Entrepreneurs et freelances

- **6.1 — Agence digitale (2 associes + agents IA)**
  Configuration : VPS Hetzner, Vault, PostgreSQL, Mattermost, cockpit web. Piliers : Infra, Agents, Knowledge, Business, Communication. Resultats apres 3 mois.

- **6.2 — Consultant freelance**
  Communication client, redaction de propositions, suivi du temps. Configuration minimaliste qui fonctionne.

- **6.3 — E-commerce**
  Gestion des commandes, support client, monitoring inventaire. Integration avec les outils de vente.

### Partie B — Equipes et entreprises

- **6.4 — Equipe technique (5-15 personnes)**
  Base de connaissances interne, assistant de code review, documentation automatique. Multi-agents specialises.

- **6.5 — Cabinet comptable**
  Triage de dossiers, conformite fiscale, rappels clients. Contraintes RGPD et secret professionnel.

- **6.6 — Startup early-stage**
  Updates investisseurs, veille concurrentielle, pipeline de recrutement. Budget serre, impact maximum.

### Partie C — Contribuer votre cas d'usage

- **6.7 — Comment soumettre votre retour d'experience**
  Format : Contexte / Probleme / Configuration / Resultat / Template reutilisable. Via Issue GitHub ou PR.

---

## Chapitre 7 — Localisation

> Contexte local par geographie — legislation, ecosysteme, pratiques culturelles.

- **7.1 — France (fr-FR)** *(existe deja — a enrichir)*
  RGPD, AI Act, droit du travail. Ecosysteme (OVH, Scaleway, Pennylane, Sellsy). Rythme business francais (aout, rentree, dejeuner). Vouvoiement/tutoiement. Modeles recommandes pour le francais.

- **7.2 — Belgique (fr-BE)**
  Specificites reglementaires, ecosysteme local, bilinguisme.

- **7.3 — Suisse (fr-CH)**
  LPD (protection des donnees suisse), hebergement Infomaniak, multilinguisme.

- **7.4 — Quebec (fr-CA)**
  Loi 25, ecosysteme nord-americain avec specificites francophones.

- **7.5 — Afrique francophone**
  Contraintes d'infrastructure (bande passante, hebergement), ecosysteme mobile-first, outils locaux.

---

## Annexes

- **A — Glossaire**
  Tous les termes techniques utilises dans le playbook, expliques simplement.

- **B — Checklist complete d'installation**
  La liste a cocher de A a Z, sans explication. Pour ceux qui connaissent deja et veulent aller vite.

- **C — Ports et services**
  Tableau de tous les ports utilises, quel service, quel bind.

- **D — Commandes de diagnostic rapide**
  Le "cheat sheet" des commandes a connaitre par coeur.

- **E — Ressources externes**
  Documentation OpenClaw officielle, livre de Steinberg, communaute, outils recommandes.

- **F — Modele de template pour contribuer une section**
  Le format standard copier-coller pour ecrire une nouvelle section.

---

## Statistiques de la structure

| Chapitre | Sections | Sous-sections estimees |
|----------|----------|----------------------|
| 0 — Guide de lecture | 4 | ~4 |
| 1 — Definition | 6 | ~12 |
| 2 — Installation | 19 | ~40 |
| 3 — Configuration | 17 | ~35 |
| 4 — Personnalisation | 14 | ~30 |
| 5 — Maintenance | 14 | ~28 |
| 6 — Cas d'usage | 7 | ~14 |
| 7 — Localisation | 5 | ~10 |
| Annexes | 6 | ~12 |
| **Total** | **92 sections** | **~185 sous-sections** |

---

## Ce qui vient du livre de Steinberg (integre dans les sections)

| Concept Steinberg | Ou dans notre playbook |
|-------------------|----------------------|
| La Spirale (comprendre → automatiser → decider → reflechir) | 1.2 |
| Onboarding Interview (20 questions) | 3.3 |
| USER.md vs SOUL.md (identite vs caractere) | 3.2, 3.3 |
| Les 3 zones de memoire | 3.6 |
| Night consolidation / oubli volontaire | 3.7, 5.5 |
| Calendrier d'abord, toujours | 3.10 |
| Une source a la fois, pas en vrac | 3.9 |
| Construire un skill custom (4 parties) | 3.13 |
| Le morning briefing test | 3.16 |
| La pyramide des droits | 3.1, 4.11 |
| Le boundary prompt | 4.12 |
| Systeme de taches (commencer simple) | 4.4, 4.5 |
| Dry run avant confiance | 4.8 |
| Reconnaitre une routine | 4.7 |
| Le rythme hebdomadaire | 4.10 |
| Le prompt de correction | 5.6 |
| Audit d'acces | 4.13 |

---

## Prochaine etape

Omar valide cette structure, puis on ecrit section par section.
Chaque section est un fichier .md independant dans sections/.
