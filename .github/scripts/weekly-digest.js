const https = require('https');

function request(options, body) {
  return new Promise((resolve, reject) => {
    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => {
        try { resolve(JSON.parse(data)); }
        catch (e) { resolve({}); }
      });
    });
    req.on('error', reject);
    if (body) req.write(body);
    req.end();
  });
}

async function gh(path) {
  const [owner, repoName] = process.env.REPO.split('/');
  return request({
    hostname: 'api.github.com',
    path: `/repos/${owner}/${repoName}${path}`,
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${process.env.GITHUB_TOKEN}`,
      'User-Agent': 'openclawfieldplaybook-digest',
      'Accept': 'application/vnd.github.v3+json'
    }
  }, null);
}

async function main() {
  const since = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString();

  const [newIssues, openPRs, closedIssues, repoInfo] = await Promise.all([
    gh(`/issues?state=open&since=${since}&per_page=20`),
    gh('/pulls?state=open&per_page=10'),
    gh(`/issues?state=closed&since=${since}&per_page=10`),
    gh('')
  ]);

  const newIssueCount = Array.isArray(newIssues) ? newIssues.length : 0;
  const closedCount = Array.isArray(closedIssues) ? closedIssues.length : 0;
  const openPRCount = Array.isArray(openPRs) ? openPRs.length : 0;
  const stars = repoInfo.stargazers_count || 0;

  const issueTitles = Array.isArray(newIssues)
    ? newIssues.slice(0, 5).map((i) => `- ${i.title}`).join('\n')
    : 'none';

  const prTitles = Array.isArray(openPRs)
    ? openPRs.slice(0, 5).map((p) => `- ${p.title}`).join('\n')
    : 'none';

  const summary = `Weekly activity for OpenClaw Field Playbook:
- New issues this week: ${newIssueCount}
- Issues closed: ${closedCount}
- Open PRs: ${openPRCount}
- Total stars: ${stars}

New issue titles:
${issueTitles}

Open PRs:
${prTitles}`;

  const claudeBody = JSON.stringify({
    model: 'claude-sonnet-4-6',
    max_tokens: 400,
    messages: [{
      role: 'user',
      content: `You are the AI assistant for the OpenClaw Field Playbook GitHub project.
Generate a concise weekly digest for the project founder (Alex Willemetz).

Data:
${summary}

Format:
1. One honest opening line about the week
2. Activity summary (3 bullets max)
3. Priority actions for this week (2 max)
4. One closing line

Be direct, concrete, useful. No filler. Max 120 words.`
    }]
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

  console.log('\n=== OPENCLAW FIELD PLAYBOOK — WEEKLY DIGEST ===\n');
  console.log(claudeRes.content[0].text);
  console.log('\n================================================\n');
}

main().catch((err) => {
  console.error('Error:', err.message);
  process.exit(1);
});
