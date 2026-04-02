#!/usr/bin/env python3
"""
Build script for OpenClaw Field Playbook -- multi-page static site.

Generates:
  - index.html        (landing page)
  - chapitre-00.html  through  chapitre-07.html
  - checklist.html

All output files are written to the repo root for GitHub Pages.
"""

import os
import markdown

REPO_ROOT = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
)
SECTIONS_DIR = os.path.join(REPO_ROOT, 'sections')
TEMPLATE_PATH = os.path.join(REPO_ROOT, 'index_template.html')

GITHUB_URL = 'https://github.com/alexwill87/openclaw-field-playbook'

# Ordered chapter definitions: (folder_or_file, slug, short_title, description)
CHAPTERS = [
    ('00-reading-guide.md', 'chapitre-00', 'Chapitre 0 -- Guide de lecture',
     'Comment lire ce guide et par ou commencer'),
    ('01-definition', 'chapitre-01', 'Chapitre 1 -- Definition',
     'Ce qu\'est OpenClaw, ce que ce n\'est pas'),
    ('02-installation', 'chapitre-02', 'Chapitre 2 -- Installation',
     'Installer OpenClaw de zero sur un VPS'),
    ('03-configuration', 'chapitre-03', 'Chapitre 3 -- Configuration',
     'Configurer l\'agent pour son contexte'),
    ('04-personalisation', 'chapitre-04', 'Chapitre 4 -- Personnalisation',
     'Adapter le comportement, le ton, les workflows'),
    ('05-maintenance', 'chapitre-05', 'Chapitre 5 -- Maintenance',
     'Garder l\'agent fiable dans le temps'),
    ('06-use-cases', 'chapitre-06', 'Chapitre 6 -- Cas d\'usage',
     'Exemples concrets par type d\'organisation'),
    ('07-localisation', 'chapitre-07', 'Chapitre 7 -- Localisation',
     'Adapter OpenClaw a d\'autres langues et contextes'),
]

MD_EXTENSIONS = ['tables', 'fenced_code', 'codehilite', 'toc']


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def strip_frontmatter(text):
    """Remove YAML front matter from markdown content."""
    if text.startswith('---'):
        end = text.find('---', 3)
        if end != -1:
            return text[end + 3:].strip()
    return text


def read_template():
    """Read the HTML template."""
    with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        return f.read()


def get_chapter_md_files(entry):
    """Return ordered list of .md file paths for a chapter entry."""
    path = os.path.join(SECTIONS_DIR, entry)

    # Single file (chapter 00)
    if os.path.isfile(path):
        return [path]

    # Directory -- README first, then alphabetical
    if os.path.isdir(path):
        readme = os.path.join(path, 'README.md')
        others = sorted([
            os.path.join(path, f)
            for f in os.listdir(path)
            if f.endswith('.md') and f != 'README.md'
        ])
        files = []
        if os.path.exists(readme):
            files.append(readme)
        files.extend(others)
        return files

    return []


def concatenate_chapter_md(entry):
    """Read and concatenate all markdown for a chapter, stripped of frontmatter."""
    parts = []
    for filepath in get_chapter_md_files(entry):
        with open(filepath, 'r', encoding='utf-8') as f:
            raw = f.read()
        parts.append(strip_frontmatter(raw))
    return '\n\n'.join(parts)


def build_sidebar(active_slug):
    """Build sidebar navigation HTML with the active chapter highlighted."""
    items = []
    items.append(
        '<a href="index.html"{}>Accueil</a>'.format(
            ' class="active"' if active_slug == 'index' else ''
        )
    )
    for _, slug, title, _ in CHAPTERS:
        active = ' class="active"' if slug == active_slug else ''
        items.append(
            '<a href="{}.html"{}>{}</a>'.format(slug, active, title)
        )
    items.append(
        '<a href="checklist.html"{}>Checklist</a>'.format(
            ' class="active"' if active_slug == 'checklist' else ''
        )
    )
    items.append(
        '<a href="decouverte.html"{}>C\'est quoi OpenClaw ?</a>'.format(
            ' class="active"' if active_slug == 'decouverte' else ''
        )
    )
    items.append(
        '<a href="contribuer.html"{}>Contribuer</a>'.format(
            ' class="active"' if active_slug == 'contribuer' else ''
        )
    )
    return '\n'.join(items)


def render_page(title, content_html, active_slug):
    """Inject content into the template and return final HTML."""
    template = read_template()
    html = template.replace('<!-- TITLE_PLACEHOLDER -->', title)
    html = html.replace('<!-- NAVIGATION_PLACEHOLDER -->', build_sidebar(active_slug))
    html = html.replace('<!-- CONTENT_PLACEHOLDER -->', content_html)
    return html


def write_page(filename, html):
    """Write an HTML file to the repo root."""
    path = os.path.join(REPO_ROOT, filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'  -> {filename}')


# ---------------------------------------------------------------------------
# Page builders
# ---------------------------------------------------------------------------

def build_chapter_pages():
    """Build one HTML page per chapter."""
    for entry, slug, title, _ in CHAPTERS:
        md_content = concatenate_chapter_md(entry)
        html_content = markdown.markdown(md_content, extensions=MD_EXTENSIONS)

        # Wrap in chapter div
        wrapped = '<section class="chapter">\n{}\n</section>'.format(html_content)

        # Determine prev / next
        idx = [c[1] for c in CHAPTERS].index(slug)
        nav_links = ['<hr>', '<div style="display:flex;justify-content:space-between;padding:1rem 0;font-size:0.9rem;">']
        if idx > 0:
            prev_slug = CHAPTERS[idx - 1][1]
            prev_title = CHAPTERS[idx - 1][2]
            nav_links.append(
                '<a href="{}.html">&larr; {}</a>'.format(prev_slug, prev_title)
            )
        else:
            nav_links.append('<span></span>')
        if idx < len(CHAPTERS) - 1:
            next_slug = CHAPTERS[idx + 1][1]
            next_title = CHAPTERS[idx + 1][2]
            nav_links.append(
                '<a href="{}.html">{} &rarr;</a>'.format(next_slug, next_title)
            )
        else:
            nav_links.append('<span></span>')
        nav_links.append('</div>')

        # Lien "Editer sur GitHub" pour les chapitres avec dossier
        edit_link = ''
        chapter_dir = entry
        if os.path.isdir(os.path.join(SECTIONS_DIR, entry)):
            edit_url = '{}/tree/main/sections/{}/'.format(GITHUB_URL, chapter_dir)
            edit_link = '\n<p class="edit-link"><a href="{}">Proposer une modification sur GitHub</a></p>'.format(edit_url)

        # Giscus comments
        giscus = """
<div class="giscus-wrapper">
  <h3 style="font-size:1rem;margin-bottom:1rem;">Commentaires et discussions</h3>
  <script src="https://giscus.app/client.js"
    data-repo="alexwill87/openclaw-field-playbook"
    data-repo-id="R_kgDORvZ2yQ"
    data-category="General"
    data-category-id="DIC_kwDORvZ2yc4C54bl"
    data-mapping="pathname"
    data-strict="0"
    data-reactions-enabled="1"
    data-emit-metadata="0"
    data-input-position="top"
    data-theme="preferred_color_scheme"
    data-lang="fr"
    data-loading="lazy"
    crossorigin="anonymous"
    async>
  </script>
</div>"""

        full_content = wrapped + edit_link + giscus + '\n' + '\n'.join(nav_links)
        page_html = render_page(title, full_content, slug)
        write_page(f'{slug}.html', page_html)


def build_index_page():
    """Build the landing page (index.html)."""
    # Build chapter cards
    cards = []
    for _, slug, title, desc in CHAPTERS:
        cards.append(
            '<a class="chapter-card" href="{slug}.html">'
            '<div class="num">{title}</div>'
            '<div class="card-desc">{desc}</div>'
            '</a>'.format(slug=slug, title=title, desc=desc)
        )

    content = """
<div class="landing-hero">
  <h1>OpenClaw Field Playbook</h1>
  <p class="lead">Le guide de terrain pour installer et operer OpenClaw en entreprise.<br>
  Ecrit par des praticiens. Teste sur le terrain. Open source.</p>
  <p style="font-size:0.88rem;color:var(--text-muted);max-width:540px;margin:0 auto 1.5rem;">
    Ne de 3 installations ratees et 5 mois de travail. 81 sections, 7 chapitres,
    des commandes copiables et des decisions documentees.
  </p>
  <div class="hero-actions">
    <a href="chapitre-00.html" class="btn-primary">Commencer la lecture</a>
    <a href="decouverte.html" class="btn-secondary">C'est quoi OpenClaw ?</a>
    <a href="{github}" class="btn-secondary" target="_blank">Voir sur GitHub</a>
  </div>
</div>

<div class="landing-section">
  <h2>A qui s'adresse ce guide</h2>
  <div class="audience-grid">
    <div class="audience-card">
      <strong>Entrepreneurs</strong>
      <p>Vous voulez un agent IA qui travaille pour votre business, pas juste un chatbot.</p>
    </div>
    <div class="audience-card">
      <strong>Equipes techniques</strong>
      <p>Vous deployer OpenClaw pour votre organisation et avez besoin d'un guide solide.</p>
    </div>
    <div class="audience-card">
      <strong>Freelances</strong>
      <p>Vous cherchez un avantage competitif en automatisant vos operations.</p>
    </div>
    <div class="audience-card">
      <strong>Agents IA</strong>
      <p>Vous bootstrappez votre propre installation en suivant les sections comme un runbook.</p>
    </div>
  </div>
</div>

<div class="landing-section">
  <h2>Par ou commencer</h2>
  <p>Trois parcours selon votre profil :</p>
  <ul class="path-list">
    <li>
      <strong>Je decouvre OpenClaw</strong>
      <span><a href="chapitre-01.html">Definition</a> &rarr; <a href="chapitre-02.html">Installation</a> &rarr; <a href="chapitre-03.html">Configuration</a>. Comptez une journee.</span>
    </li>
    <li>
      <strong>J'ai deja installe, je veux configurer</strong>
      <span><a href="chapitre-03.html">Configuration</a> &rarr; <a href="chapitre-04.html">Personnalisation</a>. Les deux chapitres les plus denses.</span>
    </li>
    <li>
      <strong>Je veux des exemples concrets</strong>
      <span><a href="chapitre-06.html">Cas d'usage</a> d'abord, puis remontez vers les chapitres techniques selon vos besoins.</span>
    </li>
  </ul>
</div>

<div class="landing-section">
  <h2>Les chapitres</h2>
  <div class="chapter-grid">
    {cards}
  </div>
</div>

<div class="landing-section">
  <h2>Outils</h2>
  <div class="audience-grid">
    <a class="audience-card" href="checklist.html" style="text-decoration:none;color:var(--text);">
      <strong>Checklist interactive</strong>
      <p>Suivez votre progression etape par etape. Sauvegarde automatique.</p>
    </a>
    <a class="audience-card" href="contribuer.html" style="text-decoration:none;color:var(--text);">
      <strong>Contribuer</strong>
      <p>Corrigez une erreur, ajoutez un cas d'usage, proposez une section.</p>
    </a>
    <a class="audience-card" href="decouverte.html" style="text-decoration:none;color:var(--text);">
      <strong>C'est quoi OpenClaw ?</strong>
      <p>Pour ceux qui partent de zero. Pas de jargon.</p>
    </a>
    <a class="audience-card" href="{github}/issues" style="text-decoration:none;color:var(--text);" target="_blank">
      <strong>Signaler un probleme</strong>
      <p>Une commande qui ne marche pas ? Un lien casse ? Dites-le nous.</p>
    </a>
  </div>
</div>
""".format(github=GITHUB_URL, cards='\n    '.join(cards))

    page_html = render_page('Accueil', content, 'index')
    write_page('index.html', page_html)


def build_checklist_page():
    """Build the interactive checklist page (checklist.html)."""
    checklist_data = {
        'Chapitre 2 -- Installation': [
            'VPS commande et accessible en SSH',
            'Utilisateur non-root cree avec sudo',
            'Pare-feu configure (UFW / iptables)',
            'SSH securise (cle uniquement, port change)',
            'Fail2ban installe et actif',
            'Tailscale installe et connecte',
            'Docker et Docker Compose installes',
            'Node.js et PM2 installes',
            'Structure de dossiers creee',
            'Vault configure et secrets stockes',
            'PostgreSQL installe et base creee',
            'Health check endpoint fonctionnel',
            'OpenClaw installe et demarre',
            'Compte OpenRouter cree et cle API configuree',
            'Bot Telegram cree et connecte',
            'Gateway systemd configuree et active',
            'Repository Git initialise',
            'CLAUDE.md cree a la racine',
            'Script de deploiement en place',
        ],
        'Chapitre 3 -- Configuration': [
            'Perimetre de l\'agent defini',
            'SOUL.md redige',
            'USER.md redige',
            'AGENTS.md redige (si multi-agents)',
            'CONSTITUTION.md redigee',
            'Trois zones memoire configurees',
            'MEMORY.md initialise',
            'Knowledge base alimentee',
            'Principe une-source-de-verite applique',
            'Calendrier et taches connectes',
            'Briefing du matin configure',
            'Crons planifies',
        ],
        'Chapitre 4 -- Personnalisation': [
            'System prompt redige et teste',
            'Personnalite et ton definis',
            'Taches recurrentes configurees',
            'Workflows documentes dans workflows.md',
            'Boundary prompt en place',
            'Audit des acces realise',
            'Rythme hebdomadaire etabli',
            'Configuration bilingue si necessaire',
        ],
        'Chapitre 5 -- Maintenance': [
            'Health check automatise',
            'Logs centralises et consultables',
            'Backups automatises et testes',
            'Monitoring en place (alertes)',
            'Procedure en cas de panne documentee',
        ],
    }

    # Build checklist HTML
    items_html = []
    item_index = 0
    for section_title, items in checklist_data.items():
        items_html.append('<h3>{}</h3>'.format(section_title))
        for item in items:
            items_html.append(
                '<label class="checklist-item">'
                '<input type="checkbox" data-index="{idx}" onchange="saveChecklist()">'
                '<span>{text}</span>'
                '</label>'.format(idx=item_index, text=item)
            )
            item_index += 1

    total_items = item_index

    content = """
<section class="chapter">
<h1>Checklist de progression</h1>
<p>Cochez les etapes au fur et a mesure de votre avancement. Votre progression est sauvegardee automatiquement dans votre navigateur.</p>
<p style="margin-bottom:1.5rem;">
  <strong>Progression :</strong> <span id="progress-count">0</span> / {total} etapes
  <span id="progress-bar" style="display:inline-block;width:200px;height:8px;background:var(--border);border-radius:4px;margin-left:0.5rem;vertical-align:middle;">
    <span id="progress-fill" style="display:block;height:100%;background:var(--accent);border-radius:4px;width:0%;transition:width 0.3s;"></span>
  </span>
</p>
<div style="margin-bottom:1.5rem;">
  <button onclick="exportChecklist()" style="padding:0.5rem 1rem;border:1px solid var(--border);border-radius:6px;background:var(--bg);cursor:pointer;font-size:0.85rem;">Exporter en texte</button>
  <button onclick="resetChecklist()" style="padding:0.5rem 1rem;border:1px solid var(--border);border-radius:6px;background:var(--bg);cursor:pointer;font-size:0.85rem;margin-left:0.5rem;">Reinitialiser</button>
</div>

{items}

</section>

<style>
.checklist-item {{
  display: flex;
  align-items: flex-start;
  gap: 0.6rem;
  padding: 0.4rem 0;
  font-size: 0.92rem;
  cursor: pointer;
}}
.checklist-item input[type="checkbox"] {{
  margin-top: 0.25rem;
  width: 1rem;
  height: 1rem;
  cursor: pointer;
  flex-shrink: 0;
}}
.checklist-item input[type="checkbox"]:checked + span {{
  text-decoration: line-through;
  color: var(--text-muted);
}}
</style>

<script>
var STORAGE_KEY = 'openclaw-checklist';
var TOTAL_ITEMS = {total};

function loadChecklist() {{
  var saved = localStorage.getItem(STORAGE_KEY);
  if (!saved) return;
  try {{
    var data = JSON.parse(saved);
    var boxes = document.querySelectorAll('.checklist-item input[type="checkbox"]');
    boxes.forEach(function(box) {{
      var idx = parseInt(box.getAttribute('data-index'));
      if (data[idx]) box.checked = true;
    }});
    updateProgress();
  }} catch(e) {{}}
}}

function saveChecklist() {{
  var boxes = document.querySelectorAll('.checklist-item input[type="checkbox"]');
  var data = {{}};
  boxes.forEach(function(box) {{
    var idx = parseInt(box.getAttribute('data-index'));
    if (box.checked) data[idx] = true;
  }});
  localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
  updateProgress();
}}

function updateProgress() {{
  var boxes = document.querySelectorAll('.checklist-item input[type="checkbox"]');
  var checked = 0;
  boxes.forEach(function(box) {{ if (box.checked) checked++; }});
  document.getElementById('progress-count').textContent = checked;
  var pct = Math.round((checked / TOTAL_ITEMS) * 100);
  document.getElementById('progress-fill').style.width = pct + '%';
}}

function resetChecklist() {{
  if (!confirm('Reinitialiser toute la checklist ?')) return;
  localStorage.removeItem(STORAGE_KEY);
  var boxes = document.querySelectorAll('.checklist-item input[type="checkbox"]');
  boxes.forEach(function(box) {{ box.checked = false; }});
  updateProgress();
}}

function exportChecklist() {{
  var boxes = document.querySelectorAll('.checklist-item input[type="checkbox"]');
  var lines = ['OpenClaw Field Playbook -- Checklist de progression', ''];
  var currentHeading = '';
  var container = document.querySelector('.chapter');
  var elements = container.querySelectorAll('h3, .checklist-item');
  elements.forEach(function(el) {{
    if (el.tagName === 'H3') {{
      if (currentHeading) lines.push('');
      currentHeading = el.textContent;
      lines.push(currentHeading);
      lines.push('-'.repeat(currentHeading.length));
    }} else {{
      var box = el.querySelector('input[type="checkbox"]');
      var text = el.querySelector('span').textContent;
      var status = box.checked ? '[x]' : '[ ]';
      lines.push(status + ' ' + text);
    }}
  }});

  var blob = new Blob([lines.join('\\n')], {{ type: 'text/plain' }});
  var url = URL.createObjectURL(blob);
  var a = document.createElement('a');
  a.href = url;
  a.download = 'openclaw-checklist.txt';
  a.click();
  URL.revokeObjectURL(url);
}}

document.addEventListener('DOMContentLoaded', loadChecklist);
</script>
""".format(items='\n'.join(items_html), total=total_items)

    page_html = render_page('Checklist', content, 'checklist')
    write_page('checklist.html', page_html)


def build_contribuer_page():
    """Build the contribuer.html page."""
    content = """
<section class="chapter">
<h1>Contribuer au playbook</h1>
<p>Ce playbook est un projet open-source. Toute contribution est bienvenue, a condition de respecter les niveaux de gouvernance decrits ci-dessous.</p>

<h2>Trois niveaux de contribution</h2>

<h3>T3 -- Corrections</h3>
<p>Typos, liens casses, exemples a clarifier, reformulations mineures. Vous pouvez soumettre une Pull Request directement ou ouvrir une Issue. Ces contributions sont mergees rapidement.</p>

<h3>T2 -- Sections</h3>
<p>Nouveau contenu, reecritures de sections existantes, ajout de cas d'usage. Ouvrez d'abord une Issue pour decrire votre proposition. Une fois validee par le maintainer, soumettez une Pull Request.</p>

<h3>T1 -- Structure</h3>
<p>Modifier l'organisation des chapitres, ajouter ou supprimer un chapitre, changer l'architecture du playbook. Ces modifications requierent une Issue etiquetee <code>governance</code> et une decision du fondateur. Ne soumettez pas de PR sans validation prealable.</p>

<h2>Comment soumettre une correction</h2>
<ol>
  <li><strong>Fork</strong> le repository sur GitHub</li>
  <li><strong>Editez</strong> le fichier concerne dans le dossier <code>sections/</code> (jamais <code>PLAYBOOK.md</code> directement)</li>
  <li><strong>Creez une Pull Request</strong> avec une description claire de votre modification</li>
  <li><strong>Attendez la review</strong> du maintainer</li>
</ol>

<h2>Format d'une section</h2>
<p>Chaque section du playbook suit un format standard :</p>
<pre><code>---
status: draft | review | complete
audience: human | agent | both
chapter: XX
last_updated: YYYY-MM-DD
contributors: [nom]
---

## Contexte
Pourquoi cette section existe, quel probleme elle resout.

## Etapes
Les actions concretes, dans l'ordre.

## Erreurs courantes
Ce qui peut mal tourner et comment l'eviter.

## Template
Fichiers ou configurations a copier-coller.

## Verification
Comment savoir que tout fonctionne.
</code></pre>

<h2>Qui maintient ce projet</h2>
<p>Ce playbook est maintenu par <strong>Alex Willemetz</strong>, Paris. Fondateur du projet OpenClaw Field Playbook.</p>
<p>Profil GitHub : <a href="https://github.com/alexwill87">github.com/alexwill87</a></p>

<h2>Documentation complete</h2>
<p>Pour plus de details, consultez le fichier <a href="{github}/blob/main/CONTRIBUTING.md">CONTRIBUTING.md</a> sur GitHub.</p>

</section>
""".format(github=GITHUB_URL)

    page_html = render_page('Contribuer', content, 'contribuer')
    write_page('contribuer.html', page_html)


def build_decouverte_page():
    """Build the decouverte.html page."""
    content = """
<section class="chapter">
<h1>C'est quoi OpenClaw ?</h1>
<p>Cette page est pour ceux qui ne connaissent rien a OpenClaw. Pas de jargon, pas de prerequis techniques. Juste l'essentiel pour comprendre de quoi on parle.</p>

<h2>En une phrase</h2>
<p>OpenClaw est un outil qui permet de creer des assistants IA qui travaillent pour vous -- pas juste repondre a des questions, mais agir, surveiller, organiser.</p>

<h2>A quoi ca sert concretement</h2>
<p>Voici cinq exemples simples de ce qu'un agent OpenClaw peut faire pour vous :</p>
<ul>
  <li><strong>Briefing du matin</strong> -- Chaque matin, votre agent vous envoie un resume de ce qui s'est passe pendant la nuit : emails importants, alertes, taches du jour.</li>
  <li><strong>Triage email</strong> -- L'agent lit vos emails, les classe par priorite, et vous signale ceux qui demandent une reponse urgente.</li>
  <li><strong>Suivi clients</strong> -- Il surveille les messages de vos clients et vous alerte quand quelqu'un attend une reponse depuis trop longtemps.</li>
  <li><strong>Surveillance serveur</strong> -- Il verifie que vos services tournent correctement et vous previent avant qu'un probleme ne devienne critique.</li>
  <li><strong>Documentation automatique</strong> -- Il prend en note ce qui se passe dans votre projet et tient votre documentation a jour sans effort.</li>
</ul>

<h2>De quoi a-t-on besoin</h2>
<ul>
  <li>Un serveur (VPS) -- un ordinateur distant que vous louez</li>
  <li>Une connexion internet</li>
  <li>Une cle API pour un modele IA (OpenRouter, Anthropic, ou autre)</li>
  <li>2 a 3 heures de configuration initiale</li>
</ul>
<p><strong>Budget :</strong> entre 20 et 40 EUR par mois pour le serveur et les appels API.</p>

<h2>C'est quoi un VPS ?</h2>
<p>Un VPS, c'est un ordinateur dans un datacenter que vous louez. Vous y accedez a distance, depuis votre ordinateur ou votre telephone. C'est comme un bureau virtuel toujours allume, toujours connecte. Votre agent OpenClaw vit dessus et travaille 24h/24.</p>

<h2>Pourquoi pas juste ChatGPT ?</h2>
<table>
  <thead>
    <tr><th>ChatGPT</th><th>OpenClaw</th></tr>
  </thead>
  <tbody>
    <tr><td>Attend vos questions</td><td>Agit de lui-meme selon vos regles</td></tr>
    <tr><td>Oublie tout entre les conversations</td><td>A une memoire persistante</td></tr>
    <tr><td>Vit chez OpenAI</td><td>Vit chez vous, sur votre serveur</td></tr>
  </tbody>
</table>

<h2>Pret a commencer ?</h2>
<p>Si tout cela vous parle, voici les prochaines etapes :</p>
<ul>
  <li><a href="chapitre-01.html">Chapitre 1 -- Definition</a> : comprendre en detail ce qu'est OpenClaw et ce que ce n'est pas</li>
  <li><a href="chapitre-02.html">Chapitre 2 -- Installation</a> : installer OpenClaw de zero sur un serveur</li>
</ul>

<h2>Liens utiles</h2>
<ul>
  <li><a href="https://github.com/open-claw" target="_blank">Documentation officielle OpenClaw</a></li>
  <li><a href="https://github.com/alexwill87/openclaw-field-playbook" target="_blank">Ce playbook sur GitHub</a></li>
  <li>Livre de Dennis Steinberg sur OpenClaw (reference communautaire)</li>
</ul>

</section>
"""

    page_html = render_page('C\'est quoi OpenClaw ?', content, 'decouverte')
    write_page('decouverte.html', page_html)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    print('OpenClaw Field Playbook -- build multi-page site')
    print('=' * 50)

    build_index_page()
    build_chapter_pages()
    build_checklist_page()
    build_contribuer_page()
    build_decouverte_page()

    print('=' * 50)
    print('Build complete. All files written to repo root.')
