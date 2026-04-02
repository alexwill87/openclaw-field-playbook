
import os
import re
import markdown

REPO_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
SECTIONS_DIR = os.path.join(REPO_ROOT, 'sections')
TEMPLATES_DIR = REPO_ROOT

INDEX_TEMPLATE_PATH = os.path.join(TEMPLATES_DIR, 'index_template.html')
OUTPUT_INDEX_PATH = os.path.join(REPO_ROOT, 'index.html')


def strip_frontmatter(text):
    """Remove YAML front matter from markdown content."""
    if text.startswith('---'):
        end = text.find('---', 3)
        if end != -1:
            return text[end + 3:].strip()
    return text


def get_title_from_md(filepath):
    """Extract first H1 title from a markdown file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    content = strip_frontmatter(content)
    for line in content.split('\n'):
        line = line.strip()
        if line.startswith('# '):
            return line[2:].strip()
    return os.path.basename(filepath).replace('.md', '').replace('-', ' ').title()


def get_all_sections():
    """Get all section files organized by chapter."""
    chapters = []

    # Handle 00-reading-guide.md (single file, not a directory)
    reading_guide = os.path.join(SECTIONS_DIR, '00-reading-guide.md')
    if os.path.exists(reading_guide):
        title = get_title_from_md(reading_guide)
        chapters.append({
            'id': 'chapter-00',
            'title': title,
            'files': [reading_guide]
        })

    # Handle chapter directories (01-definition, 02-installation, etc.)
    entries = sorted(os.listdir(SECTIONS_DIR))
    for entry in entries:
        full_path = os.path.join(SECTIONS_DIR, entry)
        if not os.path.isdir(full_path):
            continue

        # Get README.md as the chapter intro
        readme = os.path.join(full_path, 'README.md')
        if not os.path.exists(readme):
            continue

        chapter_title = get_title_from_md(readme)
        chapter_id = 'chapter-' + entry.split('-')[0]

        # Collect all .md files in the directory
        md_files = sorted([
            os.path.join(full_path, f)
            for f in os.listdir(full_path)
            if f.endswith('.md')
        ])

        # Put README.md first, then the rest
        ordered_files = [readme] + [f for f in md_files if f != readme]

        chapters.append({
            'id': chapter_id,
            'title': chapter_title,
            'files': ordered_files
        })

    return chapters


def build_navigation(chapters):
    """Build sidebar navigation HTML."""
    nav_items = []
    for ch in chapters:
        nav_items.append(f'<a href="#{ch["id"]}">{ch["title"]}</a>')
    return '\n'.join(nav_items)


def build_content(chapters):
    """Build main content HTML from all sections."""
    md_extensions = ['tables', 'fenced_code', 'codehilite', 'toc']
    sections_html = []

    for ch in chapters:
        # Chapter wrapper
        sections_html.append(f'<section id="{ch["id"]}" class="chapter">')

        for filepath in ch['files']:
            with open(filepath, 'r', encoding='utf-8') as f:
                raw = f.read()

            clean = strip_frontmatter(raw)
            html = markdown.markdown(clean, extensions=md_extensions)
            sections_html.append(html)

        sections_html.append('</section>')

    return '\n'.join(sections_html)


if __name__ == "__main__":
    print("Starting site build...")

    chapters = get_all_sections()
    print(f"Found {len(chapters)} chapters, {sum(len(c['files']) for c in chapters)} total files")

    navigation_html = build_navigation(chapters)
    main_content_html = build_content(chapters)

    with open(INDEX_TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        template_content = f.read()

    final_html = template_content.replace('<!-- NAVIGATION_PLACEHOLDER -->', navigation_html)
    final_html = final_html.replace('<!-- CONTENT_PLACEHOLDER -->', main_content_html)

    with open(OUTPUT_INDEX_PATH, 'w', encoding='utf-8') as f:
        f.write(final_html)

    print(f"Successfully built {OUTPUT_INDEX_PATH}")
    for ch in chapters:
        print(f"  {ch['id']}: {ch['title']} ({len(ch['files'])} files)")
