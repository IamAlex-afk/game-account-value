(function () {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  if (!window.matchMedia('(pointer: fine)').matches) return;

  // Magnetic CTAs — button nudges toward the cursor within its own bounds.
  document.querySelectorAll('.btn-primary, .btn-secondary, .nav-cta').forEach(function (btn) {
    btn.addEventListener('mousemove', function (e) {
      var rect = btn.getBoundingClientRect();
      var x = e.clientX - rect.left - rect.width / 2;
      var y = e.clientY - rect.top - rect.height / 2;
      btn.style.transform = 'translate(' + (x * 0.25).toFixed(1) + 'px, ' + (y * 0.25).toFixed(1) + 'px)';
    }, { passive: true });
    btn.addEventListener('mouseleave', function () {
      btn.style.transform = '';
    });
  });

  // Spotlight glow that tracks the cursor, css vars read by .step::before /
  // details::before in style.css. Kept off .game-card/.cert-sample img —
  // those already tilt in 3D (see tilt.js) and stacking both reads as
  // clutter instead of polish.
  document.querySelectorAll('.step, details').forEach(function (el) {
    el.addEventListener('mousemove', function (e) {
      var rect = el.getBoundingClientRect();
      el.style.setProperty('--mx', ((e.clientX - rect.left) / rect.width * 100).toFixed(1) + '%');
      el.style.setProperty('--my', ((e.clientY - rect.top) / rect.height * 100).toFixed(1) + '%');
    }, { passive: true });
  });
})();
