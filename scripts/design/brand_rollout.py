"""Brand pass (owner-approved 2026-09-29 on the ru/brawl-stars sample):
- breadcrumbs "Home › page" replace the "← Back to home" button (+ BreadcrumbList JSON-LD)
- GAV emblem on the homepage robot's chest
- robot note next to every calculator result: why the number is approximate
- Organization logo JSON-LD on the root homepage
Idempotent: pages already carrying .crumbs / .g-why are skipped for that step.
Run from anywhere: python scripts/design/brand_rollout.py"""
import os, re, json, glob, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + os.sep
SITE = 'https://gameaccountvalue.com/'
LANGS = ['en', 'ru', 'es', 'fr', 'pt', 'id', 'ar', 'de', 'tr', 'vi', 'hi', 'it', 'ja', 'ko', 'zh', 'pl', 'th']

HOME = dict(en='Home', ru='Главная', es='Inicio', fr='Accueil', pt='Início', id='Beranda', ar='الرئيسية',
            de='Startseite', tr='Ana Sayfa', vi='Trang chủ', hi='होम', it='Home', ja='ホーム', ko='홈',
            zh='首页', pl='Strona główna', th='หน้าแรก')
CRUMB_LABEL = dict(en='Breadcrumb', ru='Навигационная цепочка', es='Ruta de navegación', fr="Fil d'Ariane",
                   pt='Trilha de navegação', id='Navigasi breadcrumb', ar='مسار التنقل', de='Brotkrumen-Navigation',
                   tr='Gezinme yolu', vi='Đường dẫn điều hướng', hi='ब्रेडक्रंब नेविगेशन', it='Percorso di navigazione',
                   ja='パンくずリスト', ko='탐색 경로', zh='面包屑导航', pl='Ścieżka nawigacji', th='เส้นทางนำทาง')

# Robot note: heading + sentence template with {x} (what the calculator sees) and {y} (what it can't).
WHY_T = {
 'en': ('Why is it approximate?', 'The calculator only sees {x}. It can’t see {y} — the bot counts those from your screenshots.'),
 'ru': ('Почему это примерно?', 'Калькулятор видит только {x}. {Y} он не знает — их по скриншотам учтёт бот.'),
 'es': ('¿Por qué es aproximado?', 'La calculadora solo ve {x}. No puede ver {y}: eso lo tiene en cuenta el bot con tus capturas.'),
 'fr': ('Pourquoi est-ce approximatif ?', 'Le calculateur ne voit que {x}. Il ne voit pas {y} : le bot en tient compte à partir de vos captures d’écran.'),
 'pt': ('Por que é aproximado?', 'A calculadora só vê {x}. Ela não vê {y} — o bot considera isso a partir das suas capturas de tela.'),
 'id': ('Kenapa ini cuma perkiraan?', 'Kalkulator hanya melihat {x}. Kalkulator tidak bisa melihat {y} — bot akan menghitungnya dari screenshot kamu.'),
 'ar': ('لماذا القيمة تقريبية؟', 'الحاسبة ترى فقط {x}. ولا ترى {y} — يأخذها البوت في الحسبان من لقطات الشاشة.'),
 'de': ('Warum nur ungefähr?', 'Der Rechner sieht nur {x}. {Y} sieht er nicht – die berücksichtigt der Bot anhand deiner Screenshots.'),
 'tr': ('Neden yaklaşık?', 'Hesaplayıcı yalnızca {x} görür. {Y} göremez — bunları bot ekran görüntülerinden hesaba katar.'),
 'vi': ('Vì sao chỉ là ước tính?', 'Máy tính chỉ thấy {x}. Nó không thấy {y} — bot sẽ tính những thứ đó từ ảnh chụp màn hình của bạn.'),
 'hi': ('यह सिर्फ़ अनुमान क्यों है?', 'कैलकुलेटर सिर्फ़ {x} देखता है। {y} वह नहीं देख सकता — इन्हें बॉट आपके स्क्रीनशॉट से गिनता है।'),
 'it': ('Perché è approssimativo?', 'Il calcolatore vede solo {x}. Non vede {y}: di questi tiene conto il bot dai tuoi screenshot.'),
 'ja': ('なぜ目安なの？', '計算ツールが見ているのは{x}だけです。{y}は分かりません。これらはボットがスクリーンショットから反映します。'),
 'ko': ('왜 대략적인 값인가요?', '계산기는 {x}만 봅니다. {y} 알 수 없어요. 이런 요소는 봇이 스크린샷으로 반영해요.'),
 'zh': ('为什么只是估算？', '计算器只能看到{x}。它看不到{y}——这些由机器人根据你的截图来计算。'),
 'pl': ('Dlaczego to tylko przybliżenie?', 'Kalkulator widzi tylko {x}. Nie widzi {y} — to uwzględni bot na podstawie Twoich zrzutów ekranu.'),
 'th': ('ทำไมถึงเป็นค่าประมาณ?', 'เครื่องคิดเลขเห็นแค่{x} แต่ไม่เห็น{y} — บอทจะนำไปคิดจากภาพหน้าจอของคุณ'),
}

# (x, y) per game per language. ru: accusative; tr: accusative; pl: x accusative, y genitive;
# de: y is the sentence start (accusative); ko: y carries its topic particle.
XY = {
 'brawl-stars': {
  'en': ('trophies and Power Level 11 brawlers', 'rare skins, hypercharges or your full brawler collection'),
  'ru': ('трофеи и бойцов на Power Level 11', 'редкие скины, гиперзаряды и полноту коллекции бойцов'),
  'es': ('los trofeos y los brawlers a nivel de poder 11', 'las skins raras, las hipercargas ni tu colección completa de brawlers'),
  'fr': ('les trophées et les brawlers au niveau de puissance 11', 'les skins rares, les hypercharges ni votre collection complète de brawlers'),
  'pt': ('troféus e brawlers no nível de poder 11', 'skins raras, hipercargas nem sua coleção completa de brawlers'),
  'id': ('trofi dan brawler Power Level 11', 'skin langka, hypercharge, dan koleksi brawler lengkap'),
  'ar': ('الكؤوس والمقاتلين بمستوى القوة 11', 'السكنات النادرة والشحنات الفائقة (Hypercharge) واكتمال مجموعة المقاتلين'),
  'de': ('Trophäen und Brawler auf Powerlevel 11', 'seltene Skins, Hypercharges und deine komplette Brawler-Sammlung'),
  'tr': ('kupaları ve Güç Seviyesi 11 savaşçıları', 'nadir kostümleri, hiper yükleri ve savaşçı koleksiyonunun tamamını'),
  'vi': ('cúp và số brawler cấp sức mạnh 11', 'skin hiếm, hypercharge và bộ sưu tập brawler đầy đủ'),
  'hi': ('ट्रॉफ़ी और पावर लेवल 11 वाले ब्रॉलर', 'रेयर स्किन, हाइपरचार्ज और पूरा ब्रॉलर कलेक्शन'),
  'it': ('i trofei e i brawler a livello di potenza 11', 'le skin rare, le ipercariche né la tua collezione completa di brawler'),
  'ja': ('トロフィーとパワーレベル11のキャラ数', 'レアスキン、ハイパーチャージ、キャラのコレクション全体'),
  'ko': ('트로피와 파워 레벨 11 브롤러', '희귀 스킨, 하이퍼차지, 브롤러 컬렉션 전체는'),
  'zh': ('奖杯数和11级战力英雄数', '稀有皮肤、超级充能和完整的英雄收藏'),
  'pl': ('trofea i zadymiarzy na poziomie mocy 11', 'rzadkich skórek, hiperładunków ani pełnej kolekcji zadymiarzy'),
  'th': ('ถ้วยรางวัลและบรอว์เลอร์พาวเวอร์เลเวล 11', 'สกินหายาก ไฮเปอร์ชาร์จ และคอลเลกชันบรอว์เลอร์ทั้งหมด'),
 },
 'clash-of-clans': {
  'en': ('Town Hall level and upgrade type', 'hero levels, epic equipment, hero skins or sceneries'),
  'ru': ('уровень Ратуши и тип прокачки', 'уровни героев, эпическое снаряжение, скины героев и декорации'),
  'es': ('el nivel del Ayuntamiento y el tipo de mejora', 'los niveles de los héroes, el equipamiento épico, las skins de héroes ni los escenarios'),
  'fr': ("le niveau de l'hôtel de ville et le type de progression", 'les niveaux des héros, l’équipement épique, les skins de héros ni les décors'),
  'pt': ('o nível do Centro de Vila e o tipo de evolução', 'níveis dos heróis, equipamentos épicos, skins de heróis nem cenários'),
  'id': ('level Town Hall dan jenis upgrade', 'level hero, equipment epik, skin hero, dan scenery'),
  'ar': ('مستوى قاعة البلدة (Town Hall) ونوع الترقية', 'مستويات الأبطال والمعدات الملحمية وسكنات الأبطال والمناظر'),
  'de': ('das Rathaus-Level und den Ausbaustatus', 'Heldenlevel, epische Ausrüstung, Helden-Skins und Szenerien'),
  'tr': ('Belediye Binası seviyesini ve yükseltme türünü', 'kahraman seviyelerini, epik ekipmanları, kahraman kostümlerini ve manzaraları'),
  'vi': ('cấp Nhà Chính và kiểu nâng cấp', 'cấp tướng, trang bị sử thi, skin tướng và phong cảnh'),
  'hi': ('टाउन हॉल लेवल और अपग्रेड टाइप', 'हीरो लेवल, एपिक इक्विपमेंट, हीरो स्किन और सीनरी'),
  'it': ('il livello del Municipio e il tipo di potenziamento', 'i livelli degli eroi, l’equipaggiamento epico, le skin degli eroi né gli scenari'),
  'ja': ('タウンホールのレベルと育成タイプ', 'ヒーローのレベル、エピック装備、ヒーロースキン、景観'),
  'ko': ('마을회관 레벨과 업그레이드 유형', '영웅 레벨, 에픽 장비, 영웅 스킨, 풍경은'),
  'zh': ('大本营等级和升级类型', '英雄等级、史诗装备、英雄皮肤和场景'),
  'pl': ('poziom ratusza i typ rozbudowy', 'poziomów bohaterów, epickiego wyposażenia, skórek bohaterów ani scenerii'),
  'th': ('เลเวลทาวน์ฮอลล์และประเภทการอัปเกรด', 'เลเวลฮีโร่ อุปกรณ์ระดับมหากาพย์ สกินฮีโร่ และฉากหลัง'),
 },
 'clash-royale': {
  'en': ('King Tower level and max-level cards', 'card evolutions, champions or tower skins'),
  'ru': ('уровень King Tower и карты максимального уровня', 'эволюции карт, чемпионов и скины башен'),
  'es': ('el nivel de la Torre del Rey y las cartas al máximo', 'las evoluciones de cartas, los campeones ni las skins de torre'),
  'fr': ('le niveau de la tour du Roi et les cartes au niveau max', 'les évolutions de cartes, les champions ni les skins de tour'),
  'pt': ('o nível da Torre do Rei e as cartas no nível máximo', 'evoluções de cartas, campeões nem skins de torre'),
  'id': ('level King Tower dan kartu level maksimal', 'evolusi kartu, champion, dan skin tower'),
  'ar': ('مستوى برج الملك والبطاقات بأقصى مستوى', 'تطويرات البطاقات والأبطال وسكنات الأبراج'),
  'de': ('das King-Tower-Level und Karten auf Max-Level', 'Kartenentwicklungen, Champions und Turm-Skins'),
  'tr': ('Kral Kulesi seviyesini ve maksimum seviyeli kartları', 'kart evrimlerini, şampiyonları ve kule kostümlerini'),
  'vi': ('cấp Tháp Vua và số thẻ cấp tối đa', 'tiến hóa thẻ, tướng champion và skin tháp'),
  'hi': ('किंग टावर लेवल और मैक्स-लेवल कार्ड', 'कार्ड इवॉल्यूशन, चैंपियन और टावर स्किन'),
  'it': ('il livello della Torre del Re e le carte al massimo', 'le evoluzioni delle carte, i campioni né le skin delle torri'),
  'ja': ('キングタワーのレベルと最大レベルのカード', 'カードの進化、チャンピオン、タワースキン'),
  'ko': ('킹 타워 레벨과 최대 레벨 카드', '카드 진화, 챔피언, 타워 스킨은'),
  'zh': ('国王塔等级和满级卡牌数', '卡牌进化、英雄卡和塔皮肤'),
  'pl': ('poziom Wieży Króla i karty na maksymalnym poziomie', 'ewolucji kart, czempionów ani skórek wież'),
  'th': ('เลเวลคิงทาวเวอร์และการ์ดเลเวลสูงสุด', 'การวิวัฒนาการการ์ด แชมเปี้ยน และสกินป้อม'),
 },
 'free-fire': {
  'en': ('rank and the number of rare bundles and pets', 'evo guns, which bundles exactly, diamonds or an old UID'),
  'ru': ('ранг и число редких бандлов и питомцев', 'эво-оружие, какие именно бандлы, алмазы и старый UID'),
  'es': ('el rango y la cantidad de bundles y mascotas raros', 'las armas evo, qué bundles exactamente, los diamantes ni un UID antiguo'),
  'fr': ('le rang et le nombre de bundles et d’animaux rares', 'les armes évolutives, quels bundles exactement, les diamants ni un ancien UID'),
  'pt': ('o rank e a quantidade de pacotes e pets raros', 'armas evolutivas, quais pacotes exatamente, diamantes nem um UID antigo'),
  'id': ('rank dan jumlah bundle serta pet langka', 'senjata evo, bundle apa saja persisnya, diamond, dan UID lama'),
  'ar': ('الرتبة وعدد الحزم والحيوانات الأليفة النادرة', 'أسلحة Evo وأي حزم بالتحديد والجواهر ورقم UID القديم'),
  'de': ('den Rang und die Zahl seltener Bundles und Pets', 'Evo-Waffen, die genauen Bundles, Diamanten und eine alte UID'),
  'tr': ('rütbeyi ve nadir paket ile evcil hayvan sayısını', 'evo silahları, tam olarak hangi paketler olduğunu, elmasları ve eski UID’yi'),
  'vi': ('rank và số gói đồ, thú cưng hiếm', 'súng tiến hóa, cụ thể là gói nào, kim cương và UID cũ'),
  'hi': ('रैंक और रेयर बंडल/पेट की संख्या', 'इवो गन, कौन-से बंडल हैं, डायमंड और पुराना UID'),
  'it': ('il grado e il numero di bundle e pet rari', 'le armi evo, quali bundle esattamente, i diamanti né un UID vecchio'),
  'ja': ('ランクとレアバンドル・ペットの数', 'エボ武器、どのバンドルか、ダイヤ、古いUID'),
  'ko': ('랭크와 희귀 번들·펫 수', '진화 무기, 정확히 어떤 번들인지, 다이아, 오래된 UID는'),
  'zh': ('段位和稀有礼包/宠物数量', '进化武器、具体是哪些礼包、钻石和老UID'),
  'pl': ('rangę i liczbę rzadkich pakietów i zwierzaków', 'broni evo, konkretnych pakietów, diamentów ani starego UID'),
  'th': ('แรงก์และจำนวนบันเดิลกับสัตว์เลี้ยงหายาก', 'ปืนอีโว บันเดิลที่มีจริง ๆ เพชร และ UID เก่า'),
 },
 'genshin-impact': {
  'en': ('the number of 5★ characters and C6 characters', 'which characters and weapons exactly, artifacts or Adventure Rank'),
  'ru': ('число 5★ персонажей и персонажей с C6', 'каких именно персонажей и оружие, артефакты и ранг приключений'),
  'es': ('la cantidad de personajes 5★ y de personajes C6', 'qué personajes y armas exactamente, los artefactos ni el rango de aventura'),
  'fr': ('le nombre de personnages 5★ et de personnages C6', 'quels personnages et armes exactement, les artefacts ni le rang d’aventure'),
  'pt': ('a quantidade de personagens 5★ e com C6', 'quais personagens e armas exatamente, artefatos nem o Nível de Aventura'),
  'id': ('jumlah karakter 5★ dan karakter C6', 'karakter dan senjata apa persisnya, artefak, dan Adventure Rank'),
  'ar': ('عدد شخصيات 5★ والشخصيات بمستوى C6', 'أي شخصيات وأسلحة بالتحديد والآثار ورتبة المغامرة'),
  'de': ('die Zahl der 5★-Charaktere und der C6-Charaktere', 'Die genauen Charaktere und Waffen, Artefakte und den Abenteuerrang'),
  'tr': ('5★ karakter ve C6 karakter sayısını', 'tam olarak hangi karakter ve silahlar olduğunu, eserleri ve Macera Rütbesini'),
  'vi': ('số nhân vật 5★ và nhân vật C6', 'cụ thể là nhân vật, vũ khí nào, thánh di vật và Hạng Mạo Hiểm'),
  'hi': ('5★ कैरेक्टर और C6 कैरेक्टर की संख्या', 'कौन-से कैरेक्टर और हथियार हैं, आर्टिफ़ैक्ट और एडवेंचर रैंक'),
  'it': ('il numero di personaggi 5★ e di personaggi C6', 'quali personaggi e armi esattamente, i manufatti né il grado avventura'),
  'ja': ('★5キャラと完凸（C6）キャラの数', 'どのキャラ・武器か、聖遺物、冒険ランク'),
  'ko': ('5성 캐릭터와 6돌(C6) 캐릭터 수', '정확히 어떤 캐릭터와 무기인지, 성유물, 모험 등급은'),
  'zh': ('五星角色数和满命（C6）角色数', '具体是哪些角色和武器、圣遗物和冒险等级'),
  'pl': ('liczbę postaci 5★ i postaci z C6', 'konkretnych postaci i broni, artefaktów ani rangi przygody'),
  'th': ('จำนวนตัวละคร 5★ และตัวละคร C6', 'ตัวละครและอาวุธที่มีจริง ๆ อาร์ติแฟกต์ และแรงก์การผจญภัย'),
 },
 'mobile-legends': {
  'en': ('total skins and rank', 'which skins exactly (Legend, Collector, limited) or your number of heroes'),
  'ru': ('общее число скинов и ранг', 'какие именно скины (Legend, Collector, лимитированные) и число героев'),
  'es': ('el total de skins y el rango', 'qué skins exactamente (Legend, Collector, limitadas) ni tu número de héroes'),
  'fr': ('le nombre total de skins et le rang', 'quels skins exactement (Legend, Collector, limités) ni votre nombre de héros'),
  'pt': ('o total de skins e o rank', 'quais skins exatamente (Legend, Collector, limitadas) nem sua quantidade de heróis'),
  'id': ('total skin dan rank', 'skin apa persisnya (Legend, Collector, limited) dan jumlah hero'),
  'ar': ('إجمالي السكنات والرتبة', 'أي سكنات بالتحديد (Legend وCollector والمحدودة) وعدد الأبطال'),
  'de': ('die Gesamtzahl der Skins und den Rang', 'Die genauen Skins (Legend, Collector, limitierte) und die Zahl deiner Helden'),
  'tr': ('toplam kostüm sayısını ve rütbeyi', 'tam olarak hangi kostümler olduğunu (Legend, Collector, sınırlı) ve kahraman sayını'),
  'vi': ('tổng số skin và rank', 'cụ thể là skin nào (Legend, Collector, giới hạn) và số tướng'),
  'hi': ('कुल स्किन और रैंक', 'कौन-सी स्किन हैं (Legend, Collector, लिमिटेड) और हीरो की संख्या'),
  'it': ('il totale delle skin e il grado', 'quali skin esattamente (Legend, Collector, limitate) né il numero di eroi'),
  'ja': ('スキンの総数とランク', 'どのスキンか（Legend、Collector、限定）とヒーロー数'),
  'ko': ('전체 스킨 수와 랭크', '정확히 어떤 스킨인지(Legend, Collector, 한정)와 영웅 수는'),
  'zh': ('皮肤总数和段位', '具体是哪些皮肤（Legend、Collector、限定）和英雄数量'),
  'pl': ('łączną liczbę skórek i rangę', 'konkretnych skórek (Legend, Collector, limitowanych) ani liczby bohaterów'),
  'th': ('จำนวนสกินทั้งหมดและแรงก์', 'สกินที่มีจริง ๆ (Legend, Collector, ลิมิเต็ด) และจำนวนฮีโร่'),
 },
 'fortnite': {
  'en': ('total skins, rare OG items and seven named skins', 'other rare skins, pickaxes, emotes or V-Bucks'),
  'ru': ('общее число скинов, редкие OG-предметы и семь именных скинов', 'другие редкие скины, кирки, эмоции и V-Bucks'),
  'es': ('el total de skins, los objetos OG raros y siete skins concretas', 'otras skins raras, picos, gestos ni paVos'),
  'fr': ('le nombre total de skins, les objets OG rares et sept skins précis', 'les autres skins rares, pioches, emotes ni les V-bucks'),
  'pt': ('o total de skins, os itens OG raros e sete skins específicas', 'outras skins raras, picaretas, gestos nem V-Bucks'),
  'id': ('total skin, item OG langka, dan tujuh skin tertentu', 'skin langka lain, pickaxe, emote, dan V-Bucks'),
  'ar': ('إجمالي السكنات والعناصر OG النادرة وسبعة سكنات محددة', 'السكنات النادرة الأخرى والفؤوس والرقصات وV-Bucks'),
  'de': ('die Gesamtzahl der Skins, seltene OG-Items und sieben bestimmte Skins', 'Andere seltene Skins, Spitzhacken, Emotes und V-Bucks'),
  'tr': ('toplam kostüm sayısını, nadir OG eşyaları ve yedi belirli kostümü', 'diğer nadir kostümleri, kazmaları, ifadeleri ve V-Papel’i'),
  'vi': ('tổng số skin, vật phẩm OG hiếm và bảy skin cụ thể', 'skin hiếm khác, cuốc, biểu cảm và V-Bucks'),
  'hi': ('कुल स्किन, रेयर OG आइटम और सात ख़ास स्किन', 'दूसरी रेयर स्किन, पिकैक्स, इमोट और V-Bucks'),
  'it': ('il totale delle skin, gli oggetti OG rari e sette skin precise', 'altre skin rare, picconi, emote né i V-buck'),
  'ja': ('スキンの総数、レアなOGアイテム、指定の7スキン', 'ほかのレアスキン、ツルハシ、エモート、V-Bucks'),
  'ko': ('전체 스킨 수, 희귀 OG 아이템, 지정된 스킨 7종', '다른 희귀 스킨, 곡괭이, 이모트, V-Bucks는'),
  'zh': ('皮肤总数、稀有OG物品和七款指定皮肤', '其他稀有皮肤、镐、表情和V币'),
  'pl': ('łączną liczbę skórek, rzadkie przedmioty OG i siedem konkretnych skórek', 'innych rzadkich skórek, kilofów, emotek ani V-dolców'),
  'th': ('จำนวนสกินทั้งหมด ไอเทม OG หายาก และสกินที่ระบุ 7 ตัว', 'สกินหายากอื่น ๆ พลั่ว อีโมต และ V-Bucks'),
 },
 'minecraft': {
  'en': ('the account type', 'the exact username, other capes or the account’s history'),
  'ru': ('тип аккаунта', 'конкретный ник, другие плащи и историю аккаунта'),
  'es': ('el tipo de cuenta', 'el nombre de usuario exacto, otras capas ni el historial de la cuenta'),
  'fr': ('le type de compte', 'le pseudo exact, les autres capes ni l’historique du compte'),
  'pt': ('o tipo de conta', 'o nome de usuário exato, outras capas nem o histórico da conta'),
  'id': ('jenis akun', 'username persisnya, cape lain, dan riwayat akun'),
  'ar': ('نوع الحساب', 'اسم المستخدم بالتحديد والعباءات الأخرى وتاريخ الحساب'),
  'de': ('den Kontotyp', 'Den genauen Namen, weitere Umhänge und die Kontohistorie'),
  'tr': ('hesap türünü', 'tam kullanıcı adını, diğer pelerinleri ve hesap geçmişini'),
  'vi': ('loại tài khoản', 'tên người dùng cụ thể, các áo choàng khác và lịch sử tài khoản'),
  'hi': ('अकाउंट का टाइप', 'असली यूज़रनेम, दूसरी केप और अकाउंट की हिस्ट्री'),
  'it': ('il tipo di account', 'il nome utente preciso, altri mantelli né la storia dell’account'),
  'ja': ('アカウントの種類', '実際のユーザー名、ほかのマント、アカウントの履歴'),
  'ko': ('계정 유형', '정확한 닉네임, 다른 망토, 계정 이력은'),
  'zh': ('账号类型', '具体用户名、其他披风和账号历史'),
  'pl': ('typ konta', 'konkretnej nazwy użytkownika, innych peleryn ani historii konta'),
  'th': ('ประเภทบัญชี', 'ชื่อผู้ใช้จริง เสื้อคลุมอื่น ๆ และประวัติบัญชี'),
 },
 'roblox': {
  'en': ('account age, Robux, common Limiteds and three named rares', 'Dominus and other rare Limiteds, a short username or Premium'),
  'ru': ('возраст аккаунта, Robux, обычные Limited и три именных редких предмета', 'Dominus и другие редкие Limited, короткий ник и Premium'),
  'es': ('la antigüedad, los Robux, los Limited comunes y tres raros con nombre', 'los Dominus y otros Limited raros, un nombre corto ni Premium'),
  'fr': ('l’ancienneté, les Robux, les Limited courants et trois rares nommés', 'les Dominus et autres Limited rares, un pseudo court ni Premium'),
  'pt': ('a idade da conta, os Robux, os Limited comuns e três raros nomeados', 'Dominus e outros Limited raros, um nome curto nem Premium'),
  'id': ('usia akun, Robux, Limited biasa, dan tiga item langka bernama', 'Dominus dan Limited langka lain, username pendek, dan Premium'),
  'ar': ('عمر الحساب وRobux وعناصر Limited العادية وثلاثة عناصر نادرة مسماة', 'Dominus وعناصر Limited النادرة الأخرى والاسم القصير وPremium'),
  'de': ('Kontoalter, Robux, gewöhnliche Limiteds und drei namhafte Rares', 'Dominus und andere seltene Limiteds, einen kurzen Namen und Premium'),
  'tr': ('hesap yaşını, Robux’u, sıradan Limited’leri ve üç isimli nadir eşyayı', 'Dominus ve diğer nadir Limited’leri, kısa kullanıcı adını ve Premium’u'),
  'vi': ('tuổi acc, Robux, vật phẩm Limited thường và ba món hiếm có tên', 'Dominus và các Limited hiếm khác, tên ngắn và Premium'),
  'hi': ('अकाउंट की उम्र, Robux, आम Limited और तीन नामी रेयर आइटम', 'Dominus और दूसरे रेयर Limited, छोटा यूज़रनेम और Premium'),
  'it': ('l’anzianità, i Robux, i Limited comuni e tre rari con nome', 'i Dominus e altri Limited rari, un nome breve né il Premium'),
  'ja': ('アカウントの年数、Robux、一般的なLimited、名前付きレア3種', 'Dominusなどのレアな Limited、短いユーザー名、Premium'),
  'ko': ('계정 연식, Robux, 일반 Limited, 네임드 희귀 아이템 3종', 'Dominus 등 다른 희귀 Limited, 짧은 닉네임, Premium은'),
  'zh': ('账号年龄、Robux、普通Limited和三件知名稀有道具', 'Dominus等其他稀有Limited、短用户名和Premium'),
  'pl': ('wiek konta, Robux, zwykłe przedmioty Limited i trzy rzadkie z nazwą', 'Dominusów i innych rzadkich Limited, krótkiej nazwy ani Premium'),
  'th': ('อายุบัญชี Robux ไอเทม Limited ทั่วไป และของหายากที่มีชื่อ 3 ชิ้น', 'Dominus และ Limited หายากอื่น ๆ ชื่อสั้น และ Premium'),
 },
 # homepage calculator switches games, so it gets a general note
 '_home': {
  'en': ('a few basic numbers for each game', 'your rare items, skins, heroes or upgrades'),
  'ru': ('несколько базовых цифр по каждой игре', 'твои редкие предметы, скины, героев и прокачку'),
  'es': ('unos pocos datos básicos de cada juego', 'tus objetos raros, skins, héroes ni mejoras'),
  'fr': ('quelques chiffres de base pour chaque jeu', 'vos objets rares, skins, héros ni progression'),
  'pt': ('alguns números básicos de cada jogo', 'seus itens raros, skins, heróis nem evoluções'),
  'id': ('beberapa angka dasar untuk tiap game', 'item langka, skin, hero, dan upgrade kamu'),
  'ar': ('بعض الأرقام الأساسية لكل لعبة', 'عناصرك النادرة وسكناتك وأبطالك وترقياتك'),
  'de': ('ein paar Grundwerte pro Spiel', 'Deine seltenen Items, Skins, Helden und Upgrades'),
  'tr': ('her oyun için birkaç temel değeri', 'nadir eşyalarını, kostümlerini, kahramanlarını ve yükseltmelerini'),
  'vi': ('vài con số cơ bản của mỗi game', 'vật phẩm hiếm, skin, tướng và mức nâng cấp của bạn'),
  'hi': ('हर गेम के कुछ बुनियादी आंकड़े', 'आपके रेयर आइटम, स्किन, हीरो और अपग्रेड'),
  'it': ('pochi dati di base per ogni gioco', 'i tuoi oggetti rari, skin, eroi né potenziamenti'),
  'ja': ('各ゲームのいくつかの基本的な数値', 'レアアイテム、スキン、キャラ、育成状況'),
  'ko': ('게임별 기본 수치 몇 가지', '희귀 아이템, 스킨, 영웅, 육성 상태는'),
  'zh': ('每款游戏的几个基础数值', '你的稀有物品、皮肤、英雄和养成情况'),
  'pl': ('kilka podstawowych liczb dla każdej gry', 'Twoich rzadkich przedmiotów, skórek, bohaterów ani rozbudowy'),
  'th': ('ตัวเลขพื้นฐานไม่กี่อย่างของแต่ละเกม', 'ไอเทมหายาก สกิน ฮีโร่ และการอัปเกรดของคุณ'),
 },
}

MINI_BOT = ('<svg viewBox="0 0 64 72" aria-hidden="true">'
            '<line x1="32" y1="3" x2="32" y2="12" stroke="#00F0FF" stroke-width="2"/>'
            '<circle cx="32" cy="4" r="3" fill="#FF2E88"/>'
            '<rect x="9" y="12" width="46" height="32" rx="11" fill="#15132E" stroke="#00F0FF" stroke-width="2"/>'
            '<rect x="15" y="19" width="34" height="13" rx="6.5" fill="#05121A" stroke="#00F0FF" stroke-width="1.5"/>'
            '<rect x="20" y="22" width="9" height="7" rx="2" fill="#FCEE0A"/>'
            '<rect x="35" y="22" width="9" height="7" rx="2" fill="#FCEE0A"/>'
            '<path d="M26 38h12" stroke="#00F0FF" stroke-width="2" stroke-linecap="round"/>'
            '<path d="M4 72c2-14 12-22 28-22s26 8 28 22z" fill="#15132E" stroke="#00F0FF" stroke-width="2"/>'
            '<image href="{P}assets/emblem.webp" x="19" y="49" width="26" height="26"/>'
            '</svg>')

ROBOT_LINE = '<path d="M150 470h160" stroke="#FCEE0A" stroke-width="4"/>'
ROBOT_TEXT = '<text x="230" y="505" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="14" fill="#00F0FF" letter-spacing="3">GAV-AI</text>'
ROBOT_EMBLEM = ('<rect x="196" y="436" width="68" height="68" rx="14" fill="#080B11" stroke="#00F0FF" stroke-opacity=".6" stroke-width="2"/>'
                '<image href="{P}assets/emblem.webp" x="200" y="440" width="60" height="60"/>')
ROBOT_TEXT_NEW = '<text x="310" y="480" text-anchor="start" font-family="JetBrains Mono, monospace" font-size="14" fill="#00F0FF" letter-spacing="3">GAV-AI</text>'

GAME_NAMES = {'brawl-stars': 'Brawl Stars', 'clash-of-clans': 'Clash of Clans', 'clash-royale': 'Clash Royale',
              'free-fire': 'Free Fire', 'genshin-impact': 'Genshin Impact', 'mobile-legends': 'Mobile Legends',
              'fortnite': 'Fortnite', 'minecraft': 'Minecraft', 'roblox': 'Roblox'}


def why_html(lang, key, prefix):
    head, tpl = WHY_T[lang]
    x, y = XY[key][lang]
    body = tpl.replace('{x}', x).replace('{Y}', y[:1].upper() + y[1:]).replace('{y}', y)
    return ('<div class="g-why">' + MINI_BOT.replace('{P}', prefix) + '<p><strong>' + head + '</strong>' + body + '</p></div>')


def page_name(s, slug):
    if slug in GAME_NAMES:
        return GAME_NAMES[slug]
    t = re.search(r'<title>([^<|]+)', s).group(1).strip()
    return re.split(r'[:：]', t)[0].strip()


def process(path):
    rel = os.path.relpath(path, ROOT).replace('\\', '/')
    parts = rel.split('/')
    lang = parts[0] if len(parts) == 2 else 'en'
    if lang not in LANGS:  # old-format locales: only the homepage robot
        s = open(path, encoding='utf-8').read()
        if ROBOT_LINE in s:
            s = s.replace(ROBOT_LINE, ROBOT_EMBLEM.replace('{P}', '../'), 1).replace(ROBOT_TEXT, ROBOT_TEXT_NEW, 1)
            open(path, 'w', encoding='utf-8', newline='').write(s)
            return ['robot']
        return []
    prefix = '../' if len(parts) == 2 else ''
    slug = parts[-1][:-5]
    s = open(path, encoding='utf-8').read()
    orig, done = s, []
    base = SITE + ('' if lang == 'en' else lang + '/')

    # 1. breadcrumbs
    m = re.search(r'<div class="back-btn"><a href="([^"]*)">[^<]*</a></div>', s)
    if m and 'class="crumbs"' not in s:
        items = [(HOME[lang], './', base)]
        if slug.endswith('-news'):
            g = slug[:-5]
            items.append((GAME_NAMES[g], './' + g + '.html', base + g + '.html'))
        cur = page_name(s, slug)
        if slug.endswith('-news'):
            cur = re.sub(r'^' + re.escape(GAME_NAMES[slug[:-5]]) + r'\s*', '', cur) or cur
        li = []
        for i, (name, href, _) in enumerate(items):
            icon = '<img src="' + prefix + 'assets/emblem.webp" alt="" width="22" height="22">' if i == 0 else ''
            li.append('<li><a href="' + href + '">' + icon + name + '</a></li>')
        li.append('<li aria-current="page">' + cur + '</li>')
        s = s.replace(m.group(0), '<nav class="crumbs" aria-label="' + CRUMB_LABEL[lang] + '"><ol>' + ''.join(li) + '</ol></nav>', 1)
        ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement":
              [{"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, _, u) in enumerate(items)] +
              [{"@type": "ListItem", "position": len(items) + 1, "name": cur}]}
        s = s.replace('</head>', '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + '</script>\n</head>', 1)
        done.append('crumbs')

    # 2. robot note next to the calculator result
    if 'class="g-actions"' in s and 'class="g-why"' not in s:
        key = slug if slug in XY else ('_home' if slug == 'index' else None)
        if key:
            s = s.replace('<div class="g-actions">', why_html(lang, key, prefix) + '<div class="g-actions">', 1)
            done.append('why')

    # 3. emblem on the homepage robot
    if ROBOT_LINE in s:
        s = s.replace(ROBOT_LINE, ROBOT_EMBLEM.replace('{P}', prefix), 1).replace(ROBOT_TEXT, ROBOT_TEXT_NEW, 1)
        done.append('robot')

    if s != orig:
        open(path, 'w', encoding='utf-8', newline='').write(s)
    return done


def org_logo():
    p = ROOT + 'index.html'
    s = open(p, encoding='utf-8').read()
    if '"#organization"' in s:
        return
    ld = {"@context": "https://schema.org", "@type": "Organization", "@id": SITE + "#organization",
          "name": "GameAccountValue", "url": SITE, "logo": SITE + "favicon-192.png",
          "sameAs": ["https://t.me/GameAccountValue_Bot"]}
    s = s.replace('</head>', '<script type="application/ld+json">' + json.dumps(ld) + '</script>\n</head>', 1)
    open(p, 'w', encoding='utf-8', newline='').write(s)


if __name__ == '__main__':
    files = subprocess.run(['git', 'ls-files', '*.html'], cwd=ROOT, capture_output=True, text=True).stdout.split()
    tally = {}
    for f in files:
        if f.startswith('scripts/'):
            continue
        for d in process(ROOT + f):
            tally[d] = tally.get(d, 0) + 1
    org_logo()
    print(tally)
