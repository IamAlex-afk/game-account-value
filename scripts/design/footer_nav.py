"""Footer section links on every page (SITE-STANDARD plan step 6, 2026-10-05):
Games · Guides · News / About, above the footer notice. Labels reuse the header menu
(nav_menu.L, guide_labels) and the footer's own About link text, so nothing new to translate.
Idempotent: replaces the block between <!--foot-nav--> markers. Run: python scripts/design/footer_nav.py"""
import glob, os, re
import nav_menu as N

ROOT = N.ROOT


def about_label(s):
    m = re.search(r'<footer>.*?<a href="\./about\.html">([^<]+)</a>', s, re.S)
    return m.group(1).strip() if m else None


def build(lang, slug, about):
    g, gd, news, mr, _ = N.L[lang]
    gl = N.guide_labels(lang)
    cur = lambda k: ' aria-current="page"' if k == slug else ''
    li = lambda k, t: f'<li><a href="./{k}.html"{cur(k)}>{t}</a></li>'
    games = ''.join(li(k, n) for k, n in N.GAMES)
    plain = lambda t: re.sub(r'^[^\w]+', '', t).strip()  # menu labels carry an emoji prefix
    guides = li('market-report', plain(mr)) + ''.join(li(k, plain(gl.get(k, k))) for k in N.GUIDES[1:])
    site = li('news', news) + (li('about', about) if about else '')
    col = lambda h, items: f'<div class="foot-col"><p class="foot-h">{h}</p><ul>{items}</ul></div>'
    # a plain <div> inside <footer> (every <nav> here is styled as the sticky header bar)
    return (f'<!--foot-nav--><div class="foot-nav">'
            f'{col(g, games)}{col(gd, guides)}{col("GameAccountValue", site)}</div><!--/foot-nav-->')


def main():
    n = 0
    for f in glob.glob(ROOT + '**/*.html', recursive=True):
        rp = os.path.relpath(f, ROOT).replace(os.sep, '/')
        if rp.startswith(('scripts/', '_', 'node_modules/', 'google')) or rp == '404.html':
            continue
        parts = rp.split('/')
        lang = parts[0] if len(parts) == 2 else 'en'
        if lang not in N.L:
            continue
        s = open(f, encoding='utf-8').read()
        if '<footer>' not in s:
            continue
        s = re.sub(r'[ \t]*<!--foot-nav-->.*?<!--/foot-nav-->\n', '', s, flags=re.S)
        s = s.replace('<footer>\n', '<footer>\n  ' + build(lang, parts[-1][:-5], about_label(s)) + '\n', 1)
        open(f, 'w', encoding='utf-8', newline='').write(s)
        n += 1
    print('footer nav on', n, 'pages')


if __name__ == '__main__':
    main()
