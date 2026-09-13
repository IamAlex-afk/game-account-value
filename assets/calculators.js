(function () {
  "use strict";

  function lerp(t, a, b) { return a + (b - a) * t; }

  function norm(v, min, max) {
    if (max === min) return 0;
    var t = (v - min) / (max - min);
    return t < 0 ? 0 : t > 1 ? 1 : t;
  }

  // brackets: array of [low, high] anchor points spaced evenly across the 0..1 score.
  // These anchor values are copied verbatim from each page's own published price table —
  // the slider only interpolates between real, already-cited numbers, it never invents new ones.
  function interpBrackets(score, brackets) {
    var n = brackets.length;
    var scaled = score * (n - 1);
    var i = Math.min(Math.floor(scaled), n - 2);
    var t = scaled - i;
    var lo = lerp(t, brackets[i][0], brackets[i + 1][0]);
    var hi = lerp(t, brackets[i][1], brackets[i + 1][1]);
    return [lo, hi];
  }

  function formatMoney(n) {
    if (n < 10) return "$" + n.toFixed(2).replace(/\.00$/, "");
    if (n < 1000) return "$" + Math.round(n);
    var rounded = n < 10000 ? Math.round(n / 10) * 10 : Math.round(n / 100) * 100;
    return "$" + rounded.toLocaleString("en-US");
  }

  // --- per-game compute functions -----------------------------------------
  // Every bracket below is taken directly from that game's own "Real Market
  // Prices" table on the same page — see the <table class="tier-table"> there.
  var GAMES = {
    "brawl-stars": {
      sliders: [
        { key: "trophies", label: "Трофеи (кубки)", min: 5000, max: 45000, step: 1000, fmt: function (v) { return v.toLocaleString("en-US"); } },
        { key: "maxed", label: "Бойцы Power Level 11", min: 0, max: 85, step: 1, fmt: function (v) { return v; } }
      ],
      compute: function (v) {
        var score = 0.5 * norm(v.trophies, 5000, 45000) + 0.5 * norm(v.maxed, 0, 85);
        return interpBrackets(score, [[3, 15], [15, 50], [50, 150], [150, 300]]);
      }
    },
    "clash-of-clans": {
      sliders: [
        { key: "th", label: "Уровень Ратуши (Town Hall)", min: 13, max: 18, step: 1, fmt: function (v) { return "TH" + v; } }
      ],
      select: { key: "type", label: "Тип прокачки", options: [["full", "Full Max"], ["standard", "Стандартный"], ["rushed", "Rushed"]] },
      compute: function (v) {
        var table = {
          18: { full: [100, 260], standard: [45, 120], rushed: [20, 35] },
          17: { full: [55, 185], standard: [30, 50], rushed: [30, 55] },
          16: { full: [40, 100], standard: [20, 35], rushed: [15, 25] },
          15: { full: [30, 65], standard: [15, 25], rushed: [15, 20] },
          14: { full: [25, 50], standard: [15, 25], rushed: [10, 20] },
          13: { full: [15, 40], standard: [10, 15], rushed: [8, 12] }
        };
        return table[v.th][v.type];
      }
    },
    "clash-royale": {
      sliders: [
        { key: "kt", label: "Уровень King Tower", min: 9, max: 15, step: 1, fmt: function (v) { return "KT" + v; } },
        { key: "maxed", label: "Карт максимального уровня", min: 0, max: 40, step: 1, fmt: function (v) { return v; } }
      ],
      compute: function (v) {
        var score = 0.5 * norm(v.kt, 9, 15) + 0.5 * norm(v.maxed, 0, 40);
        return interpBrackets(score, [[0.5, 15], [15, 50], [50, 150], [150, 300]]);
      }
    },
    "free-fire": {
      sliders: [
        { key: "rank", label: "Ранг", min: 1, max: 7, step: 1, fmt: function (v) {
          return ["Bronze", "Silver", "Gold", "Platinum", "Diamond", "Heroic", "Grandmaster"][v - 1];
        } },
        { key: "bundles", label: "Редких бандлов/питомцев", min: 0, max: 10, step: 1, fmt: function (v) { return v; } }
      ],
      compute: function (v) {
        var score = 0.5 * norm(v.rank, 1, 7) + 0.5 * norm(v.bundles, 0, 10);
        return interpBrackets(score, [[0.73, 15], [15, 50], [50, 150], [150, 300]]);
      }
    },
    "genshin-impact": {
      sliders: [
        { key: "fivestars", label: "5★ персонажей", min: 0, max: 20, step: 1, fmt: function (v) { return v; } },
        { key: "c6", label: "Персонажей с C6", min: 0, max: 20, step: 1, fmt: function (v) { return v; } }
      ],
      compute: function (v) {
        if (v.fivestars < 3) return [5, 60];
        var score = 0.5 * norm(v.fivestars, 3, 20) + 0.5 * norm(v.c6, 0, 20);
        return interpBrackets(score, [[30, 200], [300, 1000], [1000, 4200], [8400, 8995]]);
      }
    },
    "mobile-legends": {
      sliders: [
        { key: "skins", label: "Всего скинов", min: 0, max: 400, step: 10, fmt: function (v) { return v; } },
        { key: "rank", label: "Ранг", min: 1, max: 7, step: 1, fmt: function (v) {
          return ["Warrior", "Elite", "Master", "Grandmaster", "Epic", "Legend", "Mythical Glory"][v - 1];
        } }
      ],
      compute: function (v) {
        var score = 0.5 * norm(v.skins, 0, 400) + 0.5 * norm(v.rank, 1, 7);
        return interpBrackets(score, [[0.5, 15], [15, 50], [50, 150], [150, 300]]);
      }
    },
    "fortnite": {
      sliders: [
        { key: "skins", label: "Всего скинов", min: 0, max: 250, step: 5, fmt: function (v) { return v; } },
        { key: "ogItems", label: "Редких OG-предметов", min: 0, max: 5, step: 1, fmt: function (v) { return v; } }
      ],
      compute: function (v) {
        var score = 0.5 * norm(v.skins, 0, 250) + 0.5 * norm(v.ogItems, 0, 5);
        return interpBrackets(score, [[10.9, 15], [15, 50], [50, 150], [150, 1100]]);
      }
    },
    "minecraft": {
      sliders: [
        { key: "type", label: "Тип аккаунта", min: 1, max: 4, step: 1, fmt: function (v) {
          return ["Обычный аккаунт", "MVP+/Hypixel, редкий скин плаща", "Держатель плаща Minecon", "2-симв. ник (алфавитно-цифровой)"][v - 1];
        } }
      ],
      compute: function (v) {
        var table = { 1: [0.5, 25], 2: [25, 632], 3: [2000, 5000], 4: [25000, 50000] };
        return table[v.type];
      }
    },
    "roblox": {
      sliders: [
        { key: "age", label: "Возраст аккаунта", min: 0, max: 15, step: 1, fmt: function (v) { return v + " " + (v === 1 ? "год" : (v >= 2 && v <= 4 ? "года" : "лет")); } },
        { key: "robux", label: "Баланс Robux", min: 0, max: 50000, step: 1000, fmt: function (v) { return v.toLocaleString("en-US") + " R$"; } },
        { key: "limiteds", label: "Предметов Limited", min: 0, max: 10, step: 1, fmt: function (v) { return v; } }
      ],
      compute: function (v) {
        var score = (norm(v.age, 0, 15) + norm(v.robux, 0, 50000) + norm(v.limiteds, 0, 10)) / 3;
        return interpBrackets(score, [[0.5, 5], [5, 25], [25, 60]]);
      }
    }
  };

  function buildCalculator(root) {
    var game = root.getAttribute("data-game");
    var cfg = GAMES[game];
    if (!cfg) return;

    var state = {};
    var slidersWrap = root.querySelector(".vc-sliders");
    var resultOut = root.querySelector(".vc-result-value");
    var resultNote = root.querySelector(".vc-result-note");

    function recompute() {
      var range = cfg.compute(state);
      resultOut.textContent = formatMoney(range[0]) + " – " + formatMoney(range[1]);
    }

    (cfg.sliders || []).forEach(function (s) {
      var field = document.createElement("div");
      field.className = "vc-field";
      var labelId = root.id + "-" + s.key + "-label";
      field.innerHTML =
        '<label for="' + root.id + "-" + s.key + '" id="' + labelId + '">' +
        s.label + ': <strong class="vc-field-val"></strong></label>' +
        '<input type="range" id="' + root.id + "-" + s.key + '" min="' + s.min +
        '" max="' + s.max + '" step="' + s.step + '" value="' + s.min +
        '" aria-labelledby="' + labelId + '">';
      slidersWrap.appendChild(field);

      var input = field.querySelector("input");
      var valEl = field.querySelector(".vc-field-val");
      state[s.key] = s.min;
      valEl.textContent = s.fmt(s.min);
      input.addEventListener("input", function () {
        var v = Number(input.value);
        state[s.key] = v;
        valEl.textContent = s.fmt(v);
        recompute();
      });
    });

    if (cfg.select) {
      var field = document.createElement("div");
      field.className = "vc-field";
      var selId = root.id + "-" + cfg.select.key;
      var html = '<label for="' + selId + '">' + cfg.select.label + "</label>" +
        '<select id="' + selId + '" class="vc-select">';
      cfg.select.options.forEach(function (opt) {
        html += '<option value="' + opt[0] + '">' + opt[1] + "</option>";
      });
      html += "</select>";
      field.innerHTML = html;
      slidersWrap.appendChild(field);
      var select = field.querySelector("select");
      state[cfg.select.key] = cfg.select.options[0][0];
      select.addEventListener("change", function () {
        state[cfg.select.key] = select.value;
        recompute();
      });
    }

    recompute();

    var shareBtn = root.querySelector(".vc-share-btn");
    if (shareBtn) {
      shareBtn.addEventListener("click", function () {
        var text = resultOut.textContent;
        var title = root.getAttribute("data-title") || "GameAccountValue";
        var shareText = title + ": " + text + " — https://t.me/GameAccountValue_Bot";
        if (navigator.share) {
          navigator.share({ text: shareText }).catch(function () {});
        } else if (navigator.clipboard) {
          navigator.clipboard.writeText(shareText).then(function () {
            var original = shareBtn.textContent;
            shareBtn.textContent = resultNote.getAttribute("data-copied") || "Copied!";
            setTimeout(function () { shareBtn.textContent = original; }, 1800);
          }).catch(function () {});
        }
      });
    }
  }

  document.addEventListener("DOMContentLoaded", function () {
    var roots = document.querySelectorAll(".value-calc");
    for (var i = 0; i < roots.length; i++) buildCalculator(roots[i]);
  });
})();
