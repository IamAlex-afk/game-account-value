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

## Next steps
1. Finish Brawl Stars country data (BR, KR still unverified), build the
   section, show owner on 2-3 languages.
2. Other 8 games (start with Mobile Legends, Free Fire — strong regional leagues).
3. Events timelines for the other 8 games (official sources only).
4. SEO/AI audit: update llms.txt; Event JSON-LD only for in-person events;
   owner to add the site to Bing Webmaster Tools (AI Performance report).
5. LCP 2.4–2.9 s → target ≤ 2.5 s.
