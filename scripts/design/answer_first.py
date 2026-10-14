# -*- coding: utf-8 -*-
"""Answer-first paragraph on every game page, 24 languages (2026-10-14).

AI answer engines (ChatGPT search, Perplexity, Gemini, Google AI Overviews) quote a short
paragraph that answers the question with numbers. Each game page gets one, right after its
intro: the usual asking range and the top listing (the same figures as the comparison page's
ceiling table); Minecraft names the separate username market instead. No new figures; formatted like the language's own market-report prices.
Idempotent (replaces its own <p class="answer-first">). Run after pubg_page.py / news_pages.py.
Run: python scripts/design/answer_first.py
"""
import io, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + os.sep
# usual asking range, top listing — which-game-accounts-are-most-valuable.html (ceiling table)
FIG = {'roblox': ('0.50', '60', '1500'), 'brawl-stars': ('3', '150', '300+'), 'clash-of-clans': ('10', '250', '250'),
       'clash-royale': ('0.50', '300', '600'), 'free-fire': ('0.73', '250', '755'), 'genshin-impact': ('5', '60', '8995'),
       'pubg-mobile': ('15', '300', '4960'), 'mobile-legends': ('0.50', '300', '2500'), 'fortnite': ('15', '300', '6200'),
       'minecraft': ('0.50', '632', '200000')}
NAME = {'roblox': 'Roblox', 'brawl-stars': 'Brawl Stars', 'clash-of-clans': 'Clash of Clans', 'clash-royale': 'Clash Royale',
        'free-fire': 'Free Fire', 'genshin-impact': 'Genshin Impact', 'pubg-mobile': 'PUBG Mobile',
        'mobile-legends': 'Mobile Legends', 'fortnite': 'Fortnite', 'minecraft': 'Minecraft'}
T = {
 'en': 'In short: a {game} account usually asks {typ} on resale marketplaces, and the top listings reach {top}.',
 'ru': 'Коротко: аккаунт {game} на площадках перепродажи обычно стоит {typ}, а самые дорогие объявления доходят до {top}.',
 'es': 'En resumen: una cuenta de {game} suele anunciarse por {typ} en los marketplaces de reventa, y los anuncios más caros llegan a {top}.',
 'pt': 'Resumindo: uma conta de {game} costuma ser anunciada por {typ} nos marketplaces de revenda, e os anúncios mais caros chegam a {top}.',
 'fr': 'En bref : un compte {game} est généralement proposé à {typ} sur les marketplaces de revente, et les annonces les plus chères atteignent {top}.',
 'de': 'Kurz gesagt: Ein {game}-Account wird auf Wiederverkaufsplattformen meist für {typ} angeboten, die teuersten Angebote erreichen {top}.',
 'it': 'In breve: un account {game} di solito viene proposto a {typ} sui marketplace di rivendita, e gli annunci più cari arrivano a {top}.',
 'tr': 'Kısaca: Bir {game} hesabı ikinci el pazar yerlerinde genellikle {typ} fiyatla ilana çıkıyor; en pahalı ilanlar {top} seviyesine ulaşıyor.',
 'ar': 'باختصار: يُعرض حساب {game} عادةً بسعر {typ} في أسواق إعادة البيع، وتصل أغلى الإعلانات إلى {top}.',
 'id': 'Singkatnya: akun {game} biasanya ditawarkan {typ} di marketplace jual-beli, dan listing termahal mencapai {top}.',
 'ms': 'Ringkasnya: akaun {game} biasanya ditawarkan pada {typ} di pasaran jualan semula, dan senarai termahal mencecah {top}.',
 'vi': 'Tóm lại: acc {game} thường được rao {typ} trên các chợ mua bán lại, còn tin đăng đắt nhất lên tới {top}.',
 'hi': 'संक्षेप में: {game} अकाउंट आमतौर पर रीसेल मार्केटप्लेस पर {typ} में लिस्ट होता है, और सबसे महंगी लिस्टिंग {top} तक जाती हैं।',
 'ja': '結論：{game}のアカウントは転売マーケットで通常{typ}で出品され、最も高い出品は{top}に達します。',
 'ko': '요약: {game} 계정은 재판매 마켓에서 보통 {typ}에 올라오며, 가장 비싼 매물은 {top}까지 갑니다.',
 'zh': '简而言之：{game} 账号在转卖平台上通常挂价 {typ}，最贵的挂牌可达 {top}。',
 'th': 'สรุปสั้น ๆ: บัญชี {game} มักตั้งราคาขายบนตลาดซื้อขายต่อที่ {typ} และประกาศที่แพงที่สุดสูงถึง {top}',
 'pl': 'W skrócie: konto {game} zwykle jest wystawiane za {typ} na platformach odsprzedaży, a najdroższe oferty sięgają {top}.',
 'tl': 'Sa madaling salita: ang {game} account ay karaniwang nakalista sa {typ} sa mga resale marketplace, at umaabot sa {top} ang pinakamahal na listing.',
 'sw': 'Kwa ufupi: akaunti ya {game} kwa kawaida huuzwa kwa {typ} kwenye masoko ya kuuza tena, na matangazo ya bei ghali zaidi hufika {top}.',
 'uz': 'Qisqasi: {game} akkaunti qayta sotish maydonchalarida odatda {typ} ga qoʻyiladi, eng qimmat eʼlonlar esa {top} gacha boradi.',
 'kk': 'Қысқасы: {game} аккаунты қайта сату алаңдарында әдетте {typ} бағасымен қойылады, ал ең қымбат хабарландырулар {top} дейін жетеді.',
 'tk': 'Gysgaça: {game} hasaby gaýtadan satyş meýdançalarynda adatça {typ} bahadan goýulýar, iň gymmat bildirişler bolsa {top} çenli ýetýär.',
 'ky': 'Кыскасы: {game} аккаунту кайра сатуу аянтчаларында адатта {typ} баада коюлат, ал эң кымбат жарнамалар {top} чейин жетет.',
}

# Minecraft: the ~$200,000 figure is a reported username sale, not a listing - say so instead
MC = {
 "en": "In short: a regular {game} account usually asks {typ} on resale marketplaces; rare short usernames are a separate collector market with far higher prices.",
 "ru": "Коротко: обычный аккаунт {game} на площадках перепродажи стоит {typ}; редкие короткие ники — отдельный коллекционный рынок с гораздо более высокими ценами.",
 "es": "En resumen: una cuenta normal de {game} suele anunciarse por {typ} en los marketplaces de reventa; los nombres de usuario cortos y raros son un mercado de coleccionistas aparte, con precios mucho más altos.",
 "pt": "Resumindo: uma conta comum de {game} costuma ser anunciada por {typ} nos marketplaces de revenda; nomes de usuário curtos e raros são um mercado de colecionadores à parte, com preços bem mais altos.",
 "fr": "En bref : un compte {game} ordinaire est généralement proposé à {typ} sur les marketplaces de revente ; les pseudos courts et rares forment un marché de collection à part, bien plus cher.",
 "de": "Kurz gesagt: Ein normaler {game}-Account wird auf Wiederverkaufsplattformen meist für {typ} angeboten; seltene kurze Nutzernamen sind ein eigener Sammlermarkt mit weit höheren Preisen.",
 "it": "In breve: un normale account {game} di solito viene proposto a {typ} sui marketplace di rivendita; i nomi utente corti e rari sono un mercato da collezione a parte, con prezzi molto più alti.",
 "tr": "Kısaca: Sıradan bir {game} hesabı ikinci el pazar yerlerinde genellikle {typ} fiyatla ilana çıkıyor; nadir kısa kullanıcı adları çok daha yüksek fiyatlı ayrı bir koleksiyon pazarı.",
 "ar": "باختصار: يُعرض حساب {game} العادي عادةً بسعر {typ} في أسواق إعادة البيع؛ أما أسماء المستخدمين القصيرة النادرة فهي سوق مقتنيات منفصل بأسعار أعلى بكثير.",
 "id": "Singkatnya: akun {game} biasa ditawarkan {typ} di marketplace jual-beli; username pendek yang langka adalah pasar kolektor tersendiri dengan harga jauh lebih tinggi.",
 "ms": "Ringkasnya: akaun {game} biasa ditawarkan pada {typ} di pasaran jualan semula; nama pengguna pendek yang jarang ialah pasaran pengumpul tersendiri dengan harga jauh lebih tinggi.",
 "vi": "Tóm lại: acc {game} thông thường được rao {typ} trên các chợ mua bán lại; tên người dùng ngắn hiếm là một thị trường sưu tầm riêng với giá cao hơn nhiều.",
 "hi": "संक्षेप में: सामान्य {game} अकाउंट रीसेल मार्केटप्लेस पर आमतौर पर {typ} में लिस्ट होता है; दुर्लभ छोटे यूज़रनेम का अलग कलेक्टर बाज़ार है, जहाँ कीमतें कहीं ज़्यादा हैं।",
 "ja": "結論：通常の{game}アカウントは転売マーケットで{typ}程度で出品されます。希少な短いユーザー名は別のコレクター市場で、価格ははるかに高くなります。",
 "ko": "요약: 일반 {game} 계정은 재판매 마켓에서 보통 {typ}에 올라옵니다. 희귀한 짧은 사용자명은 훨씬 비싼 별도의 수집가 시장입니다.",
 "zh": "简而言之：普通 {game} 账号在转卖平台上通常挂价 {typ}；稀有的短用户名是另一个收藏市场，价格高得多。",
 "th": "สรุปสั้น ๆ: บัญชี {game} ทั่วไปมักตั้งราคาขายบนตลาดซื้อขายต่อที่ {typ} ส่วนชื่อผู้ใช้สั้นที่หายากเป็นตลาดนักสะสมแยกต่างหากซึ่งราคาสูงกว่ามาก",
 "pl": "W skrócie: zwykłe konto {game} jest wystawiane za {typ} na platformach odsprzedaży; rzadkie krótkie nazwy użytkownika to osobny rynek kolekcjonerski z dużo wyższymi cenami.",
 "tl": "Sa madaling salita: ang karaniwang {game} account ay nakalista sa {typ} sa mga resale marketplace; ang mga bihirang maikling username ay hiwalay na merkado ng kolektor na mas mahal.",
 "sw": "Kwa ufupi: akaunti ya kawaida ya {game} huuzwa kwa {typ} kwenye masoko ya kuuza tena; majina mafupi adimu ya watumiaji ni soko tofauti la wakusanyaji lenye bei ya juu zaidi.",
 "uz": "Qisqasi: oddiy {game} akkaunti qayta sotish maydonchalarida odatda {typ} ga qoʻyiladi; noyob qisqa nikneymlar esa ancha qimmat alohida kolleksiya bozori.",
 "kk": "Қысқасы: қарапайым {game} аккаунты қайта сату алаңдарында әдетте {typ} бағасымен қойылады; сирек қысқа никнеймдер — бағасы әлдеқайда жоғары бөлек коллекция нарығы.",
 "tk": "Gysgaça: adaty {game} hasaby gaýtadan satyş meýdançalarynda adatça {typ} bahadan goýulýar; seýrek gysga lakamlar bolsa has gymmat aýratyn kolleksiýa bazary.",
 "ky": "Кыскасы: кадимки {game} аккаунту кайра сатуу аянтчаларында адатта {typ} баада коюлат; сейрек кыска никнеймдер — баасы алда канча жогору өзүнчө коллекция рыногу."
}


def money_style(sample):
    """From a market-report price like '$0.50 – $2,500' / '0,50 $ – 2.500 $' / '0.50$ – 2,500$'."""
    lo = re.match(r'\s*(\$?)\s*0([.,])50(\s*\$?)', sample)
    hi = re.search(r'2([.,   ]?)500', sample)
    return dict(before=bool(lo.group(1)), dec=lo.group(2), suffix=lo.group(3), thou=hi.group(1))


def fmt(st, v):
    plus = v.endswith('+'); v = v.rstrip('+')
    whole, _, frac = v.partition('.')
    out = ''
    while len(whole) > 3:
        out = st['thou'] + whole[-3:] + out; whole = whole[:-3]
    s = whole + out + (st['dec'] + frac if frac else '')
    s = ('$' + s) if st['before'] else (s + st['suffix'])
    return s + ('+' if plus else '')


def main():
    n = 0
    for lang, tpl in T.items():
        pre = '' if lang == 'en' else lang + '/'
        mr = io.open(ROOT + pre + 'market-report.html', encoding='utf-8').read()
        ml = re.search(r'href="\./mobile-legends\.html" class="game-card">.*?<span class="price"[^>]*>(.*?)</span>', mr, re.S).group(1)
        st = money_style(ml)
        for g, (a, b, top) in FIG.items():
            typ = fmt(st, a) + ' – ' + fmt(st, b)
            if lang == 'ar':
                typ = '<span dir="ltr">' + typ + '</span>'
            text = (MC[lang] if g == 'minecraft' else tpl).format(game=NAME[g], typ=typ, top=fmt(st, top))
            para = '<p class="answer-first">' + text + '</p>'
            p = ROOT + pre + g + '.html'
            s = io.open(p, encoding='utf-8', newline='').read()
            s2 = re.sub(r'\s*<p class="answer-first">.*?</p>', '', s, flags=re.S)
            main_at = s2.find('<main')
            h1 = re.search(r'</h1>', s2[main_at:])
            intro = re.search(r'<p[^>]*>.*?</p>', s2[main_at + h1.end():], re.S)
            at = main_at + h1.end() + intro.end()
            s2 = s2[:at] + '\n  ' + para + s2[at:]
            if s2 != s:
                io.open(p, 'w', encoding='utf-8', newline='').write(s2); n += 1
    print('pages updated:', n)


if __name__ == '__main__':
    main()
