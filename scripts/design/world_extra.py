"""Extra blocks for the world section: esports prize money by country,
top earners, most-watched live streamers. Data from aggregators, labelled
as such, with dates. Imported by world_markets.py."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from world_data import EXTRA as _MORE, TW_ONLY

HERE = os.path.dirname(os.path.abspath(__file__))
NAMES = json.load(open(os.path.join(HERE, 'country_names.json'), encoding='utf-8'))
LANG_COUNTRY = {'en': 'US', 'es': 'ES', 'pt': 'BR', 'ru': 'RU', 'de': 'DE', 'fr': 'FR', 'it': 'IT', 'pl': 'PL', 'ja': 'JP', 'zh': 'CN',
                'ko': 'KR', 'tr': 'TR', 'id': 'ID', 'vi': 'VN', 'th': 'TH', 'hi': 'IN', 'ar': None}
FLAGS = {c: chr(0x1F1E6 + ord(c[0]) - 65) + chr(0x1F1E6 + ord(c[1]) - 65) for c in NAMES['countries']['en']}

EXTRA = {
  'brawl-stars': dict(
    esports=dict(src=('Esports Earnings', 'https://www.esportsearnings.com/games/586-brawl-stars/countries'), total='$9,171,511.80', tournaments=210,
                 span='2019-02 – 2024-11',
                 rows=[('JP', '$2,229,688', 87), ('BR', '$786,542', 53), ('ES', '$755,104', 46), ('US', '$653,592', 49), ('DE', '$580,053', 10),
                       ('CA', '$433,583', 15), ('PL', '$417,667', 6), ('SG', '$370,167', 48), ('IT', '$366,909', 13), ('MX', '$304,254', 33),
                       ('GB', '$283,608', 9), ('CN', '$282,886', 57), ('FR', '$249,781', 28), ('PR', '$205,267', 4), ('RU', '$192,650', 25)]),
    players=dict(src=('Esports Earnings', 'https://www.esportsearnings.com/games/586-brawl-stars'),
                 rows=[('Tensai', 'JP', '$423,833'), ('sitetampo', 'JP', '$348,500'), ('Achapi', 'JP', '$291,167'), ('Symantec', 'DE', '$246,582'), ('Moya', 'JP', '$225,750')]),
    streams=dict(src=('TwitchMetrics', 'https://www.twitchmetrics.net/channels/popularity?game=Brawl+Stars'), date='2026-09-25',
                 rows=[('nearz_z', 'es', 1833), ('Trebor', 'es', 1138), ('cu6ickk', 'ru', 886), ('alekzz03', 'ru', 856), ('SpiukBS', 'es', 848),
                       ('TV_BroCast', 'de', 730), ('BrawlBallLeague', 'en', 713), ('Kuzan_TV', 'fr', 692), ('prostislavv', 'ru', 645), ('neguesti', 'ru', 456),
                       ('BrawlStars', 'en', 447), ('Ferre', 'it', 412), ('Igor10d', 'ru', 390), ('PiouPiouLover', 'fr', 342), ('Gassbss', 'fr', 260)]),
  ),
}

X = {
 'en': dict(esp='Esports prize money by country', esp_i='Total prize money won by players from each country in {game} tournaments.', esp_c=('Country', 'Prize money', 'Players'),
   yours='Your country', not_top='{c} is not in the top 15 by prize money yet.', top='Top earners worldwide', top_c=('Player', 'Country', 'Prize money'),
   st='Most-watched live streamers right now', st_i='Twitch channels ranked by average viewers over the last 30 days. Streams in your language come first.',
   st_c=('Channel', 'Language', 'Avg viewers'), st_none='No stream in your language in the top 15 right now.',
   src='Source: {s}', rec='tournaments recorded {span}', upd='updated {d}'),
 'ru': dict(esp='Призовые в киберспорте по странам', esp_i='Сколько призовых выиграли игроки из каждой страны на турнирах по {game}.', esp_c=('Страна', 'Призовые', 'Игроков'),
   yours='Твоя страна', not_top='{c} пока не входит в топ-15 по призовым.', top='Лучшие игроки мира по заработку', top_c=('Игрок', 'Страна', 'Призовые'),
   st='Самые популярные стримеры сейчас', st_i='Каналы Twitch по среднему числу зрителей за последние 30 дней. Трансляции на твоём языке — первыми.',
   st_c=('Канал', 'Язык', 'Ср. зрителей'), st_none='Сейчас в топ-15 нет трансляций на твоём языке.',
   src='Источник: {s}', rec='учтены турниры {span}', upd='обновлено {d}'),
 'es': dict(esp='Premios de esports por país', esp_i='Premios totales ganados por jugadores de cada país en torneos de {game}.', esp_c=('País', 'Premios', 'Jugadores'),
   yours='Tu país', not_top='{c} aún no está en el top 15 por premios.', top='Los que más han ganado en el mundo', top_c=('Jugador', 'País', 'Premios'),
   st='Streamers más vistos ahora', st_i='Canales de Twitch según la media de espectadores de los últimos 30 días. Primero, los directos en tu idioma.',
   st_c=('Canal', 'Idioma', 'Espectadores medios'), st_none='Ahora mismo no hay directos en tu idioma en el top 15.',
   src='Fuente: {s}', rec='torneos registrados {span}', upd='actualizado {d}'),
 'pt': dict(esp='Premiações de esports por país', esp_i='Total de prêmios ganhos por jogadores de cada país em torneios de {game}.', esp_c=('País', 'Prêmios', 'Jogadores'),
   yours='Seu país', not_top='{c} ainda não está no top 15 em prêmios.', top='Maiores ganhadores do mundo', top_c=('Jogador', 'País', 'Prêmios'),
   st='Streamers mais assistidos agora', st_i='Canais da Twitch pela média de espectadores dos últimos 30 dias. Lives no seu idioma aparecem primeiro.',
   st_c=('Canal', 'Idioma', 'Média de espectadores'), st_none='No momento não há lives no seu idioma no top 15.',
   src='Fonte: {s}', rec='torneios registrados {span}', upd='atualizado {d}'),
 'id': dict(esp='Hadiah esports per negara', esp_i='Total hadiah yang dimenangkan pemain dari tiap negara di turnamen {game}.', esp_c=('Negara', 'Hadiah', 'Pemain'),
   yours='Negara kamu', not_top='{c} belum masuk 15 besar berdasarkan hadiah.', top='Pemain dengan penghasilan tertinggi di dunia', top_c=('Pemain', 'Negara', 'Hadiah'),
   st='Streamer paling banyak ditonton saat ini', st_i='Channel Twitch berdasarkan rata-rata penonton 30 hari terakhir. Siaran dalam bahasa kamu ditampilkan lebih dulu.',
   st_c=('Channel', 'Bahasa', 'Rata-rata penonton'), st_none='Saat ini belum ada siaran dalam bahasa kamu di 15 besar.',
   src='Sumber: {s}', rec='turnamen tercatat {span}', upd='diperbarui {d}'),
 'tr': dict(esp='Ülkelere göre espor ödülleri', esp_i='{game} turnuvalarında her ülkeden oyuncuların kazandığı toplam ödül.', esp_c=('Ülke', 'Ödül', 'Oyuncu'),
   yours='Senin ülken', not_top='{c} henüz ödülde ilk 15\'te değil.', top='Dünyada en çok kazananlar', top_c=('Oyuncu', 'Ülke', 'Ödül'),
   st='Şu an en çok izlenen yayıncılar', st_i='Son 30 gündeki ortalama izleyiciye göre Twitch kanalları. Senin dilindeki yayınlar önce.',
   st_c=('Kanal', 'Dil', 'Ort. izleyici'), st_none='Şu anda ilk 15\'te senin dilinde yayın yok.',
   src='Kaynak: {s}', rec='kayıtlı turnuvalar {span}', upd='güncelleme {d}'),
 'ar': dict(esp='جوائز الرياضات الإلكترونية حسب الدولة', esp_i='إجمالي الجوائز التي فاز بها لاعبو كل دولة في بطولات {game}.', esp_c=('الدولة', 'الجوائز', 'اللاعبون'),
   yours='دولتك', not_top='{c} ليست ضمن أفضل 15 دولة في الجوائز بعد.', top='الأعلى دخلاً في العالم', top_c=('اللاعب', 'الدولة', 'الجوائز'),
   st='أكثر صانعي البث مشاهدة الآن', st_i='قنوات Twitch حسب متوسط المشاهدين في آخر 30 يوماً. البث بلغتك يظهر أولاً.',
   st_c=('القناة', 'اللغة', 'متوسط المشاهدين'), st_none='لا يوجد حالياً بث بلغتك ضمن أفضل 15.',
   src='المصدر: {s}', rec='البطولات المسجلة {span}', upd='آخر تحديث {d}'),
 'vi': dict(esp='Tiền thưởng esports theo quốc gia', esp_i='Tổng tiền thưởng người chơi từng quốc gia giành được ở các giải {game}.', esp_c=('Quốc gia', 'Tiền thưởng', 'Người chơi'),
   yours='Quốc gia của bạn', not_top='{c} chưa lọt top 15 về tiền thưởng.', top='Người chơi kiếm nhiều nhất thế giới', top_c=('Người chơi', 'Quốc gia', 'Tiền thưởng'),
   st='Streamer được xem nhiều nhất hiện nay', st_i='Kênh Twitch xếp theo số người xem trung bình 30 ngày qua. Kênh cùng ngôn ngữ với bạn hiện trước.',
   st_c=('Kênh', 'Ngôn ngữ', 'Người xem TB'), st_none='Hiện chưa có kênh nào bằng ngôn ngữ của bạn trong top 15.',
   src='Nguồn: {s}', rec='giải được ghi nhận {span}', upd='cập nhật {d}'),
 'hi': dict(esp='देश के अनुसार ईस्पोर्ट्स इनामी राशि', esp_i='{game} टूर्नामेंट में हर देश के खिलाड़ियों द्वारा जीती गई कुल इनामी राशि।', esp_c=('देश', 'इनामी राशि', 'खिलाड़ी'),
   yours='आपका देश', not_top='{c} अभी इनामी राशि में टॉप 15 में नहीं है।', top='दुनिया के सबसे ज़्यादा कमाने वाले', top_c=('खिलाड़ी', 'देश', 'इनामी राशि'),
   st='अभी सबसे ज़्यादा देखे जाने वाले स्ट्रीमर', st_i='पिछले 30 दिनों के औसत दर्शकों के अनुसार Twitch चैनल। आपकी भाषा की स्ट्रीम पहले।',
   st_c=('चैनल', 'भाषा', 'औसत दर्शक'), st_none='अभी टॉप 15 में आपकी भाषा की कोई स्ट्रीम नहीं है।',
   src='स्रोत: {s}', rec='दर्ज टूर्नामेंट {span}', upd='अपडेट {d}'),
 'fr': dict(esp='Gains en esport par pays', esp_i='Total des gains remportés par les joueurs de chaque pays dans les tournois {game}.', esp_c=('Pays', 'Gains', 'Joueurs'),
   yours='Votre pays', not_top='{c} n\'est pas encore dans le top 15 des gains.', top='Les plus gros gains au monde', top_c=('Joueur', 'Pays', 'Gains'),
   st='Streamers les plus regardés en ce moment', st_i='Chaînes Twitch classées par spectateurs moyens sur les 30 derniers jours. Les streams dans votre langue d\'abord.',
   st_c=('Chaîne', 'Langue', 'Spectateurs moyens'), st_none='Aucun stream dans votre langue dans le top 15 pour le moment.',
   src='Source : {s}', rec='tournois enregistrés {span}', upd='mis à jour le {d}'),
 'de': dict(esp='E-Sport-Preisgeld nach Land', esp_i='Gesamtes Preisgeld, das Spieler aus jedem Land bei {game}-Turnieren gewonnen haben.', esp_c=('Land', 'Preisgeld', 'Spieler'),
   yours='Dein Land', not_top='{c} ist beim Preisgeld noch nicht in den Top 15.', top='Die Top-Verdiener weltweit', top_c=('Spieler', 'Land', 'Preisgeld'),
   st='Die meistgesehenen Streamer gerade', st_i='Twitch-Kanäle nach durchschnittlichen Zuschauern der letzten 30 Tage. Streams in deiner Sprache zuerst.',
   st_c=('Kanal', 'Sprache', 'Ø Zuschauer'), st_none='Derzeit kein Stream in deiner Sprache in den Top 15.',
   src='Quelle: {s}', rec='erfasste Turniere {span}', upd='aktualisiert {d}'),
 'it': dict(esp='Montepremi esport per paese', esp_i='Montepremi totale vinto dai giocatori di ogni paese nei tornei di {game}.', esp_c=('Paese', 'Montepremi', 'Giocatori'),
   yours='Il tuo paese', not_top='{c} non è ancora nella top 15 per montepremi.', top='I giocatori che hanno guadagnato di più al mondo', top_c=('Giocatore', 'Paese', 'Montepremi'),
   st='Gli streamer più seguiti ora', st_i='Canali Twitch per spettatori medi negli ultimi 30 giorni. Prima le dirette nella tua lingua.',
   st_c=('Canale', 'Lingua', 'Spettatori medi'), st_none='Al momento nessuna diretta nella tua lingua nella top 15.',
   src='Fonte: {s}', rec='tornei registrati {span}', upd='aggiornato il {d}'),
 'ja': dict(esp='国別のeスポーツ賞金', esp_i='{game}の大会で各国のプレイヤーが獲得した賞金総額。', esp_c=('国', '賞金', '選手数'),
   yours='あなたの国', not_top='{c}は賞金額でまだトップ15に入っていません。', top='世界の獲得賞金トップ', top_c=('選手', '国', '賞金'),
   st='今いちばん見られている配信者', st_i='過去30日間の平均視聴者数によるTwitchチャンネル。あなたの言語の配信を先に表示。',
   st_c=('チャンネル', '言語', '平均視聴者'), st_none='現在、トップ15にあなたの言語の配信はありません。',
   src='出典：{s}', rec='記録された大会 {span}', upd='更新 {d}'),
 'ko': dict(esp='국가별 e스포츠 상금', esp_i='{game} 대회에서 각 나라 선수들이 받은 상금 총액.', esp_c=('국가', '상금', '선수'),
   yours='내 나라', not_top='{c}은(는) 아직 상금 기준 상위 15개국에 들지 않습니다.', top='세계 상금 랭킹 상위 선수', top_c=('선수', '국가', '상금'),
   st='지금 가장 많이 보는 스트리머', st_i='최근 30일 평균 시청자 수 기준 Twitch 채널. 내 언어 방송을 먼저 보여 줍니다.',
   st_c=('채널', '언어', '평균 시청자'), st_none='현재 상위 15위 안에 내 언어 방송이 없습니다.',
   src='출처: {s}', rec='기록된 대회 {span}', upd='업데이트 {d}'),
 'th': dict(esp='เงินรางวัลอีสปอร์ตแยกตามประเทศ', esp_i='เงินรางวัลรวมที่ผู้เล่นแต่ละประเทศได้รับจากการแข่งขัน {game}', esp_c=('ประเทศ', 'เงินรางวัล', 'ผู้เล่น'),
   yours='ประเทศของคุณ', not_top='{c} ยังไม่ติด 15 อันดับแรกด้านเงินรางวัล', top='ผู้เล่นที่ได้เงินรางวัลสูงสุดในโลก', top_c=('ผู้เล่น', 'ประเทศ', 'เงินรางวัล'),
   st='สตรีมเมอร์ที่มีคนดูมากที่สุดตอนนี้', st_i='ช่อง Twitch จัดตามจำนวนผู้ชมเฉลี่ย 30 วันล่าสุด สตรีมภาษาของคุณแสดงก่อน',
   st_c=('ช่อง', 'ภาษา', 'ผู้ชมเฉลี่ย'), st_none='ตอนนี้ยังไม่มีสตรีมภาษาของคุณใน 15 อันดับแรก',
   src='แหล่งที่มา: {s}', rec='การแข่งขันที่บันทึก {span}', upd='อัปเดต {d}'),
 'pl': dict(esp='Nagrody w e-sporcie według krajów', esp_i='Łączne nagrody zdobyte przez graczy z każdego kraju w turniejach {game}.', esp_c=('Kraj', 'Nagrody', 'Gracze'),
   yours='Twój kraj', not_top='{c} nie jest jeszcze w top 15 pod względem nagród.', top='Najlepiej zarabiający na świecie', top_c=('Gracz', 'Kraj', 'Nagrody'),
   st='Najczęściej oglądani streamerzy teraz', st_i='Kanały Twitch według średniej liczby widzów z ostatnich 30 dni. Transmisje w Twoim języku najpierw.',
   st_c=('Kanał', 'Język', 'Śr. widzów'), st_none='Obecnie w top 15 nie ma transmisji w Twoim języku.',
   src='Źródło: {s}', rec='zarejestrowane turnieje {span}', upd='aktualizacja {d}'),
 'zh': dict(esp='各国电竞奖金', esp_i='各国选手在{game}赛事中获得的奖金总额。', esp_c=('国家/地区', '奖金', '选手数'),
   yours='您的国家', not_top='{c}目前尚未进入奖金前15名。', top='全球奖金最高的选手', top_c=('选手', '国家/地区', '奖金'),
   st='当前最受关注的主播', st_i='按过去30天平均观众数排名的Twitch频道。您的语言的直播排在前面。',
   st_c=('频道', '语言', '平均观众'), st_none='目前前15名中没有您语言的直播。',
   src='来源：{s}', rec='收录赛事 {span}', upd='更新于 {d}'),
}

EXTRA.update(_MORE)

def cname(lang, c):
    return NAMES['countries'][lang][c]

def render_extra(game, lang, game_name):
    e = EXTRA.get(game)
    if not e:
        return ''
    x = X[lang]; mine = LANG_COUNTRY[lang]
    link = lambda s: '<a href="' + s[1] + '" target="_blank" rel="noopener">' + s[0] + '</a>'
    out = []
    # esports by country
    es = e.get('esports')
    rows = ''
    for i, (c, money, n) in enumerate(es['rows'] if es else [], 1):
        me = c == mine
        rows += ('<tr' + (' class="wm-mine"' if me else '') + '><th scope="row"><span class="wm-rank">' + str(i) + '</span><span class="wm-flag" aria-hidden="true">' + FLAGS[c] + '</span>' +
                 cname(lang, c) + (' <span class="wm-you">' + x['yours'] + '</span>' if me else '') +
                 '</th><td data-l="' + x['esp_c'][1] + '" class="wm-num">' + money + '</td><td data-l="' + x['esp_c'][2] + '" class="wm-num">' + str(n) + '</td></tr>')
    note = ''
    if es and mine and mine not in [r[0] for r in es['rows']]:
        note = '<p class="wm-miss">' + x['not_top'].format(c=cname(lang, mine)) + '</p>'
    if es: out.append('<h3>🏆 ' + x['esp'] + '</h3><p class="wm-intro">' + x['esp_i'].format(game=game_name) + ' ' + es['total'] + '.</p>' + note +
               '<div class="wm-wrap"><table class="wm-table wm-small"><thead><tr><th scope="col">' + '</th><th scope="col">'.join(x['esp_c']) +
               '</th></tr></thead><tbody>' + rows + '</tbody></table></div>' +
               '<p class="wm-note">' + x['src'].format(s=link(es['src'])) + ', ' + x['rec'].format(span=es['span']) + '.</p>')
    # top players
    pl = e.get('players')
    rows = '' if not pl else ''.join('<tr><th scope="row">' + p + '</th><td data-l="' + x['top_c'][1] + '"><span class="wm-flag" aria-hidden="true">' + FLAGS[c] + '</span>' + cname(lang, c) +
                   '</td><td data-l="' + x['top_c'][2] + '" class="wm-num">' + m + '</td></tr>' for p, c, m in pl['rows'])
    if pl: out.append('<h3>🥇 ' + x['top'] + '</h3><div class="wm-wrap"><table class="wm-table wm-small"><thead><tr><th scope="col">' + '</th><th scope="col">'.join(x['top_c']) +
               '</th></tr></thead><tbody>' + rows + '</tbody></table></div><p class="wm-note">' + x['src'].format(s=link(pl['src'])) + '.</p>')
    # streamers: reader's language first
    st = e['streams']
    rs = sorted(st['rows'], key=lambda r: (r[1] != lang, -r[2]))
    has = any(r[1] == lang for r in rs)
    rows = ''.join('<tr' + (' class="wm-mine"' if l == lang else '') + '><th scope="row"><a href="https://www.twitch.tv/' + ch.lower() + '" target="_blank" rel="noopener">' + ch +
                   '</a></th><td data-l="' + x['st_c'][1] + '">' + NAMES['languages'][lang][l] + '</td><td data-l="' + x['st_c'][2] + '" class="wm-num">' + f'{v:,}' + '</td></tr>'
                   for ch, l, v in rs)
    out.append('<h3>📺 ' + x['st'] + '</h3><p class="wm-intro">' + x['st_i'] + '</p>' + ('' if has else '<p class="wm-miss">' + x['st_none'] + '</p>') +
               '<div class="wm-wrap"><table class="wm-table wm-small"><thead><tr><th scope="col">' + '</th><th scope="col">'.join(x['st_c']) +
               '</th></tr></thead><tbody>' + rows + '</tbody></table></div><p class="wm-note">' + x['src'].format(s=link(st['src'])) + ', ' + x['upd'].format(d=st['date']) + '. ' + TW_ONLY[lang] + '</p>')
    return '\n'.join(out)

# Malay (2026-09-30)
LANG_COUNTRY['ms'] = 'MY'
X['ms'] = {'esp': 'Wang hadiah e-sukan mengikut negara',
 'esp_c': ('Negara', 'Wang hadiah', 'Pemain'),
 'esp_i': 'Jumlah wang hadiah yang dimenangi pemain dari setiap negara dalam kejohanan {game}.',
 'not_top': '{c} belum berada dalam 15 teratas mengikut wang hadiah.',
 'rec': 'kejohanan yang direkodkan {span}',
 'src': 'Sumber: {s}',
 'st': 'Penstrim langsung paling ramai ditonton sekarang',
 'st_c': ('Saluran', 'Bahasa', 'Purata penonton'),
 'st_i': 'Saluran Twitch disusun mengikut purata penonton dalam 30 hari lepas. Strim dalam bahasa anda dipaparkan dahulu.',
 'st_none': 'Tiada strim dalam bahasa anda dalam 15 teratas buat masa ini.',
 'top': 'Pemenang wang tertinggi di dunia',
 'top_c': ('Pemain', 'Negara', 'Wang hadiah'),
 'upd': 'dikemas kini {d}',
 'yours': 'Negara anda'}

# Uzbek (2026-09-30)
LANG_COUNTRY['uz'] = 'UZ'
X['uz'] = {'esp': 'Mamlakatlar boʻyicha kibersport mukofot pullari',
 'esp_c': ('Mamlakat', 'Mukofot puli', 'Oʻyinchilar'),
 'esp_i': '{game} turnirlarida har bir mamlakat oʻyinchilari yutgan jami mukofot pullari.',
 'not_top': '{c} hali mukofot pullari boʻyicha top-15 ga kirmagan.',
 'rec': '{span} davrida qayd etilgan turnirlar',
 'src': 'Manba: {s}',
 'st': 'Hozir eng koʻp tomosha qilinayotgan striminglar',
 'st_c': ('Kanal', 'Til', 'Oʻrt. tomoshabin'),
 'st_i': 'Oxirgi 30 kundagi oʻrtacha tomoshabinlar boʻyicha saralangan Twitch kanallari. Sizning tilingizdagi striminglar birinchi koʻrsatiladi.',
 'st_none': 'Hozir top-15 da sizning tilingizdagi strim yoʻq.',
 'top': 'Dunyodagi eng koʻp yutganlar',
 'top_c': ('Oʻyinchi', 'Mamlakat', 'Mukofot puli'),
 'upd': '{d} da yangilangan',
 'yours': 'Sizning mamlakatingiz'}

# kk
LANG_COUNTRY['kk'] = 'KZ'
X['kk'] = {'esp': 'Елдер бойынша киберспорт жүлде ақшасы',
 'esp_c': ('Ел', 'Жүлде ақшасы', 'Ойыншылар'),
 'esp_i': '{game} турнирлерінде әр елдің ойыншылары ұтқан жалпы жүлде ақшасы.',
 'not_top': '{c} әзірге жүлде ақшасы бойынша топ-15-ке кірмеген.',
 'rec': '{span} аралығында тіркелген турнирлер',
 'src': 'Дереккөз: {s}',
 'st': 'Қазір ең көп көрілетін стримерлер',
 'st_c': ('Арна', 'Тіл', 'Орт. көрермен'),
 'st_i': 'Соңғы 30 күндегі орташа көрермендер бойынша сұрыпталған Twitch арналары. Сіздің тіліңіздегі стримдер бірінші көрсетіледі.',
 'st_none': 'Қазір топ-15-те сіздің тіліңіздегі стрим жоқ.',
 'top': 'Әлемдегі ең көп ұтқандар',
 'top_c': ('Ойыншы', 'Ел', 'Жүлде ақшасы'),
 'upd': '{d} жаңартылды',
 'yours': 'Сіздің еліңіз'}
