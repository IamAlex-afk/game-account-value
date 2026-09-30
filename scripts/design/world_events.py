"""Official upcoming events per game (Oct 2026 – Mar 2027), shown inside the
world section in all 17 languages. Publisher sources only; unannounced
dates are TBA, never guessed. Checked 2026-09-28.
Date labels are pre-formatted per language by Node's Intl (CLDR): see
scripts/design/event_dates.json (built by build_event_dates.js)."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))

SC = 'https://supercell.com/en/games/brawlstars/blog/'
EVENTS = {
 'brawl-stars': [
   dict(id='bs-bow', month='2026-10', title='Brawl-O-Ween', where=None, kind='ingame', status='tba', src=(SC + 'release-notes/release-notes-august-2026/', 'Supercell')),
   dict(id='bs-lcq', start='2026-10-17', end='2026-10-18', title='BSC 2026 Last Chance Qualifier', where=('Guangzhou', 'CN'), kind='esports', status='ok', src=(SC + 'esports/last-chance-qualifier-format-2/', 'Supercell')),
   dict(id='bs-wf', start='2026-11-20', end='2026-11-22', title='Brawl Stars World Finals 2026 · $1,000,000', where=('Tokyo', 'JP'), kind='esports', status='ok', major=True, src=(SC + 'esports/brawl-stars-world-finals-format/', 'Supercell')),
   dict(id='bs-8y', start='2026-12-12', end='2026-12-12', title='Brawl Stars · 8', where=None, kind='anniv', status='fact', src=None),
 ],
 'mobile-legends': [
   dict(id='ml-enc', start='2026-11-23', end='2026-11-29', title='Esports Nations Cup 2026 · MLBB', where=('Riyadh', 'SA'), kind='esports', status='ok', src=('https://en.moonton.com/news/298.html', 'MOONTON')),
   dict(id='ml-m8wc', month=None, title='M8 World Championship · Wild Card', where=(None, 'TH'), kind='esports', status='tba', src=('https://en.moonton.com/news/299.html', 'MOONTON')),
   dict(id='ml-m8', month='2027-01', title='M8 World Championship · Finals', where=(None, 'TR'), kind='esports', status='tba', major=True, src=('https://en.moonton.com/news/299.html', 'MOONTON')),
 ],
 'free-fire': [
   dict(id='ff-wsgf', start='2026-11-06', end=None, title='Free Fire World Series 2026 · Global Finals', where=('Bangkok', 'TH'), kind='esports', status='ok', major=True, src=('https://ff.garena.com/en/article/1605/', 'Garena')),
 ],
 'clash-of-clans': [
   dict(id='coc-lcq', month='2026-10', title='Clash of Clans World Championship · Last Chance Qualifier', where=None, kind='esports', status='tba', src=('https://event.supercell.com/clashofclans/en/cups/world-championship/how-to-compete', 'Supercell')),
   dict(id='coc-wf', month=None, title='Clash of Clans World Championship 2026 · Finals · $1,000,000', where=None, kind='esports', status='tba', major=True, src=('https://event.supercell.com/clashofclans/en/cups/world-championship', 'Supercell')),
 ],
 'genshin-impact': [
   dict(id='gi-6y', start='2026-09-28', end='2026-09-28', title='Genshin Impact · 6', where=None, kind='anniv', status='fact', src=None),
 ],
}

L = {
 'en': dict(h='Upcoming official events', i='Tournaments and events announced by the publishers themselves. Dates not yet announced are marked TBA. Countdowns are calculated in your browser.',
   k=dict(esports='Esports', ingame='In-game event', anniv='Anniversary'), s=dict(ok='Confirmed', tba='Announced · date TBA', fact='Date fact'),
   anniv='{n} years since launch', tba='TBA', src='Source', online='Online',
   c=dict(days='In {n} days', tomorrow='Tomorrow', live='Live now', month='This month', done='Finished')),
 'ru': dict(h='Ближайшие официальные события', i='Турниры и события, объявленные самими издателями. Если дата ещё не объявлена, стоит пометка «уточняется». Отсчёт считается в твоём браузере.',
   k=dict(esports='Киберспорт', ingame='Событие в игре', anniv='Годовщина'), s=dict(ok='Подтверждено', tba='Объявлено · дата уточняется', fact='Дата-факт'),
   anniv='{n} лет с запуска', tba='уточняется', src='Источник', online='Онлайн',
   c=dict(days='Через {n} дн.', tomorrow='Завтра', live='Идёт сейчас', month='В этом месяце', done='Завершено')),
 'es': dict(h='Próximos eventos oficiales', i='Torneos y eventos anunciados por los propios editores. Las fechas aún no anunciadas aparecen como «por confirmar». La cuenta atrás se calcula en tu navegador.',
   k=dict(esports='Esports', ingame='Evento del juego', anniv='Aniversario'), s=dict(ok='Confirmado', tba='Anunciado · fecha por confirmar', fact='Fecha'),
   anniv='{n} años desde el lanzamiento', tba='por confirmar', src='Fuente', online='Online',
   c=dict(days='En {n} días', tomorrow='Mañana', live='En curso', month='Este mes', done='Terminado')),
 'pt': dict(h='Próximos eventos oficiais', i='Torneios e eventos anunciados pelas próprias publicadoras. Datas ainda não anunciadas aparecem como «a confirmar». A contagem regressiva é calculada no seu navegador.',
   k=dict(esports='Esports', ingame='Evento no jogo', anniv='Aniversário'), s=dict(ok='Confirmado', tba='Anunciado · data a confirmar', fact='Data'),
   anniv='{n} anos desde o lançamento', tba='a confirmar', src='Fonte', online='Online',
   c=dict(days='Em {n} dias', tomorrow='Amanhã', live='Acontecendo agora', month='Este mês', done='Encerrado')),
 'id': dict(h='Acara resmi mendatang', i='Turnamen dan acara yang diumumkan langsung oleh penerbit. Tanggal yang belum diumumkan ditandai "belum diumumkan". Hitung mundur dihitung di browser kamu.',
   k=dict(esports='Esports', ingame='Event dalam game', anniv='Ulang tahun'), s=dict(ok='Terkonfirmasi', tba='Diumumkan · tanggal menyusul', fact='Tanggal'),
   anniv='{n} tahun sejak rilis', tba='belum diumumkan', src='Sumber', online='Online',
   c=dict(days='{n} hari lagi', tomorrow='Besok', live='Sedang berlangsung', month='Bulan ini', done='Selesai')),
 'tr': dict(h='Yaklaşan resmi etkinlikler', i='Yayıncıların kendilerinin duyurduğu turnuvalar ve etkinlikler. Henüz açıklanmayan tarihler "açıklanacak" olarak işaretlenir. Geri sayım tarayıcında hesaplanır.',
   k=dict(esports='Espor', ingame='Oyun içi etkinlik', anniv='Yıl dönümü'), s=dict(ok='Onaylandı', tba='Duyuruldu · tarih açıklanacak', fact='Tarih'),
   anniv='Çıkışından bu yana {n} yıl', tba='açıklanacak', src='Kaynak', online='Çevrimiçi',
   c=dict(days='{n} gün sonra', tomorrow='Yarın', live='Şu an sürüyor', month='Bu ay', done='Bitti')),
 'ar': dict(h='الفعاليات الرسمية القادمة', i='بطولات وفعاليات أعلنها الناشرون أنفسهم. التواريخ غير المعلنة بعد مُعلَّمة بـ«يُحدَّد لاحقاً». يُحسب العد التنازلي في متصفحك.',
   k=dict(esports='رياضات إلكترونية', ingame='حدث داخل اللعبة', anniv='ذكرى سنوية'), s=dict(ok='مؤكد', tba='مُعلن · التاريخ يُحدَّد لاحقاً', fact='تاريخ'),
   anniv='{n} سنوات منذ الإطلاق', tba='يُحدَّد لاحقاً', src='المصدر', online='عبر الإنترنت',
   c=dict(days='بعد {n} يوماً', tomorrow='غداً', live='جارٍ الآن', month='هذا الشهر', done='انتهى')),
 'vi': dict(h='Sự kiện chính thức sắp tới', i='Các giải đấu và sự kiện do chính nhà phát hành công bố. Ngày chưa công bố được ghi "chưa công bố". Đếm ngược được tính trên trình duyệt của bạn.',
   k=dict(esports='Esports', ingame='Sự kiện trong game', anniv='Kỷ niệm'), s=dict(ok='Đã xác nhận', tba='Đã công bố · chưa có ngày', fact='Ngày'),
   anniv='{n} năm kể từ khi ra mắt', tba='chưa công bố', src='Nguồn', online='Trực tuyến',
   c=dict(days='Còn {n} ngày', tomorrow='Ngày mai', live='Đang diễn ra', month='Tháng này', done='Đã kết thúc')),
 'hi': dict(h='आने वाले आधिकारिक इवेंट', i='पब्लिशर द्वारा ख़ुद घोषित टूर्नामेंट और इवेंट। जिनकी तारीख़ अभी घोषित नहीं हुई, वे "घोषित होना बाकी" के रूप में दिखे हैं। काउंटडाउन आपके ब्राउज़र में गिना जाता है।',
   k=dict(esports='ईस्पोर्ट्स', ingame='इन-गेम इवेंट', anniv='सालगिरह'), s=dict(ok='पुष्टि', tba='घोषित · तारीख़ बाकी', fact='तारीख़'),
   anniv='लॉन्च के {n} साल', tba='घोषित होना बाकी', src='स्रोत', online='ऑनलाइन',
   c=dict(days='{n} दिन बाकी', tomorrow='कल', live='अभी चल रहा है', month='इस महीने', done='समाप्त')),
 'fr': dict(h='Prochains événements officiels', i='Tournois et événements annoncés par les éditeurs eux-mêmes. Les dates pas encore annoncées sont notées « à confirmer ». Les comptes à rebours sont calculés dans votre navigateur.',
   k=dict(esports='Esport', ingame='Événement en jeu', anniv='Anniversaire'), s=dict(ok='Confirmé', tba='Annoncé · date à confirmer', fact='Date'),
   anniv='{n} ans depuis la sortie', tba='à confirmer', src='Source', online='En ligne',
   c=dict(days='Dans {n} jours', tomorrow='Demain', live='En cours', month='Ce mois-ci', done='Terminé')),
 'de': dict(h='Kommende offizielle Events', i='Turniere und Events, die die Publisher selbst angekündigt haben. Noch nicht bekannte Termine sind mit „folgt“ markiert. Countdowns werden in deinem Browser berechnet.',
   k=dict(esports='E-Sport', ingame='Ingame-Event', anniv='Jubiläum'), s=dict(ok='Bestätigt', tba='Angekündigt · Termin folgt', fact='Datum'),
   anniv='{n} Jahre seit dem Start', tba='folgt', src='Quelle', online='Online',
   c=dict(days='In {n} Tagen', tomorrow='Morgen', live='Läuft gerade', month='Diesen Monat', done='Beendet')),
 'it': dict(h='Prossimi eventi ufficiali', i='Tornei ed eventi annunciati direttamente dagli editori. Le date non ancora annunciate sono indicate come «da definire». I conti alla rovescia sono calcolati nel tuo browser.',
   k=dict(esports='Esport', ingame='Evento di gioco', anniv='Anniversario'), s=dict(ok='Confermato', tba='Annunciato · data da definire', fact='Data'),
   anniv='{n} anni dal lancio', tba='da definire', src='Fonte', online='Online',
   c=dict(days='Tra {n} giorni', tomorrow='Domani', live='In corso', month='Questo mese', done='Concluso')),
 'ja': dict(h='今後の公式イベント', i='パブリッシャー自身が発表した大会とイベントです。日付未発表のものは「未定」と表示しています。カウントダウンはブラウザ内で計算されます。',
   k=dict(esports='eスポーツ', ingame='ゲーム内イベント', anniv='周年'), s=dict(ok='確定', tba='発表済み・日程未定', fact='日付'),
   anniv='リリースから{n}周年', tba='未定', src='出典', online='オンライン',
   c=dict(days='あと{n}日', tomorrow='明日', live='開催中', month='今月', done='終了')),
 'ko': dict(h='다가오는 공식 이벤트', i='퍼블리셔가 직접 발표한 대회와 이벤트입니다. 아직 발표되지 않은 날짜는 "미정"으로 표시합니다. 카운트다운은 브라우저에서 계산됩니다.',
   k=dict(esports='e스포츠', ingame='게임 내 이벤트', anniv='주년'), s=dict(ok='확정', tba='발표됨 · 날짜 미정', fact='날짜'),
   anniv='출시 {n}주년', tba='미정', src='출처', online='온라인',
   c=dict(days='{n}일 남음', tomorrow='내일', live='진행 중', month='이번 달', done='종료')),
 'th': dict(h='กิจกรรมทางการที่กำลังจะมาถึง', i='การแข่งขันและกิจกรรมที่ผู้จัดจำหน่ายประกาศเอง วันที่ที่ยังไม่ประกาศจะแสดงว่า "รอประกาศ" การนับถอยหลังคำนวณในเบราว์เซอร์ของคุณ',
   k=dict(esports='อีสปอร์ต', ingame='กิจกรรมในเกม', anniv='ครบรอบ'), s=dict(ok='ยืนยันแล้ว', tba='ประกาศแล้ว · รอวันที่', fact='วันที่'),
   anniv='ครบ {n} ปีนับจากเปิดตัว', tba='รอประกาศ', src='แหล่งที่มา', online='ออนไลน์',
   c=dict(days='อีก {n} วัน', tomorrow='พรุ่งนี้', live='กำลังจัดอยู่', month='เดือนนี้', done='จบแล้ว')),
 'pl': dict(h='Nadchodzące oficjalne wydarzenia', i='Turnieje i wydarzenia ogłoszone przez samych wydawców. Daty jeszcze nieogłoszone są oznaczone jako „do ustalenia”. Odliczanie jest liczone w Twojej przeglądarce.',
   k=dict(esports='E-sport', ingame='Wydarzenie w grze', anniv='Rocznica'), s=dict(ok='Potwierdzone', tba='Ogłoszone · data do ustalenia', fact='Data'),
   anniv='{n} lat od premiery', tba='do ustalenia', src='Źródło', online='Online',
   c=dict(days='Za {n} dni', tomorrow='Jutro', live='Trwa teraz', month='W tym miesiącu', done='Zakończone')),
 'zh': dict(h='即将到来的官方活动', i='由发行商官方公布的赛事与活动。尚未公布的日期标注为"待定"。倒计时在您的浏览器中计算。',
   k=dict(esports='电竞', ingame='游戏内活动', anniv='周年'), s=dict(ok='已确认', tba='已公布 · 日期待定', fact='日期'),
   anniv='上线{n}周年', tba='待定', src='来源', online='线上',
   c=dict(days='还有{n}天', tomorrow='明天', live='进行中', month='本月', done='已结束')),
}

DATES = json.load(open(os.path.join(HERE, 'event_dates.json'), encoding='utf-8'))

def render_events(game, lang, names):
    evs = EVENTS.get(game)
    if not evs:
        return ''
    t = L[lang]; lab = t['c']
    attrs = ' '.join('data-l-' + k + '="' + v + '"' for k, v in lab.items())
    items = []
    for e in evs:
        date_txt = DATES[e['id']][lang] if e['id'] in DATES else t['tba']
        data = ''
        if e.get('start'):
            data = ' data-start="' + e['start'] + '"' + (' data-end="' + e['end'] + '"' if e.get('end') else '')
        elif e.get('month'):
            data = ' data-month="' + e['month'] + '"'
        title = e['title']
        if e['kind'] == 'anniv':
            n = title.split('·')[-1].strip(); title = title.split('·')[0].strip() + ' · ' + t['anniv'].format(n=n)
        where = ''
        if e.get('where'):
            city, cc = e['where']
            where = '<span class="ev-where">' + ((city + ', ') if city else '') + names['countries'][lang][cc] + '</span>'
        src = ('<p class="ev-src">' + t['src'] + ': <a href="' + e['src'][0] + '" target="_blank" rel="noopener">' + e['src'][1] + '</a></p>') if e.get('src') else ''
        st_cls = {'ok': 'ev-ok', 'tba': 'ev-ann', 'fact': 'ev-fact'}[e['status']]
        items.append('<li class="ev' + (' ev-major' if e.get('major') else '') + '"' + data + '><div class="ev-date"><time' +
                     ((' datetime="' + (e.get('start') or e.get('month')) + '"') if (e.get('start') or e.get('month')) else '') + '>' + date_txt + '</time></div>'
                     '<div class="ev-body"><p class="ev-tags"><span class="ev-kind">' + t['k'][e['kind']] + '</span><span class="ev-status ' + st_cls + '">' + t['s'][e['status']] +
                     '</span><span class="ev-count"></span></p><h3>' + title + '</h3>' + where + src + '</div></li>')
    return ('<h3>📅 ' + t['h'] + '</h3><p class="wm-intro">' + t['i'] + '</p><ol class="ev-list" ' + attrs + '>' + ''.join(items) + '</ol>')


# ---- schema.org Event (Google event rich results) ------------------------
# Only in-person events with a confirmed start date (Google excludes
# virtual-only and undated events). Mirrors the visible timeline.
VENUE = {'bs-lcq': ('Guangzhou', 'Guangzhou', 'CN'), 'bs-wf': ('Tokyo Metropolitan Gymnasium', 'Tokyo', 'JP'),
         'ml-enc': ('Riyadh', 'Riyadh', 'SA'), 'ff-wsgf': ('Bangkok', 'Bangkok', 'TH')}

def render_event_ld(game):
    out = []
    for e in EVENTS.get(game, []):
        if e['id'] not in VENUE or not e.get('start') or e['status'] != 'ok':
            continue
        name, city, cc = VENUE[e['id']]
        ev = {'@context': 'https://schema.org', '@type': 'Event', 'name': e['title'].split(' · $')[0],
              'startDate': e['start'], 'eventStatus': 'https://schema.org/EventScheduled',
              'eventAttendanceMode': 'https://schema.org/OfflineEventAttendanceMode',
              'location': {'@type': 'Place', 'name': name, 'address': {'@type': 'PostalAddress', 'addressLocality': city, 'addressCountry': cc}},
              'organizer': {'@type': 'Organization', 'name': e['src'][1]}, 'url': e['src'][0]}
        if e.get('end'):
            ev['endDate'] = e['end']
        out.append(ev)
    if not out:
        return ''
    return '<script type="application/ld+json">' + json.dumps(out if len(out) > 1 else out[0], ensure_ascii=False) + '</script>'

# Malay (2026-09-30)
L['ms'] = {'anniv': '{n} tahun sejak pelancaran',
 'c': {'days': 'Dalam {n} hari', 'done': 'Selesai', 'live': 'Sedang berlangsung', 'month': 'Bulan ini', 'tomorrow': 'Esok'},
 'h': 'Acara rasmi akan datang',
 'i': 'Kejohanan dan acara yang diumumkan oleh penerbit sendiri. Tarikh yang belum diumumkan ditanda TBA. Kiraan detik dikira dalam pelayar anda.',
 'k': {'anniv': 'Ulang tahun', 'esports': 'E-sukan', 'ingame': 'Acara dalam permainan'},
 'online': 'Dalam talian',
 's': {'fact': 'Fakta tarikh', 'ok': 'Disahkan', 'tba': 'Diumumkan · tarikh TBA'},
 'src': 'Sumber',
 'tba': 'TBA'}

# Uzbek (2026-09-30)
L['uz'] = {'anniv': 'chiqqaniga {n} yil',
 'c': {'days': '{n} kundan keyin', 'done': 'Yakunlangan', 'live': 'Hozir efirda', 'month': 'Shu oy', 'tomorrow': 'Ertaga'},
 'h': 'Yaqinlashayotgan rasmiy tadbirlar',
 'i': 'Noshirlarning oʻzlari eʼlon qilgan turnirlar va tadbirlar. Hali eʼlon qilinmagan sanalar TBA deb belgilangan. Teskari sanoq brauzeringizda hisoblanadi.',
 'k': {'anniv': 'Yubiley', 'esports': 'Kibersport', 'ingame': 'Oʻyin ichidagi tadbir'},
 'online': 'Onlayn',
 's': {'fact': 'Sana fakti', 'ok': 'Tasdiqlangan', 'tba': 'Eʼlon qilingan · sana TBA'},
 'src': 'Manba',
 'tba': 'TBA'}
