#!/bin/bash
# audit.sh — Audit complet du site OpenClaw Field Playbook
# Usage : ./scripts/audit.sh
# Peut être lancé par un humain ou un agent IA

set -e
cd "$(dirname "$0")/.."

echo "========================================"
echo "  OpenClaw Field Playbook — Audit"
echo "  $(date '+%Y-%m-%d %H:%M UTC')"
echo "========================================"
echo ""

# --- CONTENU ---
echo "=== CONTENU ==="
pages=$(ls *.html 2>/dev/null | wc -l)
md_files=$(find sections -name '*.md' 2>/dev/null | wc -l)
words=$(find sections -name '*.md' -exec cat {} + 2>/dev/null | wc -w)
echo "  Pages HTML      : $pages"
echo "  Fichiers .md    : $md_files"
echo "  Mots de contenu : $words"
echo ""

# --- PERFORMANCE ---
echo "=== PERFORMANCE ==="
response_time=$(curl -s -o /dev/null -w '%{time_total}' https://www.openclawfieldplaybook.com/ 2>/dev/null || echo "N/A")
index_size=$(curl -s https://www.openclawfieldplaybook.com/ 2>/dev/null | wc -c)
css_size=$(wc -c < assets/style.css 2>/dev/null || echo 0)
js_size=$(wc -c < assets/script.js 2>/dev/null || echo 0)
echo "  Temps de réponse : ${response_time}s"
echo "  Taille index     : $index_size octets"
echo "  CSS              : $css_size octets"
echo "  JS               : $js_size octets"
echo "  Total assets     : $((css_size + js_size)) octets"
echo ""

# --- LIENS ---
echo "=== LIENS INTERNES ==="
broken=0
for f in *.html; do
  grep -oP 'href="([^"#]+\.html)"' "$f" 2>/dev/null | sed 's/href="//;s/"//' | while read link; do
    if [ ! -f "$link" ]; then
      echo "  CASSÉ: $f → $link"
      broken=$((broken+1))
    fi
  done
done
if [ $broken -eq 0 ]; then
  echo "  Aucun lien cassé"
fi
echo ""

# --- SEO ---
echo "=== SEO ==="
[ -f robots.txt ] && echo "  robots.txt       : OK" || echo "  robots.txt       : MANQUANT"
[ -f sitemap.xml ] && echo "  sitemap.xml      : OK ($(grep -c '<url>' sitemap.xml) URLs)" || echo "  sitemap.xml      : MANQUANT"
[ -f search-index.json ] && echo "  search-index.json: OK" || echo "  search-index.json: MANQUANT"
grep -q 'og:title' index.html && echo "  OG tags          : OK" || echo "  OG tags          : MANQUANT"
grep -q 'meta name="description"' index.html && echo "  Meta description : OK" || echo "  Meta description : MANQUANT"
echo ""

# --- GITHUB ---
echo "=== GITHUB ==="
if command -v gh &>/dev/null; then
  open_issues=$(gh issue list -R alexwill87/openclaw-field-playbook --state open --json number 2>/dev/null | jq length 2>/dev/null || echo "?")
  closed_issues=$(gh issue list -R alexwill87/openclaw-field-playbook --state closed --json number --limit 200 2>/dev/null | jq length 2>/dev/null || echo "?")
  stars=$(gh api repos/alexwill87/openclaw-field-playbook --jq '.stargazers_count' 2>/dev/null || echo "?")
  forks=$(gh api repos/alexwill87/openclaw-field-playbook --jq '.forks_count' 2>/dev/null || echo "?")
  echo "  Issues ouvertes  : $open_issues"
  echo "  Issues fermées   : $closed_issues"
  echo "  Étoiles          : $stars"
  echo "  Forks            : $forks"
else
  echo "  gh CLI non disponible"
fi
echo "  Dernier commit   : $(git log -1 --format='%h %s' 2>/dev/null)"
echo ""

# --- SCORE ---
echo "=== SCORE ==="
score=0
max=10
[ $pages -ge 90 ] && score=$((score+1)) && echo "  [+1] Pages >= 90"
[ $md_files -ge 80 ] && score=$((score+1)) && echo "  [+1] Fichiers .md >= 80"
[ -f robots.txt ] && score=$((score+1)) && echo "  [+1] robots.txt présent"
[ -f sitemap.xml ] && score=$((score+1)) && echo "  [+1] sitemap.xml présent"
[ -f search-index.json ] && score=$((score+1)) && echo "  [+1] search-index.json présent"
grep -q 'og:title' index.html && score=$((score+1)) && echo "  [+1] OG tags présents"
grep -q 'meta name="description"' index.html && score=$((score+1)) && echo "  [+1] Meta description présente"
[ "$broken" -eq 0 ] && score=$((score+1)) && echo "  [+1] Zéro lien cassé"
[ "$css_size" -lt 50000 ] && score=$((score+1)) && echo "  [+1] CSS < 50Ko"
[ "$js_size" -lt 50000 ] && score=$((score+1)) && echo "  [+1] JS < 50Ko"
echo ""
echo "  SCORE: $score / $max"
echo ""
echo "========================================"
echo "  Audit terminé"
echo "========================================"
