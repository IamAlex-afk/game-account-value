(function () {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var els = document.querySelectorAll('.stat-num');
  if (!els.length || !('IntersectionObserver' in window)) return;

  function animateCount(el) {
    var text = el.textContent;
    var match = text.match(/\d+/);
    if (!match) return;
    var target = parseInt(match[0], 10);
    var prefix = text.slice(0, match.index);
    var suffix = text.slice(match.index + match[0].length);
    var start = null;
    var duration = 1000;

    function tick(now) {
      if (start === null) start = now;
      var p = Math.min((now - start) / duration, 1);
      var eased = 1 - Math.pow(1 - p, 3);
      el.textContent = prefix + Math.round(target * eased) + suffix;
      if (p < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  }

  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        animateCount(entry.target);
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.5 });

  els.forEach(function (el) { observer.observe(el); });
})();
