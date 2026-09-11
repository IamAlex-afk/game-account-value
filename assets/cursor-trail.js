(function () {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  if (!window.matchMedia('(pointer: fine)').matches) return;

  var canvas = document.createElement('canvas');
  canvas.setAttribute('aria-hidden', 'true');
  canvas.style.cssText = 'position:fixed;inset:0;width:100vw;height:100vh;pointer-events:none;z-index:9998;';
  document.body.appendChild(canvas);
  var ctx = canvas.getContext('2d');

  function resize() {
    var dpr = window.devicePixelRatio || 1;
    canvas.width = window.innerWidth * dpr;
    canvas.height = window.innerHeight * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }
  resize();
  window.addEventListener('resize', resize);

  var colors = ['212,175,55', '18,184,146', '45,212,191']; // gold, emerald, accent — same brand palette as :root
  var particles = [];
  var lastX = null, lastY = null;

  document.addEventListener('pointermove', function (e) {
    if (e.pointerType && e.pointerType !== 'mouse') return;
    var dx = lastX === null ? 0 : e.clientX - lastX;
    var dy = lastY === null ? 0 : e.clientY - lastY;
    var dist = Math.sqrt(dx * dx + dy * dy);
    lastX = e.clientX; lastY = e.clientY;
    // Spawn count scales with pointer speed so a fast swipe gets a fuller tail
    // than a slow drift, instead of one dot per mousemove event.
    var count = Math.min(4, Math.max(1, Math.round(dist / 12)));
    for (var i = 0; i < count; i++) {
      particles.push({
        x: e.clientX,
        y: e.clientY,
        vx: (Math.random() - 0.5) * 0.4,
        vy: (Math.random() - 0.5) * 0.4 - 0.2,
        life: 1,
        size: 2 + Math.random() * 2.5,
        color: colors[Math.floor(Math.random() * colors.length)]
      });
    }
    if (particles.length > 200) particles.splice(0, particles.length - 200);
  }, { passive: true });

  function tick() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for (var i = particles.length - 1; i >= 0; i--) {
      var p = particles[i];
      p.life -= 0.025;
      if (p.life <= 0) { particles.splice(i, 1); continue; }
      p.x += p.vx;
      p.y += p.vy;
      var r = p.size * p.life * 3;
      var grad = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, r);
      grad.addColorStop(0, 'rgba(' + p.color + ',' + (0.55 * p.life) + ')');
      grad.addColorStop(1, 'rgba(' + p.color + ',0)');
      ctx.fillStyle = grad;
      ctx.beginPath();
      ctx.arc(p.x, p.y, r, 0, Math.PI * 2);
      ctx.fill();
    }
    requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
})();
