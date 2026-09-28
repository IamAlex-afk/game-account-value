"""Make the 13 full-locale homepages that had no calculator tool-first too.
Starts from each page's pre-redesign HTML (commit 3108b00), inserts the same
calculator section the en/ru/id/pt homepages have (heading + note translated,
result/share strings reused from that locale's own game pages), then runs
the regular rollout + stabilize steps and the later performance cleanups."""
import os, re, sys, subprocess, importlib.util, collections

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('r', os.path.join(HERE, 'rollout.py'))
R = importlib.util.module_from_spec(spec); spec.loader.exec_module(R)
os.chdir(R.ROOT)
BASE_COMMIT = '3108b00'

TX = {
 'es': ('Estímalo gratis — aquí mismo', 'Sin registro. No se introduce ni se envía nada: todo el cálculo se hace en tu navegador.', 'Elige un juego'),
 'fr': ('Estimez-le gratuitement — ici même', "Sans inscription. Rien n'est saisi ni envoyé : tout le calcul se fait dans votre navigateur.", 'Choisissez un jeu'),
 'ar': ('قدّر قيمته مجاناً — هنا مباشرة', 'بلا تسجيل. لا يُدخَل أو يُرسَل أي شيء — الحساب كله يتم في متصفحك.', 'اختر لعبة'),
 'de': ('Kostenlos schätzen — direkt hier', 'Ohne Anmeldung. Nichts wird eingegeben oder gesendet — die ganze Berechnung läuft in deinem Browser.', 'Spiel auswählen'),
 'tr': ('Ücretsiz hesapla — hemen burada', 'Kayıt yok. Hiçbir şey girilmez ya da gönderilmez — tüm hesaplama tarayıcında yapılır.', 'Bir oyun seç'),
 'vi': ('Ước tính miễn phí — ngay tại đây', 'Không cần đăng ký. Không nhập hay gửi gì cả — toàn bộ phép tính chạy trong trình duyệt của bạn.', 'Chọn trò chơi'),
 'hi': ('मुफ़्त अनुमान — यहीं पर', 'कोई रजिस्ट्रेशन नहीं। कुछ भी दर्ज या भेजा नहीं जाता — पूरी गणना आपके ब्राउज़र में होती है।', 'गेम चुनें'),
 'it': ('Stimalo gratis — proprio qui', 'Nessuna registrazione. Non si inserisce né si invia nulla: tutto il calcolo avviene nel tuo browser.', 'Scegli un gioco'),
 'ja': ('無料で査定 — このページで', '登録不要。何も入力・送信されません。計算はすべてあなたのブラウザ内で行われます。', 'ゲームを選択'),
 'ko': ('무료로 가치 추정 — 바로 여기서', '가입 없음. 아무것도 입력하거나 전송하지 않습니다 — 모든 계산은 브라우저 안에서 이루어집니다.', '게임 선택'),
 'zh': ('免费估价——就在这里', '无需注册。不输入、不发送任何内容——所有计算都在你的浏览器中完成。', '选择游戏'),
 'pl': ('Wyceń za darmo — tutaj', 'Bez rejestracji. Nic nie jest wpisywane ani wysyłane — całe obliczenie odbywa się w Twojej przeglądarce.', 'Wybierz grę'),
 'th': ('ประเมินฟรี — ได้ที่นี่เลย', 'ไม่ต้องสมัคร ไม่มีการกรอกหรือส่งข้อมูลใด ๆ — การคำนวณทั้งหมดทำในเบราว์เซอร์ของคุณ', 'เลือกเกม'),
}

def section(lang):
    g = open(lang + '/brawl-stars.html', encoding='utf-8').read()
    note = re.search(r'<span class="vc-result-note" data-copied="([^"]*)">([^<]*)</span>', g)
    share = re.search(r'<button type="button" class="vc-share-btn">([^<]*)</button>', g)
    h2, sub, choose = TX[lang]
    return ('<!-- LIVE CALCULATOR -->\n<section class="section">\n  <h2 class="section-title">' + h2 + '</h2>\n  <p class="section-sub">' + sub + '</p>\n'
            '  <div class="value-calc" id="vc-home" data-switcher style="max-width: 480px; margin: 0 auto;">\n'
            '    <select class="vc-switcher" aria-label="' + choose + '"></select>\n    <div class="vc-sliders"></div>\n    <div class="vc-result">\n'
            '      <strong class="vc-result-value">—</strong>\n      <span class="vc-result-note" data-copied="' + note.group(1) + '">' + note.group(2) + '</span>\n'
            '      <button type="button" class="vc-share-btn">' + share.group(1) + '</button>\n    </div>\n  </div>\n</section>\n\n')

stab = importlib.util.spec_from_file_location('st', os.path.join(HERE, 'stabilize.py'))
for lang in (sys.argv[1:] or TX):
    path = lang + '/index.html'
    orig = subprocess.run(['git', 'show', BASE_COMMIT + ':' + path], capture_output=True).stdout.decode('utf-8')
    assert '<!-- HOW IT WORKS -->' in orig and 'class="value-calc"' not in orig, lang
    base = orig.replace('<!-- HOW IT WORKS -->', section(lang) + '<!-- HOW IT WORKS -->', 1)
    k = base.rindex('</body>')
    base = base[:k] + '<script src="../assets/calculators.js" defer></script>\n' + base[k:]
    open(path, 'w', encoding='utf-8', newline='').write(base)
    p = R.Page(R.ROOT + path)
    R.do_home(p)
    if not p.check():
        raise SystemExit('text check failed: ' + lang)
    s = p.s
    s = re.sub(r'<link rel="preload" href="(\.\./|\./)assets/fonts/(serif|body)\.woff2" as="font" type="font/woff2" crossorigin>\n?', '', s)
    s = s.replace('<div class="g-rain"></div>', '')
    open(path, 'w', encoding='utf-8', newline='').write(s)
    print('tool homepage:', lang)
# pre-render the calculator shell (tiles, result, CTA) like the other homepages
st = importlib.util.module_from_spec(stab); stab.loader.exec_module(st)
