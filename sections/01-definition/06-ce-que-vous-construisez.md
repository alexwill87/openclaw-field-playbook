---
status: complete
audience: both
chapter: 01
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 1.6 -- Ce que vous allez construire dans ce guide

**A qui s'adresse cette section :** Tout lecteur qui veut voir la destination avant d'entamer le chemin.
**Temps de lecture :** 8 minutes.
**Difficulte :** Debutant.

### Contexte

Avant de plonger dans les chapitres techniques, voici une vue d'ensemble de ce que vous aurez a la fin du parcours. Pas une promesse -- une cible.

### Le resultat final

A la fin de ce playbook, si vous suivez les etapes, vous aurez :

1. **Un serveur operationnel** -- un VPS (ou une machine locale) avec une stack technique propre, securisee, maintenable.
2. **Un ou plusieurs agents configures** -- avec des roles clairs, une memoire structuree, des outils connectes.
3. **Une base de connaissances** -- vos documents, vos regles, votre contexte, organises pour que les agents puissent les exploiter.
4. **Des workflows automatises** -- des sequences d'actions qui tournent sans votre intervention, avec des garde-fous.
5. **Un systeme de maintenance** -- sauvegardes, mises a jour, monitoring, pour que le tout continue a fonctionner dans la duree.

### Schema de l'architecture cible

```
+================================================================+
|                        VOTRE VPS / MACHINE                     |
|================================================================|
|                                                                |
|  +------------------+    +------------------+                  |
|  |   REVERSE PROXY  |    |    MONITORING    |                  |
|  |   (Caddy/Nginx)  |    |  (logs, alertes) |                  |
|  +--------+---------+    +------------------+                  |
|           |                                                    |
|  +--------v-------------------------------------------------+  |
|  |                    DOCKER NETWORK                         |  |
|  |                                                           |  |
|  |  +-------------+  +-------------+  +----------------+    |  |
|  |  |  AGENT 1    |  |  AGENT 2    |  |  AGENT N       |    |  |
|  |  |  (role A)   |  |  (role B)   |  |  (role ...)    |    |  |
|  |  +------+------+  +------+------+  +-------+--------+    |  |
|  |         |                |                  |             |  |
|  |  +------v----------------v------------------v---------+   |  |
|  |  |              COUCHE KNOWLEDGE                       |   |  |
|  |  |  +----------+  +-----------+  +----------------+   |   |  |
|  |  |  | Memoire  |  | Documents |  | Regles metier  |   |   |  |
|  |  |  +----------+  +-----------+  +----------------+   |   |  |
|  |  +----------------------------------------------------+   |  |
|  |                                                           |  |
|  |  +----------------------------------------------------+   |  |
|  |  |              COUCHE OUTILS                          |   |  |
|  |  |  +-------+  +-------+  +--------+  +-----------+   |   |  |
|  |  |  | Email |  |  API  |  | Fichiers|  | Calendrier|   |   |  |
|  |  |  +-------+  +-------+  +--------+  +-----------+   |   |  |
|  |  +----------------------------------------------------+   |  |
|  |                                                           |  |
|  +-----------------------------------------------------------+  |
|                                                                |
|  +-----------------------------------------------------------+  |
|  |  SECURITE : Vault / secrets, certificats SSL, firewall    |  |
|  +-----------------------------------------------------------+  |
|                                                                |
+================================================================+
```

### Ce que ce schema vous dit

**Tout tourne dans Docker.** Chaque composant est isole, reproductible, et peut etre mis a jour independamment.

**Les agents partagent une couche Knowledge commune.** Ils ne sont pas isoles les uns des autres -- ils peuvent partager du contexte, de la memoire, des regles. C'est ce qui permet la coordination.

**Les outils sont des connexions, pas des composants.** Votre email, vos API, vos fichiers -- ce sont des interfaces que les agents utilisent. Ils ne font pas partie de l'installation OpenClaw elle-meme.

**La securite est transversale.** Elle n'est pas un composant parmi d'autres -- elle enveloppe tout le reste. Vault pour les secrets, SSL pour les communications, firewall pour le perimetre.

### Ce que ce schema ne vous dit pas

Il ne montre pas la complexite reelle de la configuration. Chaque boite dans ce schema represente des heures de travail de configuration, de test et d'ajustement. Ce playbook vous guide a travers chacune de ces etapes.

Il ne montre pas non plus l'evolution dans le temps. Votre installation dans un mois ne ressemblera pas a votre installation du premier jour. C'est normal et souhaitable.

> **Principe :** Construisez l'architecture minimale qui fonctionne, puis iterez. Le schema ci-dessus est une cible, pas un prerequis. Votre premiere installation aura un seul agent, pas cinq.

> **Note de terrain :** Les installations les plus robustes que nous avons vues sont celles qui ont commence petit. Un VPS, un agent, un cas d'usage. Puis un deuxieme agent quand le premier tournait de maniere fiable. Puis un troisieme. La tentation de tout deployer d'un coup est forte. Resistez-y.
