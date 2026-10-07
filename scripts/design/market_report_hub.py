"""Market report as a short card hub (2026-10-07) for the 13 languages that still carried the old long-form
report (es tr ar vi hi fr de it ja ko th pl zh). The long form repeated the game pages and drifted out of date;
the hub only links to them, with the same headline figures the game pages and the English hub show.
Keeps each page's own shell (head, menu, footer); replaces <main>, the meta description and drops the FAQPage
node from JSON-LD (its questions are no longer on the page). Idempotent.
Run: python scripts/design/market_report_hub.py
"""
import io, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + os.sep
ICON = {'roblox': '🟦', 'brawl-stars': '🐻', 'clash-of-clans': '⚔️', 'clash-royale': '🃏', 'free-fire': '🔫',
        'genshin-impact': '⚗️', 'mobile-legends': '🏆', 'fortnite': '🌀', 'minecraft': '⛏️'}
NAME = {'roblox': 'Roblox', 'brawl-stars': 'Brawl Stars', 'clash-of-clans': 'Clash of Clans', 'clash-royale': 'Clash Royale',
        'free-fire': 'Free Fire', 'genshin-impact': 'Genshin Impact', 'mobile-legends': 'Mobile Legends',
        'fortnite': 'Fortnite', 'minecraft': 'Minecraft'}
# headline figures: the same as market-report.html (English) and each game page's own range, 2026-10-07
RANGE = {'brawl-stars': ('3', '300+'), 'clash-of-clans': ('10', '260'), 'clash-royale': ('0.50', '600+'),
         'free-fire': ('0.73', '755'), 'mobile-legends': ('0.50', '2500'), 'fortnite': ('10.90', '6200'),
         'minecraft': ('0.50', '200000')}
# number style per language: (decimal mark, thousands mark, '$' before the number?)
FMT = {'es': (',', '.', True), 'tr': (',', '.', False), 'ar': ('.', ',', False), 'vi': ('.', ',', True), 'hi': ('.', ',', True),
       'fr': (',', ' ', False), 'de': (',', '.', False), 'it': (',', '.', False), 'ja': ('.', ',', True), 'ko': ('.', ',', True),
       'th': ('.', ',', True), 'pl': (',', ' ', False), 'zh': ('.', ',', True)}
SUFFIX = {'tr': ' $', 'ar': '$', 'fr': ' $', 'de': ' $', 'it': '$', 'pl': '$'}

T = {
 'es': dict(
  lead='Rangos de precios reales de mercado para 9 juegos — con fuentes, no al azar. Elige un juego para ver el desglose completo: datos, tramos de precio, casos documentados, qué determina el valor y riesgos de estafa.',
  compiled='Elaborado en septiembre de 2026 a partir de listados públicos de mercados y reportes documentados de jugadores.',
  cards=['Existe un mercado real — y el valor también está en las colecciones de objetos.', 'Cuentas al máximo frente a listados de progreso medio.', 'El precio depende casi por completo del nivel del Ayuntamiento y de las mejoras de héroes.', 'El nivel de las cartas y la preparación para torneos marcan el precio.', 'El rango y las colecciones de paquetes y mascotas raras fijan el tramo de precio.', 'Existe un mercado real, con una categoría propia de cuentas «ballena».', 'El precio depende casi por completo de la rareza de los aspectos.', 'El rango real frente a los viejos titulares de «cuentas de $90K».', 'El único juego con un mercado real de nombres de usuario raros.'],
  top='Mayor colección: {v}', upto='Hasta {v}', read='Leer el informe completo →', about_h='Sobre este informe',
  about_p='El informe completo de cada juego enumera sus propias fuentes: listados de mercados, rastreadores de jugadores del sector y casos documentados. Las cifras son precios solicitados y casos autoreportados, no ventas auditadas.',
  desc='Rangos de precios reales de mercado para Roblox, Genshin Impact, Fortnite, Minecraft y 5 juegos más. Elige un juego para ver el desglose completo — con fuentes, no al azar.'),
 'tr': dict(
  lead='9 oyun için gerçek pazar fiyat aralıkları — tahmin değil, kaynaklı. Tam döküm için aşağıdan bir oyun seç: veriler, fiyat kademeleri, belgelenmiş örnekler, değeri belirleyenler ve dolandırıcılık riskleri.',
  compiled='Eylül 2026’da herkese açık pazar yeri ilanlarından ve belgelenmiş oyuncu bildirimlerinden derlendi.',
  cards=['Gerçek bir pazar var — değer ayrıca koleksiyon eşyalarında duruyor.', 'Tam gelişmiş hesaplar ile orta seviye ilanlar.', 'Fiyat neredeyse tamamen Belediye Binası seviyesine ve kahraman geliştirmelerine bağlı.', 'Kart seviyeleri ve turnuvaya hazır olma fiyatı belirliyor.', 'Rütbe ile nadir paket ve evcil hayvan koleksiyonu fiyat kademesini belirliyor.', 'Gerçek bir pazar var; «balina» hesaplar için ayrı bir kategori de mevcut.', 'Fiyat neredeyse tamamen görünümlerin nadirliğine bağlı.', 'Gerçek aralık ile eski «90 bin dolarlık hesap» başlıkları.', 'Gerçek bir nadir kullanıcı adı pazarı olan tek oyun.'],
  top='En büyük koleksiyon: {v}', upto='En fazla {v}', read='Raporun tamamını oku →', about_h='Bu rapor hakkında',
  about_p='Her oyunun tam raporu kendi kaynaklarını listeler: pazar yeri ilanları, sektörün oyuncu sayısı takipçileri ve belgelenmiş örnekler. Rakamlar istenen fiyatlar ve kişilerin kendi bildirdiği örneklerdir, denetlenmiş satışlar değildir.',
  desc='Roblox, Genshin Impact, Fortnite, Minecraft ve 5 oyun daha için gerçek pazar fiyat aralıkları. Tam döküm için bir oyun seç — tahmin değil, kaynaklı.'),
 'ar': dict(
  lead='نطاقات أسعار حقيقية من الأسواق لتسع ألعاب — بمصادر لا بتخمين. اختر لعبة أدناه للتفاصيل الكاملة: حقائق، وشرائح أسعار، وحالات موثّقة، وما يحدد القيمة، ومخاطر الاحتيال.',
  compiled='أُعدّ في سبتمبر 2026 من إعلانات عامة في الأسواق وتقارير موثّقة من اللاعبين.',
  cards=['يوجد سوق حقيقي — والقيمة موجودة أيضًا في مقتنيات هواة الجمع.', 'حسابات مطوَّرة بالكامل مقابل إعلانات لحسابات متوسطة التقدّم.', 'السعر يعتمد تقريبًا بالكامل على مستوى قاعة البلدة وترقيات الأبطال.', 'اكتمال ترقية البطاقات والجاهزية للبطولات يحددان السعر.', 'الرتبة ومجموعات الحزم والحيوانات الأليفة النادرة تحدد شريحة السعر.', 'يوجد سوق حقيقي، وفيه فئة خاصة بحسابات «الحيتان».', 'السعر يعتمد تقريبًا بالكامل على ندرة المظاهر.', 'النطاق الحقيقي مقابل عناوين قديمة عن «حسابات بـ90 ألف دولار».', 'اللعبة الوحيدة التي لها سوق حقيقي لأسماء المستخدمين النادرة.'],
  top='أكبر مجموعة مقتنيات: {v}', upto='حتى {v}', read='اقرأ التقرير الكامل ←', about_h='عن هذا التقرير',
  about_p='التقرير الكامل لكل لعبة يذكر مصادره: إعلانات الأسواق، ومواقع تتبّع أعداد اللاعبين، والحالات الموثّقة. الأرقام أسعار مطلوبة وحالات أعلنها أصحابها، وليست مبيعات مدقّقة.',
  desc='نطاقات أسعار حقيقية من الأسواق لـRoblox وGenshin Impact وFortnite وMinecraft وخمس ألعاب أخرى. اختر لعبة للتفاصيل الكاملة — بمصادر لا بتخمين.'),
 'vi': dict(
  lead='Khoảng giá thị trường thực tế của 9 game — có nguồn, không đoán mò. Chọn một game bên dưới để xem phân tích đầy đủ: số liệu, các mức giá, trường hợp được ghi nhận, yếu tố quyết định giá trị và rủi ro lừa đảo.',
  compiled='Tổng hợp tháng 9/2026 từ các tin đăng công khai trên chợ giao dịch và báo cáo có ghi nhận của người chơi.',
  cards=['Có chợ giao dịch thực sự — giá trị còn nằm ở bộ sưu tập vật phẩm.', 'Tài khoản nâng tối đa so với các tin đăng tiến độ trung bình.', 'Giá gần như phụ thuộc hoàn toàn vào cấp Town Hall và mức nâng cấp tướng.', 'Mức nâng cấp thẻ bài và độ sẵn sàng thi đấu quyết định giá.', 'Hạng và bộ sưu tập gói đồ, thú cưng hiếm quyết định mức giá.', 'Có chợ giao dịch thực sự, kể cả mục riêng cho tài khoản «cá voi».', 'Giá gần như phụ thuộc hoàn toàn vào độ hiếm của skin.', 'Khoảng giá thực tế so với các tiêu đề cũ về «tài khoản 90 nghìn đô».', 'Game duy nhất có thị trường tên người dùng hiếm thực sự.'],
  top='Bộ sưu tập lớn nhất: {v}', upto='Lên tới {v}', read='Đọc báo cáo đầy đủ →', about_h='Về báo cáo này',
  about_p='Báo cáo đầy đủ của từng game liệt kê nguồn riêng: tin đăng trên chợ giao dịch, các trang theo dõi số người chơi trong ngành và các trường hợp được ghi nhận. Các con số là giá rao bán và trường hợp do người chơi tự công bố, không phải giao dịch đã kiểm toán.',
  desc='Khoảng giá thị trường thực tế cho Roblox, Genshin Impact, Fortnite, Minecraft và 5 game khác. Chọn một game để xem phân tích đầy đủ — có nguồn, không đoán mò.'),
 'hi': dict(
  lead='9 गेम की असली मार्केट प्राइस रेंज — स्रोतों के साथ, अंदाज़े से नहीं। पूरी जानकारी के लिए नीचे कोई गेम चुनें: तथ्य, प्राइस टियर, दर्ज किए गए मामले, वैल्यू तय करने वाली बातें और स्कैम के जोखिम।',
  compiled='सितंबर 2026 में सार्वजनिक मार्केटप्लेस लिस्टिंग और खिलाड़ियों की दर्ज रिपोर्टों से तैयार।',
  cards=['असली मार्केटप्लेस मौजूद है — वैल्यू कलेक्टर आइटम में भी बसती है।', 'पूरी तरह मैक्स अकाउंट बनाम मध्यम प्रगति वाली लिस्टिंग।', 'कीमत लगभग पूरी तरह Town Hall लेवल और हीरो अपग्रेड पर निर्भर है।', 'कार्ड अपग्रेड कितने पूरे हैं और टूर्नामेंट की तैयारी कीमत तय करते हैं।', 'रैंक और दुर्लभ बंडल व पेट का कलेक्शन प्राइस टियर तय करता है।', 'असली मार्केटप्लेस मौजूद है, जिसमें «व्हेल» अकाउंट की अलग कैटेगरी भी है।', 'कीमत लगभग पूरी तरह स्किन की दुर्लभता पर निर्भर है।', 'असली रेंज बनाम «$90K अकाउंट» वाली पुरानी सुर्ख़ियाँ।', 'इकलौता गेम जिसमें दुर्लभ यूज़रनेम का असली मार्केट है।'],
  top='सबसे बड़ा कलेक्शन: {v}', upto='{v} तक', read='पूरी रिपोर्ट पढ़ें →', about_h='इस रिपोर्ट के बारे में',
  about_p='हर गेम की पूरी रिपोर्ट अपने स्रोत बताती है: मार्केटप्लेस लिस्टिंग, इंडस्ट्री के प्लेयर-काउंट ट्रैकर और दर्ज किए गए मामले। आँकड़े माँगी गई कीमतें और खुद बताए गए मामले हैं, ऑडिट की हुई बिक्री नहीं।',
  desc='Roblox, Genshin Impact, Fortnite, Minecraft और 5 अन्य गेम की असली मार्केट प्राइस रेंज। पूरी जानकारी के लिए कोई गेम चुनें — स्रोतों के साथ, अंदाज़े से नहीं।'),
 'fr': dict(
  lead='Fourchettes de prix réelles du marché pour 9 jeux — sourcées, pas devinées. Choisissez un jeu ci-dessous pour l’analyse complète : chiffres, paliers de prix, cas documentés, ce qui fait la valeur et risques d’arnaque.',
  compiled='Établi en septembre 2026 à partir d’annonces publiques de places de marché et de témoignages documentés de joueurs.',
  cards=['Un vrai marché existe — et la valeur se trouve aussi dans les collections d’objets.', 'Comptes entièrement améliorés face aux annonces de progression moyenne.', 'Le prix dépend presque entièrement du niveau de l’Hôtel de ville et des améliorations de héros.', 'Le niveau des cartes et l’aptitude aux tournois font le prix.', 'Le rang et les collections de packs et de familiers rares fixent le palier de prix.', 'Un vrai marché existe, avec une catégorie dédiée aux comptes « baleine ».', 'Le prix dépend presque entièrement de la rareté des skins.', 'La fourchette réelle face aux vieux titres sur les « comptes à 90 000 $ ».', 'Le seul jeu doté d’un vrai marché des pseudos rares.'],
  top='Plus grande collection : {v}', upto='Jusqu’à {v}', read='Lire le rapport complet →', about_h='À propos de ce rapport',
  about_p='Le rapport complet de chaque jeu indique ses propres sources : annonces de places de marché, outils de suivi du nombre de joueurs et cas documentés. Les chiffres sont des prix demandés et des cas déclarés par les joueurs, pas des ventes auditées.',
  desc='Fourchettes de prix réelles du marché pour Roblox, Genshin Impact, Fortnite, Minecraft et 5 autres jeux. Choisissez un jeu pour l’analyse complète — sourcée, pas devinée.'),
 'de': dict(
  lead='Echte Marktpreisspannen für 9 Spiele — mit Quellen, nicht geraten. Wähle unten ein Spiel für die vollständige Aufschlüsselung: Fakten, Preisstufen, dokumentierte Fälle, Werttreiber und Betrugsrisiken.',
  compiled='Zusammengestellt im September 2026 aus öffentlichen Marktplatz-Angeboten und dokumentierten Spielerberichten.',
  cards=['Es gibt einen echten Marktplatz — der Wert steckt auch in Sammlerbeständen.', 'Voll ausgebaute Konten gegenüber Angeboten mit mittlerem Fortschritt.', 'Der Preis hängt fast vollständig vom Rathaus-Level und den Helden-Upgrades ab.', 'Kartenlevel und Turniertauglichkeit bestimmen den Preis.', 'Rang und Sammlungen seltener Bundles und Begleiter bestimmen die Preisstufe.', 'Es gibt einen echten Marktplatz, samt eigener Kategorie für „Whale“-Konten.', 'Der Preis hängt fast vollständig von der Seltenheit der Skins ab.', 'Die echte Spanne gegenüber alten Schlagzeilen über „90.000-$-Konten“.', 'Das einzige Spiel mit einem echten Markt für seltene Benutzernamen.'],
  top='Größter Bestand: {v}', upto='Bis zu {v}', read='Vollständigen Bericht lesen →', about_h='Über diesen Bericht',
  about_p='Der vollständige Bericht zu jedem Spiel nennt seine eigenen Quellen: Marktplatz-Angebote, Branchen-Tracker für Spielerzahlen und dokumentierte Fälle. Die Zahlen sind Angebotspreise und selbst gemeldete Fälle, keine geprüften Verkäufe.',
  desc='Echte Marktpreisspannen für Roblox, Genshin Impact, Fortnite, Minecraft und 5 weitere Spiele. Wähle ein Spiel für die vollständige Aufschlüsselung — mit Quellen, nicht geraten.'),
 'it': dict(
  lead='Fasce di prezzo reali di mercato per 9 giochi — con fonti, non a caso. Scegli un gioco qui sotto per l’analisi completa: dati, fasce di prezzo, casi documentati, cosa determina il valore e rischi di truffa.',
  compiled='Redatto a settembre 2026 da annunci pubblici dei marketplace e testimonianze documentate dei giocatori.',
  cards=['Esiste un vero marketplace — e il valore sta anche nelle collezioni di oggetti.', 'Account al massimo contro annunci con progressi medi.', 'Il prezzo dipende quasi del tutto dal livello del Municipio e dai potenziamenti degli eroi.', 'Il livello delle carte e la prontezza per i tornei determinano il prezzo.', 'Il grado e le collezioni di pacchetti e animali rari fissano la fascia di prezzo.', 'Esiste un vero marketplace, con una categoria dedicata agli account «whale».', 'Il prezzo dipende quasi del tutto dalla rarità delle skin.', 'La fascia reale contro i vecchi titoli sugli «account da 90.000 $».', 'L’unico gioco con un vero mercato dei nomi utente rari.'],
  top='Collezione più grande: {v}', upto='Fino a {v}', read='Leggi il report completo →', about_h='Informazioni su questo report',
  about_p='Il report completo di ogni gioco elenca le proprie fonti: annunci dei marketplace, tracker del numero di giocatori e casi documentati. Le cifre sono prezzi richiesti e casi dichiarati dai giocatori, non vendite verificate.',
  desc='Fasce di prezzo reali di mercato per Roblox, Genshin Impact, Fortnite, Minecraft e altri 5 giochi. Scegli un gioco per l’analisi completa — con fonti, non a caso.'),
 'ja': dict(
  lead='9タイトルの実際の市場価格帯を、推測ではなく出典付きで掲載しています。下からゲームを選ぶと、データ、価格帯、記録された事例、価値を決める要因、詐欺のリスクを詳しく見られます。',
  compiled='2026年9月、公開されているマーケットプレイスの出品とプレイヤーの記録された報告をもとに作成。',
  cards=['実際のマーケットが存在し、価値はコレクターの所持品にもあります。', '最大まで育成したアカウントと中程度の進行度の出品。', '価格はほぼタウンホールレベルとヒーローの強化で決まります。', 'カードの育成度と大会への対応度が価格を決めます。', 'ランクとレアなバンドル・ペットのコレクションが価格帯を決めます。', '実際のマーケットが存在し、「廃課金」アカウント専用のカテゴリもあります。', '価格はほぼスキンのレア度で決まります。', '実際の価格帯と、かつての「9万ドルのアカウント」という見出し。', 'レアなユーザー名の実際の市場がある唯一のゲーム。'],
  top='最大の所持コレクション：{v}', upto='最大{v}', read='レポート全文を読む →', about_h='このレポートについて',
  about_p='各ゲームの詳細レポートには、マーケットプレイスの出品、業界のプレイヤー数トラッカー、記録された事例など、それぞれの出典を記載しています。数値は出品価格と自己申告の事例であり、監査済みの売買ではありません。',
  desc='Roblox、Genshin Impact、Fortnite、Minecraftほか5タイトルの実際の市場価格帯。ゲームを選ぶと詳細を見られます。推測ではなく出典付きです。'),
 'ko': dict(
  lead='9개 게임의 실제 시장 가격대를 추측이 아닌 출처와 함께 정리했습니다. 아래에서 게임을 고르면 데이터, 가격 구간, 기록된 사례, 가치를 결정하는 요소, 사기 위험을 자세히 볼 수 있습니다.',
  compiled='2026년 9월, 공개된 마켓플레이스 판매글과 기록된 플레이어 제보를 바탕으로 작성.',
  cards=['실제 마켓플레이스가 있으며, 가치는 수집 아이템에도 있습니다.', '완전히 육성한 계정과 중간 진행도 판매글.', '가격은 거의 전적으로 타운홀 레벨과 영웅 업그레이드에 달려 있습니다.', '카드 육성 정도와 대회 준비 수준이 가격을 좌우합니다.', '랭크와 희귀 번들·펫 컬렉션이 가격 구간을 정합니다.', '실제 마켓플레이스가 있으며, «고래» 계정 전용 카테고리도 있습니다.', '가격은 거의 전적으로 스킨의 희귀도에 달려 있습니다.', '실제 가격대와 예전의 «9만 달러 계정» 기사 제목.', '희귀 사용자 이름의 실제 시장이 있는 유일한 게임.'],
  top='최대 보유 컬렉션: {v}', upto='최대 {v}', read='전체 보고서 읽기 →', about_h='이 보고서에 대하여',
  about_p='각 게임의 전체 보고서에는 마켓플레이스 판매글, 업계 플레이어 수 추적 사이트, 기록된 사례 등 자체 출처가 적혀 있습니다. 수치는 판매 희망가와 본인이 밝힌 사례이며, 감사를 거친 거래가 아닙니다.',
  desc='Roblox, Genshin Impact, Fortnite, Minecraft 외 5개 게임의 실제 시장 가격대. 게임을 고르면 자세한 내용을 볼 수 있습니다 — 추측이 아닌 출처 기반.'),
 'th': dict(
  lead='ช่วงราคาตลาดจริงของ 9 เกม — มีแหล่งที่มา ไม่ใช่การเดา เลือกเกมด้านล่างเพื่อดูรายละเอียดทั้งหมด: ข้อมูล ระดับราคา กรณีที่มีบันทึก ปัจจัยที่กำหนดมูลค่า และความเสี่ยงจากการหลอกลวง',
  compiled='จัดทำเมื่อเดือนกันยายน 2026 จากประกาศสาธารณะในตลาดซื้อขายและรายงานของผู้เล่นที่มีบันทึก',
  cards=['มีตลาดซื้อขายจริง — และมูลค่ายังอยู่ในของสะสมด้วย', 'บัญชีที่อัปเต็มเทียบกับประกาศที่มีความคืบหน้าระดับกลาง', 'ราคาขึ้นอยู่กับเลเวล Town Hall และการอัปเกรดฮีโร่เกือบทั้งหมด', 'ระดับการอัปเกรดการ์ดและความพร้อมลงทัวร์นาเมนต์เป็นตัวกำหนดราคา', 'แรงก์และคอลเลกชันบันเดิลกับสัตว์เลี้ยงหายากเป็นตัวกำหนดระดับราคา', 'มีตลาดซื้อขายจริง รวมถึงหมวดเฉพาะสำหรับบัญชี «วาฬ»', 'ราคาขึ้นอยู่กับความหายากของสกินเกือบทั้งหมด', 'ช่วงราคาจริงเทียบกับพาดหัวเก่าเรื่อง «บัญชี 90,000 ดอลลาร์»', 'เกมเดียวที่มีตลาดชื่อผู้ใช้หายากจริง ๆ'],
  top='คอลเลกชันใหญ่ที่สุด: {v}', upto='สูงสุด {v}', read='อ่านรายงานฉบับเต็ม →', about_h='เกี่ยวกับรายงานนี้',
  about_p='รายงานฉบับเต็มของแต่ละเกมระบุแหล่งที่มาของตัวเอง: ประกาศในตลาดซื้อขาย เว็บติดตามจำนวนผู้เล่นของอุตสาหกรรม และกรณีที่มีบันทึก ตัวเลขเป็นราคาที่ตั้งขายและกรณีที่ผู้เล่นเปิดเผยเอง ไม่ใช่ยอดขายที่ผ่านการตรวจสอบ',
  desc='ช่วงราคาตลาดจริงของ Roblox, Genshin Impact, Fortnite, Minecraft และอีก 5 เกม เลือกเกมเพื่อดูรายละเอียดทั้งหมด — มีแหล่งที่มา ไม่ใช่การเดา'),
 'pl': dict(
  lead='Rzeczywiste przedziały cen rynkowych dla 9 gier — ze źródłami, a nie na oko. Wybierz grę poniżej, aby zobaczyć pełne omówienie: dane, progi cenowe, udokumentowane przypadki, co decyduje o wartości i ryzyko oszustw.',
  compiled='Opracowano we wrześniu 2026 r. na podstawie publicznych ogłoszeń z platform handlowych i udokumentowanych relacji graczy.',
  cards=['Prawdziwy rynek istnieje — a wartość tkwi też w kolekcjach przedmiotów.', 'Konta w pełni rozwinięte a ogłoszenia o średnim postępie.', 'Cena zależy niemal całkowicie od poziomu Ratusza i ulepszeń bohaterów.', 'Poziom kart i gotowość do turniejów decydują o cenie.', 'Ranga oraz kolekcje rzadkich zestawów i zwierzaków wyznaczają próg cenowy.', 'Prawdziwy rynek istnieje, łącznie z osobną kategorią kont „wielorybów”.', 'Cena zależy niemal całkowicie od rzadkości skórek.', 'Rzeczywisty przedział a stare nagłówki o „kontach za 90 tys. dolarów”.', 'Jedyna gra z prawdziwym rynkiem rzadkich nazw użytkownika.'],
  top='Największa kolekcja: {v}', upto='Do {v}', read='Przeczytaj pełny raport →', about_h='O tym raporcie',
  about_p='Pełny raport każdej gry podaje własne źródła: ogłoszenia z platform handlowych, branżowe serwisy śledzące liczbę graczy i udokumentowane przypadki. Liczby to ceny ofertowe i przypadki zgłoszone przez samych graczy, a nie zweryfikowane transakcje.',
  desc='Rzeczywiste przedziały cen rynkowych dla Roblox, Genshin Impact, Fortnite, Minecraft i 5 innych gier. Wybierz grę, aby zobaczyć pełne omówienie — ze źródłami, a nie na oko.'),
 'zh': dict(
  lead='9 款游戏的真实市场价格区间——有来源，不靠猜。在下方选择一款游戏查看完整分析：数据、价格档位、有记录的案例、决定价值的因素以及诈骗风险。',
  compiled='2026 年 9 月根据公开的交易平台挂牌信息和有记录的玩家报告整理。',
  cards=['存在真实的交易市场——价值也体现在收藏品持有上。', '完全养成的账号与中等进度的挂牌。', '价格几乎完全取决于大本营等级和英雄升级。', '卡牌养成程度和比赛就绪度决定价格。', '段位以及稀有套装和宠物的收藏决定价格档位。', '存在真实的交易市场，还有专门的“氪金大佬”账号分类。', '价格几乎完全取决于皮肤的稀有度。', '真实价格区间与过去“9 万美元账号”的标题。', '唯一拥有真实稀有用户名市场的游戏。'],
  top='最大收藏持有：{v}', upto='最高 {v}', read='阅读完整报告 →', about_h='关于本报告',
  about_p='每款游戏的完整报告都列出了各自的来源：交易平台挂牌信息、行业玩家数量追踪网站以及有记录的案例。数字为挂牌要价和玩家自述的案例，并非经过审计的成交。',
  desc='Roblox、Genshin Impact、Fortnite、Minecraft 及另外 5 款游戏的真实市场价格区间。选择一款游戏查看完整分析——有来源，不靠猜。'),
}


def money(lang, v):
    dec, thou, before = FMT[lang]
    plus = v.endswith('+'); n = v.rstrip('+')
    whole, _, frac = n.partition('.')
    if len(whole) > 3:
        whole = whole[:-3] + thou + whole[-3:]
    s = whole + (dec + frac if frac else '')
    if plus:
        s += '+'
    return '$' + s if before else s + SUFFIX[lang]


def price(lang, game):
    t = T[lang]
    if game == 'roblox':
        dec, _, before = FMT[lang]
        v = '2' + dec + '45M'
        return t['top'].format(v='~' + ('$' + v if before else v + SUFFIX[lang]))
    if game == 'genshin-impact':
        return t['upto'].format(v=money(lang, '9000'))
    lo, hi = RANGE[game]
    return money(lang, lo) + ' – ' + money(lang, hi)


def ltr(lang, game):
    """A bare 'low – high' range must read left to right inside a right-to-left page."""
    return ' dir="ltr"' if lang == 'ar' and game in RANGE else ''


def build(lang):
    p = ROOT + lang + os.sep + 'market-report.html'
    s = io.open(p, encoding='utf-8', newline='').read()
    nl = '\r\n' if '\r\n' in s else '\n'
    a, b = s.index('<main'), s.index('</main>') + 7
    old = s[a:b]; t = T[lang]
    h1 = re.search(r'<h1[^>]*>.*?</h1>', old, re.S).group(0)
    # blocks kept from the page itself: the "we don't recommend trading" notice, the guide links, the bot button
    notice = re.search(r'<section style="max-width: 760px;[^"]*">.*?</section>', old, re.S).group(0)
    cta = re.search(r'(?:<img class="g-joystick"[^>]*>\s*)?<div class="report-cta">.*?</div>', old, re.S)
    # guide links: labels come from this page's own menu, the heading from the language's game pages
    head = s[:a]

    def label(href):
        m = re.search(r'<a href="\./' + re.escape(href) + r'"[^>]*>(.*?)</a>', head, re.S)
        return re.sub(r'<[^>]+>', '', m.group(1)).strip()
    game_page = io.open(ROOT + lang + os.sep + 'roblox.html', encoding='utf-8').read()
    more = re.search(r'<span class="resources-label">(.*?)</span>', game_page, re.S).group(1)
    links = ''.join(f'  <a href="./{h}">{label(h)}</a>\n' for h in (
        'glossary.html', 'account-trading-safety.html', 'which-game-accounts-are-most-valuable.html', 'methodology.html'))
    res = f'<div class="resources-callout">\n  <span class="resources-label">{more}</span>\n{links}</div>'
    assert cta and notice, lang
    cards = ''.join(
        f'  <a href="./{g}.html" class="game-card">\n    <span class="icon">{ICON[g]}</span>\n    <h2>{NAME[g]}</h2>\n'
        f'    <p>{t["cards"][i]}</p>\n    <span class="price"{ltr(lang, g)}>{price(lang, g)}</span>\n    <span class="arrow">{t["read"]}</span>\n  </a>\n'
        for i, g in enumerate(NAME))
    main = ('<main>\n<section class="report-hero" id="main-content">\n  ' + h1 + '\n'
            f'  <p style="color:var(--muted); font-size:17px;">{t["lead"]}</p>\n  <p class="report-updated">{t["compiled"]}</p>\n</section>\n\n'
            + notice + '\n\n' + res + '\n\n<hr class="report-divider">\n\n<div class="game-grid" style="margin-top: 32px;">\n' + cards + '</div>\n\n'
            + cta.group(0) + '\n\n<section class="sources-list">\n'
            f'  <h2 style="font-size:16px; color:var(--text); margin-bottom:10px;">{t["about_h"]}</h2>\n  <p>{t["about_p"]}</p>\n</section>\n</main>')
    out = s[:a] + main.replace('\n', nl) + s[b:]
    # page-specific CSS: the card grid rules live in the hub's inline <style> (same block as ru/market-report.html)
    ref = io.open(ROOT + 'ru' + os.sep + 'market-report.html', encoding='utf-8').read()
    ref_css = re.findall(r'<style[^>]*>.*?</style>', ref[:ref.index('<main')], re.S)[-1]
    own_css = re.findall(r'<style[^>]*>.*?</style>', out[:out.index('<main')], re.S)[-1]
    out = out.replace(own_css, ref_css.replace('\r\n', '\n').replace('\n', nl), 1)
    # meta description (meta, og, twitter, JSON-LD) and JSON-LD without the FAQ that is no longer on the page
    od = re.search(r'<meta name="description" content="([^"]*)"', out).group(1)
    out = out.replace(od, t['desc'].replace('"', '&quot;'))

    def ld(m):
        j = json.loads(m.group(1))
        g = j.get('@graph')
        if isinstance(g, list):
            j['@graph'] = [n for n in g if n.get('@type') != 'FAQPage']
        elif j.get('@type') == 'FAQPage':
            return ''
        for n in (j.get('@graph') or [j]):
            if 'description' in n and n.get('@type') in ('Article', 'WebPage', 'CollectionPage'):
                n['description'] = t['desc']
        return '<script type="application/ld+json">' + json.dumps(j, ensure_ascii=False) + '</script>'
    out = re.sub(r'<script type="application/ld\+json">(.*?)</script>', ld, out, flags=re.S)
    if out != s:
        io.open(p, 'w', encoding='utf-8', newline='').write(out)
        return 1
    return 0


if __name__ == '__main__':
    print('market report hubs rebuilt:', sum(build(L) for L in T))
