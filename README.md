# GameAccountValue — Landing Page

Landing page for [@GameAccountValue_Bot](https://t.me/GameAccountValue_Bot), a Telegram bot that
gives an independent, AI-generated market value estimate for game accounts (Roblox, Brawl Stars,
Clash of Clans, Clash Royale, Free Fire, Genshin Impact, Mobile Legends, Fortnite, Minecraft).

**Live site:** https://iamalex-afk.github.io/game-account-value/

## Structure

- `index.html` — homepage (English)
- `{lang}/index.html` — localized versions: ru, es, pt, id, tr, ar, vi, hi, fr, de, it, ja, ko, th
- `privacy.html`, `terms.html` — legal pages
- `robots.txt`, `sitemap.xml` — SEO
- `llms.txt`, `ai.txt` — structured info for AI crawlers/agents (JSON-LD is also embedded inline
  in every page)
- `manifest.json`, `favicon.svg` / `favicon.png`, `og-image.png` — PWA manifest and social preview
- `.well-known/security.txt`, `SECURITY.md` — security contact and policy
- `sw.js` — service worker (offline support, installable PWA)

## Deploy

Static site, auto-deployed to GitHub Pages on every push to `main`. No build step.

## License

GPL v3 — see [LICENSE](LICENSE).
