const https = require('https');

function request(options, body) {
  return new Promise((resolve, reject) => {
    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => {
        try { resolve(JSON.parse(data)); }
        catch (e) { resolve({ raw: data }); }
      });
    });
    req.on('error', reject);
    if (body) req.write(body);
    req.end();
  });
}

async function main() {
  const isPR = process.env.IS_PR === 'true';
  const title = process.env.ITEM_TITLE || '';
  const body = process.env.ITEM_BODY || '';
  const number = process.env.ITEM_NUMBER;
  const repo = process.env.REPO;
  const [owner, repoName] = repo.split('/');

  const isFrench = /[àâéèêëîïôùûüç]/i.test(body + title);
  const lang = isFrench ? 'French' : 'English';

  const systemPrompt = `You are the AI moderator for the OpenClaw Field Playbook — an open source practitioner's guide for configuring OpenClaw as an AI assistant for entrepreneurs and builders.

Your role: review new Issues and Pull Requests and post a helpful, direct comment.

Rules:
- Max 150 words
- Respond in ${lang} (same language as the contribution)
- Identify the type: suggestion / correction / question / governance / use-case / other
- Suggest the most relevant chapter (0-7) if applicable
- State clearly what the contributor should do next
- Tone: professional, warm, not robotic
- Never use filler like "Great question!" or "Thanks for your amazing contribution!"
- Always end with one concrete next step

This project welcomes entrepreneurs, developers, freelancers, and AI agents as contributors.`;

  const userPrompt = `Review this ${isPR ? 'Pull Request' : 'Issue'}:\n\nTitle: ${title}\n\nBody: ${body}\n\nPost a review comment.`;

  const claudeBody = JSON.stringify({
    model: 'claude-sonnet-4-6',
    max_tokens: 400,
    system: systemPrompt,
    messages: [{ role: 'user', content: userPrompt }]
  });

  const claudeRes = await request({
    hostname: 'api.anthropic.com',
    path: '/v1/messages',
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-api-key': process.env.ANTHROPIC_API_KEY,
      'anthropic-version': '2023-06-01',
      'Content-Length': Buffer.byteLength(claudeBody)
    }
  }, claudeBody);

  if (!claudeRes.content || !claudeRes.content[0]) {
    console.error('Claude API error:', JSON.stringify(claudeRes));
    process.exit(1);
  }

  const review = claudeRes.content[0].text;
  const comment = `${review}\n\n---\n*AI moderator — [OpenClaw Field Playbook](https://github.com/${owner}/${repoName})*`;

  const ghBody = JSON.stringify({ body: comment });

  await request({
    hostname: 'api.github.com',
    path: `/repos/${owner}/${repoName}/issues/${number}/comments`,
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${process.env.GITHUB_TOKEN}`,
      'User-Agent': 'openclawfieldplaybook-bot',
      'Content-Length': Buffer.byteLength(ghBody)
    }
  }, ghBody);

  console.log('Review posted successfully.');
}

main().catch((err) => {
  console.error('Error:', err.message);
  process.exit(1);
});
