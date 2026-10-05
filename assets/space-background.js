/* GameAccountValue — deep-space backdrop (v3, 2026-10-05). Decorative only: every layer is
   aria-hidden, pointer-events:none and sits behind the page (negative z-index).

   Layers, far to near (one light source: the sun in the top-left of the sky image, so every
   object below is lit from the upper left too):
     1. sky        photoreal star field + sun (CSS background)              mouse parallax 6px
     2. far canvas twinkling stars, comets (comets pass BEHIND the planets) mouse parallax 10px
     3. planets    gas giant and Mars (perfect discs, shaded in code-free bake: no black night side)          mouse 14-26px, scroll
     4. near canvas old satellite, skeleton astronaut, android, drone, a rare UFO, and game-item
                   "easter eggs" (12 loot items: helmet, airdrop, chest, trophy, sword...) that fade in
                   one at a time near the edges; soft wave on click            mouse parallax 30px
   The existing cursor trail (assets/cursor-trail.js, z-index 9998) is untouched.
   Budget: starts after load (no effect on LCP), pauses in hidden tabs, ~30 fps and fewer
   objects on phones (no mouse there), one still frame for prefers-reduced-motion.
   No libraries, no third-party requests. */
(function () {
  "use strict";
  var me = document.currentScript && document.currentScript.src;
  var BASE = me ? me.replace(/space-background\.js.*$/, "space/") : "/assets/space/";
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var finePointer = window.matchMedia && matchMedia("(pointer: fine)").matches;
  var phone = Math.min(screen.width, screen.height) < 600;
  var TAU = Math.PI * 2, rnd = Math.random;
  var W = 0, H = 0, dpr = 1, last = 0, t0 = 0, raf = 0;
  var far, fx, near, nx, sky, planetEls = [], stars = [], comets = [], waves = [], nextComet = 0;
  var mouse = { x: 0, y: 0, tx: 0, ty: 0 };

  // persistent objects: position as a fraction of the screen, width in px at a 1000px-wide screen,
  // slow drift (px/s), spin (rad/s), scroll parallax, mouse depth (px)
  // wanderers: start spread over the screen, then each slowly drifts to a new random spot,
  // always keeping away from the others; they do NOT follow the page scroll
  var OBJECTS = [
    { src: "satellite.webp", x: 0.30, y: 0.22, w: 170, spin: -0.02, m: 22, phone: true },
    { src: "astronaut.webp", x: 0.08, y: 0.70, w: 165, spin: 0.025, m: 28, phone: true },
    { src: "robot.webp", x: 0.90, y: 0.55, w: 105, spin: 0.012, m: 26, home: true }
  ];
  var EGGS = ["item-helmet.webp", "item-trophy.webp", "item-airdrop.webp", "item-potion.webp", "item-chest.webp", "item-headset.webp",
              "item-backpack.webp", "item-coins.webp", "item-gamepad.webp", "item-sword.webp", "item-crystal.webp", "item-lootcrate.webp"];
  // game pages (any language, the game page, its news hub and its articles) get that game's own loot set
  var GAMES = { "roblox": 3, "brawl-stars": 6, "clash-of-clans": 6, "clash-royale": 6, "free-fire": 6,
                "genshin-impact": 6, "mobile-legends": 6, "fortnite": 6, "minecraft": 5 };
  var GAME = null, GI = 0;
  Object.keys(GAMES).forEach(function (g, i) {
    if (new RegExp("/(news-)?" + g + "(-news|-[0-9]{4}-[a-z0-9-]+)?[.]html$").test(location.pathname)) { GAME = g; GI = i + 1; }
  });
  if (GAME) { EGGS = []; for (var gi = 1; gi <= GAMES[GAME]; gi++) EGGS.push("g-" + GAME + "-" + gi + ".webp"); }
  // phone evolution: one at a time, oldest first, continues from page to page within the visit
  var PHONES = ["phone-1.webp", "phone-2.webp", "phone-3.webp", "phone-4.webp", "phone-5.webp", "phone-6.webp"], phoneObj = null, nextPhone = 0, phoneIdx = 0;
  try { phoneIdx = +(sessionStorage.getItem("gavPhone") || 0) % PHONES.length; } catch (e) {}
  // each game page sees the scene from its own angle: sky crop, tint and planet layout
  var VIEW = [
    { pos: "center top", hue: 0, P: 0, st: 1.0, cm: 1.0, ax: 0.08, ay: 0.7, as: 1.0 },
    { pos: "20% 10%", hue: 25, P: 1, st: 1.4, cm: 0.7, ax: 0.88, ay: 0.3, as: 0.8 },
    { pos: "80% 30%", hue: -20, P: 2, st: 0.8, cm: 1.3, ax: 0.1, ay: 0.25, as: 1.1 },
    { pos: "40% 60%", hue: 40, P: 1, st: 1.2, cm: 1.0, ax: 0.9, ay: 0.75, as: 0.7 },
    { pos: "65% 15%", hue: -35, P: 2, st: 0.9, cm: 0.8, ax: 0.06, ay: 0.62, as: 1.0 },
    { pos: "10% 45%", hue: 15, P: 1, st: 1.5, cm: 0.6, ax: 0.85, ay: 0.2, as: 0.9 },
    { pos: "90% 70%", hue: -10, P: 2, st: 1.6, cm: 1.4, ax: 0.12, ay: 0.4, as: 0.75 },
    { pos: "50% 35%", hue: 55, P: 1, st: 1.0, cm: 0.9, ax: 0.92, ay: 0.65, as: 1.15 },
    { pos: "30% 85%", hue: -45, P: 2, st: 1.3, cm: 0.6, ax: 0.05, ay: 0.8, as: 0.85 },
    { pos: "70% 50%", hue: 30, P: 1, st: 0.7, cm: 1.6, ax: 0.8, ay: 0.35, as: 1.05 }
  ][GI];
  OBJECTS.forEach(function (o) { if (o.src === "astronaut.webp") { o.x = VIEW.ax; o.y = VIEW.ay; o.w = Math.round(o.w * VIEW.as); } });
  var eggs = [], nextEgg = 0, eggIdx = Math.floor(rnd() * EGGS.length), ufo = null, nextUfo = 0;
  var images = {};

  function img(src) { if (!images[src]) { var i = new Image(); i.decoding = "async"; i.src = BASE + src; images[src] = i; } return images[src]; }
  function ready(i) { return i && i.complete && i.naturalWidth > 0; }
  function el(tag, css) { var e = document.createElement(tag); e.setAttribute("aria-hidden", "true"); e.style.cssText = css; return e; }

  function build() {
    dpr = Math.min(window.devicePixelRatio || 1, phone ? 1 : 1.5);
    W = innerWidth; H = innerHeight;
    [far, near].forEach(function (c) { c.width = Math.round(W * dpr); c.height = Math.round(H * dpr); c.getContext("2d").setTransform(dpr, 0, 0, dpr, 0, 0); });
    var n = Math.round(Math.min(phone ? 60 : 160, W * H / 10000) * VIEW.st);
    stars = [];
    for (var i = 0; i < n; i++) stars.push({ x: rnd() * W, y: rnd() * H * 1.3, r: rnd() < 0.1 ? 1.3 : 0.4 + rnd() * 0.7, d: 0.01 + rnd() * 0.04, p: rnd() * TAU, s: 0.4 + rnd() * 1.4 });
    // planets: big one cropped at the bottom-right, the ringed giant far away on the left
    var m = Math.min(W, H);
    var LAY = [   // x, y = planet centre as a fraction of the screen; always at the edges, partly off-screen
      [{ src: "planet-giant.webp", w: 0.22, x: -0.02, y: 0.42, op: 0.85 }, { src: "planet-mars.webp", w: 0.42, x: 0.97, y: 0.92, op: 0.95 }],
      [{ src: "planet-mars.webp", w: 0.38, x: 0.0, y: 0.95, op: 0.95 }, { src: "planet-giant.webp", w: 0.2, x: 0.99, y: 0.32, op: 0.85 }],
      [{ src: "planet-giant.webp", w: 0.36, x: 1.0, y: 0.9, op: 0.9 }, { src: "planet-mars.webp", w: 0.18, x: -0.01, y: 0.3, op: 0.85 }]
    ][VIEW.P];
    var P = LAY.map(function (l) { return { src: l.src, w: m * l.w * (phone ? 1.4 : 1), x: l.x, y: l.y, d: 0.02, mm: 14 + l.w * 20, op: l.op }; });

    P.forEach(function (p, k) {
      var e = planetEls[k];
      if (!e) { e = el("img", "position:fixed;left:0;top:0;z-index:-4;pointer-events:none;will-change:transform;user-select:none"); e.alt = ""; e.decoding = "async"; e.src = BASE + p.src; document.body.insertBefore(e, near); planetEls[k] = e; }
      e._p = p; e.style.width = Math.round(p.w) + "px"; e.style.opacity = p.op;
    });
  }

  function place(sy) {
    sky.style.transform = "translate3d(" + (-mouse.x * 6) + "px," + (-mouse.y * 6) + "px,0) scale(1.03)";
    far.style.transform = "translate3d(" + (-mouse.x * 10) + "px," + (-mouse.y * 10) + "px,0)";
    near.style.transform = "translate3d(" + (-mouse.x * 30) + "px," + (-mouse.y * 30) + "px,0)";
    for (var i = 0; i < planetEls.length; i++) {
      var e = planetEls[i], p = e._p;
      var half = p.w / 2, x = p.x * W - half - mouse.x * p.mm, y = p.y * H - half - mouse.y * p.mm;   // p.x/p.y = centre
      e.style.transform = "translate3d(" + Math.round(x) + "px," + Math.round(y) + "px,0)";
    }
  }

  function drawFar(t, dt, sy) {
    fx.clearRect(0, 0, W, H);
    for (var i = 0; i < stars.length; i++) {
      var s = stars[i], y = ((s.y - sy * s.d) % (H * 1.3) + H * 1.3) % (H * 1.3) - H * 0.15;
      fx.globalAlpha = 0.2 + 0.7 * (0.5 + 0.5 * Math.sin(t * 0.001 * s.s + s.p));
      fx.fillStyle = "#fff"; fx.beginPath(); fx.arc(s.x, y, s.r, 0, TAU); fx.fill();
    }
    fx.globalAlpha = 1;
    // comets: rare, from the sun's side, fast, soft tail
    if (last > nextComet) {
      nextComet = last + ((phone ? 9000 : 5000) + rnd() * 7000) * VIEW.cm;
      var v = 0.45 + rnd() * 0.35;
      comets.push({ x: W * (0.15 + rnd() * 0.5), y: -40, vx: v * (0.6 + rnd() * 0.6), vy: v * (0.45 + rnd() * 0.35), len: 160 + rnd() * 200, a: 0 });
    }
    fx.globalCompositeOperation = "lighter";
    for (i = comets.length - 1; i >= 0; i--) {
      var c = comets[i]; c.x += c.vx * dt; c.y += c.vy * dt; c.a = Math.min(1, c.a + dt / 400);
      var fade = c.y > H * 0.75 ? Math.max(0, 1 - (c.y - H * 0.75) / (H * 0.25)) : 1;
      if (c.x > W + 300 || c.y > H + 100) { comets.splice(i, 1); continue; }
      var k = Math.hypot(c.vx, c.vy), tx = c.x - c.vx / k * c.len, ty = c.y - c.vy / k * c.len, al = c.a * fade;
      var g = fx.createLinearGradient(c.x, c.y, tx, ty);
      g.addColorStop(0, "rgba(255,250,240," + 0.9 * al + ")"); g.addColorStop(0.2, "rgba(186,230,253," + 0.35 * al + ")"); g.addColorStop(1, "rgba(186,230,253,0)");
      fx.strokeStyle = g; fx.lineWidth = 1.8; fx.lineCap = "round"; fx.beginPath(); fx.moveTo(c.x, c.y); fx.lineTo(tx, ty); fx.stroke();
      var h = fx.createRadialGradient(c.x, c.y, 0, c.x, c.y, 7); h.addColorStop(0, "rgba(255,255,255," + al + ")"); h.addColorStop(1, "rgba(255,255,255,0)");
      fx.fillStyle = h; fx.beginPath(); fx.arc(c.x, c.y, 7, 0, TAU); fx.fill();
    }
    fx.globalCompositeOperation = "source-over";
  }

  function pickTarget(o, w) {
    // a random spot on screen, at least ~35% of the screen away from every other wanderer
    var best = null, bestD = -1;
    for (var tries = 0; tries < 12; tries++) {
      var x = w / 2 + rnd() * (W - w), y = H * 0.12 + w / 2 + rnd() * (H * 0.86 - w), dmin = 1e9;
      for (var j = 0; j < OBJECTS.length; j++) {
        var q = OBJECTS[j]; if (q === o || q.px === undefined || (phone && !q.phone)) continue;
        dmin = Math.min(dmin, Math.hypot(x - (q.tx !== undefined ? q.tx : q.px), y - (q.ty !== undefined ? q.ty : q.py)));
      }
      if (dmin > bestD) { bestD = dmin; best = [x, y]; }
      if (dmin > Math.min(W, H) * 0.35 * 1.4) break;
    }
    o.tx = best[0]; o.ty = best[1];
  }

  function sprite(i, cxp, cyp, w, rot, alpha) {
    var h = w * i.naturalHeight / i.naturalWidth;
    // on phones the whole screen is the text column: objects a bit see-through
    nx.save(); nx.globalAlpha = alpha * (phone ? 0.75 : 1); nx.translate(cxp, cyp); nx.rotate(rot); nx.drawImage(i, -w / 2, -h / 2, w, h); nx.restore();
  }

  function drawNear(t, dt, sy) {
    nx.clearRect(0, 0, W, H);
    var sec = t / 1000, scale = phone ? Math.max(0.55, Math.min(0.8, W / 520)) : Math.max(0.6, Math.min(1.2, W / 1000));
    for (var k = 0; k < OBJECTS.length; k++) {
      var o = OBJECTS[k]; if ((phone && !o.phone) || (o.home && GAME)) continue;
      var im = img(o.src); if (!ready(im)) continue;
      var w = o.w * scale;
      if (o.px === undefined) { o.px = o.x * W; o.py = o.y * H; pickTarget(o, w); }
      var dx = o.tx - o.px, dy = o.ty - o.py, dist = Math.hypot(dx, dy), speed = (phone ? 6 : 9) * dt / 1000;
      if (dist < 4) pickTarget(o, w); else { o.px += dx / dist * speed; o.py += dy / dist * speed; }
      // fade a little while crossing the text column, so reading is never harder
      var mid = 1 - Math.min(1, Math.abs(o.px / W - 0.5) / 0.32);
      sprite(im, o.px, o.py + Math.sin(sec * 0.3 + k) * 8, w, sec * o.spin + Math.sin(sec * 0.2 + k) * 0.06, 0.92 - 0.5 * mid);
    }
    // game-item easter eggs: up to 2 (1 on phones) at once, anywhere on screen away from the
    // wanderers, fade in, drift and spin slowly for ~12 s, fade out
    var maxEggs = phone ? 1 : 2;
    if (eggs.length < maxEggs && last > nextEgg) {
      var src = EGGS[eggIdx++ % EGGS.length], ex = 0, ey = 0, bestD = -1;
      for (var tr = 0; tr < 10; tr++) {
        var cx2 = W * (0.05 + rnd() * 0.9), cy2 = H * (0.15 + rnd() * 0.75), dm = 1e9;
        OBJECTS.concat(eggs).forEach(function (q) { if (q.px !== undefined) dm = Math.min(dm, Math.hypot(cx2 - q.px, cy2 - q.py)); });
        if (dm > bestD) { bestD = dm; ex = cx2; ey = cy2; }
      }
      eggs.push({ src: src, px: ex, py: ey, vx: (rnd() - 0.5) * 8, vy: (rnd() - 0.5) * 6, spin: (rnd() - 0.5) * 0.3, born: last, life: 12000 });
      img(src); nextEgg = last + (phone ? 9000 : 4500) + rnd() * 4000;
    }
    for (var ei2 = eggs.length - 1; ei2 >= 0; ei2--) {
      var eg = eggs[ei2], eimg = img(eg.src), age = last - eg.born;
      if (age > eg.life) { eggs.splice(ei2, 1); continue; }
      eg.px += eg.vx * dt / 1000; eg.py += eg.vy * dt / 1000;
      if (!ready(eimg)) continue;
      var ea = Math.min(1, age / 1500, (eg.life - age) / 1500), emid = 1 - Math.min(1, Math.abs(eg.px / W - 0.5) / 0.32);
      sprite(eimg, eg.px, eg.py, 95 * scale, age / 1000 * eg.spin, ea * (0.95 - 0.5 * emid));
    }
    // phone evolution: every ~25 s one phone floats across, oldest first
    if (!phoneObj && last > nextPhone) {
      var fromL = rnd() < 0.5;
      phoneObj = { src: PHONES[phoneIdx], x: fromL ? -60 : W + 60, y: H * (0.2 + rnd() * 0.55), vx: (fromL ? 1 : -1) * (phone ? 26 : 34), spin: (rnd() - 0.5) * 0.4, born: last };
      img(phoneObj.src); phoneIdx = (phoneIdx + 1) % PHONES.length;
      try { sessionStorage.setItem("gavPhone", phoneIdx); } catch (e) {}
    }
    if (phoneObj) {
      var pim = img(phoneObj.src), pa = (last - phoneObj.born) / 1000, ppx = phoneObj.x + phoneObj.vx * pa;
      if (ppx < -120 || ppx > W + 120) { phoneObj = null; nextPhone = last + (phone ? 30000 : 20000) + rnd() * 10000; }
      else if (ready(pim)) {
        var pmid = 1 - Math.min(1, Math.abs(ppx / W - 0.5) / 0.32);
        sprite(pim, ppx, phoneObj.y + Math.sin(pa * 0.8) * 10, 80 * scale, pa * phoneObj.spin, 0.95 - 0.5 * pmid);
      }
    }
    // rare UFO crossing far away (small)
    if (!ufo && last > nextUfo && !phone) {
      ufo = { y: H * (0.1 + rnd() * 0.25), dir: rnd() < 0.5 ? 1 : -1, born: last };
    }
    if (ufo) {
      var ui = img("ufo.webp"), ua = (last - ufo.born) / 1000, uw = 46 * scale, ux = ufo.dir > 0 ? -60 + ua * 140 : W + 60 - ua * 140;
      if (ux < -80 || ux > W + 80) { ufo = null; nextUfo = last + 40000 + rnd() * 30000; }
      else if (ready(ui)) sprite(ui, ux, ufo.y + Math.sin(ua * 2) * 6, uw, Math.sin(ua * 3) * 0.05, 0.85);
    }
    // click wave: short, nearly transparent
    for (var i = waves.length - 1; i >= 0; i--) {
      var wv = waves[i], p = (last - wv.t) / 700;
      if (p >= 1) { waves.splice(i, 1); continue; }
      nx.strokeStyle = "rgba(165,243,252," + 0.22 * (1 - p) + ")"; nx.lineWidth = 1.5;
      nx.beginPath(); nx.arc(wv.x + mouse.x * 30, wv.y + mouse.y * 30, 10 + p * 110, 0, TAU); nx.stroke();
    }
  }

  function frame(now) {
    raf = requestAnimationFrame(frame);
    if (phone && now - last < 33) return;
    var dt = Math.min(64, now - (last || now)); last = now;
    var t = now - t0, sy = window.scrollY || 0;
    mouse.x += (mouse.tx - mouse.x) * 0.05; mouse.y += (mouse.ty - mouse.y) * 0.05;
    place(sy); drawFar(t, dt, sy); drawNear(t, dt, sy);
    if (reduce) cancelAnimationFrame(raf);
  }

  function start() {
    var body = document.body;
    var skySrc = phone ? "sky-phone.webp" : innerWidth > 1400 ? "sky-1920.webp" : "sky-1280.webp";
    sky = el("div", "position:fixed;inset:-2%;z-index:-6;pointer-events:none;will-change:transform;background:#03050b url(" + BASE + skySrc + ") " + VIEW.pos + " / cover no-repeat;filter:hue-rotate(" + VIEW.hue + "deg)");
    far = el("canvas", "position:fixed;inset:0;width:100%;height:100%;z-index:-5;pointer-events:none;will-change:transform");
    near = el("canvas", "position:fixed;inset:0;width:100%;height:100%;z-index:-3;pointer-events:none;will-change:transform");
    body.insertBefore(near, body.firstChild); body.insertBefore(far, body.firstChild); body.insertBefore(sky, body.firstChild);
    body.style.background = "transparent";               // let the fixed layers show; <html> keeps the base colour
    // the hero's old skyline layer (city, rain and its dark gradient overlay) is hidden only while the space scene runs — the markup stays
    [].forEach.call(document.querySelectorAll(".g-fx"), function (e) { e.style.display = "none"; });
    fx = far.getContext("2d"); nx = near.getContext("2d");
    OBJECTS.forEach(function (o) { if ((!phone || o.phone) && !(o.home && GAME)) img(o.src); });
    build(); t0 = performance.now(); nextComet = t0 + 2500; nextEgg = t0 + (phone ? 1500 : 4000); nextUfo = t0 + 20000; nextPhone = t0 + (phone ? 4000 : 6000);
    if (finePointer && !phone && !reduce) {
      addEventListener("pointermove", function (e) { mouse.tx = e.clientX / W * 2 - 1; mouse.ty = e.clientY / H * 2 - 1; }, { passive: true });
      addEventListener("pointerdown", function (e) { if (e.pointerType === "mouse") waves.push({ x: e.clientX, y: e.clientY, t: last }); }, { passive: true });
    }
    raf = requestAnimationFrame(frame);
    var rt; addEventListener("resize", function () { clearTimeout(rt); rt = setTimeout(build, 200); });
    document.addEventListener("visibilitychange", function () {
      if (document.hidden) cancelAnimationFrame(raf); else if (!reduce) { last = 0; raf = requestAnimationFrame(frame); }
    });
  }
  // start on the visitor's first move / scroll / touch, or 6 s after the page is loaded and idle —
  // whichever comes first. The scene must never compete with the page's own startup work.
  var started = false;
  function go() { if (started) return; started = true; EV.forEach(function (n) { removeEventListener(n, go); }); start(); }
  var EV = ["pointermove", "scroll", "touchstart", "keydown"];
  EV.forEach(function (n) { addEventListener(n, go, { passive: true, once: true }); });
  function later() {
    var idle = function () { setTimeout(go, phone ? 2500 : 6000); };
    if (window.requestIdleCallback) requestIdleCallback(idle, { timeout: 3000 }); else idle();
  }
  if (document.readyState === "complete") later(); else addEventListener("load", later);
})();
