"""Site-wide technical audit: indexability, canonical, hreflang, internal
links/assets, JSON-LD, <html lang> vs folder, title/description, sitemap
coverage. Run from the repo root: python scripts/audit_site.py"""
import glob, os, re, json, collections
from urllib.parse import urlparse, unquote

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
BASE = 'https://gameaccountvalue.com/'
os.chdir(ROOT)
pages = sorted(p.replace('\\', '/') for p in glob.glob('*.html') + glob.glob('*/*.html')
               if not os.path.basename(p).startswith(('googl', 'proto', '_')))
issues = collections.defaultdict(list)
sitemap = open('sitemap.xml', encoding='utf-8').read()
sm_urls = set(re.findall(r'<loc>(.*?)</loc>', sitemap))

def url_of(p):
    return BASE + (p[:-10] if p.endswith('index.html') else p)

def local_target(page, href):
    if href.startswith(('http://', 'https://')):
        if not href.startswith(BASE):
            return None
        path = href[len(BASE):]
    elif href.startswith(('mailto:', 'tel:', 'javascript:', '#', 'data:')):
        return None
    elif href.startswith('/'):
        path = href[1:]
    else:
        path = os.path.normpath(os.path.join(os.path.dirname(page), href)).replace('\\', '/')
    path = unquote(path.split('#')[0].split('?')[0])
    if path in ('', '.'):
        path = 'index.html'
    if path.endswith('/'):
        path += 'index.html'
    return path

for p in pages:
    s = open(p, encoding='utf-8').read()
    folder = p.split('/')[0] if '/' in p else 'en'
    lang = re.search(r'<html[^>]*\blang="([^"]+)"', s)
    if not lang: issues['no html lang'].append(p)
    elif folder != 'en' and not lang.group(1).lower().startswith(folder): issues['lang != folder'].append(p + ' ' + lang.group(1))
    if re.search(r'<meta[^>]+name="robots"[^>]+noindex', s, re.I): issues['NOINDEX'].append(p)
    if not re.search(r'<title>[^<]{5,}</title>', s): issues['no/short title'].append(p)
    if not re.search(r'<meta name="description" content="[^"]{30,}"', s): issues['no/short meta description'].append(p)
    can = re.search(r'<link rel="canonical" href="([^"]+)"', s)
    if p != '404.html':
        if not can: issues['no canonical'].append(p)
        elif can.group(1) != url_of(p): issues['canonical != own URL'].append(p + ' -> ' + can.group(1))
        if url_of(p) not in sm_urls and p not in ('404.html',): issues['not in sitemap'].append(p)
    for h in re.findall(r'<link rel="alternate" hreflang="[^"]+" href="([^"]+)"', s):
        t = local_target(p, h)
        if t and not os.path.exists(t): issues['hreflang -> missing page'].append(p + ' -> ' + h)
    for m in re.finditer(r'<(?:a|link|script|img|source)\b[^>]*\b(?:href|src)="([^"]+)"', s):
        h = m.group(1)
        if 'hreflang' in m.group(0) or 'rel="canonical"' in m.group(0) or 'preconnect' in m.group(0): continue
        t = local_target(p, h)
        if t and not os.path.exists(t): issues['broken internal link/asset'].append(p + ' -> ' + h)
    for j in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try: json.loads(j)
        except Exception as e: issues['bad JSON-LD'].append(p + ' ' + str(e)[:60])
    ids = re.findall(r'\bid="([^"]+)"', s)
    d = [i for i, c in collections.Counter(ids).items() if c > 1]
    if d: issues['duplicate id'].append(p + ' ' + ','.join(d[:5]))
    if s.count('<h1') != 1: issues['h1 count != 1'].append(p + ' (' + str(s.count('<h1')) + ')')

for u in sm_urls:
    path = local_target('index.html', u)
    if path and not os.path.exists(path): issues['sitemap URL -> missing file'].append(u)

print('pages audited:', len(pages), '| sitemap URLs:', len(sm_urls))
if not issues: print('NO ISSUES')
for k, v in sorted(issues.items()):
    print('\n##', k, '(' + str(len(v)) + ')')
    for x in v[:12]: print('  ', x)
    if len(v) > 12: print('   ...')
