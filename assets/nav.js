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

if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/game-account-value/sw.js').catch(function () {});
}
