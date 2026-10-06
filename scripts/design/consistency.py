"""Site-wide consistency pass (2026-09-30, owner: "what the main pages have,
every page should have"). Idempotent. Run after nav_menu.py, then run
nav_menu.py again so the pages given a skeleton <nav> here get the full menu.

1. 18+ card above the footer notice on every page with the standard footer
2. arcade joystick above the bottom bot CTA (.report-cta) on every page
3. market-report: breadcrumbs (+ BreadcrumbList JSON-LD) and the bottom bot
   CTA where the page version lacks them (en + 10 newer locales)
4. 404 / privacy / terms: site header (menu, language, bot button)"""
import glob, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + os.sep
SITE = 'https://gameaccountvalue.com/'
BOT = 'https://t.me/GameAccountValue_Bot'


def lang_of(rel):
    p = rel.split('/')
    return p[0] if len(p) == 2 else 'en'


def prefix(rel):
    return '../' if '/' in rel else './'


def main():
    stats = dict(g18=0, joy=0, crumbs=0, cta=0, header=0)
    for f in glob.glob(ROOT + '**/*.html', recursive=True):
        rel = os.path.relpath(f, ROOT).replace(os.sep, '/')
        if rel.startswith(('scripts/', '_', 'node_modules/', 'google')):
            continue
        s = o = open(f, encoding='utf-8').read()
        P = prefix(rel)
        lang = lang_of(rel)
        # 1) 18+ card
        if 'class="g-18"' not in s:
            s, n = re.subn(r'(<footer>\s*<div class="footer-logo">[^<]*</div>)',
                           lambda m: m.group(1) + f'\n  <img class="g-18" src="{P}assets/cyber-18.webp" width="420" height="449" alt="18+" loading="lazy" decoding="async">', s, count=1)
            stats['g18'] += n
        # 3) market-report gaps
        if rel.endswith('market-report.html'):
            gl = open(ROOT + ('glossary.html' if lang == 'en' else lang + '/glossary.html'), encoding='utf-8').read()
            if 'class="crumbs"' not in s:
                cm = re.search(r'<nav class="crumbs" aria-label="([^"]+)"><ol><li><a href="\./">(<img[^>]*>)([^<]+)</a></li>', gl)
                title = re.sub(r'<[^>]+>', '', re.search(r'<h1>(.*?)</h1>', s, re.S).group(1)).strip()
                crumbs = (f'\n<nav class="crumbs" aria-label="{cm.group(1)}"><ol><li><a href="./">{cm.group(2)}{cm.group(3)}</a></li>'
                          f'<li aria-current="page">{title}</li></ol></nav>\n')
                s = re.sub(r'(<nav(?: aria-label="[^"]*")?>.*?</nav>)', lambda m: m.group(1) + crumbs, s, count=1, flags=re.S)
                home = SITE + ('' if lang == 'en' else lang + '/')
                ld = {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
                    {'@type': 'ListItem', 'position': 1, 'name': cm.group(3), 'item': home},
                    {'@type': 'ListItem', 'position': 2, 'name': title, 'item': home + 'market-report.html'}]}
                s = s.replace('</head>', '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + '</script>\n</head>', 1)
                stats['crumbs'] += 1
            if 'class="report-cta"' not in s:
                cta = re.search(r'<div class="report-cta">.*?</div>', gl, re.S).group(0)
                utm = f'?start=landing_home&utm_source=website&utm_medium=landing&utm_campaign=market_report&utm_content={lang}'
                cta = cta.replace(f'href="{BOT}"', f'href="{BOT}{utm}"', 1)
                s = s.replace('<section class="sources-list">', cta + '\n\n<section class="sources-list">', 1)
                stats['cta'] += 1
        # 2) joystick above the bottom CTA
        if 'g-joystick' not in s and 'class="report-cta"' in s:
            s, n = re.subn(r'(<div class="report-cta">)',
                           lambda m: f'<img class="g-joystick" src="{P}assets/joystick.webp" width="480" height="435" alt="" loading="lazy" decoding="async">\n' + m.group(1), s, count=1)
            stats['joy'] += n
        # 4) header skeleton for pages without one
        if rel in ('404.html', 'privacy.html', 'terms.html') and '<nav' not in s:
            skel = (f'<nav>\n  <a href="./" class="logo">GameAccountValue</a>\n  <div class="nav-right">\n'
                    f'    <a href="{BOT}?start=landing_home&utm_source=website&utm_medium=landing&utm_campaign={rel[:-5]}" aria-label="Open Bot" class="nav-cta" data-event="cta_to_bot" rel="noopener noreferrer">🤖 Open Bot</a>\n  </div>\n</nav>\n')
            s = s.replace('<body>', '<body>\n' + skel, 1)
            if 'assets/style.css' not in s:
                s = s.replace('<link rel="stylesheet" href="./assets/glass.css">', '<link rel="stylesheet" href="./assets/style.css">\n<link rel="stylesheet" href="./assets/glass.css">', 1)
            stats['header'] += 1
        if s != o:
            open(f, 'w', encoding='utf-8', newline='').write(s)
    print(stats)


if __name__ == '__main__':
    main()
