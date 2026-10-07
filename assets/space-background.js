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
  var sysReduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var userStill = false;
  try { userStill = localStorage.getItem("gavMotion") === "off"; } catch (e) {}
  var reduce = sysReduce || userStill;
  if (userStill) document.documentElement.classList.add("gav-still");
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

  function img(src) { if (!images[src]) { var i = new Image(); i.decoding = "async"; i.src = BASE + src + "?v=7"; images[src] = i; } return images[src]; }
  function ready(i) { return i && i.complete && i.naturalWidth > 0; }
  function el(tag, css) { var e = document.createElement(tag); e.setAttribute("aria-hidden", "true"); e.style.cssText = css; return e; }

  function build() {
    dpr = Math.min(window.devicePixelRatio || 1, phone ? 1 : 1.5);
    // phones: size to the LARGE viewport (URL bar hidden) and never shrink, so the browser bar
    // sliding in/out while scrolling does not rescale the scene
    W = innerWidth; H = phone ? Math.max(H || 0, innerHeight, document.documentElement.clientHeight) : innerHeight;
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

  var lastPlace = "";
  function place(sy) {
    var key = mouse.x.toFixed(3) + "," + mouse.y.toFixed(3) + "," + W + "," + H;
    if (key === lastPlace) return; lastPlace = key;
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
    // comets: two kinds — a big slow one (rare) and a small quick one — entering from any edge and heading
    // across the screen. Each lights its path: a wide faint glow stays behind the head and fades in ~2 s.
    if (last > nextComet) {
      var big = rnd() < 0.3;
      nextComet = last + ((phone ? 15000 : 14000) + rnd() * 12000) * VIEW.cm;
      var edge = rnd(), sx, sy0;
      if (edge < 0.45) { sx = rnd() * W; sy0 = -30; } else if (edge < 0.65) { sx = -30; sy0 = rnd() * H * 0.7; }
      else if (edge < 0.85) { sx = W + 30; sy0 = rnd() * H * 0.7; } else { sx = rnd() * W; sy0 = H + 30; }
      var ax = W * (0.2 + rnd() * 0.6) - sx, ay = H * (0.2 + rnd() * 0.5) - sy0, an = Math.hypot(ax, ay) || 1;
      var v = big ? 0.3 + rnd() * 0.12 : 0.55 + rnd() * 0.3;
      comets.push({ x: sx, y: sy0, x0: sx, y0: sy0, vx: ax / an * v, vy: ay / an * v, v: v, k: big ? 1 : 0.55,
                    len: big ? 260 + rnd() * 120 : 120 + rnd() * 70, glow: big ? 2400 : 1500, a: 0, warm: rnd() < 0.5 });
    }
    fx.globalCompositeOperation = "lighter"; fx.lineCap = "round";
    for (i = comets.length - 1; i >= 0; i--) {
      var c = comets[i]; c.x += c.vx * dt; c.y += c.vy * dt; c.a = Math.min(1, c.a + dt / 500);
      var ux = c.vx / c.v, uy = c.vy / c.v, run = Math.hypot(c.x - c.x0, c.y - c.y0), gl = Math.min(run, c.v * c.glow);
      var gx = c.x - ux * gl, gy = c.y - uy * gl;                       // where the lit path has already gone dark
      if ((gx < -60 || gx > W + 60 || gy < -60 || gy > H + 60) && run > 200) { comets.splice(i, 1); continue; }
      var al = c.a, tint = c.warm ? "255,226,190" : "186,230,253";
      var g = fx.createLinearGradient(c.x, c.y, gx, gy);                 // the lit path
      g.addColorStop(0, "rgba(" + tint + "," + 0.2 * al + ")"); g.addColorStop(0.35, "rgba(" + tint + "," + 0.07 * al + ")"); g.addColorStop(1, "rgba(" + tint + ",0)");
      fx.strokeStyle = g; fx.lineWidth = 9 * c.k; fx.beginPath(); fx.moveTo(c.x, c.y); fx.lineTo(gx, gy); fx.stroke();
      var tl = Math.min(run, c.len), tx = c.x - ux * tl, ty = c.y - uy * tl;
      g = fx.createLinearGradient(c.x, c.y, tx, ty);                     // the bright tail
      g.addColorStop(0, "rgba(255,250,240," + 0.95 * al + ")"); g.addColorStop(0.18, "rgba(" + tint + "," + 0.45 * al + ")"); g.addColorStop(1, "rgba(" + tint + ",0)");
      fx.strokeStyle = g; fx.lineWidth = 2.6 * c.k; fx.beginPath(); fx.moveTo(c.x, c.y); fx.lineTo(tx, ty); fx.stroke();
      var hr = 12 * c.k, h = fx.createRadialGradient(c.x, c.y, 0, c.x, c.y, hr);   // the head
      h.addColorStop(0, "rgba(255,255,255," + al + ")"); h.addColorStop(0.3, "rgba(" + tint + "," + 0.5 * al + ")"); h.addColorStop(1, "rgba(" + tint + ",0)");
      fx.fillStyle = h; fx.beginPath(); fx.arc(c.x, c.y, hr, 0, TAU); fx.fill();
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
    var t = now - t0, sy = phone ? 0 : (window.scrollY || 0);   // no scroll-linked motion on phones (it lags native scrolling)
    mouse.x += (mouse.tx - mouse.x) * 0.05; mouse.y += (mouse.ty - mouse.y) * 0.05;
    place(sy); drawFar(t, dt, sy); drawNear(t, dt, sy);
    if (reduce) cancelAnimationFrame(raf);
  }

  // start-up is split into short steps so no single task blocks the page (body transparency and
  // hiding the old skyline are done in glass.css, so nothing here forces a full-page repaint)
  function step(fn) { if (window.requestIdleCallback) requestIdleCallback(fn, { timeout: 500 }); else setTimeout(fn, 16); }
  function start() {
    var body = document.body;
    var skySrc = phone ? "sky-phone.webp" : innerWidth > 1400 ? "sky-1920.webp" : "sky-1280.webp";
    sky = el("div", "position:fixed;left:-2%;top:-2%;width:104%;height:104vh;height:104lvh;z-index:-6;pointer-events:none;will-change:transform;background:#03050b url(" + BASE + skySrc + ") " + VIEW.pos + " / cover no-repeat;filter:hue-rotate(" + VIEW.hue + "deg)");
    body.insertBefore(sky, body.firstChild);
    step(function () {
      far = el("canvas", "position:fixed;left:0;top:0;width:100%;height:100vh;height:100lvh;z-index:-5;pointer-events:none;will-change:transform");
      near = el("canvas", "position:fixed;left:0;top:0;width:100%;height:100vh;height:100lvh;z-index:-3;pointer-events:none;will-change:transform");
      body.insertBefore(near, sky.nextSibling); body.insertBefore(far, near);
      fx = far.getContext("2d"); nx = near.getContext("2d");
      build();
      step(function () { OBJECTS.forEach(function (o) { if ((!phone || o.phone) && !(o.home && GAME)) img(o.src); }); step(run); });
    });
  }
  function run() {
    t0 = performance.now(); nextComet = t0 + 6000; nextEgg = t0 + (phone ? 1500 : 4000); nextUfo = t0 + 20000; nextPhone = t0 + (phone ? 4000 : 6000);
    if (finePointer && !phone && !reduce) {
      addEventListener("pointermove", function (e) { mouse.tx = e.clientX / W * 2 - 1; mouse.ty = e.clientY / H * 2 - 1; }, { passive: true });
      addEventListener("pointerdown", function (e) { if (e.pointerType === "mouse") waves.push({ x: e.clientX, y: e.clientY, t: last }); }, { passive: true });
    }
    raf = requestAnimationFrame(frame);
    var rt, lastW = innerWidth;
    addEventListener("resize", function () {
      if (phone && innerWidth === lastW) return;          // height-only change = URL bar, ignore
      lastW = innerWidth; H = 0; clearTimeout(rt); rt = setTimeout(function () { build(); lastPlace = ""; }, 200);
    });
    document.addEventListener("visibilitychange", function () {
      if (document.hidden) cancelAnimationFrame(raf); else if (!reduce) { last = 0; raf = requestAnimationFrame(frame); }
    });
  }
  // ---- WCAG 2.2.2: an on-page control to stop / resume all looping motion (footer, page language) ----
  var PAUSE = {
    en: ["Pause animation", "Play animation"], ru: ["Остановить анимацию", "Включить анимацию"],
    es: ["Pausar animación", "Reanudar animación"], pt: ["Pausar animação", "Retomar animação"],
    id: ["Jeda animasi", "Putar animasi"], tr: ["Animasyonu durdur", "Animasyonu başlat"],
    ar: ["إيقاف الحركة", "تشغيل الحركة"], vi: ["Tạm dừng hiệu ứng", "Bật hiệu ứng"],
    hi: ["एनिमेशन रोकें", "एनिमेशन चलाएँ"], fr: ["Mettre l’animation en pause", "Relancer l’animation"],
    de: ["Animation anhalten", "Animation abspielen"], it: ["Metti in pausa l’animazione", "Riprendi l’animazione"],
    ja: ["アニメーションを停止", "アニメーションを再生"], ko: ["애니메이션 멈추기", "애니메이션 재생"],
    th: ["หยุดภาพเคลื่อนไหว", "เล่นภาพเคลื่อนไหว"], pl: ["Zatrzymaj animację", "Wznów animację"],
    zh: ["暂停动画", "播放动画"], tl: ["I-pause ang animation", "I-play ang animation"],
    sw: ["Simamisha uhuishaji", "Endesha uhuishaji"], ms: ["Jeda animasi", "Mainkan animasi"],
    uz: ["Animatsiyani to‘xtatish", "Animatsiyani yoqish"], kk: ["Анимацияны тоқтату", "Анимацияны қосу"],
    tk: ["Animasiýany saklamak", "Animasiýany goşmak"], ky: ["Анимацияны токтотуу", "Анимацияны күйгүзүү"]
  };
  function motionButton() {
    var foot = document.querySelector("footer"); if (!foot || sysReduce) return;
    var lang = (document.documentElement.lang || "en").slice(0, 2), L = PAUSE[lang] || PAUSE.en;
    var b = document.createElement("button");
    b.type = "button"; b.className = "gav-motion";
    function label() { b.textContent = (userStill ? "▶ " : "⏸ ") + L[userStill ? 1 : 0]; b.setAttribute("aria-pressed", userStill ? "true" : "false"); }
    label();
    b.addEventListener("click", function () {
      userStill = !userStill; reduce = userStill;
      try { localStorage.setItem("gavMotion", userStill ? "off" : "on"); } catch (e) {}
      document.documentElement.classList.toggle("gav-still", userStill);
      if (userStill) { cancelAnimationFrame(raf); }
      else if (!started) { go(); }
      else { last = 0; raf = requestAnimationFrame(frame); }
      label();
    });
    var p = document.createElement("p"); p.className = "gav-motion-wrap"; p.appendChild(b);
    foot.insertBefore(p, foot.querySelector(".footer-logo") || foot.firstChild);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", motionButton); else motionButton();

  // start on the visitor's first move / scroll / touch, or 6 s after the page is loaded and idle —
  // whichever comes first. The scene must never compete with the page's own startup work.
  var started = false;
  function go() { if (started) return; started = true; EV.forEach(function (n) { removeEventListener(n, go); }); start(); }
  var EV = ["pointermove", "pointerdown", "touchstart", "keydown", "wheel"];   // real input only: browsers fire "scroll" on their own (anchors, restore)
  EV.forEach(function (n) { addEventListener(n, go, { passive: true, once: true }); });
  function later() {
    var idle = function () { setTimeout(go, phone ? 5000 : 6000); };
    if (window.requestIdleCallback) requestIdleCallback(idle, { timeout: 3000 }); else idle();
  }
  if (document.readyState === "complete") later(); else addEventListener("load", later);
})();
