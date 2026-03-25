
import os
import glob
import markdown
from bs4 import BeautifulSoup

# Adjust REPO_ROOT to be the directory one level above .github/scripts
# Assuming script is in .github/scripts/, REPO_ROOT should be the main repo directory
REPO_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
SECTIONS_DIR = os.path.join(REPO_ROOT, 'sections')
TEMPLATES_DIR = REPO_ROOT

INDEX_TEMPLATE_PATH = os.path.join(TEMPLATES_DIR, 'index_template.html')
OUTPUT_INDEX_PATH = os.path.join(REPO_ROOT, 'index.html')

def build_navigation(section_files):
    nav_html = []
    for filepath, title in section_files:
        # Generate a clean ID for the anchor link
        # Example: sections/01-definition/README.md -> chapter-01-definition
        base_name = os.path.basename(os.path.dirname(filepath))
        section_id = "chapter-" + base_name.replace('-', '_')
        
        # For navigation, we want a link to the section on the same page
        nav_html.append(f'<a href="#{section_id}">{title}</a>')
    return '\n'.join(nav_html)

def build_content(section_files):

    full_content_html = []
    for filepath, title in section_files:
        with open(filepath, 'r', encoding='utf-8') as f:
            md_content = f.read()
        html_content = markdown.markdown(md_content) # Convert Markdown to HTML

        # Generate a clean ID for the anchor link
        base_name = os.path.basename(os.path.dirname(filepath))
        section_id = "chapter-" + base_name.replace('-', '_')

        # Wrap content in a section with the appropriate ID and title
        full_content_html.append(f'<section id="{section_id}" class="chapter">\n')
        full_content_html.append(f'<h2 id="{section_id}-title">{title}</h2>\n')
        full_content_html.append(html_content)
        full_content_html.append(f'\n</section>\n')

    return '\n'.join(full_content_html)

def get_section_info(directory):
    section_data = []
    # List directories directly under SECTIONS_DIR
    chapter_dirs = sorted([d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))])

    for chapter_dir_name in chapter_dirs:
        chapter_path = os.path.join(directory, chapter_dir_name)
        main_md_file = None

        # Try to find README.md first
        if os.path.exists(os.path.join(chapter_path, 'README.md')):
            main_md_file = os.path.join(chapter_path, 'README.md')
        else: # Or find the first .md file in the directory that starts with the chapter name
            md_files = glob.glob(os.path.join(chapter_path, f'{chapter_dir_name}*.md'))
            if md_files: # Take the first one if multiple
                main_md_file = sorted(md_files)[0]

        if not main_md_file or not os.path.exists(main_md_file):
            # If no suitable markdown file, skip this directory
            continue

        # Read title from the first H1 in the Markdown file
        with open(main_md_file, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
            if first_line.startswith('# '):
                title = first_line[2:].strip()
            else:
                # Fallback to directory name, cleaned up
                title = chapter_dir_name.replace('-', ' ').replace('_', ' ').title() 
        
        section_data.append((main_md_file, title))
    return section_data

if __name__ == "__main__":
    print("Starting site build...")
    
    # Get section files details
    section_files_info = get_section_info(SECTIONS_DIR)

    # Build navigation
    navigation_html = build_navigation(section_files_info)
    
    # Build main content
    main_content_html = build_content(section_files_info)

    # Read template
    with open(INDEX_TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        template_content = f.read()

    # Inject content and navigation
    final_html = template_content.replace('<!-- NAVIGATION_PLACEHOLDER -->', navigation_html)
    final_html = final_html.replace('<!-- CONTENT_PLACEHOLDER -->', main_content_html)

    # Write final index.html
    with open(OUTPUT_INDEX_PATH, 'w', encoding='utf-8') as f:
        f.write(final_html)

    print(f"Successfully built {OUTPUT_INDEX_PATH}")
