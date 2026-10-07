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
// and appear as they enter the screen. Nothing is measured while the page loads: the observer itself reports where
// each block is (no forced layout), and a sweep after every scroll pause is the safety net.
(function () {
  var sel = '.section .feature, .section .step, .section .faq details, .section .game-card, .section .section-title, .hub-card, .cert-sample, .step, .feature';
  if (!('IntersectionObserver' in window) || !document.querySelectorAll) return;
  if (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var hidden = [];
  function show(e) {
    if (e.classList.contains('rv-in')) return;
    e.classList.add('rv-in');
    var k = hidden.indexOf(e); if (k >= 0) hidden.splice(k, 1);
    setTimeout(function () { e.classList.remove('rv', 'rv-in'); }, 900);
  }
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (x) {
      var e = x.target;
      if (!e.rvSeen) {                       // first report: hide only what lies below the screen
        e.rvSeen = 1;
        var h = x.rootBounds ? x.rootBounds.height : innerHeight;
        if (!x.isIntersecting && x.boundingClientRect.top > h) { e.classList.add('rv'); hidden.push(e); }
        else io.unobserve(e);
        return;
      }
      if (x.isIntersecting) { show(e); io.unobserve(e); }
    });
  }, { rootMargin: '0px 0px -5% 0px' });
  function init() { [].forEach.call(document.querySelectorAll(sel), function (e) { io.observe(e); }); }
  if (window.requestIdleCallback) requestIdleCallback(init, { timeout: 1500 }); else setTimeout(init, 300);
  function sweep() { hidden.slice().forEach(function (e) { if (e.getBoundingClientRect().top < innerHeight) show(e); }); }
  var t = 0;
  function soon() { if (!hidden.length) return; clearTimeout(t); t = setTimeout(sweep, 200); }
  addEventListener('scroll', soon, { passive: true }); addEventListener('touchend', soon, { passive: true });
  addEventListener('resize', soon); addEventListener('pageshow', soon);
})();
