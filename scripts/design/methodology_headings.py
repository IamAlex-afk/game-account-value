"""Methodology page: the seven question-style headings become plain statements. Google shows FAQ rich results
only for government/health sites since 2023, so the FAQPage JSON-LD is dropped
while the Article node stays. Idempotent. Run: python scripts/design/methodology_headings.py"""
import glob, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + os.sep
H = {
 'en': ['Where our prices come from', 'The two-listing rule: when an item counts as a value driver', 'When nothing repeats, stats set the price',
        'How often we re-check, and what the date badge means', 'What we never do with the numbers', "Why we don't copy numbers from other value calculators",
        'How many sources a number needs'],
 'ru': ['Откуда берутся наши цены', 'Правило двух объявлений: когда предмет влияет на цену', 'Если ничего не повторяется, цену задают показатели',
        'Как часто мы перепроверяем цены и что значит дата на странице', 'Чего мы никогда не делаем с цифрами', 'Почему мы не берём цифры из чужих калькуляторов',
        'Сколько источников нужно для одной цифры'],
 'es': ['De dónde salen nuestros precios', 'La regla de los dos anuncios: cuándo un objeto sube el valor', 'Si nada se repite, las estadísticas marcan el precio',
        'Cada cuánto revisamos y qué significa la fecha', 'Lo que nunca hacemos con las cifras', 'Por qué no copiamos cifras de otras calculadoras',
        'Cuántas fuentes necesita una cifra'],
 'pt': ['De onde vêm os nossos preços', 'A regra dos dois anúncios: quando um item conta para o valor', 'Se nada se repete, as estatísticas definem o preço',
        'Com que frequência revisamos e o que significa a data', 'O que nunca fazemos com os números', 'Por que não copiamos números de outras calculadoras',
        'Quantas fontes um número precisa'],
 'id': ['Dari mana harga kami berasal', 'Aturan dua listing: kapan item memengaruhi nilai', 'Jika tidak ada yang berulang, statistik yang menentukan harga',
        'Seberapa sering kami cek ulang dan arti tanggal di halaman', 'Yang tidak pernah kami lakukan dengan angka', 'Kenapa kami tidak menyalin angka dari kalkulator lain',
        'Berapa sumber yang dibutuhkan satu angka'],
 'tr': ['Fiyatlarımız nereden geliyor', 'İki ilan kuralı: bir eşya ne zaman değeri belirler', 'Hiçbir şey tekrarlanmıyorsa fiyatı istatistikler belirler',
        'Ne sıklıkla yeniden kontrol ediyoruz ve tarih rozeti ne anlama geliyor', 'Rakamlarla asla yapmadığımız şeyler', 'Neden başka hesaplayıcılardan rakam kopyalamıyoruz',
        'Bir rakam için kaç kaynak gerekir'],
 'ar': ['من أين تأتي أسعارنا', 'قاعدة الإعلانين: متى يؤثر العنصر في القيمة', 'عندما لا يتكرر شيء، تحدد الإحصاءات السعر',
        'كم مرة نعيد التحقق وماذا يعني التاريخ على الصفحة', 'ما لا نفعله أبدًا بالأرقام', 'لماذا لا ننسخ أرقامًا من حاسبات أخرى',
        'كم مصدرًا يحتاج الرقم الواحد'],
 'vi': ['Giá của chúng tôi đến từ đâu', 'Quy tắc hai tin đăng: khi nào một vật phẩm quyết định giá trị', 'Khi không có gì lặp lại, chỉ số quyết định giá',
        'Chúng tôi kiểm tra lại bao lâu một lần và ngày trên trang nghĩa là gì', 'Những điều chúng tôi không bao giờ làm với con số', 'Vì sao chúng tôi không sao chép số liệu từ máy tính khác',
        'Một con số cần bao nhiêu nguồn'],
 'hi': ['हमारी कीमतें कहाँ से आती हैं', 'दो लिस्टिंग का नियम: कोई आइटम कब कीमत बढ़ाता है', 'जब कुछ भी दोहराया न जाए, तो आँकड़े कीमत तय करते हैं',
        'हम कितनी बार दोबारा जाँचते हैं और तारीख़ वाले बैज का मतलब', 'आँकड़ों के साथ हम क्या कभी नहीं करते', 'हम दूसरे कैलकुलेटरों से आँकड़े क्यों नहीं लेते',
        'एक आँकड़े के लिए कितने स्रोत चाहिए'],
 'fr': ['D’où viennent nos prix', 'La règle des deux annonces : quand un objet fait la valeur', 'Quand rien ne se répète, les statistiques fixent le prix',
        'À quelle fréquence nous revérifions, et ce que signifie la date', 'Ce que nous ne faisons jamais avec les chiffres', 'Pourquoi nous ne reprenons pas les chiffres d’autres calculateurs',
        'Combien de sources faut-il pour un chiffre'],
 'de': ['Woher unsere Preise kommen', 'Die Zwei-Angebote-Regel: wann ein Item den Wert bestimmt', 'Wenn sich nichts wiederholt, entscheiden die Werte',
        'Wie oft wir nachprüfen und was das Datum bedeutet', 'Was wir mit Zahlen nie tun', 'Warum wir keine Zahlen aus anderen Rechnern übernehmen',
        'Wie viele Quellen eine Zahl braucht'],
 'it': ['Da dove vengono i nostri prezzi', 'La regola dei due annunci: quando un oggetto fa il valore', 'Se nulla si ripete, sono le statistiche a fare il prezzo',
        'Ogni quanto ricontrolliamo e cosa significa la data', 'Cosa non facciamo mai con i numeri', 'Perché non copiamo i numeri di altri calcolatori',
        'Quante fonti servono per un numero'],
 'ja': ['価格データの出どころ', '「2件ルール」：アイテムが価値を左右すると判断する条件', '繰り返しが見つからない場合は数値で価格が決まる',
        '再確認の頻度と日付バッジの意味', '数値について私たちが決してしないこと', '他の査定ツールの数値をそのまま使わない理由',
        '1つの数値に必要な情報源の数'],
 'ko': ['가격 데이터의 출처', '두 매물 규칙: 아이템이 가치를 좌우한다고 보는 기준', '반복되는 것이 없으면 수치가 가격을 정합니다',
        '재확인 주기와 날짜 배지의 의미', '숫자에 대해 우리가 절대 하지 않는 것', '다른 계산기의 숫자를 가져오지 않는 이유',
        '숫자 하나에 필요한 출처 수'],
 'zh': ['我们的价格从哪里来', '“两条挂单”规则：物品何时算作价值因素', '没有重复项时，由数据决定价格',
        '我们多久复核一次，日期标签代表什么', '我们绝不会对数字做的事', '为什么我们不照搬其他估值计算器的数字',
        '一个数字需要几个来源'],
 'pl': ['Skąd biorą się nasze ceny', 'Zasada dwóch ogłoszeń: kiedy przedmiot podnosi wartość', 'Gdy nic się nie powtarza, cenę wyznaczają statystyki',
        'Jak często sprawdzamy ceny ponownie i co oznacza data', 'Czego nigdy nie robimy z liczbami', 'Dlaczego nie kopiujemy liczb z innych kalkulatorów',
        'Ile źródeł potrzebuje jedna liczba'],
 'th': ['ราคาของเรามาจากไหน', 'กฎสองประกาศ: เมื่อไหร่ที่ไอเทมนับว่ามีผลต่อมูลค่า', 'เมื่อไม่มีอะไรซ้ำ ค่าสถิติจะเป็นตัวกำหนดราคา',
        'เราตรวจสอบซ้ำบ่อยแค่ไหน และวันที่บนหน้าหมายถึงอะไร', 'สิ่งที่เราไม่ทำกับตัวเลขเด็ดขาด', 'ทำไมเราไม่คัดลอกตัวเลขจากเครื่องคิดเลขอื่น',
        'ตัวเลขหนึ่งตัวต้องมีกี่แหล่งที่มา'],
 'tl': ['Saan nanggagaling ang aming presyo', 'Ang panuntunang dalawang listing: kailan nakakaapekto ang item sa halaga', 'Kapag walang umuulit, ang stats ang nagtatakda ng presyo',
        'Gaano kadalas kami nagsusuri ulit at ano ang ibig sabihin ng petsa', 'Ang hindi namin kailanman ginagawa sa mga numero', 'Bakit hindi namin kinokopya ang numero ng ibang calculator',
        'Ilang source ang kailangan ng isang numero'],
 'sw': ['Bei zetu zinatoka wapi', 'Kanuni ya matangazo mawili: lini kitu kinaamua thamani', 'Pasipo kujirudia, takwimu ndizo zinaamua bei',
        'Tunaangalia upya mara ngapi, na tarehe kwenye ukurasa inamaanisha nini', 'Tusichofanya kamwe na namba', 'Kwa nini hatunakili namba za vikokotoo vingine',
        'Namba moja inahitaji vyanzo vingapi'],
 'ms': ['Dari mana harga kami datang', 'Peraturan dua senarai: bila item mempengaruhi nilai', 'Apabila tiada yang berulang, statistik menentukan harga',
        'Berapa kerap kami semak semula dan maksud tarikh pada halaman', 'Perkara yang kami tidak pernah lakukan dengan angka', 'Kenapa kami tidak menyalin angka daripada kalkulator lain',
        'Berapa sumber yang diperlukan untuk satu angka'],
 'uz': ['Narxlarimiz qayerdan olinadi', 'Ikki eʻlon qoidasi: buyum qachon qiymatga taʻsir qiladi', 'Hech narsa takrorlanmasa, narxni koʻrsatkichlar belgilaydi',
        'Qanchalik tez-tez qayta tekshiramiz va sahifadagi sana nimani anglatadi', 'Raqamlar bilan hech qachon qilmaydigan ishlarimiz', 'Nega boshqa kalkulyatorlarning raqamlarini olmaymiz',
        'Bitta raqamga nechta manba kerak'],
 'kk': ['Бағаларымыз қайдан алынады', 'Екі хабарландыру ережесі: зат құнға қашан әсер етеді', 'Ештеңе қайталанбаса, бағаны көрсеткіштер анықтайды',
        'Қаншалықты жиі қайта тексереміз және беттегі күн нені білдіреді', 'Сандармен ешқашан жасамайтын нәрселеріміз', 'Неге басқа калькуляторлардың сандарын алмаймыз',
        'Бір санға неше дереккөз керек'],
 'tk': ['Bahalarymyz nireden gelýär', 'Iki bildiriş düzgüni: haçan bir zat bahany kesgitleýär', 'Hiç zat gaýtalanmasa, bahany görkezijiler kesgitleýär',
        'Näçe wagtdan bir gaýtadan barlaýarys we sahypadaky sene näme aňladýar', 'Sanlar bilen hiç haçan etmeýän zatlarymyz', 'Näme üçin beýleki kalkulýatorlaryň sanlaryny almaýarys',
        'Bir san üçin näçe çeşme gerek'],
 'ky': ['Бааларыбыз кайдан алынат', 'Эки жарыя эрежеси: буюм баага качан таасир этет', 'Эч нерсе кайталанбаса, бааны көрсөткүчтөр аныктайт',
        'Канчалык көп кайра текшеребиз жана барактагы дата эмнени билдирет', 'Сандар менен эч качан кылбаган нерселерибиз', 'Эмне үчүн башка калькуляторлордун сандарын албайбыз',
        'Бир санга канча булак керек'],
}


# First sentence of the 'other value calculators' section: it used to answer a question heading, so after the
# headings became statements it was left as a fragment. (old fragment, full sentence) per language.
FIRST = {
 'en': ('Differently from a real marketplace listing.',
        'We treat a number from another value calculator differently from a real marketplace listing.'),
 'ru': ('Иначе, чем к реальному листингу маркетплейса.',
        'К цифре из чужого калькулятора мы относимся иначе, чем к реальному листингу маркетплейса.'),
 'es': ('De forma diferente a un anuncio de marketplace real.',
        'Tratamos una cifra de otra calculadora de forma diferente a un anuncio real de marketplace.'),
 'pt': ('De forma diferente de um anúncio real de marketplace.',
        'Tratamos um número de outra calculadora de forma diferente de um anúncio real de marketplace.'),
 'id': ('Berbeda dari listing marketplace sungguhan.',
        'Kami memperlakukan angka dari kalkulator lain secara berbeda dari listing marketplace sungguhan.'),
 'tr': ('Gerçek bir pazar yeri ilanından farklı olarak.',
        'Başka bir hesaplayıcıdan gelen rakamı, gerçek bir pazar yeri ilanından farklı değerlendiririz.'),
 'ar': ('بشكل مختلف عن إعلان سوق حقيقي.',
        'نتعامل مع الرقم المأخوذ من حاسبة أخرى بشكل مختلف عن إعلان حقيقي في السوق.'),
 'vi': ('Khác với một tin đăng chợ thực tế.',
        'Chúng tôi xử lý con số từ một máy tính khác theo cách khác với một tin đăng thực tế trên chợ.'),
 'hi': ('असली मार्केटप्लेस लिस्टिंग से अलग तरीके से।',
        'दूसरे कैलकुलेटर के आँकड़े को हम असली मार्केटप्लेस लिस्टिंग से अलग तरीके से देखते हैं।'),
 'fr': ("Différemment d'une vraie annonce de marketplace.",
        "Nous traitons un chiffre issu d'un autre calculateur différemment d'une vraie annonce de marketplace."),
 'de': ('Anders als ein echtes Marktplatz-Angebot.',
        'Eine Zahl aus einem anderen Rechner behandeln wir anders als ein echtes Marktplatz-Angebot.'),
 'it': ("In modo diverso da un'inserzione marketplace reale.",
        "Trattiamo un numero di un altro calcolatore in modo diverso da un'inserzione reale di marketplace."),
 'ja': ('実際のマーケットプレイス出品とは異なる扱いをする。',
        '他の査定ツールの数値は、実際のマーケットプレイス出品とは異なる扱いをする。'),
 'ko': ('실제 마켓플레이스 매물과는 다르게 다룬다.',
        '다른 계산기의 숫자는 실제 마켓플레이스 매물과는 다르게 다룬다.'),
 'th': ('แตกต่างจากรายการขายบนตลาดจริง',
        'เราปฏิบัติต่อตัวเลขจากเครื่องคำนวณอื่นแตกต่างจากรายการขายบนตลาดจริง'),
 'pl': ('Inaczej niż prawdziwą ofertę rynkową.',
        'Liczbę z innego kalkulatora traktujemy inaczej niż prawdziwą ofertę rynkową.'),
 'zh': ('与真实交易平台挂牌的对待方式不同。',
        '我们对待其他估值计算器的数字，与对待真实交易平台挂牌的方式不同。'),
 'tl': ('Iba sa tunay na marketplace listing.',
        'Iba ang trato namin sa numero mula sa ibang calculator kaysa sa tunay na marketplace listing.'),
 'sw': ('Tofauti na tangazo halisi la soko.',
        'Namba kutoka kikokotoo kingine tunaichukulia tofauti na tangazo halisi la soko.'),
 'ms': ('Secara berbeza daripada iklan pasaran sebenar.',
        'Kami melayan angka daripada kalkulator lain secara berbeza daripada iklan pasaran sebenar.'),
 'uz': ('Haqiqiy bozor eʼlonidan farqli ravishda.',
        'Boshqa kalkulyatordagi raqamga biz haqiqiy bozor eʼlonidan farqli munosabatda boʻlamiz.'),
 'kk': ('Нақты нарық хабарландыруынан өзгеше.',
        'Басқа калькулятордағы санға біз нақты нарық хабарландыруынан өзгеше қараймыз.'),
 'tk': ('Hakyky bazar bildirişinden başgaça.',
        'Başga kalkulýatoryň sanyna biz hakyky bazar bildirişinden başgaça garaýarys.'),
 'ky': ('Чыныгы рынок жарыясынан башкача.',
        'Башка калькулятордогу санга биз чыныгы рынок жарыясынан башкача карайбыз.'),
}


def main():
    n = 0
    for f in ['methodology.html'] + glob.glob(ROOT + '*' + os.sep + 'methodology.html'):
        f = f if os.path.isabs(f) else ROOT + f
        lang = os.path.basename(os.path.dirname(f)) if os.path.dirname(f).rstrip(os.sep) != ROOT.rstrip(os.sep) else 'en'
        if lang not in H:
            continue
        s = open(f, encoding='utf-8').read()
        head, body = s[:s.find('<main')], s[s.find('<main'):]
        i = iter(H[lang])
        body, k = re.subn(r'(<h3[^>]*>)(.*?)(</h3>)', lambda m: m.group(1) + next(i) + m.group(3), body, count=7, flags=re.S)
        assert k == 7, (f, k)
        if FIRST[lang][1] not in body:
            body = body.replace(FIRST[lang][0], FIRST[lang][1], 1)

        def drop_faq(m):
            d = json.loads(m.group(1))
            if isinstance(d, dict) and d.get('@type') == 'FAQPage':
                return ''
            if isinstance(d, dict) and isinstance(d.get('@graph'), list):
                d['@graph'] = [x for x in d['@graph'] if x.get('@type') != 'FAQPage']
                return '<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False) + '</script>'
            return m.group(0)
        out = re.sub(r'<script type="application/ld\+json">(.*?)</script>', drop_faq, head + body, flags=re.S)
        open(f, 'w', encoding='utf-8', newline='').write(out)
        n += 1
    print('methodology headings updated:', n)


if __name__ == '__main__':
    main()
