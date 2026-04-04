#!/usr/bin/env python3
"""
Translation engine for OpenClaw Field Playbook.

Translates all .md source files from French to English using Claude Haiku.
Uses a SHA256 cache to skip unchanged files.

Usage:
  python3 translate.py                    # Translate all changed files
  python3 translate.py --force            # Force re-translate everything
  python3 translate.py --file sections/01-definition/07-journee-type.md  # Single file
  python3 translate.py --dry-run          # Show what would be translated

Requires: ANTHROPIC_API_KEY environment variable
"""

import os
import sys
import json
import hashlib
import time
import re

REPO_ROOT = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
)
SECTIONS_DIR = os.path.join(REPO_ROOT, 'sections')
SECTIONS_EN_DIR = os.path.join(REPO_ROOT, 'sections-en')
CACHE_DIR = os.path.join(REPO_ROOT, '.translations')
CACHE_FILE = os.path.join(CACHE_DIR, 'cache.json')

MODEL = 'claude-haiku-4-5-20251001'
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds

# ---------------------------------------------------------------------------
# Translation prompt — crafted for professional-quality FR→EN translation
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """You are a professional technical translator specializing in software documentation. You translate French to English with the precision of a financial translation agency and the naturalness of a native English technical writer.

## Rules

1. **Markdown integrity**: Preserve ALL markdown formatting exactly — headers, lists, tables, code blocks, links, frontmatter YAML, horizontal rules. Do not add or remove any structural element.

2. **Code blocks**: NEVER translate content inside code blocks (```...```), inline code (`...`), file paths, command-line arguments, variable names, or JSON keys/values. Code stays exactly as-is.

3. **YAML frontmatter**: Keep all fields as-is EXCEPT change `lang: fr` to `lang: en`. Do not translate status, audience, chapter, contributors, or any other field.

4. **Technical terms**: Keep English technical terms that appear in the French source (API, VPS, webhook, system prompt, knowledge base, Docker, SSH, etc.). Do not translate brand names (OpenClaw, Tailscale, Telegram, Hetzner, etc.).

5. **Natural English**: Translate idiomatically, not literally. French "il faut que" → English should use natural phrasing ("you need to", "make sure to"), not word-for-word translation. Adapt sentence structure to flow naturally in English.

6. **Tone**: Maintain the original tone — practical, direct, no unnecessary jargon. The playbook is written by a practitioner, not an academic. Keep it conversational but professional.

7. **Proper nouns**: Keep names (Alex Willemetz, Jean, Marc, Sophie, Karim), city names (Paris, Montreuil), and organization names unchanged.

8. **Currency**: Keep EUR amounts as-is. Do not convert to USD or other currencies.

9. **Links**: Keep all link targets (.md filenames, URLs, anchors) exactly as-is. Only translate link display text.

10. **Completeness**: Translate EVERYTHING that is French text. Do not skip sections, summarize, or abbreviate. The English version must have the exact same structure and content as the French original.

11. **Accents**: The French source may be missing accents (e.g., "metier" instead of "métier"). This is intentional in the source files. In the English translation this is irrelevant since you're translating to English.

12. **Section numbers**: Keep section numbers (1.7, 3.18, 6.8) exactly as-is."""

USER_PROMPT_TEMPLATE = """Translate the following French markdown document to English. Return ONLY the translated markdown, nothing else — no explanations, no commentary, no wrapper.

---
{content}
---"""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def sha256(content):
    """Compute SHA256 hash of content."""
    return hashlib.sha256(content.encode('utf-8')).hexdigest()


def load_cache():
    """Load the translation cache."""
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def save_cache(cache):
    """Save the translation cache."""
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(cache, f, indent=2, ensure_ascii=False)
    print(f'  Cache saved ({len(cache)} entries)')


def find_all_md_files():
    """Find all .md files in sections/ directory."""
    md_files = []
    for root, _dirs, files in os.walk(SECTIONS_DIR):
        for fname in sorted(files):
            if fname.endswith('.md'):
                md_files.append(os.path.join(root, fname))
    return md_files


def relative_path(filepath):
    """Get path relative to SECTIONS_DIR."""
    return os.path.relpath(filepath, SECTIONS_DIR)


def en_path(filepath):
    """Get the corresponding English file path."""
    rel = relative_path(filepath)
    return os.path.join(SECTIONS_EN_DIR, rel)


# ---------------------------------------------------------------------------
# Translation via Anthropic API
# ---------------------------------------------------------------------------

def translate_content(client, content):
    """Translate a single markdown document using Claude Haiku."""
    for attempt in range(MAX_RETRIES):
        try:
            response = client.messages.create(
                model=MODEL,
                max_tokens=8192,
                system=SYSTEM_PROMPT,
                messages=[{
                    'role': 'user',
                    'content': USER_PROMPT_TEMPLATE.format(content=content)
                }]
            )
            translated = response.content[0].text

            # Strip any markdown wrapper the model might add
            if translated.startswith('```markdown\n'):
                translated = translated[len('```markdown\n'):]
                if translated.endswith('\n```'):
                    translated = translated[:-len('\n```')]
            elif translated.startswith('```\n'):
                translated = translated[len('```\n'):]
                if translated.endswith('\n```'):
                    translated = translated[:-len('\n```')]

            return translated.strip()

        except Exception as e:
            if attempt < MAX_RETRIES - 1:
                print(f'    Retry {attempt + 1}/{MAX_RETRIES} after error: {e}')
                time.sleep(RETRY_DELAY * (attempt + 1))
            else:
                raise


def validate_translation(original, translated):
    """Basic validation that translation preserved structure."""
    issues = []

    # Check frontmatter preserved
    if original.startswith('---') and not translated.startswith('---'):
        issues.append('Missing YAML frontmatter')

    # Check code blocks count matches
    orig_code = len(re.findall(r'```', original))
    trans_code = len(re.findall(r'```', translated))
    if orig_code != trans_code:
        issues.append(f'Code block count mismatch: {orig_code} vs {trans_code}')

    # Check heading count matches
    orig_h = len(re.findall(r'^#+\s', original, re.MULTILINE))
    trans_h = len(re.findall(r'^#+\s', translated, re.MULTILINE))
    if orig_h != trans_h:
        issues.append(f'Heading count mismatch: {orig_h} vs {trans_h}')

    # Check table row count matches
    orig_tables = len(re.findall(r'^\|', original, re.MULTILINE))
    trans_tables = len(re.findall(r'^\|', translated, re.MULTILINE))
    if orig_tables != trans_tables:
        issues.append(f'Table row count mismatch: {orig_tables} vs {trans_tables}')

    # Check links preserved (href targets should be identical)
    orig_links = sorted(re.findall(r'\]\(([^)]+)\)', original))
    trans_links = sorted(re.findall(r'\]\(([^)]+)\)', translated))
    if orig_links != trans_links:
        missing = set(orig_links) - set(trans_links)
        added = set(trans_links) - set(orig_links)
        if missing:
            issues.append(f'Missing links: {missing}')
        if added:
            issues.append(f'Extra links: {added}')

    # Check lang field changed
    if 'lang: fr' in original and 'lang: en' not in translated:
        issues.append('lang: fr not changed to lang: en')

    return issues


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Translate playbook FR→EN')
    parser.add_argument('--force', action='store_true', help='Force re-translate all files')
    parser.add_argument('--file', help='Translate a single file')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be translated')
    args = parser.parse_args()

    # Check API key
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key and not args.dry_run:
        print('ERROR: ANTHROPIC_API_KEY environment variable is required.')
        print('Set it with: export ANTHROPIC_API_KEY=sk-ant-...')
        sys.exit(1)

    # Initialize client
    client = None
    if not args.dry_run:
        from anthropic import Anthropic
        client = Anthropic(api_key=api_key)

    # Load cache
    cache = load_cache()

    # Find files to translate
    if args.file:
        filepath = os.path.abspath(args.file)
        if not os.path.exists(filepath):
            print(f'ERROR: File not found: {filepath}')
            sys.exit(1)
        md_files = [filepath]
    else:
        md_files = find_all_md_files()

    print(f'OpenClaw Field Playbook — Translation FR→EN')
    print(f'Model: {MODEL}')
    print(f'Files found: {len(md_files)}')
    print(f'Cache entries: {len(cache)}')
    print('=' * 60)

    # Determine what needs translation
    to_translate = []
    skipped = 0

    for filepath in md_files:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        content_hash = sha256(content)
        rel = relative_path(filepath)
        en_file = en_path(filepath)

        if not args.force and rel in cache and cache[rel]['hash'] == content_hash:
            # Check that the EN file still exists
            if os.path.exists(en_file):
                skipped += 1
                continue

        to_translate.append((filepath, rel, content, content_hash))

    print(f'To translate: {len(to_translate)}')
    print(f'Skipped (cached): {skipped}')
    print()

    if args.dry_run:
        for _, rel, _, _ in to_translate:
            print(f'  Would translate: {rel}')
        return

    if not to_translate:
        print('Nothing to translate. All files are up to date.')
        return

    # Translate
    success = 0
    errors = 0

    for i, (filepath, rel, content, content_hash) in enumerate(to_translate):
        print(f'[{i+1}/{len(to_translate)}] {rel}')

        try:
            translated = translate_content(client, content)

            # Validate
            issues = validate_translation(content, translated)
            if issues:
                print(f'  WARNINGS:')
                for issue in issues:
                    print(f'    - {issue}')

            # Write translated file
            out_path = en_path(filepath)
            os.makedirs(os.path.dirname(out_path), exist_ok=True)
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(translated + '\n')

            # Update cache
            cache[rel] = {
                'hash': content_hash,
                'translated_hash': sha256(translated),
                'model': MODEL,
                'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
            }

            success += 1
            print(f'  OK ({len(content)} → {len(translated)} chars)')

        except Exception as e:
            errors += 1
            print(f'  ERROR: {e}')

    # Save cache
    save_cache(cache)

    print()
    print('=' * 60)
    print(f'Translation complete: {success} OK, {errors} errors, {skipped} cached')

    if errors > 0:
        sys.exit(1)


if __name__ == '__main__':
    main()
