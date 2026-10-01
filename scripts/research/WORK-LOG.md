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

## Done 2026-09-30 / 10-01 (read SITE-STANDARD.md first — it is the working prompt)
- SITE-STANDARD.md + scripts/site_check.py (0 errors gate) + scripts/deep_audit.py (page-by-page report).
- Privacy/terms/about in 24 languages (scripts/design/legal_pages.py, legal_text_*.py, about_text_*.py),
  matched to what the bot stores; About link in every footer.
- News in 24 languages: 10 articles from official publisher announcements (scripts/design/news_pages.py,
  news_data.py, news_text_*.py; sources in research/news-2026-09.md). Game news hubs are noindex,follow
  until 3 articles (MIN_HUB_ARTICLES). Old English market-watch news pages replaced; their events
  timeline and regional prices still live on the game pages (#world).
- Freshness badge rewritten (no 'researched live by AI' — contradicted methodology), HowTo LD removed.
- Card teasers (hero chip + mini card under every calculator), carousel on the 2nd screen.
- Bot: /delete erases fingerprints + feedback, fingerprints expire after 90 days; legal links in the
  user's language. Needs server deploy: bash /opt/gavbot/app/deploy/install.sh
- Decided NOT to add templated "pros & cons" blocks (game pages already have evidence, comparison,
  value drivers, risks, rules, sources) nor a sitemap-style footer (menu links are crawlable).
- Search Console: domain property (sc-domain) -> sitemap must be submitted as the full URL.
  Resubmitted 2026-10-01. Bing ~54 pages indexed; Google ~180 via site: query.
- News batch 2 (2026-10-01): +14 articles x 24; hubs open for Roblox, Brawl Stars, CoC, CR, Free Fire, MLBB,
  Minecraft; Genshin (2) and Fortnite (1, site bot-protected) stay noindex. 1249 pages, sitemap 1200.
- Next: monthly price refresh 2026-10-28; add news so game hubs reach 3 articles; brand mentions/backlinks.

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

## 2026-09-30 (evening) — art, navigation, collection cards
Pushed: tl+sw locales (all 24 bot langs full); raster cyborg hero + visual pack (rays, cables, holo cards,
view transitions, slot roll, scroll reveal) + robot animations; og share cards (logo-first, calc robot, ?v=3,
baseline JPEG); mobile perf (srcset, no rain/backdrop blur on phones, SW shell-only precache, network-first
CSS/JS); site-wide menu (Games/Guides/News) + same-page language switcher (nav_menu.py); news.html hub;
homepage "Everything on the site" hub (home_hub.py); methodology plain headings, FAQPage LD dropped;
card collection carousel on 24 homepages (card_collection.py, 11 cards x 24 langs from the bot drawer);
CTA hierarchy (bot = primary); consistency.py (18+ card, joystick, market-report crumbs/CTA, 404/legal header).
Bot f7fe786: collection numbering from #1 (card_seq), GENESIS 1-100 / FOUNDER 101-1000, tier foil, tilt video.
OPEN: owner runs `bash /opt/gavbot/app/deploy/install.sh`; news are Sept-21 and EN-only (next: official-source
news articles, 24 langs, NewsArticle LD); NO automated scraping (Eldorado ToS 3.1 forbids); Eldorado affiliate
application + data-access letter (owner decision); founders /gift + public card counter + rules page; footer
section links + "fresh for this game" block; PageSpeed (Google API quota hit 09-30) re-check; WhatsApp preview
test by owner; optional PDF digital signature; GitHub repo research for ideas.

## 2026-10-01 external audit pass (owner's 12-point prompt)
- CoC TH17 rushed: changed to [30,35] (bd55d6ab), then REVERTED to [30,55]. Not a bug: the calculator mirrors the page's
  "Real Market Prices" table (igitems.com report), and igitems on 2026-10-01 still shows TH17 rushed $25-$55 vs standard
  $30-$50. Rule: never "fix" a calculator number by pattern - check the page table and its source first.
- Game pages: "Latest <game> news" lists the 3 newest articles + hub (news_pages.GAME_BLOCK_ARTICLES), dates
  bidi-isolated for ar; Organization sameAs + GitHub repo on the 8 homepages that carry it (f12e06e8). IndexNow 224 URLs -> 200.
- Audit claims that were false (tool did not see <head>/JSON-LD): hreflang, NewsArticle/BreadcrumbList LD, llms.txt,
  news source links (576/576 articles link the publisher). Zenodo DOI is the owner's paper -> stays on Person, not Organization.
- Cloudflare proxy ON (owner, 2026-10-01): HSTS, X-Frame-Options, nosniff, Referrer-Policy, Permissions-Policy live.
  Note: Cloudflare sets browser cache 4h on assets (was 600s) - owner may switch to "Respect Existing Headers".
- Removed tracked screenshot leftovers _snapw.html/_snapy.html.
- NEXT refresh (~2026-10-28): igitems CoC table moved slightly (TH18 100-250/50-115/20-30, TH17 55-180/30-50/25-55,
  TH16 40-95, TH13 15-35) - update page table (24 langs) and calculators.js together.
