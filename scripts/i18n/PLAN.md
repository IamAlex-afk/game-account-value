# Building the 7 thin locales to full depth (owner request 2026-09-29)

Order: **ms → uz → kk → ky → tk → tl → sw** (one locale at a time: build,
verify, push, then the next). Read this file first when resuming.

## Base pages
- ms, tl, sw: English pages (global data; the id pages carry Indonesia-only
  Tokopedia/rupiah content that must not appear as "local" elsewhere).
- uz, kk, ky, tk: Russian pages (CIS market / FunPay already local there).

## Steps per locale
1. Generators: add the locale to scripts/design world_markets.py (LANGS,
   LOCAL, T), world_extra.py (X, LANG_COUNTRY), world_events.py (L),
   world_results.py (RL), world_data*.py notes (N/N2), country_names.json
   (CLDR via Node Intl), brand_rollout.py (HOME, CRUMB_LABEL, WHY_T, XY),
   assets/calculators.js (T.<lang> + whitelist), add_home_tool.py (TX).
2. `python scripts/i18n/segments.py extract <base> <lang>` → translate
   scripts/i18n/<lang>/todo.json into done.json (world section excluded:
   it is regenerated in step 4).
3. `python scripts/i18n/segments.py build <base> <lang>` → <lang>/*.html
   (paths ../, drop EN-only news FAB + google verification + org logo LD).
4. Regenerate the world section for the locale; hreflang on every page of
   every locale; language menus; sitemap; audit_site.py; screenshots;
   Lighthouse; word check; push; IndexNow.

Rules: register per locale (ms "anda", uz/kk/ky/tk "siz"-level polite,
tl "ka/mo" casual-neutral, sw neutral); no fabricated local marketplace
sources — local sources only if checked live, otherwise the global ones.

## Status
- [x] ms (2026-09-30)  - [ ] uz  - [ ] kk  - [ ] ky  - [ ] tk  - [ ] tl  - [ ] sw

## How ms was built (repeat for the next locale)
1. `segments.py extract en <lang>` → translate todo.json (done in chunks) → merge into done.json.
2. `segments.py build en <lang>` then `from_en.py <lang>` (paths ../, canonical/og:url/JSON-LD → /<lang>/,
   utm_content, drop news FAB + 2nd GSC tag, lang-current, keywords from KEYWORDS).
3. calculators.js: add STR.<lang> + whitelist.
4. World section: append <lang> to world_markets (LANGS, LOCAL, T), world_extra (LANG_COUNTRY, X),
   world_events (L), world_results (RL), world_data (N, TW_ONLY) — strings mapped from done.json;
   add <lang> to build_event_dates.js and country_names.json (Node Intl, CLDR); run world_markets.py per game.
5. hreflang <lang> on the 13 pages in every locale; sitemap; audit_site.py; JSON-LD parse check;
   English-leftover scan; phone screenshots via same-origin iframe (local server).
