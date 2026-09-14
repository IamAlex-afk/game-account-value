(function () {
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduceMotion) return;

  // Shared tilt math for both the mouse path (desktop, pointer:fine) and the
  // finger-drag path (mobile, pointer:coarse) below — px/py are -0.5..0.5
  // position within the element, same formula either way so the two feel
  // identical, just driven by a different input event.
  function applyTilt(el, px, py) {
    var rotateY = px * 14;
    var rotateX = -py * 14;
    el.style.transform = 'perspective(700px) rotateX(' + rotateX.toFixed(2) + 'deg) rotateY(' + rotateY.toFixed(2) + 'deg) scale(1.03)';
    var sheen = el._sheenEl;
    if (sheen) {
      // Holographic trading-card sheen: a diagonal light band that slides
      // with the same px/py the tilt uses, so the "light" always seems to
      // come from wherever the cursor/finger is — matches the certificate's
      // own tiered-collectible-card concept (bot side: core/drawer.py).
      var angle = 115 + px * 40;
      var pos = 50 + py * 40;
      sheen.style.background = 'linear-gradient(' + angle.toFixed(0) + 'deg, transparent 30%, rgba(255,255,255,0.22) ' + pos.toFixed(0) + '%, transparent 70%)';
      sheen.style.opacity = '1';
    }
  }

  function clearTilt(el) {
    el.style.transform = '';
    if (el._sheenEl) el._sheenEl.style.opacity = '0';
  }

  // Wrap each target in a positioned container and inject the sheen layer —
  // done here in JS (not in each language's index.html) so this ships to
  // all 8 full-language homepages from this one shared file, no per-page
  // markup edits needed.
  function addSheen(el) {
    var parent = el.parentElement;
    if (!parent || parent.classList.contains('tilt-sheen-wrap')) { el._sheenEl = el._sheenEl || (parent && parent.querySelector('.tilt-sheen')); return; }
    var wrap = document.createElement('div');
    wrap.className = 'tilt-sheen-wrap';
    wrap.style.cssText = 'position:relative; display:inline-block; width:100%;';
    parent.insertBefore(wrap, el);
    wrap.appendChild(el);
    var sheen = document.createElement('div');
    sheen.className = 'tilt-sheen';
    sheen.style.cssText = 'position:absolute; inset:0; border-radius:inherit; pointer-events:none; opacity:0; transition:opacity .25s; mix-blend-mode:overlay;';
    wrap.appendChild(sheen);
    el._sheenEl = sheen;
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
    });
  }
})();
