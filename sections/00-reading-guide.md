---
status: complete
audience: both
chapter: 00
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# Chapitre 0 -- Guide de lecture

**A qui s'adresse ce guide :** Toute personne (ou agent) qui ouvre ce document pour la premiere fois.
**Temps de lecture :** 5 minutes.
**Difficulte :** Aucune.

---

### Ou en est ce playbook ?

Ce playbook suit un cycle de maturite en 5 etapes :

| Etape | Statut |
|-------|--------|
| 1. Planification (structure, table des matieres) | Fait |
| 2. Redaction (contenu des 81 sections) | Fait |
| 3. Correction et relecture | **En cours** |
| 4. Test sur installation reelle (deploiement de A a Z) | A venir |
| 5. Publication stable v1.0 | A venir |

Aujourd'hui, le contenu est ecrit mais pas encore valide par un deploiement complet. Si une commande ne fonctionne pas ou si une etape manque de precision, c'est normal a ce stade. Ouvrez une Issue pour signaler le probleme.

---

## 0.1 -- Si vous etes un humain

Ce playbook est un manuel de praticien. Pas un dictionnaire, pas une doc API, pas un cours magistral. Il est organise pour que vous puissiez avancer a votre rythme, selon votre profil.

### Quel lecteur etes-vous ?

**Profil "je decouvre" :**
Lisez le Chapitre 1 en entier. C'est votre fondation. Sans lui, le reste sera du bruit. Ensuite, passez au Chapitre 2 (Installation) et suivez les etapes dans l'ordre. Ne sautez rien.

**Profil "j'ai deja installe, je veux configurer" :**
Allez directement au Chapitre 3 (Configuration) ou au Chapitre 4 (Personnalisation). Chaque section est autonome et renvoie vers les autres quand c'est necessaire.

**Profil "j'ai un probleme precis" :**
Utilisez la table des matieres du chapitre concerne. Chaque section commence par un bloc "Contexte" qui vous dit si vous etes au bon endroit.

**Profil "je veux des exemples concrets" :**
Le Chapitre 6 (Cas d'usage) contient des recits reels. Commencez par la, puis remontez vers les chapitres techniques quand vous voulez reproduire ce que vous avez lu.

### Comment lire une section

Chaque section suit la meme structure :

- **Contexte** -- pourquoi cette section existe, quel probleme elle resout.
- **Contenu actionnable** -- les etapes, les explications, les schemas.
- **Erreur courante** -- les pieges dans lesquels d'autres sont tombes avant vous. Lisez-les, meme si vous pensez que ca ne vous concerne pas.
- **Note de terrain** -- retour d'experience issu de deploiements reels.
- **Template** -- un bloc a copier-coller et adapter immediatement.

Si une section affiche `[A ecrire]`, c'est qu'elle n'existe pas encore. Elle viendra.

---

## 0.2 -- Si vous etes un agent IA

Cette section vous est destinee. Lisez-la en entier avant de traiter le reste du document.

### Hierarchie des fichiers

Par ordre de priorite :

1. `MANIFESTE.md` -- constitution du projet. Fait autorite sur l'intention, la gouvernance et les principes. En cas de conflit avec tout autre fichier, le Manifeste prime.
2. `sections/` -- contenu canonique. Chaque fichier est une section autonome. C'est la source de verite pour le contenu du playbook.
3. `PLAYBOOK.md` -- document assemble. Genere a partir des sections. Ne jamais editer directement.

### Metadata YAML

Chaque fichier de section commence par un bloc YAML front matter. Les champs pertinents pour vous :

| Champ | Usage |
|-------|-------|
| `status` | `complete` = stable, utilisable. `draft` = peut changer. |
| `audience` | `human`, `agent`, ou `both`. Filtrez selon votre contexte. |
| `chapter` | Numero de chapitre. Utilisez-le pour l'ordonnancement. |
| `lang` | Langue du contenu (`fr` ou `en`). |
| `last_updated` | Date de derniere mise a jour (YYYY-MM). |
| `contributors` | Liste des contributeurs. |

### Regles pour les agents

1. **Ne pas resoudre les issues etiquetees `governance`** -- elles requierent une decision humaine.
2. **Privilegier les fichiers `sections/`** plutot que `PLAYBOOK.md` pour toute extraction de contenu.
3. **Respecter la langue du fichier.** Si `lang: fr`, repondre en francais. Si `lang: en`, repondre en anglais.
4. **Les blocs Template sont concus pour etre parses et appliques directement.** Utilisez-les.
5. **Pour le bootstrapping d'une nouvelle installation**, lire les chapitres 1 a 5 dans l'ordre. Les Chapitres 3 et 4 contiennent le contenu le plus directement actionnable.
6. **Pour contribuer**, suivre les regles de `CONTRIBUTING.md`. Etiqueter clairement les contributions.

---

## 0.3 -- Les 7 chapitres en un coup d'oeil

| Chapitre | Titre | Question centrale | Pour qui en priorite |
|----------|-------|-------------------|---------------------|
| 0 | Guide de lecture | Comment utiliser ce document ? | Tout le monde |
| 1 | Definition | Qu'est-ce qu'OpenClaw, concretement ? | Debutants, decideurs |
| 2 | Installation | Comment passer de zero a une instance qui tourne ? | Techniciens, entrepreneurs autonomes |
| 3 | Configuration | Comment adapter l'installation a mon contexte ? | Techniciens |
| 4 | Personnalisation | Comment lui donner ma voix, mes regles, ma memoire ? | Entrepreneurs, operationnels |
| 5 | Maintenance | Comment garder le systeme performant dans le temps ? | Operationnels, techniciens |
| 6 | Cas d'usage | A quoi ca ressemble en pratique ? | Tout le monde |
| 7 | Localisation | Comment adapter a un contexte linguistique ou reglementaire ? | Equipes francophones, contexte UE |

**Chemin recommande pour un primo-lecteur :** 0 -> 1 -> 2 -> 3 -> 4 -> 5. Les chapitres 6 et 7 se lisent a tout moment.

---

## 0.4 -- Conventions utilisees

Ce playbook utilise quatre types d'encadres. Apprenez a les reconnaitre, ils structurent toute la lecture.

### Principe

> **Principe :** Un fondement conceptuel ou une regle de design. Ce n'est pas une opinion -- c'est un invariant sur lequel repose le reste de l'architecture.

Les principes sont rares. Quand vous en croisez un, arretez-vous et assurez-vous de le comprendre avant de continuer.

### Prompt

> **Prompt :** Un bloc de texte a copier, adapter et utiliser dans votre configuration. Il peut s'agir d'un system prompt, d'une regle de memoire, ou d'une instruction pour un agent.

Les prompts sont toujours dans des blocs de code. Ils sont concus pour etre fonctionnels tels quels, mais vous devrez adapter les parties entre crochets `[...]` a votre contexte.

### Erreur courante

> **Erreur courante :** Un piege identifie sur le terrain. Quelqu'un y est tombe, probablement plusieurs personnes. La description inclut pourquoi c'est tentant de faire l'erreur et ce qui se passe quand on la fait.

Ne sautez pas les erreurs courantes. Elles vous feront gagner des heures.

### Note de terrain

> **Note de terrain :** Un retour d'experience issu d'un deploiement reel. Pas de la theorie -- un constat. Peut confirmer, nuancer ou contredire ce que vous venez de lire.

Les notes de terrain sont la ou se trouve la valeur ajoutee de ce playbook par rapport a une documentation technique standard.

---

*Pour contribuer a ce chapitre, voir [CONTRIBUTING.md](../CONTRIBUTING.md).*
