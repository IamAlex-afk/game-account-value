"""Recent champions of each game's finished majors, all 17 languages.
Winner origin only where the official source states it."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
DATES = json.load(open(os.path.join(HERE, 'event_dates.json'), encoding='utf-8'))

RESULTS = {
 'brawl-stars': [dict(id='r-bswf25', title='Brawl Stars World Finals 2025', where=('Stockholm', 'SE'), winner='Crazy Raccoon', origin='JP', prize='$400,000', pool='$1,000,000',
                      src=('https://supercell.com/en/news/brawl-wf-2025/', 'Supercell'))],
 'mobile-legends': [dict(id='r-msc26', title='MLBB Mid Season Cup 2026 (EWC)', where=('Paris', 'FR'), winner='Team Spirit', origin='cis', prize='$1,000,000', pool='$3,000,000+',
                         src=('https://esportsworldcup.com/en/press-releases/team-spirit-emerges-victorious-mlbb-msc-at-ewc26-finals', 'Esports World Cup')),
                    dict(id='r-m7', title='M7 World Championship', where=('Jakarta', 'ID'), winner='Aurora Gaming PH', origin='PH', prize=None, pool='$1,000,000',
                         src=('https://en.wikipedia.org/wiki/MLBB_M7_World_Championship', 'Wikipedia'))],
 'free-fire': [dict(id='r-ffewc26', title='Free Fire · Esports World Cup 2026', where=('Paris', 'FR'), winner='LYON', origin='latam', prize='$300,000', pool=None,
                    src=('https://esportsworldcup.com/en/press-releases/lyon-crowned-free-fire-champions-at-ewc26', 'Esports World Cup'))],
 'fortnite': [dict(id='r-fncs26', title='FNCS Global Championship 2026', where=('Antwerp', 'BE'), winner='Swizzy & Pixie', origin=None, prize=None, pool='$2,000,000',
                   src=('https://www.fortnite.com/competitive/fncs-2026-global-championship', 'Epic Games'))],
 'clash-royale': [dict(id='r-crl25', title='Clash Royale League 2025 World Finals', where=('Atlanta', 'US'), winner='Mohamed Light', origin='EG', prize='$200,000', pool='$500,000',
                       src=('https://liquipedia.net/clashroyale/Clash_Royale_League/2025/World_Finals', 'Liquipedia'))],
 'clash-of-clans': [dict(id='r-cocwc25', title='Clash of Clans World Championship 2025', where=('Atlanta', 'US'), winner='Tribe Gaming', origin=None, prize='$300,000', pool='$700,000',
                         src=('https://liquipedia.net/clashofclans/Clash_of_Clans_World_Championship/2025', 'Liquipedia'))],
}

RL = {
 'en': dict(h='Recent champions', c=('Tournament', 'Winner', 'From', "Winner's prize", 'Prize pool'), latam='Latin America', cis='Eastern Europe & Central Asia'),
 'ru': dict(h='Недавние чемпионы', c=('Турнир', 'Победитель', 'Откуда', 'Приз победителя', 'Призовой фонд'), latam='Латинская Америка', cis='Восточная Европа и Центральная Азия'),
 'es': dict(h='Campeones recientes', c=('Torneo', 'Ganador', 'De', 'Premio del ganador', 'Bolsa de premios'), latam='Latinoamérica', cis='Europa del Este y Asia Central'),
 'pt': dict(h='Campeões recentes', c=('Torneio', 'Vencedor', 'De onde', 'Prêmio do vencedor', 'Premiação total'), latam='América Latina', cis='Leste Europeu e Ásia Central'),
 'id': dict(h='Juara terbaru', c=('Turnamen', 'Pemenang', 'Asal', 'Hadiah pemenang', 'Total hadiah'), latam='Amerika Latin', cis='Eropa Timur & Asia Tengah'),
 'tr': dict(h='Son şampiyonlar', c=('Turnuva', 'Kazanan', 'Nereden', 'Kazanan ödülü', 'Ödül havuzu'), latam='Latin Amerika', cis='Doğu Avrupa ve Orta Asya'),
 'ar': dict(h='أبطال حديثون', c=('البطولة', 'الفائز', 'من', 'جائزة الفائز', 'مجموع الجوائز'), latam='أمريكا اللاتينية', cis='أوروبا الشرقية وآسيا الوسطى'),
 'vi': dict(h='Nhà vô địch gần đây', c=('Giải đấu', 'Vô địch', 'Đến từ', 'Thưởng vô địch', 'Tổng giải thưởng'), latam='Mỹ Latinh', cis='Đông Âu & Trung Á'),
 'hi': dict(h='हाल के चैंपियन', c=('टूर्नामेंट', 'विजेता', 'कहाँ से', 'विजेता की इनामी राशि', 'कुल इनामी राशि'), latam='लैटिन अमेरिका', cis='पूर्वी यूरोप और मध्य एशिया'),
 'fr': dict(h='Champions récents', c=('Tournoi', 'Vainqueur', 'Origine', 'Gain du vainqueur', 'Cagnotte'), latam='Amérique latine', cis="Europe de l'Est et Asie centrale"),
 'de': dict(h='Aktuelle Champions', c=('Turnier', 'Sieger', 'Herkunft', 'Siegprämie', 'Preisgeld gesamt'), latam='Lateinamerika', cis='Osteuropa & Zentralasien'),
 'it': dict(h='Campioni recenti', c=('Torneo', 'Vincitore', 'Provenienza', 'Premio al vincitore', 'Montepremi'), latam='America Latina', cis='Europa orientale e Asia centrale'),
 'ja': dict(h='最近の優勝者', c=('大会', '優勝', '出身', '優勝賞金', '賞金総額'), latam='ラテンアメリカ', cis='東欧・中央アジア'),
 'ko': dict(h='최근 우승자', c=('대회', '우승', '출신', '우승 상금', '총상금'), latam='라틴아메리카', cis='동유럽·중앙아시아'),
 'th': dict(h='แชมป์ล่าสุด', c=('รายการ', 'ผู้ชนะ', 'จาก', 'เงินรางวัลผู้ชนะ', 'เงินรางวัลรวม'), latam='ละตินอเมริกา', cis='ยุโรปตะวันออกและเอเชียกลาง'),
 'pl': dict(h='Ostatni mistrzowie', c=('Turniej', 'Zwycięzca', 'Skąd', 'Nagroda zwycięzcy', 'Pula nagród'), latam='Ameryka Łacińska', cis='Europa Wschodnia i Azja Środkowa'),
 'zh': dict(h='近期冠军', c=('赛事', '冠军', '来自', '冠军奖金', '总奖金'), latam='拉丁美洲', cis='东欧及中亚'),
}

def flag(cc):
    return chr(0x1F1E6 + ord(cc[0]) - 65) + chr(0x1F1E6 + ord(cc[1]) - 65)

def render_results(game, lang, names):
    rs = RESULTS.get(game)
    if not rs:
        return ''
    r = RL[lang]; c = r['c']
    rows = ''
    for e in rs:
        o = e['origin']
        if not o:
            origin = '—'
        elif o in ('latam', 'cis'):
            origin = r[o]
        else:
            origin = '<span class="wm-flag" aria-hidden="true">' + flag(o) + '</span>' + names['countries'][lang][o]
        date = DATES.get(e['id'], {}).get(lang, '')
        place = e['where'][0] + ', ' + names['countries'][lang][e['where'][1]]
        rows += ('<tr><th scope="row">' + e['title'] + '<span class="ev-where">' + date + ' · ' + place +
                 ' · <a href="' + e['src'][0] + '" target="_blank" rel="noopener">' + e['src'][1] + '</a></span></th>'
                 '<td data-l="' + c[1] + '"><strong>🏆 ' + e['winner'] + '</strong></td><td data-l="' + c[2] + '">' + origin + '</td>'
                 '<td data-l="' + c[3] + '" class="wm-num">' + (e['prize'] or '—') + '</td><td data-l="' + c[4] + '" class="wm-num">' + (e['pool'] or '—') + '</td></tr>')
    return ('<h3>🏆 ' + r['h'] + '</h3><div class="wm-wrap"><table class="wm-table wm-small wm-results"><thead><tr><th scope="col">' +
            '</th><th scope="col">'.join(c) + '</th></tr></thead><tbody>' + rows + '</tbody></table></div>')

# Malay (2026-09-30)
RL['ms'] = {'c': ('Kejohanan', 'Pemenang', 'Dari', 'Hadiah pemenang', 'Kumpulan hadiah'),
 'cis': 'Eropah Timur & Asia Tengah',
 'h': 'Juara terkini',
 'latam': 'Amerika Latin'}

# Uzbek (2026-09-30)
RL['uz'] = {'c': ('Turnir', 'Gʻolib', 'Qayerdan', 'Gʻolib mukofoti', 'Mukofot jamgʻarmasi'),
 'cis': 'Sharqiy Yevropa va Markaziy Osiyo',
 'h': 'Soʻnggi chempionlar',
 'latam': 'Lotin Amerikasi'}

# kk
RL['kk'] = {'c': ('Турнир', 'Жеңімпаз', 'Қайдан', 'Жеңімпаз жүлдесі', 'Жүлде қоры'),
 'cis': 'Шығыс Еуропа және Орталық Азия',
 'h': 'Соңғы чемпиондар',
 'latam': 'Латын Америкасы'}

# ky
RL['ky'] = {'c': ('Турнир', 'Жеңүүчү', 'Кайдан', 'Жеңүүчүнүн сыйлыгы', 'Сыйлык фонду'),
 'cis': 'Чыгыш Европа жана Борбордук Азия',
 'h': 'Акыркы чемпиондор',
 'latam': 'Латын Америкасы'}

# tk
RL['tk'] = {'c': ('Ýaryş', 'Ýeňiji', 'Nireden', 'Ýeňijiniň baýragy', 'Baýrak gazna'),
 'cis': 'Gündogar Ýewropa we Merkezi Aziýa',
 'h': 'Soňky çempionlar',
 'latam': 'Latyn Amerikasy'}
