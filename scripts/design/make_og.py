"""Social preview images (1200x630) in the Cyber-Glass style.
Text is only the game name, the price range and the domain, so one image
serves all languages. Usage: python scripts/design/make_og.py [game ...]
Writes og/<game>.jpg via headless Chrome (fresh profile each run)."""
import os, sys, subprocess, tempfile, uuid
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

# game: (title, accent, second accent, price, top-end note)
GAMES = {
    'roblox': ('Roblox', '#38BDF8', '#22C55E', '$0.50 – $60', '~$800'),
    'brawl-stars': ('Brawl Stars', '#FFD21F', '#B86BFF', '$3 – $150', '$300+'),
    'clash-of-clans': ('Clash of Clans', '#F6B042', '#E8823A', '$10 – $260', ''),
    'clash-royale': ('Clash Royale', '#7C9BFF', '#F9C846', '$0.50 – $600+', ''),
    'free-fire': ('Free Fire', '#FF8A1F', '#FF4D4D', '$0.73 – $250', '~$755'),
    'genshin-impact': ('Genshin Impact', '#6EE7D8', '#E9C46A', '$5 – $60', '$9,000'),
    'mobile-legends': ('Mobile Legends', '#FF6B85', '#F4C95D', '$0.50 – $300', '~$605'),
    'fortnite': ('Fortnite', '#B98BFF', '#4DB0FF', '$10.90 – $6,200', ''),
    'minecraft': ('Minecraft', '#7BD34F', '#C0925E', '$0.50 – $632', ''),
    # site-wide image (homepages, resource pages)
    'default': ('Game Account Value', '#22D3EE', '#A78BFA', '9 games', '17 languages'),
}

TPL = '''<!doctype html><meta charset=utf-8><style>
@font-face{font-family:Inter;src:url(%%FONT%%);font-weight:100 900}
*{margin:0;box-sizing:border-box}
body{width:1200px;height:630px;overflow:hidden;background:#080B11;font-family:Inter,sans-serif;color:#F4F6FB;position:relative}
.g1{position:absolute;width:760px;height:760px;left:-180px;top:-280px;background:radial-gradient(closest-side,color-mix(in srgb,%%B%% 50%,transparent),transparent)}
.g2{position:absolute;width:640px;height:640px;right:-140px;bottom:-280px;background:radial-gradient(closest-side,color-mix(in srgb,%%A%% 32%,transparent),transparent)}
.grid{position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.035) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.035) 1px,transparent 1px);background-size:40px 40px}
.city{position:absolute;left:0;right:0;bottom:0;height:340px;opacity:.6}.city svg{width:100%;height:100%}
.card{position:absolute;inset:64px;border:1px solid rgba(255,255,255,.14);border-radius:36px;background:linear-gradient(135deg,rgba(20,24,38,.9),rgba(12,14,24,.72));box-shadow:0 30px 80px rgba(0,0,0,.5);padding:52px 64px;display:flex;flex-direction:column;justify-content:space-between}
.top{display:flex;align-items:center;gap:18px;font-weight:800;font-size:32px}
.top img{width:68px;height:68px;border-radius:16px}
.age{margin-left:auto;font-size:22px;font-weight:800;padding:8px 16px;border-radius:12px;border:2px solid rgba(255,255,255,.35);color:#cfd5e6}
h1{font-size:%%H1%%px;max-width:690px;font-weight:900;letter-spacing:-.03em;line-height:1.05}
h1 span{background:linear-gradient(90deg,%%A%%,%%B%%);-webkit-background-clip:text;background-clip:text;color:transparent}
.price{max-width:690px;flex-wrap:wrap;display:flex;align-items:baseline;gap:22px;margin-top:18px}
.price b{font-size:%%PB%%px;font-weight:900;color:%%A%%;text-shadow:0 0 34px color-mix(in srgb,%%A%% 50%,transparent);letter-spacing:-.02em}
.price i{font-style:normal;font-size:34px;color:#cfd5e6;font-weight:700}
.bot{position:absolute;right:56px;top:60px;width:320px;height:320px;filter:drop-shadow(0 0 40px color-mix(in srgb,%%B%% 55%,transparent))}.bot svg{width:100%;height:100%}
.foot{display:flex;align-items:center;justify-content:space-between;font-size:28px;font-weight:700}
.bar{height:10px;border-radius:6px;background:linear-gradient(90deg,%%A%%,%%B%%);width:420px;box-shadow:0 0 24px color-mix(in srgb,%%B%% 60%,transparent)}
</style>
<div class=g1></div><div class=g2></div><div class=grid></div><div class=city>%%CITY%%</div>
<div class=card>
 <div class=top><img src="%%EMBLEM%%">GameAccountValue<span class=age>18+</span></div>
 <div><h1><span>%%TITLE%%</span></h1><div class=price><b>%%PRICE%%</b>%%TOPEND%%</div></div>
 <div class=bot>%%BOT%%</div>
 <div class=foot><div class=bar></div><span>gameaccountvalue.com</span></div>
</div>'''


def file_url(p):
    return 'file:///' + p.replace('\\', '/')


def render(game, out_dir):
    title, a, b, price, top = GAMES[game]
    tmp = tempfile.mkdtemp()
    emblem = os.path.join(tmp, 'emblem.png')
    import emblem as em_mod
    em_mod.emblem(192).save(emblem)
    city = open(os.path.join(HERE, 'city.svg'), encoding='utf-8').read()
    import importlib.util as iu
    sp = iu.spec_from_file_location('br', os.path.join(HERE, 'brand_rollout.py')); br = iu.module_from_spec(sp); sp.loader.exec_module(br)
    bot = open(os.path.join(HERE, 'bot.svg'), encoding='utf-8').read()
    bot = bot.replace(br.ROBOT_LINE, br.ROBOT_EMBLEM.replace('{P}assets/emblem.webp', file_url(os.path.join(ROOT, 'assets', 'emblem.webp')))).replace(br.ROBOT_TEXT, br.ROBOT_TEXT_NEW)
    h1 = 96 if len(title) <= 12 else (78 if len(title) <= 15 else 72)
    pb = 80 if len(price) <= 11 else 66
    html = (TPL.replace('%%FONT%%', file_url(os.path.join(ROOT, 'assets', 'fonts', 'inter-latin.woff2')))
            .replace('%%CITY%%', city).replace('%%BOT%%', bot).replace('%%H1%%', str(h1)).replace('%%PB%%', str(pb)).replace('%%EMBLEM%%', file_url(emblem)).replace('%%TITLE%%', title)
            .replace('%%PRICE%%', price).replace('%%TOPEND%%', '<i>/ ' + top + '</i>' if top else '').replace('%%A%%', a).replace('%%B%%', b))
    page = os.path.join(tmp, 'og.html')
    open(page, 'w', encoding='utf-8').write(html)
    shot = os.path.join(tmp, 'og.png')
    subprocess.run([CHROME, '--headless=new', '--user-data-dir=' + os.path.join(tmp, 'p' + uuid.uuid4().hex),
                    '--window-size=1200,630', '--hide-scrollbars', '--screenshot=' + shot, file_url(page)],
                   capture_output=True, timeout=60)
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, game + '.jpg')
    Image.open(shot).convert('RGB').save(out, quality=88, optimize=True, progressive=True)
    return out


if __name__ == '__main__':
    out_dir = os.environ.get('OG_OUT', os.path.join(ROOT, 'og'))
    for g in sys.argv[1:] or GAMES:
        print(render(g, out_dir))
