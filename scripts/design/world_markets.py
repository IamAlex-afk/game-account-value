"""'Prices around the world' section for game pages, all 17 languages.

Data: asking prices actually seen on public marketplaces (never completed
sales), with the marketplace linked and the check date. Each language shows
its own market first. Descriptive only — no buy/sell advice.
Source notes: scripts/research/world-markets.md

Usage: python scripts/design/world_markets.py brawl-stars
"""
import os, re, sys, glob, collections, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from world_extra import render_extra
from world_data import MARKETS, N
spec = importlib.util.spec_from_file_location('r', os.path.join(HERE, 'rollout.py'))
R = importlib.util.module_from_spec(spec); spec.loader.exec_module(R)

CHECKED = '2026-09-28'
LANGS = ['en', 'ru', 'es', 'pt', 'id', 'tr', 'ar', 'vi', 'hi', 'fr', 'de', 'it', 'ja', 'ko', 'th', 'pl', 'zh']
LOCAL = {'en': 'global', 'es': 'global', 'fr': 'global', 'de': 'global', 'it': 'global', 'pl': 'global', 'ar': 'global', 'hi': 'global',
         'ru': 'cis', 'zh': 'cn', 'ja': 'jp', 'ko': 'kr', 'tr': 'tr', 'vi': 'sea', 'id': 'sea', 'th': 'sea', 'pt': 'br'}
ORDER = ['global', 'cis', 'cn', 'jp', 'kr', 'tr', 'sea', 'br']
FLAG = {'global': '🌍', 'cis': '🇷🇺', 'cn': '🇨🇳', 'jp': '🇯🇵', 'kr': '🇰🇷', 'tr': '🇹🇷', 'sea': '🌏', 'br': '🇧🇷'}

DATA = {
  'brawl-stars': {
    'global': dict(where=[('Eldorado.gg', 'https://www.eldorado.gg/brawl-stars-accounts/a/56-1-0'), ('igitems.com', 'https://igitems.com/brawl_stars-account')], local='$3 – $300+', usd='$3 – $300+', demand='global'),
    'cis':    dict(where=[('FunPay', 'https://funpay.com/en/lots/436/')], local='€0.21 – €3,852', usd='$0.24 – $4,386', demand='cis'),
    'cn':     dict(where=[('交易猫 Jiaoyimao', 'https://m.jiaoyimao.com/jg1009835/c1/')], local='¥100 – ¥1,200', usd='$15 – $179', demand='cn'),
    'jp':     dict(where=[('GameTrade', 'https://gametrade.jp/brawl-stars/exhibits')], local='¥500 – ¥23,000', usd='$3 – $146', demand='jp'),
    'kr':     dict(where=[('저팔계 Jeo8gye', 'https://www.jeo8gye.com/trade/list?game_code=111')], local='₩15,000 – ₩2,500,000', usd='$11 – $1,825', demand='kr'),
    'tr':     dict(where=[('GameSatış', 'https://www.gamesatis.com/brawl-stars-hesap-satisi')], local='59.99 ₺ – 19,900 ₺', usd='$1.2 – $408', demand='tr'),
    'sea':    dict(where=[('igitems.com', 'https://igitems.com/brawl_stars-account')], local='₫318,890 – ₫10,716,283', usd='$13 – $429', demand='sea'),
    'br':     None,   # GGMAX / Desapego / DFG block automated checks → not verified
  },
}

DATA.update(MARKETS)

# ---- translations -------------------------------------------------------
T = {
 'en': dict(title='{game} account prices around the world', nav='🌍 World',
   intro='Asking prices on public marketplaces in different countries, all checked on the same day. Your market comes first; the others show what players elsewhere value most.',
   your='Your market', others='Other markets', cols=('Market', 'Where', 'Asking prices seen', '≈ USD', 'Most valued there'),
   nv='Not verified yet — the main marketplaces there block automated checks.',
   note='Asking prices, not completed sales. Converted to USD at the rates of 25–27 September 2026. Descriptive only — not advice to buy or sell; account trading may break the game\'s rules.',
   checked='Checked',
   reg=dict(global_='Global / Western sites', cis='Russia & CIS', cn='China', jp='Japan', kr='South Korea', tr='Türkiye', sea='Southeast Asia', br='Brazil'),
   dem=dict(global_='Trophies and brawler count — the highest-priced listings name no rare skin', cis='Fully maxed accounts: all hypercharges, coins', cn='Cosmetics: retired and zodiac skins, wings; Master rank; account age', jp='Master rank, national ranking, first-owner accounts', kr='National ranking and prestige; very large skin collections', tr='Trophy count, costume count, transferable email / Supercell ID', sea='Trophies and maxed brawlers; many listings, asking prices falling')),
 'ru': dict(title='Цены на аккаунты {game} в мире', nav='🌍 Мир',
   intro='Цены в объявлениях на открытых площадках разных стран, проверенные в один день. Сначала — ваш рынок, дальше — что больше всего ценят игроки в других странах.',
   your='Ваш рынок', others='Другие рынки', cols=('Рынок', 'Где', 'Цены в объявлениях', '≈ USD', 'Что там ценят больше всего'),
   nv='Пока не проверено — основные площадки блокируют автоматическую проверку.',
   note='Это цены объявлений, а не завершённых сделок. Пересчёт в USD по курсам на 25–27 сентября 2026. Только описание рынка — не совет покупать или продавать; торговля аккаунтами может нарушать правила игры.',
   checked='Проверено',
   reg=dict(global_='Мировые / западные площадки', cis='Россия и СНГ', cn='Китай', jp='Япония', kr='Южная Корея', tr='Турция', sea='Юго-Восточная Азия', br='Бразилия'),
   dem=dict(global_='Кубки и число бойцов — в самых дорогих объявлениях редкие скины не упоминаются', cis='Полностью прокачанные аккаунты: все гиперзаряды, монеты', cn='Косметика: снятые с продажи скины и «созвездия», крылья; ранг Master; возраст аккаунта', jp='Ранг Master, место в рейтинге страны, аккаунты от первого владельца', kr='Место в рейтинге страны и престиж; огромные коллекции скинов', tr='Кубки, число костюмов, перенос почты / Supercell ID', sea='Кубки и прокачанные бойцы; объявлений много, цены снижаются')),
 'es': dict(title='Precios de cuentas de {game} en el mundo', nav='🌍 Mundo',
   intro='Precios pedidos en marketplaces públicos de distintos países, revisados el mismo día. Primero tu mercado; después, lo que más valoran los jugadores en otros lugares.',
   your='Tu mercado', others='Otros mercados', cols=('Mercado', 'Dónde', 'Precios pedidos', '≈ USD', 'Lo más valorado allí'),
   nv='Aún sin verificar: los principales marketplaces bloquean las comprobaciones automáticas.',
   note='Precios pedidos, no ventas cerradas. Convertido a USD con los tipos del 25–27 de septiembre de 2026. Solo descriptivo: no es un consejo de compra o venta; comerciar cuentas puede incumplir las reglas del juego.',
   checked='Revisado',
   reg=dict(global_='Sitios globales / occidentales', cis='Rusia y CEI', cn='China', jp='Japón', kr='Corea del Sur', tr='Turquía', sea='Sudeste Asiático', br='Brasil'),
   dem=dict(global_='Trofeos y número de brawlers: los anuncios más caros no mencionan ninguna skin rara', cis='Cuentas al máximo: todas las hipercargas, monedas', cn='Cosméticos: skins retiradas y del zodiaco, alas; rango Maestro; antigüedad de la cuenta', jp='Rango Maestro, ranking nacional, cuentas de primer dueño', kr='Ranking nacional y prestigio; colecciones de skins muy grandes', tr='Trofeos, número de trajes, correo / Supercell ID transferible', sea='Trofeos y brawlers al máximo; muchos anuncios, precios pedidos a la baja')),
 'pt': dict(title='Preços de contas de {game} pelo mundo', nav='🌍 Mundo',
   intro='Preços pedidos em marketplaces públicos de vários países, verificados no mesmo dia. Primeiro o seu mercado; depois, o que os jogadores de outros lugares mais valorizam.',
   your='Seu mercado', others='Outros mercados', cols=('Mercado', 'Onde', 'Preços pedidos', '≈ USD', 'O mais valorizado lá'),
   nv='Ainda não verificado — os principais marketplaces bloqueiam verificações automáticas.',
   note='Preços pedidos, não vendas concluídas. Convertido para USD pelas cotações de 25–27 de setembro de 2026. Apenas descritivo — não é conselho de compra ou venda; negociar contas pode violar as regras do jogo.',
   checked='Verificado',
   reg=dict(global_='Sites globais / ocidentais', cis='Rússia e CEI', cn='China', jp='Japão', kr='Coreia do Sul', tr='Turquia', sea='Sudeste Asiático', br='Brasil'),
   dem=dict(global_='Troféus e número de brawlers — os anúncios mais caros não citam nenhuma skin rara', cis='Contas no máximo: todas as hipercargas, moedas', cn='Cosméticos: skins retiradas e do zodíaco, asas; rank Mestre; idade da conta', jp='Rank Mestre, ranking nacional, contas de primeiro dono', kr='Ranking nacional e prestígio; coleções de skins enormes', tr='Troféus, número de trajes, e-mail / Supercell ID transferível', sea='Troféus e brawlers no máximo; muitos anúncios, preços pedidos em queda')),
 'id': dict(title='Harga akun {game} di seluruh dunia', nav='🌍 Dunia',
   intro='Harga yang diminta di marketplace publik berbagai negara, dicek pada hari yang sama. Pasar Anda ditampilkan pertama; sisanya menunjukkan apa yang paling dihargai pemain di tempat lain.',
   your='Pasar Anda', others='Pasar lain', cols=('Pasar', 'Di mana', 'Harga yang diminta', '≈ USD', 'Paling dihargai di sana'),
   nv='Belum terverifikasi — marketplace utama di sana memblokir pengecekan otomatis.',
   note='Harga yang diminta, bukan penjualan yang selesai. Dikonversi ke USD dengan kurs 25–27 September 2026. Hanya deskriptif — bukan saran membeli atau menjual; jual beli akun dapat melanggar aturan game.',
   checked='Dicek',
   reg=dict(global_='Situs global / Barat', cis='Rusia & CIS', cn='Tiongkok', jp='Jepang', kr='Korea Selatan', tr='Turki', sea='Asia Tenggara', br='Brasil'),
   dem=dict(global_='Trofi dan jumlah brawler — listing termahal tidak menyebut skin langka', cis='Akun maksimal: semua hypercharge, koin', cn='Kosmetik: skin yang sudah ditarik dan skin zodiak, sayap; rank Master; umur akun', jp='Rank Master, peringkat nasional, akun pemilik pertama', kr='Peringkat nasional dan prestige; koleksi skin sangat besar', tr='Jumlah trofi, jumlah kostum, email / Supercell ID yang bisa dipindah', sea='Trofi dan brawler maksimal; banyak listing, harga yang diminta turun')),
 'tr': dict(title='Dünyada {game} hesap fiyatları', nav='🌍 Dünya',
   intro='Farklı ülkelerdeki açık pazar yerlerinde istenen fiyatlar, hepsi aynı gün kontrol edildi. Önce sizin pazarınız; ardından diğer ülkelerdeki oyuncuların en çok değer verdikleri.',
   your='Sizin pazarınız', others='Diğer pazarlar', cols=('Pazar', 'Nerede', 'İstenen fiyatlar', '≈ USD', 'Orada en çok değer verilen'),
   nv='Henüz doğrulanmadı — oradaki başlıca pazar yerleri otomatik kontrolü engelliyor.',
   note='İstenen fiyatlardır, tamamlanmış satışlar değil. 25–27 Eylül 2026 kurlarıyla USD\'ye çevrildi. Yalnızca açıklayıcıdır — alım ya da satım tavsiyesi değildir; hesap ticareti oyunun kurallarını ihlal edebilir.',
   checked='Kontrol',
   reg=dict(global_='Küresel / Batı siteleri', cis='Rusya ve BDT', cn='Çin', jp='Japonya', kr='Güney Kore', tr='Türkiye', sea='Güneydoğu Asya', br='Brezilya'),
   dem=dict(global_='Kupa ve karakter sayısı — en pahalı ilanlar hiçbir nadir kostümden söz etmiyor', cis='Tamamen maksimum hesaplar: tüm hiper yükler, altın', cn='Kozmetikler: satıştan kalkmış ve burç kostümleri, kanatlar; Usta rütbesi; hesap yaşı', jp='Usta rütbesi, ulusal sıralama, ilk sahibinden hesaplar', kr='Ulusal sıralama ve prestij; çok büyük kostüm koleksiyonları', tr='Kupa sayısı, kostüm sayısı, devredilebilir e-posta / Supercell ID', sea='Kupalar ve maksimum karakterler; çok ilan var, istenen fiyatlar düşüyor')),
 'ar': dict(title='أسعار حسابات {game} حول العالم', nav='🌍 العالم',
   intro='الأسعار المطلوبة في المتاجر العامة في دول مختلفة، وقد تم فحصها كلها في اليوم نفسه. يظهر سوقك أولاً، ثم ما يقدّره اللاعبون أكثر في أماكن أخرى.',
   your='سوقك', others='أسواق أخرى', cols=('السوق', 'أين', 'الأسعار المطلوبة', '≈ دولار', 'الأكثر قيمة هناك'),
   nv='لم يتم التحقق بعد — المتاجر الرئيسية هناك تمنع الفحص الآلي.',
   note='هذه أسعار مطلوبة وليست مبيعات مكتملة. تم التحويل إلى الدولار بأسعار 25–27 سبتمبر 2026. للوصف فقط — ليست نصيحة بالشراء أو البيع؛ وقد يخالف تداول الحسابات قواعد اللعبة.',
   checked='تاريخ الفحص',
   reg=dict(global_='المواقع العالمية / الغربية', cis='روسيا ورابطة الدول المستقلة', cn='الصين', jp='اليابان', kr='كوريا الجنوبية', tr='تركيا', sea='جنوب شرق آسيا', br='البرازيل'),
   dem=dict(global_='الكؤوس وعدد الشخصيات — أغلى الإعلانات لا تذكر أي سكن نادر', cis='حسابات مطوّرة بالكامل: كل الشحنات الفائقة والعملات', cn='المظهر: سكنات متوقفة وسكنات الأبراج والأجنحة؛ رتبة ماستر؛ عمر الحساب', jp='رتبة ماستر، الترتيب الوطني، حسابات المالك الأول', kr='الترتيب الوطني والمكانة؛ مجموعات سكنات ضخمة جداً', tr='عدد الكؤوس وعدد الأزياء، بريد / Supercell ID قابل للنقل', sea='الكؤوس والشخصيات المطوّرة؛ إعلانات كثيرة وأسعار مطلوبة في انخفاض')),
 'vi': dict(title='Giá tài khoản {game} trên thế giới', nav='🌍 Thế giới',
   intro='Giá rao bán trên các chợ công khai ở nhiều quốc gia, tất cả được kiểm tra trong cùng một ngày. Thị trường của bạn hiện trước; phần còn lại cho thấy người chơi nơi khác coi trọng điều gì nhất.',
   your='Thị trường của bạn', others='Thị trường khác', cols=('Thị trường', 'Ở đâu', 'Giá rao bán', '≈ USD', 'Được coi trọng nhất ở đó'),
   nv='Chưa xác minh — các chợ chính ở đó chặn kiểm tra tự động.',
   note='Đây là giá rao bán, không phải giao dịch đã hoàn tất. Quy đổi sang USD theo tỷ giá ngày 25–27/9/2026. Chỉ mang tính mô tả — không phải lời khuyên mua hay bán; mua bán tài khoản có thể vi phạm quy định của trò chơi.',
   checked='Đã kiểm tra',
   reg=dict(global_='Trang toàn cầu / phương Tây', cis='Nga & SNG', cn='Trung Quốc', jp='Nhật Bản', kr='Hàn Quốc', tr='Thổ Nhĩ Kỳ', sea='Đông Nam Á', br='Brazil'),
   dem=dict(global_='Cúp và số brawler — các tin đắt nhất không nhắc skin hiếm nào', cis='Tài khoản full: đủ mọi hypercharge, vàng', cn='Trang phục: skin đã ngừng bán và skin cung hoàng đạo, cánh; hạng Master; tuổi tài khoản', jp='Hạng Master, xếp hạng quốc gia, tài khoản chủ đầu tiên', kr='Xếp hạng quốc gia và prestige; bộ sưu tập skin cực lớn', tr='Số cúp, số trang phục, email / Supercell ID chuyển được', sea='Cúp và brawler full cấp; nhiều tin rao, giá rao đang giảm')),
 'hi': dict(title='दुनिया भर में {game} अकाउंट की कीमतें', nav='🌍 दुनिया',
   intro='अलग-अलग देशों के सार्वजनिक मार्केटप्लेस पर माँगी गई कीमतें, सभी एक ही दिन जाँची गईं। पहले आपका बाज़ार; बाकी दिखाते हैं कि दूसरी जगहों के खिलाड़ी किस चीज़ को सबसे ज़्यादा महत्व देते हैं।',
   your='आपका बाज़ार', others='अन्य बाज़ार', cols=('बाज़ार', 'कहाँ', 'माँगी गई कीमतें', '≈ USD', 'वहाँ सबसे ज़्यादा महत्व'),
   nv='अभी सत्यापित नहीं — वहाँ के मुख्य मार्केटप्लेस स्वचालित जाँच रोकते हैं।',
   note='ये माँगी गई कीमतें हैं, पूरी हुई बिक्री नहीं। 25–27 सितंबर 2026 की दरों पर USD में बदला गया। केवल जानकारी के लिए — खरीदने या बेचने की सलाह नहीं; अकाउंट का लेन-देन गेम के नियमों का उल्लंघन कर सकता है।',
   checked='जाँचा गया',
   reg=dict(global_='वैश्विक / पश्चिमी साइटें', cis='रूस और CIS', cn='चीन', jp='जापान', kr='दक्षिण कोरिया', tr='तुर्किये', sea='दक्षिण-पूर्व एशिया', br='ब्राज़ील'),
   dem=dict(global_='ट्रॉफ़ी और ब्रॉलर की संख्या — सबसे महँगी लिस्टिंग में कोई दुर्लभ स्किन नहीं', cis='पूरी तरह मैक्स अकाउंट: सारे हाइपरचार्ज, कॉइन', cn='कॉस्मेटिक: बंद हो चुकी और ज़ोडिएक स्किन, पंख; मास्टर रैंक; अकाउंट की उम्र', jp='मास्टर रैंक, राष्ट्रीय रैंकिंग, पहले मालिक वाले अकाउंट', kr='राष्ट्रीय रैंकिंग और प्रेस्टीज; बहुत बड़े स्किन संग्रह', tr='ट्रॉफ़ी, कॉस्ट्यूम की संख्या, ट्रांसफ़र होने वाला ईमेल / Supercell ID', sea='ट्रॉफ़ी और मैक्स ब्रॉलर; बहुत लिस्टिंग, माँगी गई कीमतें गिर रही हैं')),
 'fr': dict(title='Prix des comptes {game} dans le monde', nav='🌍 Monde',
   intro='Prix demandés sur des marketplaces publiques de différents pays, tous relevés le même jour. Votre marché d\'abord ; les autres montrent ce que les joueurs d\'ailleurs valorisent le plus.',
   your='Votre marché', others='Autres marchés', cols=('Marché', 'Où', 'Prix demandés', '≈ USD', 'Le plus valorisé là-bas'),
   nv='Pas encore vérifié — les principales plateformes bloquent les vérifications automatiques.',
   note='Prix demandés, pas des ventes conclues. Convertis en USD aux taux du 25–27 septembre 2026. Purement descriptif — ce n\'est pas un conseil d\'achat ou de vente ; le commerce de comptes peut enfreindre les règles du jeu.',
   checked='Vérifié',
   reg=dict(global_='Sites mondiaux / occidentaux', cis='Russie et CEI', cn='Chine', jp='Japon', kr='Corée du Sud', tr='Turquie', sea='Asie du Sud-Est', br='Brésil'),
   dem=dict(global_='Trophées et nombre de brawlers — les annonces les plus chères ne citent aucun skin rare', cis='Comptes au maximum : toutes les hypercharges, pièces', cn='Cosmétiques : skins retirés et du zodiaque, ailes ; rang Maître ; ancienneté du compte', jp='Rang Maître, classement national, comptes de premier propriétaire', kr='Classement national et prestige ; très grandes collections de skins', tr='Trophées, nombre de costumes, e-mail / Supercell ID transférable', sea='Trophées et brawlers au maximum ; beaucoup d\'annonces, prix demandés en baisse')),
 'de': dict(title='Preise für {game}-Konten weltweit', nav='🌍 Welt',
   intro='Angebotspreise auf öffentlichen Marktplätzen in verschiedenen Ländern, alle am selben Tag geprüft. Zuerst dein Markt; die anderen zeigen, was Spieler anderswo am meisten schätzen.',
   your='Dein Markt', others='Andere Märkte', cols=('Markt', 'Wo', 'Gesehene Angebotspreise', '≈ USD', 'Dort am meisten geschätzt'),
   nv='Noch nicht geprüft — die wichtigsten Marktplätze dort blockieren automatische Prüfungen.',
   note='Angebotspreise, keine abgeschlossenen Verkäufe. In USD umgerechnet zu den Kursen vom 25.–27. September 2026. Nur beschreibend — keine Kauf- oder Verkaufsempfehlung; Kontohandel kann gegen die Spielregeln verstoßen.',
   checked='Geprüft',
   reg=dict(global_='Globale / westliche Seiten', cis='Russland & GUS', cn='China', jp='Japan', kr='Südkorea', tr='Türkei', sea='Südostasien', br='Brasilien'),
   dem=dict(global_='Trophäen und Brawler-Anzahl — die teuersten Angebote nennen keinen seltenen Skin', cis='Voll ausgebaute Konten: alle Hypercharges, Münzen', cn='Kosmetik: ausgelaufene und Tierkreis-Skins, Flügel; Meister-Rang; Kontoalter', jp='Meister-Rang, nationales Ranking, Konten aus erster Hand', kr='Nationales Ranking und Prestige; sehr große Skin-Sammlungen', tr='Trophäen, Anzahl der Kostüme, übertragbare E-Mail / Supercell ID', sea='Trophäen und voll ausgebaute Brawler; viele Angebote, sinkende Angebotspreise')),
 'it': dict(title='Prezzi degli account di {game} nel mondo', nav='🌍 Mondo',
   intro='Prezzi richiesti su marketplace pubblici di vari paesi, tutti controllati nello stesso giorno. Prima il tuo mercato; gli altri mostrano ciò che i giocatori altrove apprezzano di più.',
   your='Il tuo mercato', others='Altri mercati', cols=('Mercato', 'Dove', 'Prezzi richiesti', '≈ USD', 'Il più apprezzato lì'),
   nv='Non ancora verificato: i principali marketplace bloccano i controlli automatici.',
   note='Prezzi richiesti, non vendite concluse. Convertiti in USD ai cambi del 25–27 settembre 2026. Solo descrittivo: non è un consiglio di acquisto o vendita; il commercio di account può violare le regole del gioco.',
   checked='Controllato',
   reg=dict(global_='Siti globali / occidentali', cis='Russia e CSI', cn='Cina', jp='Giappone', kr='Corea del Sud', tr='Turchia', sea='Sud-est asiatico', br='Brasile'),
   dem=dict(global_='Trofei e numero di brawler: gli annunci più cari non citano alcuna skin rara', cis='Account al massimo: tutte le ipercariche, monete', cn='Cosmetici: skin ritirate e dello zodiaco, ali; rango Maestro; anzianità dell\'account', jp='Rango Maestro, classifica nazionale, account di primo proprietario', kr='Classifica nazionale e prestigio; collezioni di skin enormi', tr='Trofei, numero di costumi, e-mail / Supercell ID trasferibile', sea='Trofei e brawler al massimo; molti annunci, prezzi richiesti in calo')),
 'ja': dict(title='世界の{game}アカウント価格', nav='🌍 世界',
   intro='各国の公開マーケットプレイスでの出品価格を、すべて同じ日に確認しました。まずあなたの市場、続いて他の国のプレイヤーが最も重視しているものを示します。',
   your='あなたの市場', others='その他の市場', cols=('市場', 'サイト', '出品価格', '≈ USD', 'そこで最も重視されるもの'),
   nv='未確認 — 主要なマーケットプレイスが自動チェックをブロックしています。',
   note='出品価格であり、成立した取引価格ではありません。2026年9月25〜27日のレートでUSDに換算。説明のみを目的としており、売買を勧めるものではありません。アカウント取引はゲームの規約に違反する場合があります。',
   checked='確認日',
   reg=dict(global_='グローバル / 欧米サイト', cis='ロシア・CIS', cn='中国', jp='日本', kr='韓国', tr='トルコ', sea='東南アジア', br='ブラジル'),
   dem=dict(global_='トロフィー数とキャラ数 — 最高額の出品でもレアスキンの記載なし', cis='完全育成アカウント：全ハイパーチャージ、コイン', cn='見た目：販売終了スキン・星座スキン、翼；マスターランク；アカウント歴', jp='マスターランク、国内ランキング、初期所有者アカウント', kr='国内ランキングとプレステージ；非常に多いスキンコレクション', tr='トロフィー数、コスチューム数、移行可能なメール / Supercell ID', sea='トロフィーと育成済みキャラ；出品が多く、出品価格は下落中')),
 'ko': dict(title='세계의 {game} 계정 가격', nav='🌍 세계',
   intro='여러 나라 공개 거래 사이트의 판매 호가를 모두 같은 날 확인했습니다. 먼저 내 시장을, 이어서 다른 나라 플레이어가 가장 중시하는 것을 보여 줍니다.',
   your='내 시장', others='다른 시장', cols=('시장', '거래처', '판매 호가', '≈ USD', '그곳에서 가장 중시되는 것'),
   nv='아직 확인되지 않음 — 주요 거래 사이트가 자동 확인을 차단합니다.',
   note='판매 호가이며 완료된 거래가가 아닙니다. 2026년 9월 25~27일 환율로 USD 환산. 설명용일 뿐 매매 권유가 아니며, 계정 거래는 게임 규정 위반일 수 있습니다.',
   checked='확인일',
   reg=dict(global_='글로벌 / 서구 사이트', cis='러시아·CIS', cn='중국', jp='일본', kr='대한민국', tr='튀르키예', sea='동남아시아', br='브라질'),
   dem=dict(global_='트로피와 브롤러 수 — 최고가 매물에도 희귀 스킨 언급 없음', cis='풀강 계정: 모든 하이퍼차지, 코인', cn='외형: 판매 종료 스킨·별자리 스킨, 날개; 마스터 랭크; 계정 연차', jp='마스터 랭크, 국내 랭킹, 1차 소유 계정', kr='국내 랭킹과 프레스티지; 매우 큰 스킨 컬렉션', tr='트로피 수, 코스튬 수, 이전 가능한 이메일 / Supercell ID', sea='트로피와 만렙 브롤러; 매물이 많고 호가 하락 중')),
 'th': dict(title='ราคาบัญชี {game} ทั่วโลก', nav='🌍 ทั่วโลก',
   intro='ราคาที่ตั้งขายบนตลาดสาธารณะในหลายประเทศ ตรวจสอบทั้งหมดในวันเดียวกัน แสดงตลาดของคุณก่อน ส่วนที่เหลือบอกว่าผู้เล่นที่อื่นให้คุณค่ากับอะไรมากที่สุด',
   your='ตลาดของคุณ', others='ตลาดอื่น', cols=('ตลาด', 'ที่ไหน', 'ราคาที่ตั้งขาย', '≈ USD', 'สิ่งที่มีค่าที่สุดที่นั่น'),
   nv='ยังไม่ได้ตรวจสอบ — ตลาดหลักที่นั่นบล็อกการตรวจสอบอัตโนมัติ',
   note='เป็นราคาที่ตั้งขาย ไม่ใช่ราคาที่ขายได้จริง แปลงเป็น USD ตามอัตราวันที่ 25–27 กันยายน 2026 เพื่อให้ข้อมูลเท่านั้น ไม่ใช่คำแนะนำให้ซื้อหรือขาย การซื้อขายบัญชีอาจผิดกฎของเกม',
   checked='ตรวจสอบ',
   reg=dict(global_='เว็บไซต์ระดับโลก / ตะวันตก', cis='รัสเซียและ CIS', cn='จีน', jp='ญี่ปุ่น', kr='เกาหลีใต้', tr='ตุรกี', sea='เอเชียตะวันออกเฉียงใต้', br='บราซิล'),
   dem=dict(global_='ถ้วยรางวัลและจำนวนตัวละคร — ประกาศที่แพงที่สุดไม่ระบุสกินหายากเลย', cis='บัญชีตันทุกอย่าง: ไฮเปอร์ชาร์จครบ เหรียญ', cn='คอสเมติก: สกินที่เลิกขายและสกินจักรราศี ปีก; แรงค์ Master; อายุบัญชี', jp='แรงค์ Master อันดับในประเทศ บัญชีมือหนึ่ง', kr='อันดับในประเทศและเพรสทีจ; คอลเลกชันสกินขนาดใหญ่มาก', tr='จำนวนถ้วย จำนวนคอสตูม อีเมล / Supercell ID ที่โอนได้', sea='ถ้วยรางวัลและตัวละครตัน; ประกาศเยอะ ราคาตั้งขายกำลังลดลง')),
 'pl': dict(title='Ceny kont {game} na świecie', nav='🌍 Świat',
   intro='Ceny ofertowe na publicznych platformach w różnych krajach, wszystkie sprawdzone tego samego dnia. Najpierw Twój rynek, potem to, co gracze gdzie indziej cenią najbardziej.',
   your='Twój rynek', others='Inne rynki', cols=('Rynek', 'Gdzie', 'Ceny ofertowe', '≈ USD', 'Najbardziej cenione tam'),
   nv='Jeszcze niezweryfikowane — główne platformy blokują automatyczne sprawdzanie.',
   note='Ceny ofertowe, a nie zawarte transakcje. Przeliczone na USD po kursach z 25–27 września 2026. Wyłącznie opis — nie jest to porada kupna ani sprzedaży; handel kontami może łamać zasady gry.',
   checked='Sprawdzono',
   reg=dict(global_='Serwisy globalne / zachodnie', cis='Rosja i WNP', cn='Chiny', jp='Japonia', kr='Korea Południowa', tr='Turcja', sea='Azja Południowo-Wschodnia', br='Brazylia'),
   dem=dict(global_='Trofea i liczba zadymiarzy — najdroższe oferty nie wymieniają żadnej rzadkiej skórki', cis='Konta wymaksowane: wszystkie hiperładunki, monety', cn='Kosmetyka: wycofane i zodiakalne skórki, skrzydła; ranga Mistrz; wiek konta', jp='Ranga Mistrz, ranking krajowy, konta z pierwszej ręki', kr='Ranking krajowy i prestiż; ogromne kolekcje skórek', tr='Liczba trofeów, liczba kostiumów, przenoszalny e-mail / Supercell ID', sea='Trofea i wymaksowani zadymiarze; dużo ofert, ceny ofertowe spadają')),
 'zh': dict(title='全球{game}账号价格', nav='🌍 全球',
   intro='不同国家公开交易平台上的挂售价格，均在同一天核查。先显示您所在的市场，其余展示其他地区玩家最看重什么。',
   your='您的市场', others='其他市场', cols=('市场', '平台', '挂售价格', '≈ 美元', '当地最看重'),
   nv='尚未核实——当地主要平台屏蔽自动核查。',
   note='以上为挂售价格，并非成交价。按2026年9月25–27日汇率折算为美元。仅作描述，不构成买卖建议；账号交易可能违反游戏规则。',
   checked='核查日期',
   reg=dict(global_='全球 / 欧美平台', cis='俄罗斯及独联体', cn='中国', jp='日本', kr='韩国', tr='土耳其', sea='东南亚', br='巴西'),
   dem=dict(global_='奖杯数与英雄数——最高价挂单也未提及任何稀有皮肤', cis='全满账号：全部超级充能、金币', cn='外观：绝版与星座皮肤、翅膀；大师段位；账号年龄', jp='大师段位、全国排名、一手账号', kr='全国排名与荣耀等级；超大皮肤收藏', tr='奖杯数、服装数量、可转移邮箱 / Supercell ID', sea='奖杯与满级英雄；挂单多，挂价下降')),
}

def render(game, lang, game_name):
    t = T[lang]; data = DATA[game]; local = LOCAL[lang]
    reg = lambda k: t['reg']['global_' if k == 'global' else k]
    def dem(k):
        if k is None: return '—'
        key = 'global_' if k == 'global' else k
        return t['dem'][key] if key in t['dem'] else N[lang][k]
    def row(k, mine=False):
        d = data.get(k)
        cls = ' class="wm-mine"' if mine else ''
        head = '<th scope="row"><span class="wm-flag" aria-hidden="true">' + FLAG[k] + '</span>' + reg(k) + (' <span class="wm-you">' + t['your'] + '</span>' if mine else '') + '</th>'
        if d is None:
            return '<tr' + cls + '>' + head + '<td colspan="4" class="wm-nv">' + t['nv'] + '</td></tr>'
        where = ', '.join('<a href="' + u + '" target="_blank" rel="noopener">' + n + '</a>' for n, u in d['where'])
        c = t['cols']
        return ('<tr' + cls + '>' + head + '<td data-l="' + c[1] + '">' + where + '</td><td data-l="' + c[2] + '" class="wm-num">' + d['local'] +
                '</td><td data-l="' + c[3] + '" class="wm-num">' + d['usd'] + '</td><td data-l="' + c[4] + '">' + dem(d['demand']) + '</td></tr>')
    rows = row(local, True) + '<tr class="wm-sep"><td colspan="5">' + t['others'] + '</td></tr>' + ''.join(row(k) for k in ORDER if k != local and k in data)
    c = t['cols']
    return ('<section class="g-card g-news-card g-world"><span id="world" class="anchor-target"></span>\n'
            '<h2>' + t['title'].format(game=game_name) + '</h2>\n'
            '<p class="wm-intro">' + t['intro'] + '</p>\n'
            '<div class="wm-wrap"><table class="wm-table"><thead><tr><th scope="col">' + c[0] + '</th><th scope="col">' + c[1] + '</th><th scope="col">' + c[2] +
            '</th><th scope="col">' + c[3] + '</th><th scope="col">' + c[4] + '</th></tr></thead><tbody>' + rows + '</tbody></table></div>\n'
            '<p class="wm-note">' + t['note'] + ' ' + t['checked'] + ': <time datetime="' + CHECKED + '">' + CHECKED + '</time>.</p>\n' +
            render_extra(game, lang, game_name) + '\n</section>\n')

def apply(game):
    names = {'brawl-stars': 'Brawl Stars', 'roblox': 'Roblox', 'clash-of-clans': 'Clash of Clans', 'clash-royale': 'Clash Royale', 'free-fire': 'Free Fire',
             'genshin-impact': 'Genshin Impact', 'mobile-legends': 'Mobile Legends', 'fortnite': 'Fortnite', 'minecraft': 'Minecraft'}
    n = 0
    for lang in LANGS:
        f = os.path.join(R.ROOT, (lang + '/' if lang != 'en' else '') + game + '.html')
        s = open(f, encoding='utf-8').read()
        s = re.sub(r'<section class="g-card g-news-card g-world">.*?</section>\n', '', s, flags=re.S)   # idempotent
        s = re.sub(r'\s*<a href="#world">[^<]*</a>', '', s)
        block = render(game, lang, names[game])
        i = s.index('<span id="pricing" class="anchor-target"></span>')
        j = s.index('</section>', i) + len('</section>\n')
        s = s[:j] + block + s[j:]
        m = re.search(r'(<div class="section-nav">\s*<a href="#pricing">[^<]*</a>)', s)
        s = s[:m.end()] + '\n  <a href="#world">' + T[lang]['nav'] + '</a>' + s[m.end():]
        open(f, 'w', encoding='utf-8', newline='').write(s)
        n += 1
    print(game, 'pages updated:', n)

if __name__ == '__main__':
    apply(sys.argv[1] if len(sys.argv) > 1 else 'brawl-stars')
