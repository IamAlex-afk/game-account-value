// Glass skin helpers. All pricing stays in calculators.js; this file only
// wires UI around it. The markup (game tiles, result shell, action row,
// bot CTA) is pre-rendered in the HTML so nothing shifts on load (CLS);
// this script just makes it interactive:
//  - slider fill (--p) for the glowing track
//  - Reset button (reuses the calculator's own reset, gamepad "A")
//  - game tiles (.g-pick) drive the calculator's <select>
//  - phones: a mini bar mirrors the live price while the result is off-screen
(function () {
  "use strict";

  function paint(r) {
    var min = parseFloat(r.min) || 0, max = parseFloat(r.max) || 100;
    r.style.setProperty("--p", ((parseFloat(r.value) - min) / ((max - min) || 1) * 100) + "%");
  }
  function paintAll(root) {
    root.querySelectorAll('input[type="range"]').forEach(function (r) {
      paint(r);
      if (!r.dataset.gPaint) { r.dataset.gPaint = "1"; r.addEventListener("input", function () { paint(r); }); }
    });
  }

  function addReset(root) {
    var share = root.querySelector(".vc-share-btn");
    if (!share || root.querySelector(".g-reset")) return;
    var row = share.closest(".g-actions");
    if (!row) {
      row = document.createElement("div");
      row.className = "g-actions";
      share.parentNode.insertBefore(row, share);
      row.appendChild(share);
    }
    var reset = document.createElement("button");
    reset.type = "button";
    reset.className = "g-reset";
    // label = the calculator's own localized reset caption (gamepad "A")
    var cap = root.querySelector(".vc-btn-a");
    cap = cap && cap.parentNode.querySelector(".vc-btn-label");
    var text = cap ? cap.textContent.trim() : "";
    reset.textContent = "↺ " + text;
    reset.setAttribute("aria-label", text || "Reset");
    reset.addEventListener("click", function () {
      var a = root.querySelector(".vc-btn-a");
      if (a) a.click();
      paintAll(root);
    });
    row.appendChild(reset);
  }

  function wirePicker(root) {
    var pick = document.querySelector(".g-pick");
    var sel = root.querySelector(".vc-switcher");
    if (!pick || !sel) return;
    var btns = pick.querySelectorAll(".g-pick-btn[data-g]");
    btns.forEach(function (b) {
      b.addEventListener("click", function () {
        var id = b.getAttribute("data-g");
        var go = function () {
          sel.value = id;
          sel.dispatchEvent(new Event("change"));
          btns.forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
          paintAll(root);
        };
        if (document.startViewTransition && !matchMedia("(prefers-reduced-motion: reduce)").matches) document.startViewTransition(go); else go();
      });
    });
  }

  // Phones: the result card sits below the sliders, so while it is
  // off-screen a small bar mirrors the live price (tap = jump to result).
  function miniBar(root) {
    var result = root.querySelector(".vc-result"), value = root.querySelector(".vc-result-value");
    if (!document.querySelector(".g-tool") || !result || !value || !("IntersectionObserver" in window)) return;
    var bar = document.createElement("div");
    bar.className = "g-mini";
    bar.setAttribute("aria-hidden", "true");
    bar.innerHTML = '<span></span><a href="#' + root.id + '" tabindex="-1">↓</a>';
    document.body.appendChild(bar);
    var sync = function () { bar.firstChild.textContent = value.textContent; };
    new MutationObserver(sync).observe(value, { childList: true, subtree: true, characterData: true });
    sync();
    var sliders = root.querySelector(".vc-sliders"), resultSeen = false, slidersSeen = false;
    var update = function () { bar.classList.toggle("on", slidersSeen && !resultSeen); };
    new IntersectionObserver(function (es) { resultSeen = es[0].isIntersecting; update(); }).observe(result);
    if (sliders) new IntersectionObserver(function (es) { slidersSeen = es[0].isIntersecting; update(); }).observe(sliders);
  }

  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".value-calc").forEach(function (root) {
      paintAll(root); addReset(root); wirePicker(root); miniBar(root);
    });
  });
})();

/* Robot sitting on the result bar flashes when the estimate changes. */
(function () {
  var img = document.querySelector(".g-sit img"), val = document.querySelector(".vc-result-value");
  if (!img || !val || !window.MutationObserver) return;
  new MutationObserver(function () { img.classList.remove("blink"); void img.offsetWidth; img.classList.add("blink"); })
    .observe(val, { subtree: true, characterData: true, childList: true });
})();

/* Hero icons start flying after load, so they do not compete with first paint. */
window.addEventListener("load", function () { setTimeout(function () { document.documentElement.classList.add("gav-ld"); }, 400); });

/* Visual pack: cables from the cyborg into the calculator, holo tilt on game cards, slot roll of the estimate. */
(function () {
  var cy = document.querySelector(".g-cyborg");
  if (cy) {
    var ns = "http://www.w3.org/2000/svg", svg = document.createElementNS(ns, "svg");
    svg.setAttribute("class", "vis-cables"); svg.setAttribute("viewBox", "0 0 300 150"); svg.setAttribute("preserveAspectRatio", "none"); svg.setAttribute("aria-hidden", "true");
    var paths = ["M168 0 C 160 60, 110 70, 70 146", "M184 4 C 188 80, 150 100, 132 146", "M156 2 C 120 50, 50 80, 12 146"];
    paths.forEach(function (d, i) {
      ["c", "h", "p p" + (i + 1)].forEach(function (cls) { var p = document.createElementNS(ns, "path"); p.setAttribute("d", d); p.setAttribute("class", cls); svg.appendChild(p); });
    });
    [[70,146],[132,146],[12,146]].forEach(function (pt) { var r = document.createElementNS(ns, "rect"); r.setAttribute("x", pt[0]-6); r.setAttribute("y", pt[1]-4); r.setAttribute("width", 12); r.setAttribute("height", 9); r.setAttribute("rx", 2); r.setAttribute("class", "plug"); svg.appendChild(r); });
    cy.appendChild(svg);
  }
  var root = document.documentElement;
  document.addEventListener("click", function (e) {
    if (e.target.closest(".g-pick-btn")) { root.classList.add("vis-hot"); clearTimeout(root._vt); root._vt = setTimeout(function () { root.classList.remove("vis-hot"); }, 1600); }
  });
  document.querySelectorAll(".game-card, .g-pick-btn").forEach(function (c) {
    c.addEventListener("pointermove", function (e) {
      var r = c.getBoundingClientRect();
      c.style.setProperty("--hx", ((e.clientX - r.left) / r.width * 100).toFixed(0) + "%");
      c.style.setProperty("--hy", ((e.clientY - r.top) / r.height * 100).toFixed(0) + "%");
    });
  });
  var val = document.querySelector(".vc-result-value");
  if (val && window.MutationObserver) new MutationObserver(function () { val.classList.remove("vis-roll"); void val.offsetWidth; val.classList.add("vis-roll"); })
    .observe(val, { subtree: true, characterData: true, childList: true });
})();

/* Card collection carousel (homepages). */
(function () {
  var track = document.querySelector(".gc-track"); if (!track) return;
  var cards = [].slice.call(track.querySelectorAll(".gc-card")), cap = document.querySelector(".gc-cap"), dots = document.querySelector(".gc-dots");
  cards.forEach(function () { dots.appendChild(document.createElement("i")); });
  var cur = -1;
  function center(i, smooth) { var c = cards[i]; track.scrollTo({ left: c.offsetLeft - (track.clientWidth - c.clientWidth) / 2, behavior: smooth ? "smooth" : "auto" }); }
  function mark() {
    var mid = track.scrollLeft + track.clientWidth / 2, best = 0, bd = 1e9;
    cards.forEach(function (c, i) { var d = Math.abs(c.offsetLeft + c.clientWidth / 2 - mid); if (d < bd) { bd = d; best = i; } });
    if (best === cur) return; cur = best;
    cards.forEach(function (c, i) { c.classList.toggle("on", i === best); });
    [].forEach.call(dots.children, function (d, i) { d.classList.toggle("on", i === best); });
    cap.innerHTML = "<strong>" + cards[best].dataset.t + "</strong><span>" + cards[best].dataset.d + "</span>";
  }
  track.addEventListener("scroll", function () { requestAnimationFrame(mark); });
  document.querySelector(".gc-prev").onclick = function () { center(Math.max(0, cur - 1), true); };
  document.querySelector(".gc-next").onclick = function () { center(Math.min(cards.length - 1, cur + 1), true); };
  cards.forEach(function (c, i) {
    c.addEventListener("click", function () {
      if (i !== cur) { center(i, true); return; }
      c.classList.remove("play"); void c.offsetWidth; c.classList.add("play");
    });
  });
  var start = cards.findIndex(function (c) { return c.dataset.k === "diamond"; });
  requestAnimationFrame(function () { center(start < 0 ? 0 : start, false); mark(); setTimeout(function () { cards[cur].classList.add("play"); }, 600); });
})();
