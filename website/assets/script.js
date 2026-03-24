document.addEventListener('DOMContentLoaded', function() {
    // Search setup
    const chapters = [
      { id: 'chapter-0', title: 'Reading Guide', keywords: 'how to read navigate language contract agent human' },
      { id: 'chapter-1', title: 'Definition', keywords: 'what is openclaw proactive reactive sovereign alternatives' },
      { id: 'chapter-2', title: 'Installation', keywords: 'install setup local cloud VPS ubuntu prerequisites' },
      { id: 'chapter-3', title: 'Configuration', keywords: 'configure tools memory triggers multi-agent architecture' },
      { id: 'chapter-4', title: 'Personalisation', keywords: 'system prompt personality voice workflows rules guardrails' },
      { id: 'chapter-5', title: 'Maintenance', keywords: 'maintain review audit memory drift error handling' },
      { id: 'chapter-6', title: 'Use Cases', keywords: 'use case field report freelance artisan enterprise developer' },
      { id: 'chapter-7', title: 'Localisation', keywords: 'locale france fr-FR en-US RGPD legislation ecosystem' }
    ];

    const searchInput = document.getElementById('search-input');
    const searchResults = document.getElementById('search-results');

    if(searchInput) {
        searchInput.addEventListener('input', function() {
          const q = this.value.trim().toLowerCase();
          if (q.length < 2) { searchResults.classList.remove('visible'); return; }

          const matches = chapters.filter(c =>
            c.title.toLowerCase().includes(q) || c.keywords.toLowerCase().includes(q)
          );

          if (matches.length === 0) {
            searchResults.innerHTML = '<div class="search-result-item">No results</div>';
          } else {
            searchResults.innerHTML = matches.map(c =>
              `<div class="search-result-item" onclick="scrollTo('${c.id}')">
                <strong>Chapter ${chapters.indexOf(c)} — ${c.title}</strong>
              </div>`
            ).join('');
          }
          searchResults.classList.add('visible');
        });
    }
});

// PDF download (Global scope)
window.generateLivePDF = function() {
  const element = document.getElementById('content');
  const opt = {
    margin:       [10, 15],
    filename:     'OpenClaw-Field-Playbook.pdf',
    image:        { type: 'jpeg', quality: 0.98 },
    html2canvas:  { scale: 2, useCORS: true },
    jsPDF:        { unit: 'mm', format: 'a4', orientation: 'portrait' }
  };
  html2pdf().set(opt).from(element).save();
}

function scrollTo(id) {
  document.getElementById(id).scrollIntoView({ behavior: 'smooth' });
  const results = document.getElementById('search-results');
  if(results) results.classList.remove('visible');
  const input = document.getElementById('search-input');
  if(input) input.value = '';
}
