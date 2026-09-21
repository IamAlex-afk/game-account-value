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

## Per-game themes (in progress)

Goal: each game's report page gets a distinct visual accent reflecting
that game's own vernacular — not its trademarked logo/art/typeface
(false-affiliation risk — the footer explicitly disclaims any
affiliation with the game studios), but a *generic* concept genuinely
tied to the page's subject matter.

Status:
- **Roblox** — base brand tokens (gold/emerald), no override. Button
  modernization applied.
- **Fortnite** — in progress. First attempt (hot pink + cyan "cyberpunk"
  neon, scanline overlay, flickering H1) was reviewed against the "AI
  slop" list above and rejected as a generic default, not a grounded
  choice. Current direction: the page's own subject is skin *rarity*
  driving account value (see the "by skin count" price-bracket table) —
  loot-rarity tiering (common→uncommon→rare→epic→legendary, a genre-wide
  convention, not Fortnite-exclusive IP) is the actual differentiator to
  design around, e.g. color-coding the price-bracket table by tier and
  giving the single most important number (the price range) the
  "legendary" treatment, rather than decorating the whole page.
- Remaining 7 games — not started. Do Pass 1 (above) per game before
  touching CSS; don't reuse Fortnite's palette for a different game.

## How to apply

Before any new per-game theme: write the Pass 1 plan in the PR/commit
message or in chat first, get it reviewed, then implement. Before
declaring a visual change "done": either get a real screenshot (Claude
in Chrome) or say plainly that it wasn't visually verified.
