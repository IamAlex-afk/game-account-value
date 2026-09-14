(function () {
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduceMotion) return;

  // Shared tilt math for both the mouse path (desktop, pointer:fine) and the
  // finger-drag path (mobile, pointer:coarse) below — px/py are -0.5..0.5
  // position within the element, same formula either way so the two feel
  // identical, just driven by a different input event.
  function applyTilt(el, px, py) {
    // 22deg/scale 1.06 (was 14deg/1.03) — the smaller rotation read as too
    // subtle to notice on a phone screen, this is a deliberately more
    // dramatic "expensive collectible" tilt.
    var rotateY = px * 22;
    var rotateX = -py * 22;
    el.style.transform = 'perspective(650px) rotateX(' + rotateX.toFixed(2) + 'deg) rotateY(' + rotateY.toFixed(2) + 'deg) scale(1.06)';
    var sheen = el._sheenEl;
    if (sheen) {
      // Two-layer holographic foil (the real technique real holo-card CSS
      // uses — see poke-holo.simey.me — not just one sliding gradient):
      // layer 1 (iris, set here) is a soft rainbow radial "under the foil"
      // wash via color-dodge, which is what actually reads as holographic;
      // layer 2 (glare, below) is the sharp directional light streak on
      // top. Neither alone looks like foil — together they do.
      var angle = 115 + px * 40;
      var pos = 50 + py * 40;
      sheen.style.background = 'linear-gradient(' + angle.toFixed(0) + 'deg, transparent 30%, rgba(255,255,255,0.22) ' + pos.toFixed(0) + '%, transparent 70%)';
      sheen.style.opacity = '1';
    }
    var iris = el._irisEl;
    if (iris) {
      var ix = (50 + px * 100).toFixed(0);
      var iy = (50 + py * 100).toFixed(0);
      iris.style.background = 'radial-gradient(circle at ' + ix + '% ' + iy + '%, rgba(255,80,140,0.35), rgba(255,210,80,0.3) 25%, rgba(80,255,180,0.3) 50%, rgba(80,160,255,0.35) 75%, transparent 90%)';
      iris.style.opacity = '0.55';
    }
  }

  function clearTilt(el) {
    el.style.transform = '';
    if (el._sheenEl) el._sheenEl.style.opacity = '0';
    if (el._irisEl) el._irisEl.style.opacity = '0';
  }

  // Wrap each target in a positioned container and inject the sheen + iris
  // layers — done here in JS (not in each language's index.html) so this
  // ships to all 8 full-language homepages from this one shared file, no
  // per-page markup edits needed.
  function addSheen(el) {
    var parent = el.parentElement;
    if (!parent || parent.classList.contains('tilt-sheen-wrap')) {
      el._sheenEl = el._sheenEl || (parent && parent.querySelector('.tilt-sheen'));
      el._irisEl = el._irisEl || (parent && parent.querySelector('.tilt-iris'));
      return;
    }
    var wrap = document.createElement('div');
    wrap.className = 'tilt-sheen-wrap';
    wrap.style.cssText = 'position:relative; display:inline-block; width:100%;';
    parent.insertBefore(wrap, el);
    wrap.appendChild(el);
    var iris = document.createElement('div');
    iris.className = 'tilt-iris';
    iris.style.cssText = 'position:absolute; inset:0; border-radius:inherit; pointer-events:none; opacity:0; transition:opacity .3s; mix-blend-mode:color-dodge;';
    wrap.appendChild(iris);
    var sheen = document.createElement('div');
    sheen.className = 'tilt-sheen';
    sheen.style.cssText = 'position:absolute; inset:0; border-radius:inherit; pointer-events:none; opacity:0; transition:opacity .25s; mix-blend-mode:overlay;';
    wrap.appendChild(sheen);
    el._sheenEl = sheen;
    el._irisEl = iris;
  }

  var targets = document.querySelectorAll('.game-card, .cert-sample img');

  if (window.matchMedia('(pointer: fine)').matches) {
    targets.forEach(function (el) {
      el.addEventListener('mousemove', function (e) {
        var rect = el.getBoundingClientRect();
        applyTilt(el, (e.clientX - rect.left) / rect.width - 0.5, (e.clientY - rect.top) / rect.height - 0.5);
      }, { passive: true });
      el.addEventListener('mouseleave', function () { clearTilt(el); });
    });
  }

  // Finger-drag tilt for touch screens — the mouse version only fires on
  // hover, which doesn't exist on touch, so this needs its own listener
  // path rather than reusing mousemove. Scoped to the certificate preview
  // only (not .game-card): dragging a finger across a 3x3 game grid would
  // fight normal page scrolling, but the single, large cert image has
  // enough dead space around it on a phone that a deliberate drag reads as
  // intentional, not an accidental scroll hijack.
  if (window.matchMedia('(pointer: coarse)').matches) {
    document.querySelectorAll('.cert-sample img').forEach(function (el) {
      addSheen(el);
      var dragging = false;
      el.addEventListener('touchstart', function (e) {
        dragging = true;
        el.style.transition = 'none';
        // Tiny tactile "pick it up" cue on grab. Android only — iOS Safari
        // has no Vibration API and silently no-ops, so this is safe
        // everywhere with no feature-detection branch needed beyond the
        // existence check itself.
        if (navigator.vibrate) navigator.vibrate(12);
      }, { passive: true });
      el.addEventListener('touchmove', function (e) {
        if (!dragging || !e.touches.length) return;
        var t = e.touches[0];
        var rect = el.getBoundingClientRect();
        applyTilt(el, (t.clientX - rect.left) / rect.width - 0.5, (t.clientY - rect.top) / rect.height - 0.5);
      }, { passive: true });
      var release = function () {
        dragging = false;
        el.style.transition = 'transform .35s cubic-bezier(.2,.8,.2,1)';
        clearTilt(el);
      };
      el.addEventListener('touchend', release, { passive: true });
      el.addEventListener('touchcancel', release, { passive: true });

      // Most mobile visitors scroll past without ever touching the card —
      // give them a one-time auto sweep when it enters view so the holo
      // effect isn't something only the minority who drag it ever see.
      // .tilt-idle-sweep is a plain CSS @keyframes animation (assets/style.css)
      // that plays once and removes itself; doesn't touch el.style.transform
      // at all, so it can never conflict with the drag path above.
      var wrap = el.closest('.tilt-sheen-wrap');
      if (wrap && 'IntersectionObserver' in window) {
        var io = new IntersectionObserver(function (entries) {
          entries.forEach(function (entry) {
            if (entry.isIntersecting) {
              wrap.classList.add('tilt-idle-sweep');
              io.disconnect();
            }
          });
        }, { threshold: 0.5 });
        io.observe(wrap);
      }
    });
  }
})();
