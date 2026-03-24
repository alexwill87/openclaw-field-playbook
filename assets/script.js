// Search
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

document.addEventListener('click', function(e) {
  if (!e.target.closest('#search-bar')) searchResults.classList.remove('visible');
});

function scrollTo(id) {
  document.getElementById(id).scrollIntoView({ behavior: 'smooth' });
  searchResults.classList.remove('visible');
  searchInput.value = '';
}

// PDF download
document.getElementById('download-pdf').addEventListener('click', function(e) {
  e.preventDefault();
  window.open('https://github.com/alexwill87/openclawfieldplaybook/releases/latest/download/PLAYBOOK.pdf', '_blank');
});

// Smooth scroll for nav links
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', function(e) {
    const target = document.querySelector(this.getAttribute('href'));
    if (target) { e.preventDefault(); target.scrollIntoView({ behavior: 'smooth' }); }
  });
});
