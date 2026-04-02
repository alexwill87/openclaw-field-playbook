---
status: complete
audience: both
chapter: 02
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 2.13 -- Connexion OpenRouter

## Contexte

OpenRouter est une passerelle API qui donne acces a plusieurs modeles IA (Claude, Gemini, Mistral, Llama, etc.) via une seule cle API et un format unifie. Avantage principal : si un modele est indisponible, vous basculez sur un autre sans changer de code.

## Etape 1 : Obtenir la cle API

1. Connectez-vous sur [openrouter.ai](https://openrouter.ai)
2. Allez dans Settings > API Keys
3. Creez une nouvelle cle
4. Copiez la cle (format : `sk-or-v1-...`)

## Etape 2 : Stocker la cle dans Vault

Si ce n'est pas deja fait (section 07) :

```bash
$ docker exec vault vault kv put secret/openrouter api_key="sk-or-v1-VOTRE_CLE_ICI"
```

Verifiez :

```bash
$ docker exec vault vault kv get -field=api_key secret/openrouter
```

## Etape 3 : Tester un appel API

Test rapide avec curl pour verifier que la cle fonctionne :

```bash
$ API_KEY=$(docker exec vault vault kv get -field=api_key secret/openrouter)

$ curl -s https://openrouter.ai/api/v1/chat/completions \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "anthropic/claude-haiku-3.5",
    "messages": [{"role": "user", "content": "Reponds juste OK"}]
  }' | python3 -m json.tool
```

Resultat attendu : une reponse JSON contenant "OK" (ou equivalent) dans `choices[0].message.content`.

## Etape 4 : Verifier le credit

```bash
$ curl -s https://openrouter.ai/api/v1/auth/key \
  -H "Authorization: Bearer $API_KEY" | python3 -m json.tool
```

Ce endpoint retourne votre solde et vos limites.

## Comparaison des modeles disponibles

| Modele | Cas d'usage | Vitesse | Qualite code | Cout relatif |
|--------|-------------|---------|-------------|--------------|
| `anthropic/claude-sonnet-4-20250514` | Taches complexes, raisonnement, code | Moyen | Excellent | $$$ |
| `anthropic/claude-haiku-3.5` | Taches rapides, classification, tri | Rapide | Bon | $ |
| `mistral/mistral-large-latest` | Texte francais, analyse | Moyen | Bon | $$ |
| `google/gemini-2.0-flash-001` | Volume, grande fenetre contexte | Tres rapide | Correct | $ |
| `meta-llama/llama-3.3-70b-instruct` | Open source, pas de filtre | Moyen | Correct | $ |

### Strategie recommandee

- **Modele par defaut** : Claude Sonnet 4 pour la precision
- **Modele fallback** : Claude Haiku 3.5 pour la vitesse et le cout
- **Modele experimentation** : Gemini Flash pour les gros volumes

## Configuration dans OpenClaw

La connexion est configuree dans `~/.openclaw/config.json` (section 12). Le champ `model.provider` doit etre `"openrouter"` et la cle est lue automatiquement depuis Vault.

## Alertes budget

OpenRouter permet de definir des limites de depenses dans le dashboard. Configurez :
- Alerte a 10 EUR/mois
- Limite dure a 30 EUR/mois

Cela evite les mauvaises surprises si un agent boucle.

## Erreurs courantes

- **"Invalid API key"** : La cle est mal copiee ou expiree. Regenerez-la sur openrouter.ai.
- **"Insufficient credits"** : Rechargez votre compte sur openrouter.ai.
- **"Model not found"** : Le nom du modele a change. Verifiez sur openrouter.ai/models le nom exact.
- **Timeout sur les appels** : Certains modeles sont lents en charge. Le fallback (Haiku) prend le relais automatiquement si configure.

## Verification

```bash
$ docker exec vault vault kv get -field=api_key secret/openrouter
$ curl -s https://openrouter.ai/api/v1/auth/key \
  -H "Authorization: Bearer $(docker exec vault vault kv get -field=api_key secret/openrouter)" \
  | python3 -m json.tool
```

Resultats attendus :
- La cle est lisible depuis Vault
- L'API retourne les infos du compte (solde, limites)

## Temps estime

10 minutes.
