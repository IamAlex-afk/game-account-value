document.querySelectorAll('.lang-selector').forEach(function (sel) {
  var btn = sel.querySelector('.lang-btn');
  btn.addEventListener('click', function (e) {
    e.stopPropagation();
    var isOpen = sel.classList.toggle('open');
    btn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
  });
});
document.addEventListener('click', function () {
  document.querySelectorAll('.lang-selector.open').forEach(function (sel) {
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
