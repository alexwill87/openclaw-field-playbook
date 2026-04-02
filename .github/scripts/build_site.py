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

        full_content = wrapped + '\n' + '\n'.join(nav_links)
        page_html = render_page(title, full_content, slug)
        write_page(f'{slug}.html', page_html)


def build_index_page():
    """Build the landing page (index.html)."""
    content = """
<header id="hero">
  <h1>OpenClaw Field Playbook</h1>
  <p class="tagline">Le guide de terrain pour installer et operer OpenClaw en entreprise</p>
  <p>Ce guide est ne de 3 installations ratees et 5 mois de travail. Chaque section est ecrite par des praticiens qui ont fait les erreurs avant vous. Pas de theorie abstraite : des commandes, des fichiers, des decisions documentees.</p>
  <div style="margin-top:1.5rem;display:flex;gap:1rem;flex-wrap:wrap;">
    <a href="chapitre-00.html" style="display:inline-block;padding:0.6rem 1.2rem;background:var(--accent);color:#fff;border-radius:6px;text-decoration:none;font-weight:600;font-size:0.9rem;">Commencer la lecture</a>
    <a href="{github}" style="display:inline-block;padding:0.6rem 1.2rem;border:1px solid var(--border);border-radius:6px;text-decoration:none;color:var(--text);font-size:0.9rem;">GitHub</a>
  </div>
</header>

<section class="chapter">
<h2>A qui s'adresse ce guide</h2>
<ul>
  <li><strong>Entrepreneurs</strong> qui veulent un agent IA operationnel</li>
  <li><strong>Equipes techniques</strong> qui deploient OpenClaw pour leur organisation</li>
  <li><strong>Freelances</strong> qui cherchent un avantage competitif</li>
  <li><strong>Agents IA</strong> qui bootstrappent leur propre installation</li>
</ul>
</section>

<section class="chapter">
<h2>Par ou commencer</h2>
<p>Trois parcours selon votre profil :</p>

<h3>Je decouvre</h3>
<p><a href="chapitre-01.html">Chapitre 1 -- Definition</a> &rarr; <a href="chapitre-02.html">Chapitre 2 -- Installation</a> &rarr; <a href="chapitre-03.html">Chapitre 3 -- Configuration</a></p>

<h3>J'ai deja installe, je veux configurer</h3>
<p><a href="chapitre-03.html">Chapitre 3 -- Configuration</a> &rarr; <a href="chapitre-04.html">Chapitre 4 -- Personnalisation</a></p>

<h3>Je veux des exemples concrets</h3>
<p><a href="chapitre-06.html">Chapitre 6 -- Cas d'usage</a> &rarr; puis remonter vers les chapitres techniques selon vos besoins</p>
</section>

<section class="chapter">
<h2>Les 8 chapitres</h2>
<table>
  <thead>
    <tr><th>N.</th><th>Titre</th><th>Description</th></tr>
  </thead>
  <tbody>
""".format(github=GITHUB_URL)

    for _, slug, title, desc in CHAPTERS:
        content += '    <tr><td><a href="{slug}.html">{title}</a></td><td>{title}</td><td>{desc}</td></tr>\n'.format(
            slug=slug, title=title, desc=desc
        )

    content += """  </tbody>
</table>
</section>

<section class="chapter">
<h2>Checklist</h2>
<p><a href="checklist.html">Telechargez la checklist complete</a> pour suivre votre progression etape par etape a travers le playbook.</p>
</section>
"""
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


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    print('OpenClaw Field Playbook -- build multi-page site')
    print('=' * 50)

    build_index_page()
    build_chapter_pages()
    build_checklist_page()

    print('=' * 50)
    print('Build complete. All files written to repo root.')
