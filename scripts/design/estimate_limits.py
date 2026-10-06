"""'What an estimate can and can't tell you' block on game pages (SITE-STANDARD plan step 5).
Placed after 'What Actually Determines Value', before 'Scams & Trading Risks'.
Every line restates a fact already on that page (price table, sources, rules) or in the
bot's own pricer (GameAccountValue_Bot core/valuation.py) - nothing new is claimed.
Rollout is deliberately slow (owner, 2026-10-05): one game at a time, EN + RU first;
other languages only after native review. Idempotent via <!--limits--> markers.
Run: python scripts/design/estimate_limits.py"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + os.sep

# TEXT[lang][game] = (heading, intro, solid_title, [solid...], limits_title, [limits...])
TEXT = {
 'en': {
  'clash-royale': (
   "What an estimate can and can't tell you",
   'The calculator above and the bot both turn what they can see into a price range. '
   'Here is where that range stands on firm ground and where it doesn&rsquo;t.',
   'Where it holds up',
   ['It rests on real listings: Eldorado.gg (from $0.50 for a starter account to $600 for a full max one) and '
    '852 igitems.com listings broken into price brackets (September 2026).',
    'In the 10 highest-priced listings checked, 9 named no cosmetics at all &mdash; titles were built on King Tower level, '
    'trophies and evolutions, the same things the estimate is built on.',
    'The quick calculator asks only King Tower level and max-level cards. The bot&rsquo;s screenshot check also reads '
    'evolutions, champions, heroes, tower skins, rare emotes, trophies, gems, Pass Royale, a CRL badge and global tournament wins.'],
   'Where it falls short',
   ['These are asking prices. On igitems.com sold prices ran about 21% below asking &mdash; what a buyer finally pays is '
    'usually lower than the listing.',
    'The market moves fast: the average asking price there rose from $81.89 to $107.20 in a few months. The figures are '
    'from September 2026 and change with every season and balance update.',
    'Two accounts at the same King Tower level can differ a lot in value: evolutions and card levels matter, and the '
    'quick calculator cannot see them.',
    'A price is not a permission. Supercell&rsquo;s Terms of Service prohibit selling or transferring accounts, and a traded '
    'account can be banned for good &mdash; the range describes the market, it does not say anyone could or should sell.']),
  'clash-of-clans': (
   "What an estimate can and can't tell you",
   'The calculator above and the bot both turn what they can see into a price range. '
   'Here is where that range stands on firm ground and where it doesn\'t.',
   'Where it holds up',
   ['It rests on a large sample: 4,463 igitems.com listings, broken out by Town Hall level and upgrade progress '
    '(September 2026), with Eldorado.gg and EpicNPC listings showing the same general shape.',
    'Town Hall level and how complete the base is are the two biggest price drivers in that data &mdash; '
    'a full-max TH18 lists for $100&ndash;$260, a rushed one for $20&ndash;$35.',
    'The quick calculator asks only those two things. The bot\'s screenshot check also reads hero levels, '
    'epic equipment, hero skins, sceneries, CWL medals and Builder Hall level.'],
   'Where it falls short',
   ['These are asking prices, not completed sales: listings show what sellers want, not what buyers finally paid.',
    'Asking prices are not always logical. At TH17, rushed accounts are listed at up to $55 &mdash; above the $50 '
    'top of standard ones. The table shows the market as it is, without smoothing it out.',
    'A snapshot ages. The figures are from September 2026 and shift with every Town Hall release and balance update.',
    'A price is not a permission. Supercell\'s Terms of Service prohibit selling or transferring accounts, and a '
    'traded account can be banned for good &mdash; the range describes the market, it does not say anyone could '
    'or should sell.']),
 },
 'ru': {
  'clash-royale': (
   'Что оценка может и чего не может сказать',
   'И калькулятор выше, и бот превращают то, что видят, в диапазон цен. '
   'Вот где этот диапазон надёжен, а где нет.',
   'На что можно опираться',
   ['В основе реальные объявления: Eldorado.gg (от $0.50 за стартовый аккаунт до $600 за «полностью максимальный») и '
    '852 объявления igitems.com с разбивкой по ценовым корзинам (сентябрь 2026).',
    'В 10 самых дорогих проверенных объявлениях 9 не назвали ни одного косметического предмета &mdash; заголовки строились '
    'на уровне Королевской башни, кубках и эволюциях, то есть на том же, на чём строится оценка.',
    'Быстрый калькулятор спрашивает только уровень King Tower и число карт максимального уровня. Бот по скриншотам '
    'дополнительно читает эволюции, чемпионов, героев, скины башен, редкие эмоции, кубки, гемы, Pass Royale, значок CRL '
    'и победы в глобальных турнирах.'],
   'Где у оценки пределы',
   ['Это цены в объявлениях. На igitems.com реальные продажи шли примерно на 21% ниже запрашиваемых цен &mdash; '
    'покупатель в итоге обычно платит меньше, чем написано в объявлении.',
    'Рынок быстро меняется: средняя запрашиваемая цена там выросла с $81.89 до $107.20 за несколько месяцев. Цифры '
    'собраны в сентябре 2026 и меняются с каждым сезоном и балансным обновлением.',
    'Два аккаунта с одинаковым уровнем King Tower могут стоить очень по-разному: важны эволюции и уровни карт, а быстрый '
    'калькулятор их не видит.',
    'Цена &mdash; не разрешение. Условия использования Supercell запрещают продавать и передавать аккаунты, а проданный '
    'аккаунт могут заблокировать навсегда. Диапазон описывает рынок и не означает, что аккаунт можно или стоит продавать.']),
  'clash-of-clans': (
   'Что оценка может и чего не может сказать',
   'И калькулятор выше, и бот превращают то, что видят, в диапазон цен. '
   'Вот где этот диапазон надёжен, а где нет.',
   'На что можно опираться',
   ['В основе большая выборка: 4&nbsp;463 объявления igitems.com с разбивкой по уровню Ратуши и прокачке '
    '(сентябрь 2026), а объявления на Eldorado.gg и EpicNPC показывают ту же общую картину.',
    'Уровень Ратуши и то, насколько докачана база, &mdash; два главных фактора цены в этих данных: '
    'TH18 в «полном максе» выставляется за $100&ndash;$260, раш-аккаунт &mdash; за $20&ndash;$35.',
    'Быстрый калькулятор спрашивает только эти два параметра. Бот по скриншотам дополнительно читает уровни героев, '
    'эпическое снаряжение, скины героев, декорации, медали ЛВК и уровень Деревни строителя.'],
   'Где у оценки пределы',
   ['Это цены в объявлениях, а не завершённые сделки: видно, сколько просят продавцы, но не сколько в итоге заплатили.',
    'Цены в объявлениях не всегда логичны. На TH17 раш-аккаунты выставляют до $55 &mdash; дороже верхней планки '
    '«Стандарта» ($50). Таблица показывает рынок как есть, без сглаживания.',
    'Снимок устаревает. Цифры собраны в сентябре 2026 и меняются с каждой новой Ратушей и балансным обновлением.',
    'Цена &mdash; не разрешение. Условия использования Supercell запрещают продавать и передавать аккаунты, а '
    'проданный аккаунт могут заблокировать навсегда. Диапазон описывает рынок и не означает, что аккаунт можно или '
    'стоит продавать.']),
 },
}


def block(t):
    h, intro, st, solid, lt, limits = t
    ul = lambda items: '<ul>' + ''.join(f'<li>{x}</li>' for x in items) + '</ul>'
    return (f'<!--limits--><section class="g-card g-news-card"><span id="limits" class="anchor-target"></span>\n'
            f'<h2>{h}</h2>\n<p>{intro}</p>\n<h3>✅ {st}</h3>\n{ul(solid)}\n<h3>⚠️ {lt}</h3>\n{ul(limits)}\n</section><!--/limits-->\n')


def main():
    n = 0
    for lang, games in TEXT.items():
        for game, t in games.items():
            p = ROOT + ('' if lang == 'en' else lang + os.sep) + game + '.html'
            s = open(p, encoding='utf-8').read()
            s = re.sub(r'<!--limits-->.*?<!--/limits-->\n', '', s, flags=re.S)
            anchor = '<section class="g-card g-news-card"><span id="scams" class="anchor-target"></span>'
            if s.count(anchor) != 1:
                raise SystemExit(f'{p}: scams section anchor not found exactly once')
            s = s.replace(anchor, block(t) + anchor, 1)
            open(p, 'w', encoding='utf-8', newline='').write(s)
            n += 1
    print('limits block on', n, 'pages')


if __name__ == '__main__':
    main()
