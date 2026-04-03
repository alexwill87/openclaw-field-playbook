#!/usr/bin/env python3
"""
Build script for OpenClaw Field Playbook -- multi-page static site (v2).

One HTML page per SECTION (not per chapter).

Generates:
  - index.html          (landing page)
  - 00-guide.html       (chapter 0)
  - XX-00-sommaire.html (chapter summary pages)
  - XX-NN-slug.html     (individual section pages)
  - checklist.html
  - contribuer.html
  - decouverte.html

All output files are written to the repo root for GitHub Pages.
"""

import os
import re
import json
import markdown

REPO_ROOT = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
)
SECTIONS_DIR = os.path.join(REPO_ROOT, 'sections')
TEMPLATE_PATH = os.path.join(REPO_ROOT, 'index_template.html')

GITHUB_URL = 'https://github.com/alexwill87/openclaw-field-playbook'
GISCUS_REPO_ID = 'R_kgDORvZ2yQ'
GISCUS_CATEGORY_ID = 'DIC_kwDORvZ2yc4C54bl'

# Ordered chapter definitions: (folder_or_file, chapter_num, short_title, description)
CHAPTERS = [
    ('00-reading-guide.md', '00', 'Guide de lecture',
     'Comment lire ce guide et par ou commencer'),
    ('01-definition', '01', 'Definition',
     'Ce qu\'est OpenClaw, ce que ce n\'est pas'),
    ('02-installation', '02', 'Installation',
     'Installer OpenClaw de zero sur un VPS'),
    ('03-configuration', '03', 'Configuration',
     'Configurer l\'agent pour son contexte'),
    ('04-personalisation', '04', 'Personnalisation',
     'Adapter le comportement, le ton, les workflows'),
    ('05-maintenance', '05', 'Maintenance',
     'Garder l\'agent fiable dans le temps'),
    ('06-use-cases', '06', 'Cas d\'usage',
     'Exemples concrets par type d\'organisation'),
    ('07-localisation', '07', 'Localisation',
     'Adapter OpenClaw a d\'autres langues et contextes'),
]

MD_EXTENSIONS = ['tables', 'fenced_code', 'codehilite', 'toc']

MONTH_NAMES_FR = {
    '01': 'janvier', '02': 'fevrier', '03': 'mars', '04': 'avril',
    '05': 'mai', '06': 'juin', '07': 'juillet', '08': 'aout',
    '09': 'septembre', '10': 'octobre', '11': 'novembre', '12': 'decembre',
}


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


def parse_frontmatter(text):
    """Parse YAML front matter and return (metadata_dict, content_without_frontmatter).

    Returns a tuple (dict, str). If no frontmatter is found, returns ({}, text).
    """
    if text.startswith('---'):
        end = text.find('---', 3)
        if end != -1:
            fm_block = text[3:end].strip()
            meta = {}
            for line in fm_block.split('\n'):
                line = line.strip()
                if ':' in line:
                    key, _, value = line.partition(':')
                    meta[key.strip()] = value.strip()
            return meta, text[end + 3:].strip()
    return {}, text


def format_last_updated(value):
    """Format a last_updated value like '2026-04' into 'avril 2026'."""
    if not value:
        return None
    value = str(value).strip()
    match = re.match(r'^(\d{4})-(\d{2})$', value)
    if match:
        year, month = match.group(1), match.group(2)
        month_name = MONTH_NAMES_FR.get(month, month)
        return f'{month_name} {year}'
    # Fallback: return as-is
    return value


def rewrite_md_links(html, section_map):
    """Rewrite .md links to .html links using the section filename mapping.

    section_map: dict mapping source .md filename to output .html filename
    e.g. {'01-prerequis.md': '02-01-prerequis.html', 'README.md': '02-00-sommaire.html'}
    """
    import re
    def replacer(match):
        prefix = match.group(1)  # href=" or src="
        md_file = match.group(2)  # e.g. 01-prerequis.md
        suffix = match.group(3)  # closing quote
        # Try direct match
        if md_file in section_map:
            return f'{prefix}{section_map[md_file]}{suffix}'
        # Try without path components (e.g. ../../tools/install-tracker/README.md)
        basename = os.path.basename(md_file)
        if basename in section_map:
            return f'{prefix}{section_map[basename]}{suffix}'
        # Leave as-is if no match (external links, anchors, etc.)
        return match.group(0)

    return re.sub(r'(href=")([^"]*\.md)(")', replacer, html)


def read_template():
    """Read the HTML template."""
    with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        return f.read()


def extract_h1(md_text):
    """Extract the first H1 title from markdown content (after frontmatter)."""
    clean = strip_frontmatter(md_text)
    for line in clean.split('\n'):
        line = line.strip()
        if line.startswith('# '):
            return line[2:].strip()
    return 'Sans titre'


def truncate(text, max_len=35):
    """Truncate text to max_len characters, adding ... if needed."""
    if len(text) <= max_len:
        return text
    return text[:max_len - 3].rstrip() + '...'


# ---------------------------------------------------------------------------
# Section registry -- build the ordered list of all pages
# ---------------------------------------------------------------------------

class Section:
    """Represents one page of the site."""
    def __init__(self, slug, html_file, title, sidebar_title, chapter_num,
                 is_sommaire, md_path, github_edit_path):
        self.slug = slug
        self.html_file = html_file
        self.title = title                # full H1 title
        self.sidebar_title = sidebar_title  # truncated for sidebar
        self.chapter_num = chapter_num    # '00', '01', etc.
        self.is_sommaire = is_sommaire    # True for README / chapter 0
        self.md_path = md_path            # absolute path to .md file
        self.github_edit_path = github_edit_path  # relative path for edit link


def build_section_registry():
    """Scan sections/ and build an ordered list of Section objects."""
    all_sections = []

    for entry, chapter_num, short_title, description in CHAPTERS:
        path = os.path.join(SECTIONS_DIR, entry)

        # Chapter 0 -- single file
        if os.path.isfile(path):
            with open(path, 'r', encoding='utf-8') as f:
                raw = f.read()
            h1 = extract_h1(raw)
            slug = '00-guide'
            sec = Section(
                slug=slug,
                html_file=f'{slug}.html',
                title=h1,
                sidebar_title=f'0. {short_title}',
                chapter_num=chapter_num,
                is_sommaire=True,
                md_path=path,
                github_edit_path=f'sections/{entry}',
            )
            all_sections.append(sec)
            continue

        # Multi-section chapter -- README first, then numbered files
        if os.path.isdir(path):
            readme = os.path.join(path, 'README.md')
            if os.path.exists(readme):
                with open(readme, 'r', encoding='utf-8') as f:
                    raw = f.read()
                h1 = extract_h1(raw)
                slug = f'{chapter_num}-00-sommaire'
                sec = Section(
                    slug=slug,
                    html_file=f'{slug}.html',
                    title=h1,
                    sidebar_title=f'{int(chapter_num)}. {short_title}',
                    chapter_num=chapter_num,
                    is_sommaire=True,
                    md_path=readme,
                    github_edit_path=f'sections/{entry}/README.md',
                )
                all_sections.append(sec)

            # Sub-sections (sorted alphabetically = numerically)
            sub_files = sorted([
                f for f in os.listdir(path)
                if f.endswith('.md') and f != 'README.md'
            ])
            for sub_file in sub_files:
                sub_path = os.path.join(path, sub_file)
                with open(sub_path, 'r', encoding='utf-8') as f:
                    raw = f.read()
                h1 = extract_h1(raw)

                # Extract section number from filename, e.g. "07-vault.md" -> "07"
                match = re.match(r'^(\d+)-(.+)\.md$', sub_file)
                if match:
                    sec_num = match.group(1)
                    file_slug = match.group(2)
                else:
                    sec_num = '00'
                    file_slug = sub_file.replace('.md', '')

                slug = f'{chapter_num}-{sec_num}-{file_slug}'
                sec = Section(
                    slug=slug,
                    html_file=f'{slug}.html',
                    title=h1,
                    sidebar_title=truncate(h1),
                    chapter_num=chapter_num,
                    is_sommaire=False,
                    md_path=sub_path,
                    github_edit_path=f'sections/{entry}/{sub_file}',
                )
                all_sections.append(sec)

    return all_sections


# ---------------------------------------------------------------------------
# Sidebar builder
# ---------------------------------------------------------------------------

def build_sidebar(all_sections, active_slug, active_chapter):
    """Build hierarchical sidebar navigation HTML."""
    items = []

    # Home link
    active_cls = ' class="active"' if active_slug == 'index' else ''
    items.append(f'<a href="index.html" class="nav-home"{active_cls}>Accueil</a>')

    # Group sections by chapter
    chapters_order = []
    chapters_map = {}
    for sec in all_sections:
        if sec.chapter_num not in chapters_map:
            chapters_order.append(sec.chapter_num)
            chapters_map[sec.chapter_num] = []
        chapters_map[sec.chapter_num].append(sec)

    # Helper to render a chapter block
    def render_chapter(ch_num):
        ch_sections = chapters_map.get(ch_num, [])
        if not ch_sections:
            return
        sommaire = ch_sections[0]
        sub_sections = ch_sections[1:]

        if ch_num == '00':
            active_cls = ' class="active"' if active_slug == sommaire.slug else ''
            items.append(f'<div class="nav-chapter">')
            items.append(f'  <a href="{sommaire.html_file}" class="nav-chapter-title"{active_cls}>{sommaire.sidebar_title}</a>')
            items.append(f'</div>')
            return

        is_open = (active_chapter == ch_num)
        items.append(f'<div class="nav-chapter{"  open" if is_open else ""}">')
        active_cls = ' class="active"' if active_slug == sommaire.slug else ''
        items.append(f'  <a href="{sommaire.html_file}" class="nav-chapter-title"{active_cls}>{sommaire.sidebar_title}</a>')

        if is_open and sub_sections:
            items.append(f'  <div class="nav-sections">')
            for sub in sub_sections:
                active_cls = ' class="active"' if active_slug == sub.slug else ''
                items.append(f'    <a href="{sub.html_file}"{active_cls}>{sub.sidebar_title}</a>')
            items.append(f'  </div>')

        items.append(f'</div>')

    def render_util(slug, file, label):
        active_cls = ' class="active"' if active_slug == slug else ''
        items.append(f'<a href="{file}"{active_cls}>{label}</a>')

    # --- DECOUVRIR ---
    items.append('<div class="nav-group-label">Decouvrir</div>')
    render_util('decouverte', 'decouverte.html', "C'est quoi OpenClaw ?")
    render_chapter('00')
    render_chapter('01')

    # --- DEPLOYER ---
    items.append('<div class="nav-group-label">Deployer</div>')
    render_chapter('02')
    render_chapter('03')
    render_chapter('04')

    # --- OPERER ---
    items.append('<div class="nav-group-label">Operer</div>')
    render_chapter('05')
    render_chapter('06')

    # --- RESSOURCES ---
    items.append('<div class="nav-group-label">Ressources</div>')
    render_util('ecosystem', 'ecosystem.html', 'Ecosysteme')
    render_chapter('07')
    render_util('checklist', 'checklist.html', 'Checklist')
    render_util('contribuer', 'contribuer.html', 'Contribuer')
    render_util('privacy', 'privacy.html', 'Confidentialite')

    return '\n'.join(items)


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

def render_page(title, content_html, sidebar_html):
    """Inject content into the template and return final HTML."""
    template = read_template()
    html = template.replace('<!-- TITLE_PLACEHOLDER -->', title)
    html = html.replace('<!-- NAVIGATION_PLACEHOLDER -->', sidebar_html)
    html = html.replace('<!-- CONTENT_PLACEHOLDER -->', content_html)
    return html


def write_page(filename, html):
    """Write an HTML file to the repo root."""
    path = os.path.join(REPO_ROOT, filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'  -> {filename}')


def build_issues_widget():
    """Return the issues widget HTML (populated by JS)."""
    return """
<div id="issues-widget" style="margin-top:2rem;padding-top:1.5rem;border-top:1px solid var(--border);"></div>"""


def build_giscus_widget():
    """Return the Giscus comments widget HTML."""
    return """
<div class="giscus-wrapper">
  <h3 style="font-size:1rem;margin-bottom:1rem;">Commentaires et discussions</h3>
  <script src="https://giscus.app/client.js"
    data-repo="alexwill87/openclaw-field-playbook"
    data-repo-id="{repo_id}"
    data-category="General"
    data-category-id="{cat_id}"
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
</div>""".format(repo_id=GISCUS_REPO_ID, cat_id=GISCUS_CATEGORY_ID)


def build_edit_link(github_edit_path):
    """Return an 'Edit on GitHub' link."""
    edit_url = f'{GITHUB_URL}/edit/main/{github_edit_path}'
    return f'\n<p class="edit-link"><a href="{edit_url}">Proposer une modification sur GitHub</a></p>'


# ---------------------------------------------------------------------------
# Section page builder
# ---------------------------------------------------------------------------

def build_section_pages(all_sections):
    """Build one HTML page per section."""
    counts = {}  # chapter_num -> count of pages generated

    # Build a mapping from .md filename to .html filename for link rewriting
    section_map = {}
    for sec in all_sections:
        md_basename = os.path.basename(sec.md_path)
        section_map[md_basename] = sec.html_file

    # Build a lookup: chapter_num -> sommaire Section (for breadcrumb level 2)
    sommaire_map = {}
    for sec in all_sections:
        if sec.is_sommaire and sec.chapter_num not in sommaire_map:
            sommaire_map[sec.chapter_num] = sec

    for i, sec in enumerate(all_sections):
        # Read and convert markdown
        with open(sec.md_path, 'r', encoding='utf-8') as f:
            raw = f.read()
        meta, md_content = parse_frontmatter(raw)
        html_content = markdown.markdown(md_content, extensions=MD_EXTENSIONS)

        # Rewrite .md links to .html links
        html_content = rewrite_md_links(html_content, section_map)

        # Build breadcrumb
        breadcrumb_parts = [
            '<nav class="breadcrumb">',
            '  <a href="index.html">Accueil</a>',
        ]
        if sec.is_sommaire:
            # Sommaire page: Accueil / Chapitre (text, no link)
            breadcrumb_parts.append('  <span class="sep">/</span>')
            breadcrumb_parts.append(f'  <span>{sec.title}</span>')
        else:
            # Sub-section page: Accueil / Chapitre (link) / Section (text)
            sommaire = sommaire_map.get(sec.chapter_num)
            if sommaire:
                breadcrumb_parts.append('  <span class="sep">/</span>')
                breadcrumb_parts.append(f'  <a href="{sommaire.html_file}">{sommaire.sidebar_title}</a>')
            breadcrumb_parts.append('  <span class="sep">/</span>')
            breadcrumb_parts.append(f'  <span>{sec.title}</span>')
        breadcrumb_parts.append('</nav>')
        breadcrumb_html = '\n'.join(breadcrumb_parts)

        # Build last-updated
        last_updated_html = ''
        last_updated_val = meta.get('last_updated')
        if last_updated_val:
            formatted = format_last_updated(last_updated_val)
            if formatted:
                last_updated_html = f'<div class="last-updated">Derniere mise a jour : {formatted}</div>'

        # Wrap in section div
        wrapped = f'<section class="chapter">\n{html_content}\n</section>'

        # Edit link
        edit_link = build_edit_link(sec.github_edit_path)

        # Giscus
        giscus = build_giscus_widget()

        # Prev/Next navigation
        nav_links = ['<hr>', '<div style="display:flex;justify-content:space-between;padding:1rem 0;font-size:0.9rem;">']
        if i > 0:
            prev_sec = all_sections[i - 1]
            nav_links.append(
                f'<a href="{prev_sec.html_file}">&larr; {truncate(prev_sec.title, 50)}</a>'
            )
        else:
            nav_links.append('<span></span>')
        if i < len(all_sections) - 1:
            next_sec = all_sections[i + 1]
            nav_links.append(
                f'<a href="{next_sec.html_file}">{truncate(next_sec.title, 50)} &rarr;</a>'
            )
        else:
            nav_links.append('<span></span>')
        nav_links.append('</div>')

        # Issues widget
        issues = build_issues_widget()

        # Assemble: breadcrumb + last-updated BEFORE the section content
        full_content = breadcrumb_html + '\n' + last_updated_html + '\n' + wrapped + edit_link + issues + giscus + '\n' + '\n'.join(nav_links)
        sidebar_html = build_sidebar(all_sections, sec.slug, sec.chapter_num)
        page_html = render_page(sec.title, full_content, sidebar_html)
        write_page(sec.html_file, page_html)

        # Track counts
        counts[sec.chapter_num] = counts.get(sec.chapter_num, 0) + 1

    return counts


# ---------------------------------------------------------------------------
# Page builders (kept from v1)
# ---------------------------------------------------------------------------

def build_index_page(all_sections):
    """Build the landing page (index.html)."""
    # Build chapter cards -- point to sommaire pages
    cards = []
    for entry, chapter_num, short_title, desc in CHAPTERS:
        # Find the sommaire/first page for this chapter
        if chapter_num == '00':
            href = '00-guide.html'
        else:
            href = f'{chapter_num}-00-sommaire.html'
        title = f'Chapitre {int(chapter_num)} -- {short_title}'
        cards.append(
            '<a class="chapter-card" href="{href}">'
            '<div class="num">{title}</div>'
            '<div class="card-desc">{desc}</div>'
            '</a>'.format(href=href, title=title, desc=desc)
        )

    content = """
<div class="landing-hero">
  <h1>OpenClaw Field Playbook</h1>
  <p class="lead">Le seul guide open-source qui couvre le parcours complet :<br>
  de l'installation a l'operation quotidienne d'OpenClaw en entreprise.</p>
  <div style="display:flex;gap:2rem;justify-content:center;margin:1.5rem 0;flex-wrap:wrap;">
    <div style="text-align:center;">
      <div style="font-size:1.8rem;font-weight:700;color:var(--accent);">92</div>
      <div style="font-size:0.78rem;color:var(--text-muted);">sections</div>
    </div>
    <div style="text-align:center;">
      <div style="font-size:1.8rem;font-weight:700;color:var(--accent);">7</div>
      <div style="font-size:0.78rem;color:var(--text-muted);">chapitres</div>
    </div>
    <div style="text-align:center;">
      <div style="font-size:1.8rem;font-weight:700;color:var(--accent);">20</div>
      <div style="font-size:0.78rem;color:var(--text-muted);">bugs corriges par un agent terrain</div>
    </div>
  </div>
  <p style="font-size:0.88rem;color:var(--text-muted);max-width:560px;margin:0 auto 1.5rem;">
    Ne de 3 installations ratees et 5 mois de travail. Teste sur un VPS reel par un agent IA installateur.
    Des commandes copiables, des decisions documentees, des erreurs corrigees.
  </p>
  <div class="hero-actions">
    <a href="decouverte.html" class="btn-primary">C'est quoi OpenClaw ?</a>
    <a href="02-00-sommaire.html" class="btn-secondary">Commencer l'installation</a>
    <a href="{github}" class="btn-secondary" target="_blank">GitHub</a>
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
      <span><a href="01-00-sommaire.html">Definition</a> &rarr; <a href="02-00-sommaire.html">Installation</a> &rarr; <a href="03-00-sommaire.html">Configuration</a>. Comptez une journee.</span>
    </li>
    <li>
      <strong>J'ai deja installe, je veux configurer</strong>
      <span><a href="03-00-sommaire.html">Configuration</a> &rarr; <a href="04-00-sommaire.html">Personnalisation</a>. Les deux chapitres les plus denses.</span>
    </li>
    <li>
      <strong>Je veux des exemples concrets</strong>
      <span><a href="06-00-sommaire.html">Cas d'usage</a> d'abord, puis remontez vers les chapitres techniques selon vos besoins.</span>
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

    sidebar_html = build_sidebar(all_sections, 'index', None)
    page_html = render_page('Accueil', content, sidebar_html)
    write_page('index.html', page_html)


def build_checklist_page(all_sections):
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
<nav class="breadcrumb">
  <a href="index.html">Accueil</a>
  <span class="sep">/</span>
  <span>Checklist</span>
</nav>
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

    sidebar_html = build_sidebar(all_sections, 'checklist', None)
    page_html = render_page('Checklist', content, sidebar_html)
    write_page('checklist.html', page_html)


def build_contribuer_page(all_sections):
    """Build the contribuer.html page."""
    content = """
<nav class="breadcrumb">
  <a href="index.html">Accueil</a>
  <span class="sep">/</span>
  <span>Contribuer</span>
</nav>
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

    sidebar_html = build_sidebar(all_sections, 'contribuer', None)
    page_html = render_page('Contribuer', content, sidebar_html)
    write_page('contribuer.html', page_html)


def build_decouverte_page(all_sections):
    """Build the decouverte.html page."""
    content = """
<nav class="breadcrumb">
  <a href="index.html">Accueil</a>
  <span class="sep">/</span>
  <span>C'est quoi OpenClaw ?</span>
</nav>
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
  <li><a href="01-00-sommaire.html">Chapitre 1 -- Definition</a> : comprendre en detail ce qu'est OpenClaw et ce que ce n'est pas</li>
  <li><a href="02-00-sommaire.html">Chapitre 2 -- Installation</a> : installer OpenClaw de zero sur un serveur</li>
</ul>

<h2>Liens utiles</h2>
<ul>
  <li><a href="https://github.com/open-claw" target="_blank">Documentation officielle OpenClaw</a></li>
  <li><a href="https://github.com/alexwill87/openclaw-field-playbook" target="_blank">Ce playbook sur GitHub</a></li>
  <li>Livre de Dennis Steinberg sur OpenClaw (reference communautaire)</li>
</ul>

</section>
"""

    sidebar_html = build_sidebar(all_sections, 'decouverte', None)
    page_html = render_page('C\'est quoi OpenClaw ?', content, sidebar_html)
    write_page('decouverte.html', page_html)


# ---------------------------------------------------------------------------
# Cleanup old files
# ---------------------------------------------------------------------------

def cleanup_old_chapter_files():
    """Remove old chapitre-XX.html files from repo root."""
    removed = 0
    for f in os.listdir(REPO_ROOT):
        if re.match(r'^chapitre-\d+\.html$', f):
            os.remove(os.path.join(REPO_ROOT, f))
            print(f'  [cleanup] removed {f}')
            removed += 1
    return removed


def build_privacy_page(all_sections):
    """Build the privacy.html page (politique de confidentialite)."""
    content = """
<nav class="breadcrumb">
  <a href="index.html">Accueil</a>
  <span class="sep">/</span>
  <span>Confidentialite</span>
</nav>
<section class="chapter">
<h1>Politique de confidentialite</h1>
<p>Cette page decrit comment le site OpenClaw Field Playbook traite vos donnees.</p>

<h2>Donnees collectees</h2>
<p>Ce site ne collecte aucune donnee personnelle directement.</p>
<ul>
  <li>Les <strong>commentaires giscus</strong> passent par GitHub et sont soumis a la <a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement" target="_blank">politique de confidentialite de GitHub</a>.</li>
  <li>Les <strong>badges GitHub</strong> (etoiles, forks) utilisent l'API publique de GitHub. Aucune donnee utilisateur n'est transmise.</li>
</ul>

<h2>Cookies</h2>
<p>Ce site n'utilise aucun cookie.</p>
<p>Le site utilise <code>localStorage</code> pour sauvegarder :</p>
<ul>
  <li>Votre preference de theme (clair ou sombre)</li>
  <li>Votre progression dans la checklist interactive</li>
</ul>
<p>Ces donnees restent uniquement dans votre navigateur. Aucun cookie tiers. Aucun tracking. Aucun outil d'analyse (pas de Google Analytics, pas de Matomo, rien).</p>

<h2>Hebergement</h2>
<p>Le site est heberge sur <strong>GitHub Pages</strong>. Le code source est public et consultable sur <a href="https://github.com/alexwill87/openclaw-field-playbook" target="_blank">GitHub</a>.</p>
<p>GitHub Pages peut collecter des informations techniques (adresse IP, user-agent) dans le cadre de son fonctionnement. Consultez la <a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement" target="_blank">politique de confidentialite de GitHub</a> pour plus de details.</p>

<h2>Contact</h2>
<p>Pour toute question relative a cette politique de confidentialite, vous pouvez <a href="https://github.com/alexwill87/openclaw-field-playbook/issues" target="_blank">ouvrir une issue sur GitHub</a>.</p>

</section>
"""
    sidebar_html = build_sidebar(all_sections, 'privacy', None)
    page_html = render_page('Politique de confidentialite', content, sidebar_html)
    write_page('privacy.html', page_html)


def build_ecosystem_page(all_sections):
    """Build the ecosystem.html page."""
    content = """
<nav class="breadcrumb">
  <a href="index.html">Accueil</a>
  <span class="sep">/</span>
  <span>Ecosysteme</span>
</nav>
<section class="chapter">
<h1>Ecosysteme OpenClaw</h1>
<p>Tout ce qui gravite autour d'OpenClaw : le projet officiel, les marketplaces de skills, les frameworks concurrents, les outils communautaires, les hebergeurs, les ressources d'apprentissage et les enjeux de securite.</p>
<p>Derniere mise a jour : avril 2026.</p>

<hr>

<h2>Le projet officiel</h2>

<table>
<thead><tr><th>Ressource</th><th>Description</th><th>Lien</th></tr></thead>
<tbody>
<tr><td><strong>OpenClaw (site officiel)</strong></td><td>Assistant IA personnel open-source. Framework d'agents qui transforme les LLM en agents operationnels.</td><td><a href="https://openclaw.ai" target="_blank">openclaw.ai</a></td></tr>
<tr><td><strong>Documentation officielle</strong></td><td>Guide d'installation, reference API, configuration des skills et du gateway.</td><td><a href="https://docs.openclaw.ai" target="_blank">docs.openclaw.ai</a></td></tr>
<tr><td><strong>GitHub OpenClaw</strong></td><td>Repo principal. 250 000+ etoiles (mars 2026). Le projet open-source a la croissance la plus rapide sur GitHub.</td><td><a href="https://github.com/openclaw" target="_blank">github.com/openclaw</a></td></tr>
<tr><td><strong>ClawHub</strong></td><td>Marketplace officielle de skills. 13 700+ skills communautaires. Standard MCP (Model Context Protocol).</td><td><a href="https://github.com/openclaw/clawhub" target="_blank">github.com/openclaw/clawhub</a></td></tr>
</tbody>
</table>

<hr>

<h2>Marketplaces et registres de skills</h2>

<table>
<thead><tr><th>Projet</th><th>Description</th><th>Lien</th></tr></thead>
<tbody>
<tr><td><strong>ClawHub</strong></td><td>Registre officiel. 13 729 skills (fevrier 2026). Attention : ~20% sont de faible qualite ou potentiellement risques. Toujours verifier le code source avant d'installer.</td><td><a href="https://github.com/openclaw/clawhub" target="_blank">GitHub</a></td></tr>
<tr><td><strong>awesome-openclaw-skills</strong></td><td>5 400+ skills filtrees et categorizees depuis le registre officiel. Curate par VoltAgent.</td><td><a href="https://github.com/VoltAgent/awesome-openclaw-skills" target="_blank">GitHub</a></td></tr>
<tr><td><strong>awesome-openclaw-agents</strong></td><td>162 templates SOUL.md prets a l'emploi, classes en 19 categories (productivite, dev, marketing, business).</td><td><a href="https://github.com/mergisi/awesome-openclaw-agents" target="_blank">GitHub</a></td></tr>
</tbody>
</table>

<hr>

<h2>Ressources communautaires et listes curatees</h2>

<table>
<thead><tr><th>Projet</th><th>Description</th><th>Lien</th></tr></thead>
<tbody>
<tr><td><strong>awesome-openclaw</strong> (vincentkoc)</td><td>La liste curatee la plus complete : skills, plugins, systemes de memoire, outils MCP, stacks de deploiement, plateformes ecosysteme.</td><td><a href="https://github.com/vincentkoc/awesome-openclaw" target="_blank">GitHub</a></td></tr>
<tr><td><strong>awesome-openclaw</strong> (SamurAIGPT)</td><td>Ressources, outils, skills, tutoriels et articles. Bonne porte d'entree pour les debutants.</td><td><a href="https://github.com/SamurAIGPT/awesome-openclaw" target="_blank">GitHub</a></td></tr>
<tr><td><strong>awesome-openclaw-resources</strong></td><td>Projets open-source, outils, tutoriels, podcasts et createurs de contenu.</td><td><a href="https://github.com/SebConejo/awesome-openclaw-resources" target="_blank">GitHub</a></td></tr>
<tr><td><strong>awesome-openclaw-usecases</strong></td><td>Cas d'usage reels : workflows pratiques montrant comment OpenClaw s'integre dans le quotidien.</td><td><a href="https://github.com/hesamsheikh/awesome-openclaw-usecases" target="_blank">GitHub</a></td></tr>
<tr><td><strong>OpenClaw Field Playbook</strong></td><td>Ce guide. 81 sections, 7 chapitres, le seul playbook francophone couvrant le parcours complet installation-a-maintenance.</td><td><a href="https://github.com/alexwill87/openclaw-field-playbook" target="_blank">GitHub</a></td></tr>
</tbody>
</table>

<hr>

<h2>Livres et guides</h2>

<table>
<thead><tr><th>Titre</th><th>Auteur</th><th>Format</th><th>Prix</th><th>Description</th></tr></thead>
<tbody>
<tr><td><strong>The OpenClaw Playbook</strong></td><td>Dennis Steinberg</td><td>eBook (LeanPub)</td><td>~23 USD</td><td>Guide "prompt-first" en 24 chapitres. Couvre identite, memoire, connexions, securite, taches, routines, decisions. La reference conceptuelle.</td></tr>
<tr><td><strong>OpenClaw Playbook</strong></td><td>Lunar</td><td>eBook (Fnac/Everand)</td><td>~15 USD</td><td>Guide pratique oriente configuration.</td></tr>
<tr><td><strong>OpenClaw Field Playbook</strong></td><td>Alex Willemetz</td><td>Site web + GitHub (CC-BY 4.0)</td><td>Gratuit</td><td>Ce guide. Open-source, francophone, teste sur le terrain.</td></tr>
</tbody>
</table>

<hr>

<h2>Hebergement et deploiement</h2>

<table>
<thead><tr><th>Provider</th><th>Type</th><th>Prix</th><th>Particularite</th></tr></thead>
<tbody>
<tr><td><strong>Hetzner</strong></td><td>VPS auto-gere</td><td>~4-7 EUR/mois</td><td>Recommande dans ce playbook. Datacenters EU (Allemagne, Finlande). Excellent rapport qualite/prix.</td></tr>
<tr><td><strong>OVHcloud</strong></td><td>VPS auto-gere</td><td>~4-8 EUR/mois</td><td>Datacenters en France. Ideal pour la conformite RGPD.</td></tr>
<tr><td><strong>Scaleway</strong></td><td>VPS auto-gere</td><td>~5-10 EUR/mois</td><td>Infrastructure francaise. Bonne integration Docker.</td></tr>
<tr><td><strong>DigitalOcean</strong></td><td>VPS + Marketplace</td><td>~6-12 USD/mois</td><td>Image OpenClaw 1-click dans le Marketplace. App Platform pour deploiement manage.</td></tr>
<tr><td><strong>Hostinger</strong></td><td>VPS manage</td><td>~7 USD/mois</td><td>Template Docker pre-configure pour OpenClaw. 1-click deploy.</td></tr>
<tr><td><strong>Oracle Cloud</strong></td><td>Free tier</td><td>Gratuit</td><td>24 Go RAM gratuits (Always Free). Suffisant pour des modeles 7B locaux.</td></tr>
<tr><td><strong>Contabo</strong></td><td>VPS budget</td><td>~4 EUR/mois</td><td>Le moins cher. RAM genereuse. Performances reseau inferieures.</td></tr>
<tr><td><strong>Kimi Claw</strong></td><td>Cloud manage</td><td>Variable</td><td>Deploiement OpenClaw en secondes, zero configuration.</td></tr>
</tbody>
</table>

<hr>

<h2>Providers LLM (via OpenRouter ou direct)</h2>

<table>
<thead><tr><th>Provider</th><th>Modeles cles</th><th>Acces</th><th>Notes</th></tr></thead>
<tbody>
<tr><td><strong>OpenRouter</strong></td><td>Tous (proxy multi-provider)</td><td><a href="https://openrouter.ai" target="_blank">openrouter.ai</a></td><td>Recommande : un seul compte pour acceder a tous les modeles. Suivi des couts integre.</td></tr>
<tr><td><strong>Anthropic</strong></td><td>Claude Sonnet 4, Claude Haiku 4.5, Claude Opus 4.6</td><td><a href="https://console.anthropic.com" target="_blank">console.anthropic.com</a></td><td>Excellent en francais. Le meilleur pour les taches complexes.</td></tr>
<tr><td><strong>Mistral AI</strong></td><td>Mistral Large, Mistral Medium</td><td><a href="https://console.mistral.ai" target="_blank">console.mistral.ai</a></td><td>Entreprise francaise. Tres bon en francais. Modeles efficaces en tokens.</td></tr>
<tr><td><strong>Google</strong></td><td>Gemini 2.5 Pro, Gemini 2.5 Flash</td><td><a href="https://aistudio.google.com" target="_blank">aistudio.google.com</a></td><td>Contexte long (1M tokens). Bon pour l'analyse de documents.</td></tr>
<tr><td><strong>OpenAI</strong></td><td>GPT-4o, o3, o4-mini</td><td><a href="https://platform.openai.com" target="_blank">platform.openai.com</a></td><td>Large ecosysteme. Bon generaliste.</td></tr>
<tr><td><strong>Meta (Llama)</strong></td><td>Llama 4 Scout, Llama 4 Maverick</td><td>Via OpenRouter ou local</td><td>Open-source. Gratuit si heberge localement.</td></tr>
</tbody>
</table>

<hr>

<h2>Frameworks concurrents et complementaires</h2>

<table>
<thead><tr><th>Framework</th><th>Approche</th><th>Force</th><th>Faiblesse vs OpenClaw</th></tr></thead>
<tbody>
<tr><td><strong>LangChain / LangGraph</strong></td><td>Orchestration par graphes</td><td>Controle deterministe, ideal pour la conformite</td><td>Plus complexe a configurer. Pas d'interface utilisateur native.</td></tr>
<tr><td><strong>CrewAI</strong></td><td>Multi-agents par roles</td><td>Setup rapide (~30% plus rapide que LangChain). Architecture Crews + Flows.</td><td>Moins de skills pre-faites. Ecosysteme plus petit.</td></tr>
<tr><td><strong>AutoGPT / AgentGPT</strong></td><td>Autonomie maximale</td><td>L'agent definit ses propres sous-taches</td><td>Difficile a controler. Cout en tokens eleve. Risque de boucles infinies.</td></tr>
<tr><td><strong>n8n</strong></td><td>Low-code visual</td><td>1000+ connecteurs. Interface visuelle. Pas besoin de coder.</td><td>Moins flexible pour les agents conversationnels.</td></tr>
<tr><td><strong>Nanobot</strong></td><td>Ultra-leger (4000 lignes Python)</td><td>99% plus petit qu'OpenClaw. Simple a comprendre et modifier.</td><td>Moins de features. Pas de marketplace de skills.</td></tr>
<tr><td><strong>NanoClaw</strong></td><td>Securise par defaut</td><td>Isolation container, execution sandboxee</td><td>Moins de skills. Oriente securite enterprise.</td></tr>
<tr><td><strong>Moltworker</strong></td><td>Serverless (Cloudflare Workers)</td><td>Pas d'acces systeme local. Sandbox par design.</td><td>Pas d'acces au filesystem. Limite pour les taches systeme.</td></tr>
</tbody>
</table>

<hr>

<h2>Securite</h2>

<p>OpenClaw a connu des incidents de securite significatifs en 2026. Voici ce que vous devez savoir :</p>

<table>
<thead><tr><th>Incident</th><th>Date</th><th>Impact</th><th>Mitigation</th></tr></thead>
<tbody>
<tr><td><strong>ClawJacked</strong></td><td>Fevrier 2026</td><td>Tout site web peut hijacker un agent OpenClaw local via WebSocket. Le rate limiter exempte localhost.</td><td>Mettre a jour vers la derniere version. Configurer un mot de passe gateway fort.</td></tr>
<tr><td><strong>ClawHavoc</strong></td><td>Mars 2026</td><td>300+ skills malicieuses sur ClawHub avec des noms typosquattes.</td><td>Verifier le code source. Utiliser le skill Security Auditor. Verifier les scans VirusTotal sur ClawHub.</td></tr>
<tr><td><strong>9 CVE en 4 jours</strong></td><td>Mars 2026</td><td>1 CVE critique (9.9/10), 6 high, 2 medium. 135 000 instances exposees publiquement.</td><td>Mettre a jour immediatement. Ne JAMAIS exposer le gateway sur Internet public. Utiliser Tailscale.</td></tr>
</tbody>
</table>

<p><strong>Outils de securite :</strong></p>
<ul>
<li><strong>NemoClaw</strong> (NVIDIA) — Sandbox kernel-level pour les agents. Enterprise preview. <a href="https://www.chainup.com/blog/agentic-ai-openclaw-crypto-exchange-infrastructure/" target="_blank">En savoir plus</a></li>
<li><strong>KnoxClaw</strong> (AccuKnox) — Sandboxing kernel pour les instances OpenClaw. <a href="https://accuknox.com/blog/introducing-knoxclaw-for-openclaw-instances" target="_blank">En savoir plus</a></li>
<li><strong>Security Auditor skill</strong> — Skill ClawHub qui audite les permissions et les acces de votre agent a runtime.</li>
</ul>

<blockquote>
<p><strong>Recommandation de ce playbook :</strong> Ne JAMAIS exposer le port du gateway OpenClaw sur Internet public. Toujours utiliser Tailscale ou un VPN. Toujours verifier le code source d'un skill avant de l'installer. Mettre a jour regulierement.</p>
</blockquote>

<hr>

<h2>Outils MCP (Model Context Protocol)</h2>

<p>MCP est le standard ouvert cree par Anthropic pour connecter les modeles IA au monde reel. OpenClaw supporte MCP nativement via ClawHub.</p>

<table>
<thead><tr><th>Serveur MCP</th><th>Description</th><th>Lien</th></tr></thead>
<tbody>
<tr><td><strong>openclaw-mcp</strong></td><td>Bridge securise entre Claude.ai et votre instance OpenClaw auto-hebergee. Authentification OAuth2.</td><td><a href="https://github.com/freema/openclaw-mcp" target="_blank">GitHub</a></td></tr>
<tr><td><strong>Playwright MCP</strong></td><td>Automatisation navigateur complete via MCP.</td><td>ClawHub</td></tr>
<tr><td><strong>Supabase MCP</strong></td><td>Acces base de donnees PostgreSQL via MCP.</td><td>ClawHub</td></tr>
<tr><td><strong>Tavily MCP</strong></td><td>Recherche web en temps reel via MCP.</td><td>ClawHub</td></tr>
</tbody>
</table>

<hr>

<h2>Apprentissage et tutoriels</h2>

<table>
<thead><tr><th>Ressource</th><th>Format</th><th>Description</th><th>Lien</th></tr></thead>
<tbody>
<tr><td><strong>10 GitHub Repos to Master OpenClaw</strong></td><td>Article</td><td>Selection curatee par KDnuggets des meilleurs repos pour apprendre.</td><td><a href="https://www.kdnuggets.com/10-github-repositories-to-master-openclaw" target="_blank">KDnuggets</a></td></tr>
<tr><td><strong>9 OpenClaw Projects to Build</strong></td><td>Tutoriels</td><td>Projets pratiques : bots Reddit, serveurs auto-reparants, etc.</td><td><a href="https://www.datacamp.com/blog/openclaw-projects" target="_blank">DataCamp</a></td></tr>
<tr><td><strong>OpenClaw Explained</strong></td><td>Article</td><td>Introduction complete pour debutants.</td><td><a href="https://www.kdnuggets.com/openclaw-explained-the-free-ai-agent-tool-going-viral-already-in-2026" target="_blank">KDnuggets</a></td></tr>
<tr><td><strong>What is OpenClaw?</strong></td><td>Guide</td><td>Introduction technique par DigitalOcean.</td><td><a href="https://www.digitalocean.com/resources/articles/what-is-openclaw" target="_blank">DigitalOcean</a></td></tr>
<tr><td><strong>OpenClaw MasterClass</strong></td><td>Cours</td><td>Cours structure avec module ClawHub.</td><td><a href="https://tenten.co/openclaw/en/docs/masterclass/module-04-clawhub" target="_blank">Tenten</a></td></tr>
</tbody>
</table>

</section>
"""
    sidebar_html = build_sidebar(all_sections, 'ecosystem', None)
    page_html = render_page('Ecosysteme OpenClaw', content, sidebar_html)
    write_page('ecosystem.html', page_html)
    print('  -> ecosystem.html')


def build_search_index(all_sections):
    """Generate search-index.json with slug, title, url and body excerpt for each section."""
    index = []
    for sec in all_sections:
        with open(sec.md_path, 'r', encoding='utf-8') as f:
            raw = f.read()
        # Strip frontmatter
        content = strip_frontmatter(raw)
        # Strip markdown headings, code fences, links syntax, images, bold/italic markers
        plain = re.sub(r'```[\s\S]*?```', ' ', content)   # code blocks
        plain = re.sub(r'`[^`]*`', ' ', plain)            # inline code
        plain = re.sub(r'!\[[^\]]*\]\([^)]*\)', ' ', plain)  # images
        plain = re.sub(r'\[[^\]]*\]\([^)]*\)', ' ', plain)   # links
        plain = re.sub(r'#{1,6}\s+', ' ', plain)          # headings
        plain = re.sub(r'[*_~]{1,3}', '', plain)          # bold/italic/strikethrough
        plain = re.sub(r'\|', ' ', plain)                  # table pipes
        plain = re.sub(r'-{3,}', ' ', plain)              # horizontal rules
        plain = re.sub(r'\s+', ' ', plain).strip()         # collapse whitespace
        body = plain[:200]
        index.append({
            'slug': sec.slug,
            'title': sec.title,
            'url': sec.html_file,
            'body': body,
        })
    output_path = os.path.join(REPO_ROOT, 'search-index.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    print(f'  -> search-index.json ({len(index)} entries)')


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    print('OpenClaw Field Playbook -- build multi-page site (v2: 1 page per section)')
    print('=' * 60)

    # Cleanup old chapter files
    removed = cleanup_old_chapter_files()
    if removed:
        print(f'  Removed {removed} old chapitre-XX.html files')
        print()

    # Build section registry
    all_sections = build_section_registry()
    print(f'Found {len(all_sections)} sections across {len(CHAPTERS)} chapters')
    print()

    # Build all section pages
    print('Building section pages...')
    counts = build_section_pages(all_sections)
    print()

    # Build utility pages
    print('Building utility pages...')
    build_index_page(all_sections)
    build_checklist_page(all_sections)
    build_contribuer_page(all_sections)
    build_decouverte_page(all_sections)
    build_ecosystem_page(all_sections)
    build_privacy_page(all_sections)
    print()

    # Build search index
    print('Building search index...')
    build_search_index(all_sections)
    print()

    # Summary
    print('=' * 60)
    print('Build summary:')
    total = 0
    for entry, chapter_num, short_title, _ in CHAPTERS:
        n = counts.get(chapter_num, 0)
        total += n
        print(f'  Chapitre {int(chapter_num)} ({short_title}): {n} pages')
    print(f'  Utility pages: 6 (index, checklist, contribuer, decouverte, ecosystem, privacy)')
    print(f'  TOTAL: {total + 6} HTML files')
    print()
    print('Build complete. All files written to repo root.')
