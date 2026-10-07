// Phone header: one row (logo · bot · burger); the burger opens the menu + language.
(function () {
  var nav = document.querySelector('nav:not(.crumbs)');
  var burger = nav && nav.querySelector('.nav-burger');
  if (!burger) return;
  function setOpen(open) {
    nav.classList.toggle('nav-open', open);
    burger.setAttribute('aria-expanded', open ? 'true' : 'false');
  }
  burger.addEventListener('click', function (e) {
    e.stopPropagation();
    setOpen(!nav.classList.contains('nav-open'));
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && nav.classList.contains('nav-open')) { setOpen(false); burger.focus(); }
  });
})();

document.querySelectorAll('.lang-selector').forEach(function (sel) {
  var btn = sel.querySelector('.lang-btn');
  btn.addEventListener('click', function (e) {
    e.stopPropagation();
    var isOpen = sel.classList.toggle('open');
    btn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
  });
});
document.addEventListener('click', function (e) {
  document.querySelectorAll('.lang-selector.open').forEach(function (sel) {
    // A tap on one of the language links must not hide the dropdown
    // (display:none) while the same click is still mid-flight — some
    // mobile browsers (notably iOS Safari) cancel the link's navigation
    // if its container is hidden before the click finishes bubbling.
    // Desktop browsers tolerate it, which is why this only broke on phones.
    if (sel.contains(e.target)) return;
    sel.classList.remove('open');
    sel.querySelector('.lang-btn').setAttribute('aria-expanded', 'false');
  });
});
document.addEventListener('keydown', function (e) {
  if (e.key === 'Escape') {
    document.querySelectorAll('.lang-selector.open').forEach(function (sel) {
      sel.classList.remove('open');
    });
  }
});

(function () {
  var wrap = document.getElementById('pwa-install-wrap');
  var btn = document.getElementById('pwa-install-btn');
  if (!wrap || !btn) return;
  var deferredPrompt = null;
  window.addEventListener('beforeinstallprompt', function (e) {
    e.preventDefault();
    deferredPrompt = e;
    wrap.style.display = '';
  });
  btn.addEventListener('click', function () {
    if (!deferredPrompt) return;
    deferredPrompt.prompt();
    deferredPrompt.userChoice.finally(function () {
      deferredPrompt = null;
      wrap.style.display = 'none';
    });
  });
  window.addEventListener('appinstalled', function () {
    deferredPrompt = null;
    wrap.style.display = 'none';
  });
})();

// Register after load so the SW's precache download doesn't compete with
// the first page's own resources (web.dev "Service worker registration").
if ('serviceWorker' in navigator) {
  window.addEventListener('load', function () {
    navigator.serviceWorker.register('/sw.js').catch(function () {});
  });
}

// Reveal on scroll (was a scroll-driven CSS animation; see glass.css). Blocks below the first screen start hidden
// and appear as they enter the screen. Three safety nets so nothing can stay invisible: an observer, a sweep after
// every scroll pause and timers, and a final "show everything" if the observer is missing.
(function () {
  var sel = '.section .feature, .section .step, .section .faq details, .section .game-card, .section .section-title, .hub-card, .cert-sample, .step, .feature';
  if (!('IntersectionObserver' in window) || !document.querySelectorAll) return;
  if (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var els = [].slice.call(document.querySelectorAll(sel)).filter(function (e) { return e.getBoundingClientRect().top > innerHeight * 0.92; });
  if (!els.length) return;
  function show(e) {
    if (e.classList.contains('rv-in')) return;
    e.classList.add('rv-in');
    e.addEventListener('animationend', function () { e.classList.remove('rv', 'rv-in'); }, { once: true });
    setTimeout(function () { e.classList.remove('rv', 'rv-in'); }, 1200);
  }
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (x) { if (x.isIntersecting) { show(x.target); io.unobserve(x.target); } });
  }, { rootMargin: '0px 0px -5% 0px' });
  els.forEach(function (e) { e.classList.add('rv'); io.observe(e); });
  function sweep() { els.forEach(function (e) { if (e.classList.contains('rv') && e.getBoundingClientRect().top < innerHeight) show(e); }); }
  var t = 0;
  addEventListener('scroll', function () { clearTimeout(t); t = setTimeout(sweep, 200); }, { passive: true });
  addEventListener('resize', sweep); addEventListener('pageshow', sweep);
  setInterval(sweep, 1500);
})();
