"""Translation round-trip for building a new full locale from an existing one.

  python scripts/i18n/segments.py extract <base_lang> <new_lang>
      → scripts/i18n/<new_lang>/todo.json : {segment: ""} for every
        translatable string on the base locale's 15 pages (visible text,
        SEO/social meta, alt/aria/title attributes, data-* UI labels,
        JSON-LD strings); already-translated keys in done.json are kept.
  python scripts/i18n/segments.py build <base_lang> <new_lang>
      → writes <new_lang>/*.html from the base pages using done.json
        (exact-segment replacement; untranslated segments are reported and
        the build refuses to write while any remain).

Paths, lang attributes, canonical/og:url and inLanguage are rewritten for
the new locale; hreflang wiring across the whole site is a separate step.
"""
import json, os, re, sys, html as H

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + os.sep
PAGES = ["index", "roblox", "brawl-stars", "clash-of-clans", "clash-royale", "free-fire", "genshin-impact",
         "mobile-legends", "fortnite", "minecraft", "methodology", "account-trading-safety",
         "which-game-accounts-are-most-valuable", "glossary", "market-report"]
LETTER = re.compile(r"[^\W\d_]", re.U)
SKIP_BLOCKS = re.compile(r"(?is)<(script|style|svg|code)\b[^>]*>.*?</\1>")
ATTRS = ("alt", "aria-label", "title", "placeholder", "data-copied", "data-l-days", "data-l-tomorrow",
         "data-l-live", "data-l-month", "data-l-done", "data-title")
META = re.compile(r'<meta\s+(?:name|property)="(description|og:title|og:description|og:image:alt|twitter:title|twitter:description|og:site_name)"\s+content="([^"]*)"')
LD_KEYS = {"name", "description", "text", "headline", "alternateName", "about", "abstract", "keywords",
           "articleSection", "disambiguatingDescription", "caption", "award"}


def page_path(lang, page):
    return ROOT + (page + ".html" if lang == "en" else f"{lang}/{page}.html")


def _ld_strings(node, out):
    if isinstance(node, dict):
        for k, v in node.items():
            if k in LD_KEYS and isinstance(v, str):
                out.append(v)
            elif isinstance(v, (dict, list)):
                _ld_strings(v, out)
            elif k in LD_KEYS and isinstance(v, list):
                out += [x for x in v if isinstance(x, str)]
    elif isinstance(node, list):
        for x in node:
            _ld_strings(x, out)


def segments(src: str) -> list:
    segs = []
    m = re.search(r"<title>(.*?)</title>", src, re.S)
    if m:
        segs.append(H.unescape(m.group(1).strip()))
    segs += [H.unescape(c) for _, c in META.findall(src)]
    body = SKIP_BLOCKS.sub(" ", src[src.find("<body"):] if "<body" in src else src)
    for t in re.findall(r">([^<>]+)<", body):
        t = H.unescape(t).strip()
        if LETTER.search(t):
            segs.append(t)
    for a in ATTRS:
        segs += [H.unescape(v) for v in re.findall(r'\s' + re.escape(a) + r'="([^"]*)"', body) if LETTER.search(v)]
    for block in re.findall(r'(?s)<script type="application/ld\+json">(.*?)</script>', src):
        try:
            _ld_strings(json.loads(block), segs)
        except ValueError:
            pass
    seen, out = set(), []
    for s in segs:
        s = s.strip()
        if s and LETTER.search(s) and s not in seen:
            seen.add(s)
            out.append(s)
    return out


def extract(base, new):
    d = ROOT + f"scripts/i18n/{new}/"
    os.makedirs(d, exist_ok=True)
    done = json.load(open(d + "done.json", encoding="utf-8")) if os.path.exists(d + "done.json") else {}
    todo, total = {}, 0
    for p in PAGES:
        for s in segments(open(page_path(base, p), encoding="utf-8").read()):
            total += 1
            if s not in done:
                todo[s] = ""
    json.dump(todo, open(d + "todo.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print(f"{len(todo)} segments to translate ({len(done)} done, {total} occurrences)")


def _replace_text_nodes(body, tr):
    # text can also sit right after a protected <svg>/<script> placeholder
    # (\x00N\x00), e.g. an icon followed by a button label
    def rep(m):
        raw = m.group(2)
        t = H.unescape(raw).strip()
        if t in tr:
            lead = raw[: len(raw) - len(raw.lstrip())]
            trail = raw[len(raw.rstrip()):]
            return m.group(1) + lead + H.escape(tr[t], quote=False) + trail
        return m.group(0)
    return re.sub(r"(>|\x00\d+\x00)([^<>\x00]+)(?=<|\x00)", rep, body)


def build(base, new):
    d = ROOT + f"scripts/i18n/{new}/"
    tr = json.load(open(d + "done.json", encoding="utf-8"))
    missing = set()
    for p in PAGES:
        src = open(page_path(base, p), encoding="utf-8").read()
        missing |= {s for s in segments(src) if s not in tr}
    if missing:
        json.dump({s: "" for s in sorted(missing)}, open(d + "todo.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
        sys.exit(f"{len(missing)} untranslated segments — see {d}todo.json")
    os.makedirs(ROOT + new, exist_ok=True)
    for p in PAGES:
        s = open(page_path(base, p), encoding="utf-8").read()
        # protect script/style/svg/code blocks, translate the rest
        blocks = []
        def keep(m):
            blocks.append(m.group(0))
            return f"\x00{len(blocks) - 1}\x00"
        s = SKIP_BLOCKS.sub(keep, s)
        s = re.sub(r"<title>(.*?)</title>", lambda m: "<title>" + H.escape(tr.get(H.unescape(m.group(1).strip()), H.unescape(m.group(1))), quote=False) + "</title>", s, 1, re.S)
        s = META.sub(lambda m: m.group(0).replace(m.group(2), H.escape(tr.get(H.unescape(m.group(2)), H.unescape(m.group(2))))), s)
        for a in ATTRS:
            s = re.sub(r'(\s' + re.escape(a) + r'=")([^"]*)(")', lambda m: m.group(1) + H.escape(tr.get(H.unescape(m.group(2)), H.unescape(m.group(2)))) + m.group(3), s)
        s = _replace_text_nodes(s, tr)
        s = re.sub("\x00(\\d+)\x00", lambda m: blocks[int(m.group(1))], s)
        # JSON-LD strings
        def ld(m):
            try:
                data = json.loads(m.group(1))
            except ValueError:
                return m.group(0)
            def walk(n):
                if isinstance(n, dict):
                    return {k: (tr.get(v, v) if k in LD_KEYS and isinstance(v, str) else walk(v)) for k, v in n.items()}
                if isinstance(n, list):
                    return [walk(x) if not isinstance(x, str) else tr.get(x, x) for x in n]
                return n
            data = walk(data)
            data = json.loads(json.dumps(data).replace(f'"inLanguage": "{base}"', f'"inLanguage": "{new}"'))
            return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False, indent=2) + "</script>"
        s = re.sub(r'(?s)<script type="application/ld\+json">(.*?)</script>', ld, s)
        # locale wiring
        s = re.sub(r'<html lang="[^"]*"', f'<html lang="{new}"', s, 1)
        s = s.replace(f"https://gameaccountvalue.com/{base}/", f"https://gameaccountvalue.com/{new}/") if base != "en" else s
        s = s.replace(f'"inLanguage": "{base}"', f'"inLanguage": "{new}"').replace(f"utm_content={base}", f"utm_content={new}")
        open(ROOT + f"{new}/{p}.html", "w", encoding="utf-8", newline="").write(s)
    print("built", len(PAGES), "pages for", new)


if __name__ == "__main__":
    {"extract": extract, "build": build}[sys.argv[1]](sys.argv[2], sys.argv[3])
