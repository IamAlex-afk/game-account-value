# GameAccountValue — Design System

This file exists so design decisions on this site are made against a fixed
reference instead of improvised per prompt. Read this before making any
visual change (colors, layout, new page themes). It captures both the
site's existing base tokens and the working method for extending them.

## Method: two passes, not straight to CSS

**Pass 1 — plan before coding.** For any new visual work, write down:
- **Color**: which tokens, and *why* (grounded in the actual subject —
  not a generic genre label).
- **Type**: which existing font roles apply — don't introduce new
  typefaces without a reason.
- **Layout**: one sentence + rough structure, not just "make it modern."
- **Principle**: the one thing that makes this treatment specific to
  *this* content, not reusable for any other page.

**Pass 2 — check before shipping.** Before writing the CSS, ask: does any
part of this "read like the generic default you'd produce for any similar
page"? If yes, revise the concept, not just the color values.

**Restraint.** Spend boldness in one place per page. Pick the single most
important element (usually the number the visitor came for) and let that
carry the visual weight. Everything else stays quiet. Structural devices
(borders, color-coding, dividers) should encode information, not decorate.

**Self-critique.** Screenshot and look at real output before calling
something done, whenever the environment allows it (Claude in Chrome).
When it isn't available (as has been the case in this project so far —
no browser connection all session), say so explicitly rather than
claiming a visual result is confirmed.

## Patterns to avoid ("AI slop" defaults)

These aren't wrong in themselves — they're overused defaults. Only use
one if the brief specifically calls for it, not by default:
- Dark background + acid-neon accent (hot pink/cyan cyberpunk, acid-green,
  vermilion) — this was the first (rejected) version of the Fortnite
  theme; see git history. It's a generic "make it edgy" cliché, not
  something derived from Fortnite's actual subject matter.
- Warm cream background + serif + terracotta.
- Identical rounded "SaaS cards" with uniform shadow + gradient decoration.
- ALL-CAPS eyebrow labels, middle-dot metadata, arrow-appended links as
  decoration rather than function.
- Scattered motion (fade-and-slide-up on every section, flicker/pulse on
  multiple elements at once) instead of one deliberate moment.

## Base tokens (site-wide, `assets/style.css`)

Brand: "Aurora-glass" — deep charcoal-emerald base, gold/emerald gradient,
frosted-glass surfaces. Shared with the Telegram bot's PDF certificate
(`core/drawer.py` in the private bot repo) — keep any site-wide token
change in sync with that if it's ever touched.

| Token | Value | Role |
|---|---|---|
| `--gold` | `#D4AF37` | primary accent — CTAs, prices, headings |
| `--emerald` | `#12b892` | secondary accent — calculator UI |
| `--bg` | `#08100E` | page background |
| `--card` | `rgba(255,255,255,0.045)` | glass panel fill |
| `--border-strong` | `rgba(212,175,55,0.4)` | accent borders |
| `--text` / `--muted` | `#F1F2F6` / `#9c9cac` | body / secondary text |
| `--serif` | `'GAVSerif', Georgia, serif` | headings, h2 eyebrow labels |
| `--body-font` | `'GAVBody', system sans` | body text |

Every report page (`{game}.html`) re-declares these as CSS custom
properties in its own inline `<style>` block if it wants a per-game
theme — see "Per-game themes" below. Because shared components
(`.btn-primary`, `.section-nav a`, `.resources-callout a`, etc.) are all
built on `var(--gold)` / `var(--emerald)`, redeclaring the variables
re-themes the whole page without touching those shared rules.

## Per-game themes (done — pending real visual review)

Goal: each game's report page gets a distinct visual accent reflecting
that game's own vernacular — not its trademarked logo/art/typeface
(false-affiliation risk — the footer explicitly disclaims any
affiliation with the game studios), but a *generic* concept genuinely
tied to the page's subject matter. Every theme redeclares `--gold` /
`--gold-rgb` / `--border-strong` and overrides `.nav-cta` / `.btn-primary`
/ `.resources-callout a` / `.logo::before` under a `body.theme-*` class,
applied to the English page and all 16 Level-1 languages identically.
`.price-range` (the single number every visitor came for) stays a
consistent warm amber-gold (`#FF9D2E`/`#FFB35C`) glow across every
theme on purpose — one recognizable "here's your answer" signal
regardless of which game's UI color surrounds it.

| Game | Class | Accent | Grounding (not decoration) |
|---|---|---|---|
| Roblox | *(none)* | brand gold/emerald | Base brand, no override |
| Fortnite | `theme-rarity` | Epic purple `#A855F7` | Skin *rarity* drives value (price-bracket table color-coded common→legendary) |
| Brawl Stars | `theme-mythic` | Mythic pink `#E8449A` | Trophies + Mythic/Legendary skin rarity (llms.txt-cited value drivers) |
| Clash of Clans | `theme-bronze` | Bronze/copper `#C17A3D` | Town Hall/hero level progression, CWL medals — "war village" upgrade ladder |
| Clash Royale | `theme-royal` | Royal blue-violet `#6C5CE7` | King Tower level, card evolutions — "Royale"/crown/arena vocabulary; deliberately cooler than CoC despite being a sister game |
| Free Fire | `theme-diamond` | Diamond cyan `#22C1D6` | Diamond count is a named value driver — the in-game currency's own color |
| Genshin Impact | `theme-gacha` | Gacha lavender `#A78BFA` | 5-star character/weapon pull count — genre-wide gacha-banner purple |
| Mobile Legends | `theme-immortal` | Mythic crimson `#E63950` | Competitive rank — MOBA "Mythic/Immortal" top-rank color convention |
| Minecraft | `theme-overworld` | Overworld green `#6B9B3A` | No natural rarity ladder here, so this one also sharpens corners (`border-radius` down on cards/pills) — a nod to voxels, the game's actual defining trait, not just a color swap |

**Not yet done:** real screenshot review. No browser connection was
available for this whole rollout (Claude in Chrome never connected) —
every theme above was built and validated (`html-validate`, JSON-LD
parse, CSS brace balance) but never actually *seen*. Treat this table
as "implemented per the stated logic," not "confirmed to look good."
Open each theme in a real browser and compare against the anti-slop
list before calling this fully done.

## How to apply

Before any new per-game theme: write the Pass 1 plan in the PR/commit
message or in chat first, get it reviewed, then implement. Before
declaring a visual change "done": either get a real screenshot (Claude
in Chrome) or say plainly that it wasn't visually verified.
