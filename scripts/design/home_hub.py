"""Homepage block "Everything on the site": news + the 5 guides as cards, so a
visitor sees the whole site without opening a game first (owner request
2026-09-30). Labels for the guides come from nav_menu (localized resources
callout); card titles/descriptions below. Idempotent. Run after nav_menu.py."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nav_menu as nm

ROOT = nm.ROOT
# (section title, subtitle, [news, market, compare, safety, glossary, methodology] descriptions)
T = {
 'en': ('Everything on the site', 'Fresh prices, guides and the rules behind every number',
        ['Fresh prices by region, with dates and sources', 'Real price ranges for all 9 games', 'Which game has the priciest accounts',
         'Real scam patterns and how to avoid them', 'OG, whale, smurf and 20+ terms explained', 'How we check every number']),
 'ru': ('Всё на сайте', 'Свежие цены, гайды и правила, по которым мы считаем каждую цифру',
        ['Свежие цены по регионам — с датами и источниками', 'Реальные диапазоны цен по всем 9 играм', 'В какой игре самые дорогие аккаунты',
         'Реальные схемы обмана и как их избежать', 'OG, whale, smurf и ещё 20+ терминов простыми словами', 'Как мы проверяем каждую цифру']),
 'es': ('Todo en el sitio', 'Precios frescos, guías y las reglas detrás de cada cifra',
        ['Precios frescos por región, con fechas y fuentes', 'Rangos de precio reales de los 9 juegos', 'Qué juego tiene las cuentas más caras',
         'Estafas reales y cómo evitarlas', 'OG, whale, smurf y 20+ términos explicados', 'Cómo verificamos cada cifra']),
 'pt': ('Tudo no site', 'Preços frescos, guias e as regras por trás de cada número',
        ['Preços frescos por região, com datas e fontes', 'Faixas de preço reais dos 9 jogos', 'Qual jogo tem as contas mais caras',
         'Golpes reais e como evitá-los', 'OG, whale, smurf e mais de 20 termos explicados', 'Como verificamos cada número']),
 'id': ('Semua di situs ini', 'Harga terbaru, panduan, dan aturan di balik setiap angka',
        ['Harga terbaru per wilayah, dengan tanggal dan sumber', 'Kisaran harga nyata untuk 9 game', 'Game mana yang akunnya paling mahal',
         'Pola penipuan nyata dan cara menghindarinya', 'OG, whale, smurf dan 20+ istilah dijelaskan', 'Cara kami mengecek setiap angka']),
 'tr': ('Sitede neler var', 'Güncel fiyatlar, rehberler ve her rakamın arkasındaki kurallar',
        ['Bölgelere göre güncel fiyatlar, tarih ve kaynaklarla', '9 oyunun gerçek fiyat aralıkları', 'En pahalı hesaplar hangi oyunda',
         'Gerçek dolandırıcılık yöntemleri ve korunma yolları', 'OG, whale, smurf ve 20+ terim açıklandı', 'Her rakamı nasıl kontrol ediyoruz']),
 'ar': ('كل ما في الموقع', 'أسعار حديثة وأدلة وقواعد كل رقم ننشره',
        ['أسعار حديثة حسب المنطقة مع التواريخ والمصادر', 'نطاقات أسعار حقيقية لجميع الألعاب التسع', 'أي لعبة حساباتها الأغلى',
         'أساليب احتيال حقيقية وكيف تتجنبها', 'شرح OG وwhale وsmurf وأكثر من 20 مصطلحًا', 'كيف نتحقق من كل رقم']),
 'vi': ('Mọi thứ trên trang', 'Giá mới nhất, hướng dẫn và nguyên tắc đằng sau mỗi con số',
        ['Giá mới nhất theo khu vực, kèm ngày và nguồn', 'Khoảng giá thực của cả 9 trò chơi', 'Trò chơi nào có tài khoản đắt nhất',
         'Các chiêu lừa đảo thực tế và cách tránh', 'Giải thích OG, whale, smurf và hơn 20 thuật ngữ', 'Cách chúng tôi kiểm tra từng con số']),
 'hi': ('साइट पर सब कुछ', 'ताज़ा कीमतें, गाइड और हर आँकड़े के पीछे के नियम',
        ['क्षेत्र के हिसाब से ताज़ा कीमतें, तारीख़ और स्रोत के साथ', 'सभी 9 गेम की असली कीमत रेंज', 'किस गेम के अकाउंट सबसे महँगे हैं',
         'असली धोखाधड़ी के तरीके और उनसे बचाव', 'OG, whale, smurf और 20+ शब्द आसान भाषा में', 'हम हर आँकड़ा कैसे जाँचते हैं']),
 'fr': ('Tout le site', 'Prix récents, guides et règles derrière chaque chiffre',
        ['Prix récents par région, avec dates et sources', 'Fourchettes de prix réelles des 9 jeux', 'Quel jeu a les comptes les plus chers',
         'Arnaques réelles et comment les éviter', 'OG, whale, smurf et 20+ termes expliqués', 'Comment nous vérifions chaque chiffre']),
 'de': ('Alles auf der Seite', 'Aktuelle Preise, Ratgeber und die Regeln hinter jeder Zahl',
        ['Aktuelle Preise nach Region, mit Datum und Quellen', 'Echte Preisspannen für alle 9 Spiele', 'Welches Spiel die teuersten Accounts hat',
         'Echte Betrugsmaschen und wie du sie vermeidest', 'OG, Whale, Smurf und 20+ Begriffe erklärt', 'Wie wir jede Zahl prüfen']),
 'it': ('Tutto sul sito', 'Prezzi aggiornati, guide e le regole dietro ogni numero',
        ['Prezzi aggiornati per regione, con date e fonti', 'Fasce di prezzo reali per tutti i 9 giochi', 'Quale gioco ha gli account più costosi',
         'Truffe reali e come evitarle', 'OG, whale, smurf e oltre 20 termini spiegati', 'Come verifichiamo ogni numero']),
 'ja': ('サイトのすべて', '最新価格、ガイド、そしてすべての数値の根拠',
        ['地域別の最新価格（日付・出典つき）', '全9タイトルの実際の価格帯', 'アカウントが最も高いゲームは？',
         '実際の詐欺パターンと対策', 'OG・whale・smurfなど20以上の用語解説', '数値の確認方法']),
 'ko': ('사이트 전체 보기', '최신 가격, 가이드, 그리고 모든 숫자의 기준',
        ['지역별 최신 가격, 날짜와 출처 포함', '9개 게임의 실제 가격대', '계정이 가장 비싼 게임은?',
         '실제 사기 수법과 피하는 방법', 'OG, whale, smurf 등 20개+ 용어 설명', '모든 숫자를 확인하는 방법']),
 'zh': ('本站全部内容', '最新价格、指南，以及每个数字背后的规则',
        ['按地区的最新价格，附日期和来源', '全部9款游戏的真实价格区间', '哪款游戏的账号最贵',
         '真实骗局套路及防范方法', 'OG、whale、smurf等20多个术语详解', '我们如何核对每个数字']),
 'pl': ('Wszystko na stronie', 'Świeże ceny, poradniki i zasady stojące za każdą liczbą',
        ['Świeże ceny według regionów, z datami i źródłami', 'Prawdziwe przedziały cen dla 9 gier', 'Która gra ma najdroższe konta',
         'Prawdziwe oszustwa i jak ich unikać', 'OG, whale, smurf i 20+ pojęć wyjaśnionych', 'Jak sprawdzamy każdą liczbę']),
 'th': ('ทุกอย่างในเว็บไซต์', 'ราคาล่าสุด คู่มือ และหลักการเบื้องหลังทุกตัวเลข',
        ['ราคาล่าสุดแยกตามภูมิภาค พร้อมวันที่และแหล่งที่มา', 'ช่วงราคาจริงของทั้ง 9 เกม', 'เกมไหนมีบัญชีราคาแพงที่สุด',
         'กลโกงที่เกิดขึ้นจริงและวิธีหลีกเลี่ยง', 'อธิบาย OG, whale, smurf และคำศัพท์อีก 20+ คำ', 'วิธีที่เราตรวจสอบทุกตัวเลข']),
 'tl': ('Lahat ng nasa site', 'Pinakabagong presyo, mga gabay at ang mga patakaran sa likod ng bawat numero',
        ['Pinakabagong presyo ayon sa rehiyon, may petsa at source', 'Tunay na saklaw ng presyo ng 9 na laro', 'Aling laro ang may pinakamahal na account',
         'Tunay na mga scam at paano iiwasan', 'OG, whale, smurf at 20+ termino, ipinaliwanag', 'Paano namin sinusuri ang bawat numero']),
 'sw': ('Kila kitu kwenye tovuti', 'Bei mpya, miongozo na kanuni nyuma ya kila namba',
        ['Bei mpya kwa kila eneo, zenye tarehe na vyanzo', 'Viwango halisi vya bei kwa michezo yote 9', 'Mchezo gani una akaunti za bei ghali zaidi',
         'Utapeli halisi na jinsi ya kuuepuka', 'OG, whale, smurf na istilahi 20+ zimefafanuliwa', 'Jinsi tunavyokagua kila namba']),
 'ms': ('Semua di laman ini', 'Harga terkini, panduan dan peraturan di sebalik setiap angka',
        ['Harga terkini mengikut rantau, dengan tarikh dan sumber', 'Julat harga sebenar untuk 9 permainan', 'Permainan mana yang akaunnya paling mahal',
         'Penipuan sebenar dan cara mengelaknya', 'OG, whale, smurf dan 20+ istilah diterangkan', 'Cara kami menyemak setiap angka']),
 'uz': ('Saytda hammasi', 'Yangi narxlar, qoʻllanmalar va har bir raqam ortidagi qoidalar',
        ['Hududlar boʻyicha yangi narxlar, sana va manbalar bilan', 'Barcha 9 oʻyinning haqiqiy narx oraligʻi', 'Qaysi oʻyinda akkauntlar eng qimmat',
         'Haqiqiy firibgarlik usullari va ulardan saqlanish', 'OG, whale, smurf va 20+ atama tushuntirilgan', 'Har bir raqamni qanday tekshiramiz']),
 'kk': ('Сайттағының бәрі', 'Жаңа бағалар, нұсқаулықтар және әр санның ережелері',
        ['Өңірлер бойынша жаңа бағалар, күні мен дереккөзімен', 'Барлық 9 ойынның нақты баға ауқымы', 'Қай ойынның аккаунттары ең қымбат',
         'Нақты алаяқтық тәсілдері және олардан сақтану', 'OG, whale, smurf және 20+ термин түсіндірілген', 'Әр санды қалай тексереміз']),
 'tk': ('Saýtdaky ähli zat', 'Täze bahalar, gollanmalar we her sanyň aňyrsyndaky düzgünler',
        ['Sebitler boýunça täze bahalar, senesi we çeşmesi bilen', 'Ähli 9 oýnuň hakyky baha aralygy', 'Haýsy oýnuň hasaplary iň gymmat',
         'Hakyky galplyk usullary we olardan gorag', 'OG, whale, smurf we 20+ adalga düşündirildi', 'Her sany nähili barlaýarys']),
 'ky': ('Сайттагынын баары', 'Жаңы баалар, колдонмолор жана ар бир сандын эрежелери',
        ['Аймактар боюнча жаңы баалар, датасы жана булагы менен', 'Бардык 9 оюндун чыныгы баа диапазону', 'Кайсы оюндун аккаунттары эң кымбат',
         'Чыныгы алдамчылык ыкмалары жана алардан сактануу', 'OG, whale, smurf жана 20+ термин түшүндүрүлгөн', 'Ар бир санды кантип текшеребиз']),
}
ICONS = ['📰', '📊', '⚖️', '🛡️', '📖', '🔬']


def block(lang):
    title, sub, descs = T[lang]
    g, gd, news, mr, _ = nm.L[lang]
    gl = nm.guide_labels(lang)
    strip = lambda s: re.sub(r'^\W+\s*', '', s)
    items = [(nm.SITE + 'news.html', news), ('./market-report.html', strip(mr)),
             ('./which-game-accounts-are-most-valuable.html', strip(gl.get('which-game-accounts-are-most-valuable', ''))),
             ('./account-trading-safety.html', strip(gl.get('account-trading-safety', ''))),
             ('./glossary.html', strip(gl.get('glossary', ''))), ('./methodology.html', strip(gl.get('methodology', '')))]
    cards = ''.join(f'\n    <a class="hub-card" href="{h}"><span class="hub-ico">{ICONS[i]}</span><strong>{lbl}</strong><span>{descs[i]}</span></a>'
                    for i, (h, lbl) in enumerate(items))
    return (f'<!-- SITE HUB -->\n<section class="section g-hub">\n  <h2 class="section-title">{title}</h2>\n'
            f'  <p class="section-sub">{sub}</p>\n  <div class="hub-grid">{cards}\n  </div>\n</section>\n\n')


def main():
    n = 0
    for lang in T:
        f = ROOT + ('index.html' if lang == 'en' else lang + os.sep + 'index.html')
        s = open(f, encoding='utf-8').read()
        s = re.sub(r'<!-- SITE HUB -->.*?</section>\n\n', '', s, flags=re.S)
        s = s.replace('<!-- HOW IT WORKS -->', block(lang) + '<!-- HOW IT WORKS -->', 1)
        open(f, 'w', encoding='utf-8', newline='').write(s)
        n += 1
    print('hub block on', n, 'homepages')


if __name__ == '__main__':
    main()
