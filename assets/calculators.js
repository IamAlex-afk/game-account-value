(function () {
  "use strict";

  var prefersReducedMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var LANG = (document.documentElement.getAttribute("lang") || "en").toLowerCase();
  if (["en", "ru", "id", "pt"].indexOf(LANG) === -1) LANG = "en";

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

  // --- i18n --------------------------------------------------------------
  // Only UI text is localized here. All scoring/pricing math below is
  // language-independent and identical across en/ru/id/pt.
  var STR = {
    en: {
      sliders: {
        "brawl-stars": { trophies: "Trophies (cups)", maxed: "Power Level 11 brawlers" },
        "clash-of-clans": { th: "Town Hall level" },
        "clash-royale": { kt: "King Tower level", maxed: "Max-level cards" },
        "free-fire": { rank: "Rank", bundles: "Rare bundles/pets" },
        "genshin-impact": { fivestars: "5★ characters", c6: "Characters with C6" },
        "mobile-legends": { skins: "Total skins", rank: "Rank" },
        "fortnite": { skins: "Total skins", ogItems: "Rare OG items" },
        "minecraft": { type: "Account type" },
        "roblox": { age: "Account age", robux: "Robux balance", limiteds: "Common Limited items (not named rares)" }
      },
      select: { "clash-of-clans": { label: "Upgrade type", options: [["full", "Full Max"], ["standard", "Standard"], ["rushed", "Rushed"]] } },
      ageUnit: function (v) { return v + " " + (v === 1 ? "year" : "years"); },
      minecraftTypes: ["Regular account", "MVP+/Hypixel, rare cape", "Minecon cape holder", "2-char name (alphanumeric)"],
      checkboxHeading: "Named rare items (optional):",
      confidence: { low: "Low", medium: "Medium", high: "High" },
      confidencePrefix: "Confidence: ",
      copiedFallback: "Copied!"
    },
    ru: {
      sliders: {
        "brawl-stars": { trophies: "Трофеи (кубки)", maxed: "Бойцы Power Level 11" },
        "clash-of-clans": { th: "Уровень Ратуши (Town Hall)" },
        "clash-royale": { kt: "Уровень King Tower", maxed: "Карт максимального уровня" },
        "free-fire": { rank: "Ранг", bundles: "Редких бандлов/питомцев" },
        "genshin-impact": { fivestars: "5★ персонажей", c6: "Персонажей с C6" },
        "mobile-legends": { skins: "Всего скинов", rank: "Ранг" },
        "fortnite": { skins: "Всего скинов", ogItems: "Редких OG-предметов" },
        "minecraft": { type: "Тип аккаунта" },
        "roblox": { age: "Возраст аккаунта", robux: "Баланс Robux", limiteds: "Обычных Limited-предметов (не именных редких)" }
      },
      select: { "clash-of-clans": { label: "Тип прокачки", options: [["full", "Full Max"], ["standard", "Стандартный"], ["rushed", "Rushed"]] } },
      ageUnit: function (v) { return v + " " + (v === 1 ? "год" : (v >= 2 && v <= 4 ? "года" : "лет")); },
      minecraftTypes: ["Обычный аккаунт", "MVP+/Hypixel, редкий скин плаща", "Держатель плаща Minecon", "2-симв. ник (алфавитно-цифровой)"],
      checkboxHeading: "Именные редкие предметы (опционально):",
      confidence: { low: "Низкая", medium: "Средняя", high: "Высокая" },
      confidencePrefix: "Уверенность: ",
      copiedFallback: "Скопировано!"
    },
    id: {
      sliders: {
        "brawl-stars": { trophies: "Trofi (cup)", maxed: "Brawler Power Level 11" },
        "clash-of-clans": { th: "Level Town Hall" },
        "clash-royale": { kt: "Level King Tower", maxed: "Kartu level maksimum" },
        "free-fire": { rank: "Rank", bundles: "Bundle/pet langka" },
        "genshin-impact": { fivestars: "Karakter 5★", c6: "Karakter dengan C6" },
        "mobile-legends": { skins: "Total skin", rank: "Rank" },
        "fortnite": { skins: "Total skin", ogItems: "Item OG langka" },
        "minecraft": { type: "Jenis akun" },
        "roblox": { age: "Usia akun", robux: "Saldo Robux", limiteds: "Item Limited biasa (bukan yang langka bernama)" }
      },
      select: { "clash-of-clans": { label: "Jenis upgrade", options: [["full", "Full Max"], ["standard", "Standar"], ["rushed", "Rushed"]] } },
      ageUnit: function (v) { return v + " tahun"; },
      minecraftTypes: ["Akun biasa", "MVP+/Hypixel, cape langka", "Pemilik cape Minecon", "Nama 2 karakter (alfanumerik)"],
      checkboxHeading: "Item langka bernama (opsional):",
      confidence: { low: "Rendah", medium: "Sedang", high: "Tinggi" },
      confidencePrefix: "Keyakinan: ",
      copiedFallback: "Disalin!"
    },
    pt: {
      sliders: {
        "brawl-stars": { trophies: "Troféus (copas)", maxed: "Brawlers Power Level 11" },
        "clash-of-clans": { th: "Nível do Town Hall" },
        "clash-royale": { kt: "Nível da King Tower", maxed: "Cartas no nível máximo" },
        "free-fire": { rank: "Rank", bundles: "Bundles/pets raros" },
        "genshin-impact": { fivestars: "Personagens 5★", c6: "Personagens com C6" },
        "mobile-legends": { skins: "Total de skins", rank: "Rank" },
        "fortnite": { skins: "Total de skins", ogItems: "Itens OG raros" },
        "minecraft": { type: "Tipo de conta" },
        "roblox": { age: "Idade da conta", robux: "Saldo de Robux", limiteds: "Itens Limited comuns (não os raros nomeados)" }
      },
      select: { "clash-of-clans": { label: "Tipo de evolução", options: [["full", "Full Max"], ["standard", "Padrão"], ["rushed", "Rushed"]] } },
      ageUnit: function (v) { return v + " " + (v === 1 ? "ano" : "anos"); },
      minecraftTypes: ["Conta comum", "MVP+/Hypixel, cape raro", "Dono de cape Minecon", "Nick de 2 caracteres (alfanumérico)"],
      checkboxHeading: "Itens raros nomeados (opcional):",
      confidence: { low: "Baixa", medium: "Média", high: "Alta" },
      confidencePrefix: "Confiança: ",
      copiedFallback: "Copiado!"
    }
  };
  var T = STR[LANG];

  // Roblox named-item price adds — official Robux purchase cost x the
  // $0.0035-0.004/Robux secondary rate used elsewhere on this page (not a
  // live resale listing, an acquisition-cost proxy): Korblox Deathspeaker
  // 17,000 R$, Headless Horseman 31,000 R$ (seasonal, Oct-only official
  // sale), Violet Valkyrie 50,000 R$. Kept as ranges, not single points,
  // same convention as every other bracket on this page.
  var ROBLOX_RARE_ITEMS = [
    { key: "korblox", name: "Korblox Deathspeaker", lo: 60, hi: 70 },
    { key: "headless", name: "Headless Horseman", lo: 110, hi: 140 },
    { key: "violet", name: "Violet Valkyrie", lo: 175, hi: 200 }
  ];

  // Rank ladders are the games' own official English rank names — kept
  // identical across languages on purpose, the same way "Town Hall" or
  // "C6" isn't translated either.
  var FREE_FIRE_RANKS = ["Bronze", "Silver", "Gold", "Platinum", "Diamond", "Heroic", "Grandmaster"];
  var ML_RANKS = ["Warrior", "Elite", "Master", "Grandmaster", "Epic", "Legend", "Mythical Glory"];

  // Tier vocabulary matches the bot's PDF certificate (core/valuation.py:
  // STARTER/CASUAL/PRO/COLLECTOR — kept in English in every language, same
  // as the bot does), so the site and the bot speak the same language. The
  // boundaries themselves are this widget's own score quartiles, not a
  // byte-for-byte copy of the bot's per-game conditions — those depend on
  // named items (specific skins, badges) this slider-only widget
  // deliberately doesn't collect. Two games (Clash of Clans by TH, Genshin
  // by C6 count) happen to line up with the bot's real thresholds because
  // their score IS that same slider; the rest are an honest approximation,
  // not a claimed 1:1 match.
  function tierFromScore(score) {
    if (score >= 0.75) return { label: "COLLECTOR", cls: "tier-collector" };
    if (score >= 0.5) return { label: "PRO", cls: "tier-pro" };
    if (score >= 0.25) return { label: "CASUAL", cls: "tier-casual" };
    return { label: "STARTER", cls: "tier-starter" };
  }

  function confidenceLabel(ratio) {
    if (ratio >= 0.8) return T.confidence.high;
    if (ratio >= 0.4) return T.confidence.medium;
    return T.confidence.low;
  }

  // --- per-game config -----------------------------------------------
  // Every bracket/table value is taken directly from that game's own
  // "Real Market Prices" table on the same page.
  var GAMES = {
    "brawl-stars": {
      name: "Brawl Stars",
      sliders: [
        { key: "trophies", min: 5000, max: 45000, step: 1000, fmt: function (v) { return v.toLocaleString("en-US"); } },
        { key: "maxed", min: 0, max: 85, step: 1, fmt: function (v) { return v; } }
      ],
      score: function (v) { return 0.5 * norm(v.trophies, 5000, 45000) + 0.5 * norm(v.maxed, 0, 85); },
      compute: function (v, score) { return interpBrackets(score, [[3, 15], [15, 50], [50, 150], [150, 300]]); }
    },
    "clash-of-clans": {
      name: "Clash of Clans",
      sliders: [
        { key: "th", min: 13, max: 18, step: 1, fmt: function (v) { return "TH" + v; } }
      ],
      choices: [{ key: "type", label: T.select["clash-of-clans"].label, options: T.select["clash-of-clans"].options }],
      score: function (v) { return norm(v.th, 13, 18); },
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
      name: "Clash Royale",
      sliders: [
        { key: "kt", min: 9, max: 15, step: 1, fmt: function (v) { return "KT" + v; } },
        { key: "maxed", min: 0, max: 40, step: 1, fmt: function (v) { return v; } }
      ],
      score: function (v) { return 0.5 * norm(v.kt, 9, 15) + 0.5 * norm(v.maxed, 0, 40); },
      compute: function (v, score) { return interpBrackets(score, [[0.5, 15], [15, 50], [50, 150], [150, 600]]); }
    },
    "free-fire": {
      name: "Free Fire",
      sliders: [
        { key: "bundles", min: 0, max: 10, step: 1, fmt: function (v) { return v; } }
      ],
      choices: [{ key: "rank", label: T.sliders["free-fire"].rank, options: FREE_FIRE_RANKS.map(function (name, i) { return [String(i + 1), name]; }) }],
      score: function (v) { return 0.5 * norm(v.rank, 1, 7) + 0.5 * norm(v.bundles, 0, 10); },
      compute: function (v, score) { return interpBrackets(score, [[0.73, 15], [15, 50], [50, 150], [150, 300]]); }
    },
    "genshin-impact": {
      name: "Genshin Impact",
      sliders: [
        { key: "fivestars", min: 0, max: 20, step: 1, fmt: function (v) { return v; } },
        { key: "c6", min: 0, max: 20, step: 1, fmt: function (v) { return v; } }
      ],
      score: function (v) {
        if (v.fivestars < 3) return 0;
        return 0.5 * norm(v.fivestars, 3, 20) + 0.5 * norm(v.c6, 0, 20);
      },
      compute: function (v, score) {
        if (v.fivestars < 3) return [5, 60];
        return interpBrackets(score, [[30, 200], [300, 1000], [1000, 4200], [8400, 8995]]);
      }
    },
    "mobile-legends": {
      name: "Mobile Legends",
      sliders: [
        { key: "skins", min: 0, max: 400, step: 10, fmt: function (v) { return v; } }
      ],
      choices: [{ key: "rank", label: T.sliders["mobile-legends"].rank, options: ML_RANKS.map(function (name, i) { return [String(i + 1), name]; }) }],
      score: function (v) { return 0.5 * norm(v.skins, 0, 400) + 0.5 * norm(v.rank, 1, 7); },
      compute: function (v, score) { return interpBrackets(score, [[0.5, 15], [15, 50], [50, 150], [150, 300]]); }
    },
    "fortnite": {
      name: "Fortnite",
      sliders: [
        { key: "skins", min: 0, max: 250, step: 5, fmt: function (v) { return v; } },
        { key: "ogItems", min: 0, max: 5, step: 1, fmt: function (v) { return v; } }
      ],
      score: function (v) { return 0.5 * norm(v.skins, 0, 250) + 0.5 * norm(v.ogItems, 0, 5); },
      compute: function (v, score) { return interpBrackets(score, [[10.9, 15], [15, 50], [50, 150], [150, 1100]]); }
    },
    "minecraft": {
      name: "Minecraft",
      choices: [{ key: "type", label: T.sliders["minecraft"].type, options: T.minecraftTypes.map(function (name, i) { return [String(i + 1), name]; }) }],
      score: function (v) { return norm(v.type, 1, 4); },
      compute: function (v) {
        var table = { 1: [0.5, 25], 2: [25, 632], 3: [2000, 5000], 4: [25000, 50000] };
        return table[v.type];
      }
    },
    "roblox": {
      name: "Roblox",
      sliders: [
        { key: "age", min: 0, max: 15, step: 1, fmt: function (v) { return T.ageUnit(v); } },
        { key: "robux", min: 0, max: 50000, step: 1000, fmt: function (v) { return v.toLocaleString("en-US") + " R$"; } },
        { key: "limiteds", min: 0, max: 10, step: 1, fmt: function (v) { return v; } }
      ],
      checkboxes: ROBLOX_RARE_ITEMS,
      score: function (v) { return (norm(v.age, 0, 15) + norm(v.robux, 0, 50000) + norm(v.limiteds, 0, 10)) / 3; },
      compute: function (v, score) {
        var base = interpBrackets(score, [[0.5, 5], [5, 25], [25, 60]]);
        var extraLo = 0, extraHi = 0;
        ROBLOX_RARE_ITEMS.forEach(function (item) {
          if (v[item.key]) { extraLo += item.lo; extraHi += item.hi; }
        });
        return [base[0] + extraLo, base[1] + extraHi];
      }
    }
  };

  var GAME_ORDER = ["roblox", "brawl-stars", "clash-of-clans", "clash-royale", "free-fire",
    "genshin-impact", "mobile-legends", "fortnite", "minecraft"];

  var rafIds = new WeakMap();

  function animateNumber(el, fromVal, toVal) {
    if (prefersReducedMotion || fromVal === toVal) { el.textContent = formatMoney(toVal); return; }
    var pending = rafIds.get(el);
    if (pending) cancelAnimationFrame(pending);
    var start = null;
    var duration = 220;
    function tick(now) {
      if (start === null) start = now;
      var p = Math.min((now - start) / duration, 1);
      el.textContent = formatMoney(fromVal + (toVal - fromVal) * p);
      if (p < 1) {
        rafIds.set(el, requestAnimationFrame(tick));
      } else {
        rafIds.delete(el);
      }
    }
    rafIds.set(el, requestAnimationFrame(tick));
  }

  function ensureResultShell(root) {
    var resultBox = root.querySelector(".vc-result");
    var valueEl = resultBox.querySelector(".vc-result-value");
    valueEl.setAttribute("aria-live", "polite");
    if (!valueEl.querySelector(".vc-lo")) {
      valueEl.innerHTML = '<span class="vc-lo">—</span> – <span class="vc-hi">—</span>';
    }
    if (!resultBox.querySelector(".vc-scale")) {
      var scale = document.createElement("div");
      scale.className = "vc-scale";
      scale.setAttribute("aria-hidden", "true");
      scale.innerHTML = '<div class="vc-scale-fill"></div>';
      valueEl.insertAdjacentElement("afterend", scale);
      var meta = document.createElement("div");
      meta.className = "vc-meta";
      meta.innerHTML = '<span class="vc-tier"></span><span class="vc-confidence"></span>';
      scale.insertAdjacentElement("afterend", meta);
    }
    return {
      lo: valueEl.querySelector(".vc-lo"),
      hi: valueEl.querySelector(".vc-hi"),
      scaleFill: resultBox.querySelector(".vc-scale-fill"),
      tier: resultBox.querySelector(".vc-tier"),
      confidence: resultBox.querySelector(".vc-confidence")
    };
  }

  function mount(root, gameId) {
    var cfg = GAMES[gameId];
    if (!cfg) return;
    root.setAttribute("data-game", gameId);
    root.setAttribute("data-title", cfg.name);

    var slidersWrap = root.querySelector(".vc-sliders");
    slidersWrap.innerHTML = "";
    var els = ensureResultShell(root);
    var resultNote = root.querySelector(".vc-result-note");

    var state = {};
    var totalInputs = (cfg.sliders || []).length + (cfg.choices ? cfg.choices.length : 0) + (cfg.checkboxes ? cfg.checkboxes.length : 0);
    var touched = new Set();
    var prevLo = null, prevHi = null;

    function recompute() {
      var score = cfg.score(state);
      var range = cfg.compute(state, score);
      var lo = range[0], hi = range[1];
      animateNumber(els.lo, prevLo === null ? lo : prevLo, lo);
      animateNumber(els.hi, prevHi === null ? hi : prevHi, hi);
      prevLo = lo; prevHi = hi;

      els.scaleFill.style.width = Math.round(score * 100) + "%";
      var tier = tierFromScore(score);
      els.tier.textContent = tier.label;
      els.tier.className = "vc-tier " + tier.cls;
      els.confidence.textContent = T.confidencePrefix + confidenceLabel(totalInputs ? touched.size / totalInputs : 1);
    }

    (cfg.sliders || []).forEach(function (s) {
      var label = T.sliders[gameId][s.key];
      var field = document.createElement("div");
      field.className = "vc-field";
      var labelId = root.id + "-" + s.key + "-label";
      field.innerHTML =
        '<label for="' + root.id + "-" + s.key + '" id="' + labelId + '">' +
        label + ': <strong class="vc-field-val"></strong></label>' +
        '<input type="range" id="' + root.id + "-" + s.key + '" min="' + s.min +
        '" max="' + s.max + '" step="' + s.step + '" value="' + s.min +
        '" aria-labelledby="' + labelId + '">';
      slidersWrap.appendChild(field);

      var input = field.querySelector("input");
      var valEl = field.querySelector(".vc-field-val");
      state[s.key] = s.min;
      valEl.textContent = s.fmt(s.min);
      input.addEventListener("input", function () {
        touched.add(s.key);
        var v = Number(input.value);
        state[s.key] = v;
        valEl.textContent = s.fmt(v);
        recompute();
      });
    });

    (cfg.choices || []).forEach(function (choice) {
      var field = document.createElement("div");
      field.className = "vc-field";
      var groupName = root.id + "-" + choice.key;
      var html = '<span class="vc-choice-heading">' + choice.label + '</span><div class="vc-choice-tiles" role="radiogroup" aria-label="' + choice.label + '">';
      choice.options.forEach(function (opt, i) {
        var optId = groupName + "-" + i;
        html += '<input type="radio" name="' + groupName + '" id="' + optId + '" value="' + opt[0] + '"' + (i === 0 ? " checked" : "") + '>' +
          '<label for="' + optId + '" class="vc-choice-tile">' + opt[1] + "</label>";
      });
      html += "</div>";
      field.innerHTML = html;
      slidersWrap.appendChild(field);
      state[choice.key] = choice.options[0][0];
      field.querySelectorAll('input[type="radio"]').forEach(function (radio) {
        radio.addEventListener("change", function () {
          touched.add(choice.key);
          state[choice.key] = radio.value;
          recompute();
        });
      });
    });

    if (cfg.checkboxes && cfg.checkboxes.length) {
      var cbField = document.createElement("div");
      cbField.className = "vc-field vc-checkbox-group";
      var cbHtml = '<span class="vc-checkbox-heading">' + T.checkboxHeading + '</span>';
      cfg.checkboxes.forEach(function (item, i) {
        var cbId = root.id + "-cb-" + item.key;
        cbHtml += '<label class="vc-checkbox" for="' + cbId + '">' +
          '<input type="checkbox" id="' + cbId + '">' +
          '<span>' + item.name + ' (+' + formatMoney(item.lo) + '–' + formatMoney(item.hi) + ')</span>' +
          '</label>';
      });
      cbField.innerHTML = cbHtml;
      slidersWrap.appendChild(cbField);
      cfg.checkboxes.forEach(function (item) {
        var cbId = root.id + "-cb-" + item.key;
        var input = cbField.querySelector("#" + cbId);
        state[item.key] = false;
        input.addEventListener("change", function () {
          touched.add(item.key);
          state[item.key] = input.checked;
          recompute();
        });
      });
    }

    recompute();

    var shareBtn = root.querySelector(".vc-share-btn");
    if (shareBtn && !shareBtn.dataset.bound) {
      shareBtn.dataset.bound = "1";
      shareBtn.addEventListener("click", function () {
        var text = els.lo.textContent + " – " + els.hi.textContent;
        var title = root.getAttribute("data-title") || "GameAccountValue";
        var shareText = title + ": " + text + " — https://t.me/GameAccountValue_Bot";
        if (navigator.share) {
          navigator.share({ text: shareText }).catch(function () {});
        } else if (navigator.clipboard) {
          navigator.clipboard.writeText(shareText).then(function () {
            var original = shareBtn.textContent;
            shareBtn.textContent = resultNote.getAttribute("data-copied") || T.copiedFallback;
            setTimeout(function () { shareBtn.textContent = original; }, 1800);
          }).catch(function () {});
        }
      });
    }
  }

  function initSwitcher(root) {
    var switcher = root.querySelector(".vc-switcher");
    if (!switcher) return;
    switcher.innerHTML = "";
    GAME_ORDER.forEach(function (id) {
      var opt = document.createElement("option");
      opt.value = id;
      opt.textContent = GAMES[id].name;
      switcher.appendChild(opt);
    });
    switcher.value = GAME_ORDER[0];
    mount(root, GAME_ORDER[0]);
    switcher.addEventListener("change", function () {
      mount(root, switcher.value);
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".value-calc[data-switcher]").forEach(initSwitcher);
    document.querySelectorAll(".value-calc[data-game]:not([data-switcher])").forEach(function (root) {
      mount(root, root.getAttribute("data-game"));
    });
  });

  window.GAVCalc = { GAMES: GAMES, GAME_ORDER: GAME_ORDER, mount: mount };
})();
