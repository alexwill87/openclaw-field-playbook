---
status: complete
audience: both
chapter: 04
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 4.13 -- Audit : que peut acceder votre agent ?

## Contexte

Vous avez configure votre agent, defini les boundaries, ecrit le system prompt. Mais savez-vous vraiment ce qu'il peut faire ? La realite de ses acces correspond-elle a votre intention ?

L'audit repond a cette question. C'est un inventaire : ce que l'agent peut lire, ecrire, executer, et ce que ca coute.

## Le prompt auto-audit

Demandez a votre agent de s'auditer :

```
Fais un audit complet de tes acces. Pour chaque categorie,
liste ce que tu PEUX faire et ce que tu NE PEUX PAS faire.

Categories :
1. Systeme de fichiers : quels dossiers/fichiers peux-tu lire ? ecrire ? supprimer ?
2. Base de donnees : quelles tables ? SELECT/INSERT/UPDATE/DELETE ?
3. Services : quels containers peux-tu demarrer/arreter/redemarrer ?
4. Reseau : quels ports peux-tu atteindre ? quelles API externes ?
5. Git : quelles operations ? sur quelles branches ?
6. Secrets : quels secrets peux-tu lire ? via Vault ? en clair ?

Pour chaque acces, dis-moi si c'est intentionnel ou si ca devrait etre restreint.
```

## Verifier realite vs intention

L'audit revele souvent des surprises :

| Intention | Realite | Action |
|---|---|---|
| Lecture seule sur /opt | Lecture + ecriture | Restreindre les permissions |
| Pas d'acces aux backups | Peut lire /var/backups | Changer les permissions du dossier |
| SELECT uniquement sur DB | L'utilisateur a tous les droits | Creer un role PostgreSQL read-only |
| Pas d'acces aux secrets | Peut lire .env | Deplacer les secrets dans Vault |

### Verifications manuelles

Ne vous fiez pas uniquement a l'auto-audit. L'agent peut ne pas connaitre toutes ses permissions. Verifiez :

```bash
# Quels fichiers l'agent peut lire (testez avec l'utilisateur qui execute l'agent)
find /opt /home /var -readable -type f 2>/dev/null | head -50

# Droits PostgreSQL
psql -c "\du" 
psql -c "\dp" # permissions sur les tables

# Ports ouverts accessibles
ss -tlnp

# Variables d'environnement (secrets potentiels)
env | grep -i "key\|secret\|token\|pass\|api"
```

## Budget tokens et couts

L'audit, c'est aussi le cout. Chaque requete a un cout en tokens. Tracez-le.

### Calculer le cout

```
Cout par requete = tokens input + tokens output

Tokens input = system prompt + contexte + memoire + votre message
Tokens output = reponse de l'agent

Prix (Claude Sonnet, avril 2026) :
- Input : ~3$ / million de tokens
- Output : ~15$ / million de tokens
```

### Ce qui coute cher

| Element | Tokens typiques | Cout/requete (estime) |
|---|---|---|
| System prompt court (150 mots) | ~200 | $0.0006 |
| System prompt long (500 mots) | ~700 | $0.0021 |
| Memoire (10 fichiers contexte) | ~3000 | $0.009 |
| Fichier lu dans le contexte | ~500-5000 | $0.0015-0.015 |
| Reponse courte | ~200 | $0.003 |
| Reponse longue (code) | ~2000 | $0.03 |

### Optimiser les couts

- Gardez le system prompt sous 200 mots (section 4.3).
- Ne chargez pas toute la memoire a chaque requete.
- Pour les fichiers volumineux, demandez a l'agent de lire la partie pertinente, pas le fichier entier.
- Utilisez des scripts bash pour les operations repetitives au lieu de demander a l'agent.

### Suivi mensuel

Tracez vos couts chaque mois :

```
Mars 2026 :
- Requetes : ~850
- Cout total : ~$12
- Cout moyen/requete : ~$0.014
- Plus gros poste : lectures de fichiers longs

Actions : condenser le system prompt, utiliser tasks.sh au lieu 
de demander a l'agent de requeter la DB.
```

## Erreurs courantes

**Ne jamais auditer.** L'agent a des acces que vous avez oublie avoir donne. Un jour ca pose probleme.

**Auditer une fois et oublier.** Les acces changent quand vous ajoutez des services, des fichiers, des integrations. Auditez au moins une fois par trimestre.

**Ignorer les couts.** "C'est pas cher." Jusqu'au mois ou vous faites 3000 requetes avec des fichiers de 5000 tokens chacun. Tracez pour eviter les surprises.

**Faire confiance a l'auto-audit.** L'agent vous dit ce qu'il pense pouvoir faire. Verifiez manuellement ce qu'il peut reellement faire.

## Etapes

1. Lancez le prompt auto-audit ci-dessus.
2. Comparez avec les verifications manuelles (find, psql, ss, env).
3. Identifiez les ecarts entre intention et realite.
4. Corrigez les permissions excessives.
5. Calculez votre cout mensuel moyen.
6. Planifiez un audit trimestriel.

## Verification

- [ ] Un audit complet a ete fait (auto-audit + verification manuelle).
- [ ] Les ecarts intention/realite sont identifies et corriges.
- [ ] Les permissions excessives sont restreintes.
- [ ] Le cout mensuel est connu et trace.
- [ ] Un audit trimestriel est planifie.
