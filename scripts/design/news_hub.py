"""news.html — hub of the 9 per-game "Fresh Market Watch" pages, newest first.
Built from roblox-news.html's shell; cards read each page's h1, lead and check date.
Run after any *-news.html update: python scripts/design/news_hub.py"""
import os, re, json, html as H, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + os.sep
SITE = 'https://gameaccountvalue.com/'
GAMES = ['roblox', 'brawl-stars', 'clash-of-clans', 'clash-royale', 'free-fire', 'genshin-impact', 'mobile-legends', 'fortnite', 'minecraft']

def card_data(g):
    s = open(ROOT + g + '-news.html', encoding='utf-8').read()
    h1 = re.sub(r'<[^>]+>', '', re.search(r'<h1>(.*?)</h1>', s, re.S).group(1)).strip()
    lead = re.search(r'</h1>\s*<p[^>]*>(.*?)</p>', s, re.S).group(1).strip()
    date = re.search(r'"dateModified"\s*:\s*"([0-9-]+)"', s) or re.search(r'"datePublished"\s*:\s*"([0-9-]+)"', s)
    return dict(slug=g, h1=h1, lead=re.sub(r'<[^>]+>', '', lead), date=date.group(1) if date else '')

def main():
    cards = sorted((card_data(g) for g in GAMES), key=lambda c: c['date'], reverse=True)
    newest = cards[0]['date']
    nice = datetime.date.fromisoformat(newest).strftime('%B %-d, %Y') if os.name != 'nt' else datetime.date.fromisoformat(newest).strftime('%B %d, %Y').replace(' 0', ' ')
    s = open(ROOT + 'roblox-news.html', encoding='utf-8').read()
    title = 'Fresh Game Account Market News — 9 Games | GameAccountValue'
    desc = f'Fresh region-by-region account market watch for Roblox, Fortnite, Genshin Impact, Free Fire and 5 more games — real listings, sources and check dates. Latest update {nice}.'
    s = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', s, 1)
    s = re.sub(r'(<meta name="description" content=")[^"]*', r'\g<1>' + H.escape(desc), s, 1)
    s = re.sub(r'(<meta property="og:title" content=")[^"]*', r'\g<1>Fresh Market News — GameAccountValue', s, 1)
    s = re.sub(r'(<meta name="twitter:title" content=")[^"]*', r'\g<1>Fresh Market News — GameAccountValue', s, 1)
    s = re.sub(r'(<meta property="og:description" content=")[^"]*', r'\g<1>' + H.escape(desc), s, 1)
    s = s.replace('/og/roblox.jpg', '/og/default.jpg').replace('GameAccountValue — Roblox account value', 'GameAccountValue — game account value for 9 games')
    s = s.replace(SITE + 'roblox-news.html', SITE + 'news.html')
    items = [{'@type': 'ListItem', 'position': i + 1, 'url': SITE + c['slug'] + '-news.html', 'name': c['h1'].replace('📰 ', '')} for i, c in enumerate(cards)]
    ld = {'@context': 'https://schema.org', '@type': 'CollectionPage', 'name': 'Fresh Market News', 'url': SITE + 'news.html',
          'description': desc, 'dateModified': newest, 'inLanguage': 'en',
          'isPartOf': {'@type': 'WebSite', 'name': 'GameAccountValue', 'url': SITE},
          'mainEntity': {'@type': 'ItemList', 'itemListElement': items}}
    s = re.sub(r'<script type="application/ld\+json">.*?</script>', '', s, flags=re.S)
    s = s.replace('</head>', '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + '</script>\n</head>', 1)
    grid = ''.join(
        f'\n  <a class="news-card" href="./{c["slug"]}-news.html"><span class="news-date">🕒 {c["date"]}</span>'
        f'<strong>{H.escape(c["h1"].replace("📰 ", ""))}</strong><span class="news-lead">{H.escape(c["lead"])}</span>'
        f'<span class="news-more">Read the update →</span></a>' for c in cards)
    main = (f'<main>\n<section class="report-hero" id="main-content">\n  <h1>📰 Fresh Market News</h1>\n'
            f'  <p style="color:var(--muted); font-size:16px;">What game accounts are listed for right now, region by region — with sources and the date every number was checked.</p>\n'
            f'  <div class="fresh-badge">🌍 Latest update: {nice}</div>\n</section>\n'
            f'<section class="news-grid">{grid}\n</section>\n</main>')
    s = re.sub(r'<main>.*?</main>', lambda m: main, s, 1, flags=re.S)
    open(ROOT + 'news.html', 'w', encoding='utf-8', newline='').write(s)
    print('news.html:', len(cards), 'cards, newest', newest)

if __name__ == '__main__':
    main()
