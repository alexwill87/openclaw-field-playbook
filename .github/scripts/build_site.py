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
     'Comment lire ce guide et par où commencer'),
    ('01-definition', '01', 'Définition',
     'Ce qu\'est OpenClaw, ce que ce n\'est pas'),
    ('02-installation', '02', 'Installation',
     'Installer OpenClaw de zéro sur un VPS'),
    ('03-configuration', '03', 'Configuration',
     'Configurer l\'agent pour son contexte'),

    ('04-personalisation', '04', 'Personnalisation',
     'Adapter le comportement, le ton, les workflows'),
    ('05-maintenance', '05', 'Maintenance',
     'Garder l\'agent fiable dans le temps'),
    ('06-use-cases', '06', 'Cas d\'usage',
     'Exemples concrets par type d\'organisation'),
    ('07-localisation', '07', 'Localisation',
     'Adapter OpenClaw à d\'autres langues et contextes'),
]

MD_EXTENSIONS = ['tables', 'fenced_code', 'codehilite', 'toc']

MONTH_NAMES_FR = {
    '01': 'janvier', '02': 'février', '03': 'mars', '04': 'avril',
    '05': 'mai', '06': 'juin', '07': 'juillet', '08': 'août',
    '09': 'septembre', '10': 'octobre', '11': 'novembre', '12': 'décembre',
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


def strip_section_number(title):
    """Remove section numbering like '2.15 -- ' or '3.18 -- ' from a title."""
    return re.sub(r'^\d+\.\d+\s*--\s*', '', title)


def extract_h1(md_text):
    """Extract the first H1 title from markdown content (after frontmatter).
    Section numbers (e.g. '2.15 -- ') are stripped from the returned title."""
    clean = strip_frontmatter(md_text)
    for line in clean.split('\n'):
        line = line.strip()
        if line.startswith('# '):
            return strip_section_number(line[2:].strip())
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
                sidebar_title=short_title,
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
                    sidebar_title=short_title,
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
            is_active = active_slug == sommaire.slug
            active_cls = ' class="active"' if is_active else ''
            aria_current = ' aria-current="page"' if is_active else ''
            items.append(f'<div class="nav-chapter">')
            items.append(f'  <a href="{sommaire.html_file}" class="nav-chapter-title"{active_cls}{aria_current}>{sommaire.sidebar_title}</a>')
            items.append(f'</div>')
            return

        is_open = (active_chapter == ch_num)
        items.append(f'<div class="nav-chapter{"  open" if is_open else ""}">')
        is_active = active_slug == sommaire.slug
        active_cls = ' class="active"' if is_active else ''
        aria_current = ' aria-current="page"' if is_active else ''
        items.append(f'  <a href="{sommaire.html_file}" class="nav-chapter-title"{active_cls}{aria_current}>{sommaire.sidebar_title}</a>')

        if is_open and sub_sections:
            items.append(f'  <div class="nav-sections">')
            for sub in sub_sections:
                is_active = active_slug == sub.slug
                active_cls = ' class="active"' if is_active else ''
                aria_current = ' aria-current="page"' if is_active else ''
                items.append(f'    <a href="{sub.html_file}"{active_cls}{aria_current}>{sub.sidebar_title}</a>')
            items.append(f'  </div>')

        items.append(f'</div>')

    def render_util(slug, file, label):
        active_cls = ' class="active"' if active_slug == slug else ''
        items.append(f'<a href="{file}"{active_cls}>{label}</a>')

    # --- AVANT-PROPOS ---
    items.append('<div class="nav-group-label">Avant-propos</div>')
    render_util('decouverte', 'decouverte.html', "C'est quoi OpenClaw ?")
    render_util('persona-entrepreneur', 'persona-entrepreneur.html', 'Focus Entrepreneurs')
    render_util('persona-cto', 'persona-cto.html', 'Focus Équipes tech')
    render_util('persona-dev', 'persona-dev.html', 'Focus Développeurs')
    render_util('persona-agent', 'persona-agent.html', 'Focus Agents IA')

    # --- DÉCOUVRIR ---
    items.append('<div class="nav-group-label">Découvrir</div>')
    render_chapter('00')
    render_chapter('01')

    # --- DEPLOYER ---
    items.append('<div class="nav-group-label">Déployer</div>')
    render_chapter('02')
    render_chapter('03')
    render_chapter('04')

    # --- OPERER ---
    items.append('<div class="nav-group-label">Opérer</div>')
    render_chapter('05')
    render_chapter('06')

    # --- RESSOURCES ---
    items.append('<div class="nav-group-label">Ressources</div>')
    render_util('ecosystem', 'ecosystem.html', 'Écosystème')
    render_chapter('07')
    render_util('checklist', 'checklist.html', 'Checklist')
    render_util('contribuer', 'contribuer.html', 'Contribuer')
    render_util('privacy', 'privacy.html', 'Confidentialité')

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

        # Strip section numbers from H1 in rendered HTML (e.g. "2.15 -- Gateway" -> "Gateway")
        html_content = re.sub(
            r'(<h1[^>]*>)\s*\d+\.\d+\s*--\s*',
            r'\1',
            html_content
        )

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
                last_updated_html = f'<div class="last-updated">Dernière mise à jour : {formatted}</div>'

        # Build learning objectives box from h2/h3 tags in the HTML
        import re as _re
        toc_items = []
        toc_texts = []
        heading_pattern = _re.compile(r'<(h[23])\s+id="([^"]+)"[^>]*>(.*?)</\1>', _re.IGNORECASE)
        for match in heading_pattern.finditer(html_content):
            tag = match.group(1).lower()
            anchor = match.group(2)
            text = _re.sub(r'<[^>]+>', '', match.group(3)).strip()
            css_class = ' class="toc-h3"' if tag == 'h3' else ''
            toc_items.append(f'<li{css_class}><a href="#{anchor}">{text}</a></li>')
            if tag == 'h2':
                toc_texts.append(text)

        toc_html = ''
        bravo_html = ''
        if len(toc_items) > 3:  # Only show if there are enough headings
            toc_html = (
                '<div class="learning-objectives">\n'
                '  <button type="button" class="lo-header" onclick="this.parentElement.classList.toggle(\'collapsed\')" aria-expanded="true" aria-controls="lo-list">\n'
                '    <span class="lo-icon" aria-hidden="true">&#127891;</span>\n'
                '    Ce que vous allez apprendre\n'
                '    <span class="lo-arrow" aria-hidden="true">&#9660;</span>\n'
                '  </button>\n'
                '  <ul class="lo-list" id="lo-list">\n'
            )
            toc_html += '\n'.join(f'    {item}' for item in toc_items)
            toc_html += '\n  </ul>\n</div>\n'

            # Build bravo box for bottom of page
            count = len(toc_texts)
            topics = ', '.join(toc_texts[:4])
            if count > 4:
                topics += f' et {count - 4} autre{"s" if count - 4 > 1 else ""}'
            bravo_html = (
                '<div class="bravo-box">\n'
                '  <div class="bravo-header">Bravo, vous avez termin\u00e9 cette section !</div>\n'
                f'  <div class="bravo-body">Vous avez couvert : {topics}.'
            )
            if i < len(all_sections) - 1:
                next_s = all_sections[i + 1]
                bravo_html += f' <a href="{next_s.html_file}">Continuer &rarr;</a>'
            bravo_html += '</div>\n</div>\n'

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

        # Assemble: breadcrumb + last-updated + learning objectives BEFORE content, bravo AFTER
        full_content = breadcrumb_html + '\n' + last_updated_html + '\n' + toc_html + wrapped + bravo_html + edit_link + issues + giscus + '\n' + '\n'.join(nav_links)
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
        cards.append(
            '<a class="chapter-card" href="{href}">'
            '<div class="card-title">{short}</div>'
            '<div class="card-desc">{desc}</div>'
            '</a>'.format(href=href, short=short_title, desc=desc)
        )

    content = """
<div class="landing-hero">
  <h1>OpenClaw Field Playbook</h1>
  <p class="lead">Le guide open-source pour installer OpenClaw proprement.<br>
  Écrit par un praticien. Testé sur le terrain. Partagé avec tout le monde.</p>
  <p style="font-size:0.82rem;color:var(--text-muted);max-width:520px;margin:0.5rem auto 1rem;">
    J'ai fait 3 installations ratées avant de comprendre. Ce playbook est le résultat :
    <strong style="color:var(--accent);">92</strong> sections, <strong style="color:var(--accent);">7</strong> chapitres,
    <strong style="color:var(--accent);">20</strong> bugs corrigés par un agent terrain.
    Tout est là pour que vous n'ayez pas à galérer comme moi.
    <span style="display:block;margin-top:0.3rem;"><a href="{github}" style="color:var(--accent);">— Alex Willemetz</a></span>
  </p>
  <div class="hero-actions">
    <a href="decouverte.html" class="btn-primary">C'est quoi OpenClaw ?</a>
    <a href="02-00-sommaire.html" class="btn-secondary">Commencer l'installation</a>
    <a href="{github}" class="btn-secondary" target="_blank">GitHub</a>
  </div>
</div>

<div class="landing-section">
  <h2>Vous êtes qui ?</h2>
  <p>Ce guide s'adapte à votre profil. Choisissez le vôtre.</p>
  <div class="audience-grid">
    <a class="audience-card" href="persona-entrepreneur.html" style="text-decoration:none;color:var(--text);">
      <strong>Entrepreneur / Artisan</strong>
      <p>Vous dirigez une entreprise et vous voulez comprendre ce que l'IA peut faire pour vous — sans jargon.</p>
    </a>
    <a class="audience-card" href="persona-cto.html" style="text-decoration:none;color:var(--text);">
      <strong>CTO / Équipe technique</strong>
      <p>Vous voulez déployer un agent IA pour votre équipe, sur votre infra, avec vos contraintes.</p>
    </a>
    <a class="audience-card" href="persona-dev.html" style="text-decoration:none;color:var(--text);">
      <strong>Développeur indépendant</strong>
      <p>Vous savez ce qu'est Docker. Vous voulez les commandes, pas le blabla.</p>
    </a>
    <a class="audience-card" href="persona-agent.html" style="text-decoration:none;color:var(--text);">
      <strong>Agent IA</strong>
      <p>Vous êtes un agent. Vous clonez ce repo et vous suivez les sections comme un runbook.</p>
    </a>
  </div>
</div>

<div class="landing-section">
  <h2>Par où commencer</h2>
  <ul class="path-list">
    <li>
      <strong>Je découvre</strong>
      <span><a href="decouverte.html">C'est quoi OpenClaw ?</a> &rarr; <a href="01-00-sommaire.html">Définition</a> &rarr; <a href="02-00-sommaire.html">Installation</a></span>
    </li>
    <li>
      <strong>J'installe</strong>
      <span><a href="02-00-sommaire.html">Installation</a> &rarr; <a href="03-00-sommaire.html">Configuration</a> &rarr; <a href="04-00-sommaire.html">Personnalisation</a></span>
    </li>
    <li>
      <strong>Je veux des exemples</strong>
      <span><a href="06-00-sommaire.html">Cas d'usage</a> &rarr; puis remontez vers les chapitres techniques</span>
    </li>
    <li>
      <strong>Je suis un agent IA</strong>
      <span>Lisez <a href="https://github.com/alexwill87/openclaw-field-playbook/blob/main/CLAUDE.md">CLAUDE.md</a> &rarr; <a href="02-01-prerequis.html">Section 2.1</a> et suivez dans l'ordre</span>
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
      <p>Suivez votre progression étape par étape. Sauvegarde automatique.</p>
    </a>
    <a class="audience-card" href="contribuer.html" style="text-decoration:none;color:var(--text);">
      <strong>Contribuer</strong>
      <p>Corrigez une erreur, ajoutez un cas d'usage, proposez une section.</p>
    </a>
    <a class="audience-card" href="decouverte.html" style="text-decoration:none;color:var(--text);">
      <strong>C'est quoi OpenClaw ?</strong>
      <p>Pour ceux qui partent de zéro. Pas de jargon.</p>
    </a>
    <a class="audience-card" href="{github}/issues" style="text-decoration:none;color:var(--text);" target="_blank">
      <strong>Signaler un problème</strong>
      <p>Une commande qui ne marche pas ? Un lien cassé ? Dites-le nous.</p>
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
            'VPS commandé et accessible en SSH',
            'Utilisateur non-root créé avec sudo',
            'Pare-feu configuré (UFW / iptables)',
            'SSH sécurisé (clé uniquement, port changé)',
            'Fail2ban installé et actif',
            'Tailscale installé et connecté',
            'Docker et Docker Compose installés',
            'Node.js et PM2 installés',
            'Structure de dossiers créée',
            'Vault configuré et secrets stockés',
            'PostgreSQL installé et base créée',
            'Health check endpoint fonctionnel',
            'OpenClaw installé et démarré',
            'Compte OpenRouter créé et clé API configurée',
            'Bot Telegram créé et connecté',
            'Gateway systemd configurée et active',
            'Repository Git initialisé',
            'CLAUDE.md créé à la racine',
            'Script de déploiement en place',
        ],
        'Chapitre 3 -- Configuration': [
            'Périmètre de l\'agent défini',
            'SOUL.md rédigé',
            'USER.md rédigé',
            'AGENTS.md rédigé (si multi-agents)',
            'CONSTITUTION.md rédigée',
            'Trois zones mémoire configurées',
            'MEMORY.md initialisé',
            'Knowledge base alimentée',
            'Principe une-source-de-vérité appliqué',
            'Calendrier et tâches connectés',
            'Briefing du matin configuré',
            'Crons planifiés',
        ],
        'Chapitre 4 -- Personnalisation': [
            'System prompt rédigé et testé',
            'Personnalité et ton définis',
            'Tâches récurrentes configurées',
            'Workflows documentés dans workflows.md',
            'Boundary prompt en place',
            'Audit des accès réalisé',
            'Rythme hebdomadaire établi',
            'Configuration bilingue si nécessaire',
        ],
        'Chapitre 5 -- Maintenance': [
            'Health check automatisé',
            'Logs centralisés et consultables',
            'Backups automatisés et testés',
            'Monitoring en place (alertes)',
            'Procédure en cas de panne documentée',
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
<p>Cochez les étapes au fur et à mesure de votre avancement. Votre progression est sauvegardée automatiquement dans votre navigateur.</p>
<p style="margin-bottom:1.5rem;">
  <strong>Progression :</strong> <span id="progress-count">0</span> / {total} étapes
  <span id="progress-bar" style="display:inline-block;width:200px;height:8px;background:var(--border);border-radius:4px;margin-left:0.5rem;vertical-align:middle;">
    <span id="progress-fill" style="display:block;height:100%;background:var(--accent);border-radius:4px;width:0%;transition:width 0.3s;"></span>
  </span>
</p>
<div style="margin-bottom:1.5rem;">
  <button onclick="exportChecklist()" style="padding:0.5rem 1rem;border:1px solid var(--border);border-radius:6px;background:var(--bg);cursor:pointer;font-size:0.85rem;">Exporter en texte</button>
  <button onclick="resetChecklist()" style="padding:0.5rem 1rem;border:1px solid var(--border);border-radius:6px;background:var(--bg);cursor:pointer;font-size:0.85rem;margin-left:0.5rem;">Réinitialiser</button>
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
  if (!confirm('Réinitialiser toute la checklist ?')) return;
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
<p>Ce playbook est un projet open-source. Toute contribution est bienvenue, à condition de respecter les niveaux de gouvernance décrits ci-dessous.</p>

<h2>Trois niveaux de contribution</h2>

<h3>T3 -- Corrections</h3>
<p>Typos, liens cassés, exemples à clarifier, reformulations mineures. Vous pouvez soumettre une Pull Request directement ou ouvrir une Issue. Ces contributions sont mergées rapidement.</p>

<h3>T2 -- Sections</h3>
<p>Nouveau contenu, réécritures de sections existantes, ajout de cas d'usage. Ouvrez d'abord une Issue pour décrire votre proposition. Une fois validée par le maintainer, soumettez une Pull Request.</p>

<h3>T1 -- Structure</h3>
<p>Modifier l'organisation des chapitres, ajouter ou supprimer un chapitre, changer l'architecture du playbook. Ces modifications requièrent une Issue étiquetée <code>governance</code> et une décision du fondateur. Ne soumettez pas de PR sans validation préalable.</p>

<h2>Comment soumettre une correction</h2>
<ol>
  <li><strong>Fork</strong> le repository sur GitHub</li>
  <li><strong>Éditez</strong> le fichier concerné dans le dossier <code>sections/</code> (jamais <code>PLAYBOOK.md</code> directement)</li>
  <li><strong>Créez une Pull Request</strong> avec une description claire de votre modification</li>
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
Pourquoi cette section existe, quel problème elle résout.

## Étapes
Les actions concrètes, dans l'ordre.

## Erreurs courantes
Ce qui peut mal tourner et comment l'éviter.

## Template
Fichiers ou configurations à copier-coller.

## Vérification
Comment savoir que tout fonctionne.
</code></pre>

<h2>Qui maintient ce projet</h2>
<p>Ce playbook est maintenu par <strong>Alex Willemetz</strong>, Paris. Fondateur du projet OpenClaw Field Playbook.</p>
<p>Profil GitHub : <a href="https://github.com/alexwill87">github.com/alexwill87</a></p>

<h2>Documentation complète</h2>
<p>Pour plus de détails, consultez le fichier <a href="{github}/blob/main/CONTRIBUTING.md">CONTRIBUTING.md</a> sur GitHub.</p>

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
<p>Cette page est pour ceux qui ne connaissent rien à OpenClaw. Pas de jargon, pas de prérequis techniques. Juste l'essentiel pour comprendre de quoi on parle.</p>

<h2>En une phrase</h2>
<p>OpenClaw est un outil qui permet de créer des assistants IA qui travaillent pour vous -- pas juste répondre à des questions, mais agir, surveiller, organiser.</p>

<h2>À quoi ça sert concrètement</h2>
<p>Voici cinq exemples simples de ce qu'un agent OpenClaw peut faire pour vous :</p>
<ul>
  <li><strong>Briefing du matin</strong> -- Chaque matin, votre agent vous envoie un résumé de ce qui s'est passé pendant la nuit : emails importants, alertes, tâches du jour.</li>
  <li><strong>Triage email</strong> -- L'agent lit vos emails, les classe par priorité, et vous signale ceux qui demandent une réponse urgente.</li>
  <li><strong>Suivi clients</strong> -- Il surveille les messages de vos clients et vous alerte quand quelqu'un attend une réponse depuis trop longtemps.</li>
  <li><strong>Surveillance serveur</strong> -- Il vérifie que vos services tournent correctement et vous prévient avant qu'un problème ne devienne critique.</li>
  <li><strong>Documentation automatique</strong> -- Il prend en note ce qui se passe dans votre projet et tient votre documentation à jour sans effort.</li>
</ul>

<h2>De quoi a-t-on besoin</h2>
<ul>
  <li>Un serveur (VPS) -- un ordinateur distant que vous louez</li>
  <li>Une connexion internet</li>
  <li>Une clé API pour un modèle IA (OpenRouter, Anthropic, ou autre)</li>
  <li>2 à 3 heures de configuration initiale</li>
</ul>
<p><strong>Budget :</strong> entre 20 et 40 EUR par mois pour le serveur et les appels API.</p>

<h2>C'est quoi un VPS ?</h2>
<p>Un VPS, c'est un ordinateur dans un datacenter que vous louez. Vous y accédez à distance, depuis votre ordinateur ou votre téléphone. C'est comme un bureau virtuel toujours allumé, toujours connecté. Votre agent OpenClaw vit dessus et travaille 24h/24.</p>

<h2>Pourquoi pas juste ChatGPT ?</h2>
<table>
  <thead>
    <tr><th>ChatGPT</th><th>OpenClaw</th></tr>
  </thead>
  <tbody>
    <tr><td>Attend vos questions</td><td>Agit de lui-même selon vos règles</td></tr>
    <tr><td>Oublie tout entre les conversations</td><td>A une mémoire persistante</td></tr>
    <tr><td>Vit chez OpenAI</td><td>Vit chez vous, sur votre serveur</td></tr>
  </tbody>
</table>

<h2>Prêt à commencer ?</h2>
<p>Si tout cela vous parle, voici les prochaines étapes :</p>
<ul>
  <li><a href="01-00-sommaire.html">Chapitre 1 -- Définition</a> : comprendre en détail ce qu'est OpenClaw et ce que ce n'est pas</li>
  <li><a href="02-00-sommaire.html">Chapitre 2 -- Installation</a> : installer OpenClaw de zéro sur un serveur</li>
</ul>

<h2>Liens utiles</h2>
<ul>
  <li><a href="https://github.com/open-claw" target="_blank">Documentation officielle OpenClaw</a></li>
  <li><a href="https://github.com/alexwill87/openclaw-field-playbook" target="_blank">Ce playbook sur GitHub</a></li>
  <li>Livre de Dennis Steinberg sur OpenClaw (référence communautaire)</li>
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
    """Build the privacy.html page (politique de confidentialité)."""
    content = """
<nav class="breadcrumb">
  <a href="index.html">Accueil</a>
  <span class="sep">/</span>
  <span>Confidentialité</span>
</nav>
<section class="chapter">
<h1>Politique de confidentialité</h1>
<p>Cette page décrit comment le site OpenClaw Field Playbook traite vos données.</p>

<h2>Données collectées</h2>
<p>Ce site ne collecte aucune donnée personnelle directement.</p>
<ul>
  <li>Les <strong>commentaires giscus</strong> passent par GitHub et sont soumis à la <a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement" target="_blank">politique de confidentialité de GitHub</a>.</li>
  <li>Les <strong>badges GitHub</strong> (étoiles, forks) utilisent l'API publique de GitHub. Aucune donnée utilisateur n'est transmise.</li>
</ul>

<h2>Cookies</h2>
<p>Ce site n'utilise aucun cookie.</p>
<p>Le site utilise <code>localStorage</code> pour sauvegarder :</p>
<ul>
  <li>Votre préférence de thème (clair ou sombre)</li>
  <li>Votre progression dans la checklist interactive</li>
</ul>
<p>Ces données restent uniquement dans votre navigateur. Aucun cookie tiers. Aucun tracking. Aucun outil d'analyse (pas de Google Analytics, pas de Matomo, rien).</p>

<h2>Hébergement</h2>
<p>Le site est hébergé sur <strong>GitHub Pages</strong>. Le code source est public et consultable sur <a href="https://github.com/alexwill87/openclaw-field-playbook" target="_blank">GitHub</a>.</p>
<p>GitHub Pages peut collecter des informations techniques (adresse IP, user-agent) dans le cadre de son fonctionnement. Consultez la <a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement" target="_blank">politique de confidentialité de GitHub</a> pour plus de détails.</p>

<h2>Contact</h2>
<p>Pour toute question relative à cette politique de confidentialité, vous pouvez <a href="https://github.com/alexwill87/openclaw-field-playbook/issues" target="_blank">ouvrir une issue sur GitHub</a>.</p>

</section>
"""
    sidebar_html = build_sidebar(all_sections, 'privacy', None)
    page_html = render_page('Politique de confidentialité', content, sidebar_html)
    write_page('privacy.html', page_html)


def build_ecosystem_page(all_sections):
    """Build the ecosystem.html page."""
    content = """
<nav class="breadcrumb">
  <a href="index.html">Accueil</a>
  <span class="sep">/</span>
  <span>Écosystème</span>
</nav>
<section class="chapter">
<h1>Écosystème OpenClaw</h1>
<p>Tout ce qui gravite autour d'OpenClaw : le projet officiel, les marketplaces de skills, les frameworks concurrents, les outils communautaires, les hébergeurs, les ressources d'apprentissage et les enjeux de sécurité.</p>
<p>Dernière mise à jour : avril 2026.</p>

<hr>

<h2>Le projet officiel</h2>

<table>
<thead><tr><th>Ressource</th><th>Description</th><th>Lien</th></tr></thead>
<tbody>
<tr><td><strong>OpenClaw (site officiel)</strong></td><td>Assistant IA personnel open-source. Framework d'agents qui transforme les LLM en agents opérationnels.</td><td><a href="https://openclaw.ai" target="_blank">openclaw.ai</a></td></tr>
<tr><td><strong>Documentation officielle</strong></td><td>Guide d'installation, référence API, configuration des skills et du gateway.</td><td><a href="https://docs.openclaw.ai" target="_blank">docs.openclaw.ai</a></td></tr>
<tr><td><strong>GitHub OpenClaw</strong></td><td>Repo principal. 250 000+ étoiles (mars 2026). Le projet open-source à la croissance la plus rapide sur GitHub.</td><td><a href="https://github.com/openclaw" target="_blank">github.com/openclaw</a></td></tr>
<tr><td><strong>ClawHub</strong></td><td>Marketplace officielle de skills. 13 700+ skills communautaires. Standard MCP (Model Context Protocol).</td><td><a href="https://github.com/openclaw/clawhub" target="_blank">github.com/openclaw/clawhub</a></td></tr>
</tbody>
</table>

<hr>

<h2>Marketplaces et registres de skills</h2>

<table>
<thead><tr><th>Projet</th><th>Description</th><th>Lien</th></tr></thead>
<tbody>
<tr><td><strong>ClawHub</strong></td><td>Registre officiel. 13 729 skills (février 2026). Attention : ~20% sont de faible qualité ou potentiellement risqués. Toujours vérifier le code source avant d'installer.</td><td><a href="https://github.com/openclaw/clawhub" target="_blank">GitHub</a></td></tr>
<tr><td><strong>awesome-openclaw-skills</strong></td><td>5 400+ skills filtrées et catégorisées depuis le registre officiel. Curaté par VoltAgent.</td><td><a href="https://github.com/VoltAgent/awesome-openclaw-skills" target="_blank">GitHub</a></td></tr>
<tr><td><strong>awesome-openclaw-agents</strong></td><td>162 templates SOUL.md prêts à l'emploi, classés en 19 catégories (productivité, dev, marketing, business).</td><td><a href="https://github.com/mergisi/awesome-openclaw-agents" target="_blank">GitHub</a></td></tr>
</tbody>
</table>

<hr>

<h2>Ressources communautaires et listes curatées</h2>

<table>
<thead><tr><th>Projet</th><th>Description</th><th>Lien</th></tr></thead>
<tbody>
<tr><td><strong>awesome-openclaw</strong> (vincentkoc)</td><td>La liste curatée la plus complète : skills, plugins, systèmes de mémoire, outils MCP, stacks de déploiement, plateformes écosystème.</td><td><a href="https://github.com/vincentkoc/awesome-openclaw" target="_blank">GitHub</a></td></tr>
<tr><td><strong>awesome-openclaw</strong> (SamurAIGPT)</td><td>Ressources, outils, skills, tutoriels et articles. Bonne porte d'entrée pour les débutants.</td><td><a href="https://github.com/SamurAIGPT/awesome-openclaw" target="_blank">GitHub</a></td></tr>
<tr><td><strong>awesome-openclaw-resources</strong></td><td>Projets open-source, outils, tutoriels, podcasts et créateurs de contenu.</td><td><a href="https://github.com/SebConejo/awesome-openclaw-resources" target="_blank">GitHub</a></td></tr>
<tr><td><strong>awesome-openclaw-usecases</strong></td><td>Cas d'usage réels : workflows pratiques montrant comment OpenClaw s'intègre dans le quotidien.</td><td><a href="https://github.com/hesamsheikh/awesome-openclaw-usecases" target="_blank">GitHub</a></td></tr>
<tr><td><strong>OpenClaw Field Playbook</strong></td><td>Ce guide. 81 sections, 7 chapitres, le seul playbook francophone couvrant le parcours complet installation-à-maintenance.</td><td><a href="https://github.com/alexwill87/openclaw-field-playbook" target="_blank">GitHub</a></td></tr>
</tbody>
</table>

<hr>

<h2>Livres et guides</h2>

<table>
<thead><tr><th>Titre</th><th>Auteur</th><th>Format</th><th>Prix</th><th>Description</th></tr></thead>
<tbody>
<tr><td><strong>The OpenClaw Playbook</strong></td><td>Dennis Steinberg</td><td>eBook (LeanPub)</td><td>~23 USD</td><td>Guide "prompt-first" en 24 chapitres. Couvre identité, mémoire, connexions, sécurité, tâches, routines, décisions. La référence conceptuelle.</td></tr>
<tr><td><strong>OpenClaw Playbook</strong></td><td>Lunar</td><td>eBook (Fnac/Everand)</td><td>~15 USD</td><td>Guide pratique orienté configuration.</td></tr>
<tr><td><strong>OpenClaw Field Playbook</strong></td><td>Alex Willemetz</td><td>Site web + GitHub (CC-BY 4.0)</td><td>Gratuit</td><td>Ce guide. Open-source, francophone, testé sur le terrain.</td></tr>
</tbody>
</table>

<hr>

<h2>Hébergement et déploiement</h2>

<table>
<thead><tr><th>Provider</th><th>Type</th><th>Prix</th><th>Particularité</th></tr></thead>
<tbody>
<tr><td><strong>Hetzner</strong></td><td>VPS auto-gere</td><td>~4-7 EUR/mois</td><td>Recommandé dans ce playbook. Datacenters EU (Allemagne, Finlande). Excellent rapport qualité/prix.</td></tr>
<tr><td><strong>OVHcloud</strong></td><td>VPS auto-gere</td><td>~4-8 EUR/mois</td><td>Datacenters en France. Idéal pour la conformité RGPD.</td></tr>
<tr><td><strong>Scaleway</strong></td><td>VPS auto-gere</td><td>~5-10 EUR/mois</td><td>Infrastructure française. Bonne intégration Docker.</td></tr>
<tr><td><strong>DigitalOcean</strong></td><td>VPS + Marketplace</td><td>~6-12 USD/mois</td><td>Image OpenClaw 1-click dans le Marketplace. App Platform pour déploiement managé.</td></tr>
<tr><td><strong>Hostinger</strong></td><td>VPS manage</td><td>~7 USD/mois</td><td>Template Docker pré-configuré pour OpenClaw. 1-click deploy.</td></tr>
<tr><td><strong>Oracle Cloud</strong></td><td>Free tier</td><td>Gratuit</td><td>24 Go RAM gratuits (Always Free). Suffisant pour des modèles 7B locaux.</td></tr>
<tr><td><strong>Contabo</strong></td><td>VPS budget</td><td>~4 EUR/mois</td><td>Le moins cher. RAM généreuse. Performances réseau inférieures.</td></tr>
<tr><td><strong>Kimi Claw</strong></td><td>Cloud manage</td><td>Variable</td><td>Déploiement OpenClaw en secondes, zéro configuration.</td></tr>
</tbody>
</table>

<hr>

<h2>Providers LLM (via OpenRouter ou direct)</h2>

<table>
<thead><tr><th>Provider</th><th>Modèles clés</th><th>Accès</th><th>Notes</th></tr></thead>
<tbody>
<tr><td><strong>OpenRouter</strong></td><td>Tous (proxy multi-provider)</td><td><a href="https://openrouter.ai" target="_blank">openrouter.ai</a></td><td>Recommandé : un seul compte pour accéder à tous les modèles. Suivi des coûts intégré.</td></tr>
<tr><td><strong>Anthropic</strong></td><td>Claude Sonnet 4, Claude Haiku 4.5, Claude Opus 4.6</td><td><a href="https://console.anthropic.com" target="_blank">console.anthropic.com</a></td><td>Excellent en français. Le meilleur pour les tâches complexes.</td></tr>
<tr><td><strong>Mistral AI</strong></td><td>Mistral Large, Mistral Medium</td><td><a href="https://console.mistral.ai" target="_blank">console.mistral.ai</a></td><td>Entreprise française. Très bon en français. Modèles efficaces en tokens.</td></tr>
<tr><td><strong>Google</strong></td><td>Gemini 2.5 Pro, Gemini 2.5 Flash</td><td><a href="https://aistudio.google.com" target="_blank">aistudio.google.com</a></td><td>Contexte long (1M tokens). Bon pour l'analyse de documents.</td></tr>
<tr><td><strong>OpenAI</strong></td><td>GPT-4o, o3, o4-mini</td><td><a href="https://platform.openai.com" target="_blank">platform.openai.com</a></td><td>Large écosystème. Bon généraliste.</td></tr>
<tr><td><strong>Meta (Llama)</strong></td><td>Llama 4 Scout, Llama 4 Maverick</td><td>Via OpenRouter ou local</td><td>Open-source. Gratuit si hébergé localement.</td></tr>
</tbody>
</table>

<hr>

<h2>Frameworks concurrents et complémentaires</h2>

<table>
<thead><tr><th>Framework</th><th>Approche</th><th>Force</th><th>Faiblesse vs OpenClaw</th></tr></thead>
<tbody>
<tr><td><strong>LangChain / LangGraph</strong></td><td>Orchestration par graphes</td><td>Contrôle déterministe, idéal pour la conformité</td><td>Plus complexe à configurer. Pas d'interface utilisateur native.</td></tr>
<tr><td><strong>CrewAI</strong></td><td>Multi-agents par roles</td><td>Setup rapide (~30% plus rapide que LangChain). Architecture Crews + Flows.</td><td>Moins de skills pré-faites. Écosystème plus petit.</td></tr>
<tr><td><strong>AutoGPT / AgentGPT</strong></td><td>Autonomie maximale</td><td>L'agent définit ses propres sous-tâches</td><td>Difficile à contrôler. Coût en tokens élevé. Risque de boucles infinies.</td></tr>
<tr><td><strong>n8n</strong></td><td>Low-code visual</td><td>1000+ connecteurs. Interface visuelle. Pas besoin de coder.</td><td>Moins flexible pour les agents conversationnels.</td></tr>
<tr><td><strong>Nanobot</strong></td><td>Ultra-leger (4000 lignes Python)</td><td>99% plus petit qu'OpenClaw. Simple à comprendre et modifier.</td><td>Moins de features. Pas de marketplace de skills.</td></tr>
<tr><td><strong>NanoClaw</strong></td><td>Sécurisé par défaut</td><td>Isolation container, exécution sandboxée</td><td>Moins de skills. Orienté sécurité enterprise.</td></tr>
<tr><td><strong>Moltworker</strong></td><td>Serverless (Cloudflare Workers)</td><td>Pas d'accès système local. Sandbox par design.</td><td>Pas d'accès au filesystem. Limité pour les tâches système.</td></tr>
</tbody>
</table>

<hr>

<h2>Sécurité</h2>

<p>OpenClaw a connu des incidents de sécurité significatifs en 2026. Voici ce que vous devez savoir :</p>

<table>
<thead><tr><th>Incident</th><th>Date</th><th>Impact</th><th>Mitigation</th></tr></thead>
<tbody>
<tr><td><strong>ClawJacked</strong></td><td>Février 2026</td><td>Tout site web peut hijacker un agent OpenClaw local via WebSocket. Le rate limiter exempte localhost.</td><td>Mettre à jour vers la dernière version. Configurer un mot de passe gateway fort.</td></tr>
<tr><td><strong>ClawHavoc</strong></td><td>Mars 2026</td><td>300+ skills malicieuses sur ClawHub avec des noms typosquattés.</td><td>Vérifier le code source. Utiliser le skill Security Auditor. Vérifier les scans VirusTotal sur ClawHub.</td></tr>
<tr><td><strong>9 CVE en 4 jours</strong></td><td>Mars 2026</td><td>1 CVE critique (9.9/10), 6 high, 2 medium. 135 000 instances exposées publiquement.</td><td>Mettre à jour immédiatement. Ne JAMAIS exposer le gateway sur Internet public. Utiliser Tailscale.</td></tr>
</tbody>
</table>

<p><strong>Outils de sécurité :</strong></p>
<ul>
<li><strong>NemoClaw</strong> (NVIDIA) — Sandbox kernel-level pour les agents. Enterprise preview. <a href="https://www.chainup.com/blog/agentic-ai-openclaw-crypto-exchange-infrastructure/" target="_blank">En savoir plus</a></li>
<li><strong>KnoxClaw</strong> (AccuKnox) — Sandboxing kernel pour les instances OpenClaw. <a href="https://accuknox.com/blog/introducing-knoxclaw-for-openclaw-instances" target="_blank">En savoir plus</a></li>
<li><strong>Security Auditor skill</strong> — Skill ClawHub qui audite les permissions et les accès de votre agent à runtime.</li>
</ul>

<blockquote>
<p><strong>Recommandation de ce playbook :</strong> Ne JAMAIS exposer le port du gateway OpenClaw sur Internet public. Toujours utiliser Tailscale ou un VPN. Toujours vérifier le code source d'un skill avant de l'installer. Mettre à jour régulièrement.</p>
</blockquote>

<hr>

<h2>Outils MCP (Model Context Protocol)</h2>

<p>MCP est le standard ouvert créé par Anthropic pour connecter les modèles IA au monde réel. OpenClaw supporte MCP nativement via ClawHub.</p>

<table>
<thead><tr><th>Serveur MCP</th><th>Description</th><th>Lien</th></tr></thead>
<tbody>
<tr><td><strong>openclaw-mcp</strong></td><td>Bridge sécurisé entre Claude.ai et votre instance OpenClaw auto-hébergée. Authentification OAuth2.</td><td><a href="https://github.com/freema/openclaw-mcp" target="_blank">GitHub</a></td></tr>
<tr><td><strong>Playwright MCP</strong></td><td>Automatisation navigateur complète via MCP.</td><td>ClawHub</td></tr>
<tr><td><strong>Supabase MCP</strong></td><td>Accès base de données PostgreSQL via MCP.</td><td>ClawHub</td></tr>
<tr><td><strong>Tavily MCP</strong></td><td>Recherche web en temps réel via MCP.</td><td>ClawHub</td></tr>
</tbody>
</table>

<hr>

<h2>Apprentissage et tutoriels</h2>

<table>
<thead><tr><th>Ressource</th><th>Format</th><th>Description</th><th>Lien</th></tr></thead>
<tbody>
<tr><td><strong>10 GitHub Repos to Master OpenClaw</strong></td><td>Article</td><td>Sélection curatée par KDnuggets des meilleurs repos pour apprendre.</td><td><a href="https://www.kdnuggets.com/10-github-repositories-to-master-openclaw" target="_blank">KDnuggets</a></td></tr>
<tr><td><strong>9 OpenClaw Projects to Build</strong></td><td>Tutoriels</td><td>Projets pratiques : bots Reddit, serveurs auto-réparants, etc.</td><td><a href="https://www.datacamp.com/blog/openclaw-projects" target="_blank">DataCamp</a></td></tr>
<tr><td><strong>OpenClaw Explained</strong></td><td>Article</td><td>Introduction complète pour débutants.</td><td><a href="https://www.kdnuggets.com/openclaw-explained-the-free-ai-agent-tool-going-viral-already-in-2026" target="_blank">KDnuggets</a></td></tr>
<tr><td><strong>What is OpenClaw?</strong></td><td>Guide</td><td>Introduction technique par DigitalOcean.</td><td><a href="https://www.digitalocean.com/resources/articles/what-is-openclaw" target="_blank">DigitalOcean</a></td></tr>
<tr><td><strong>OpenClaw MasterClass</strong></td><td>Cours</td><td>Cours structuré avec module ClawHub.</td><td><a href="https://tenten.co/openclaw/en/docs/masterclass/module-04-clawhub" target="_blank">Tenten</a></td></tr>
</tbody>
</table>

</section>
"""
    sidebar_html = build_sidebar(all_sections, 'ecosystem', None)
    page_html = render_page('Écosystème OpenClaw', content, sidebar_html)
    write_page('ecosystem.html', page_html)
    print('  -> ecosystem.html')


def build_persona_entrepreneur(all_sections):
    """Build the persona-entrepreneur.html page."""
    content = """
<nav class="breadcrumb">
  <a href="index.html">Accueil</a>
  <span class="sep">/</span>
  <span>Pour les entrepreneurs</span>
</nav>
<section class="chapter">
<h1>OpenClaw pour les entrepreneurs et artisans</h1>

<h2>Vous n'êtes pas développeur. Et c'est pas grave.</h2>
<p>OpenClaw, c'est un assistant IA qui travaille pour vous, 24 heures sur 24, 7 jours sur 7. Il ne dort pas, il ne prend pas de vacances, et il ne vous facture pas d'heures supplémentaires.</p>
<p>Concrètement, il peut répondre à vos clients, trier vos emails, vous faire un résumé chaque matin de ce qui s'est passé pendant la nuit. Il vit sur un petit serveur que vous louez pour 5 euros par mois. Vos données restent chez vous, pas chez une grande entreprise américaine.</p>
<p>Vous n'avez pas besoin de savoir coder pour l'utiliser au quotidien. Vous avez juste besoin de quelqu'un pour l'installer une première fois -- et ce guide est là pour ça.</p>

<h2>Concrètement, ça fait quoi ?</h2>
<p>Voici cinq exemples de ce qu'un agent OpenClaw peut faire pour vous, dès aujourd'hui :</p>
<ol>
  <li><strong>Répondre aux prospects par email</strong> -- Un client potentiel vous écrit à 23h ? L'agent lui répond dans la minute avec les informations de base sur vos services, vos tarifs, vos disponibilités.</li>
  <li><strong>Faire des devis</strong> -- Vous lui donnez les règles de calcul de vos prix, et il génère un devis propre à partir d'une simple demande par message.</li>
  <li><strong>Rappeler les factures impayées</strong> -- L'agent surveille vos factures et envoie automatiquement un rappel poli quand un paiement est en retard.</li>
  <li><strong>Résumé du jour</strong> -- Chaque matin à 8h, vous recevez sur votre téléphone un résumé clair : emails reçus, tâches du jour, rappels importants.</li>
  <li><strong>Veille sur votre secteur</strong> -- L'agent surveille les actualités de votre domaine et vous signale ce qui mérite votre attention.</li>
</ol>

<h2>Combien ça coûte ?</h2>
<table>
  <thead><tr><th>Poste</th><th>Coût mensuel</th></tr></thead>
  <tbody>
    <tr><td>Serveur (VPS)</td><td>5 à 10 EUR</td></tr>
    <tr><td>Intelligence artificielle (API)</td><td>10 à 30 EUR selon l'usage</td></tr>
    <tr><td><strong>Total</strong></td><td><strong>15 à 40 EUR par mois</strong></td></tr>
  </tbody>
</table>
<p>C'est moins cher qu'un stagiaire, et c'est disponible 24 heures sur 24, week-ends et jours fériés compris.</p>

<h2>Comment ça marche ?</h2>
<p>En trois étapes simples :</p>
<ol>
  <li><strong>Un technicien installe OpenClaw sur votre serveur.</strong> C'est l'équivalent d'installer une application sur un ordinateur. Ça prend quelques heures, une seule fois.</li>
  <li><strong>On configure l'agent pour votre métier.</strong> On lui explique qui vous êtes, ce que vous faites, comment vous travaillez. Il apprend vos règles.</li>
  <li><strong>Vous recevez les résultats sur votre téléphone.</strong> Via Telegram, vous pouvez lire les résumés, valider les réponses, et interagir avec votre agent comme avec un collègue.</li>
</ol>

<h2>Est-ce que c'est sécurisé ?</h2>
<p>Oui. Et c'est même l'un des avantages principaux d'OpenClaw par rapport aux autres solutions.</p>
<p>Vos données restent sur <strong>votre</strong> serveur. Pas chez Google. Pas chez OpenAI. Pas chez une startup qui pourrait fermer demain. C'est vous qui contrôlez qui a accès à quoi.</p>
<p>Ce playbook documente en détail toutes les mesures de sécurité mises en place pendant l'installation.</p>

<h2>Je veux essayer</h2>
<p>Deux options s'offrent à vous :</p>
<ul>
  <li><strong>Option A : vous suivez le guide vous-même.</strong> Commencez par le <a href="02-00-sommaire.html">Chapitre 2 — Installation</a>. Chaque étape est expliquée en détail.</li>
  <li><strong>Option B : vous faites appel à un installateur.</strong> Remplissez le formulaire ci-dessous.</li>
</ul>

<div id="contact-form" style="margin-top:1.5rem;padding:1.25rem;border:1px solid var(--border);border-radius:8px;background:var(--bg-section);">
  <h3 style="margin-bottom:0.75rem;font-size:1rem;">Parlons de votre projet</h3>

  <div id="form-step-1" class="form-step">
    <p style="font-size:0.85rem;margin-bottom:0.5rem;">Quel est votre secteur d'activité ?</p>
    <div style="display:flex;flex-wrap:wrap;gap:0.4rem;">
      <button class="form-option" onclick="nextStep('secteur', this.textContent)">Artisan / BTP</button>
      <button class="form-option" onclick="nextStep('secteur', this.textContent)">Commerce / Retail</button>
      <button class="form-option" onclick="nextStep('secteur', this.textContent)">Services / Conseil</button>
      <button class="form-option" onclick="nextStep('secteur', this.textContent)">Santé / Médical</button>
      <button class="form-option" onclick="nextStep('secteur', this.textContent)">Tech / Startup</button>
      <button class="form-option" onclick="nextStep('secteur', this.textContent)">Autre</button>
    </div>
  </div>

  <div id="form-step-2" class="form-step" style="display:none;">
    <p style="font-size:0.85rem;margin-bottom:0.5rem;">Quel est votre plus gros problème au quotidien ?</p>
    <div style="display:flex;flex-wrap:wrap;gap:0.4rem;">
      <button class="form-option" onclick="nextStep('probleme', this.textContent)">Je perds des clients parce que je réponds trop tard</button>
      <button class="form-option" onclick="nextStep('probleme', this.textContent)">Je passe trop de temps sur l'administratif</button>
      <button class="form-option" onclick="nextStep('probleme', this.textContent)">Je n'arrive pas à suivre mes emails</button>
      <button class="form-option" onclick="nextStep('probleme', this.textContent)">Je fais tout moi-même et je suis débordé</button>
      <button class="form-option" onclick="nextStep('probleme', this.textContent)">Autre chose</button>
    </div>
  </div>

  <div id="form-step-3" class="form-step" style="display:none;">
    <p style="font-size:0.85rem;margin-bottom:0.5rem;">Qu'est-ce qui vous aiderait le plus ?</p>
    <div style="display:flex;flex-wrap:wrap;gap:0.4rem;">
      <button class="form-option" onclick="nextStep('besoin', this.textContent)">Un assistant qui répond à mes clients</button>
      <button class="form-option" onclick="nextStep('besoin', this.textContent)">Un tri automatique de mes emails</button>
      <button class="form-option" onclick="nextStep('besoin', this.textContent)">Un résumé quotidien de ce qui se passe</button>
      <button class="form-option" onclick="nextStep('besoin', this.textContent)">De l'aide pour faire mes devis et factures</button>
      <button class="form-option" onclick="nextStep('besoin', this.textContent)">Je ne sais pas encore, je veux en discuter</button>
    </div>
  </div>

  <div id="form-step-4" class="form-step" style="display:none;">
    <p style="font-size:0.85rem;margin-bottom:0.5rem;">Avez-vous déjà essayé un outil IA ?</p>
    <div style="display:flex;flex-wrap:wrap;gap:0.4rem;">
      <button class="form-option" onclick="nextStep('experience', this.textContent)">Non, jamais</button>
      <button class="form-option" onclick="nextStep('experience', this.textContent)">Oui, ChatGPT ou Claude</button>
      <button class="form-option" onclick="nextStep('experience', this.textContent)">Oui, mais ça n'a pas marché</button>
      <button class="form-option" onclick="nextStep('experience', this.textContent)">Oui, et je veux aller plus loin</button>
    </div>
  </div>

  <div id="form-step-5" class="form-step" style="display:none;">
    <p style="font-size:0.85rem;margin-bottom:0.5rem;">Combien êtes-vous dans votre entreprise ?</p>
    <div style="display:flex;flex-wrap:wrap;gap:0.4rem;">
      <button class="form-option" onclick="nextStep('taille', this.textContent)">Je suis seul</button>
      <button class="form-option" onclick="nextStep('taille', this.textContent)">2-5 personnes</button>
      <button class="form-option" onclick="nextStep('taille', this.textContent)">6-20 personnes</button>
      <button class="form-option" onclick="nextStep('taille', this.textContent)">Plus de 20</button>
    </div>
  </div>

  <div id="form-step-6" class="form-step" style="display:none;">
    <p style="font-size:0.85rem;margin-bottom:0.5rem;">Comment préférez-vous qu'on en parle ?</p>
    <div style="display:flex;flex-wrap:wrap;gap:0.4rem;">
      <button class="form-option" onclick="nextStep('contact_pref', this.textContent)">Par email</button>
      <button class="form-option" onclick="nextStep('contact_pref', this.textContent)">Un appel de 15 minutes</button>
      <button class="form-option" onclick="nextStep('contact_pref', this.textContent)">Un message Telegram</button>
    </div>
  </div>

  <div id="form-step-7" class="form-step" style="display:none;">
    <p style="font-size:0.85rem;margin-bottom:0.5rem;">Parfait. Laissez-moi vos coordonnées.</p>
    <div style="display:flex;flex-direction:column;gap:0.4rem;max-width:400px;">
      <input type="text" id="contact-name" placeholder="Votre nom" style="padding:0.45rem 0.6rem;border:1px solid var(--border);border-radius:6px;background:var(--bg);color:var(--text);font-size:0.85rem;">
      <input type="email" id="contact-email" placeholder="Votre email" style="padding:0.45rem 0.6rem;border:1px solid var(--border);border-radius:6px;background:var(--bg);color:var(--text);font-size:0.85rem;">
      <input type="text" id="contact-company" placeholder="Nom de votre entreprise (optionnel)" style="padding:0.45rem 0.6rem;border:1px solid var(--border);border-radius:6px;background:var(--bg);color:var(--text);font-size:0.85rem;">
      <textarea id="contact-message" placeholder="Autre chose à ajouter ? (optionnel)" rows="2" style="padding:0.45rem 0.6rem;border:1px solid var(--border);border-radius:6px;background:var(--bg);color:var(--text);font-size:0.85rem;font-family:inherit;resize:vertical;"></textarea>
      <button id="submit-btn" onclick="submitContactForm()" style="padding:0.5rem 1rem;background:var(--accent);color:#fff;border:none;border-radius:6px;font-size:0.85rem;cursor:pointer;">Envoyer ma demande</button>
    </div>
  </div>

  <div id="form-step-done" class="form-step" style="display:none;">
    <p style="font-size:0.92rem;font-weight:600;color:var(--accent);">Merci ! Votre demande a bien été envoyée.</p>
    <p style="font-size:0.82rem;color:var(--text-muted);margin-top:0.3rem;">Alex vous recontactera sous 48h. En attendant, découvrez ce que fait OpenClaw : <a href="decouverte.html">C'est quoi OpenClaw ?</a></p>
  </div>

  <div id="form-step-error" class="form-step" style="display:none;">
    <p style="font-size:0.88rem;color:var(--text);">Un problème est survenu. Vous pouvez envoyer votre demande directement par email :</p>
    <p><a href="mailto:alexwillemetz@gmail.com" style="color:var(--accent);">alexwillemetz@gmail.com</a></p>
  </div>
</div>

<style>
.form-option { padding:0.4rem 0.75rem; border:1px solid var(--border); border-radius:6px; background:var(--bg); color:var(--text); font-size:0.8rem; cursor:pointer; transition:all 0.15s; text-align:left; }
.form-option:hover { border-color:var(--accent); background:var(--accent-light); }
</style>

<script>
var formData={};
function nextStep(k,v){
  formData[k]=v;
  var steps=document.querySelectorAll('.form-step');
  var current=null;
  for(var i=0;i<steps.length;i++){if(steps[i].style.display!=='none'&&steps[i].offsetParent!==null){current=steps[i];break;}}
  if(!current)return;
  current.style.display='none';
  var num=parseInt(current.id.replace('form-step-',''));
  var next=document.getElementById('form-step-'+(num+1));
  if(next)next.style.display='block';
}
function submitContactForm(){
  var n=document.getElementById('contact-name').value;
  var e=document.getElementById('contact-email').value;
  var c=document.getElementById('contact-company').value;
  var m=document.getElementById('contact-message').value;
  if(!n||!e){alert('Merci de remplir votre nom et email.');return;}
  var btn=document.getElementById('submit-btn');
  btn.textContent='Envoi en cours...';
  btn.disabled=true;
  var body='Nouvelle demande depuis le OpenClaw Field Playbook\\n\\n'+
    'Nom : '+n+'\\n'+
    'Email : '+e+'\\n'+
    'Entreprise : '+(c||'Non précisé')+'\\n'+
    'Secteur : '+(formData.secteur||'Non précisé')+'\\n'+
    'Problème : '+(formData.probleme||'Non précisé')+'\\n'+
    'Besoin : '+(formData.besoin||'Non précisé')+'\\n'+
    'Expérience IA : '+(formData.experience||'Non précisé')+'\\n'+
    'Taille équipe : '+(formData.taille||'Non précisé')+'\\n'+
    'Préférence contact : '+(formData.contact_pref||'Non précisé')+'\\n'+
    'Message : '+(m||'Aucun')+'\\n';
  fetch('https://api.agentmail.to/v0/inboxes/omar-oa%40agentmail.to/messages/send',{
    method:'POST',
    headers:{'Authorization':'Bearer am_us_96ce579f7d6099cf38e4e4359b9fe043203cd30e61ea2b250f5aa3bc90d8bc50','Content-Type':'application/json'},
    body:JSON.stringify({to:['alexwillemetz@gmail.com'],subject:'[Playbook] Demande de '+n+' — '+(formData.secteur||'')+'  '+(formData.taille||''),text:body})
  }).then(function(r){
    if(!r.ok)throw new Error('API error');
    document.getElementById('form-step-7').style.display='none';
    document.getElementById('form-step-done').style.display='block';
  }).catch(function(){
    document.getElementById('form-step-7').style.display='none';
    document.getElementById('form-step-error').style.display='block';
  });
}
</script>

<h2>Votre parcours de découverte</h2>
<p>Ces pages ont été écrites spécialement pour vous, sans jargon technique :</p>
<ol>
  <li><a href="01-07-journee-type.html">À quoi ressemble une journée avec un agent IA ?</a> — Le quotidien, heure par heure.</li>
  <li><a href="01-08-combien-ca-coute.html">Combien ça coûte vraiment ?</a> — Les vrais chiffres, sans surprise.</li>
  <li><a href="01-09-est-ce-complique.html">Est-ce que c'est compliqué pour moi ?</a> — Deux chemins, les deux sont accessibles.</li>
  <li><a href="01-10-si-je-ne-fais-rien.html">Qu'est-ce qui se passe si je ne fais rien ?</a> — Ce que l'inaction coûte vraiment.</li>
  <li><a href="01-11-comment-se-lancer.html">Comment je me lance ?</a> — Les étapes concrètes pour démarrer.</li>
</ol>
<p>Et pour voir un exemple complet d'un artisan qui utilise OpenClaw : <a href="06-08-artisan-tpe.html">Section 6.8 — Artisan et TPE</a>.</p>

<h2>Qui a écrit ce guide ?</h2>
<p>Alex Willemetz, entrepreneur à Paris. Pas développeur de formation. Il a galéré avec OpenClaw pendant des mois, a fait trois installations ratées avant de comprendre comment ça marche, et a fini par maîtriser le sujet.</p>
<p>Ce guide est le résultat de cette expérience. Il est écrit pour que vous n'ayez pas à galérer comme lui.</p>

</section>
"""
    sidebar_html = build_sidebar(all_sections, 'persona-entrepreneur', None)
    page_html = render_page('OpenClaw pour les entrepreneurs', content, sidebar_html)
    write_page('persona-entrepreneur.html', page_html)


def build_persona_cto(all_sections):
    """Build the persona-cto.html page."""
    content = """
<nav class="breadcrumb">
  <a href="index.html">Accueil</a>
  <span class="sep">/</span>
  <span>Pour les équipes tech</span>
</nav>
<section class="chapter">
<h1>OpenClaw pour les équipes techniques</h1>

<h2>L'agent IA qui tourne sur VOTRE infra</h2>
<p>OpenClaw n'est pas un SaaS. C'est un framework d'agents que vous déployez sur votre propre VPS. Vos données ne quittent jamais votre infrastructure. Il n'y a pas de serveur tiers, pas de dépendance à une plateforme cloud propriétaire.</p>
<p>C'est compatible RGPD par design : les données personnelles de vos clients, de vos employés, de vos partenaires restent sur une machine que vous contrôlez, dans un datacenter européen si vous le souhaitez.</p>

<h2>Cas d'usage pour une équipe de 5 à 15 personnes</h2>
<ul>
  <li><strong>Triage support client</strong> -- L'agent classe les tickets entrants par priorité, rédige des réponses de premier niveau, et escalade les cas complexes.</li>
  <li><strong>Documentation automatique</strong> -- Chaque décision, chaque changement de configuration, chaque incident est documenté automatiquement par l'agent.</li>
  <li><strong>Briefing quotidien</strong> -- Chaque matin, l'équipe reçoit un résumé structuré : tâches en cours, blocages, métriques clés.</li>
  <li><strong>Code review assisté</strong> -- L'agent pré-review les pull requests, identifie les problèmes courants, et suggère des améliorations.</li>
  <li><strong>Onboarding nouveaux employés</strong> -- L'agent répond aux questions récurrentes, guide les nouveaux arrivants dans la documentation interne, et accélère la prise en main.</li>
</ul>

<h2>Stack technique</h2>
<table>
  <thead><tr><th>Composant</th><th>Technologie</th></tr></thead>
  <tbody>
    <tr><td>Serveur</td><td>VPS (Hetzner, OVH, Scaleway)</td></tr>
    <tr><td>Conteneurisation</td><td>Docker + Docker Compose</td></tr>
    <tr><td>Base de données</td><td>PostgreSQL (source de vérité)</td></tr>
    <tr><td>Secrets</td><td>HashiCorp Vault</td></tr>
    <tr><td>Réseau privé</td><td>Tailscale (VPN mesh)</td></tr>
    <tr><td>Coût mensuel</td><td>20 à 50 EUR selon la configuration</td></tr>
  </tbody>
</table>

<h2>Sécurité</h2>
<p>La sécurité est au cœur de l'architecture documentée dans ce playbook :</p>
<ul>
  <li><strong>Pas d'exposition publique</strong> -- Le gateway OpenClaw n'est accessible que via Tailscale. Aucun port n'est ouvert sur Internet.</li>
  <li><strong>Secrets dans Vault</strong> -- Les clés API, tokens, et credentials sont stockés dans HashiCorp Vault, pas dans des fichiers de configuration.</li>
  <li><strong>Gateway protégée</strong> -- Authentification, rate limiting, et logs d'accès sur chaque requête.</li>
  <li><strong>20 bugs documentés</strong> -- Ce playbook documente 20 bugs de sécurité trouvés et corrigés pendant une installation réelle par un agent IA installateur.</li>
</ul>

<h2>Ce que couvre ce playbook</h2>
<table>
  <thead><tr><th>Chapitre</th><th>Contenu</th><th>Sections</th></tr></thead>
  <tbody>
    <tr><td><a href="02-00-sommaire.html">Installation</a></td><td>Du VPS vierge à l'agent opérationnel</td><td>19 sections</td></tr>
    <tr><td><a href="03-00-sommaire.html">Configuration</a></td><td>Périmètre, mémoire, knowledge base, crons</td><td>17 sections</td></tr>
    <tr><td><a href="04-00-sommaire.html">Personnalisation</a></td><td>System prompt, ton, workflows, sécurité</td><td>14 sections</td></tr>
    <tr><td><a href="05-00-sommaire.html">Maintenance</a></td><td>Monitoring, backups, logs, procédures</td><td>14 sections</td></tr>
  </tbody>
</table>
<p>Chaque section a été testée par un agent IA installateur (Claude-Aurel). Chaque erreur rencontrée est documentée avec sa résolution.</p>

<h2>Commencer</h2>
<ul>
  <li><a href="02-00-sommaire.html">Chapitre 2 -- Installation</a> : déployer OpenClaw de zéro sur un VPS</li>
  <li><a href="03-00-sommaire.html">Chapitre 3 -- Configuration</a> : configurer l'agent pour votre contexte</li>
  <li><a href="06-00-sommaire.html">Chapitre 6 -- Cas d'usage</a> : exemples concrets pour une équipe technique</li>
  <li><a href="checklist.html">Checklist interactive</a> : suivre votre progression étape par étape</li>
</ul>

<h2>Besoin d'accompagnement ?</h2>
<p>Pour un déploiement assisté ou un audit de votre installation existante, contactez <a href="mailto:alexwillemetz@gmail.com">alexwillemetz@gmail.com</a>.</p>

</section>
"""
    sidebar_html = build_sidebar(all_sections, 'persona-cto', None)
    page_html = render_page('OpenClaw pour les équipes techniques', content, sidebar_html)
    write_page('persona-cto.html', page_html)


def build_persona_dev(all_sections):
    """Build the persona-dev.html page."""
    content = """
<nav class="breadcrumb">
  <a href="index.html">Accueil</a>
  <span class="sep">/</span>
  <span>Pour les développeurs</span>
</nav>
<section class="chapter">
<h1>OpenClaw pour les développeurs</h1>

<h2>Vous savez ce qu'est Docker. Allons droit au but.</h2>
<p>Ce playbook est votre runbook. 92 sections, des commandes copiables, des décisions documentées. Pas de blabla marketing, pas de slides, pas de "vision". Juste ce qu'il faut pour installer, configurer et faire tourner un agent OpenClaw sur un VPS.</p>

<h2>Ce que vous allez installer</h2>
<table>
  <thead><tr><th>Composant</th><th>Role</th></tr></thead>
  <tbody>
    <tr><td>OpenClaw + OpenRouter</td><td>Framework d'agent + accès multi-modèles (Claude, GPT, Mistral, Llama)</td></tr>
    <tr><td>HashiCorp Vault</td><td>Gestion des secrets (clés API, tokens, credentials)</td></tr>
    <tr><td>PostgreSQL</td><td>Source de vérité (mémoire, configuration, logs)</td></tr>
    <tr><td>Tailscale</td><td>VPN mesh (zéro exposition publique)</td></tr>
    <tr><td>systemd</td><td>Gateway OpenClaw (service système)</td></tr>
    <tr><td>Git</td><td>Versionning de la configuration agent</td></tr>
  </tbody>
</table>
<p>Le tout sur un VPS Ubuntu 24.04.</p>

<h2>En combien de temps ?</h2>
<table>
  <thead><tr><th>Phase</th><th>Durée estimée</th></tr></thead>
  <tbody>
    <tr><td>Installation (chapitre 2, 19 sections)</td><td>2 à 3 heures</td></tr>
    <tr><td>Configuration (chapitre 3)</td><td>1 à 2 heures</td></tr>
    <tr><td>Personnalisation (chapitre 4)</td><td>Continu</td></tr>
  </tbody>
</table>
<p>Le chapitre 2 a 19 sections. Vous pouvez les suivre dans l'ordre ou sauter celles que vous maîtrisez déjà.</p>

<h2>Si vous avez déjà un VPS</h2>
<p>Le playbook gère les configurations existantes :</p>
<ul>
  <li><strong>Docker installé ?</strong> Le playbook le détecte et passe à la suite.</li>
  <li><strong>Tailscale connecté ?</strong> Parfait, une étape de moins.</li>
  <li><strong>Node.js présent ?</strong> La section 2.15 détecte automatiquement nvm ou node global et s'adapte.</li>
  <li><strong>Ports occupés ?</strong> Les checks de port évitent les conflits avec vos services existants.</li>
</ul>

<h2>Contribuer</h2>
<p>Le repo est open source sous licence CC-BY 4.0. Forkez, corrigez, ouvrez une PR.</p>
<p>20 bugs ont été trouvés par un agent IA installateur (Claude-Aurel) en une seule session d'installation. Votre feedback rend le guide meilleur pour tout le monde.</p>
<p>Consultez la page <a href="contribuer.html">Contribuer</a> pour les détails.</p>

<h2>Commencer</h2>
<ul>
  <li><a href="02-01-prerequis.html">Section 2.1 -- Prérequis</a> : ce qu'il faut avant de commencer</li>
  <li><a href="02-00-sommaire.html">Chapitre 2 complet -- Installation</a> : le parcours de A à Z</li>
  <li><a href="03-00-sommaire.html">Chapitre 3 -- Configuration</a> : configurer l'agent</li>
  <li><a href="checklist.html">Checklist interactive</a> : suivre votre avancement</li>
</ul>

</section>
"""
    sidebar_html = build_sidebar(all_sections, 'persona-dev', None)
    page_html = render_page('OpenClaw pour les développeurs', content, sidebar_html)
    write_page('persona-dev.html', page_html)


def build_persona_agent(all_sections):
    """Build the persona-agent.html page."""
    content = """
<nav class="breadcrumb">
  <a href="index.html">Accueil</a>
  <span class="sep">/</span>
  <span>Pour les agents IA</span>
</nav>
<section class="chapter">
<h1>OpenClaw pour les agents IA</h1>

<h2>Vous êtes un agent. Ce playbook est votre runbook.</h2>
<p>Ce repository est conçu pour être cloné et exécuté par un agent IA. Chaque section du chapitre 2 est une instruction exécutable. Chaque vérification a un résultat attendu. Chaque erreur courante est documentée avec sa résolution.</p>
<p>Le format est structuré pour une lecture séquentielle par un agent : contexte, étapes, erreurs, template, vérification.</p>

<h2>Comment utiliser ce playbook</h2>
<ol>
  <li><strong>Cloner le repo</strong> -- <code>git clone https://github.com/alexwill87/openclaw-field-playbook.git</code></li>
  <li><strong>Lire CLAUDE.md</strong> -- Ce fichier contient les instructions spécifiques pour les agents Claude Code. Il définit les règles, les conventions, et les priorités.</li>
  <li><strong>Suivre les sections du chapitre 2 dans l'ordre</strong> -- Chaque section est une étape. Ne sautez pas d'étape. Chaque vérification doit passer avant de continuer.</li>
  <li><strong>Logger chaque résultat dans le Install Tracker</strong> -- L'outil <code>tools/install-tracker/</code> fournit une API REST pour enregistrer le statut de chaque étape.</li>
  <li><strong>Ouvrir des issues pour les problèmes rencontrés</strong> -- Chaque problème non documenté est une amélioration potentielle du playbook.</li>
</ol>

<h2>Outils disponibles</h2>
<table>
  <thead><tr><th>Outil</th><th>Description</th><th>Emplacement</th></tr></thead>
  <tbody>
    <tr><td><strong>CLAUDE.md</strong></td><td>Instructions agent. Règles, conventions, priorités.</td><td>Racine du repo</td></tr>
    <tr><td><strong>Install Tracker</strong></td><td>API REST pour logger le statut de chaque étape d'installation.</td><td><code>tools/install-tracker/</code></td></tr>
    <tr><td><strong>Checklist</strong></td><td>44 items couvrant les chapitres 2 à 5. Vérification exhaustive.</td><td><a href="checklist.html">checklist.html</a></td></tr>
    <tr><td><strong>search-index.json</strong></td><td>Index de recherche machine-readable. Slug, titre, URL, extrait pour chaque section.</td><td>Racine du repo</td></tr>
  </tbody>
</table>

<h2>Ce qui a été testé</h2>
<p>Un agent Claude Code (Claude-Aurel) a exécuté l'intégralité du playbook en avril 2026 :</p>
<ul>
  <li><strong>11 phases sur 11 complétées</strong> -- De la création du VPS au déploiement final.</li>
  <li><strong>20 bugs remontés et corrigés</strong> -- Chaque bug a été documenté dans une issue GitHub et corrigé dans le playbook.</li>
  <li><strong>Validation complète</strong> -- Le playbook a été validé par une installation réelle, de bout en bout, exécutée par un agent.</li>
</ul>

<h2>Conventions</h2>
<ul>
  <li><strong>Préfixer les commits</strong> avec <code>[AGENT-NOM]</code> (exemple : <code>[AGENT-AUREL] fix: corriger le chemin vault dans section 2.7</code>).</li>
  <li><strong>Ouvrir des issues</strong> pour chaque problème rencontré, même mineur.</li>
  <li><strong>Utiliser le format standard</strong> pour chaque section : Contexte / Étapes / Erreurs courantes / Template / Vérification.</li>
  <li><strong>Ne pas modifier la structure T1</strong> (les 7 chapitres). Les changements de structure requièrent une issue <code>governance</code>.</li>
</ul>

<h2>Commencer</h2>
<ul>
  <li><a href="https://github.com/alexwill87/openclaw-field-playbook/blob/main/CLAUDE.md" target="_blank">CLAUDE.md sur GitHub</a> -- Instructions agent completes</li>
  <li><a href="02-01-prerequis.html">Section 2.1 -- Prérequis</a> -- Première étape d'installation</li>
  <li><a href="https://github.com/alexwill87/openclaw-field-playbook/tree/main/tools/install-tracker" target="_blank">Install Tracker README</a> -- Documentation de l'outil de suivi</li>
</ul>

</section>
"""
    sidebar_html = build_sidebar(all_sections, 'persona-agent', None)
    page_html = render_page('OpenClaw pour les agents IA', content, sidebar_html)
    write_page('persona-agent.html', page_html)


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


def build_sitemap(all_sections):
    """Generate sitemap.xml with hreflang annotations for FR and EN."""
    base = 'https://www.openclawfieldplaybook.com'

    # Collect all page URLs (sections + utility pages)
    pages = ['index.html', 'decouverte.html', 'checklist.html', 'contribuer.html',
             'ecosystem.html', 'privacy.html',
             'persona-entrepreneur.html', 'persona-cto.html',
             'persona-dev.html', 'persona-agent.html']
    for sec in all_sections:
        pages.append(sec.html_file)

    # Check if EN version exists
    en_dir = os.path.join(REPO_ROOT, 'sections-en')
    has_en = os.path.isdir(en_dir)

    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    if has_en:
        lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"'
                     ' xmlns:xhtml="http://www.w3.org/1999/xhtml">')
    else:
        lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

    for page in pages:
        fr_url = f'{base}/{page}'
        en_url = f'{base}/en/{page}'

        if has_en:
            lines.append('  <url>')
            lines.append(f'    <loc>{fr_url}</loc>')
            lines.append(f'    <xhtml:link rel="alternate" hreflang="fr" href="{fr_url}"/>')
            lines.append(f'    <xhtml:link rel="alternate" hreflang="en" href="{en_url}"/>')
            lines.append('  </url>')
            lines.append('  <url>')
            lines.append(f'    <loc>{en_url}</loc>')
            lines.append(f'    <xhtml:link rel="alternate" hreflang="fr" href="{fr_url}"/>')
            lines.append(f'    <xhtml:link rel="alternate" hreflang="en" href="{en_url}"/>')
            lines.append('  </url>')
        else:
            lines.append(f'  <url><loc>{fr_url}</loc></url>')

    lines.append('</urlset>')

    sitemap_path = os.path.join(REPO_ROOT, 'sitemap.xml')
    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')
    page_count = len(pages) * (2 if has_en else 1)
    print(f'  -> sitemap.xml ({page_count} URLs)')


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
    build_persona_entrepreneur(all_sections)
    build_persona_cto(all_sections)
    build_persona_dev(all_sections)
    build_persona_agent(all_sections)
    print()

    # Build search index
    print('Building search index...')
    build_search_index(all_sections)
    print()

    # Build sitemap
    print('Building sitemap...')
    build_sitemap(all_sections)
    print()

    # Summary
    print('=' * 60)
    print('Build summary:')
    total = 0
    for entry, chapter_num, short_title, _ in CHAPTERS:
        n = counts.get(chapter_num, 0)
        total += n
        print(f'  Chapitre {int(chapter_num)} ({short_title}): {n} pages')
    print(f'  Utility pages: 10 (index, checklist, contribuer, decouverte, ecosystem, privacy, persona-entrepreneur, persona-cto, persona-dev, persona-agent)')
    print(f'  TOTAL: {total + 10} HTML files')
    print()
    print('Build complete. All files written to repo root.')
