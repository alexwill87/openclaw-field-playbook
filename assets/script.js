// ========== MOBILE MENU TOGGLE ==========
function toggleMenu() {
  var sidebar = document.querySelector('.sidebar');
  if (sidebar) sidebar.classList.toggle('open');
}

// Close sidebar when clicking a link (mobile)
document.querySelectorAll('#side-nav a').forEach(function(a) {
  a.addEventListener('click', function() {
    var sidebar = document.querySelector('.sidebar');
    if (sidebar && window.innerWidth < 900) sidebar.classList.remove('open');
  });
});

// ========== SMOOTH SCROLL ==========
document.querySelectorAll('a[href^="#"]').forEach(function(a) {
  a.addEventListener('click', function(e) {
    var target = document.querySelector(this.getAttribute('href'));
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
});

// ========== SCROLL SPY SIDEBAR ==========
var sideNavLinks = document.querySelectorAll('#side-nav a');
var chapters = [];

sideNavLinks.forEach(function(link) {
  var href = link.getAttribute('href');
  if (href && href.startsWith('#')) {
    var el = document.getElementById(href.substring(1));
    if (el) chapters.push({ link: link, el: el });
  }
});

if (chapters.length > 0) {
  window.addEventListener('scroll', function() {
    var scrollPos = window.scrollY + 100;
    var current = chapters[0];

    for (var i = 0; i < chapters.length; i++) {
      if (chapters[i].el.offsetTop <= scrollPos) {
        current = chapters[i];
      }
    }

    sideNavLinks.forEach(function(l) { l.classList.remove('active'); });
    if (current) current.link.classList.add('active');
  });
}

// ========== DARK MODE TOGGLE ==========
(function() {
  var root = document.documentElement;
  var toggleBtn = document.querySelector('.theme-toggle');

  function getPreferredTheme() {
    var stored = localStorage.getItem('theme');
    if (stored) return stored;
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  function applyTheme(theme) {
    if (theme === 'dark') {
      root.classList.add('dark');
      root.classList.remove('light');
    } else {
      root.classList.add('light');
      root.classList.remove('dark');
    }
    updateIcon(theme);
  }

  function updateIcon(theme) {
    if (!toggleBtn) return;
    // Sun icon for dark mode (click to go light), moon icon for light mode (click to go dark)
    toggleBtn.textContent = theme === 'dark' ? '\u2600\uFE0F' : '\uD83C\uDF19';
    toggleBtn.setAttribute('aria-label', theme === 'dark' ? 'Passer en mode clair' : 'Passer en mode sombre');
  }

  // Apply on load
  var currentTheme = getPreferredTheme();
  applyTheme(currentTheme);

  // Toggle on click
  if (toggleBtn) {
    toggleBtn.addEventListener('click', function() {
      var isDark = root.classList.contains('dark');
      var newTheme = isDark ? 'light' : 'dark';
      localStorage.setItem('theme', newTheme);
      applyTheme(newTheme);
    });
  }
})();

// ========== GITHUB BADGES ==========
(function() {
  var badgesEl = document.querySelector('.github-badges');
  if (!badgesEl) return;

  var cacheKey = 'gh_repo_data';
  var cacheTimeKey = 'gh_repo_data_time';
  var cacheDuration = 5 * 60 * 1000; // 5 minutes

  function renderBadges(data) {
    badgesEl.innerHTML =
      '<span class="badge">\u2B50 ' + (data.stargazers_count || 0) + '</span>' +
      '<span class="badge">\uD83C\uDF74 ' + (data.forks_count || 0) + '</span>';
  }

  // Check sessionStorage cache
  var cached = sessionStorage.getItem(cacheKey);
  var cachedTime = sessionStorage.getItem(cacheTimeKey);

  if (cached && cachedTime && (Date.now() - parseInt(cachedTime, 10)) < cacheDuration) {
    try {
      renderBadges(JSON.parse(cached));
      return;
    } catch (e) {
      // Cache invalid, fetch fresh
    }
  }

  fetch('https://api.github.com/repos/alexwill87/openclaw-field-playbook')
    .then(function(res) {
      if (!res.ok) throw new Error('GitHub API error');
      return res.json();
    })
    .then(function(data) {
      sessionStorage.setItem(cacheKey, JSON.stringify(data));
      sessionStorage.setItem(cacheTimeKey, String(Date.now()));
      renderBadges(data);
    })
    .catch(function() {
      // Silently fail -- badges just won't show
    });
})();

// ========== FULL-TEXT SEARCH ==========
(function() {
  var searchInput = document.getElementById('search-input');
  if (!searchInput) return;

  var searchResults = document.getElementById('search-results');
  var searchIndex = null;

  // Fetch search index
  fetch('search-index.json')
    .then(function(res) {
      if (!res.ok) throw new Error('Search index not found');
      return res.json();
    })
    .then(function(data) {
      searchIndex = data;
    })
    .catch(function() {
      // Silently fail -- search just won't work
    });

  function normalize(str) {
    return str.toLowerCase()
      .normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  }

  function performSearch(query) {
    if (!searchIndex || query.length < 2) {
      searchResults.innerHTML = '';
      searchResults.style.display = 'none';
      return;
    }

    var q = normalize(query);
    var results = searchIndex.filter(function(entry) {
      return normalize(entry.title).indexOf(q) !== -1 ||
             normalize(entry.body).indexOf(q) !== -1;
    }).slice(0, 8);

    if (results.length === 0) {
      searchResults.innerHTML = '<div class="search-no-result">Aucun resultat</div>';
      searchResults.style.display = 'block';
      return;
    }

    var html = '';
    results.forEach(function(r) {
      html += '<a class="search-result-item" href="' + r.url + '">' +
              '<div class="search-result-title">' + r.title + '</div>' +
              '<div class="search-result-body">' + r.body.substring(0, 80) + '...</div>' +
              '</a>';
    });
    searchResults.innerHTML = html;
    searchResults.style.display = 'block';
  }

  searchInput.addEventListener('input', function() {
    performSearch(this.value.trim());
  });

  // Close results when clicking outside
  document.addEventListener('click', function(e) {
    if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
      searchResults.style.display = 'none';
    }
  });

  // Reopen on focus if there's a query
  searchInput.addEventListener('focus', function() {
    if (this.value.trim().length >= 2) {
      performSearch(this.value.trim());
    }
  });
})();

// ========== OPEN ISSUES WIDGET ==========
(function() {
  var widget = document.getElementById('issues-widget');
  if (!widget) return;

  var cacheKey = 'gh_issues_data';
  var cacheTimeKey = 'gh_issues_time';
  var cacheDuration = 10 * 60 * 1000;

  function renderIssues(issues) {
    if (!issues.length) {
      widget.innerHTML = '<p style="color:var(--text-muted);font-size:0.82rem;">Aucune issue ouverte pour cette section.</p>';
      return;
    }
    var html = '<div style="font-size:0.82rem;">';
    html += '<strong>' + issues.length + ' issue(s) ouverte(s) liee(s) a cette section</strong>';
    html += '<ul style="margin:0.5rem 0 0 1.2rem;padding:0;">';
    issues.forEach(function(issue) {
      var labels = '';
      if (issue.labels && issue.labels.length) {
        issue.labels.forEach(function(l) {
          labels += ' <span style="display:inline-block;padding:0.1rem 0.4rem;border-radius:8px;font-size:0.7rem;background:#' + l.color + '20;color:#' + l.color + ';">' + l.name + '</span>';
        });
      }
      html += '<li style="margin-bottom:0.3rem;"><a href="' + issue.html_url + '" target="_blank" style="color:var(--accent);text-decoration:none;">#' + issue.number + ' ' + issue.title + '</a>' + labels + '</li>';
    });
    html += '</ul></div>';
    widget.innerHTML = html;
  }

  var pagePath = window.location.pathname.split('/').pop().replace('.html', '');

  var cached = sessionStorage.getItem(cacheKey);
  var cachedTime = sessionStorage.getItem(cacheTimeKey);

  function filterAndRender(issues) {
    var matched = issues.filter(function(issue) {
      var text = ((issue.title || '') + ' ' + (issue.body || '')).toLowerCase();
      var parts = pagePath.split('-');
      if (parts.length >= 2) {
        var chap = parts[0];
        var sec = parts[1];
        return text.indexOf(chap + '.' + sec) !== -1 ||
               text.indexOf(chap + '-' + sec) !== -1 ||
               text.indexOf(chap + '.' + parseInt(sec)) !== -1 ||
               text.indexOf('section ' + parseInt(chap) + '.' + parseInt(sec)) !== -1 ||
               text.indexOf(pagePath) !== -1;
      }
      return false;
    });
    renderIssues(matched);
  }

  if (cached && cachedTime && (Date.now() - parseInt(cachedTime, 10)) < cacheDuration) {
    try { filterAndRender(JSON.parse(cached)); return; } catch(e) {}
  }

  fetch('https://api.github.com/repos/alexwill87/openclaw-field-playbook/issues?state=open&per_page=100')
    .then(function(res) { return res.json(); })
    .then(function(data) {
      sessionStorage.setItem(cacheKey, JSON.stringify(data));
      sessionStorage.setItem(cacheTimeKey, String(Date.now()));
      filterAndRender(data);
    })
    .catch(function() {});
})();
