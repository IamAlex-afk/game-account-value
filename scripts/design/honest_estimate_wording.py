"""Honest wording (owner, 2026-10-06): the site gives a rough range, the bot a MORE precise estimate —
never "exact". Scoped to the two places that promised it: the calculator subtitle on game pages
(<div class="vc-subtitle">) and the homepage bot button (text + aria-label). Idempotent.
Run: python scripts/design/honest_estimate_wording.py"""
import glob, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + os.sep

# calculator subtitle: (old phrase, new phrase) per language — comparative, not absolute
SUB = {
    "en": [("gives an exact estimate from screenshots", "gives a more precise estimate from screenshots")],
    "ar": [("تقديرًا دقيقًا من لقطات الشاشة", "تقديرًا أدق من لقطات الشاشة")],
    "de": [("eine genaue Schätzung aus Screenshots", "eine genauere Schätzung aus Screenshots")],
    "es": [("una estimación exacta a partir de", "una estimación más precisa a partir de")],
    "fr": [("une estimation exacte à partir de", "une estimation plus précise à partir de")],
    "hi": [("स्क्रीनशॉट से सटीक एस्टिमेट देता है", "स्क्रीनशॉट से ज़्यादा सटीक एस्टिमेट देता है")],
    "id": [("estimasi akurat dari screenshot", "estimasi yang lebih akurat dari screenshot")],
    "it": [("una stima esatta dagli screenshot", "una stima più precisa dagli screenshot")],
    "ja": [("正確な見積もりを提供する", "より正確な見積もりを提供する")],
    "kk": [("нақты баға береді", "дәлірек баға береді")],
    "ko": [("정확한 추정치를 제공한다", "더 정확한 추정치를 제공한다"), ("정확한 추정치를 제공합니다", "더 정확한 추정치를 제공합니다")],
    "ky": [("так баа берет", "тагыраак баа берет")],
    "ms": [("anggaran tepat daripada", "anggaran yang lebih tepat daripada")],
    "pl": [("dokładny szacunek na podstawie", "dokładniejszy szacunek na podstawie")],
    "pt": [("uma estimativa exata a partir de", "uma estimativa mais precisa a partir de")],
    "ru": [("Точную оценку по скриншотам даёт бот", "Более точную оценку по скриншотам даёт бот"),
           ("; точную оценку по скриншотам даёт бот", "; более точную оценку по скриншотам даёт бот")],
    "sw": [("makadirio sahihi kutoka picha", "makadirio sahihi zaidi kutoka picha")],
    "th": [("ค่าประมาณที่แม่นยำจากภาพหน้าจอ", "ค่าประมาณที่แม่นยำกว่าจากภาพหน้าจอ")],
    "tk": [("takyk baha berýär", "has takyk baha berýär")],
    "tl": [("ng eksaktong tantiya", "ng mas eksaktong tantiya")],
    "tr": [("kesin bir tahmin verir", "daha kesin bir tahmin verir")],
    "uz": [("aniq baho beradi", "aniqroq baho beradi")],
    "vi": [("ước tính chính xác từ ảnh", "ước tính chính xác hơn từ ảnh")],
    "zh": [("给出精确估值", "给出更精确的估值")],
}
# homepage bot button (only the languages whose button promised an exact/precise estimate)
BTN = {
    "en": ("Get Exact Estimate via Bot", "Get a More Precise Estimate via Bot"),
    "kk": ("Бот арқылы нақты баға алу", "Бот арқылы дәлірек баға алу"),
    "ky": ("Бот аркылуу так баа алуу", "Бот аркылуу тагыраак баа алуу"),
    "ms": ("Dapatkan Anggaran Tepat melalui Bot", "Dapatkan Anggaran Lebih Tepat melalui Bot"),
    "sw": ("Pata Makadirio Sahihi kupitia Bot", "Pata Makadirio Sahihi Zaidi kupitia Bot"),
    "tk": ("Bot arkaly takyk baha almak", "Bot arkaly has takyk baha almak"),
    "tl": ("Kumuha ng Eksaktong Tantiya sa Bot", "Kumuha ng Mas Eksaktong Tantiya sa Bot"),
    "uz": ("Bot orqali aniq baho olish", "Bot orqali aniqroq baho olish"),
}

sub_n = btn_n = 0
for lang, pairs in SUB.items():
    pre = ROOT + ("" if lang == "en" else lang + os.sep)
    for f in glob.glob(pre + "*.html"):
        s = open(f, encoding="utf-8").read()
        def fix(m):
            t = m.group(1)
            for old, new in pairs:
                if new not in t:
                    t = t.replace(old, new)
            return '<div class="vc-subtitle">' + t + "</div>"
        u = re.sub(r'<div class="vc-subtitle">([^<]*)</div>', fix, s)
        if lang in BTN and f.endswith(os.sep + "index.html"):
            old, new = BTN[lang]
            if old in u:
                u = u.replace(old, new); btn_n += 1
        if u != s:
            open(f, "w", encoding="utf-8", newline="").write(u); sub_n += 1
print("pages changed:", sub_n, "| homepage buttons:", btn_n)
