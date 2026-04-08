#!/usr/bin/env node
/**
 * Playbook AI Assistant Proxy
 *
 * Tiny Express server that proxies questions to Claude Haiku via OpenRouter.
 * Designed to run on the VPS behind nginx.
 *
 * Usage:
 *   OPENROUTER_API_KEY=sk-or-... node ask-server.js
 *
 * Or with Vault:
 *   export OPENROUTER_API_KEY=$(docker exec -e VAULT_ADDR=http://127.0.0.1:8200 vault vault kv get -field=api_key secret/openrouter)
 *   node ask-server.js
 *
 * Environment variables:
 *   OPENROUTER_API_KEY  - OpenRouter API key (required)
 *   PORT                - Server port (default: 3008)
 *   ALLOWED_ORIGIN      - CORS origin (default: https://www.openclawfieldplaybook.com)
 */

const http = require('http');
const https = require('https');

const PORT = parseInt(process.env.PORT || '3008', 10);
const API_KEY = process.env.OPENROUTER_API_KEY;
const ALLOWED_ORIGIN = process.env.ALLOWED_ORIGIN || 'https://www.openclawfieldplaybook.com';
const MODEL = 'anthropic/claude-haiku-4-5';

if (!API_KEY) {
  console.error('OPENROUTER_API_KEY is required');
  process.exit(1);
}

const SYSTEM_PROMPT = `Tu es l'assistant du OpenClaw Field Playbook, un guide open-source pour installer et configurer OpenClaw.

Regles:
- Reponds en francais, de maniere concise (3-5 phrases max).
- Base tes reponses UNIQUEMENT sur le contexte fourni (extraits du playbook).
- Cite les pages pertinentes par leur titre exact.
- Si tu ne trouves pas la reponse dans le contexte, dis-le clairement et suggere de creer une issue.
- Ne jamais inventer d'information.
- Ton: professionnel, direct, utile.

Format de reponse (JSON strict):
{
  "answer": "Ta reponse concise ici",
  "pages": [{"title": "Titre de la page", "url": "fichier.html"}],
  "create_issue": false
}

Si tu ne peux pas repondre, renvoie:
{
  "answer": null,
  "pages": [],
  "create_issue": true
}`;

function callOpenRouter(question, context) {
  return new Promise(function(resolve, reject) {
    var contextText = context.map(function(c) {
      return '## ' + c.title + ' (' + c.url + ')\n' + c.body;
    }).join('\n\n');

    var payload = JSON.stringify({
      model: MODEL,
      messages: [
        { role: 'system', content: SYSTEM_PROMPT },
        { role: 'user', content: 'Contexte (extraits du playbook):\n\n' + contextText + '\n\nQuestion du visiteur: ' + question }
      ],
      max_tokens: 500,
      temperature: 0.2,
      response_format: { type: 'json_object' }
    });

    var options = {
      hostname: 'openrouter.ai',
      port: 443,
      path: '/api/v1/chat/completions',
      method: 'POST',
      headers: {
        'Authorization': 'Bearer ' + API_KEY,
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(payload),
        'HTTP-Referer': 'https://www.openclawfieldplaybook.com',
        'X-Title': 'OpenClaw Field Playbook Assistant'
      }
    };

    var req = https.request(options, function(res) {
      var body = '';
      res.on('data', function(chunk) { body += chunk; });
      res.on('end', function() {
        try {
          var data = JSON.parse(body);
          if (data.choices && data.choices[0] && data.choices[0].message) {
            var content = data.choices[0].message.content;
            resolve(JSON.parse(content));
          } else {
            reject(new Error('Unexpected response format'));
          }
        } catch (e) {
          reject(e);
        }
      });
    });

    req.on('error', reject);
    req.setTimeout(10000, function() { req.destroy(); reject(new Error('Timeout')); });
    req.write(payload);
    req.end();
  });
}

// Rate limiting (simple in-memory)
var requestCounts = {};
var RATE_LIMIT = 20; // requests per IP per hour

function isRateLimited(ip) {
  var now = Date.now();
  if (!requestCounts[ip]) {
    requestCounts[ip] = [];
  }
  // Clean old entries
  requestCounts[ip] = requestCounts[ip].filter(function(t) { return now - t < 3600000; });
  if (requestCounts[ip].length >= RATE_LIMIT) {
    return true;
  }
  requestCounts[ip].push(now);
  return false;
}

// Clean rate limit map every hour
setInterval(function() {
  var now = Date.now();
  Object.keys(requestCounts).forEach(function(ip) {
    requestCounts[ip] = requestCounts[ip].filter(function(t) { return now - t < 3600000; });
    if (requestCounts[ip].length === 0) delete requestCounts[ip];
  });
}, 3600000);

var server = http.createServer(function(req, res) {
  // CORS headers
  res.setHeader('Access-Control-Allow-Origin', ALLOWED_ORIGIN);
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.writeHead(204);
    res.end();
    return;
  }

  if (req.method !== 'POST' || req.url !== '/ask') {
    res.writeHead(404, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ error: 'Not found' }));
    return;
  }

  // Rate limit
  var ip = req.headers['x-forwarded-for'] || req.socket.remoteAddress;
  if (isRateLimited(ip)) {
    res.writeHead(429, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ error: 'Too many requests', answer: 'Trop de questions en peu de temps. Reessayez dans quelques minutes.', pages: [], create_issue: false }));
    return;
  }

  var body = '';
  req.on('data', function(chunk) {
    body += chunk;
    if (body.length > 50000) {
      req.destroy();
    }
  });

  req.on('end', function() {
    try {
      var data = JSON.parse(body);
      var question = (data.question || '').trim().substring(0, 500);
      var context = (data.context || []).slice(0, 5);

      if (!question) {
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: 'Question is required' }));
        return;
      }

      callOpenRouter(question, context)
        .then(function(result) {
          res.writeHead(200, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify(result));
        })
        .catch(function(err) {
          console.error('OpenRouter error:', err.message);
          res.writeHead(500, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({
            answer: null,
            pages: context.map(function(c) { return { title: c.title, url: c.url }; }),
            create_issue: true
          }));
        });
    } catch (e) {
      res.writeHead(400, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: 'Invalid JSON' }));
    }
  });
});

server.listen(PORT, '127.0.0.1', function() {
  console.log('Playbook Assistant API listening on 127.0.0.1:' + PORT);
  console.log('Model: ' + MODEL);
  console.log('CORS origin: ' + ALLOWED_ORIGIN);
  console.log('Rate limit: ' + RATE_LIMIT + ' requests/IP/hour');
});
