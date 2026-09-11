(function () {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  if (!window.matchMedia('(pointer: fine)').matches) return;

  var targets = document.querySelectorAll('.game-card, .cert-sample img');

  targets.forEach(function (el) {
    el.addEventListener('mousemove', function (e) {
      var rect = el.getBoundingClientRect();
      var px = (e.clientX - rect.left) / rect.width - 0.5;
      var py = (e.clientY - rect.top) / rect.height - 0.5;
      var rotateY = px * 14;
      var rotateX = -py * 14;
      el.style.transform = 'perspective(700px) rotateX(' + rotateX.toFixed(2) + 'deg) rotateY(' + rotateY.toFixed(2) + 'deg) scale(1.03)';
    }, { passive: true });

    el.addEventListener('mouseleave', function () {
      el.style.transform = '';
    });
  });
})();
