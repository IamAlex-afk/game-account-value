# World markets — research data (asking prices only, with source + date)

Rule: a row goes on the site only if the marketplace page was actually viewed.
Blocked / unreachable = listed as a data gap, never estimated.

## Brawl Stars

| Market | Marketplace | Seen (local) | ≈ USD | What listings emphasise | Source / checked |
|---|---|---|---|---|---|
| Global / West | Eldorado.gg, igitems.com (1,147 listings) | $3 – $35 (Eldorado top shown); most $15–$150; 34 listings > $300 | same | trophies + brawler count; top 10 priced listings named **no** rare skin | brawl-stars.html (checked Sep 2026) |
| Global forum | EpicNPC (via search index, direct fetch blocked) | up to $1,700 asking (one outlier, Jun 2026) | same | whale titles | brawl-stars.html |
| RU / CIS | FunPay | €0.21 – €3,852 | ≈ $0.23 – $4,160 | "all hypercharges maxed", coins, trophies | brawl-stars-news.html, 2026-09-21 |
| SEA (VN pricing) | igitems.com | ₫318,890 – ₫10,716,283 | ≈ $13 – $429 (25,000 VND/$) | trophies, brawlers maxed, skins count; platform notes oversupply, falling asks | brawl-stars-news.html, 2026-09-21 |
| China | 交易猫 jiaoyimao.com (荒野乱斗 成品号), 15 listings visible | ¥100 – ¥1,200 | ≈ $15 – $179 (≈6.71 CNY/$, early Sep 2026) | **cosmetics**: 绝版 (retired) skins, 星座 zodiac skins, wings, Master rank, "6-year account"; most offer 永久包赔 buyer protection | https://m.jiaoyimao.com/jg1009835/c1/ + www., 2026-09-28 |
| Japan | GameTrade (13,269 listings) | ¥500 – ¥23,000 in real listings (a ¥99,999 placeholder-style price also shown) | ≈ $3 – $146 (≈157 JPY/$, 2026-09-25) | trophies, Master rank, emeralds, "rank 1 in Japan", first owner | https://gametrade.jp/brawl-stars/exhibits, 2026-09-28 |
| Turkey | GameSatış (30+ on page 1) | 59.99 ₺ – 19,900 ₺ (173K trophies) | TRY rate not yet verified | cups (5K–173K), characters 50–107, costumes, gold/gems, 2021 accounts, Supercell ID/Gmail transfer | https://www.gamesatis.com/brawl-stars-hesap-satisi, 2026-09-28 |
| Brazil | GGMAX (403), Desapego Games, DFG | single listings R$26.90 (GGMAX via search), R$70 / R$100 (Desapego via search) | BRL rate not verified | — | search results only → **not verified yet** |
| Korea | ItemMania / ItemBay (merged 2014) | connection refused | — | — | **gap** |
| Turkey alt | itemsatis.com, hesap.com.tr | 403 | — | — | gap |

Exchange rates found: USD/JPY 157.23 (2026-09-25, tradingeconomics); USD/CNY ≈ 6.71–6.72 (early Sep 2026, mtfx).
TRY, BRL: still to verify before showing USD equivalents.

Cross-country insight (descriptive): Western top listings sell on trophies/brawlers;
Chinese and Japanese listings foreground cosmetics and rank status.

### Update 2026-09-28 (later)
- Korea: 저팔계 jeo8gye.com (25 listings incl. completed): ₩15,000 – ₩2,500,000; top = "Korea ranking #26, prestige 202"; also "600+ skins" ₩400,000. Rate ≈ 1,370 KRW/$ (Wise, 20–23 Sep 2026 range 0.000721–0.000740 USD/KRW) → ≈ $11 – $1,825.
- Korea forum (hungryapp): sale posts ₩10,000 – ₩70,000 (Sep 2026) — low-end, supports "most accounts are cheap, ranked accounts are the ceiling".
- Brazil: GGMAX, Desapego Games, DFG all 403 → **not verified** (only search snippets).
- Rates used: EUR/USD 1.1387 (2026-09-25), USD/CNY 6.71, USD/JPY 157.2, USD/KRW ≈1,370, USD/TRY ≈48.8, USD/BRL ≈5.18, VND 25,000/$.

## All games — esports & streamers (added 2026-09-28)
Esports Earnings country pages (fetched 2026-09-28): MLBB 531 (to 2026-08; PH #1 $8.69M), Free Fire 598 (to 2026-07; TH #1 $5.90M),
Fortnite 534 (to 2026-06; US #1 $53.5M), Clash Royale 464 (to 2024-11; JP #1, EG #2 via Mohamed Light), Clash of Clans 507 (to 2024-11; DE #1),
Minecraft 559 (to 2025-09; creator events; one "Undefined" country row dropped), Roblox 738 (single $100K creator event → not shown),
Genshin: not listed (no esports). TwitchMetrics (avg viewers 30 days, updated 2026-09-25) for every game; Roblox: no results.
Genshin China row: UU898 ¥105.60–¥225.60 (from zh/genshin-impact.html research, Sep 2026).
Markets for the 8 games: global = game-page market range; CIS = FunPay, SEA = igitems (news pages, 2026-09-21).
Data lives in scripts/design/world_data.py (MARKETS, EXTRA, N notes, TW_ONLY).

## Round 2 (2026-09-28): JP / CN / KR / TR for the other games
- JP GameTrade: Genshin 119,857 listings, real range ¥3,000–¥2,500,000 (top: 8 C6 chars, "total spend ¥3M+"); ¥888,888/¥999,999 placeholders excluded.
  Clash Royale 4,461 listings ¥2,500–¥180,000; Clash of Clans 4,496 listings ¥1,280–¥248,000 (TH18). Fortnite JP section is mostly
  "Brainrot" creative-mode item trading, not accounts → not shown.
- CN 交易猫: Genshin 成品号 ¥118–¥7,500 (123 five-stars); 部落冲突 ¥210–¥12,888 (mostly TH18); 皇室战争 no listings visible.
- KR 저팔계: Genshin (game_code=89) ₩50,000–₩2,500,000; other games' codes not discoverable → gap.
- TR GameSatış: Fortnite 400–11,000₺; CoC 100–19,000₺ (top = rare name "Constantine"); CR 100–29,999₺; Roblox 50–18,000₺ (Headless+Korblox);
  Genshin 500–25,000₺ (118 five-stars); Free Fire 450–15,000₺ (Prime 8); MLBB 250–50,000₺ (807 skins). Minecraft 404.
Data: scripts/design/world_data2.py
