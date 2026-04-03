---
status: complete
audience: human
chapter: 06
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 6.8 -- Artisan et TPE : un assistant IA pour ceux qui font tout seuls

> Vous etes plombier, electricien, consultant, photographe, ou coach. Vous etes seul ou presque. Vous faites tout : les clients, les devis, la compta, la com. Voici comment OpenClaw peut vous aider.

**Pour qui :** artisan ou entrepreneur de TPE qui gere tout seul son activite
**Temps de mise en place :** 3 heures (avec un installateur)
**Difficulte :** Debutant

---

## Contexte

Jean est artisan plombier a Montreuil. Il travaille seul. Ses journees : 7h sur les chantiers, puis le soir il repond aux clients, fait les devis, relance les impayes, met a jour son site. Il dort 5 heures par nuit. Il a entendu parler de "l'IA" par son comptable.

---

## Probleme

- Il perd des clients parce qu'il repond aux demandes 48h apres
- Ses devis prennent 30 minutes chacun alors que c'est toujours le meme format
- Il oublie de relancer les factures impayees
- Il ne sait pas quels prospects sont chauds et lesquels ont abandonne

---

## Configuration

### Ce que Jean a installe (avec l'aide d'un installateur)

| Composant | Detail | Cout |
|-----------|--------|------|
| VPS | Hetzner CPX11 (2 CPU, 4 Go RAM) | 4,50 EUR/mois |
| OpenClaw | Via OpenRouter (Claude Haiku) | ~10 EUR/mois |
| Canal | Telegram (@JeanPlomberieBot) | Gratuit |
| Email | Gmail connecte via skill Himalaya | Gratuit |

**Cout total : ~15 EUR/mois** -- moins cher qu'un abonnement Netflix.

### Ce que l'agent fait pour Jean

**Chaque matin a 7h (cron briefing) :**
- "3 nouveaux messages clients hier soir. 2 demandes de devis, 1 question sur un chantier en cours."
- "Facture #2024-089 impayee depuis 15 jours. Voulez-vous que j'envoie une relance ?"
- "Meteo : pluie demain, prevoir bache pour le chantier rue de la Paix."

**Quand un client envoie un email :**
- L'agent classe le message (demande de devis / question / reclamation / spam)
- Pour les demandes de devis : il prepare un brouillon base sur les devis precedents similaires
- Pour les questions : il repond avec les infos de la base de connaissances (horaires, zones d'intervention, tarifs)

**Chaque vendredi soir (cron resume) :**
- "Cette semaine : 5 nouveaux contacts, 3 devis envoyes, 1 chantier termine. Chiffre d'affaires estime : 2 400 EUR."

### System prompt de Jean (simplifie)

```
Tu es l'assistant de Jean, artisan plombier a Montreuil.

Tu geres :
- Le triage des emails entrants
- La preparation des brouillons de devis
- Les relances de factures impayees
- Le briefing quotidien

Tu ne fais JAMAIS :
- Envoyer un email sans que Jean valide
- Modifier un devis deja envoye
- Repondre a un client mecontent (escalade vers Jean)

Ton ton : professionnel, simple, pas de jargon technique.
Langue : francais uniquement.
```

---

## Resultat apres 2 mois

- Temps de reponse aux clients : 48h -> 4h (l'agent prepare, Jean valide depuis Telegram)
- Devis envoyes par semaine : 3 -> 8 (brouillons pre-remplis)
- Factures impayees : 5 -> 1 (relances automatiques)
- Jean dort 7 heures par nuit au lieu de 5

---

## Lecons apprises

1. **Commencer par UN seul use case.** Jean a commence par le triage email. Il a ajoute les devis 3 semaines plus tard, les relances encore apres.

2. **L'agent ne remplace pas Jean.** Il prepare. Jean valide. La confiance se construit etape par etape.

3. **Le cout le plus eleve n'est pas le serveur.** C'est le temps de configuration initiale (3 heures avec un installateur). Apres, c'est 15 EUR/mois.

4. **Telegram est le bon canal.** Jean est sur son telephone toute la journee. Un message Telegram, il le voit en 30 secondes. Un email, il le voit le soir.

---

## Erreurs courantes

| Erreur | Consequence | Solution |
|--------|-------------|----------|
| Tout automatiser d'un coup | L'artisan perd confiance, desactive tout | Commencer par un seul use case, valider, puis etendre |
| Laisser l'agent repondre sans validation | Reponse inappropriee a un client mecontent | Garder la validation humaine sur tout pendant le premier mois |
| Ignorer le canal de notification | L'artisan ne voit pas les alertes | Utiliser Telegram, pas email -- l'artisan est sur son telephone |
| Ne pas alimenter la base de connaissances | L'agent invente des tarifs ou des horaires | Passer 30 minutes a entrer les infos de base au demarrage |

---

## Template reutilisable

Checklist pour un artisan/TPE :

- [ ] Choisir un canal (Telegram recommande)
- [ ] Identifier LE use case le plus douloureux (souvent : repondre aux clients)
- [ ] Installer OpenClaw (seul ou avec un installateur)
- [ ] Configurer le triage email
- [ ] Tester pendant 1 semaine avec validation manuelle sur tout
- [ ] Ajouter un 2eme use case apres 2-3 semaines

---

## Verification

- [ ] L'agent envoie le briefing matinal sur Telegram
- [ ] Un email de test est correctement trie et un brouillon de reponse est genere
- [ ] Jean peut valider ou rejeter une action depuis Telegram
- [ ] Le resume hebdomadaire arrive le vendredi soir

---

*Ce cas d'usage est inspire d'une experience reelle de mise en place. Les montants et configurations sont representatifs d'un deploiement en Europe en 2026.*
