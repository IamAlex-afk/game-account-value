"""PUBG Mobile page text (2026-10-14) — Turkish, written for Turkish players.
Turkish number format (245.000 ₺, 0,29 $, level 74,5); the own market (GameSatış) comes first.
Terms as Turkish sellers write them: koleksiyon seviyesi, max silah, spor araba, mitik."""
from pubg_text_a import EL, FP, GS, IG, EULA, PR, EWC, GOP

TEXT = {
 'tr': dict(
  thou='.', dec=',', cur_after=True,
  title='PUBG Mobile Hesabım Ne Kadar Eder? Koleksiyon Seviyesine Göre Fiyatlar (2026) | GameAccountValue',
  desc='Ücretsiz, kayıt olmadan, veri toplamadan: Eldorado.gg, FunPay ve GameSatış ilan fiyatları (0,29 $–4.960 $), koleksiyon seviyesine göre tablo, botun istediği 5 ekran görüntüsü, dolandırıcılık riskleri.',
  og_title='PUBG Mobile Hesabım Ne Kadar Eder? — GameAccountValue',
  og_alt='GameAccountValue — PUBG Mobile hesap değeri',
  h1='🪂 PUBG Mobile Hesap Değeri',
  intro='Dört pazar yerindeki ilan fiyatları, bu fiyatların bağlı olduğu tek sayı — koleksiyon seviyesi — ve onu gösteren ekran görüntüleri.',
  updated='Ekim 2026’da pazar yeri ilanlarıyla kontrol edildi. Kaynaklar sayfanın altında.',
  badge='🗓️ İlanlar elle kontrol edildi: 14 Ekim 2026',
  range='Görülen ilan fiyatları: 0,29 $ – 4.960 $ · GameSatış: 1.000 ₺ – 245.000 ₺',
  facts=['🗂️ Oyunda <strong>95</strong> koleksiyon seviyesi var',
         '🥇 PUBG Mobile Dünya Kupası 2026 şampiyonu: <strong>S2G Esports</strong> (Türkiye)',
         '🏆 Global Championship 2026, 3.000.000 $ ödül havuzu: <strong>Türkiye</strong>'],
  calc_sub='Tek kaydırıcı: koleksiyon seviyesi — satıcılar fiyatı buna göre koyuyor. Hiçbir şey girilmez, hiçbir yere gönderilmez; bot seviyeyi ekran görüntülerinden okur.',
  calc_why='Hesaplayıcı yalnızca koleksiyon seviyesini görür. X-Suit seviyelerini, max silahları ve spor arabaları göremez — bunları bot ekran görüntülerinden sayar.',
  nav_shots='📸 Ekran görüntüleri',
  h2_shots='Değerlendirme için ekran görüntüleri',
  q_worth='Bir PUBG Mobile hesabı ne kadar eder?',
  a_worth=('14 Ekim 2026’da GameSatış’ta PUBG Mobile hesapları 1.000 ₺ ile 245.000 ₺ arasında (≈ 20 $ – 4.960 $) satışa çıkarılmıştı; en pahalısı 92,6 koleksiyonlu, 761 destansı eşyalı bir hesaptı. '
           'Eldorado.gg’de <strong>10.905</strong> ilan vardı: ilk sayfada fiyatlar sade bir Altın rütbe hesap için 2 $’dan koleksiyonu 74 olan hesap için 399,99 $’a kadar gidiyordu. '
           'FunPay’de <strong>6.332</strong> ilan, 0,26 € ile 3.286 € arasında (≈ 0,29 $ – 3.676 $). Bu farkın büyük kısmını tek bir sayı açıklıyor: koleksiyon seviyesi.'),
  q_table='Hangi koleksiyon seviyesinde hesaplar ne kadara ilan ediliyor?',
  table_head=('Koleksiyon seviyesi', 'Görülen ilan fiyatı', 'Nerede'),
  table_note='14 Ekim 2026 ilan fiyatları; dolara 1 $ = 49,4 ₺, 0,894 € ve 25.633 ₫ kuruyla çevrildi. Çoğu satırda tek ilan var — fiyat listesi değil, yön gösterir. '
             '74 seviyedeki 909 $’lık ilanda ayrıca 14 max silah yazıyor.',
  q_value='Bir PUBG Mobile hesabının değerini gerçekte ne belirler?',
  value=['<strong>Koleksiyon seviyesi</strong> — oyunda 95 seviye var; sahip olunan her yeni eşya türüne ve kalitesine göre puan ekler, yani seviye bütün envanteri tek sayıda özetler.',
         '<strong>X-Suit’ler ve geliştirme seviyeleri</strong> — FunPay’de maksimum seviye X-Suit’li hesaplar 2.063 € – 2.629 € istiyordu.',
         '<strong>Geliştirilebilir silah kaplamaları</strong> ve her birinin seviyesi (ilanlarda en çok Buz Diyarı M416 geçiyor).',
         '<strong>Spor arabalar</strong> — otomobil iş birliklerinden gelen araç kaplamaları; satıcılar bunları tek tek sayıyor.',
         '<strong>Rütbe çok az etkiler</strong>: her sezon sıfırlanır; Eldorado.gg’de “Gold Rank” hesap 1,99 $, “Diamond” hesap 3,75 $ istiyordu.'],
  q_lookup='Hesaplayıcıyı kullanmadan önce oyunda neye bakmalıyım?',
  lookup=['Hesaplayıcı tek bir sayı ister: Koleksiyon ekranındaki <strong>koleksiyon seviyesi</strong> (örneğin 74,5).',
          'Sonuç, açık ilan fiyatlarına göre kaba bir aralıktır, satın alma teklifi değildir. Hesap alıp satmak oyunun kurallarına aykırıdır — <a href="#rules">kurallara</a> bakın.'],
  q_shots='Bot PUBG Mobile için hangi 5 ekran görüntüsünü istiyor?',
  shots_intro='PUBG Mobile’da değer envanterin farklı sekmelerine dağılmıştır, bu yüzden bot üç değil beş ekran görüntüsü ister:',
  shots=['<strong>Profil</strong> — oyuncu ID’si, hesap seviyesi ve rütbe okunabilmeli.',
         '<strong>Koleksiyon</strong> — koleksiyon seviyesinin göründüğü Koleksiyon ekranı (örneğin 74,5). En önemli görüntü budur.',
         '<strong>Envanter → Kıyafetler</strong> — X-Suit’ler ve mitik kıyafetler görünmeli.',
         '<strong>Geliştirilebilir silah kaplamaları</strong> — her birinin seviyesi (Lv.) görünecek şekilde.',
         '<strong>Araç kaplamaları</strong> — spor arabalar ve diğer nadir araçlar; görünüyorsa UC bakiyesi.'],
  shots_note='Koleksiyon ekranı olmadan bot yalnızca görüntülerde gördüklerini sayar — X-Suit’ler, silahlar, spor arabalar — ve tahmin daha düşük çıkar. '
             'Bot hiçbir zaman giriş bilgisi veya şifre istemez, ekran görüntüleri saklanmaz.',
  q_scams='PUBG Mobile hesap satışında en sık görülen dolandırıcılıklar neler?',
  a_scams=('Bir PUBG Mobile hesabı aynı anda birden fazla girişe bağlanabilir — örneğin Facebook, Twitter veya Google Play. Satıcıda kalan her bağlantı geri dönüş yoludur: '
           'ödemeden sonra hesap “kurtarılır” ve alıcı elinde hiçbir şeyle kalmaz. FunPay’deki ilanların bir kısmı zaten satış değil kiralamadır (“Rent” işaretli). '
           'Yayıncının kuralları hesap devrini tamamen yasakladığı için anlaşma bozulursa iki taraf da desteğe başvuramaz.'),
  q_rules='PUBG Mobile hesabı satmak kurallara aykırı mı?',
  a_rules=('Evet. PUBG Mobile kullanım koşullarında (Proxima Beta Pte. Limited) hesabın kişisel olduğu ve onu hediye etmenin, ödünç vermenin, devretmenin veya başka birinin '
           'kullanmasına izin vermenin yasak olduğu yazıyor. Sanal eşya ve para birimi de satılamaz ya da takas edilemez; yayıncı erişimi askıya alabilir veya sözleşmeyi sonlandırabilir.'),
  q_where='Bu ilanlar nereden geliyor?',
  a_where=('GameSatış Türk pazar yeridir, Eldorado.gg, FunPay ve igitems.com uluslararasıdır. Bu sayfadaki her rakam 14 Ekim 2026’da elle bakılmış bir ilan fiyatıdır — '
           'tamamlanmış satış değildir ve hiçbir veri otomatik olarak toplanmadı.'),
  world_dem=dict(global_='Koleksiyon seviyesi, X-Suit’ler, Buz Diyarı M416', cis='Maksimum seviye X-Suit’ler (Firavun, Blood Raven), spor arabalar, mitik sayısı',
                 tr='Koleksiyon seviyesi, destansı eşya sayısı, max silahlar, spor arabalar',
                 sea='Maksimum seviye Buz Diyarı M416, Mumya setleri, Gun Lab silah sayısı, mitik kıyafet sayısı'),
  q_brackets='İlan fiyatları piyasada nasıl dağılıyor?',
  brackets_head=('İlan fiyatı', 'İlandaki hesap'),
  brackets_note='igitems.com piyasa raporu, 13 Ekim 2026: 446 PUBG Mobile hesabı satışta. İlanların çoğu 50 $ ile 300 $ arasında.',
  world_note='Bunlar ilan fiyatlarıdır, tamamlanmış satışlar değil. 1 $ = 0,894 €, 49,4 ₺ ve 25.633 ₫ kuruyla çevrildi (Ekim 2026). Yalnızca piyasayı anlatır — alım ya da satım tavsiyesi değildir; hesap ticareti oyunun kurallarına aykırıdır.',
  sources=[f'GameSatış — <a href="{GS}" target="_blank" rel="noopener">PUBG Mobile hesap satışı</a>, 14 Ekim 2026’da kontrol edildi',
           f'Eldorado.gg — <a href="{EL}" target="_blank" rel="noopener">PUBG Mobile hesap ilanları</a> (10.905), 14 Ekim 2026’da kontrol edildi',
           f'FunPay — <a href="{FP}" target="_blank" rel="noopener">PUBG Mobile hesapları</a> (6.332), 14 Ekim 2026’da kontrol edildi',
           f'igitems.com — <a href="{IG}" target="_blank" rel="noopener">PUBG Mobile hesapları ve piyasa raporu</a> (446), 14 Ekim 2026’da kontrol edildi',
           f'Proxima Beta — <a href="{EULA}" target="_blank" rel="noopener">PUBG Mobile kullanım koşulları</a>',
           f'PUBG MOBILE Esports — <a href="{PR}" target="_blank" rel="noopener">2026 espor yol haritası</a> (basın bülteni, 12 Aralık 2025)',
           f'Esports World Cup — <a href="{EWC}" target="_blank" rel="noopener">S2G Esports PMWC şampiyonu</a> (16 Ağustos 2026)',
           f'GamingOnPhone — <a href="{GOP}" target="_blank" rel="noopener">koleksiyon seviyesi nasıl işler</a>'],
 ),
}
