# GameAccountValue — site standard (working prompt)

Read this, `scripts/research/WORK-LOG.md` and `git log -10` at the start of every session.
Owner rules (Telegram): short Russian replies, "стоп" = stop now, facts from primary sources only,
push only after verification, never break the certificate/verification logic, no data collection on the site.

## Why this file exists
Anthropic's prompting guide for long tasks: a clear standard with the *why*, incremental progress,
state in git + structured files, and verification tools before claiming "done". Google's guides:
full (not boilerplate-only) translation, no automated translation "at scale with little value",
people-first content, visible dates that change only when content changes, E-E-A-T (who/how/why).

## Definition of done (every change)
1. `python scripts/site_check.py` → **0 errors** (language completeness, hreflang, JSON-LD, links,
   English leftovers, required blocks).
2. Screenshots at 390 px and 1280 px of what changed (fresh Chrome profile), RTL (ar) checked.
3. No horizontal overflow at 360/390/768/1280.
4. Commit with a real description → push → `gh run list` shows **success** → live URL returns 200.
5. Lighthouse mobile on the live homepage: Performance ≥ 90, A11y/BP/SEO 100.
6. IndexNow ping for new/changed URLs; sitemap updated for new pages.
7. Remind the owner: browser cache (Ctrl+Shift+R / clear site data) if the change isn't visible.

## Every language (24: en ru es pt id tr ar vi hi fr de it ja ko th pl zh tl sw ms uz kk tk ky)
Must have the same page set as English, each fully translated (headings, body, alt, meta, JSON-LD):
home · 9 game pages · market-report · which-game-accounts-are-most-valuable · account-trading-safety ·
glossary · methodology · news hub + 9 game news · privacy · terms · about.
Translation = adapted human-quality (local number/date formats, local examples, correct register),
never machine-dumped; English leftovers only for brand/game/item names.

## Every page
Site header menu (Games/Guides/News + same-page language switcher) · breadcrumbs (except home) ·
one primary action (bot CTA) with the card teaser under calculators · 18+ card + notice in the footer ·
canonical to itself · hreflang to all existing translations · valid JSON-LD · unique title/description.

## Page types — what Google's guides ask for
- **Game page (tool + report):** calculator, real price ranges with sources and dates, what raises/
  lowers value, comparison links, honest pros & cons, scam risks, rules, FAQ, sources list.
- **News article:** its own URL, headline from a real fact, visible "Published/Updated", NewsArticle
  JSON-LD (headline, image, datePublished, dateModified, author), sources (official publishers only —
  no marketplace scraping: Eldorado ToS §3.1), links to the game page, homepage and bot.
- **About:** who runs it (Aleksei Bitkin), how estimates are made, what we never do (trade/collect data),
  contact route (Telegram bot / GitHub), links to methodology, privacy, terms.
- **Legal (privacy/terms):** full translation in each language (GDPR: information in a language the
  user understands); English stays the reference version.

## Plan (2026-09-30 → in order; tick when pushed)
- [x] 1. This standard + `scripts/site_check.py`; README/llms.txt fixed (broken og image, cards)
- [x] 2. privacy + terms in 23 languages (+ hreflang, sitemap, menu)
- [x] 3. about page in 24 languages (E-E-A-T)
- [x] 4. News: refresh from official publisher sources → one article per real fact, NewsArticle LD;
      news hub + articles in 24 languages
- [ ] 5. Game pages: honest "pros & cons of valuing this account" block, 24 languages
- [ ] 6. Footer section links (Games · Guides · News · About · Privacy · Terms) on every page
- News refresh routine: add facts to scripts/research/news-YYYY-MM.md (publisher sources only), new entries in
      news_data.ARTICLES + TEXT for all 24 languages (news_text_*.py), then `python scripts/design/news_pages.py`
      and `nav_menu.py`; our datePublished = publish day, publisher date shown separately.
- [ ] Owner actions: bot server `bash /opt/gavbot/app/deploy/install.sh`; WhatsApp preview test;
      Eldorado affiliate/data-permission decision; founders /gift + public counter + rules page (needs "да")
