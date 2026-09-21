(function () {
  var fab = document.querySelector('.fresh-news-fab');
  if (!fab) return;
  if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  if (window.matchMedia && window.matchMedia('(pointer: coarse)').matches) return;

  var radius = 90;
  var strength = 0.35;

  document.addEventListener('mousemove', function (e) {
    var rect = fab.getBoundingClientRect();
    var cx = rect.left + rect.width / 2;
    var cy = rect.top + rect.height / 2;
    var dx = e.clientX - cx;
    var dy = e.clientY - cy;
    var dist = Math.hypot(dx, dy);
    if (dist < radius) {
      var pull = (1 - dist / radius) * strength;
      fab.style.transform = 'translate(' + (dx * pull).toFixed(1) + 'px,' + (dy * pull).toFixed(1) + 'px)';
    } else {
      fab.style.transform = '';
    }
  });
})();
