<p align="center">
  <img src="og-image.png" alt="GameAccountValue — AI-powered game account appraisal" width="500">
</p>

<h1 align="center">GameAccountValue</h1>
<p align="center"><strong>Landing page for an AI-powered game account appraisal bot — not a marketplace, an independent estimate.</strong></p>

<p align="center">
  <img src="https://img.shields.io/badge/pages-live-success" alt="GitHub Pages: live">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-GPL--3.0-blue.svg" alt="License: GPL-3.0"></a>
  <img src="https://img.shields.io/badge/languages-24-brightgreen" alt="24 languages">
  <img src="https://img.shields.io/badge/build-vanilla%20JS-yellow" alt="Vanilla JS, no framework">
</p>

<p align="center"><strong>🔗 Live: <a href="https://game-account-value.com/">game-account-value.com</a></strong></p>
<p align="center">Bot: <a href="https://t.me/GameAccountValue_Bot">@GameAccountValue_Bot</a></p>

---

## What it is

Landing page for **[@GameAccountValue_Bot](https://t.me/GameAccountValue_Bot)**, a Telegram bot that gives an independent, AI-generated market value estimate for game accounts. Send screenshots of your inventory — the bot's AI vision reads them like a human appraiser and returns a price range plus a verifiable PDF certificate.

Supported games: Roblox, Brawl Stars, Clash of Clans, Clash Royale, Free Fire, Genshin Impact, Mobile Legends, Fortnite, Minecraft.

<p align="center">
  <img src="certificate-sample.jpg" alt="Example GameAccountValue PDF certificate" width="480">
  <br><em>Example certificate — sample data</em>
</p>

## What it's not

- **Not a marketplace.** We don't buy, sell, or broker accounts — only estimate their value.
- **Not a data harvester.** Screenshots are processed in RAM only and discarded after analysis; user IDs are SHA-256 hashed, never stored raw.

## Features

- ✅ **24 languages** — 17 with the full 13-page depth (9 per-game reports + methodology, glossary, safety guide, cross-game comparison): en, ru, es, fr, pt, id, ar, de, tr, vi, hi, it, ja, ko, zh, pl, th. The remaining 7 (tl, sw, ms, uz, kk, tk, ky) currently ship the homepage + market-report only.
- ✅ **Dual currency** — prices shown in USD and the visitor's local currency
- ✅ **Verifiable PDF certificates** — 9-tier gamer-style badge ladder (Wood → Whale) by estimated value, sequential collector's certificate number, QR + clickable links to both the site and the bot for instant authenticity checks
- ✅ **Joystick-style quick calculator** on every per-game page — D-pad UI, no signup, nothing sent anywhere until the user opts into the bot
- ✅ **Installable PWA** with offline support
- ✅ **Lighthouse 98 / 100 / 96 / 100** — Performance, Accessibility, Best Practices, SEO (measured 2026-09-11)

## Tech stack

Vanilla JavaScript, HTML, CSS. No frameworks, no bundler. Fully static, deployed as-is to GitHub Pages.

## Structure

```
index.html                  homepage (English)
{game}.html                  9 per-game market reports (roblox, brawl-stars, clash-of-clans,
                              clash-royale, free-fire, genshin-impact, mobile-legends, fortnite, minecraft)
methodology.html, glossary.html, account-trading-safety.html,
which-game-accounts-are-most-valuable.html   resource pages
market-report.html           cross-game hub
{lang}/                      localized copy of the above — full 13-page depth for
                              ru, es, fr, pt, id, ar, de, tr, vi, hi, it, ja, ko, zh, pl, th;
                              index.html + market-report.html only for tl, sw, ms, uz, kk, tk, ky
privacy.html, terms.html     legal pages
robots.txt, sitemap.xml      SEO
llms.txt, ai.txt             structured info for AI crawlers/agents (JSON-LD also embedded inline)
manifest.json, favicon.svg/.png, og-image.png   PWA manifest and social preview
.well-known/security.txt, SECURITY.md
sw.js                        service worker — offline support, installable PWA
assets/calculators.js        per-game quick calculator + joystick/D-pad UI
assets/analytics-placeholder.js   no-op event hook (window.gavTrackEvent), wired via data-event
                              attributes on CTA buttons — no third-party analytics wired up yet
.github/workflows/validate.yml   html-validate CI (root pages) — not yet active, needs a token
                              with the `workflow` scope to push
```

## Run locally

No build step — just serve the directory:

```bash
python -m http.server 8080
# open http://localhost:8080
```

## License

GPL-3.0 — see [LICENSE](LICENSE). © 2026 Aleksei Bitkin.
