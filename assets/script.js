// ========== BACK TO TOP ==========
(function() {
  var btn = document.createElement('button');
  btn.id = 'back-to-top';
  btn.innerHTML = '&#8593;';
  btn.title = 'Retour en haut';
  btn.setAttribute('aria-label', 'Retour en haut de la page');
  btn.onclick = function() { window.scrollTo({ top: 0, behavior: 'smooth' }); };
  document.body.appendChild(btn);

  window.addEventListener('scroll', function() {
    if (window.scrollY > 400) {
      btn.classList.add('visible');
    } else {
      btn.classList.remove('visible');
    }
  });
})();

// ========== BLOCKQUOTE TYPES ==========
(function() {
  document.querySelectorAll('.chapter blockquote').forEach(function(bq) {
    var text = bq.textContent.toLowerCase();
    if (text.match(/attention|sécurité|securite|important|critique|danger|ne jamais/)) {
      bq.classList.add('bq-warning');
      bq.setAttribute('role', 'alert');
    } else if (text.match(/recommandation|conseil|astuce|bonne pratique/)) {
      bq.classList.add('bq-tip');
      bq.setAttribute('role', 'note');
    }
  });
})();

// ========== FORM PROGRESS BAR ==========
(function() {
  var form = document.getElementById('contact-form');
  if (!form) return;
  var totalSteps = 7;
  var progress = document.createElement('div');
  progress.className = 'form-progress';
  for (var i = 0; i < totalSteps; i++) {
    var step = document.createElement('div');
    step.className = 'form-progress-step';
    step.setAttribute('data-step', i + 1);
    progress.appendChild(step);
  }
  form.insertBefore(progress, form.firstChild.nextSibling);

  // Override nextStep to update progress
  var origNextStep = window.nextStep;
  if (origNextStep) {
    window.nextStep = function(k, v) {
      origNextStep(k, v);
      var visible = form.querySelector('.form-step:not([style*="display: none"])');
      if (visible) {
        var num = parseInt(visible.id.replace('form-step-', ''));
        progress.querySelectorAll('.form-progress-step').forEach(function(s) {
          var sNum = parseInt(s.getAttribute('data-step'));
          s.classList.toggle('done', sNum < num);
        });
      }
    };
  }
})();

// ========== MOBILE MENU TOGGLE ==========
function toggleMenu() {
  var sidebar = document.querySelector('.sidebar');
  var menuBtn = document.querySelector('.menu-toggle');
  if (!sidebar) return;

  sidebar.classList.toggle('open');
  var isOpen = sidebar.classList.contains('open');
  if (menuBtn) menuBtn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');

  if (isOpen) {
    // Focus first link in sidebar
    var firstLink = sidebar.querySelector('a');
    if (firstLink) firstLink.focus();

    // Focus trap: keep Tab inside sidebar when open on mobile
    sidebar._focusTrapHandler = function(e) {
      if (e.key === 'Escape') {
        toggleMenu();
        if (menuBtn) menuBtn.focus();
        return;
      }
      if (e.key !== 'Tab') return;
      var focusable = sidebar.querySelectorAll('a, button, input, [tabindex]:not([tabindex="-1"])');
      if (focusable.length === 0) return;
      var first = focusable[0];
      var last = focusable[focusable.length - 1];
      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault();
        last.focus();
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault();
        first.focus();
      }
    };
    document.addEventListener('keydown', sidebar._focusTrapHandler);
  } else {
    // Remove focus trap
    if (sidebar._focusTrapHandler) {
      document.removeEventListener('keydown', sidebar._focusTrapHandler);
      sidebar._focusTrapHandler = null;
    }
  }
}

// Close sidebar when clicking a link (mobile)
document.querySelectorAll('#side-nav a').forEach(function(a) {
  a.addEventListener('click', function() {
    var sidebar = document.querySelector('.sidebar');
    if (sidebar && window.innerWidth < 900) {
      sidebar.classList.remove('open');
      var menuBtn = document.querySelector('.menu-toggle');
      if (menuBtn) menuBtn.setAttribute('aria-expanded', 'false');
      if (sidebar._focusTrapHandler) {
        document.removeEventListener('keydown', sidebar._focusTrapHandler);
        sidebar._focusTrapHandler = null;
      }
    }
  });
});

// ========== COPY CODE BUTTON ==========
(function() {
  // Create a live region for copy feedback (screen readers)
  var copyStatus = document.createElement('div');
  copyStatus.setAttribute('role', 'status');
  copyStatus.setAttribute('aria-live', 'polite');
  copyStatus.className = 'sr-only';
  document.body.appendChild(copyStatus);

  document.querySelectorAll('.chapter pre').forEach(function(pre) {
    var wrapper = document.createElement('div');
    wrapper.className = 'code-wrapper';
    pre.parentNode.insertBefore(wrapper, pre);
    wrapper.appendChild(pre);

    // Detect language from code class (e.g. language-bash, language-yaml)
    var code = pre.querySelector('code');
    var lang = '';
    if (code && code.className) {
      var match = code.className.match(/language-(\w+)/);
      if (match) lang = match[1];
    }
    var label = lang ? 'Copier le bloc de code ' + lang : 'Copier le bloc de code';

    var btn = document.createElement('button');
    btn.className = 'copy-btn';
    btn.textContent = 'Copier';
    btn.setAttribute('aria-label', label);
    btn.addEventListener('click', function() {
      var text = (code || pre).textContent;
      // Remove leading $ prompts
      text = text.replace(/^\$ /gm, '');
      navigator.clipboard.writeText(text).then(function() {
        btn.textContent = 'Copie !';
        btn.classList.add('copied');
        copyStatus.textContent = 'Code copie dans le presse-papier';
        setTimeout(function() {
          btn.textContent = 'Copier';
          btn.classList.remove('copied');
          copyStatus.textContent = '';
        }, 2000);
      });
    });
    wrapper.appendChild(btn);
  });
})();

// ========== SMOOTH SCROLL ==========
document.querySelectorAll('a[href^="#"]').forEach(function(a) {
  a.addEventListener('click', function(e) {
    var target = document.querySelector(this.getAttribute('href'));
    if (target) {
      e.preventDefault();
      var prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      target.scrollIntoView({ behavior: prefersReduced ? 'auto' : 'smooth', block: 'start' });
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

  // Live region for theme change announcement
  var themeStatus = document.createElement('div');
  themeStatus.setAttribute('role', 'status');
  themeStatus.setAttribute('aria-live', 'polite');
  themeStatus.className = 'sr-only';
  document.body.appendChild(themeStatus);

  function getPreferredTheme() {
    var stored = localStorage.getItem('theme');
    if (stored) return stored;
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  function applyTheme(theme, announce) {
    if (theme === 'dark') {
      root.classList.add('dark');
      root.classList.remove('light');
    } else {
      root.classList.add('light');
      root.classList.remove('dark');
    }
    updateIcon(theme);
    if (announce) {
      themeStatus.textContent = theme === 'dark' ? 'Mode sombre active' : 'Mode clair active';
      setTimeout(function() { themeStatus.textContent = ''; }, 2000);
    }
  }

  function updateIcon(theme) {
    if (!toggleBtn) return;
    toggleBtn.textContent = theme === 'dark' ? '\u2600\uFE0F' : '\uD83C\uDF19';
    toggleBtn.setAttribute('aria-label', theme === 'dark' ? 'Passer en mode clair' : 'Passer en mode sombre');
  }

  // Apply on load (no announcement)
  var currentTheme = getPreferredTheme();
  applyTheme(currentTheme, false);

  // Toggle on click (with announcement)
  if (toggleBtn) {
    toggleBtn.addEventListener('click', function() {
      var isDark = root.classList.contains('dark');
      var newTheme = isDark ? 'light' : 'dark';
      localStorage.setItem('theme', newTheme);
      applyTheme(newTheme, true);
    });
  }

  // Expose globally for onclick fallback
  window.toggleTheme = function() {
    if (toggleBtn) toggleBtn.click();
  };
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

// ========== LANGUAGE SWITCH ==========
function switchLang() {
  var toggle = document.querySelector('.lang-toggle');
  if (!toggle) return;
  var currentLang = toggle.getAttribute('data-lang') || 'fr';
  var page = window.location.pathname.split('/').pop() || 'index.html';

  if (currentLang === 'fr') {
    // Switch to English: go to /en/samepage.html
    var basePath = window.location.pathname.replace(/\/[^/]*$/, '');
    window.location.href = basePath + '/en/' + page;
  } else {
    // Switch to French: go to ../samepage.html
    window.location.href = '../' + page;
  }
}

// Remember language preference
(function() {
  var toggle = document.querySelector('.lang-toggle');
  if (!toggle) return;
  var lang = toggle.getAttribute('data-lang');
  if (lang) localStorage.setItem('preferred-lang', lang);
})();

// ========== FULL-TEXT SEARCH ==========
(function() {
  var searchInput = document.getElementById('search-input');
  if (!searchInput) return;

  var searchResults = document.getElementById('search-results');
  var searchIndex = null;
  var activeIndex = -1;

  // Add ARIA attributes for screen readers
  searchResults.setAttribute('role', 'listbox');
  searchResults.setAttribute('aria-label', 'Resultats de recherche');
  searchInput.setAttribute('role', 'combobox');
  searchInput.setAttribute('aria-autocomplete', 'list');
  searchInput.setAttribute('aria-expanded', 'false');
  searchInput.setAttribute('aria-controls', 'search-results');
  searchInput.setAttribute('aria-haspopup', 'listbox');

  // Live region for announcing result count
  var searchStatus = document.createElement('div');
  searchStatus.setAttribute('role', 'status');
  searchStatus.setAttribute('aria-live', 'polite');
  searchStatus.className = 'sr-only';
  searchInput.parentNode.appendChild(searchStatus);

  // Fetch search index
  var searchIndexUrl = 'search-index.json';
  fetch(searchIndexUrl)
    .then(function(res) {
      if (!res.ok) throw new Error('Search index not found');
      return res.json();
    })
    .then(function(data) {
      searchIndex = data;
    })
    .catch(function() {});

  function normalize(str) {
    return str.toLowerCase()
      .normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  }

  function setActiveResult(index) {
    var items = searchResults.querySelectorAll('.search-result-item');
    items.forEach(function(item) {
      item.classList.remove('search-active');
      item.setAttribute('aria-selected', 'false');
    });
    activeIndex = index;
    if (index >= 0 && index < items.length) {
      items[index].classList.add('search-active');
      items[index].setAttribute('aria-selected', 'true');
      searchInput.setAttribute('aria-activedescendant', items[index].id);
      items[index].scrollIntoView({ block: 'nearest' });
    } else {
      searchInput.removeAttribute('aria-activedescendant');
    }
  }

  function performSearch(query) {
    activeIndex = -1;
    if (!searchIndex || query.length < 2) {
      searchResults.innerHTML = '';
      searchResults.style.display = 'none';
      searchInput.setAttribute('aria-expanded', 'false');
      searchStatus.textContent = '';
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
      searchInput.setAttribute('aria-expanded', 'true');
      searchStatus.textContent = 'Aucun resultat pour "' + query + '"';
      return;
    }

    var html = '';
    results.forEach(function(r, i) {
      html += '<a class="search-result-item" role="option" id="search-result-' + i + '" aria-selected="false" href="' + r.url + '">' +
              '<div class="search-result-title">' + r.title + '</div>' +
              '<div class="search-result-body">' + r.body.substring(0, 80) + '...</div>' +
              '</a>';
    });
    searchResults.innerHTML = html;
    searchResults.style.display = 'block';
    searchInput.setAttribute('aria-expanded', 'true');
    searchStatus.textContent = results.length + ' resultat' + (results.length > 1 ? 's' : '') + ' pour "' + query + '"';
  }

  searchInput.addEventListener('input', function() {
    performSearch(this.value.trim());
  });

  // Keyboard navigation in search results
  searchInput.addEventListener('keydown', function(e) {
    var items = searchResults.querySelectorAll('.search-result-item');
    if (items.length === 0) return;

    if (e.key === 'ArrowDown') {
      e.preventDefault();
      setActiveResult(activeIndex < items.length - 1 ? activeIndex + 1 : 0);
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setActiveResult(activeIndex > 0 ? activeIndex - 1 : items.length - 1);
    } else if (e.key === 'Enter' && activeIndex >= 0) {
      e.preventDefault();
      items[activeIndex].click();
    } else if (e.key === 'Escape') {
      searchResults.style.display = 'none';
      searchInput.setAttribute('aria-expanded', 'false');
      activeIndex = -1;
    }
  });

  // Close results when clicking outside
  document.addEventListener('click', function(e) {
    if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
      searchResults.style.display = 'none';
      searchInput.setAttribute('aria-expanded', 'false');
    }
  });

  // Reopen on focus if there's a query
  searchInput.addEventListener('focus', function() {
    if (this.value.trim().length >= 2) {
      performSearch(this.value.trim());
    }
  });
})();

// ========== TABLE CAPTIONS ==========
(function() {
  document.querySelectorAll('.chapter table').forEach(function(table) {
    if (table.querySelector('caption')) return; // already has one

    // Find the nearest preceding heading to use as caption
    var prev = table.previousElementSibling;
    var captionText = '';
    while (prev) {
      if (prev.tagName && /^H[1-6]$/.test(prev.tagName)) {
        captionText = prev.textContent.trim();
        break;
      }
      // Skip over <p> and other elements to find the heading
      if (prev.tagName === 'P' || prev.tagName === 'UL' || prev.tagName === 'OL' || prev.tagName === 'BLOCKQUOTE' || prev.tagName === 'DIV' || prev.tagName === 'HR') {
        prev = prev.previousElementSibling;
      } else {
        break;
      }
    }

    if (captionText) {
      var caption = document.createElement('caption');
      caption.className = 'sr-only';
      caption.textContent = 'Tableau : ' + captionText;
      table.insertBefore(caption, table.firstChild);
    }
  });
})();

// ========== GISCUS IFRAME ACCESSIBILITY ==========
(function() {
  var wrapper = document.querySelector('.giscus-wrapper');
  if (!wrapper) return;

  // Giscus injects an iframe asynchronously -- watch for it and add a title
  var observer = new MutationObserver(function(mutations) {
    var iframe = wrapper.querySelector('iframe.giscus-frame');
    if (iframe && !iframe.title) {
      iframe.title = 'Commentaires et discussions (via GitHub Discussions)';
      iframe.setAttribute('aria-label', 'Commentaires et discussions');
      observer.disconnect();
    }
  });
  observer.observe(wrapper, { childList: true, subtree: true });
})();

// ========== EXTERNAL LINK ACCESSIBILITY ==========
(function() {
  document.querySelectorAll('a[target="_blank"]').forEach(function(a) {
    // Skip if already has an indicator
    if (a.querySelector('.sr-only')) return;
    var hint = document.createElement('span');
    hint.className = 'sr-only';
    hint.textContent = ' (ouvre un nouvel onglet)';
    a.appendChild(hint);
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
