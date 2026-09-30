# GameAccountValue — work log (read this first when resuming)

Owner: non-coder, Russian-speaking; answers in Russian, short. Site = world-level
**informational** site about game-account values + a free calculator. The AI
screenshot scan lives in the Telegram bot, not on the site.

## Standing rules (owner decisions)
- Keep existing page copy unchanged when restyling; new content is fine but
  must be sourced (publisher / marketplace page actually viewed), dated, and
  never guessed. Unknown = say "not verified / TBA".
- No sales coaching ("sell where it's pricier") — describe markets only.
- Site stays 18+; no uploads / typing / data collection on the site.
- **Privacy-by-design (owner, 2026-09-28): free, no registration, no data
  collection, no ads, no cookies, no third-party requests.** Verified: no
  cookies (server or JS), no storage, no fetch/beacon, no 3rd-party assets;
  analytics-placeholder.js is a no-op. Any future analytics must be cookieless
  and self-hosted, or not at all.
- All 17 full languages get new content (en ru es pt id tr ar vi hi fr de it ja ko th pl zh).
- Verify live (screenshots / Lighthouse / curl), then commit → push → `gh run list`.

## Done (2026-09-27/28)
- Cyber-Glass redesign on all 281 pages — commits 9907ac8, 6346f88.
  Build sources: `scripts/design/` (css parts, rollout.py, stabilize.py,
  city.svg, bot.svg, icons.json). Rebuild CSS:
  `python -c "import importlib.util as u;s=u.spec_from_file_location('r','scripts/design/rollout.py');r=u.module_from_spec(s);s.loader.exec_module(r);r.build_css()"`
  Rollout is idempotent (skips pages that already load glass.css).
- Brawl Stars news page: official events timeline (`.ev-list`, assets/events.js).
- Fixed live bugs: RTL skip-link 11,000px scroll (ar), RTL "$15 – $3",
  white-on-cyan buttons 2.4:1, calculator scroll-on-load.
- Lighthouse (gzip, mobile, settled): home ~96, game ~97, a11y/BP/SEO 100.

## In progress: "World markets" section on game pages (all 17 langs)
Owner's idea: each game page shows **Your market** (by page language) and
**Other countries** — typical range, highest *asking* price seen (never
"sold" — marketplaces show asks), what is in demand there, key events.
Pilot game: Brawl Stars → show owner → then the other 8 games.
Data file: `scripts/research/world-markets.md`.

**Brawl Stars DONE + live (commit ab0009b):** section `#world` on all 17
language pages, generator `scripts/design/world_markets.py <game>` (data dict
`DATA[game]`, translations `T`, language→market map `LOCAL`), CSS
`scripts/design/css/glass-world.css`. Brazil = not verified (403s).
To add a game: research rows (viewed pages only) → add `DATA['<game>']` +
name in `apply()` names → run script → screenshot → commit.

**All 9 games DONE (world section on 153 pages):** markets, esports by country,
top earners, Twitch streamers; data in `scripts/design/world_data.py`.

**Events + recent champions (2026-09-28):** `scripts/design/world_events.py` (EVENTS, publisher
sources only), `world_results.py` (RESULTS), dates via `node scripts/design/build_event_dates.js`
(CLDR, 17 langs; Thai uses Buddhist year = native norm). events.js labels localized via data-l-*.
Not shown (unverified officially): CRL 2026 World Finals, CoC 2026 finals date, Genshin version dates.
Refresh monthly: prices, events, streamers (TwitchMetrics), esports totals.

**Audit 2026-09-28:** audit_site.py clean (only 404 noindex, intended); register fixed
(ru/tr/id); Event JSON-LD for 4 in-person events; privacy.html 'This Website'; llms.txt
updated; sitemap lastmod refreshed + IndexNow 280 URLs -> 200. Old github.io URLs still show
in search (301 migration, normal lag).

## Next steps
0. Owner: Cloudflare proxy for security headers (HSTS etc.); Bing Webmaster Tools.
1. Deepen markets for the other 8 games (CN/JP/KR/TR marketplaces, like Brawl Stars).
2. Rarest/most valuable items per game & country; YouTube creators need a verifiable source.
3. Events timelines for the other 8 games (official sources only).
4. SEO/AI audit: update llms.txt; Event JSON-LD only for in-person events;
   owner to add the site to Bing Webmaster Tools (AI Performance report).
5. LCP 2.4–2.9 s → target ≤ 2.5 s.

## 2026-09-28 (late)
- DONE: tool-first homepage calculator on all 17 full locales (a500cff, deploy success, IndexNow 200).
- OPEN (owner): Cloudflare proxy for security headers; Bing Webmaster Tools; Search Console check of 301 migration.
- NEXT: monthly refresh of prices/events/streamers/earnings (~2026-10-28).

## 2026-09-29 acceptance pass
- Live Lighthouse (mobile): 97-99 perf, 100 a11y/BP/SEO.
- Fixed: dead links (Wikipedia Mohamed Light/Two9 -> Liquipedia; zh Eldorado/igitems; clashos .html), WCAG 2.5.3 label-in-name (4840a57).
- OPEN: zleague.gg genshin-whale-cost article deleted by publisher (37 pages cite it next to Kotaku) - needs a replacement primary source, not removed blindly.
- OPEN (owner): Cloudflare security headers + caching; Bing Webmaster Tools; GSC daily requests.

## 2026-09-30 check
- audit_site.py clean (281 pages, sitemap 280, only 404 noindex).
- External links: 470 unique, no 404/410. 403/429/405 = bot protection only
  (Fandom, Liquipedia, minecraft.wiki, Kotaku, PCGamesN, FunPay, Sportskeeda —
  sportskeeda blocks even its own section page; FF article archived 2022-12-28).
  YouTube Zy0x video alive (oEmbed 200). Not bypassed (rule).
- Mobile 390px (iframe, fresh profile): en/ar/th/ms fit, no horizontal scroll.
  Note: headless --window-size below ~500px crops — use an iframe for phone checks.
- Bot prices recalibrated to Eldorado 2026-09-29 (bot repo docs/item-status-sources.md).
- Status of languages: en 26 pages; 16 full locales 15 pages (no news/privacy/terms);
  7 thin locales (ms uz kk ky tk tl sw) 2 pages — plan in scripts/i18n/PLAN.md.

## 2026-09-30 Malay (ms) full locale
- 15 pages built from EN (1,565 segments translated, register "anda"); calculator STR.ms; world section
  for ms (LOCAL sea, country MY, CLDR dates/names); hreflang ms on 13 pages × 18 locales; sitemap +13 (293).
- segments.py fix: text right after an <svg> icon was left untranslated (e.g. "Get Exact Estimate via Bot").
- Checks: audit clean, 32 JSON-LD blocks parse, 0 English leftovers, 390px screenshots index/roblox OK.
- Next locale per PLAN.md: uz (base: Russian pages per plan, or EN with from_en.py).

## 2026-09-30 Uzbek (uz) full locale
- Same recipe as ms (base EN, 1,565 segments, "siz" register, official Latin oʻ/gʻ with U+02BB; CLDR
  names/dates normalised to ʻ). World section: market CIS first, country Uzbekistan (UZ added to names).
- hreflang uz on 13 pages × 19 locales; sitemap 306. Checks: audit clean, 32 JSON-LD OK, 0 English leftovers,
  390px screenshots OK. ms event JSON-LD back to generator's compact form (content unchanged).
- Next: kk, ky, tk, tl, sw (PLAN.md).

## 2026-09-30 older locales levelled + Kazakh
- bc5cafb: roblox manipulation subsection in 16 locales; pt/id glossary +11 terms; zh fortnite sources.
- kk full locale (15 pages, "сіз", CIS market, KZ), built with scripts/i18n/finish_locale.py.
- Local number style (numfmt.py) for uz/kk: 1 147 (NBSP), 17,8% — money kept as in source, like ru.
- Sitemap 319. Remaining thin: ky, tk, tl, sw.

- ky full locale (2026-09-30, "сиз", CIS, KG); sitemap 332. Remaining thin: tk, tl, sw.

- tk full locale (2026-09-30, "siz", CIS, TM); sitemap 345. Remaining thin: tl, sw.
