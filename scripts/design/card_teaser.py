"""Card-collection teasers (owner-approved preview 2026-09-30, "afraid they won't
scroll down to the cards"):
  1. hero chip next to the AI badge on 24 homepages -> #cards
  2. teaser under the bot CTA in every calculator (homepages + game pages) with
     a live mini card -> the carousel (#cards on the language's homepage)
  3. the carousel moves up to the 2nd screen (right after the calculator block)
Idempotent. Styles in scripts/design/css/glass-art.css."""
import glob, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + os.sep
# chip, teaser headline, teaser line (before link), link text
T = {
 'en': ('🎴 + collectible holo card', 'A paid report is your own numbered holo card', 'PDF + video, 9 foil tiers, the first 100 are GENESIS.', 'See all cards ↓'),
 'ru': ('🎴 + коллекционная голо-карта', 'Платный отчёт — это твоя именная голо-карта с номером', 'PDF + видео, 9 уровней фольги, первые 100 — GENESIS.', 'Смотреть все карты ↓'),
 'es': ('🎴 + carta holo coleccionable', 'Un informe de pago es tu propia carta holo numerada', 'PDF + vídeo, 9 niveles de lámina, las primeras 100 son GENESIS.', 'Ver todas las cartas ↓'),
 'pt': ('🎴 + carta holo colecionável', 'Um relatório pago é a sua própria carta holo numerada', 'PDF + vídeo, 9 níveis de lâmina, as primeiras 100 são GENESIS.', 'Ver todas as cartas ↓'),
 'id': ('🎴 + kartu holo koleksi', 'Laporan berbayar = kartu holo bernomor milikmu sendiri', 'PDF + video, 9 tingkat foil, 100 pertama adalah GENESIS.', 'Lihat semua kartu ↓'),
 'tr': ('🎴 + koleksiyonluk holo kart', 'Ücretli rapor, size ait numaralı bir holo karttır', 'PDF + video, 9 folyo seviyesi, ilk 100 kart GENESIS.', 'Tüm kartları gör ↓'),
 'ar': ('🎴 + بطاقة هولوغرام للمقتنين', 'التقرير المدفوع هو بطاقتك الهولوغرامية المرقّمة', 'PDF + فيديو، 9 مستويات من الرقاقة، وأول 100 بطاقة هي GENESIS.', 'شاهد كل البطاقات ↓'),
 'vi': ('🎴 + thẻ holo sưu tầm', 'Báo cáo trả phí là thẻ holo có số hiệu của riêng bạn', 'PDF + video, 9 cấp lá kim, 100 thẻ đầu tiên là GENESIS.', 'Xem tất cả thẻ ↓'),
 'hi': ('🎴 + संग्रहणीय होलो कार्ड', 'पेड रिपोर्ट = आपका अपना नंबर वाला होलो कार्ड', 'PDF + वीडियो, फ़ॉयल के 9 लेवल, पहले 100 कार्ड GENESIS हैं।', 'सभी कार्ड देखें ↓'),
 'fr': ('🎴 + carte holo à collectionner', 'Un rapport payant, c’est votre carte holo numérotée', 'PDF + vidéo, 9 niveaux de dorure, les 100 premières sont GENESIS.', 'Voir toutes les cartes ↓'),
 'de': ('🎴 + holografische Sammelkarte', 'Ein bezahlter Bericht ist deine eigene nummerierte Holokarte', 'PDF + Video, 9 Folienstufen, die ersten 100 sind GENESIS.', 'Alle Karten ansehen ↓'),
 'it': ('🎴 + carta olografica da collezione', 'Un report a pagamento è la tua carta olografica numerata', 'PDF + video, 9 livelli di lamina, le prime 100 sono GENESIS.', 'Vedi tutte le carte ↓'),
 'ja': ('🎴 + コレクション用ホロカード', '有料レポートは、番号入りのあなただけのホロカード', 'PDF + 動画、9段階の箔、最初の100枚はGENESIS。', 'すべてのカードを見る ↓'),
 'ko': ('🎴 + 컬렉션 홀로 카드', '유료 리포트 = 번호가 새겨진 나만의 홀로 카드', 'PDF + 영상, 9단계 포일, 첫 100장은 GENESIS.', '모든 카드 보기 ↓'),
 'zh': ('🎴 + 收藏级全息卡牌', '付费报告就是你专属的编号全息卡牌', 'PDF + 视频，9 个烫金等级，前 100 张为 GENESIS。', '查看全部卡牌 ↓'),
 'pl': ('🎴 + kolekcjonerska karta holo', 'Płatny raport to Twoja własna numerowana karta holo', 'PDF + wideo, 9 poziomów folii, pierwsze 100 to GENESIS.', 'Zobacz wszystkie karty ↓'),
 'th': ('🎴 + การ์ดโฮโลสะสม', 'รายงานแบบชำระเงิน = การ์ดโฮโลมีหมายเลขของคุณเอง', 'PDF + วิดีโอ ฟอยล์ 9 ระดับ 100 ใบแรกคือ GENESIS', 'ดูการ์ดทั้งหมด ↓'),
 'tl': ('🎴 + collectible na holo card', 'Ang bayad na report = sarili mong holo card na may numero', 'PDF + video, 9 na antas ng foil, GENESIS ang unang 100.', 'Tingnan ang lahat ng card ↓'),
 'sw': ('🎴 + kadi ya holo ya mkusanyiko', 'Ripoti ya kulipia ni kadi yako ya holo yenye namba', 'PDF + video, viwango 9 vya foili, 100 za kwanza ni GENESIS.', 'Tazama kadi zote ↓'),
 'ms': ('🎴 + kad holo koleksi', 'Laporan berbayar ialah kad holo bernombor milik anda', 'PDF + video, 9 peringkat foil, 100 yang pertama ialah GENESIS.', 'Lihat semua kad ↓'),
 'uz': ('🎴 + kolleksiya golo-kartasi', 'Pullik hisobot — raqamli shaxsiy golo-kartangiz', 'PDF + video, folganing 9 darajasi, birinchi 100 tasi — GENESIS.', 'Barcha kartalarni koʻrish ↓'),
 'kk': ('🎴 + коллекциялық голо-карта', 'Ақылы есеп — нөмірі бар өз голо-картаңыз', 'PDF + бейне, фольганың 9 деңгейі, алғашқы 100-і — GENESIS.', 'Барлық карталарды көру ↓'),
 'tk': ('🎴 + kolleksiýa golo-karty', 'Tölegli hasabat — belgili öz golo-kartyňyz', 'PDF + wideo, folganyň 9 derejesi, ilkinji 100-si — GENESIS.', 'Ähli kartlary gör ↓'),
 'ky': ('🎴 + коллекциялык голо-карта', 'Акы төлөнгөн отчёт — номери бар өз голо-картаң', 'PDF + видео, фольганын 9 деңгээли, алгачкы 100ү — GENESIS.', 'Бардык карталарды көрүү ↓'),
}


def teaser(lang, href, img):
    _, head, line, link = T[lang]
    return (f'<a class="gc-teaser" href="{href}"><span class="t-card"><img src="{img}" width="540" height="360" alt="" loading="lazy" decoding="async"></span>'
            f'<span><strong>{head}</strong><span>{line} <em>{link}</em></span></span></a>')


def main():
    st = dict(chip=0, teaser=0, moved=0)
    for f in glob.glob(ROOT + '**/*.html', recursive=True):
        rel = os.path.relpath(f, ROOT).replace(os.sep, '/')
        if rel.startswith(('scripts/', '_', 'node_modules/', 'google')):
            continue
        parts = rel.split('/')
        lang = parts[0] if len(parts) == 2 else 'en'
        if lang not in T:
            continue
        s = o = open(f, encoding='utf-8').read()
        P = '../' if len(parts) == 2 else './'
        home = parts[-1] == 'index.html'
        if 'class="gc-teaser"' not in s and 'data-g-slot="result"' in s:
            img = f'{P}assets/cards/{lang}/{"diamond" if home else "gold"}.webp?v=2'
            s, n = re.subn(r'(<div class="g-exact" data-g-slot="result"><a [^>]*>.*?</a>)',
                           lambda m: m.group(1) + teaser(lang, '#cards' if home else './#cards', img), s, count=1, flags=re.S)
            st['teaser'] += n
        if home:
            if 'hero-card-chip' not in s:
                s, n = re.subn(r'(<div class="hero-badge">[^<]*</div>)',
                               lambda m: f'<div class="hero-chips">{m.group(1)}<a class="hero-card-chip" href="#cards">{T[lang][0]}</a></div>', s, count=1)
                st['chip'] += n
            m = re.search(r'<!-- CARD COLLECTION -->.*?</section>\n\n', s, re.S)
            if m and s.find('<!-- CARD COLLECTION -->') > s.find('<!-- DIFFERENTIATION -->'):
                sec = m.group(0)
                s = s.replace(sec, '', 1).replace('<!-- DIFFERENTIATION -->', sec + '<!-- DIFFERENTIATION -->', 1)
                st['moved'] += 1
        if s != o:
            open(f, 'w', encoding='utf-8', newline='').write(s)
    print(st)


if __name__ == '__main__':
    main()
