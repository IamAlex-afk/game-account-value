"""Privacy policy + terms in all 24 languages (SITE-STANDARD plan step 2).
Text lives in legal_text_*.py (English master in legal_text_en.py). Each page
reuses that language's glossary.html as the shell, so header menu, breadcrumbs,
footer, 18+ card and styles match the rest of the site. Then:
  python scripts/design/nav_menu.py   (same-page language switcher)
Also points every footer's privacy/terms links at the reader's own language
and adds the pages to sitemap.xml. Idempotent."""
import glob, html, importlib, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + os.sep
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://gameaccountvalue.com/'
LANGS = ['en', 'ru', 'es', 'pt', 'id', 'tr', 'ar', 'vi', 'hi', 'fr', 'de', 'it', 'ja', 'ko', 'th', 'pl', 'zh', 'tl', 'sw', 'ms', 'uz', 'kk', 'tk', 'ky']
TEXT = {}
for f in sorted(glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'legal_text_*.py'))):
    TEXT.update(importlib.import_module(os.path.basename(f)[:-3]).TEXT)

CSS = ('<style>.legal { max-width: 760px; margin: 0 auto; padding: 0 24px 48px; }'
       '.legal h2 { font-size: 21px; margin: 32px 0 10px; }'
       '.legal ul { padding-inline-start: 22px; } .legal li { margin: 6px 0; }'
       '.legal code { background: rgba(34,211,238,.1); border: 1px solid rgba(34,211,238,.3); border-radius: 6px; padding: 1px 6px; font-size: .92em; }'
       'main code { direction: ltr; unicode-bidi: isolate; display: inline-block; }'
       '.legal .legal-ref { color: var(--muted); font-size: 13px; margin-top: 36px; border-top: 1px solid var(--border); padding-top: 14px; }</style>')


def url(lang, slug):
    return SITE + ('' if lang == 'en' else lang + '/') + slug + '.html'


def strip(t):
    return html.unescape(re.sub(r'<[^>]+>', '', t))


def build(lang, slug):
    T, P = TEXT[lang], TEXT[lang][slug]
    shell = ROOT + ('glossary.html' if lang == 'en' else lang + '/glossary.html')
    s = open(shell, encoding='utf-8').read()
    me = url(lang, slug)
    title = f'{P["title"]} | GameAccountValue'
    esc = lambda v: html.escape(v, quote=True)
    s = re.sub(r'<title>.*?</title>', lambda m: f'<title>{esc(title)}</title>', s, count=1, flags=re.S)
    for pat, val in ((r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{esc(P["desc"])}">'),
                     (r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{esc(title)}">'),
                     (r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{esc(P["desc"])}">'),
                     (r'<meta property="og:type" content="[^"]*">', '<meta property="og:type" content="website">'),
                     (r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{me}">'),
                     (r'<meta name="twitter:title" content="[^"]*">', f'<meta name="twitter:title" content="{esc(title)}">'),
                     (r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{me}">')):
        s = re.sub(pat, lambda m, v=val: v, s, count=1)
    s = re.sub(r'<link rel="alternate" hreflang="[^"]+" href="[^"]+">\n?', '', s)
    alts = f'<link rel="alternate" hreflang="x-default" href="{url("en", slug)}">\n' + ''.join(
        f'<link rel="alternate" hreflang="{L}" href="{url(L, slug)}">\n' for L in LANGS if L in TEXT)
    s = s.replace(f'<link rel="canonical" href="{me}">', f'<link rel="canonical" href="{me}">\n' + alts.rstrip('\n'), 1)
    home_name = strip(re.search(r'<nav class="crumbs"[^>]*><ol><li><a href="\./">(.*?)</a>', s, re.S).group(1)).strip()
    ld = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'WebPage', '@id': me, 'url': me, 'name': P['title'], 'description': P['desc'], 'inLanguage': lang,
         'dateModified': '2026-09-30', 'isPartOf': {'@type': 'WebSite', 'name': 'GameAccountValue', 'url': SITE},
         'publisher': {'@type': 'Person', 'name': 'Aleksei Bitkin'}},
        {'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': home_name, 'item': SITE + ('' if lang == 'en' else lang + '/')},
            {'@type': 'ListItem', 'position': 2, 'name': P['title'], 'item': me}]}]}
    s = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', '', s, flags=re.S)
    s = s.replace('</head>', '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + '</script>\n' + CSS + '\n</head>', 1)
    s = re.sub(r'(<nav class="crumbs"[^>]*><ol>.*?<li aria-current="page">)[^<]*(</li>)', lambda m: m.group(1) + P['title'] + m.group(2), s, count=1, flags=re.S)
    body = ''.join(f'<h2>{h}</h2>\n{b}\n' for h, b in P['sec'])
    main = (f'<main>\n<section class="report-hero" id="main-content">\n  <h1>{P["h1"]}</h1>\n'
            f'  <p style="color:var(--muted); font-size:16px;">{P["lead"]}</p>\n  <p class="report-updated">{T["updated"]}</p>\n</section>\n'
            f'<div class="legal">\n{body}<p class="legal-ref">{T["ref"]}</p>\n</div>\n</main>')
    s = re.sub(r'<main>.*?</main>', lambda m: main, s, count=1, flags=re.S)
    s = s.replace('utm_campaign=glossary', f'utm_campaign={slug}')
    out = ROOT + ('' if lang == 'en' else lang + '/') + slug + '.html'
    open(out, 'w', encoding='utf-8', newline='').write(s)


def footers():
    n = 0
    for L in LANGS[1:]:
        if L not in TEXT:
            continue
        for f in glob.glob(ROOT + L + '/*.html'):
            s = open(f, encoding='utf-8').read()
            t = s.replace('href="../privacy.html"', 'href="./privacy.html"').replace('href="../terms.html"', 'href="./terms.html"')
            if t != s:
                open(f, 'w', encoding='utf-8', newline='').write(t)
                n += 1
    return n


def sitemap():
    p = ROOT + 'sitemap.xml'
    s = open(p, encoding='utf-8').read()
    add = ''
    for L in LANGS:
        for slug in ('privacy', 'terms'):
            u = url(L, slug)
            if L in TEXT and f'<loc>{u}</loc>' not in s:
                add += f'  <url><loc>{u}</loc><lastmod>2026-09-30</lastmod><changefreq>yearly</changefreq><priority>0.3</priority></url>\n'
    if add:
        s = s.replace('</urlset>', add + '</urlset>')
        open(p, 'w', encoding='utf-8', newline='\n').write(s)
    return add.count('<url>')


if __name__ == '__main__':
    only = sys.argv[1:] or [L for L in LANGS if L in TEXT]
    for L in only:
        for slug in ('privacy', 'terms'):
            build(L, slug)
    print('built', len(only) * 2, 'footers', footers(), 'sitemap +', sitemap())
