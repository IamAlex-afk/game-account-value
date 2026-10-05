"""Homepage quick links (owner request 2026-10-05: 'all sections on the first screen as big
buttons'): Games · Guides · News · About as four large tiles right under the hero, before the
calculator. A <div role="navigation">, not <nav>: every <nav> is styled as the header bar. Labels reuse the header menu (nav_menu.L) and the footer's own About text, so nothing
new to translate. Games / Guides jump to sections on the same page (#games, #hub).
Idempotent via <!--quick--> markers. Run after nav_menu.py and home_hub.py."""
import os, re
import nav_menu as N

ROOT = N.ROOT


def about_label(s):
    m = re.search(r'<footer>.*?<a href="\./about\.html">([^<]+)</a>', s, re.S)
    return m.group(1).strip()


def main():
    n = 0
    for lang in N.L:
        p = ROOT + ('' if lang == 'en' else lang + os.sep) + 'index.html'
        if not os.path.exists(p):
            continue
        s = open(p, encoding='utf-8').read()
        s = re.sub(r'<!--quick-->.*?<!--/quick-->\n', '', s, flags=re.S)
        g, gd, news, _, _ = N.L[lang]
        tiles = [('#games', '🎮', g), ('#hub', '📊', gd), ('./news.html', '📰', news), ('./about.html', 'ℹ️', about_label(s))]
        block = ('<!--quick--><div class="g-quick" role="navigation" aria-label="' + ' · '.join(t[2] for t in tiles) + '">'
                 + ''.join(f'<a href="{h}"><span aria-hidden="true">{i}</span>{t}</a>' for h, i, t in tiles)
                 + '</div><!--/quick-->\n')
        # anchors for the two in-page tiles
        s = s.replace('<section class="section g-hub">', '<section class="section g-hub" id="hub">', 1)
        s = re.sub(r'<section class="section">(\s*<h2 class="section-title">[^<]*</h2>\s*<p class="section-sub">[^<]*</p>\s*<div class="games-grid">)',
                   r'<section class="section" id="games">\1', s, count=1)
        anchor = '  <div class="g-panel">'
        if s.count(anchor) != 1 or 'id="games"' not in s or 'id="hub"' not in s:
            raise SystemExit(f'{p}: anchors not found')
        s = s.replace(anchor, block + anchor, 1)
        open(p, 'w', encoding='utf-8', newline='').write(s)
        n += 1
    print('quick links on', n, 'homepages')


if __name__ == '__main__':
    main()
