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

## 2026-10-05 audit phase A + P1
- Phase A (read-only): prod vs repo conflict found - Cloudflare Web Analytics beacon injected into every page (blocked by
  CSP -> console error) and Yandex Metrica (webvisor, 3rd-party cookies) on / contradicting the 24-language privacy policy.
  Owner: Metrica removed (4e3285b9, CSP restored byte-for-byte), Cloudflare Web Analytics disabled. Live: neither present.
- Lighthouse mobile live / after removal, 3 sequential runs: Perf 87/91/90, A11y 100, BP 100, SEO 100 (earlier 62/82 = noise).
- Footer section links on 1,248 pages (footer_nav.py, 2533d9e2). CoC "estimate limits" pilot EN+RU (9fa50484) - awaits owner OK.
- Twitch/champion table links 24px targets (eabaa010): local A11y 100 on 3 pages.
- sitemap lastmod skips template-only commits (scripts/lastmod-ignore-revs.txt): 1198 x 2026-10-01, CoC en/ru 2026-10-05.
- OPEN (owner): Cloudflare Browser Cache TTL -> "Respect Existing Headers" (assets still max-age=14400); GSC Pages report per language.

## 2026-10-05/06 visual system + space scene
- assets/space-background.js on all 1,248 pages (scripts/design/space_rollout.py, bump V on script change):
  photoreal sky, Mars + gas giant, comets, satellite, skeleton astronaut, android (home), UFO, 6-step phone
  evolution, per-game view + loot set (assets/space/g-<game>-N.webp) on game pages / game news.
  Assets generated with Gemini (gemini-3-pro-image) - no logos, look-alikes of real brands dropped.
- glass.css: typed visual system (instrument calculator, gold estimate exhibit, hairline cards with corner
  brackets), JetBrains Mono headings (OFL, font-display optional), phone typography, one-row phone header,
  homepage quick tiles. CSS parts in scripts/design/css kept byte-identical with the build.
- Perf: glass.js forced reflows (void offsetWidth) removed - 455 ms layout at load. Local Lighthouse today
  unreliable (host CPU busy: baseline commit also dropped 85 -> 59-74); PSI quota exhausted - owner to re-check PSI.
- OPEN: bot fixes (fp_done order, TimedOut), morning summary + Stars revenue (owner "да" pending);
  CoC estimate-limits block for other games; Cloudflare Browser Cache TTL.

## 2026-10-06 creators, Search Console, Brawl Stars FAQ
- Owner report (Russian, read first in a new session): Desktop\ПЛНАН КАПКАН ЗИП\GAV-ОТЧЁТ.md
- Creators by language: streamers.py (YouTube Data API v3; keys ~/.gav-keys.json), creators.py, home_creators.py.
  Live: Clash Royale pt + ar. Topic rule: game in title/tags of >= 6 of last 10 uploads, >= 2 titles, no other
  tracked game named in more titles; official game channels excluded; one game per channel; language from uploads.
  30-day YouTube policy enforced in renderer; --refresh / --recheck modes.
- Search Console API read-only via ~/.gav-gsc.json (siteRestrictedUser). Rules in SITE-STANDARD.md.
- Brawl Stars 24 langs: "make account more valuable" FAQ replaced with pre-estimate checklist (02d308e1).
  Same FAQ on the other 8 games -> replace (owner approved) + add calculator options only with sources.

## 2026-10-06 (later) About cleanup, Vietnamese creators
- About page, all 24 langs (f0e7d8d4, 81bed07f, 6b6cb972): owner wants no repeated content. Removed the author section
  (footer already names the author), the two "never do" bullets the footer notice states, the second "no ads" sentence,
  and the author line from meta description / lead. Source text in scripts/design/about_text_[a-d].py edited to match.
- Creators vi (39816103): Roblox, Clash of Clans, Free Fire + vi homepage block. YouTube "Search Queries per day" quota
  ran out (HTTP 429, not 403 - streamers.py only handles 403 and crashes before add_manual/apply_exclude).
  STILL TO COLLECT for vi: clash-royale (0 passed), genshin-impact, mobile-legends, fortnite, minecraft; brawl-stars found
  only two tiny channels (820 and 6 subscribers) - dropped from the store, not published.
- BUG to fix: world_markets.py writes a raw "&" where pages have "&amp;" (e.g. vi "Nga &amp; SNG", also en/de/id/ms).
  Running it for a game touches those pages; reverted by hand this time.
- Pages build for 6b6cb972 errored once on GitHub's side; the next push built fine and carried the change.

## 2026-10-06 (evening) homepage de-duplication, generator fix
- world_markets.py / world_results.py: '&' escaped in region labels and winners (acf9b533); a full re-run for 9 games is a no-op.
- Homepage, 24 langs (6e28fd07): dropped 4 repeated cards from "Why players love it" (screenshot-only, verifiable PDF,
  not-a-marketplace, instant delivery) and the FAQ entry "What exactly is this service?" (page + FAQPage JSON-LD).
- Homepage, 24 langs: dropped the nine near-identical "how much is my <game> account worth" FAQ entries (page + JSON-LD,
  5 questions left). Search Console 2026-09-07..10-04: homepages 22 clicks / 282 impressions, visible game-named queries
  on homepages 0 clicks / 7 impressions (most queries are hidden by Google). Game pages answer the question in full.
  RE-CHECK homepage impressions in GSC around 2026-10-20..11-03.
- Owner rule (2026-10-06): no duplicated content anywhere - text already in the footer or elsewhere on the page goes.

## 2026-10-06 (night) autonomous fix loop (owner: fix -> verify -> push -> verify live, no confirmations)
- Homepage: nine per-game FAQ entries removed (1084a6c2).
- Game pages 9 x 24: calculator note said "ranges/note/Limiteds Market above" though the calculator is at the top (85d95ad0).
- Game pages 192: FAQPage JSON-LD still had the removed "make your account more valuable" Q&A; synced to the visible
  checklist question; Roblox "price manipulation on Limiteds" synced too (08738159).
- site_check.py now fails on FAQ markup questions that are not visible and on in-page anchors without a target.
- Audits that came back clean (1,249 pages): duplicate titles/descriptions per language, broken anchors and links,
  img alt/size, single h1, exact repeated text inside a page.
- Translation memory scripts/i18n/*/done.json was NOT updated for the "above -> below" fix (strings stored differently);
  if a locale is ever rebuilt from it, re-run the fix.

## 2026-10-06/07 "popular content with few competitors" -> news batch 3
- Search Console 90-day pull (data exists for ~28 days: 129 clicks / 4,030 impressions; most queries hidden). Findings:
  valuation queries already sit at positions 7-10 in fr/it/pt/es/ru with titles that match them (nothing to fix);
  marketplace-intent queries ("hesap satin al", "vendita account", "mua acc") are NOT ours to chase;
  news articles reach page 1 quickly in ko/ja/id where few pages compete -> fresh official news is the lever.
- Batch 3 (a001fa5e, 48fa5975): 4 articles x 24 langs from Supercell pages of Oct 1-5 (scripts/research/news-2026-10.md,
  texts news_text_b3_*.py). news_data.PUBLISHED_AT gives new articles their own publication day; old ones unchanged.
- BUILD ORDER (learned the hard way): all 24 languages must have texts BEFORE running news_pages.py - a partial build
  drops hreflang to the missing languages on every old article. After news_pages.py always run nav_menu.py,
  footer_nav.py, consistency.py, then check `git diff --ignore-cr-at-eol --name-only` shows no old article.
  Commit pages first, then sitemap_lastmod.py (it needs the commit), then commit the sitemaps.
- NEXT news candidates: Clash Royale October balance changes (2026-10-06); moonton / minecraft.net / hoyoverse lists were
  not readable on 2026-10-06 - retry; Fortnite stays unreadable (403).
- Lighthouse from this PC: ru homepage perf 59, vi/roblox 78, a11y/BP/SEO 100; PSI quota exhausted - re-measure before acting.
- Batch 4 (same night): 3 more articles x 24 langs - Clash Royale October balance (Supercell 10-06), MLBB Asian Games gold
  for Myanmar (MOONTON 10-01, en.moonton.com/news/378.html - the list page 404s, article ids are sequential), Minecraft
  final 2026 game drop testing (Mojang 09-30; minecraft.net answers curl with a browser User-Agent, WebFetch times out).
  Site now: 1,417 pages, 31 news articles per language. Numbers of every translation checked against the English text.

## 2026-10-06 Google guidance re-read (developers.google.com/search/docs)
- Helpful content (page updated 2026-10-05): "Who" - is it self-evident who authored; "How" - is the use of automation,
  including AI-generation, self-evident through disclosures; no preferred word count; do not change dates without
  substantial change; warning sign = content produced primarily to attract search visits.
  -> AI disclosure sentence restored on About x24 (a3769043). Author stays in the footer + news byline + Person LD.
- Spam policies (2026-08-28): scaled content abuse includes generative-AI pages "without adding value" and automated
  transformations like translating where little value is provided; "stitching or combining content from different web
  pages without adding value". RISK FOR OUR NEWS: 7 articles x 24 languages in one day, AI-written and AI-translated.
  What keeps them on the right side: one primary source per article, our own "what it means for account value"
  paragraph, real demand per language. Do NOT raise the pace or add news that has nothing to say about accounts.
- FAQ rich results: shown only for well-known government and health sites - our FAQPage markup earns no rich result;
  it only has to match the visible questions (it does).
- Article markup (2026-09-08): no required properties; recommended author / datePublished / dateModified / headline /
  image; images in 16x9, 4x3 and 1x1, at least 50K pixels. We give one image per article - optional improvement.
- NOT rolled out: "what an estimate can and can't tell you" block (pilot on CoC en+ru). It repeats the asking-price
  note and the ToS warning already on the page - conflicts with the owner's no-duplicates rule; owner decides.
- One-shot reminder set in the session for 2026-10-07 14:17 local (quota reset): vi creators for 6 games + PSI re-measure.

## 2026-10-07 cross-page number consistency
- Comparison + market-report (24 langs, 5b2e748a): Mobile Legends ceiling "$2,500" was never on the ML page -> "~$605
  (Indonesia)" (row moved below Free Fire); Free Fire typical "$150" -> "$250". Table + FAQ JSON-LD together.
- Market report, older long-form version (13 langs: es tr ar vi hi fr de it ja ko th pl zh): Free Fire 150 -> 250,
  Minecraft 630 -> 632 in headline, paragraph and JSON-LD.
- OPEN, larger: those 13 languages still carry the old long-form market report (about 48 KB, own paragraphs per game,
  FAQPage LD) while en/ru/pt/id and the 7 newer locales have the short card hub (24 KB). The long form repeats the game
  pages and drifts out of date (still there: Clash Royale "typical $0.50-$150" vs comparison table "$0.50-$300";
  Genshin "$15-$300" vs game page "starter $5-$60"). Proper fix: rebuild the 13 pages as the card hub
  (about 18 short strings per language to translate). Not done yet.
- Calculators: every sourced figure on the game pages is already used; new fields need per-item listing data that can
  only be spot-checked by hand in the owner's Chrome (extension was not connected on 2026-10-06/07).
- How to re-run this check: compare each game's hero range with market-report cards / price-range lines and the
  comparison table (see the 2026-10-07 session); calculators.js brackets must equal the page table.
- Market report hub for the 13 legacy languages (e676f582): scripts/design/market_report_hub.py rebuilds <main> as nine
  cards with the game pages' headline figures, drops FAQPage LD, sets the hub meta description. Idempotent. When a game's
  headline range changes, update RANGE there AND the cards in the 11 hand-made hubs (en ru pt id tl sw ms uz kk tk ky).
- Minecraft calculator (3afc46d9): five named capes as checkboxes, prices = the mccapers.com ranking already quoted on
  minecraft.html (Sept 2026). Page note, checklist and FAQ LD updated in 24 langs. Refresh with the page (~2026-10-28).
- Structure check across languages (h2/h3/table/li counts per page type): only expected differences left - pilot
  "estimate limits" block on CoC and Clash Royale (en+ru), creators blocks (pt ar vi), local-market sources (zh ja ko pl),
  Roblox Limiteds top-5 as a table in en vs a list elsewhere.
- External links (120 publisher / news / wiki URLs checked once): no 404; 40 answer 403 to scripts (fandom, liquipedia,
  minecraft.wiki, kotaku, doi.org, fortnite.com) - bot protection, not dead links.
- Reference links added where three pages lacked them: zh Minecraft (10 capes), zh Fortnite (8 skins), ar Genshin (4).
- MISTAKE to avoid: b25fe121 went out with invalid JSON-LD on zh/minecraft.html for ~5 minutes - the edit matched the first
  occurrence of a sentence, which was the FAQ answer inside JSON-LD, and the push was not gated on the checker
  (fixed in 32013fe9). Rules: (1) when editing visible text, search from '<main', never from the top of the file;
  (2) push only if `site_check.py` prints exactly "ERRORS: 0" - gate the command on it, do not just print it.
- Official Discord links: only Clash of Clans and Minecraft publish one in their own site HTML; Brawl Stars and Clash Royale
  list Facebook / Instagram / Reddit / TikTok / X / YouTube, no Discord. Not enough for a block - not added.
