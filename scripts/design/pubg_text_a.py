"""PUBG Mobile page text (2026-10-14) — English and Russian.
Every figure is an asking price seen by hand on 2026-10-14 (sources at the end of the page):
Eldorado.gg (10,905 listings), FunPay (6,332; € at 0.894 EUR/$), GameSatış (49.4 TRY/$).
Russian is written for Russian readers, not word-for-word from English."""

EL = 'https://www.eldorado.gg/pubg-mobile-accounts-for-sale/a/21-1-0'
FP = 'https://funpay.com/en/lots/346/'
GS = 'https://www.gamesatis.com/pubg-mobile-hesap-satisi'
EULA = 'https://www.pubgmobile.com/PK/terms.shtml'
PR = ('https://www.mynewsdesk.com/uk/swipe-right/pressreleases/'
      'pubg-mobile-esports-unveils-2026-esports-roadmap-with-expanded-global-opportunities-at-2025-pmgc-3421490')
EWC = 'https://esportsworldcup.com/en/press-releases/s2g-esports-win-nine-day-gauntlet'
GOP = 'https://gamingonphone.com/guides/how-to-get-rewards-collections-rank-in-pubg-mobile-or-bgmi/'

# collection level → asking price seen (one or two listings each), shared by every language
ROWS = [('41', '≈ $37', 'FunPay'), ('53', '≈ $176', 'FunPay'), ('67', '$249', 'Eldorado.gg'),
        ('71 – 74', '$272 – $909', 'GameSatış, Eldorado.gg'), ('81.5', '≈ $1,174', 'GameSatış'),
        ('85 – 87.8', '≈ $2,348 – $3,138', 'GameSatış'), ('92.6', '≈ $4,960', 'GameSatış')]

TEXT = {
 'en': dict(
  title='PUBG Mobile Account Value Calculator (2026): $0.29–$4,960 | GameAccountValue',
  desc='Free calculator by collection level, no sign-up, no data collected: asking prices on Eldorado.gg, FunPay and GameSatış ($0.29–$4,960), the 5 screenshots the bot needs, scam risks.',
  og_title='How Much Is My PUBG Mobile Account Worth? — GameAccountValue',
  og_alt='GameAccountValue — PUBG Mobile account value',
  h1='🪂 PUBG Mobile Account Value',
  intro='Asking prices from three marketplaces, the one number those prices follow — the collection level — and the screenshots that show it.',
  updated='Checked October 2026 against marketplace listings. Sources are listed at the bottom of the page.',
  badge='🗓️ Listings checked by hand: October 14, 2026',
  range='Asking prices seen: $0.29 – $4,960 · Eldorado.gg, first page: $2 – $400',
  facts=['🗂️ <strong>95</strong> collection levels in the game',
         '🥇 PUBG Mobile World Cup 2026: <strong>S2G Esports</strong> (Türkiye)',
         '🏆 Global Championship 2026, prize pool $3,000,000: <strong>Türkiye</strong>'],
  calc_sub='One slider: the collection level, the number listings price by. Nothing is entered or sent anywhere; the bot reads it from your screenshots.',
  calc_why='The calculator only sees the collection level. It can’t see X-Suit levels, maxed guns or supercars — the bot counts those from your screenshots.',
  nav_shots='📸 Screenshots',
  h2_shots='Screenshots for an estimate',
  q_worth='How much is a PUBG Mobile account worth?',
  a_worth=('On October 14, 2026 Eldorado.gg listed <strong>10,905</strong> PUBG Mobile accounts; the first page asked $2 for a plain Gold-rank account and up to $399.99 '
           'for an account at collection level 74. FunPay listed <strong>6,332</strong>, from €0.26 to €3,286 (≈ $0.29 – $3,676). '
           'On Türkiye’s GameSatış the asking prices ran from 1,000 ₺ to 245,000 ₺ (≈ $20 – $4,960). Most of that spread follows one number: the collection level.'),
  q_table='What do accounts ask at each collection level?',
  table_head=('Collection level', 'Asking price seen', 'Where'),
  table_note='Asking prices on October 14, 2026, converted at 49.4 TRY and 0.894 EUR per US dollar. Usually one listing per row — a direction, not a price list. '
             'The $909 listing at level 74 also names 14 maxed guns.',
  q_value='What actually determines a PUBG Mobile account’s value?',
  value=['<strong>Collection level</strong> — the game has 95 levels; every newly owned item adds points by its type and quality, so the level sums up the whole inventory.',
         '<strong>X-Suits and their upgrade level</strong> — accounts with a max-level X-Suit asked €2,063 – €2,629 on FunPay.',
         '<strong>Upgradable gun skins</strong> and the level each one reached (Glacier M416 is the one listings name most).',
         '<strong>Supercar skins</strong> from car collaborations — listings count them one by one.',
         '<strong>Rank adds little</strong>: it resets every season; on Eldorado.gg a “Gold Rank” account asked $1.99 and a “Diamond” one $3.75.'],
  q_lookup='What should I look up before using the calculator?',
  lookup=['The calculator asks for one number: the <strong>collection level</strong> from the Collection screen (for example 74.5).',
          'The result is a rough range of public asking prices, not an offer. Buying or selling accounts breaks the game’s terms — see <a href="#rules">the rules</a>.'],
  q_shots='Which 5 screenshots does the bot need for PUBG Mobile?',
  shots_intro='PUBG Mobile spreads value over several inventory tabs, so the bot asks for five screenshots instead of three:',
  shots=['<strong>Profile</strong> — player ID, account level and rank readable.',
         '<strong>Collection</strong> — the Collection screen with the collection level (for example 74.5). This one matters most.',
         '<strong>Inventory → Outfits</strong> — X-Suits and Mythic outfits visible.',
         '<strong>Upgradable gun skins</strong> — with each level (Lv.) visible.',
         '<strong>Vehicle skins</strong> — supercars and other rare cars; the UC balance if it is shown.'],
  shots_note='Without the Collection screen the bot counts only what it can see — X-Suits, upgradable guns, supercars — and the estimate comes out lower. '
             'The bot never asks for a login or password, and screenshots are not stored.',
  q_scams='What are the biggest scams in PUBG Mobile account trading?',
  a_scams=('A PUBG Mobile account can be linked to several logins at once — for example Facebook, Twitter or Google Play. Any login the seller keeps is a way back in: '
           'the account is “recovered” after payment, and the buyer is left with nothing. Some FunPay listings are rentals by design (marked “Rent”), not sales. '
           'The publisher’s terms forbid transferring accounts at all, so neither side can turn to support when a deal goes wrong.'),
  q_rules='Is trading PUBG Mobile accounts against the rules?',
  a_rules=('Yes. The PUBG Mobile terms (Proxima Beta Pte. Limited) say: “Your Account is personal to you and you are prohibited from gifting, lending, transferring or otherwise '
           'permitting any other person to access or use Your Account.” Virtual goods and currency may not be traded or sold either, and the publisher may suspend access or end the agreement.'),
  q_where='Where do these listings come from?',
  a_where=('Eldorado.gg and FunPay are international marketplaces, GameSatış is Turkish. Every figure on this page is an asking price seen by hand on October 14, 2026 — '
           'not a completed sale, and nothing was collected automatically.'),
  world_dem=dict(global_='Collection level, X-Suits, Glacier M416', cis='Max-level X-Suits (Pharaoh, Raven), sports cars, Mythic count',
                 tr='Collection level, epic item count, maxed guns, sports cars'),
  world_note='Asking prices, not completed sales. Converted at 0.894 EUR and 49.4 TRY per US dollar (October 2026). Descriptive only — not advice to buy or sell; account trading breaks the game’s rules.',
  sources=[f'Eldorado.gg — <a href="{EL}" target="_blank" rel="noopener">PUBG Mobile account listings</a> (10,905), checked October 14, 2026',
           f'FunPay — <a href="{FP}" target="_blank" rel="noopener">PUBG Mobile accounts</a> (6,332), checked October 14, 2026',
           f'GameSatış — <a href="{GS}" target="_blank" rel="noopener">PUBG Mobile hesap satışı</a>, checked October 14, 2026',
           f'Proxima Beta — <a href="{EULA}" target="_blank" rel="noopener">PUBG Mobile terms of service</a>',
           f'PUBG MOBILE Esports — <a href="{PR}" target="_blank" rel="noopener">2026 esports roadmap</a> (press release, December 12, 2025)',
           f'Esports World Cup — <a href="{EWC}" target="_blank" rel="noopener">S2G Esports win the PMWC</a> (August 16, 2026)',
           f'GamingOnPhone — <a href="{GOP}" target="_blank" rel="noopener">how the collection level works</a>'],
 ),
 'ru': dict(
  title='Калькулятор стоимости аккаунта PUBG Mobile (2026): $0.29–$4 960 | GameAccountValue',
  desc='Бесплатный калькулятор по уровню коллекции, без регистрации и сбора данных: цены объявлений на Eldorado.gg, FunPay и GameSatış ($0.29–$4 960), 5 скриншотов для бота, риски обмана.',
  og_title='Сколько стоит мой аккаунт PUBG Mobile? | GameAccountValue',
  og_alt='GameAccountValue — стоимость аккаунта PUBG Mobile',
  h1='🪂 Стоимость аккаунта PUBG Mobile',
  intro='Цены объявлений на трёх площадках, одно число, от которого они зависят, — уровень коллекции, и скриншоты, на которых его видно.',
  updated='Проверено в октябре 2026 по объявлениям на площадках. Источники — в конце страницы.',
  badge='🗓️ Объявления проверены вручную: 14 октября 2026',
  range='Цены в объявлениях: $0.29 – $4 960 · Eldorado.gg, первая страница: $2 – $400',
  facts=['🗂️ В игре <strong>95</strong> уровней коллекции',
         '🥇 Чемпионат мира PUBG Mobile 2026: <strong>S2G Esports</strong> (Турция)',
         '🏆 Global Championship 2026, призовой фонд $3 000 000: <strong>Турция</strong>'],
  thou=' ',
  calc_sub='Один ползунок — уровень коллекции: именно по нему продавцы ставят цену. Ничего не вводится и никуда не отправляется; бот считывает уровень со скриншотов.',
  calc_why='Калькулятор видит только уровень коллекции. Уровни X-костюмов, прокачанное оружие и суперкары он не видит — их бот считает по скриншотам.',
  nav_shots='📸 Скриншоты',
  h2_shots='Скриншоты для оценки',
  q_worth='Сколько стоит аккаунт PUBG Mobile?',
  a_worth=('14 октября 2026 года на Eldorado.gg было <strong>10 905</strong> аккаунтов PUBG Mobile: на первой странице — от $2 за простой аккаунт с рангом «Золото» '
           'до $399.99 за аккаунт с уровнем коллекции 74. На FunPay — <strong>6 332</strong> объявления, от €0.26 до €3 286 (≈ $0.29 – $3 676). '
           'На турецкой GameSatış — от 1 000 ₺ до 245 000 ₺ (≈ $20 – $4 960). Почти весь этот разброс объясняет одно число — уровень коллекции.'),
  q_table='Сколько просят за аккаунт на разных уровнях коллекции?',
  table_head=('Уровень коллекции', 'Цена в объявлении', 'Где'),
  table_note='Цены объявлений на 14 октября 2026, пересчёт по курсу 49.4 ₺ и €0.894 за доллар. Обычно одно объявление на строку — это ориентир, а не прайс-лист. '
             'В объявлении за $909 на уровне 74 указаны ещё 14 прокачанных до максимума стволов.',
  q_value='Что на самом деле определяет цену аккаунта PUBG Mobile?',
  value=['<strong>Уровень коллекции</strong> — в игре 95 уровней; за каждый новый предмет начисляются очки в зависимости от типа и редкости, так что уровень показывает весь инвентарь сразу.',
         '<strong>X-костюмы и их уровень прокачки</strong> — аккаунты с X-костюмом максимального уровня на FunPay стоят €2 063 – €2 629.',
         '<strong>Улучшаемые скины оружия</strong> и уровень каждого (чаще всего в объявлениях упоминают Glacier M416).',
         '<strong>Суперкары</strong> из коллабораций с автобрендами — продавцы перечисляют их поштучно.',
         '<strong>Ранг почти не влияет</strong>: он сбрасывается каждый сезон; на Eldorado.gg аккаунт «Gold Rank» стоил $1.99, «Diamond» — $3.75.'],
  q_lookup='Что посмотреть в игре перед расчётом?',
  lookup=['Калькулятору нужно одно число — <strong>уровень коллекции</strong> с экрана «Коллекция» (например, 74.5).',
          'Результат — примерный диапазон цен в открытых объявлениях, а не предложение о покупке. Покупка и продажа аккаунтов нарушают правила игры — см. <a href="#rules">правила</a>.'],
  q_shots='Какие 5 скриншотов нужны боту для PUBG Mobile?',
  shots_intro='В PUBG Mobile ценное лежит в разных вкладках инвентаря, поэтому бот просит пять скриншотов, а не три:',
  shots=['<strong>Профиль</strong> — видны ID игрока, уровень аккаунта и ранг.',
         '<strong>Коллекция</strong> — экран «Коллекция» с уровнем коллекции (например, 74.5). Это самый важный скриншот.',
         '<strong>Инвентарь → Костюмы</strong> — видны X-костюмы и мифические наряды.',
         '<strong>Улучшаемые скины оружия</strong> — с видимым уровнем (Lv.) каждого.',
         '<strong>Скины транспорта</strong> — суперкары и другие редкие машины; баланс UC, если он виден.'],
  shots_note='Без экрана коллекции бот считает только то, что видно на снимках, — X-костюмы, оружие, суперкары, — и оценка выходит ниже. '
             'Бот никогда не просит логин или пароль, скриншоты не хранятся.',
  q_scams='Какие обманы чаще всего встречаются при продаже аккаунтов PUBG Mobile?',
  a_scams=('Аккаунт PUBG Mobile можно привязать сразу к нескольким входам — например, Facebook, Twitter или Google Play. Любая привязка, оставшаяся у продавца, — '
           'это путь назад: после оплаты аккаунт «восстанавливают», и покупатель остаётся ни с чем. Часть объявлений на FunPay — аренда (с пометкой «Аренда»), а не продажа. '
           'Правила издателя вообще запрещают передавать аккаунт, так что если сделка сорвётся, обратиться в поддержку не сможет ни одна из сторон.'),
  q_rules='Нарушает ли продажа аккаунта PUBG Mobile правила игры?',
  a_rules=('Да. В правилах PUBG Mobile (Proxima Beta Pte. Limited) сказано: аккаунт личный, и его запрещено дарить, одалживать, передавать или иным образом давать '
           'другим людям доступ к нему. Продавать и обменивать виртуальные предметы и валюту тоже нельзя; издатель может заблокировать доступ или расторгнуть соглашение.'),
  q_where='Откуда эти объявления?',
  a_where=('Eldorado.gg и FunPay — международные площадки, GameSatış — турецкая. Каждая цифра на странице — цена объявления, которую мы посмотрели вручную 14 октября 2026 года; '
           'это не завершённые сделки, и автоматически ничего не собиралось.'),
  world_dem=dict(global_='Уровень коллекции, X-костюмы, Glacier M416', cis='X-костюмы максимального уровня (Фараон, Ворон), спорткары, число мификов',
                 tr='Уровень коллекции, число эпических предметов, прокачанное оружие, спорткары'),
  world_note='Это цены объявлений, а не завершённых сделок. Пересчёт по курсу €0.894 и 49.4 ₺ за доллар (октябрь 2026). Только описание рынка — не совет покупать или продавать; торговля аккаунтами нарушает правила игры.',
  sources=[f'Eldorado.gg — <a href="{EL}" target="_blank" rel="noopener">объявления об аккаунтах PUBG Mobile</a> (10 905), проверено 14 октября 2026',
           f'FunPay — <a href="{FP}" target="_blank" rel="noopener">аккаунты PUBG Mobile</a> (6 332), проверено 14 октября 2026',
           f'GameSatış — <a href="{GS}" target="_blank" rel="noopener">PUBG Mobile hesap satışı</a>, проверено 14 октября 2026',
           f'Proxima Beta — <a href="{EULA}" target="_blank" rel="noopener">пользовательское соглашение PUBG Mobile</a>',
           f'PUBG MOBILE Esports — <a href="{PR}" target="_blank" rel="noopener">киберспортивный план на 2026 год</a> (пресс-релиз, 12 декабря 2025)',
           f'Esports World Cup — <a href="{EWC}" target="_blank" rel="noopener">S2G Esports выигрывает PMWC</a> (16 августа 2026)',
           f'GamingOnPhone — <a href="{GOP}" target="_blank" rel="noopener">как устроен уровень коллекции</a>'],
 ),
}
