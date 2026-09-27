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
