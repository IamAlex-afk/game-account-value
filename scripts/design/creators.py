"""Creators block (2026-10-06), rendered from scripts/research/streamers.json (official YouTube Data API v3 +
Twitch Helix API data, every row with its own source and check date — see scripts/research/streamers.py).
- render_creators(game, lang, game_name): replaces the old global Twitch table in a game page's world section
  when that language has verified data; '' otherwise (the old table stays).
- render_home_creators(lang): homepage block, the most-subscribed verified YouTube creator per game in the
  page language; '' when there is no data.
Only languages with UI strings in T are rendered. Wording states the metric ("most subscribers"), never a bare
"most popular" without a number."""
import html, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "research", "streamers.json")
GAMES = {"roblox": "Roblox", "brawl-stars": "Brawl Stars", "clash-of-clans": "Clash of Clans", "clash-royale": "Clash Royale",
         "free-fire": "Free Fire", "genshin-impact": "Genshin Impact", "mobile-legends": "Mobile Legends",
         "fortnite": "Fortnite", "minecraft": "Minecraft"}
SEP = {"en": ",", "hi": ",", "th": ",", "ar": ",", "pt": ".", "es": ".", "id": ".", "tr": ".", "vi": ".", "ru": " "}

# h: section title · intro · yt/tw table titles · columns · q/a templates · rules · home title/intro
T = {
 "en": dict(h="{game} creators in English", intro="Channels that mainly post about {game}, in English, ranked by public numbers from YouTube and Twitch. Each figure links to the channel and shows when it was checked.",
            yt="YouTube — most subscribers", tw="Twitch — most followers", c=("Channel", "Subscribers", "Checked"), ctw=("Channel", "Followers", "Checked"),
            q="Who is the most popular {game} YouTuber in English?", a="By subscribers: {name} — {n} subscribers on YouTube (checked {d}).",
            qt="Who is the most-followed {game} streamer in English on Twitch?", at="By followers: {name} — {n} followers on Twitch (checked {d}).",
            rules="How we pick channels: at least 6 of the last 10 uploads are about {game} and the language is confirmed by YouTube or Twitch data. YouTube shows rounded subscriber numbers. Twitch lists channels seen live in the {game} category in this language.",
            home="Top creators in English by game", home_i="The most-subscribed YouTube channel about each game in English, with the date checked.", more="All {game} creators"),
 "ru": dict(h="Авторы по {game} на русском", intro="Каналы, которые в основном выпускают видео про {game} на русском, по открытым цифрам YouTube и Twitch. У каждой цифры — ссылка на канал и дата проверки.",
            yt="YouTube — больше всего подписчиков", tw="Twitch — больше всего фолловеров", c=("Канал", "Подписчики", "Проверено"), ctw=("Канал", "Фолловеры", "Проверено"),
            q="Кто самый популярный ютубер по {game} на русском?", a="По числу подписчиков — {name}: {n} подписчиков на YouTube (проверено {d}).",
            qt="Кто самый популярный стример {game} на русском на Twitch?", at="По числу фолловеров — {name}: {n} фолловеров на Twitch (проверено {d}).",
            rules="Как отбираем каналы: не меньше 6 из последних 10 видео — про {game}, язык подтверждён данными YouTube или Twitch. YouTube показывает округлённое число подписчиков. В список Twitch попадают каналы, которые мы видели в эфире в категории {game} на этом языке.",
            home="Топ авторов на русском по играм", home_i="Самый крупный по подписчикам YouTube-канал про каждую игру на русском, с датой проверки.", more="Все авторы по {game}"),
 "pt": dict(h="Criadores de {game} em português", intro="Canais que postam principalmente sobre {game} em português, classificados pelos números públicos do YouTube e da Twitch. Cada número leva ao canal e mostra quando foi conferido.",
            yt="YouTube — mais inscritos", tw="Twitch — mais seguidores", c=("Canal", "Inscritos", "Conferido"), ctw=("Canal", "Seguidores", "Conferido"),
            q="Qual é o youtuber de {game} mais popular em português?", a="Por inscritos: {name} — {n} inscritos no YouTube (conferido em {d}).",
            qt="Qual é o streamer de {game} com mais seguidores na Twitch em português?", at="Por seguidores: {name} — {n} seguidores na Twitch (conferido em {d}).",
            rules="Como escolhemos os canais: pelo menos 6 dos últimos 10 vídeos são sobre {game} e o idioma é confirmado pelos dados do YouTube ou da Twitch. O YouTube mostra o número de inscritos arredondado. Na Twitch entram canais vistos ao vivo na categoria {game} neste idioma.",
            home="Maiores criadores em português por jogo", home_i="O canal do YouTube com mais inscritos sobre cada jogo em português, com a data da conferência.", more="Todos os criadores de {game}"),
 "es": dict(h="Creadores de {game} en español", intro="Canales que publican sobre todo de {game} en español, ordenados por las cifras públicas de YouTube y Twitch. Cada cifra enlaza al canal e indica cuándo se comprobó.",
            yt="YouTube — más suscriptores", tw="Twitch — más seguidores", c=("Canal", "Suscriptores", "Comprobado"), ctw=("Canal", "Seguidores", "Comprobado"),
            q="¿Quién es el youtuber de {game} más popular en español?", a="Por suscriptores: {name} — {n} suscriptores en YouTube (comprobado el {d}).",
            qt="¿Qué streamer de {game} en español tiene más seguidores en Twitch?", at="Por seguidores: {name} — {n} seguidores en Twitch (comprobado el {d}).",
            rules="Cómo elegimos los canales: al menos 6 de los últimos 10 vídeos son de {game} y el idioma está confirmado por los datos de YouTube o Twitch. YouTube muestra los suscriptores redondeados. En Twitch entran canales vistos en directo en la categoría {game} en este idioma.",
            home="Mayores creadores en español por juego", home_i="El canal de YouTube con más suscriptores sobre cada juego en español, con la fecha de comprobación.", more="Todos los creadores de {game}"),
 "ar": dict(h="صنّاع محتوى {game} بالعربية", intro="قنوات تنشر غالبًا عن {game} باللغة العربية، مرتبة حسب الأرقام العامة من YouTube وTwitch. كل رقم يرتبط بالقناة ويُظهر تاريخ التحقق.",
            yt="YouTube — الأكثر مشتركين", tw="Twitch — الأكثر متابعين", c=("القناة", "المشتركون", "تاريخ التحقق"), ctw=("القناة", "المتابعون", "تاريخ التحقق"),
            q="من هو أشهر يوتيوبر في {game} بالعربية؟", a="حسب عدد المشتركين: {name} — {n} مشترك على YouTube (تم التحقق {d}).",
            qt="من هو أكثر ستريمر متابعة في {game} بالعربية على Twitch؟", at="حسب عدد المتابعين: {name} — {n} متابع على Twitch (تم التحقق {d}).",
            rules="كيف نختار القنوات: 6 على الأقل من آخر 10 فيديوهات عن {game}، واللغة مؤكدة من بيانات YouTube أو Twitch. يعرض YouTube عدد المشتركين بشكل تقريبي. في Twitch نُدرج القنوات التي شوهدت مباشرة في فئة {game} بهذه اللغة.",
            home="أكبر صنّاع المحتوى بالعربية حسب اللعبة", home_i="قناة YouTube الأكثر مشتركين عن كل لعبة بالعربية، مع تاريخ التحقق.", more="كل صنّاع محتوى {game}"),
 "id": dict(h="Kreator {game} berbahasa Indonesia", intro="Channel yang terutama membahas {game} dalam bahasa Indonesia, diurutkan berdasarkan angka publik dari YouTube dan Twitch. Setiap angka tertaut ke channel dan menunjukkan tanggal pengecekan.",
            yt="YouTube — subscriber terbanyak", tw="Twitch — follower terbanyak", c=("Channel", "Subscriber", "Dicek"), ctw=("Channel", "Follower", "Dicek"),
            q="Siapa YouTuber {game} paling populer berbahasa Indonesia?", a="Berdasarkan subscriber: {name} — {n} subscriber di YouTube (dicek {d}).",
            qt="Siapa streamer {game} berbahasa Indonesia dengan follower terbanyak di Twitch?", at="Berdasarkan follower: {name} — {n} follower di Twitch (dicek {d}).",
            rules="Cara kami memilih channel: minimal 6 dari 10 video terakhir membahas {game} dan bahasanya dikonfirmasi oleh data YouTube atau Twitch. YouTube menampilkan jumlah subscriber yang dibulatkan. Di Twitch kami mencantumkan channel yang terlihat live di kategori {game} dalam bahasa ini.",
            home="Kreator terbesar berbahasa Indonesia per game", home_i="Channel YouTube dengan subscriber terbanyak untuk tiap game dalam bahasa Indonesia, dengan tanggal pengecekan.", more="Semua kreator {game}"),
 "tr": dict(h="Türkçe {game} içerik üreticileri", intro="Ağırlıklı olarak Türkçe {game} içeriği paylaşan kanallar, YouTube ve Twitch'in herkese açık sayılarına göre sıralandı. Her sayı kanala bağlanır ve kontrol tarihini gösterir.",
            yt="YouTube — en çok abone", tw="Twitch — en çok takipçi", c=("Kanal", "Abone", "Kontrol"), ctw=("Kanal", "Takipçi", "Kontrol"),
            q="En popüler Türkçe {game} YouTuber'ı kim?", a="Abone sayısına göre: {name} — YouTube'da {n} abone ({d} tarihinde kontrol edildi).",
            qt="Twitch'te en çok takipçisi olan Türkçe {game} yayıncısı kim?", at="Takipçi sayısına göre: {name} — Twitch'te {n} takipçi ({d} tarihinde kontrol edildi).",
            rules="Kanalları nasıl seçiyoruz: son 10 videonun en az 6'sı {game} hakkında ve dil YouTube ya da Twitch verisiyle doğrulanıyor. YouTube abone sayısını yuvarlanmış gösterir. Twitch listesinde bu dilde {game} kategorisinde canlı görülen kanallar yer alır.",
            home="Oyunlara göre en büyük Türkçe içerik üreticileri", home_i="Her oyun için Türkçe en çok aboneye sahip YouTube kanalı, kontrol tarihiyle.", more="Tüm {game} içerik üreticileri"),
 "vi": dict(h="Nhà sáng tạo {game} tiếng Việt", intro="Các kênh chủ yếu làm nội dung {game} bằng tiếng Việt, xếp theo số liệu công khai của YouTube và Twitch. Mỗi con số đều dẫn tới kênh và ghi ngày kiểm tra.",
            yt="YouTube — nhiều người đăng ký nhất", tw="Twitch — nhiều người theo dõi nhất", c=("Kênh", "Người đăng ký", "Kiểm tra"), ctw=("Kênh", "Người theo dõi", "Kiểm tra"),
            q="YouTuber {game} tiếng Việt nổi tiếng nhất là ai?", a="Theo số người đăng ký: {name} — {n} người đăng ký trên YouTube (kiểm tra ngày {d}).",
            qt="Streamer {game} tiếng Việt nào có nhiều người theo dõi nhất trên Twitch?", at="Theo số người theo dõi: {name} — {n} người theo dõi trên Twitch (kiểm tra ngày {d}).",
            rules="Cách chọn kênh: ít nhất 6 trong 10 video gần nhất nói về {game} và ngôn ngữ được xác nhận bằng dữ liệu YouTube hoặc Twitch. YouTube hiển thị số người đăng ký đã làm tròn. Danh sách Twitch gồm các kênh từng phát trực tiếp trong mục {game} bằng ngôn ngữ này.",
            home="Nhà sáng tạo tiếng Việt lớn nhất theo game", home_i="Kênh YouTube có nhiều người đăng ký nhất về từng game bằng tiếng Việt, kèm ngày kiểm tra.", more="Tất cả nhà sáng tạo {game}"),
 "hi": dict(h="{game} के हिंदी क्रिएटर", intro="ऐसे चैनल जो ज़्यादातर हिंदी में {game} पर वीडियो बनाते हैं, YouTube और Twitch के सार्वजनिक आंकड़ों के अनुसार। हर आंकड़ा चैनल से जुड़ा है और जाँच की तारीख़ दिखाता है।",
            yt="YouTube — सबसे ज़्यादा सब्सक्राइबर", tw="Twitch — सबसे ज़्यादा फ़ॉलोअर", c=("चैनल", "सब्सक्राइबर", "जाँच"), ctw=("चैनल", "फ़ॉलोअर", "जाँच"),
            q="हिंदी में सबसे लोकप्रिय {game} यूट्यूबर कौन है?", a="सब्सक्राइबर के आधार पर: {name} — YouTube पर {n} सब्सक्राइबर ({d} को जाँचा गया)।",
            qt="Twitch पर सबसे ज़्यादा फ़ॉलो किया जाने वाला हिंदी {game} स्ट्रीमर कौन है?", at="फ़ॉलोअर के आधार पर: {name} — Twitch पर {n} फ़ॉलोअर ({d} को जाँचा गया)।",
            rules="हम चैनल कैसे चुनते हैं: पिछले 10 वीडियो में से कम से कम 6 {game} पर हों और भाषा की पुष्टि YouTube या Twitch के डेटा से हो। YouTube सब्सक्राइबर संख्या को राउंड करके दिखाता है। Twitch सूची में वे चैनल हैं जो इस भाषा में {game} श्रेणी में लाइव दिखे।",
            home="गेम के अनुसार सबसे बड़े हिंदी क्रिएटर", home_i="हर गेम पर हिंदी में सबसे ज़्यादा सब्सक्राइबर वाला YouTube चैनल, जाँच की तारीख़ के साथ।", more="{game} के सभी क्रिएटर"),
 "th": dict(h="ครีเอเตอร์ {game} ภาษาไทย", intro="ช่องที่ทำคอนเทนต์ {game} เป็นภาษาไทยเป็นหลัก เรียงตามตัวเลขสาธารณะจาก YouTube และ Twitch ทุกตัวเลขลิงก์ไปยังช่องและระบุวันที่ตรวจสอบ",
            yt="YouTube — ผู้ติดตามมากที่สุด", tw="Twitch — ผู้ติดตามมากที่สุด", c=("ช่อง", "ผู้ติดตาม", "ตรวจสอบ"), ctw=("ช่อง", "ผู้ติดตาม", "ตรวจสอบ"),
            q="ยูทูบเบอร์ {game} ภาษาไทยที่ได้รับความนิยมมากที่สุดคือใคร?", a="ตามจำนวนผู้ติดตาม: {name} — ผู้ติดตาม {n} คนบน YouTube (ตรวจสอบ {d})",
            qt="สตรีมเมอร์ {game} ภาษาไทยที่มีผู้ติดตามมากที่สุดบน Twitch คือใคร?", at="ตามจำนวนผู้ติดตาม: {name} — ผู้ติดตาม {n} คนบน Twitch (ตรวจสอบ {d})",
            rules="วิธีคัดเลือกช่อง: อย่างน้อย 6 จาก 10 วิดีโอล่าสุดเป็นเรื่อง {game} และภาษายืนยันได้จากข้อมูล YouTube หรือ Twitch YouTube แสดงจำนวนผู้ติดตามแบบปัดเศษ รายชื่อ Twitch คือช่องที่เห็นไลฟ์ในหมวด {game} ด้วยภาษานี้",
            home="ครีเอเตอร์ภาษาไทยรายใหญ่แยกตามเกม", home_i="ช่อง YouTube ที่มีผู้ติดตามมากที่สุดของแต่ละเกมในภาษาไทย พร้อมวันที่ตรวจสอบ", more="ครีเอเตอร์ {game} ทั้งหมด"),
}


def _load():
    try:
        return json.load(open(DATA, encoding="utf-8"))
    except FileNotFoundError:
        return {}


def _num(n, lang):
    return f"{n:,}".replace(",", SEP.get(lang, ","))


MAX_AGE_DAYS = 30   # YouTube API Services Developer Policies: delete or refresh stored API data within 30 days


def _fresh(r):
    import datetime
    try:
        return (datetime.date.today() - datetime.date.fromisoformat(r["checked"])).days <= MAX_AGE_DAYS
    except (KeyError, ValueError):
        return False


def _rank(d, key, k=10):
    return sorted((r for r in d.values() if _fresh(r)), key=lambda r: -(r.get(key) or 0))[:k]


def _a(r):
    return f'<a href="{html.escape(r["url"])}" target="_blank" rel="noopener">{html.escape(r["name"])}</a>'


def render_creators(game, lang, game_name):
    if lang not in T:
        return ""
    d = _load().get(game, {}).get(lang, {})
    yt, tw = _rank(d.get("youtube", {}), "subscribers"), _rank(d.get("twitch", {}), "followers")
    if not yt and not tw:
        return ""
    t = T[lang]; out = [f'<h3>📺 {t["h"].format(game=game_name)}</h3><p class="wm-intro">{t["intro"].format(game=game_name)}</p>']
    if yt:
        out.append(f'<p class="wm-qa"><strong>{t["q"].format(game=game_name)}</strong> ' +
                   t["a"].format(name=_a(yt[0]), n=_num(yt[0]["subscribers"], lang), d=yt[0]["checked"]) + "</p>")
    if tw:
        out.append(f'<p class="wm-qa"><strong>{t["qt"].format(game=game_name)}</strong> ' +
                   t["at"].format(name=_a(tw[0]), n=_num(tw[0]["followers"], lang), d=tw[0]["checked"]) + "</p>")
    for rows, title, cols, key in ((yt, t["yt"], t["c"], "subscribers"), (tw, t["tw"], t["ctw"], "followers")):
        if not rows:
            continue
        body = "".join(f'<tr><th scope="row">{_a(r)}</th><td data-l="{cols[1]}" class="wm-num">{_num(r[key], lang)}</td>'
                       f'<td data-l="{cols[2]}">{r["checked"]}</td></tr>' for r in rows)
        out.append(f'<h4>{title}</h4><div class="wm-wrap"><table class="wm-table wm-small"><thead><tr>' +
                   "".join(f'<th scope="col">{c}</th>' for c in cols) + f"</tr></thead><tbody>{body}</tbody></table></div>")
    src = []   # attribution required by the YouTube API Services policies
    if yt: src.append('<a href="https://www.youtube.com/" target="_blank" rel="noopener">YouTube</a> (YouTube Data API)')
    if tw: src.append('<a href="https://www.twitch.tv/" target="_blank" rel="noopener">Twitch</a> (Twitch API)')
    out.append(f'<p class="wm-note">{t["rules"].format(game=game_name)} · ' + " · ".join(src) + "</p>")
    return "".join(out)


def render_home_creators(lang):
    if lang not in T:
        return ""
    data, t, rows = _load(), T[lang], []
    for g, gname in GAMES.items():
        yt = _rank(data.get(g, {}).get(lang, {}).get("youtube", {}), "subscribers", 1)
        if yt:
            r = yt[0]
            rows.append(f'<tr><th scope="row"><a href="./{g}.html#world">{gname}</a></th><td>{_a(r)}</td>'
                        f'<td class="wm-num">{_num(r["subscribers"], lang)}</td><td>{r["checked"]}</td></tr>')
    if len(rows) < 3:
        return ""
    import nav_menu
    cols = (nav_menu.L[lang][0], t["c"][0], t["c"][1], t["c"][2])     # 'Games' header in the page language
    return (f'<section class="section g-creators" id="creators"><h2 class="section-title">{t["home"]}</h2>'
            f'<p class="section-sub">{t["home_i"]}</p><div class="wm-wrap"><table class="wm-table wm-small"><thead><tr>' +
            "".join(f'<th scope="col">{c}</th>' for c in cols) + "</tr></thead><tbody>" + "".join(rows) + "</tbody></table></div></section>")
