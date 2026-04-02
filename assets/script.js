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
