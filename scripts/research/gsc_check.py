"""Search Console check-up (read-only API, key in ~/.gav-gsc.json — never commit it).
What it answers, in this order:
  1. Is traffic growing?            daily clicks / impressions, last 7 days vs the 7 before
  2. Where do readers come from?    countries and devices
  3. Which pages can move up?       positions 8-20 with real impressions  -> improve content, re-check in 2-4 weeks
  4. Which snippets fail?           top-7 positions with CTR under 2%     -> read the visible queries before touching a title
  5. What is not in the index?      URL Inspection for the main page types in all 24 languages (--index, ~400 calls)
Rules for using the numbers (SITE-STANDARD.md): most queries are hidden; never rewrite a page for 1-3 visible queries,
never add a page per query, never chase another site's brand name. The API cannot request indexing or submit sitemaps.

  python scripts/research/gsc_check.py            (items 1-4)
  python scripts/research/gsc_check.py --index    (adds item 5; quota 2,000 inspections a day)
"""
import collections, concurrent.futures as cf, datetime, io, os, sys, threading

from google.oauth2 import service_account
from googleapiclient.discovery import build

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
SITE = 'sc-domain:gameaccountvalue.com'
BASE = 'https://gameaccountvalue.com/'
LANGS = ['', 'ru', 'es', 'pt', 'id', 'tr', 'ar', 'vi', 'hi', 'fr', 'de', 'it', 'ja', 'ko', 'th', 'pl', 'zh', 'tl', 'sw', 'ms', 'uz', 'kk', 'tk', 'ky']
PAGES = ['', 'roblox.html', 'brawl-stars.html', 'clash-of-clans.html', 'clash-royale.html', 'free-fire.html', 'genshin-impact.html',
         'mobile-legends.html', 'fortnite.html', 'minecraft.html', 'market-report.html', 'which-game-accounts-are-most-valuable.html',
         'account-trading-safety.html', 'glossary.html', 'methodology.html', 'about.html', 'news.html']
_local = threading.local()


def svc():
    if not hasattr(_local, 's'):
        cr = service_account.Credentials.from_service_account_file(
            os.path.expanduser('~/.gav-gsc.json'), scopes=['https://www.googleapis.com/auth/webmasters.readonly'])
        _local.s = build('searchconsole', 'v1', credentials=cr, cache_discovery=False)
    return _local.s


def query(dims, start, end, **kw):
    body = dict(startDate=str(start), endDate=str(end), dimensions=dims, rowLimit=25000, **kw)
    return svc().searchanalytics().query(siteUrl=SITE, body=body).execute().get('rows', [])


def short(u):
    return u.replace(BASE, '/')


def traffic():
    end = datetime.date.today() - datetime.timedelta(days=1)
    start = end - datetime.timedelta(days=27)
    tot = lambda rows: (sum(r['clicks'] for r in rows), sum(r['impressions'] for r in rows))
    days = query(['date'], start, end, dataState='all')
    print(f'PERIOD {start} .. {end} (the last 1-2 days are incomplete)')
    for r in days[-10:]:
        print('  ', r['keys'][0], r['clicks'], r['impressions'], round(r['position'], 1))
    print('last 7 days', tot(days[-7:]), '| previous 7', tot(days[-14:-7]), '| 28 days', tot(days))
    print('\nCOUNTRIES')
    for r in sorted(query(['country'], start, end), key=lambda r: -r['impressions'])[:12]:
        print('   %s  clicks %d  impressions %d  position %.1f  CTR %.1f%%' % (r['keys'][0], r['clicks'], r['impressions'], r['position'], 100 * r['ctr']))
    print('\nDEVICES')
    for r in query(['device'], start, end):
        print('   %s  clicks %d  impressions %d  position %.1f' % (r['keys'][0], r['clicks'], r['impressions'], r['position']))
    pages = query(['page'], start, end)
    print('\nROOM TO GROW: position 8-20, 15+ impressions')
    for r in sorted((r for r in pages if 8 <= r['position'] <= 20 and r['impressions'] >= 15), key=lambda r: -r['impressions'])[:15]:
        print('   %4d impressions %2d clicks position %4.1f  %s' % (r['impressions'], r['clicks'], r['position'], short(r['keys'][0])))
    print('\nSNIPPET CHECK: position under 8, CTR under 2%, 30+ impressions')
    for r in sorted((r for r in pages if r['position'] < 8 and r['ctr'] < 0.02 and r['impressions'] >= 30), key=lambda r: -r['impressions'])[:12]:
        print('   %4d impressions %2d clicks position %4.1f  %s' % (r['impressions'], r['clicks'], r['position'], short(r['keys'][0])))
    news = [r for r in pages if '/news' in r['keys'][0]]
    print('\nNEWS: %d pages with impressions, clicks/impressions %s' % (len(news), tot(news)))


def inspect(args):
    lang, page = args
    url = BASE + (lang + '/' if lang else '') + page
    try:
        r = svc().urlInspection().index().inspect(body=dict(inspectionUrl=url, siteUrl=SITE)).execute()['inspectionResult']['indexStatusResult']
        return lang or 'en', page or 'home', r.get('coverageState', '?'), r.get('lastCrawlTime', '')[:10]
    except Exception as e:      # quota or network: report, keep going
        return lang or 'en', page or 'home', 'ERR ' + str(e)[:60], ''


def index():
    with cf.ThreadPoolExecutor(5) as ex:
        res = list(ex.map(inspect, [(l, p) for l in LANGS for p in PAGES]))
    print('\nINDEX STATUS of %d main pages: %s' % (len(res), dict(collections.Counter(r[2] for r in res))))
    by_page, by_lang = collections.defaultdict(int), collections.defaultdict(int)
    for l, p, st, _ in res:
        if 'indexed' in st.lower() and 'not indexed' not in st.lower():
            by_page[p] += 1; by_lang[l] += 1
    print('indexed per page type (of 24):', {p or 'home': by_page[p or 'home'] for p in PAGES})
    print('indexed per language (of %d):' % len(PAGES), {l or 'en': by_lang[l or 'en'] for l in LANGS})
    print('\nCRAWLED BUT NOT INDEXED (Google read the page and passed on it - the pages to improve first):')
    for l, p, st, d in res:
        if st.startswith('Crawled'):
            print('   %-3s %-44s crawled %s' % (l, p, d))


if __name__ == '__main__':
    traffic()
    if '--index' in sys.argv:
        index()
