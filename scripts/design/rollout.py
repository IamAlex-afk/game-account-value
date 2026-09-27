"""Apply the Cyber-Glass redesign to every page, in place, idempotently.
Visible copy must stay identical except for the explicitly allowed changes
(checked per page with a word multiset diff)."""
import re, os, glob, collections, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..')).replace(os.sep, '/') + '/'   # the site
S = HERE.replace(os.sep, '/') + '/'                                                  # scripts/design (sources)
GAMES = ['roblox', 'brawl-stars', 'clash-of-clans', 'clash-royale', 'free-fire', 'genshin-impact', 'mobile-legends', 'fortnite', 'minecraft']
CITY = open(S + 'city.svg', encoding='utf-8').read()
BOT = open(S + 'bot.svg', encoding='utf-8').read()
import json
ICON = json.load(open(S + 'icons.json', encoding='utf-8'))   # neon line icons, generic shapes
ICON_CLS = {'roblox': 'g-roblox', 'brawl-stars': 'g-brawl', 'clash-of-clans': 'g-coc', 'clash-royale': 'g-cr', 'free-fire': 'g-ff',
            'genshin-impact': 'g-genshin', 'mobile-legends': 'g-ml', 'fortnite': 'g-fortnite', 'minecraft': 'g-mc'}

def build_css():
    faces = open(S + '_inter-faces.css', encoding='utf-8').read()
    title_fix = "html body .value-calc .vc-title { font-family: var(--body-font); font-variation-settings: normal; text-transform: none; letter-spacing: -.01em; }\n"
    parts = ['glass-body', None, 'glass-home', 'glass-tool', 'glass-luxe', 'glass-news', 'glass-events', 'glass-themes', 'glass-plain']
    css = ('/* GameAccountValue — Cyber-Glass design system (2026-09). Built from parts; see DESIGN.md.\n'
           '   Self-hosted Inter: the CSP only allows font-src \'self\'. */\n' + faces)
    for p in parts:
        css += title_fix if p is None else open(S + 'css/' + p + '.css', encoding='utf-8').read() + '\n'
    open(ROOT + 'assets/glass.css', 'w', encoding='utf-8', newline='\n').write(css)

def words(h):
    h = re.sub(r'<(script|style|svg)[^>]*>.*?</\1>', ' ', h, flags=re.S)
    h = re.sub(r'<[^>]+>', ' ', h)
    return collections.Counter(re.sub(r'\s+', ' ', h).split())

def div_end(s, i):
    """index just past the </div> closing the <div ...> that starts at i"""
    depth = 0
    for m in re.finditer(r'<div\b|</div>', s[i:]):
        depth += 1 if m.group(0) == '<div' else -1
        if depth == 0:
            return i + m.end()
    raise ValueError('unbalanced div')

class Page:
    def __init__(self, path):
        self.path = path
        self.s = open(path, encoding='utf-8').read()
        self.orig = self.s
        self.pre = '../' if os.path.dirname(os.path.relpath(path, ROOT)) else './'
        self.allow_missing = collections.Counter()
        self.allow_extra = collections.Counter()
    def rep(self, a, b, count=1):
        assert self.s.count(a) == count, (self.path, a[:80])
        self.s = self.s.replace(a, b)
    def cut_div(self, start):
        i = self.s.index(start); j = div_end(self.s, i)
        part = self.s[i:j]; self.s = self.s[:i] + self.s[j:]
        return part
    def cut(self, a, b):
        i = self.s.index(a); j = self.s.index(b, i) + len(b)
        part = self.s[i:j]; self.s = self.s[:i] + self.s[j:]
        return part
    def head(self, font='inter-latin.woff2'):
        link = ('<link rel="preload" href="' + self.pre + 'assets/fonts/' + font + '" as="font" type="font/woff2" crossorigin>\n'
                '<link rel="stylesheet" href="' + self.pre + 'assets/glass.css">\n')
        k = self.s.index('</head>')
        self.s = self.s[:k] + link + self.s[k:]
    def script_after_calc(self):
        tag = '<script src="' + self.pre + 'assets/calculators.js" defer></script>'
        if tag in self.s and 'assets/glass.js' not in self.s:
            self.rep(tag, tag + '\n<script src="' + self.pre + 'assets/glass.js" defer></script>')
    def wrap_sections(self):
        i = self.s.index('<div class="article-body">'); i += len('<div class="article-body">')
        j = div_end(self.s, self.s.index('<div class="article-body">')) - len('</div>')
        art = self.s[i:j]
        parts = re.split(r'(?=<span id="[^"]+" class="anchor-target"></span>)', art)
        out = parts[0] + ''.join('<section class="g-card g-news-card">' + p.rstrip() + '\n</section>\n' for p in parts[1:])
        self.s = self.s[:i] + out + self.s[j:]
    def check(self):
        A, B = words(self.orig), words(self.s)
        missing, extra = A - B, B - A
        ok = missing == self.allow_missing and extra == self.allow_extra
        if not ok:
            print('TEXT MISMATCH', self.path, 'missing', dict(missing - self.allow_missing), dict(self.allow_missing - missing),
                  'extra', dict(extra - self.allow_extra), dict(self.allow_extra - extra))
        return ok
    def save(self):
        open(self.path, 'w', encoding='utf-8', newline='').write(self.s)

def do_game(p, slug):
    if slug == 'roblox':
        p.rep('<body>', '<body class="theme-studs">')
    p.head()
    calc = p.cut_div('<div class="value-calc"')
    price = p.cut('<div class="price-range">', '</div>')
    facts = p.cut('<div class="fact-box">', '</div>')
    # badges row: "updated" line + freshness badge
    a = p.s.index('<p class="report-updated">')
    b = p.s.index('</p>', a) + 4
    if '<div class="fresh-badge">' in p.s[b:b + 40] or p.s.find('<div class="fresh-badge">', b) != -1 and p.s.find('<div class="fresh-badge">', b) < p.s.find('</section>', b):
        fb = p.s.index('<div class="fresh-badge">', b); b = p.s.index('</div>', fb) + 6
    p.s = p.s[:a] + '<div class="g-badges">\n  ' + p.s[a:b] + '\n  </div>' + p.s[b:]
    hero = p.cut('<section class="report-hero" id="main-content">', '</section>')
    rc = p.s.index('<div class="report-cta">') + len('<div class="report-cta">')
    cta = p.s[rc:p.s.index('</div>', rc)]
    p.allow_extra += words(cta)
    m = re.search(r'<main>\s*', p.s)
    block = ('<div class="g-hero">\n<div class="g-left">\n' + hero + '\n' + price + '\n' + facts + '\n</div>\n<div class="g-right">\n' + calc +
             '\n<div class="g-exact" data-g-slot="result">' + cta + '</div>\n</div>\n</div>\n')
    p.s = p.s[:m.end()] + block + p.s[m.end():]
    p.wrap_sections()
    p.script_after_calc()

def do_news(p):
    p.head()
    p.wrap_sections()
    if 'class="ev-list"' in p.s and 'assets/events.js' not in p.s:
        k = p.s.rindex('</body>')
        p.s = p.s[:k] + '<script src="' + p.pre + 'assets/events.js" defer></script>\n' + p.s[k:]

def game_icons(p):
    for slug, cls in ICON_CLS.items():
        pat = re.compile(r'<a class="game-card" href="' + re.escape(slug) + r'\.html"([^>]*)><div class="game-icon" aria-hidden="true">([^<]*)</div>')
        m = pat.search(p.s)
        if not m:
            continue
        p.allow_missing += words(m.group(2))
        p.s = pat.sub(lambda m: '<a class="game-card ' + cls + '" href="' + slug + '.html"' + m.group(1) +
                      '><div class="game-icon" aria-hidden="true"><svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.5">' +
                      ICON[slug] + '</svg></div>', p.s, count=1)

def grab(h, a, b):
    i = h.index(a); j = h.index(b, i) + len(b)
    return h[i:j]

def do_home(p):
    p.head()
    game_icons(p)
    hero_start = '<section class="hero" id="main-content">'
    if 'class="value-calc"' in p.s:
        # tool-first homepage
        c0 = p.s.index('<!-- LIVE CALCULATOR -->'); c1 = p.s.index('</section>', c0) + len('</section>')
        calc_sec = p.s[c0:c1]; p.s = p.s[:c0] + p.s[c1:]
        h2 = grab(calc_sec, '<h2', '</h2>')
        sub = grab(calc_sec, '<p class="section-sub">', '</p>')
        ci = calc_sec.index('<div class="value-calc"'); calc = calc_sec[ci:div_end(calc_sec, ci)]
        calc = re.sub(r' style="max-width: ?480px; ?margin: ?0 auto;?"', '', calc)
        pick_label = re.search(r'class="vc-switcher" aria-label="([^"]*)"', calc).group(1)
        hero = p.cut(hero_start, '</section>')
        badge = grab(hero, '<div class="hero-badge">', '</div>')
        h1 = grab(hero, '<h1>', '</h1>').replace('<br>', ' ')
        para = re.search(r'<p>.*?</p>', hero, re.S).group(0)
        cta_group = hero[hero.index('<div class="cta-group">'):div_end(hero, hero.index('<div class="cta-group">'))]
        anchors = re.findall(r'<a\b[^>]*>.*?</a>', cta_group, re.S)
        bot_btn = next(a for a in anchors if 'href="https://t.me/' in a)
        bot_btn = re.sub(r'class="btn-(primary|secondary)"', 'class="btn-secondary"', bot_btn)   # styled as the result-card CTA
        others = [a for a in anchors if a is not bot_btn and 'href="https://t.me/' not in a]
        keep = [a for a in others if 'href="#vc-home"' not in a]
        for a in others:
            if 'href="#vc-home"' in a:
                p.allow_missing += words(a)      # duplicate of the tool that is now the first screen
                p.allow_extra += collections.Counter({'1': 1})   # aria-hidden step number
        if not any('href="#vc-home"' in a for a in others):
            p.allow_extra += collections.Counter({'1': 1})
        extra_links = ('<div class="cta-group g-about-cta">' + ''.join(keep) + '</div>') if keep else ''
        notice = grab(hero, '<p class="ai-notice">', '</p>')
        tool = ('<section class="g-tool" id="main-content">\n'
                '  <div class="g-fx" aria-hidden="true">' + CITY + '<div class="g-rain"></div></div>\n'
                '  <div class="g-head"><div>' + badge + '\n' + h1 + '</div><div class="g-robot" aria-hidden="true">' + BOT + '</div></div>\n'
                '  <div class="g-panel">\n    <div class="g-intro">' + h2 + sub + '</div>\n'
                '    <div class="g-pick-wrap"><span class="g-num" aria-hidden="true">1</span><div class="g-pick" role="group" aria-label="' + pick_label + '"></div></div>\n'
                '    ' + calc + '\n  </div>\n'
                '  <div class="g-exact" data-g-slot="result">' + bot_btn + notice + '</div>\n</section>\n'
                '<section class="g-about">' + para + extra_links + '</section>\n')
        m = re.search(r'<main>\s*', p.s)
        p.s = p.s[:m.end()] + tool + p.s[m.end():]
        p.script_after_calc()
    else:
        hero = p.cut(hero_start, '</section>')
        inner = hero[len(hero_start):-len('</section>')].strip()
        new = ('<section class="g-hero g-home g-home-plain" id="main-content">\n'
               '  <div class="g-fx" aria-hidden="true">' + CITY + '<div class="g-rain"></div></div>\n'
               '  <div class="g-left">\n' + inner + '\n  </div>\n'
               '  <div class="g-robot" aria-hidden="true">' + BOT + '</div>\n</section>')
        m = re.search(r'<main>\s*', p.s)
        p.s = p.s[:m.end()] + new + '\n' + p.s[m.end():]

def do_resource(p):
    p.head()

def main(only=None):
    build_css()
    files = sorted(glob.glob(ROOT + '*.html') + glob.glob(ROOT + '*/*.html'))
    stats = collections.Counter(); bad = []
    for f in files:
        rel = os.path.relpath(f, ROOT).replace('\\', '/')
        name = os.path.basename(f)
        if rel.startswith(('_proto/', '_tmp', 'proto-')) or name.startswith(('googl', 'proto-', '_')) or '/_' in rel:
            continue
        if only and not re.search(only, rel):
            continue
        p = Page(f)
        if 'assets/glass.css' in p.s:
            stats['already'] += 1; continue
        slug = name[:-5]
        try:
            if name == 'index.html':
                do_home(p); kind = 'home'
            elif slug in GAMES:
                do_game(p, slug); kind = 'game'
            elif slug.endswith('-news'):
                do_news(p); kind = 'news'
            else:
                do_resource(p); kind = 'resource'
        except Exception as e:
            bad.append((rel, repr(e))); continue
        if p.check():
            p.save(); stats[kind] += 1
        else:
            bad.append((rel, 'text check'))
    print(dict(stats))
    for b in bad:
        print('FAILED', b)

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else None)
