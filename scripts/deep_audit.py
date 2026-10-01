"""Deep page-by-page audit (owner request 2026-10-01: 'inspect every file, what did we miss').
Reports counts + examples; not a gate. Complements site_check.py / audit_site.py."""
import collections, glob, html, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + os.sep
R = collections.defaultdict(list)
DEPRECATED_LD = {'HowTo', 'SpecialAnnouncement', 'ClaimReview', 'CourseInfo', 'EstimatedSalary', 'LearningVideo', 'VehicleListing', 'Book'}
SELF_REF = re.compile(r'Researched live by AI|HTTP 403|bot-protection|returned 403|timed out|we couldn.t get one honestly|data gap', re.I)
STALE = re.compile(r'Ultra Legendary|Ультралегендар|Starr Road|Starter Pass', re.I)


def pages():
    for f in glob.glob(ROOT + '**/*.html', recursive=True):
        rel = os.path.relpath(f, ROOT).replace(os.sep, '/')
        if not rel.startswith(('scripts/', '_', 'node_modules/', 'google')):
            yield rel


titles = collections.defaultdict(list)
for rel in sorted(pages()):
    s = open(ROOT + rel, encoding='utf-8').read()
    lang = rel.split('/')[0] if rel.count('/') == 1 else 'en'
    noindex = 'noindex' in (re.search(r'<meta name="robots" content="([^"]*)"', s) or [''])[0]
    t = re.search(r'<title>(.*?)</title>', s, re.S)
    t = html.unescape(t.group(1).strip()) if t else ''
    if not noindex:
        titles[(lang, t)].append(rel)
    if len(t) > 70: R['title > 70 chars'].append(f'{rel} ({len(t)})')
    d = re.search(r'<meta name="description" content="([^"]*)"', s)
    d = html.unescape(d.group(1)) if d else ''
    if len(d) > 170: R['description > 170 chars'].append(f'{rel} ({len(d)})')
    if len(d) < 70: R['description < 70 chars'].append(f'{rel} ({len(d)})')
    h1 = re.findall(r'<h1[\s>]', s)
    if len(h1) != 1: R['h1 count != 1'].append(f'{rel} ({len(h1)})')
    for img in re.findall(r'<img\b[^>]*>', s):
        if 'alt=' not in img: R['img without alt'].append(rel + ' ' + img[:80])
        if 'width=' not in img or 'height=' not in img: R['img without width/height (CLS)'].append(rel + ' ' + img[:80])
    for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try:
            j = json.loads(b)
        except ValueError:
            continue
        types = re.findall(r'"@type":\s*"([^"]+)"', json.dumps(j))
        for ty in types:
            if ty in DEPRECATED_LD: R['deprecated/limited LD type ' + ty].append(rel)
            if ty in ('FAQPage',): R['FAQPage (rich result only gov/health sites)'].append(rel)
            if ty in ('AggregateRating', 'Review'): R['self-serving rating/review LD'].append(rel)
        for k in ('datePublished', 'dateModified'):
            for v in re.findall(rf'"{k}":\s*"([^"]+)"', json.dumps(j)):
                if v[:10] > '2026-10-01': R['date in the future: ' + k].append(f'{rel} {v}')
    body = s[s.find('<body'):]
    vis = re.sub(r'<script.*?</script>|<style.*?</style>', '', body, flags=re.S)
    if SELF_REF.search(vis):
        R['self-referential / process wording'].append(rel + ' :: ' + SELF_REF.search(vis).group(0))
    if STALE.search(vis) and 'news-' not in rel:
        R['possibly outdated term (renamed/retired in Sept 2026)'].append(rel + ' :: ' + STALE.search(vis).group(0))
    for a in re.findall(r'<a\b[^>]*href="https?://(?!gameaccountvalue\.com|t\.me)[^"]+"[^>]*>', s):
        if 'target="_blank"' in a and 'noopener' not in a: R['target=_blank without noopener'].append(rel)
    if 'lang="' not in s[:300]: R['no html lang'].append(rel)
    og = re.search(r'<meta property="og:image" content="([^"?]+)', s)
    if og and og.group(1).startswith('https://gameaccountvalue.com/'):
        if not os.path.exists(ROOT + og.group(1)[len('https://gameaccountvalue.com/'):]): R['og:image file missing'].append(rel)
    elif not og and rel != '404.html': R['no og:image'].append(rel)

for (lang, t), ps in titles.items():
    if len(ps) > 1: R['duplicate title within a language'].append(f'{lang} "{t[:60]}" x{len(ps)}: {ps[:3]}')

for k in sorted(R, key=lambda k: -len(R[k])):
    print(f'## {k}: {len(R[k])}')
    for x in R[k][:6]:
        print('   ', x)
print('done')
