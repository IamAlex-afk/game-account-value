"""Pre-render the calculator's UI shell so nothing shifts when JS mounts."""
import re, glob, os, collections, sys
sys.path.insert(0, os.path.dirname(__file__))
import importlib.util
spec = importlib.util.spec_from_file_location('r', os.path.join(os.path.dirname(__file__), 'rollout.py'))
R = importlib.util.module_from_spec(spec); spec.loader.exec_module(R)

NAMES = [("roblox", "Roblox"), ("brawl-stars", "Brawl Stars"), ("clash-of-clans", "Clash of Clans"), ("clash-royale", "Clash Royale"),
         ("free-fire", "Free Fire"), ("genshin-impact", "Genshin Impact"), ("mobile-legends", "Mobile Legends"), ("fortnite", "Fortnite"), ("minecraft", "Minecraft")]

def tiles():
    return ''.join('<button type="button" class="g-pick-btn g-' + g + '" data-g="' + g + '" aria-pressed="' + ('true' if g == 'roblox' else 'false') +
                   '"><svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true">' + R.ICON[g] + '</svg><span>' + n + '</span></button>'
                   for g, n in NAMES)

os.chdir(R.ROOT)
stats = collections.Counter()
for f in sorted(glob.glob('*.html') + glob.glob('*/*.html')):
    if f.startswith(('_', 'proto')) or 'proto' in f:
        continue
    s = open(f, encoding='utf-8').read()
    if 'assets/glass.css' not in s or 'class="value-calc"' not in s or 'data-stable="1"' in s:
        continue
    orig = s
    allow_extra = collections.Counter()
    # 1) game tiles
    if '<div class="g-pick" role="group"' in s:
        s = re.sub(r'(<div class="g-pick" role="group" aria-label="[^"]*">)(</div>)', lambda m: m.group(1) + tiles() + m.group(2), s, count=1)
        allow_extra += R.words(tiles())
    # 2) result shell: lo/hi spans + scale + meta
    s = re.sub(r'<strong class="vc-result-value">—</strong>',
               '<strong class="vc-result-value"><span class="vc-lo">—</span> – <span class="vc-hi">—</span></strong>'
               '<div class="vc-scale" aria-hidden="true"><div class="vc-scale-fill"></div></div>'
               '<div class="vc-meta"><span class="vc-tier"></span><span class="vc-confidence"></span></div>', s, count=1)
    allow_extra += collections.Counter({'–': 1, '—': 1})
    # 3) action row around the share button
    s = re.sub(r'(<button type="button" class="vc-share-btn">.*?</button>)', r'<div class="g-actions">\1</div>', s, count=1, flags=re.S)
    # 4) bot CTA inside the result card (was moved there by JS after load)
    m = re.search(r'\n?<div class="g-exact" data-g-slot="result">.*?</div>\n?', s, re.S)
    if m:
        exact = m.group(0).strip()
        s = s[:m.start()] + '\n' + s[m.end():]
        k = s.index('<div class="g-actions">'); k = s.index('</div>', k) + len('</div>')
        s = s[:k] + exact + s[k:]
    s = s.replace('class="value-calc"', 'class="value-calc" data-stable="1"', 1)
    A, B = R.words(orig), R.words(s)
    if A - B or (B - A) != allow_extra:
        print('TEXT MISMATCH', f, dict(A - B), dict((B - A) - allow_extra), dict(allow_extra - (B - A)))
        continue
    open(f, 'w', encoding='utf-8', newline='').write(s)
    stats['ok'] += 1
print(dict(stats))
