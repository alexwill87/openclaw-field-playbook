---
status: complete
audience: both
chapter: 02
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 2.21 -- Le Gateway : le coeur de votre installation

> Vous avez installe tous les composants. Avant de passer a la configuration, arretez-vous ici. Cette section explique pourquoi le gateway est la brique la plus importante de tout votre setup — et pourquoi le maitriser change tout.

**Pour qui :** tout le monde — entrepreneur, equipe technique, agent
**Temps de lecture :** 15 minutes
**Difficulte :** Debutant a intermediaire

---

## Contexte

Dans les sections precedentes, vous avez installe Docker, Vault, PostgreSQL, Tailscale, Node.js et OpenClaw. Vous avez demarre le gateway en service systemd (section 2.15) et verifie que tout tournait (section 2.16).

Mais une question reste : **qu'est-ce que le gateway fait, concretement ?**

La plupart des gens le voient comme "un service a demarrer". C'est une erreur. Le gateway est **le point central par lequel tout passe**. Il n'est pas un composant parmi d'autres — il est le composant qui relie tous les autres.

---

## Ce que le gateway fait reellement

Le gateway OpenClaw n'est pas un simple serveur HTTP. C'est un **hub de communication** :

```
                    ┌─────────────────┐
                    │     Vous        │
                    │  (terminal)     │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
     ┌──────────────┤    GATEWAY      ├──────────────┐
     │              │  (port 3000)    │              │
     │              └──┬──────┬───┬──┘              │
     │                 │      │   │                  │
┌────▼─────┐  ┌───────▼──┐ ┌─▼───▼──┐  ┌───────────▼──┐
│ Agents   │  │   Base    │ │ Vault  │  │ Services     │
│ (Claude, │  │ donnees   │ │(secrets│  │ externes     │
│  Haiku)  │  │(Postgres) │ │  API)  │  │ (Telegram,   │
│          │  │           │ │        │  │  OpenRouter)  │
└──────────┘  └───────────┘ └────────┘  └──────────────┘
```

### Il route les commandes

Quand vous tapez `openclaw status` dans votre terminal, c'est le gateway qui recoit la requete, interroge les composants (base de donnees, Vault, services), et vous renvoie la reponse. Sans gateway, vos commandes CLI ne font rien.

### Il gere les sessions

Chaque conversation avec un agent passe par le gateway. Il maintient le contexte, gere la memoire de session, et s'assure que les messages arrivent au bon modele IA via le bon provider.

### Il expose l'etat du systeme

Le gateway sait si PostgreSQL repond, si Vault est unseal, si le provider IA est accessible. C'est votre **source de verite en temps reel** sur la sante de l'installation.

### Il connecte les agents entre eux

Si vous avez plusieurs agents (section 3.17), c'est le gateway qui gere leurs interactions. En mode remote (section 3.18), c'est lui qui accepte les connexions WebSocket des clients distants.

### Il protege les secrets

Les cles API, tokens, et credentials ne transitent jamais en dehors du gateway. Il fait le pont entre Vault (ou sont stockes les secrets) et les services qui en ont besoin.

---

## Pourquoi c'est la premiere chose a maitriser

### Avant de construire un dashboard

C'est tentant de vouloir un joli tableau de bord pour tout visualiser. Mais un dashboard est une **couche supplementaire au-dessus du gateway**. Si vous ne maitrisez pas le gateway, votre dashboard affichera des donnees que vous ne comprenez pas — ou pire, des donnees fausses.

> **Lecon terrain :** Nous avons passe des semaines a construire un cockpit (dashboard Next.js avec Supabase) pour visualiser notre installation. Ca a marche... partiellement. Le vrai probleme : nous ne maitrisions pas suffisamment le gateway en-dessous. Chaque bug du cockpit etait en realite un probleme de gateway mal compris. Quand nous avons investi du temps dans la maitrise du gateway, 80% des besoins du dashboard etaient deja couverts par les commandes CLI.

### Avant d'ajouter des outils

Uptime Kuma, Grafana, Prometheus... ces outils ont leur place (section 3.20). Mais le gateway expose deja des informations de sante nativement. Commencez par les exploiter avant d'empiler des outils supplementaires.

### Avant de passer en multi-agents

Le mode remote (section 3.18) repose entierement sur le gateway. Un gateway mal compris = un mode remote fragile.

---

## Les 5 commandes gateway que vous devez connaitre

Avant d'aller plus loin dans le playbook, assurez-vous de maitriser ces commandes :

| Commande | Ce qu'elle fait | Quand l'utiliser |
|----------|----------------|-----------------|
| `openclaw gateway status` | Etat complet du gateway (connexions, uptime, sessions actives) | Tous les jours, en premier |
| `openclaw health` | Sante de tous les composants connectes | Apres un redemarrage ou un doute |
| `openclaw status --deep` | Statut detaille (memoire, tokens, config active) | Pour diagnostiquer un probleme |
| `openclaw gateway token list` | Liste les tokens d'acces actifs | Pour auditer qui a acces |
| `openclaw sessions` | Sessions en cours et recentes | Pour comprendre l'activite |

```bash
# Votre reflexe quotidien :
$ openclaw gateway status
$ openclaw health
```

Si ces deux commandes retournent un resultat vert, votre installation fonctionne. Si l'une est rouge, vous savez exactement ou chercher.

---

## Le gateway vs un dashboard : quand construire quoi

| Besoin | Le gateway suffit | Un dashboard aide |
|--------|-------------------|-------------------|
| Savoir si tout tourne | Oui (`openclaw health`) | Non necessaire |
| Voir les sessions en cours | Oui (`openclaw sessions`) | Utile pour l'historique visuel |
| Verifier les secrets | Oui (`openclaw gateway token list`) | Non necessaire |
| Visualiser des tendances sur 30 jours | Non | Oui |
| Partager un statut avec un non-technique | Non | Oui |
| Debugger un probleme en direct | Oui (`journalctl -u openclaw-gateway -f`) | Non necessaire |
| Avoir un ecran sur un mur qui montre que tout va bien | Non | Oui |

**Regle :** Si votre besoin est couvert par une commande gateway, utilisez la commande. Construisez un dashboard uniquement quand le gateway ne suffit plus — c'est-a-dire quand vous avez besoin de **visualisation dans le temps** ou de **partage avec des non-techniques**.

---

## Architecture : le gateway au centre

Voici comment penser votre installation :

```
         Le gateway est le CENTRE. Tout passe par lui.

    ┌──────────────────────────────────────────────────────┐
    │                     GATEWAY                          │
    │                                                      │
    │  ┌──────────┐  ┌──────────┐  ┌──────────────────┐   │
    │  │ Sessions │  │  Health   │  │  Authentication  │   │
    │  │  & Agents│  │  Checks  │  │  & Tokens        │   │
    │  └──────────┘  └──────────┘  └──────────────────┘   │
    │                                                      │
    │  ┌──────────┐  ┌──────────┐  ┌──────────────────┐   │
    │  │ Routing  │  │ WebSocket│  │  Logs & Metrics  │   │
    │  │ (models) │  │ (remote) │  │                  │   │
    │  └──────────┘  └──────────┘  └──────────────────┘   │
    └────────┬──────────┬──────────┬───────────────────────┘
             │          │          │
      ┌──────▼──┐ ┌─────▼───┐ ┌───▼─────────┐
      │Vault    │ │Postgres │ │OpenRouter   │
      │(secrets)│ │(donnees)│ │(modeles IA) │
      └─────────┘ └─────────┘ └─────────────┘
```

Quand quelque chose ne fonctionne pas, la premiere question est toujours : **que dit le gateway ?**

---

## Erreurs courantes

**Traiter le gateway comme un detail technique.** C'est la brique la plus importante. Si vous ne maitrisez qu'une chose, maitrisez le gateway.

**Construire un dashboard avant de maitriser le gateway.** Vous allez passer du temps a debugger le dashboard alors que le probleme est en-dessous. Maitriser le gateway d'abord, construire par-dessus ensuite.

**Ne pas verifier le gateway quotidiennement.** `openclaw gateway status` et `openclaw health` doivent devenir un reflexe. Comme verifier ses emails le matin.

**Ignorer les logs du gateway.** `journalctl -u openclaw-gateway -f` est votre meilleur ami en cas de probleme. Les logs du gateway vous disent exactement ce qui se passe.

---

## Verification

- [ ] Vous pouvez expliquer ce que fait le gateway en une phrase ("c'est le hub central qui relie tous les composants").
- [ ] `openclaw gateway status` fonctionne et retourne un resultat comprehensible.
- [ ] `openclaw health` retourne un resultat vert.
- [ ] Vous savez ou lire les logs du gateway (`journalctl -u openclaw-gateway -f`).
- [ ] Vous comprenez pourquoi maitriser le gateway vient avant construire un dashboard.

---

## Temps estime

15 minutes de lecture. 0 minute d'installation — tout est deja en place depuis les sections precedentes.

---

*La suite logique : comprendre comment interagir avec le gateway au quotidien via votre terminal (section 3.19).*
