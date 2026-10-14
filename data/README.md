# Game account prices — open data (GameAccountValue)

`game-account-prices.csv` — asking-price ranges for game accounts in 10 games, as published on
[gameaccountvalue.com](https://gameaccountvalue.com/market-report.html). One row per game.

| Column | Meaning |
|---|---|
| `usual_low_usd`, `usual_high_usd` | the range most listings ask, in US dollars |
| `top_listing_usd`, `top_listing_note` | the highest listing seen and what it was |
| `price_basis` | always **asking prices in public listings, not completed sales** |
| `checked` | the date the listings were viewed (ISO 8601) |
| `marketplaces` | where the listings were seen |
| `page` | the full breakdown with every source link |

**How the data was collected.** Public listings were viewed by hand on the dates given — no scraping,
no automated collection. Other currencies were converted at the rate of that day. Every figure links to
its sources on the game's page. Nothing here is a price guarantee or an offer: trading accounts breaks
most games' terms of service, and the site does not recommend it.

**Updates.** Re-checked monthly; the file in this folder is always the current version, and earlier
versions stay in the git history.

**License.** The data in this folder is released under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/): use it freely, credit
"GameAccountValue (gameaccountvalue.com)". The site's code is under the repository's GPL-3.0 license.

**Cite.** See [`CITATION.cff`](../CITATION.cff).
