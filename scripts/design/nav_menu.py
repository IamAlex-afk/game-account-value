"""Site-wide header menu (2026-09-30): Games ▾ / Guides ▾ / News + a language
switcher that keeps the visitor on the SAME page in the other language
(falls back to that language's homepage when the page isn't translated).
Dropdowns reuse the .lang-selector pattern handled by assets/nav.js.
Idempotent: rebuilds the first <nav> of every page. Run: python scripts/design/nav_menu.py"""
import glob, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + os.sep
SITE = 'https://gameaccountvalue.com/'
CUR = ' class="lang-current"'
GAMES = [('roblox', 'Roblox'), ('brawl-stars', 'Brawl Stars'), ('clash-of-clans', 'Clash of Clans'),
         ('clash-royale', 'Clash Royale'), ('free-fire', 'Free Fire'), ('genshin-impact', 'Genshin Impact'),
         ('mobile-legends', 'Mobile Legends'), ('fortnite', 'Fortnite'), ('minecraft', 'Minecraft')]
GUIDES = ['market-report', 'which-game-accounts-are-most-valuable', 'account-trading-safety', 'glossary', 'methodology']
LANG_NAMES = [('en', '🇺🇸 English'), ('ru', '🇷🇺 Русский'), ('es', '🇪🇸 Español'), ('pt', '🇧🇷 Português'),
              ('id', '🇮🇩 Indonesia'), ('tr', '🇹🇷 Türkçe'), ('ar', '🇸🇦 العربية'), ('vi', '🇻🇳 Tiếng Việt'),
              ('hi', '🇮🇳 हिन्दी'), ('fr', '🇫🇷 Français'), ('de', '🇩🇪 Deutsch'), ('it', '🇮🇹 Italiano'),
              ('ja', '🇯🇵 日本語'), ('ko', '🇰🇷 한국어'), ('th', '🇹🇭 ภาษาไทย'), ('pl', '🇵🇱 Polski'),
              ('zh', '🇨🇳 中文'), ('tl', '🇵🇭 Filipino'), ('sw', '🇰🇪 Kiswahili'), ('ms', '🇲🇾 Bahasa Melayu'),
              ('uz', "🇺🇿 O'zbekcha"), ('kk', '🇰🇿 Қазақша'), ('tk', '🇹🇲 Türkmençe'), ('ky', '🇰🇬 Кыргызча')]
# (Games, Guides, News, Market report, Select language)
L = {
 'en': ('Games', 'Guides', 'News', '📊 Market report', 'Select language'),
 'ru': ('Игры', 'Гайды', 'Новости', '📊 Отчёт рынка', 'Выбрать язык'),
 'es': ('Juegos', 'Guías', 'Noticias', '📊 Informe de mercado', 'Elegir idioma'),
 'pt': ('Jogos', 'Guias', 'Notícias', '📊 Relatório de mercado', 'Escolher idioma'),
 'id': ('Game', 'Panduan', 'Berita', '📊 Laporan pasar', 'Pilih bahasa'),
 'tr': ('Oyunlar', 'Rehberler', 'Haberler', '📊 Pazar raporu', 'Dil seç'),
 'ar': ('الألعاب', 'الأدلة', 'الأخبار', '📊 تقرير السوق', 'اختر اللغة'),
 'vi': ('Trò chơi', 'Hướng dẫn', 'Tin tức', '📊 Báo cáo thị trường', 'Chọn ngôn ngữ'),
 'hi': ('गेम', 'गाइड', 'समाचार', '📊 बाज़ार रिपोर्ट', 'भाषा चुनें'),
 'fr': ('Jeux', 'Guides', 'Actus', '📊 Rapport du marché', 'Choisir la langue'),
 'de': ('Spiele', 'Ratgeber', 'News', '📊 Marktbericht', 'Sprache wählen'),
 'it': ('Giochi', 'Guide', 'Notizie', '📊 Report di mercato', 'Scegli la lingua'),
 'ja': ('ゲーム', 'ガイド', 'ニュース', '📊 市場レポート', '言語を選択'),
 'ko': ('게임', '가이드', '뉴스', '📊 시장 보고서', '언어 선택'),
 'zh': ('游戏', '指南', '资讯', '📊 市场报告', '选择语言'),
 'pl': ('Gry', 'Poradniki', 'Aktualności', '📊 Raport rynkowy', 'Wybierz język'),
 'th': ('เกม', 'คู่มือ', 'ข่าว', '📊 รายงานตลาด', 'เลือกภาษา'),
 'tl': ('Mga laro', 'Mga gabay', 'Balita', '📊 Market report', 'Pumili ng wika'),
 'sw': ('Michezo', 'Miongozo', 'Habari', '📊 Ripoti ya soko', 'Chagua lugha'),
 'ms': ('Permainan', 'Panduan', 'Berita', '📊 Laporan pasaran', 'Pilih bahasa'),
 'uz': ('Oʻyinlar', 'Qoʻllanmalar', 'Yangiliklar', '📊 Bozor hisoboti', 'Tilni tanlang'),
 'kk': ('Ойындар', 'Нұсқаулықтар', 'Жаңалықтар', '📊 Нарық есебі', 'Тілді таңдаңыз'),
 'tk': ('Oýunlar', 'Gollanmalar', 'Täzelikler', '📊 Bazar hasabaty', 'Dili saýlaň'),
 'ky': ('Оюндар', 'Колдонмолор', 'Жаңылыктар', '📊 Базар отчёту', 'Тилди тандаңыз'),
}


def guide_labels(lang):
    """Localized guide labels from the language's own resources-callout block."""
    f = ROOT + ('' if lang == 'en' else lang + os.sep) + 'roblox.html'
    s = open(f, encoding='utf-8').read()
    block = s[s.find('class="resources-callout"'):]
    block = block[:block.find('</div>')]
    out = {m.group(1): m.group(2).strip() for m in re.finditer(r'href="\./([a-z-]+)\.html">([^<]+)</a>', block)}
    return out


def page_exists(lang, slug):
    p = ROOT + ('' if lang == 'en' else lang + os.sep) + (slug + '.html' if slug != 'index' else 'index.html')
    return os.path.exists(p)


def url(lang, slug):
    base = SITE + ('' if lang == 'en' else lang + '/')
    return base if slug == 'index' else base + slug + '.html'


def build(lang, slug, logo, cta):
    g, gd, news, mr, sel = L[lang]
    gl = guide_labels(lang)
    rel = lambda s: ('./' if s == 'index' else './' + s + '.html')
    games = ''.join(f'\n        <a href="{rel(k)}"{CUR if k == slug else ""}>{n}</a>' for k, n in GAMES)
    guides = f'\n        <a href="{rel("market-report")}"{CUR if slug == "market-report" else ""}>{mr}</a>'
    for k in GUIDES[1:]:
        guides += f'\n        <a href="{rel(k)}"{CUR if k == slug else ""}>{gl.get(k, k)}</a>'
    # News: English-only pages for now; the game's own news page from a game page.
    news_slug = (slug.replace('-news', '') + '-news') if slug in dict(GAMES) or slug.endswith('-news') else 'news'
    news_href = SITE + news_slug + '.html'
    langs = ''
    for code, name in LANG_NAMES:
        target = url(code, slug) if page_exists(code, slug) else url(code, 'index')
        langs += f'\n        <a href="{target}"{CUR if code == lang else ""} hreflang="{code}">{name}</a>'
    return (f'<nav>\n  {logo}\n'
            f'  <div class="nav-menu">\n'
            f'    <div class="lang-selector nav-dd">\n'
            f'      <button type="button" class="lang-btn" aria-haspopup="true" aria-expanded="false" aria-controls="nav-games">{g} <span class="lang-arrow">▾</span></button>\n'
            f'      <div class="lang-dropdown" id="nav-games" role="menu">{games}\n      </div>\n    </div>\n'
            f'    <div class="lang-selector nav-dd">\n'
            f'      <button type="button" class="lang-btn" aria-haspopup="true" aria-expanded="false" aria-controls="nav-guides">{gd} <span class="lang-arrow">▾</span></button>\n'
            f'      <div class="lang-dropdown" id="nav-guides" role="menu">{guides}\n      </div>\n    </div>\n'
            f'    <a class="nav-news" href="{news_href}">📰 {news}</a>\n'
            f'  </div>\n'
            f'  <div class="nav-right">\n'
            f'    <div class="lang-selector">\n'
            f'      <button type="button" class="lang-btn" aria-haspopup="true" aria-expanded="false" aria-controls="lang-menu" aria-label="{sel}">🌐 {lang.upper()} <span class="lang-arrow">▾</span></button>\n'
            f'      <div class="lang-dropdown" id="lang-menu" role="menu">{langs}\n      </div>\n    </div>\n'
            f'    {cta}\n  </div>\n</nav>')


def main():
    n = 0
    for f in glob.glob(ROOT + '**/*.html', recursive=True):
        rp = os.path.relpath(f, ROOT).replace(os.sep, '/')
        if rp.startswith(('scripts/', '_', 'node_modules/', 'google')) or rp in ('404.html',):
            continue
        parts = rp.split('/')
        lang = parts[0] if len(parts) == 2 else 'en'
        if lang not in L:
            continue
        slug = parts[-1][:-5]
        s = open(f, encoding='utf-8').read()
        m = re.search(r'<nav>.*?</nav>', s, re.S)
        if not m:
            continue
        old = m.group(0)
        logo = re.search(r'<a href="[^"]*" class="logo">[^<]*</a>', old).group(0)
        cta = re.search(r'<a [^>]*class="nav-cta"[^>]*>.*?</a>', old, re.S).group(0)
        new = build(lang, slug, logo, cta)
        s = s.replace(old, new, 1)
        if 'assets/nav.js' not in s:
            pre = '../' if lang != 'en' else './'
            s = s.replace('</body>', f'<script type="module" src="{pre}assets/nav.js" defer></script>\n</body>', 1)
        open(f, 'w', encoding='utf-8', newline='').write(s)
        n += 1
    print('nav rebuilt on', n, 'pages')


if __name__ == '__main__':
    main()
