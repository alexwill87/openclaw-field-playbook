// Toggle sidebar on mobile
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

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(function(a) {
  a.addEventListener('click', function(e) {
    var target = document.querySelector(this.getAttribute('href'));
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
});

// Active sidebar link on scroll
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
