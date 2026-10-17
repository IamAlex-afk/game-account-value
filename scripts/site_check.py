"""One-command site check (SITE-STANDARD.md "definition of done").
  python scripts/site_check.py            -> summary; exit 1 on ERRORS
ERRORS: broken internal links/assets, invalid JSON-LD, canonical not self, hreflang pointing to a
missing page, a page missing a required block. TODO (not errors): pages English has but a language
lacks yet (the translation backlog), English-leftover suspects in translated pages."""
import glob, html, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + os.sep
SITE = 'https://gameaccountvalue.com/'
LANGS = ['en', 'ru', 'es', 'pt', 'id', 'tr', 'ar', 'vi', 'hi', 'fr', 'de', 'it', 'ja', 'ko', 'th', 'pl', 'zh', 'tl', 'sw', 'ms', 'uz', 'kk', 'tk', 'ky']
EN_WORDS = re.compile(r'\b(the|and|with|your|which|this|that|from|have|account is|you can|we do)\b', re.I)


GAMES = ['roblox', 'brawl-stars', 'clash-of-clans', 'clash-royale', 'free-fire', 'genshin-impact',
         'pubg-mobile', 'mobile-legends', 'fortnite', 'minecraft']


def pages():
    out = []
    for f in glob.glob(ROOT + '**/*.html', recursive=True):
        rel = os.path.relpath(f, ROOT).replace(os.sep, '/')
        if rel.startswith(('scripts/', '_', 'node_modules/', 'google')):
            continue
        # merged news articles are now instant-refresh redirect stubs to their game hub
        if 'http-equiv="refresh"' in open(f, encoding='utf-8').read(2000):
            continue
        out.append(rel)
    return sorted(out)


def lang_of(rel):
    p = rel.split('/')
    return p[0] if len(p) == 2 and p[0] in LANGS else 'en'


def squash(t):
    return re.sub(r'\W+', '', html.unescape(re.sub(r'<[^>]+>', '', t)).lower())


def questions(o):
    if isinstance(o, dict):
        if o.get('@type') == 'Question':
            yield o
        o = list(o.values())
    if isinstance(o, list):
        for v in o:
            yield from questions(v)


def main():
    files = pages()
    exist = set(files)
    errors, todo, leftovers = [], [], []
    en_set = {f for f in files if lang_of(f) == 'en'}
    for L in LANGS[1:]:
        have = {f.split('/', 1)[1] for f in files if f.startswith(L + '/')}
        missing = sorted(p for p in en_set if p not in have and p != '404.html')
        if missing:
            todo.append((L, missing))
    for rel in files:
        s = open(ROOT + rel, encoding='utf-8').read()
        d = os.path.dirname(rel)
        noindex = 'noindex' in (re.search(r'<meta name="robots" content="([^"]+)"', s) or [''])[0]
        # links / assets
        for h in re.findall(r'(?:href|src)="((?:\./|\.\./)[^"#?]*|assets/[^"#?]*)"', s):
            if rel == '404.html':
                continue
            p = os.path.normpath(os.path.join(d, h)).replace(os.sep, '/')
            if h.endswith('/') or p in ('.', ''):
                p = (p + '/index.html').lstrip('./') if p not in ('.', '') else 'index.html'
            if not os.path.exists(ROOT + p):
                errors.append(f'{rel}: broken link {h}')
        for h in re.findall(r'(?:href|src)="(/(?!/)[^"#?]*)"', s):
            p = h.lstrip('/')
            p = p + 'index.html' if (p == '' or p.endswith('/')) else p
            if not os.path.exists(ROOT + p):
                errors.append(f'{rel}: broken link {h}')
        # JSON-LD
        visible = None
        for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
            try:
                ld = json.loads(b)
            except ValueError as e:
                errors.append(f'{rel}: invalid JSON-LD ({e})')
                continue
            # FAQ markup must repeat questions the reader can see on the page (Google's FAQPage guideline)
            for q in questions(ld):
                if visible is None:
                    visible = squash(re.sub(r'<script.*?</script>|<style.*?</style>', '', s[s.find('<body'):], flags=re.S))
                if squash(q.get('name', '')) not in visible:
                    errors.append(f'{rel}: FAQ markup question not visible on the page: {q.get("name", "")[:70]}')
        # one breadcrumb trail per page (2026-10-14: 72 pages had it twice)
        if s.count('"BreadcrumbList"') > 1:
            errors.append(f'{rel}: BreadcrumbList appears {s.count(chr(34) + "BreadcrumbList" + chr(34))} times (keep one)')
        # JSON-LD is not HTML: an entity like &amp; is read literally by search engines (2026-10-14)
        for blk in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
            ent = re.search(r'&(?:amp|quot|lt|gt|nbsp|apos|#\d+|#x[0-9a-f]+);', blk, re.I)
            if ent:
                errors.append(f'{rel}: HTML entity {ent.group(0)} inside JSON-LD (write the character itself)')
                break
        # in-page anchors
        ids = set(re.findall(r'\bid="([^"]+)"', s))
        for h in re.findall(r'<a\b[^>]*\bhref="#([^"]+)"', s):
            if h not in ids:
                errors.append(f'{rel}: anchor #{h} has no target on the page')
        # canonical
        if not noindex and rel != '404.html':
            c = re.search(r'<link rel="canonical" href="([^"]+)"', s)
            want = SITE + (rel[:-10] if rel.endswith('index.html') else rel)
            if not c or c.group(1) != want:
                errors.append(f'{rel}: canonical {c.group(1) if c else "missing"} != {want}')
        # hreflang targets exist
        for href in re.findall(r'<link rel="alternate" hreflang="[^"]+" href="([^"]+)"', s):
            if href.startswith(SITE):
                p = href[len(SITE):]
                p = p + 'index.html' if (p == '' or p.endswith('/')) else p
                if p not in exist:
                    errors.append(f'{rel}: hreflang to missing {href}')
        # required blocks
        if not re.search(r'<nav(?: aria-label="[^"]*")?>', s) or 'nav-menu' not in s:
            errors.append(f'{rel}: no site menu')
        base = os.path.basename(rel)
        if '<footer>' in s and 'class="g-18"' not in s:
            errors.append(f'{rel}: footer without 18+ card')
        if base != 'index.html' and rel not in ('404.html', 'privacy.html', 'terms.html') and 'class="crumbs"' not in s and 'news' not in base:
            errors.append(f'{rel}: no breadcrumbs')
        if 'data-g-slot="result"' in s and 'gc-teaser' not in s:
            errors.append(f'{rel}: calculator without card teaser')
        # homepage "N games" counter must match the game pages that exist in that language (2026-10-17: it said 9 of 10)
        if base == 'index.html':
            pre = '' if lang_of(rel) == 'en' else lang_of(rel) + '/'
            n_games = sum(1 for g in GAMES if pre + g + '.html' in exist)
            m = re.search(r'<div class="stat-num">(\d+)</div>', s)
            if m and int(m.group(1)) != n_games:
                errors.append(f'{rel}: games counter says {m.group(1)}, the language has {n_games} game pages')
        # English leftovers in translated pages
        if lang_of(rel) != 'en':
            main_part = s[s.find('<main'):s.find('</main>')] if '<main' in s else s
            txt = html.unescape(re.sub(r'<[^>]+>', '\n', re.sub(r'<script.*?</script>|<style.*?</style>|<svg.*?</svg>', '', main_part, flags=re.S)))
            bad = [l.strip() for l in txt.split('\n') if len(l.strip()) > 40 and len(EN_WORDS.findall(l)) >= 3]
            if bad:
                leftovers.append((rel, bad[:2]))
    # mass-publishing guard: Google's scaled-content policy; a big jump in indexable URLs needs a deliberate decision
    try:
        import subprocess
        old = subprocess.run(['git', '-C', ROOT, 'show', 'HEAD:sitemap.xml'], capture_output=True, text=True, encoding='utf-8').stdout
        new = open(ROOT + 'sitemap.xml', encoding='utf-8').read()
        grow = new.count('<loc>') - old.count('<loc>')
        if old and grow > 20 and os.environ.get('GAV_ALLOW_MASS') != '1':
            errors.append(f'sitemap.xml: +{grow} indexable URLs in one change. Publish in small batches, or set GAV_ALLOW_MASS=1 after a deliberate decision')
    except OSError:
        pass
    print(f'pages: {len(files)}  languages: {len(LANGS)}')
    print(f'ERRORS: {len(errors)}')
    for e in errors[:60]:
        print('  ' + e)
    print(f'TODO translations: {sum(len(m) for _, m in todo)} pages missing across {len(todo)} languages')
    if todo:
        sample = todo[0][1]
        print(f'  every language lacks the same {len(sample)} pages, e.g. {todo[0][0]}: {", ".join(sample[:12])}'
              if all(m == sample for _, m in todo) else '\n'.join(f'  {L}: {len(m)} missing' for L, m in todo))
    print(f'English-leftover suspects: {len(leftovers)} pages')
    for rel, b in leftovers[:10]:
        print(f'  {rel}: {b[0][:110]}')
    sys.exit(1 if errors else 0)


if __name__ == '__main__':
    main()
