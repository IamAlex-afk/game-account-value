"""PUBG Mobile game page (2026-10-14) for every language that has text in pubg_text_*.py.

Built on that language's own free-fire.html: header, footer, calculator shell, card
teaser and section headings are already translated there; everything about the game
(head, JSON-LD, hero, calculator texts, sections, world block, sources) is replaced.
Idempotent. After it: nav_menu.py (Games menu + language switcher), then site_check.py.
Run: python scripts/design/pubg_page.py"""
import html, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.abspath(os.path.join(HERE, '..', '..')) + os.sep
SITE = 'https://gameaccountvalue.com/'
SLUG, GAME = 'pubg-mobile', 'PUBG Mobile'
PUBLISHED = MODIFIED = '2026-10-14'

import world_markets as WM                      # world-table labels (T) and each language's own market (LOCAL)
from world_events import render_events, render_event_ld
from world_results import render_results
from world_extra import NAMES
import pubg_text_a, pubg_text_b, pubg_text_c
TEXT = {}
for mod in (pubg_text_a, pubg_text_b, pubg_text_c):
    TEXT.update(mod.TEXT)
ROWS, BRACKETS = pubg_text_a.ROWS, pubg_text_a.BRACKETS
NBSP = ' '


def localize(t):
    """Thousands separator of the language (default ','); a space becomes a no-break space everywhere."""
    thou = t.get('thou', ',')
    if thou == ' ':
        fix = lambda x: re.sub(r'(?<=\d) (?=\d{3}\b)', NBSP, x)
        t = {k: (fix(v) if isinstance(v, str) else [fix(i) for i in v] if isinstance(v, list) else
                 {kk: fix(vv) for kk, vv in v.items()} if isinstance(v, dict) else v) for k, v in t.items()}
    glue = lambda x: re.sub(r'(?<=\d) (?=[$€₺])', NBSP, x)     # "4.960 $" never breaks between number and sign
    t = {k: (glue(v) if isinstance(v, str) else [glue(i) for i in v] if isinstance(v, list) else v) for k, v in t.items()}
    dec = t.get('dec', '.')
    sep = NBSP if thou == ' ' else thou

    def money(x):                                   # "$2,348.50" → this language's separators
        x = re.sub(r'(?<=\d)\.(?=\d)', '\x00', x)
        x = re.sub(r'(?<=\d),(?=\d{3})', sep, x)
        x = x.replace('\x00', dec)
        if t.get('cur_after'):                        # "$4.960" → "4.960 $" where the language writes it so
            x = re.sub(r'([$€])(\d[\d.,' + NBSP + r']*\d|\d)', lambda m: m.group(2) + NBSP + m.group(1), x)
        return x
    t['money'] = money
    t['level'] = lambda x: re.sub(r'(?<=\d)\.(?=\d)', dec, x)   # collection level "81.5"
    return t

OTHER = [('roblox', 'Roblox'), ('brawl-stars', 'Brawl Stars'), ('clash-of-clans', 'Clash of Clans'), ('clash-royale', 'Clash Royale'),
         ('free-fire', 'Free Fire'), ('genshin-impact', 'Genshin Impact'), ('mobile-legends', 'Mobile Legends'),
         ('fortnite', 'Fortnite'), ('minecraft', 'Minecraft')]
MARKETS = {   # region → (marketplaces, asking prices seen, ≈ USD)
    'global': ([('Eldorado.gg', pubg_text_a.EL)], '$2 – $399.99', '$2 – $400'),
    'cis': ([('FunPay', pubg_text_a.FP)], '€0.26 – €3,286', '$0.29 – $3,676'),
    'tr': ([('GameSatış', pubg_text_a.GS)], '1,000 ₺ – 245,000 ₺', '$20 – $4,960'),
    'sea': ([('igitems.com', pubg_text_a.IG)], '₫1,198,362 – ₫20,014,498', '$47 – $781'),
}
FLAG = {'global': '🌍', 'cis': '🇷🇺', 'tr': '🇹🇷', 'sea': '🌏'}
BLOCKED = {'br'}   # GGMAX PUBG Mobile page answered 403 on 2026-10-14 (as for every game before)


def path(lang):
    return ROOT + ('' if lang == 'en' else lang + os.sep)


def url(lang):
    return SITE + ('' if lang == 'en' else lang + '/') + SLUG + '.html'


def plain(h):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', h))).strip()


def world(lang, t):
    w = WM.T[lang]; c = w['cols']
    reg = lambda k: w['reg']['global_' if k == 'global' else k].replace('&', '&amp;')
    local = WM.LOCAL.get(lang, 'global')
    order = ([local] if local in MARKETS else []) + [k for k in ('global', 'cis', 'tr', 'sea') if k != local]

    def row(k, mine):
        where = ', '.join(f'<a href="{u}" target="_blank" rel="noopener">{n}</a>' for n, u in MARKETS[k][0])
        head = (f'<th scope="row"><span class="wm-flag" aria-hidden="true">{FLAG[k]}</span>{reg(k)}'
                + (f' <span class="wm-you">{w["your"]}</span>' if mine else '') + '</th>')
        cls = ' class="wm-mine"' if mine else ''
        return (f'<tr{cls}>{head}<td data-l="{c[1]}">{where}</td>'
                f'<td data-l="{c[2]}" class="wm-num">{t["money"](MARKETS[k][1])}</td><td data-l="{c[3]}" class="wm-num">{t["money"](MARKETS[k][2])}</td>'
                f'<td data-l="{c[4]}">{t["world_dem"]["global_" if k == "global" else k]}</td></tr>')
    if local in MARKETS:
        rows = row(local, True) + f'<tr class="wm-sep"><td colspan="5">{w["others"]}</td></tr>' + ''.join(row(k, False) for k in order[1:])
    elif local in BLOCKED:   # the reader's own market, tried and refused (403) — said so, never estimated
        head = (f'<th scope="row"><span class="wm-flag" aria-hidden="true">{WM.FLAG[local]}</span>{reg(local)}'
                f' <span class="wm-you">{w["your"]}</span></th>')
        rows = (f'<tr class="wm-mine">{head}<td colspan="4" class="wm-nv">{w["nv"]}</td></tr>'
                f'<tr class="wm-sep"><td colspan="5">{w["others"]}</td></tr>' + ''.join(row(k, False) for k in order))
    else:
        rows = ''.join(row(k, False) for k in order)
    return ('<section class="g-card g-news-card g-world"><span id="world" class="anchor-target"></span>\n'
            f'<h2>{w["title"].format(game=GAME)}</h2>\n<p class="wm-intro">{w["intro"]}</p>\n'
            '<div class="wm-wrap"><table class="wm-table"><thead><tr>' + ''.join(f'<th scope="col">{x}</th>' for x in c) +
            f'</tr></thead><tbody>{rows}</tbody></table></div>\n'
            f'<p class="wm-note">{t["world_note"]} {w["checked"]}: <time datetime="{MODIFIED}">{MODIFIED}</time>.</p>\n'
            + t['money'](render_events(SLUG, lang, NAMES)) + render_event_ld(SLUG) + t['money'](render_results(SLUG, lang, NAMES)) + '\n</section>\n')


def sections(t, h2):
    sec = lambda anchor, body: f'<section class="g-card g-news-card"><span id="{anchor}" class="anchor-target"></span>\n{body}\n</section>\n'
    table = ('<table class="tier-table">\n<tbody>\n  <tr>' + ''.join(f'<th>{x}</th>' for x in t['table_head']) + '</tr>\n' +
             ''.join(f'  <tr><td>{t["level"](a)}</td><td>{t["money"](b)}</td><td>{c}</td></tr>\n' for a, b, c in ROWS) + '</tbody>\n</table>')
    brackets = ('<table class="tier-table">\n<tbody>\n  <tr>' + ''.join(f'<th>{x}</th>' for x in t['brackets_head']) + '</tr>\n' +
                ''.join(f'  <tr><td>{t["money"](a)}</td><td>{b}</td></tr>\n' for a, b in BRACKETS) + '</tbody>\n</table>')
    ul = lambda items, tag='ul': f'<{tag}>\n' + ''.join(f'  <li>{i}</li>\n' for i in items) + f'</{tag}>'
    return (sec('pricing', f'<h2>{h2["pricing"]}</h2>\n<h3>{t["q_worth"]}</h3>\n<p>{t["a_worth"]}</p>\n<h3>{t["q_table"]}</h3>\n{table}\n'
                           f'<p style="font-size:13px; color:var(--muted);">{t["table_note"]}</p>\n'
                           f'<h3>{t["q_brackets"]}</h3>\n{brackets}\n<p style="font-size:13px; color:var(--muted);">{t["brackets_note"]}</p>')
            + '{WORLD}' +
            sec('value', f'<h2>{h2["value"]}</h2>\n<h3>{t["q_value"]}</h3>\n{ul(t["value"])}\n<h3>{t["q_lookup"]}</h3>\n{ul(t["lookup"])}') +
            sec('shots', f'<h2>{t["h2_shots"]}</h2>\n<h3>{t["q_shots"]}</h3>\n<p>{t["shots_intro"]}</p>\n{ul(t["shots"])}\n'
                         f'<p style="font-size:13px; color:var(--muted);">{t["shots_note"]}</p>') +
            sec('scams', f'<h2>{h2["scams"]}</h2>\n<h3>{t["q_scams"]}</h3>\n<div class="risk-box">\n  <p>{t["a_scams"]}</p>\n</div>') +
            sec('rules', f'<h2>{h2["rules"]}</h2>\n<h3>{t["q_rules"]}</h3>\n<p>{t["a_rules"]}</p>\n\n<h3>{t["q_where"]}</h3>\n<p>{t["a_where"]}</p>'))


def faq(t):
    table_txt = ' '.join(t['table_head']) + ' ' + ' '.join(f'{t["level"](a)} {t["money"](b)} {c}' for a, b, c in ROWS) + ' ' + t['table_note']
    br_txt = ' '.join(t['brackets_head']) + ' ' + ' '.join(f'{t["money"](a)} {b}' for a, b in BRACKETS) + ' ' + t['brackets_note']
    qa = [(t['q_worth'], t['a_worth']), (t['q_table'], table_txt), (t['q_brackets'], br_txt), (t['q_value'], ' '.join(t['value'])),
          (t['q_lookup'], ' '.join(t['lookup'])), (t['q_shots'], t['shots_intro'] + ' ' + ' '.join(t['shots']) + ' ' + t['shots_note']),
          (t['q_scams'], t['a_scams']), (t['q_rules'], t['a_rules']), (t['q_where'], t['a_where'])]
    return [{'@type': 'Question', 'name': plain(q), 'acceptedAnswer': {'@type': 'Answer', 'text': plain(a)}} for q, a in qa]


def build(lang):
    t = localize(dict(TEXT[lang]))
    s = open(path(lang) + 'free-fire.html', encoding='utf-8').read()
    langs = list(dict.fromkeys(['en'] + [l for l in TEXT if l != 'en']))

    # ---- head
    s = re.sub(r'<title>.*?</title>', '<title>' + html.escape(t['title'], quote=False) + '</title>', s, count=1)
    meta = lambda attr, name, val: (re.compile(r'(<meta ' + attr + '="' + re.escape(name) + r'" content=")[^"]*(")'),
                                    lambda m: m.group(1) + html.escape(val) + m.group(2))
    for attr, name, val in (('name', 'description', t['desc']), ('property', 'og:title', t['og_title']), ('property', 'og:description', t['desc']),
                            ('property', 'og:url', url(lang)), ('property', 'og:image', SITE + 'og/pubg-mobile.jpg?v=4'),
                            ('property', 'og:image:alt', t['og_alt']), ('name', 'twitter:title', plain(t['og_title']).split(' — ')[0].split(' | ')[0]),
                            ('name', 'twitter:image', SITE + 'og/pubg-mobile.jpg?v=4')):
        rx, fn = meta(attr, name, val)
        s, n = rx.subn(fn, s, count=1)
        assert n == 1, (lang, name)
    s = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{url(lang)}">', s, count=1)
    s = re.sub(r'(<link rel="alternate" hreflang="[^"]+" href="[^"]*">\n)+',
               f'<link rel="alternate" hreflang="x-default" href="{url("en")}">\n' +
               ''.join(f'<link rel="alternate" hreflang="{l}" href="{url(l)}">\n' for l in langs), s, count=1)

    # ---- JSON-LD: page graph and the short breadcrumb
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S)
    graph = json.loads(blocks[0])
    person = next(n for n in graph['@graph'] if n.get('@type') == 'Person')
    short = next(b for b in blocks[1:] if '"BreadcrumbList"' in b)
    crumbs = next((n for n in graph['@graph'] if n.get('@type') == 'BreadcrumbList'), None) or json.loads(short)
    home = crumbs['itemListElement'][0]['name']
    ld = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'BreadcrumbList', '@id': url(lang) + '#breadcrumb', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': home, 'item': crumbs['itemListElement'][0]['item']},
            {'@type': 'ListItem', 'position': 2, 'name': GAME, 'item': url(lang)}]},
        {'@type': 'Article', 'image': [SITE + 'og/pubg-mobile.jpg?v=4'], '@id': url(lang) + '#article', 'headline': plain(t['og_title']),
         'description': t['desc'], 'author': {'@id': SITE + '#author'},
         'publisher': {'@type': 'Organization', 'name': 'GameAccountValue', 'url': 'https://t.me/GameAccountValue_Bot'},
         'datePublished': PUBLISHED, 'dateModified': MODIFIED, 'inLanguage': lang, 'mainEntityOfPage': url(lang)},
        person,
        {'@type': 'FAQPage', '@id': url(lang) + '#faq', 'mainEntity': faq(t)}]}
    s = s.replace(blocks[0], '\n' + json.dumps(ld, ensure_ascii=False, indent=2) + '\n', 1)
    s = s.replace(short, json.dumps({'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': 1, 'name': home, 'item': crumbs['itemListElement'][0]['item']},
        {'@type': 'ListItem', 'position': 2, 'name': GAME}]}, ensure_ascii=False), 1)

    # ---- Free Fire's colour theme off (PUBG uses the site's default gold)
    s = re.sub(r'\n  /\* ===== theme-diamond.*?(?=</style>)', '\n', s, count=1, flags=re.S)
    s = s.replace('<body class="theme-diamond">', '<body>', 1)
    s = s.replace('start=game_free_fire&utm_campaign=free-fire', 'start=game_pubg_mobile&utm_campaign=pubg-mobile')
    s = s.replace('free-fire-news.html', 'news.html')
    s = s.replace('<li aria-current="page">Free Fire</li>', f'<li aria-current="page">{GAME}</li>', 1)

    # ---- hero
    a, b = s.index('<section class="report-hero"'), s.index('<div class="g-right">')
    hero = s[a:b]
    hero = re.sub(r'<h1>.*?</h1>', f'<h1>{t["h1"]}</h1>', hero, count=1, flags=re.S)
    hero = re.sub(r'(<p style="color:var\(--muted\); font-size:16px;">).*?(</p>)', lambda m: m.group(1) + t['intro'] + m.group(2), hero, count=1, flags=re.S)
    hero = re.sub(r'(<p class="report-updated">).*?(</p>)', lambda m: m.group(1) + t['updated'] + m.group(2), hero, count=1, flags=re.S)
    hero = re.sub(r'(<div class="fresh-badge">).*?(</div>)', lambda m: m.group(1) + t['badge'] + m.group(2), hero, count=1, flags=re.S)
    hero = re.sub(r'(<div class="price-range">).*?(</div>)', lambda m: m.group(1) + t['range'] + m.group(2), hero, count=1, flags=re.S)
    hero = re.sub(r'(<div class="fact-box">).*?(</div>)', lambda m: m.group(1) + ''.join(f'\n  <span>{f}</span>' for f in t['facts']) + '\n' + m.group(2),
                  hero, count=1, flags=re.S)
    s = s[:a] + hero + s[b:]

    # ---- calculator
    s = s.replace('id="vc-free-fire" data-game="free-fire" data-title="Free Fire"', 'id="vc-pubg-mobile" data-game="pubg-mobile" data-title="PUBG Mobile"', 1)
    s = re.sub(r'(<div class="vc-subtitle">).*?(</div>)', lambda m: m.group(1) + t['calc_sub'] + m.group(2), s, count=1, flags=re.S)
    s = re.sub(r'(<div class="g-why"><p><strong>[^<]*</strong>).*?(</p>)', lambda m: m.group(1) + t['calc_why'] + m.group(2), s, count=1, flags=re.S)

    # ---- section nav: keep the language's own labels, "Player tips" becomes "Screenshots"
    m = re.search(r'<div class="section-nav">(.*?)</div>', s, re.S)
    lab = dict(re.findall(r'href="#([a-z]+)">([^<]*)<', m.group(1)))
    nav = ''.join(f'\n  <a href="#{k}">{v}</a>' for k, v in (('pricing', lab['pricing']), ('world', WM.T[lang]['nav']), ('value', lab['value']),
                                                             ('shots', t['nav_shots']), ('scams', lab['scams']), ('rules', lab['rules'])))
    s = s[:m.start(1)] + nav + '\n' + s[m.end(1):]

    # ---- article body
    h2 = {}
    body_a = s.index('<div class="article-body">') + len('<div class="article-body">')
    body_b = s.index('<img class="g-joystick"')
    body_b = s.rindex('</div>', body_a, body_b)
    old = s[body_a:body_b]
    for k in ('pricing', 'value', 'scams', 'rules'):
        h2[k] = re.search(r'<span id="' + k + r'" class="anchor-target"></span>\s*<h2>([^<]*)</h2>', old).group(1)
    s = s[:body_a] + '\n\n' + sections(t, h2).replace('{WORLD}', world(lang, t)) + s[body_b:]

    # ---- the rest of <main>: game name in CTAs, other games, sources
    mi, mj = s.index('<main>'), s.index('</main>')
    main = s[mi:mj]
    main = re.sub(r'(<div class="report-cta"><a [^>]*>)([^<]*)', lambda m: m.group(1) + m.group(2).replace('Free Fire', GAME), main, count=1)
    main = re.sub(r'(<div class="g-exact" data-g-slot="result"><a [^>]*>)([^<]*)', lambda m: m.group(1) + m.group(2).replace('Free Fire', GAME), main, count=1)
    main = re.sub(r'(<div class="other-games">\s*<p[^>]*>[^<]*</p>).*?(\n</div>)',
                  lambda m: m.group(1) + ''.join(f'\n  <a href="./{k}.html">{n}</a>' for k, n in OTHER) + m.group(2), main, count=1, flags=re.S)
    main = re.sub(r'(<section class="sources-list">\s*<h2[^>]*>[^<]*</h2>\s*<ul>).*?(</ul>)',
                  lambda m: m.group(1) + ''.join(f'\n    <li>{x}</li>' for x in t['sources']) + '\n  ' + m.group(2), main, count=1, flags=re.S)
    s = s[:mi] + main + s[mj:]

    leftover = [x for x in re.findall(r'[^<>]{0,40}Free Fire[^<>]{0,40}', s[s.index('</nav>'):s.index('<footer>')])
                if 'free-fire.html' not in x and '>Free Fire<' not in x]
    out = path(lang) + SLUG + '.html'
    open(out, 'w', encoding='utf-8', newline='').write(s)
    return out, leftover


if __name__ == '__main__':
    for lang in TEXT:
        f, left = build(lang)
        print(lang, os.path.relpath(f, ROOT), 'Free Fire left in body:', left[:3])
