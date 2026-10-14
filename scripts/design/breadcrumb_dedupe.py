"""One BreadcrumbList per page (2026-10-14).

72 game pages (9 games x en, kk, ky, ms, sw, tk, tl, uz) carried the breadcrumb twice:
inside the page's @graph and again as a separate <script type="application/ld+json">.
Both had the same names; the @graph one also has a URL for the last step (= canonical),
so the separate block is removed. Checked before removing: names equal, last item ==
canonical. Idempotent. site_check.py now reports a second BreadcrumbList as an error.
Run: python scripts/design/breadcrumb_dedupe.py"""
import glob, json, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
BLOCK = re.compile(r'<script type="application/ld\+json">(.*?)</script>\n?', re.S)
n = 0
for f in glob.glob(os.path.join(ROOT, '**', '*.html'), recursive=True):
    rel = os.path.relpath(f, ROOT).replace(os.sep, '/')
    if rel.startswith(('scripts/', '_')):
        continue
    s = open(f, encoding='utf-8').read()
    if s.count('"BreadcrumbList"') < 2:
        continue
    graph = standalone = None
    for m in BLOCK.finditer(s):
        d = json.loads(m.group(1))
        if isinstance(d, dict) and d.get('@type') == 'BreadcrumbList':
            standalone = (m, d)
        elif isinstance(d, dict):
            graph = next((x for x in d.get('@graph', []) if x.get('@type') == 'BreadcrumbList'), graph)
    if not (graph and standalone):
        sys.exit(f'{rel}: unexpected breadcrumb layout, not touched')
    names = lambda bl: [i.get('name') for i in bl['itemListElement']]
    canon = re.search(r'<link rel="canonical" href="([^"]+)"', s).group(1)
    if names(graph) != names(standalone[1]) or graph['itemListElement'][-1].get('item') != canon:
        sys.exit(f'{rel}: breadcrumbs differ, not touched')
    m = standalone[0]
    s = s[:m.start()] + s[m.end():]
    open(f, 'w', encoding='utf-8', newline='').write(s)
    n += 1
print('duplicate BreadcrumbList removed on', n, 'pages')
