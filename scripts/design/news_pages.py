"""News section in every language (SITE-STANDARD step 4).
  article     {lang}/news-<game>-<yyyy-mm>-<slug>.html   NewsArticle + BreadcrumbList
  game hub    {lang}/<game>-news.html                   CollectionPage (replaces the old market-watch pages)
  news hub    {lang}/news.html                          CollectionPage, newest first
  game pages  "Latest <game> news" block under the calculator
Data: news_data.py (English + article list), news_text_*.py (translations). Shell = the language's
glossary.html, so menu, footer, CTA and styles match the site. Then run nav_menu.py. Idempotent."""
import glob, html, importlib, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE)) + os.sep
sys.path.insert(0, HERE)
import news_data as D

SITE = 'https://gameaccountvalue.com/'
LANGS = ['en', 'ru', 'es', 'pt', 'id', 'tr', 'ar', 'vi', 'hi', 'fr', 'de', 'it', 'ja', 'ko', 'th', 'pl', 'zh', 'tl', 'sw', 'ms', 'uz', 'kk', 'tk', 'ky']
TEXT = {L: {'ui': dict(v['ui']), 'a': dict(v['a'])} for L, v in D.TEXT.items()}
for f in sorted(glob.glob(os.path.join(HERE, 'news_text_*.py'))):
    for L, v in importlib.import_module(os.path.basename(f)[:-3]).TEXT.items():
        T = TEXT.setdefault(L, {'ui': {}, 'a': {}})
        T['ui'].update(v.get('ui', {}))
        T['a'].update(v.get('a', {}))
# a language is built only when it has the UI strings and every article
READY = [L for L in LANGS if L in TEXT and TEXT[L]['ui'] and all(a[0] in TEXT[L]['a'] for a in D.ARTICLES)]
AUTHOR = {'@type': 'Person', 'name': 'Aleksei Bitkin', 'url': SITE + 'about.html'}
PUBLISHER = {'@type': 'Organization', 'name': 'GameAccountValue', 'url': SITE,
             'logo': {'@type': 'ImageObject', 'url': SITE + 'favicon-192.png'}}
ARTS = sorted(D.ARTICLES, key=lambda a: a[3], reverse=True)
# Google: keep thin pages out of the index. A game's news hub is indexed only once it lists
# MIN_HUB_ARTICLES articles; until then it is 'noindex, follow' (crawlable, links followed),
# without hreflang and outside the sitemap. Opens automatically as articles are added.
MIN_HUB_ARTICLES = 3
# newest articles listed in the "Latest <game> news" block on the game page
GAME_BLOCK_ARTICLES = 3


def hub_indexable(game):
    return sum(1 for a in ARTS if a[1] == game) >= MIN_HUB_ARTICLES

CSS = ('<style>.news-wrap { max-width: 780px; margin: 0 auto; padding: 0 24px 40px; }'
       '.news-wrap h2 { font-size: 21px; margin: 30px 0 10px; } .news-wrap li { margin: 7px 0; } .news-wrap ul { padding-inline-start: 22px; }'
       '.news-meta { color: var(--muted); font-size: 14px; margin-top: 10px; }'
       '.news-chip { display: inline-block; padding: 4px 12px; border-radius: 999px; font-size: 13px; font-weight: 700; border: 1px solid rgba(34,211,238,.45); color: #A5F3FC; text-decoration: none; }'
       '.news-src { margin-top: 26px; padding: 14px 16px; border: 1px solid var(--border); border-radius: 12px; font-size: 14px; }'
       '.news-src a { word-break: break-word; } .news-note { color: var(--muted); font-size: 13px; margin-top: 18px; }'
       '.news-list { list-style: none; padding: 0 !important; display: grid; gap: 14px; }'
       '.news-card { display: block; padding: 16px 18px; border: 1px solid var(--border); border-radius: 14px; text-decoration: none; color: inherit; background: rgba(255,255,255,.02); }'
       '.news-card:hover { border-color: rgba(34,211,238,.6); } .news-card strong { display: block; font-size: 17px; line-height: 1.35; margin: 6px 0; color: #fff; }'
       '.news-card span { color: var(--muted); font-size: 14px; } .news-card em { font-style: normal; color: #A5F3FC; font-weight: 700; }'
       '.news-links { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 22px; } .news-links a { padding: 8px 14px; border: 1px solid var(--border); border-radius: 999px; text-decoration: none; font-size: 14px; }'
       '</style>')


def pub(aid):
    return getattr(D, 'PUBLISHED_AT', {}).get(aid, D.PUBLISHED)


def dates():
    ds = sorted({D.PUBLISHED} | set(getattr(D, 'PUBLISHED_AT', {}).values()) | {s[2] for a in D.ARTICLES for s in a[4] if s[2]})
    js = ('const L=%s,D=%s,o={};for(const l of L){o[l]={};for(const d of D)o[l][d]=new Intl.DateTimeFormat(l,{dateStyle:"long",timeZone:"UTC"}).format(new Date(d+"T00:00:00Z"))}console.log(JSON.stringify(o))'
          % (json.dumps(LANGS), json.dumps(ds)))
    return json.loads(subprocess.run(['node', '-e', js], capture_output=True, text=True, encoding='utf-8', check=True).stdout)


DATES = dates()


def url(L, name):
    return SITE + ('' if L == 'en' else L + '/') + name


def esc(v):
    return html.escape(v, quote=True)


def shell(L, slug, title, desc, crumbs, ld, main, og_type='website', image=None, index=True):
    s = open(ROOT + ('glossary.html' if L == 'en' else L + '/glossary.html'), encoding='utf-8').read()
    me = url(L, slug + '.html')
    full = title if len(title) > 55 else f'{title} | GameAccountValue'  # long titles: site name is shown by Google anyway
    for pat, val in ((r'<title>.*?</title>', f'<title>{esc(full)}</title>'),
                     (r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{esc(desc)}">'),
                     (r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{esc(full)}">'),
                     (r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{esc(desc)}">'),
                     (r'<meta property="og:type" content="[^"]*">', f'<meta property="og:type" content="{og_type}">'),
                     (r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{me}">'),
                     (r'<meta name="twitter:title" content="[^"]*">', f'<meta name="twitter:title" content="{esc(full)}">'),
                     (r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{me}">')):
        s = re.sub(pat, lambda m, v=val: v, s, count=1, flags=re.S)
    if image:
        s = re.sub(r'(<meta (?:property="og:image"|name="twitter:image") content=")[^"]*(")', lambda m: m.group(1) + image + m.group(2), s)
    s = re.sub(r'<link rel="alternate" hreflang="[^"]+" href="[^"]+">\n?', '', s)
    alts = f'<link rel="alternate" hreflang="x-default" href="{url("en", slug + ".html")}">\n' + ''.join(
        f'<link rel="alternate" hreflang="{x}" href="{url(x, slug + ".html")}">\n' for x in READY)
    if index:
        s = s.replace(f'<link rel="canonical" href="{me}">', f'<link rel="canonical" href="{me}">\n' + alts.rstrip('\n'), 1)
    else:
        s = re.sub(r'<meta name="robots" content="[^"]*">', '<meta name="robots" content="noindex, follow">', s, count=1)
    s = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', '', s, flags=re.S)
    s = s.replace('</head>', '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + '</script>\n' + CSS + '\n</head>', 1)
    home_img = re.search(r'<nav class="crumbs"[^>]*><ol><li><a href="\./">(<img[^>]*>)', s).group(1)
    label = re.search(r'<nav class="crumbs" aria-label="([^"]*)"', s).group(1)
    li = ''.join((f'<li><a href="{h}">{t}</a></li>' if h else f'<li aria-current="page">{t}</li>') for h, t in crumbs)
    li = li.replace('<li><a href="./">', f'<li><a href="./">{home_img}', 1)
    s = re.sub(r'<nav class="crumbs".*?</nav>', lambda m: f'<nav class="crumbs" aria-label="{label}"><ol>{li}</ol></nav>', s, count=1, flags=re.S)
    cta = re.search(r'(<img class="g-joystick".*?</div>)', s, re.S)
    main = main.replace('<!--CTA-->', cta.group(1) if cta else '')
    s = re.sub(r'<main>.*?</main>', lambda m: f'<main>\n{main}\n</main>', s, count=1, flags=re.S)
    s = s.replace('utm_campaign=glossary', 'utm_campaign=news')
    open(ROOT + ('' if L == 'en' else L + '/') + slug + '.html', 'w', encoding='utf-8', newline='').write(s)


def home_name(L):
    s = open(ROOT + ('glossary.html' if L == 'en' else L + '/glossary.html'), encoding='utf-8').read()
    return html.unescape(re.sub(r'<[^>]+>', '', re.search(r'<nav class="crumbs"[^>]*><ol><li><a href="\./">(.*?)</a>', s, re.S).group(1))).strip()


def bc(L, items):
    return {'@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': u} for i, (n, u) in enumerate(items)]}


def card(L, a):
    aid, game, slug, _, srcs = a
    T = TEXT[L]['a'][aid]
    d = DATES[L][srcs[0][2]] if srcs[0][2] else srcs[0][1]
    return (f'<li><a class="news-card" href="./{slug}.html"><span>{D.GAMES[game]} · {d}</span>'
            f'<strong>{T["title"]}</strong><span>{T["lead"]} <em>{TEXT[L]["ui"]["read"]} →</em></span></a></li>')


def article(L, a):
    aid, game, slug, _, srcs = a
    U, T, G = TEXT[L]['ui'], TEXT[L]['a'][aid], D.GAMES[game]
    me = url(L, slug + '.html')
    img = f'{SITE}og/{game}.jpg?v=3'
    ld = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'NewsArticle', '@id': me + '#article', 'mainEntityOfPage': me, 'headline': T['title'][:110], 'description': T['desc'],
         'image': [img], 'datePublished': pub(aid) + 'T09:00:00+00:00', 'dateModified': pub(aid) + 'T09:00:00+00:00',
         'inLanguage': L, 'author': AUTHOR, 'publisher': PUBLISHER, 'about': {'@type': 'VideoGame', 'name': G},
         'isBasedOn': [s[0] for s in srcs]},
        bc(L, [(home_name(L), url(L, '')), (U['news'], url(L, 'news.html')), (U['game_title'].format(game=G), url(L, game + '-news.html')), (T['title'], me)])]}
    src = '<br>'.join(f'<a href="{u}" rel="noopener">{esc(u.split("//")[1].split("/")[0])}</a> — {U["by_on"].format(pub=p, date=DATES[L][d]) if d else p}' for u, p, d in srcs)
    main = (f'<section class="report-hero" id="main-content">\n  <a class="news-chip" href="./{game}-news.html">{G}</a>\n  <h1>{T["title"]}</h1>\n'
            f'  <p style="color:var(--muted); font-size:16px;">{T["lead"]}</p>\n'
            f'  <p class="news-meta">{U["published"]}: <time datetime="{pub(aid)}">{DATES[L][pub(aid)]}</time> · Aleksei Bitkin</p>\n</section>\n'
            f'<div class="news-wrap">\n<h2>{U["whats_new"]}</h2>\n<ul>' + ''.join(f'<li>{x}</li>' for x in T['new']) + '</ul>\n'
            f'<h2>{U["impact"]}</h2>\n<p>{T["impact"]}</p>\n'
            f'<div class="news-src"><strong>{U["source"]}</strong><br>{src}</div>\n'
            f'<div class="news-links"><a href="./{game}.html">{U["calc"].format(game=G)}</a><a href="./{game}-news.html">{U["more"].format(game=G)}</a><a href="./news.html">{U["all"]}</a></div>\n'
            f'<p class="news-note">{U["note"]}</p>\n</div>\n<!--CTA-->')
    crumbs = [('./', home_name(L)), ('./news.html', U['news']), (f'./{game}-news.html', G), (None, T['title'])]
    shell(L, slug, T['title'], T['desc'], crumbs, ld, main, og_type='article', image=img)


def game_hub(L, game):
    U, G = TEXT[L]['ui'], D.GAMES[game]
    items = [a for a in ARTS if a[1] == game]
    title, lead = U['game_title'].format(game=G), U['game_lead'].format(game=G)
    me = url(L, game + '-news.html')
    ld = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'CollectionPage', '@id': me, 'url': me, 'name': title, 'description': lead, 'inLanguage': L,
         'hasPart': [{'@type': 'NewsArticle', 'headline': TEXT[L]['a'][a[0]]['title'][:110], 'url': url(L, a[2] + '.html')} for a in items]},
        bc(L, [(home_name(L), url(L, '')), (U['news'], url(L, 'news.html')), (title, me)])]}
    main = (f'<section class="report-hero" id="main-content">\n  <h1>{title}</h1>\n  <p style="color:var(--muted); font-size:16px;">{lead}</p>\n</section>\n'
            f'<div class="news-wrap">\n<ul class="news-list">' + ''.join(card(L, a) for a in items) + '</ul>\n'
            f'<div class="news-links"><a href="./{game}.html">{U["calc"].format(game=G)}</a><a href="./news.html">{U["all"]}</a></div>\n'
            f'<p class="news-note">{U["note"]}</p>\n</div>\n<!--CTA-->')
    shell(L, game + '-news', title, lead, [('./', home_name(L)), ('./news.html', U['news']), (None, G)], ld, main, index=hub_indexable(game))


def news_hub(L):
    U = TEXT[L]['ui']
    me = url(L, 'news.html')
    ld = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'CollectionPage', '@id': me, 'url': me, 'name': U['news_title'], 'description': U['news_lead'], 'inLanguage': L,
         'hasPart': [{'@type': 'NewsArticle', 'headline': TEXT[L]['a'][a[0]]['title'][:110], 'url': url(L, a[2] + '.html')} for a in ARTS]},
        bc(L, [(home_name(L), url(L, '')), (U['news'], me)])]}
    games = ''.join(f'<a href="./{g}-news.html">{n}</a>' for g, n in D.GAMES.items())
    main = (f'<section class="report-hero" id="main-content">\n  <h1>{U["news_title"]}</h1>\n  <p style="color:var(--muted); font-size:16px;">{U["news_lead"]}</p>\n</section>\n'
            f'<div class="news-wrap">\n<div class="news-links" style="margin-top:0">{games}</div>\n<ul class="news-list" style="margin-top:20px">' + ''.join(card(L, a) for a in ARTS) + '</ul>\n'
            f'<p class="news-note">{U["note"]}</p>\n</div>\n<!--CTA-->')
    shell(L, 'news', U['news_title'], U['news_lead'], [('./', home_name(L)), (None, U['news'])], ld, main)


def game_block(L, game):
    """'Latest <game> news' under the calculator on the game page."""
    p = ROOT + ('' if L == 'en' else L + '/') + game + '.html'
    s = open(p, encoding='utf-8').read()
    U, G = TEXT[L]['ui'], D.GAMES[game]
    items = ''
    for a in [x for x in ARTS if x[1] == game][:GAME_BLOCK_ARTICLES]:
        d = DATES[L][a[4][0][2]] if a[4][0][2] else a[4][0][1]
        items += f'<p><a href="./{a[2]}.html"><strong>{TEXT[L]["a"][a[0]]["title"]}</strong></a> <span style="color:var(--muted);unicode-bidi:isolate">· {d}</span></p>'
    block = (f'<section class="g-fresh" aria-label="{esc(U["latest"].format(game=G))}"><h2>📰 {U["latest"].format(game=G)}</h2>'
             f'{items}<p><a href="./{game}-news.html">{U["more"].format(game=G)} →</a></p></section>')
    s = re.sub(r'<section class="g-fresh".*?</section>\n?', '', s, flags=re.S)
    j = s.find('data-g-slot="result"')
    i = s.find('<section class="g-card', j) if j >= 0 else -1
    if i < 0:
        return 0
    s = s[:i] + block + '\n' + s[i:]
    open(p, 'w', encoding='utf-8', newline='').write(s)
    return 1


def sitemap():
    """Indexable news URLs in, noindex game hubs out (Google: list only URLs you want in Search)."""
    p = ROOT + 'sitemap.xml'
    s = open(p, encoding='utf-8').read()
    add, removed = '', 0
    for L in READY:
        for g in D.GAMES:
            if not hub_indexable(g):
                s, n = re.subn(r'\s*<url><loc>' + re.escape(url(L, g + '-news.html')) + r'</loc>.*?</url>', '', s)
                removed += n
        names = ['news.html'] + [g + '-news.html' for g in D.GAMES if hub_indexable(g)] + [a[2] + '.html' for a in ARTS]
        when = {a[2] + '.html': pub(a[0]) for a in ARTS}
        for name in names:
            u = url(L, name)
            if f'<loc>{u}</loc>' not in s:
                add += f'  <url><loc>{u}</loc><lastmod>{when.get(name, D.PUBLISHED)}</lastmod><changefreq>weekly</changefreq><priority>0.6</priority></url>\n'
    s = s.replace('</urlset>', add + '</urlset>')
    open(p, 'w', encoding='utf-8', newline='\n').write(s)
    return f'+{add.count("<url>")} -{removed}'


if __name__ == '__main__':
    only = sys.argv[1:] or READY
    n = blocks = 0
    for L in only:
        for a in ARTS:
            article(L, a); n += 1
        for g in D.GAMES:
            game_hub(L, g); n += 1
            blocks += game_block(L, g)
        news_hub(L); n += 1
    print('pages', n, 'game blocks', blocks, 'sitemap +', sitemap())
