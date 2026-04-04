#!/usr/bin/env python3
"""
Build the English version of the OpenClaw Field Playbook.

This script reuses the French build engine (build_site.py) but overrides:
- Source directory: sections-en/ instead of sections/
- Output directory: en/ instead of repo root
- Template: index_template_en.html
- All UI strings: French → English
- Search index: en/search-index.json
- Giscus: same repo, pathname-based (separate threads per language)

Usage:
  python3 build_en.py
"""

import os
import sys
import re
import json
import importlib.util

# Import the FR build script as a module
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.normpath(os.path.join(SCRIPT_DIR, '..', '..'))

spec = importlib.util.spec_from_file_location('build_site', os.path.join(SCRIPT_DIR, 'build_site.py'))
fr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fr)

# ---------------------------------------------------------------------------
# Override paths
# ---------------------------------------------------------------------------

EN_SECTIONS_DIR = os.path.join(REPO_ROOT, 'sections-en')
EN_OUTPUT_DIR = os.path.join(REPO_ROOT, 'en')
EN_TEMPLATE_PATH = os.path.join(REPO_ROOT, 'index_template_en.html')

# ---------------------------------------------------------------------------
# i18n strings
# ---------------------------------------------------------------------------

I18N = {
    # Sidebar
    'Accueil': 'Home',
    'Avant-propos': 'Introduction',
    "C'est quoi OpenClaw ?": 'What is OpenClaw?',
    'Focus Entrepreneurs': 'For Entrepreneurs',
    'Focus Équipes tech': 'For Tech Teams',
    'Focus Développeurs': 'For Developers',
    'Focus Agents IA': 'For AI Agents',
    'Découvrir': 'Discover',
    'Déployer': 'Deploy',
    'Opérer': 'Operate',
    'Ressources': 'Resources',
    'Écosystème': 'Ecosystem',
    'Checklist': 'Checklist',
    'Contribuer': 'Contribute',
    'Confidentialité': 'Privacy',

    # Chapter short titles
    'Guide de lecture': 'Reading Guide',
    'Définition': 'Definition',
    'Installation': 'Installation',
    'Configuration': 'Configuration',
    'Personnalisation': 'Customization',
    'Maintenance': 'Maintenance',
    "Cas d'usage": 'Use Cases',
    'Localisation': 'Localization',

    # Chapter descriptions
    "Comment lire ce guide et par où commencer": "How to read this guide and where to start",
    "Ce qu'est OpenClaw, ce que ce n'est pas": "What OpenClaw is and what it isn't",
    "Installer OpenClaw de zéro sur un VPS": "Install OpenClaw from scratch on a VPS",
    "Configurer l'agent pour son contexte": "Configure the agent for your context",
    "Adapter le comportement, le ton, les workflows": "Adapt behavior, tone, and workflows",
    "Garder l'agent fiable dans le temps": "Keep the agent reliable over time",
    "Exemples concrets par type d'organisation": "Real examples by organization type",
    "Adapter OpenClaw à d'autres langues et contextes": "Adapt OpenClaw to other languages and contexts",

    # Page elements
    'Sur cette page': 'On this page',
    'Ce que vous allez apprendre': 'What you will learn',
    'Bravo, vous avez terminé cette section !': 'Well done, you completed this section!',
    'Vous avez couvert :': 'You covered:',
    'Continuer': 'Continue',
    'Proposer une modification sur GitHub': 'Suggest an edit on GitHub',
    'Commentaires et discussions': 'Comments and discussions',
    'Dernière mise à jour :': 'Last updated:',

    # Breadcrumb
    'Accueil': 'Home',

    # Footer
    'Publie sous': 'Published under',
    'par': 'by',
    'Code source': 'Source code',
    'Signaler un probleme': 'Report an issue',

    # Month names
    'janvier': 'January', 'février': 'February', 'mars': 'March',
    'avril': 'April', 'mai': 'May', 'juin': 'June',
    'juillet': 'July', 'août': 'August', 'septembre': 'September',
    'octobre': 'October', 'novembre': 'November', 'décembre': 'December',

    # Learning objectives
    'et': 'and',
    'autre': 'more',
    'autres': 'more',
}


def translate_ui(text):
    """Translate a UI string from French to English."""
    if text in I18N:
        return I18N[text]
    return text


# ---------------------------------------------------------------------------
# Override build functions
# ---------------------------------------------------------------------------

def build_en_section_registry():
    """Build section registry from sections-en/ directory."""
    if not os.path.isdir(EN_SECTIONS_DIR):
        print(f'ERROR: {EN_SECTIONS_DIR} not found. Run translate.py first.')
        sys.exit(1)

    # Temporarily override the SECTIONS_DIR in the fr module
    original_dir = fr.SECTIONS_DIR
    fr.SECTIONS_DIR = EN_SECTIONS_DIR
    all_sections = fr.build_section_registry()
    fr.SECTIONS_DIR = original_dir

    return all_sections


def read_en_template():
    """Read the English HTML template."""
    if os.path.exists(EN_TEMPLATE_PATH):
        with open(EN_TEMPLATE_PATH, 'r', encoding='utf-8') as f:
            return f.read()
    # Fallback: use FR template with lang="en"
    template = fr.read_template()
    template = template.replace('lang="fr"', 'lang="en"')
    return template


def en_render_page(title, content_html, sidebar_html):
    """Render page using English template."""
    template = read_en_template()
    html = template.replace('<!-- TITLE_PLACEHOLDER -->', title)
    html = template.replace('<!-- TITLE_PLACEHOLDER -->', title)
    html = html.replace('<!-- NAVIGATION_PLACEHOLDER -->', sidebar_html)
    html = html.replace('<!-- CONTENT_PLACEHOLDER -->', content_html)
    return html


def en_write_page(filename, html):
    """Write an HTML file to the en/ output directory."""
    os.makedirs(EN_OUTPUT_DIR, exist_ok=True)
    path = os.path.join(EN_OUTPUT_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'  -> en/{filename}')


def build_en_sidebar(all_sections, active_slug, active_chapter):
    """Build English sidebar navigation."""
    items = []

    active_cls = ' class="active"' if active_slug == 'index' else ''
    items.append(f'<a href="index.html" class="nav-home"{active_cls}>Home</a>')

    chapters_order = []
    chapters_map = {}
    for sec in all_sections:
        if sec.chapter_num not in chapters_map:
            chapters_order.append(sec.chapter_num)
            chapters_map[sec.chapter_num] = []
        chapters_map[sec.chapter_num].append(sec)

    def render_chapter(ch_num):
        ch_sections = chapters_map.get(ch_num, [])
        if not ch_sections:
            return
        sommaire = ch_sections[0]
        sub_sections = ch_sections[1:]

        # Translate sidebar title
        sidebar_title = translate_ui(sommaire.sidebar_title)
        # Handle numbered titles like "1. Définition"
        for fr_title, en_title in I18N.items():
            if fr_title in sidebar_title:
                sidebar_title = sidebar_title.replace(fr_title, en_title)

        if ch_num == '00':
            active_cls = ' class="active"' if active_slug == sommaire.slug else ''
            items.append(f'<div class="nav-chapter">')
            items.append(f'  <a href="{sommaire.html_file}" class="nav-chapter-title"{active_cls}>{sidebar_title}</a>')
            items.append(f'</div>')
            return

        is_open = (active_chapter == ch_num)
        items.append(f'<div class="nav-chapter{"  open" if is_open else ""}">')
        active_cls = ' class="active"' if active_slug == sommaire.slug else ''
        items.append(f'  <a href="{sommaire.html_file}" class="nav-chapter-title"{active_cls}>{sidebar_title}</a>')

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

    # --- INTRODUCTION ---
    items.append('<div class="nav-group-label">Introduction</div>')
    render_util('decouverte', 'decouverte.html', 'What is OpenClaw?')
    render_util('persona-entrepreneur', 'persona-entrepreneur.html', 'For Entrepreneurs')
    render_util('persona-cto', 'persona-cto.html', 'For Tech Teams')
    render_util('persona-dev', 'persona-dev.html', 'For Developers')
    render_util('persona-agent', 'persona-agent.html', 'For AI Agents')

    # --- DISCOVER ---
    items.append('<div class="nav-group-label">Discover</div>')
    render_chapter('00')
    render_chapter('01')

    # --- DEPLOY ---
    items.append('<div class="nav-group-label">Deploy</div>')
    render_chapter('02')
    render_chapter('03')
    render_chapter('04')

    # --- OPERATE ---
    items.append('<div class="nav-group-label">Operate</div>')
    render_chapter('05')
    render_chapter('06')

    # --- RESOURCES ---
    items.append('<div class="nav-group-label">Resources</div>')
    render_util('ecosystem', 'ecosystem.html', 'Ecosystem')
    render_chapter('07')
    render_util('checklist', 'checklist.html', 'Checklist')
    render_util('contribuer', 'contribuer.html', 'Contribute')
    render_util('privacy', 'privacy.html', 'Privacy')

    return '\n'.join(items)


def build_en_section_pages(all_sections):
    """Build English section pages."""
    import markdown

    counts = {}
    section_map = {}
    for sec in all_sections:
        md_basename = os.path.basename(sec.md_path)
        section_map[md_basename] = sec.html_file

    sommaire_map = {}
    for sec in all_sections:
        if sec.is_sommaire and sec.chapter_num not in sommaire_map:
            sommaire_map[sec.chapter_num] = sec

    for i, sec in enumerate(all_sections):
        with open(sec.md_path, 'r', encoding='utf-8') as f:
            raw = f.read()
        meta, md_content = fr.parse_frontmatter(raw)
        html_content = markdown.markdown(md_content, extensions=fr.MD_EXTENSIONS)
        html_content = fr.rewrite_md_links(html_content, section_map)

        # Breadcrumb (English)
        breadcrumb_parts = [
            '<nav class="breadcrumb">',
            '  <a href="index.html">Home</a>',
        ]
        if sec.is_sommaire:
            breadcrumb_parts.append('  <span class="sep">/</span>')
            breadcrumb_parts.append(f'  <span>{sec.title}</span>')
        else:
            sommaire = sommaire_map.get(sec.chapter_num)
            if sommaire:
                breadcrumb_parts.append('  <span class="sep">/</span>')
                breadcrumb_parts.append(f'  <a href="{sommaire.html_file}">{sommaire.sidebar_title}</a>')
            breadcrumb_parts.append('  <span class="sep">/</span>')
            breadcrumb_parts.append(f'  <span>{sec.title}</span>')
        breadcrumb_parts.append('</nav>')
        breadcrumb_html = '\n'.join(breadcrumb_parts)

        # Last updated (English months)
        last_updated_html = ''
        last_updated_val = meta.get('last_updated')
        if last_updated_val:
            formatted = fr.format_last_updated(last_updated_val)
            if formatted:
                # Translate month name
                for fr_month, en_month in I18N.items():
                    if fr_month in (formatted or ''):
                        formatted = formatted.replace(fr_month, en_month)
                last_updated_html = f'<div class="last-updated">Last updated: {formatted}</div>'

        # Learning objectives (English)
        toc_items = []
        toc_texts = []
        heading_pattern = re.compile(r'<(h[23])\s+id="([^"]+)"[^>]*>(.*?)</\1>', re.IGNORECASE)
        for match in heading_pattern.finditer(html_content):
            tag = match.group(1).lower()
            anchor = match.group(2)
            text = re.sub(r'<[^>]+>', '', match.group(3)).strip()
            css_class = ' class="toc-h3"' if tag == 'h3' else ''
            toc_items.append(f'<li{css_class}><a href="#{anchor}">{text}</a></li>')
            if tag == 'h2':
                toc_texts.append(text)

        toc_html = ''
        bravo_html = ''
        if len(toc_items) > 3:
            toc_html = (
                '<div class="learning-objectives">\n'
                '  <div class="lo-header" onclick="this.parentElement.classList.toggle(\'collapsed\')">\n'
                '    <span class="lo-icon">&#127891;</span>\n'
                '    What you will learn\n'
                '    <span class="lo-arrow">&#9660;</span>\n'
                '  </div>\n'
                '  <ul class="lo-list">\n'
            )
            toc_html += '\n'.join(f'    {item}' for item in toc_items)
            toc_html += '\n  </ul>\n</div>\n'

            count = len(toc_texts)
            topics = ', '.join(toc_texts[:4])
            if count > 4:
                topics += f' and {count - 4} more'
            bravo_html = (
                '<div class="bravo-box">\n'
                '  <div class="bravo-header">Well done, you completed this section!</div>\n'
                f'  <div class="bravo-body">You covered: {topics}.'
            )
            if i < len(all_sections) - 1:
                next_s = all_sections[i + 1]
                bravo_html += f' <a href="{next_s.html_file}">Continue &rarr;</a>'
            bravo_html += '</div>\n</div>\n'

        wrapped = f'<section class="chapter">\n{html_content}\n</section>'

        edit_link = fr.build_edit_link(sec.github_edit_path)
        giscus = fr.build_giscus_widget()
        issues = fr.build_issues_widget()

        # Prev/Next
        nav_links = ['<hr>', '<div style="display:flex;justify-content:space-between;padding:1rem 0;font-size:0.9rem;">']
        if i > 0:
            prev_sec = all_sections[i - 1]
            nav_links.append(f'<a href="{prev_sec.html_file}">&larr; {fr.truncate(prev_sec.title, 50)}</a>')
        else:
            nav_links.append('<span></span>')
        if i < len(all_sections) - 1:
            next_sec = all_sections[i + 1]
            nav_links.append(f'<a href="{next_sec.html_file}">{fr.truncate(next_sec.title, 50)} &rarr;</a>')
        else:
            nav_links.append('<span></span>')
        nav_links.append('</div>')

        full_content = breadcrumb_html + '\n' + last_updated_html + '\n' + toc_html + wrapped + bravo_html + edit_link + issues + giscus + '\n' + '\n'.join(nav_links)
        sidebar_html = build_en_sidebar(all_sections, sec.slug, sec.chapter_num)
        page_html = en_render_page(sec.title, full_content, sidebar_html)
        en_write_page(sec.html_file, page_html)

        counts[sec.chapter_num] = counts.get(sec.chapter_num, 0) + 1

    return counts


def build_en_index_page(all_sections):
    """Build English landing page."""
    cards = []
    en_chapters = [
        ('00', 'Reading Guide', 'How to read this guide and where to start'),
        ('01', 'Definition', "What OpenClaw is and what it isn't"),
        ('02', 'Installation', 'Install OpenClaw from scratch on a VPS'),
        ('03', 'Configuration', 'Configure the agent for your context'),
        ('04', 'Customization', 'Adapt behavior, tone, and workflows'),
        ('05', 'Maintenance', 'Keep the agent reliable over time'),
        ('06', 'Use Cases', 'Real examples by organization type'),
        ('07', 'Localization', 'Adapt OpenClaw to other languages and contexts'),
    ]

    for chapter_num, short_title, desc in en_chapters:
        if chapter_num == '00':
            href = '00-guide.html'
        else:
            href = f'{chapter_num}-00-sommaire.html'
        cards.append(
            '<a class="chapter-card" href="{href}">'
            '<div class="num">{num}</div>'
            '<div class="card-title">{short}</div>'
            '<div class="card-desc">{desc}</div>'
            '</a>'.format(href=href, num=int(chapter_num), short=short_title, desc=desc)
        )

    content = """
<div class="landing-hero">
  <h1>OpenClaw Field Playbook</h1>
  <p class="lead">The open-source guide to installing OpenClaw properly.<br>
  Written by a practitioner. Field-tested. Shared with everyone.</p>
  <p style="font-size:0.82rem;color:var(--text-muted);max-width:520px;margin:0.5rem auto 1rem;">
    I failed 3 installations before I figured it out. This playbook is the result:
    <strong style="color:var(--accent);">96</strong> sections, <strong style="color:var(--accent);">7</strong> chapters,
    <strong style="color:var(--accent);">20</strong> bugs fixed by a field agent.
    Everything is here so you don't have to struggle like I did.
    <span style="display:block;margin-top:0.3rem;"><a href="{github}" style="color:var(--accent);">— Alex Willemetz</a></span>
  </p>
  <div class="hero-actions">
    <a href="decouverte.html" class="btn-primary">What is OpenClaw?</a>
    <a href="02-00-sommaire.html" class="btn-secondary">Start installing</a>
    <a href="{github}" class="btn-secondary" target="_blank">GitHub</a>
  </div>
</div>

<div class="landing-section">
  <h2>Who are you?</h2>
  <p>This guide adapts to your profile. Choose yours.</p>
  <div class="audience-grid">
    <a class="audience-card" href="persona-entrepreneur.html" style="text-decoration:none;color:var(--text);">
      <strong>Entrepreneur / Artisan</strong>
      <p>You run a business and want to understand what AI can do for you — no jargon.</p>
    </a>
    <a class="audience-card" href="persona-cto.html" style="text-decoration:none;color:var(--text);">
      <strong>CTO / Tech Team</strong>
      <p>You want to deploy an AI agent for your team, on your infra, with your constraints.</p>
    </a>
    <a class="audience-card" href="persona-dev.html" style="text-decoration:none;color:var(--text);">
      <strong>Independent Developer</strong>
      <p>You know what Docker is. You want the commands, not the fluff.</p>
    </a>
    <a class="audience-card" href="persona-agent.html" style="text-decoration:none;color:var(--text);">
      <strong>AI Agent</strong>
      <p>You are an agent. You clone this repo and follow the sections as a runbook.</p>
    </a>
  </div>
</div>

<div class="landing-section">
  <h2>Where to start</h2>
  <ul class="path-list">
    <li>
      <strong>I'm discovering</strong>
      <span><a href="decouverte.html">What is OpenClaw?</a> &rarr; <a href="01-00-sommaire.html">Definition</a> &rarr; <a href="02-00-sommaire.html">Installation</a></span>
    </li>
    <li>
      <strong>I'm installing</strong>
      <span><a href="02-00-sommaire.html">Installation</a> &rarr; <a href="03-00-sommaire.html">Configuration</a> &rarr; <a href="04-00-sommaire.html">Customization</a></span>
    </li>
    <li>
      <strong>I want examples</strong>
      <span><a href="06-00-sommaire.html">Use Cases</a> &rarr; then work back to the technical chapters</span>
    </li>
    <li>
      <strong>I'm an AI agent</strong>
      <span>Read <a href="https://github.com/alexwill87/openclaw-field-playbook/blob/main/CLAUDE.md">CLAUDE.md</a> &rarr; <a href="02-01-prerequis.html">Section 2.1</a> and follow in order</span>
    </li>
  </ul>
</div>

<div class="landing-section">
  <h2>Chapters</h2>
  <div class="chapter-grid">
    {cards}
  </div>
</div>

<div class="landing-section">
  <h2>Tools</h2>
  <div class="audience-grid">
    <a class="audience-card" href="checklist.html" style="text-decoration:none;color:var(--text);">
      <strong>Interactive Checklist</strong>
      <p>Track your progress step by step. Auto-saved.</p>
    </a>
    <a class="audience-card" href="contribuer.html" style="text-decoration:none;color:var(--text);">
      <strong>Contribute</strong>
      <p>Fix an error, add a use case, suggest a section.</p>
    </a>
    <a class="audience-card" href="decouverte.html" style="text-decoration:none;color:var(--text);">
      <strong>What is OpenClaw?</strong>
      <p>For those starting from zero. No jargon.</p>
    </a>
    <a class="audience-card" href="{github}/issues" style="text-decoration:none;color:var(--text);" target="_blank">
      <strong>Report a problem</strong>
      <p>A command that doesn't work? A broken link? Let us know.</p>
    </a>
  </div>
</div>
""".format(github=fr.GITHUB_URL, cards='\n    '.join(cards))

    sidebar_html = build_en_sidebar(all_sections, 'index', None)
    page_html = en_render_page('Home', content, sidebar_html)
    en_write_page('index.html', page_html)


def build_en_search_index(all_sections):
    """Build English search index."""
    index = []
    for sec in all_sections:
        with open(sec.md_path, 'r', encoding='utf-8') as f:
            raw = f.read()
        plain = fr.strip_frontmatter(raw)
        plain = re.sub(r'```[\s\S]*?```', ' ', plain)
        plain = re.sub(r'`[^`]+`', ' ', plain)
        plain = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', plain)
        plain = re.sub(r'#+\s*', '', plain)
        plain = re.sub(r'\|[^\n]+', ' ', plain)
        plain = re.sub(r'-{3,}', ' ', plain)
        plain = re.sub(r'\s+', ' ', plain).strip()
        body = plain[:200]
        index.append({
            'slug': sec.slug,
            'title': sec.title,
            'url': sec.html_file,
            'body': body,
        })
    output_path = os.path.join(EN_OUTPUT_DIR, 'search-index.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    print(f'  -> en/search-index.json ({len(index)} entries)')


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    print('OpenClaw Field Playbook -- build English site')
    print('=' * 60)

    # Check sections-en/ exists
    if not os.path.isdir(EN_SECTIONS_DIR):
        print(f'ERROR: {EN_SECTIONS_DIR} not found.')
        print('Run translate.py first to generate English translations.')
        sys.exit(1)

    # Build section registry from English sources
    all_sections = build_en_section_registry()
    print(f'Found {len(all_sections)} English sections')
    print()

    # Ensure output directory
    os.makedirs(EN_OUTPUT_DIR, exist_ok=True)

    # Copy assets (symlink or copy)
    assets_src = os.path.join(REPO_ROOT, 'assets')
    assets_dst = os.path.join(EN_OUTPUT_DIR, 'assets')
    if not os.path.exists(assets_dst):
        os.symlink(os.path.relpath(assets_src, EN_OUTPUT_DIR), assets_dst)
        print(f'  Symlinked assets/ -> en/assets/')

    # Build section pages
    print('Building English section pages...')
    counts = build_en_section_pages(all_sections)
    print()

    # Build index
    print('Building English utility pages...')
    build_en_index_page(all_sections)
    print()

    # Build search index
    print('Building English search index...')
    build_en_search_index(all_sections)
    print()

    # Summary
    print('=' * 60)
    print('English build summary:')
    total = 0
    en_chapter_names = {
        '00': 'Reading Guide', '01': 'Definition', '02': 'Installation',
        '03': 'Configuration', '04': 'Customization', '05': 'Maintenance',
        '06': 'Use Cases', '07': 'Localization',
    }
    for ch_num in sorted(counts.keys()):
        n = counts[ch_num]
        total += n
        name = en_chapter_names.get(ch_num, f'Chapter {ch_num}')
        print(f'  Chapter {int(ch_num)} ({name}): {n} pages')
    print(f'  Utility pages: 1 (index)')
    print(f'  TOTAL: {total + 1} HTML files in en/')
    print()
    print('English build complete.')
