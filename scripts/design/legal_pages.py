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
for f in sorted(glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), '*_text_*.py'))):
    for _L, _v in importlib.import_module(os.path.basename(f)[:-3]).TEXT.items():
        TEXT.setdefault(_L, {}).update(_v)
# opt-in /top leaderboard paragraph, appended to the privacy section about the public card page
from legal_top import TOP as _TOP
for _L, _t in _TOP.items():
    if _L in TEXT and 'privacy' in TEXT[_L]:
        _sec = TEXT[_L]['privacy']['sec']
        _h, _b = _sec[5]
        if '/top' not in _b:
            _sec[5] = (_h, _b + _t)
# Cloudflare + browser-storage paragraph, appended to the privacy section 'This website'
from legal_site import SITE as _SITE
for _L, _t in _SITE.items():
    if _L in TEXT and 'privacy' in TEXT[_L]:
        _sec = TEXT[_L]['privacy']['sec']
        _h, _b = _sec[1]
        if 'Cloudflare' not in _b:
            _sec[1] = (_h, _b + _t)
SLUGS = ('privacy', 'terms', 'about')
PERSON = {'@type': 'Person', 'name': 'Aleksei Bitkin', 'url': 'https://github.com/IamAlex-afk',
          'sameAs': ['https://orcid.org/0009-0002-7986-3812', 'https://github.com/IamAlex-afk',
                     'https://iamalex-afk.github.io/human-os-patch-33-protocols/']}

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
        f'<link rel="alternate" hreflang="{L}" href="{url(L, slug)}">\n' for L in LANGS if slug in TEXT.get(L, {}))
    s = s.replace(f'<link rel="canonical" href="{me}">', f'<link rel="canonical" href="{me}">\n' + alts.rstrip('\n'), 1)
    home_name = strip(re.search(r'<nav class="crumbs"[^>]*><ol><li><a href="\./">(.*?)</a>', s, re.S).group(1)).strip()
    ld = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'AboutPage' if slug == 'about' else 'WebPage', '@id': me, 'url': me, 'name': P['title'], 'description': P['desc'], 'inLanguage': lang,
         'dateModified': '2026-10-01' if slug == 'about' else '2026-09-30', 'isPartOf': {'@type': 'WebSite', 'name': 'GameAccountValue', 'url': SITE},
         'publisher': PERSON, **({'mainEntity': PERSON} if slug == 'about' else {})},
        {'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': home_name, 'item': SITE + ('' if lang == 'en' else lang + '/')},
            {'@type': 'ListItem', 'position': 2, 'name': P['title'], 'item': me}]}]}
    s = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', '', s, flags=re.S)
    s = s.replace('</head>', '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + '</script>\n' + CSS + '\n</head>', 1)
    s = re.sub(r'(<nav class="crumbs"[^>]*><ol>.*?<li aria-current="page">)[^<]*(</li>)', lambda m: m.group(1) + P['title'] + m.group(2), s, count=1, flags=re.S)
    body = ''.join(f'<h2>{h}</h2>\n{b}\n' for h, b in P['sec'])
    main = (f'<main>\n<section class="report-hero" id="main-content">\n  <h1>{P["h1"]}</h1>\n'
            f'  <p style="color:var(--muted); font-size:16px;">{P["lead"]}</p>\n'
            + (f'  <p class="report-updated">{T["updated"]}</p>\n' if slug != 'about' else '') + '</section>\n'
            f'<div class="legal">\n{body}' + (f'<p class="legal-ref">{T["ref"]}</p>\n' if slug != 'about' else '') + '</div>\n</main>')
    s = re.sub(r'<main>.*?</main>', lambda m: main, s, count=1, flags=re.S)
    s = s.replace('utm_campaign=glossary', f'utm_campaign={slug}')
    out = ROOT + ('' if lang == 'en' else lang + '/') + slug + '.html'
    open(out, 'w', encoding='utf-8', newline='').write(s)


ABOUT = {'en': 'About', 'ru': 'О проекте', 'es': 'Sobre el proyecto', 'pt': 'Sobre o projeto', 'id': 'Tentang', 'tr': 'Hakkında',
         'ar': 'من نحن', 'vi': 'Giới thiệu', 'hi': 'हमारे बारे में', 'fr': 'À propos', 'de': 'Über uns', 'it': 'Chi siamo',
         'ja': '運営者情報', 'ko': '소개', 'zh': '关于我们', 'th': 'เกี่ยวกับเรา', 'pl': 'O projekcie', 'tl': 'Tungkol sa amin',
         'sw': 'Kutuhusu', 'ms': 'Tentang kami', 'uz': 'Loyiha haqida', 'kk': 'Жоба туралы', 'tk': 'Taslama barada', 'ky': 'Долбоор жөнүндө'}


def footers():
    """Footer legal links -> the reader's own language; add the About link."""
    n = 0
    for f in glob.glob(ROOT + '**/*.html', recursive=True):
        rel = os.path.relpath(f, ROOT).replace(os.sep, '/')
        if rel.startswith(('scripts/', '_', 'node_modules/', 'google')):
            continue
        L = rel.split('/')[0] if rel.count('/') == 1 else 'en'
        if L not in TEXT:
            continue
        s = t = open(f, encoding='utf-8').read()
        if L != 'en':
            t = t.replace('href="../privacy.html"', 'href="./privacy.html"').replace('href="../terms.html"', 'href="./terms.html"')
        if 'about' in TEXT[L] and 'about.html">' not in t:
            t = re.sub(r'(<footer[^>]*>.*?)(<a href="(?:\./)?privacy\.html")', lambda m: m.group(1) + f'<a href="./about.html">{ABOUT[L]}</a>\n    ' + m.group(2), t, count=1, flags=re.S)
        if t != s:
            open(f, 'w', encoding='utf-8', newline='').write(t)
            n += 1
    return n


def sitemap():
    p = ROOT + 'sitemap.xml'
    s = open(p, encoding='utf-8').read()
    add = ''
    for L in LANGS:
        for slug in SLUGS:
            u = url(L, slug)
            if slug in TEXT.get(L, {}) and f'<loc>{u}</loc>' not in s:
                add += f'  <url><loc>{u}</loc><lastmod>2026-09-30</lastmod><changefreq>yearly</changefreq><priority>0.3</priority></url>\n'
    if add:
        s = s.replace('</urlset>', add + '</urlset>')
        open(p, 'w', encoding='utf-8', newline='\n').write(s)
    return add.count('<url>')


if __name__ == '__main__':
    only = sys.argv[1:] or [L for L in LANGS if L in TEXT]
    n = 0
    for L in only:
        for slug in SLUGS:
            if slug in TEXT[L]:
                build(L, slug)
                n += 1
    print('built', n, 'footers', footers(), 'sitemap +', sitemap())
