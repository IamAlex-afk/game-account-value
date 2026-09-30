"""Finish a locale built from EN once its translation chunks exist.

  python scripts/i18n/finish_locale.py <lang> <chunk_dir> <prev_lang> <config.json>

config.json: {"keywords": "...", "calc": {STR block as JSON}, "market": "cis|sea|global|...",
              "country": "KZ", "world_extra": {EN world string: translation}}
Steps (same recipe as ms/uz, see PLAN.md): merge chunk translations into
scripts/i18n/<lang>/done.json -> segments build -> from_en -> calculators.js STR
+ whitelist -> CLDR dates/names -> world generator dicts -> world regeneration
-> hreflang after <prev_lang> on the 13 shared pages -> sitemap.
"""
import glob, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + os.sep
lang, chunk_dir, prev, cfg_path = sys.argv[1:5]
cfg = json.load(open(cfg_path, encoding="utf-8"))
PAGES = ["roblox", "brawl-stars", "clash-of-clans", "clash-royale", "free-fire", "genshin-impact", "mobile-legends",
         "fortnite", "minecraft", "methodology", "account-trading-safety", "which-game-accounts-are-most-valuable", "glossary"]
GAMES = ["brawl-stars", "roblox", "clash-of-clans", "clash-royale", "free-fire", "genshin-impact", "mobile-legends", "fortnite", "minecraft"]
S = "https://gameaccountvalue.com/"
py = [sys.executable]
env = dict(os.environ, PYTHONIOENCODING="utf-8")

def run(args, cwd=ROOT):
    r = subprocess.run(args, cwd=cwd, env=env, capture_output=True, text=True, encoding="utf-8")
    if r.returncode:
        sys.exit(f"FAILED {args}:\n{r.stdout}\n{r.stderr}")
    return r.stdout

# 1) merge
segs = list(json.load(open(ROOT + f"scripts/i18n/{lang}/todo.json", encoding="utf-8")))
tr = {}
for f in sorted(glob.glob(os.path.join(chunk_dir, "t*.json"))):
    for k, v in json.load(open(f, encoding="utf-8")).items():
        tr[int(k)] = v
ref = json.load(open(ROOT + "scripts/i18n/ms/done.json", encoding="utf-8"))
done, miss = {}, []
sys.path.insert(0, ROOT + "scripts/i18n")
from numfmt import local_numbers
for i, s in enumerate(segs):
    done[s] = tr.get(i, s)
    if cfg.get("numfmt") and i in tr:
        done[s] = local_numbers(done[s])
    if i not in tr and ref.get(s, s) != s:
        miss.append((i, s[:70]))
if miss:
    sys.exit(f"untranslated vs ms reference: {miss[:10]}")
json.dump(done, open(ROOT + f"scripts/i18n/{lang}/done.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print("merged", len(tr))

# 2) keywords + build + from_en
fe = ROOT + "scripts/i18n/from_en.py"
s = open(fe, encoding="utf-8").read()
if f'"{lang}":' not in s.split("KEYWORDS = {")[1].split("}")[0]:
    s = s.replace("KEYWORDS = {\n", "KEYWORDS = {\n    " + json.dumps(lang) + ": " + json.dumps(cfg["keywords"], ensure_ascii=False) + ",\n", 1)
    open(fe, "w", encoding="utf-8", newline="\n").write(s)
print(run(py + ["scripts/i18n/segments.py", "build", "en", lang]).strip())
print(run(py + ["scripts/i18n/from_en.py", lang]).strip())

# 3) calculator
cj = ROOT + "assets/calculators.js"
s = open(cj, encoding="utf-8").read()
if f'"{lang}"]' not in s.split("\n")[5]:
    c = cfg["calc"]
    block = ("    " + lang + ": {\n      sliders: " + json.dumps(c["sliders"], ensure_ascii=False) +
             ",\n      select: " + json.dumps(c["select"], ensure_ascii=False) +
             ",\n      ageUnit: function (v) { return v + " + json.dumps(" " + c["year"], ensure_ascii=False) + "; },\n" +
             "      minecraftTypes: " + json.dumps(c["minecraftTypes"], ensure_ascii=False) +
             ",\n      checkboxHeading: " + json.dumps(c["checkboxHeading"], ensure_ascii=False) +
             ",\n      confidence: " + json.dumps(c["confidence"], ensure_ascii=False) +
             ",\n      confidencePrefix: " + json.dumps(c["confidencePrefix"], ensure_ascii=False) +
             ",\n      copiedFallback: " + json.dumps(c["copiedFallback"], ensure_ascii=False) +
             ",\n      gamepad: " + json.dumps(c["gamepad"], ensure_ascii=False) + "\n    }")
    end = "    }\n  };\n  var T = STR[LANG];"
    assert s.count(end) == 1
    s = s.replace(end, "    },\n" + block + "\n  };\n  var T = STR[LANG];", 1)
    lines = s.split("\n")
    lines[5] = lines[5].replace('].indexOf(LANG)', ', "' + lang + '"].indexOf(LANG)')
    s = "\n".join(lines)
    open(cj, "w", encoding="utf-8", newline="\n").write(s)
run(["node", "-e", "global.window={};global.document={documentElement:{getAttribute:()=>'" + lang +
     "'},querySelectorAll:()=>[],querySelector:()=>null,readyState:'loading',addEventListener:()=>{},getElementById:()=>null};"
     "global.navigator={};global.location={href:''};eval(require('fs').readFileSync('assets/calculators.js','utf8'));"
     "if(!window.GAVCalc)process.exit(1)"])
print("calculator ok")

# 4) CLDR dates + names
d = ROOT + "scripts/design/"
bj = open(d + "build_event_dates.js", encoding="utf-8").read()
if f"'{lang}'" not in bj.split("\n")[3]:
    bj = bj.replace("];", f",'{lang}'];", 1)
    open(d + "build_event_dates.js", "w", encoding="utf-8", newline="\n").write(bj)
run(["node", "build_event_dates.js"], cwd=d)
cc = cfg["country"]
run(["node", "-e", f"""
const fs=require('fs');const f='country_names.json';const d=JSON.parse(fs.readFileSync(f,'utf8'));
const r=new Intl.DisplayNames(['{lang}'],{{type:'region'}}),L=new Intl.DisplayNames(['{lang}'],{{type:'language'}});
const keys=new Set(Object.keys(d.countries.en));keys.add('{cc}');
d.countries['{lang}']={{}};for(const c of keys) d.countries['{lang}'][c]=r.of(c);
d.languages['{lang}']={{}};for(const c of Object.keys(d.languages.en)) d.languages['{lang}'][c]=L.of(c);
fs.writeFileSync(f,JSON.stringify(d));"""], cwd=d)
print("cldr ok")

# 5) world generator dicts
sys.path.insert(0, d)
os.chdir(d)
import importlib
WM = importlib.import_module("world_markets"); WX = importlib.import_module("world_extra")
WE = importlib.import_module("world_events"); WR = importlib.import_module("world_results"); WD = importlib.import_module("world_data")
tbl = dict(done); tbl.update(cfg["world_extra"])
missing = []
def m(v):
    if isinstance(v, str):
        if v in tbl: return tbl[v]
        missing.append(v); return v
    if isinstance(v, tuple): return tuple(m(x) for x in v)
    if isinstance(v, list): return [m(x) for x in v]
    if isinstance(v, dict): return {k: m(x) for k, x in v.items()}
    return v
if lang not in WM.T:
    import pprint
    blocks = {
        "world_markets.py": f"\n# {lang} (auto, finish_locale.py)\nLANGS.append('{lang}')\nLOCAL['{lang}'] = '{cfg['market']}'\nT['{lang}'] = " + pprint.pformat(m(WM.T['en']), width=160) + "\n",
        "world_extra.py": f"\n# {lang}\nLANG_COUNTRY['{lang}'] = '{cc}'\nX['{lang}'] = " + pprint.pformat(m(WX.X['en']), width=160) + "\n",
        "world_events.py": f"\n# {lang}\nL['{lang}'] = " + pprint.pformat(m(WE.L['en']), width=160) + "\n",
        "world_results.py": f"\n# {lang}\nRL['{lang}'] = " + pprint.pformat(m(WR.RL['en']), width=160) + "\n",
        "world_data.py": f"\n# {lang}\nN['{lang}'] = " + pprint.pformat(m(WD.N['en']), width=160) + f"\nTW_ONLY['{lang}'] = " + repr(m(WD.TW_ONLY['en'])) + "\n",
    }
    if missing:
        sys.exit(f"world strings missing: {missing}")
    for f, b in blocks.items():
        open(d + f, "a", encoding="utf-8", newline="\n").write(b)
    wm = open(d + "world_markets.py", encoding="utf-8").read()
    main = "if __name__ == '__main__':\n    apply(sys.argv[1] if len(sys.argv) > 1 else 'brawl-stars')\n"
    wm = wm.replace(main, "").rstrip("\n") + "\n\n" + main
    open(d + "world_markets.py", "w", encoding="utf-8", newline="\n").write(wm)
for g in GAMES:
    run(py + ["world_markets.py", g], cwd=d)
os.chdir(ROOT)
print("world ok")

# 6) hreflang + sitemap
n = 0
for p in PAGES:
    for f in [f"{p}.html"] + [x for x in glob.glob(f"*/{p}.html") if not x.startswith(("scripts", "_tmp"))]:
        s = open(f, encoding="utf-8").read()
        if f'hreflang="{lang}"' in s: continue
        a = f'<link rel="alternate" hreflang="{prev}" href="{S}{prev}/{p}.html">'
        assert a in s, f
        s = s.replace(a, a + f'\n<link rel="alternate" hreflang="{lang}" href="{S}{lang}/{p}.html">', 1)
        open(f, "w", encoding="utf-8", newline="").write(s); n += 1
sm = open("sitemap.xml", encoding="utf-8").read()
if f"{S}{lang}/roblox.html" not in sm:
    line = next(l for l in sm.splitlines(True) if f"/{lang}/market-report.html" in l)
    add = "".join(f"  <url><loc>{S}{lang}/{p}.html</loc><lastmod>2026-09-30</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>\n" for p in PAGES)
    sm = sm.replace(line, re.sub(r"<lastmod>[^<]*", "<lastmod>2026-09-30", line) + add)
    sm = re.sub(rf"(<loc>{re.escape(S)}{lang}/</loc><lastmod>)[^<]*", r"\g<1>2026-09-30", sm)
    open("sitemap.xml", "w", encoding="utf-8", newline="").write(sm)
print("hreflang added", n, "| sitemap", sm.count("<url>"))
