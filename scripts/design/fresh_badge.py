"""Freshness badge wording (deep audit 2026-10-01). The old badges said prices were 'researched live
by AI across marketplaces', which contradicts methodology.html and about.html (listings are checked
by hand; no automated marketplace scraping). One honest phrase per language + the real check date."""
import glob, json, os, re, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + os.sep
CHECKED = '2026-09-12'
T = {
 'en': 'Checked against live marketplace listings: {d}', 'ru': 'Сверено с актуальными объявлениями маркетплейсов: {d}',
 'es': 'Comprobado con anuncios activos de marketplaces: {d}', 'pt': 'Conferido com anúncios ativos de marketplaces: {d}',
 'id': 'Dicek dengan listing marketplace yang aktif: {d}', 'tr': 'Pazaryerlerindeki güncel ilanlarla karşılaştırıldı: {d}',
 'ar': 'تمت المطابقة مع إعلانات الأسواق النشطة: {d}', 'vi': 'Đã đối chiếu với tin đăng đang hoạt động trên các chợ: {d}',
 'hi': 'मार्केटप्लेस की सक्रिय लिस्टिंग से मिलान किया गया: {d}', 'fr': 'Vérifié sur les annonces actives des places de marché : {d}',
 'de': 'Mit aktuellen Marktplatz-Angeboten abgeglichen: {d}', 'it': 'Verificato sugli annunci attivi dei marketplace: {d}',
 'ja': 'マーケットプレイスの現行出品と照合：{d}', 'ko': '마켓플레이스 현재 매물과 대조: {d}', 'zh': '已与交易平台在售挂单核对：{d}',
 'th': 'ตรวจสอบกับประกาศขายที่เปิดอยู่ในตลาดซื้อขาย: {d}', 'pl': 'Sprawdzono z aktywnymi ofertami na marketplace’ach: {d}',
 'tl': 'Sinuri laban sa mga aktibong listing sa marketplace: {d}', 'sw': 'Imelinganishwa na matangazo hai ya masoko: {d}',
 'ms': 'Disemak dengan senarai pasaran yang aktif: {d}', 'uz': 'Marketpleyslardagi amaldagi eʼlonlar bilan solishtirildi: {d}',
 'kk': 'Маркетплейстердегі қолданыстағы хабарландырулармен салыстырылды: {d}', 'tk': 'Marketpleýslerdäki häzirki bildirişler bilen deňeşdirildi: {d}',
 'ky': 'Маркетплейстердеги учурдагы жарыялар менен салыштырылды: {d}',
}
js = ('const L=%s,o={};for(const l of L)o[l]=new Intl.DateTimeFormat(l,{dateStyle:"long",timeZone:"UTC"}).format(new Date("%sT00:00:00Z"));console.log(JSON.stringify(o))'
      % (json.dumps(list(T)), CHECKED))
D = json.loads(subprocess.run(['node', '-e', js], capture_output=True, text=True, encoding='utf-8', check=True).stdout)

n = 0
for f in glob.glob(ROOT + '**/*.html', recursive=True):
    rel = os.path.relpath(f, ROOT).replace(os.sep, '/')
    if rel.startswith(('scripts/', '_')):
        continue
    L = rel.split('/')[0] if rel.count('/') == 1 else 'en'
    s = open(f, encoding='utf-8').read()
    t, k = re.subn(r'<div class="fresh-badge">.*?</div>',
                   lambda m: f'<div class="fresh-badge">🗓️ {T[L].format(d=D[L])}</div>', s, flags=re.S)
    if k and t != s:
        open(f, 'w', encoding='utf-8', newline='').write(t)
        n += k
print('badges rewritten', n)
