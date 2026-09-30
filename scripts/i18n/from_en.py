"""Post-process a locale built from the English root pages.

  python scripts/i18n/segments.py build en <lang>
  python scripts/i18n/from_en.py <lang>

segments.py only rewrites locale URLs when the base is itself a locale
folder. English pages live at the site root, so a locale built from them
still points at root paths and root URLs. This fixes that, matching how the
existing locale folders (e.g. th/) are wired:
- relative asset/page paths → ../ (pages that exist in the locale stay local)
- canonical, og:url and JSON-LD self URLs → /<lang>/
- t.me bot links get utm_content=<lang>
- EN-only bits dropped: news FAB (news pages are English-only), the second
  Search Console verification tag
- language menu marks <lang> as current; index keywords meta from KEYWORDS
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + os.sep
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from segments import PAGES

SITE = "https://gameaccountvalue.com/"
KEYWORDS = {
    "tk": "roblox hasap bahasy, fortnite hasap bahasy, genshin impact hasap bahasy, clash of clans hasap bahasy, oýun hasabyny bahalandyrmak, AI bahalandyryş, ýygyndy bahasy, telegram bot",
    "ky": "roblox аккаунт баасы, fortnite аккаунт баасы, genshin impact аккаунт баасы, clash of clans аккаунт баасы, оюн аккаунтун баалоо, AI баалоо, жыйнактын баасы, telegram бот",
    "kk": "roblox аккаунт бағасы, fortnite аккаунт құны, genshin impact аккаунт бағасы, clash of clans аккаунт құны, ойын аккаунтын бағалау, AI бағалау, жинақ құны, telegram бот",
    "ms": "nilai akaun roblox, harga akaun fortnite, nilai akaun genshin impact, nilai akaun clash of clans, "
          "penilaian akaun permainan, penilaian AI, nilai koleksi, bot telegram",
    "uz": "roblox akkaunt narxi, fortnite akkaunt qiymati, genshin impact akkaunt narxi, clash of clans akkaunt qiymati, "
          "oʻyin akkauntini baholash, AI baholash, kolleksiya qiymati, telegram bot",
}


def fix_rel(m, lang):
    attr, q, url = m.group(1), m.group(2), m.group(3)
    if re.match(r"^(https?:|#|\.\./|/|mailto:|tg:|data:|javascript:)", url):
        return m.group(0)
    path = url[2:] if url.startswith("./") else url
    base = path.split("#")[0].split("?")[0]
    if base in ("",) or base.replace(".html", "") in PAGES:
        return m.group(0)            # page that exists in the locale folder
    return f"{attr}={q}../{path}{q}"


def fix_ld(block, lang):
    def self_url(u):
        if u == SITE or u == SITE.rstrip("/"):
            return SITE + lang + "/"
        m = re.match(re.escape(SITE) + r"([a-z0-9-]+)\.html(#.*)?$", u)
        if m and m.group(1) in PAGES:
            return f"{SITE}{lang}/{m.group(1)}.html{m.group(2) or ''}"
        if u == SITE + "#website":
            return f"{SITE}{lang}/#website"
        return u
    def walk(n, key=None):
        if isinstance(n, dict):
            if n.get("@type") == "Organization" and n.get("@id", "").endswith("#organization"):
                return n                                  # one site-wide organization
            out = {}
            for k, v in n.items():
                if k in ("url", "@id", "item", "mainEntityOfPage") and isinstance(v, str):
                    v = self_url(v)
                    v = re.sub(r"(t\.me/GameAccountValue_Bot/#(?:faq|howto))(-en)?$", r"\1-" + lang, v)
                out[k] = walk(v, k)
            return out
        if isinstance(n, list):
            return [walk(x, key) for x in n]
        return n
    try:
        data = json.loads(block)
    except ValueError:
        return None
    return json.dumps(walk(data), ensure_ascii=False, indent=2)


def process(lang):
    for p in PAGES:
        f = ROOT + f"{lang}/{p}.html"
        s = open(f, encoding="utf-8").read()
        s = re.sub(r'\b(href|src)=(["\'])([^"\']*)\2', lambda m: fix_rel(m, lang), s)
        s = re.sub(r'(<image\b[^>]*\bhref=")(?!https?:|\.\./)(?:\./)?([^"]+")', r"\1../\2", s)
        own = SITE + (f"{p}.html" if p != "index" else "")
        mine = SITE + lang + "/" + (f"{p}.html" if p != "index" else "")
        s = s.replace(f'rel="canonical" href="{own}"', f'rel="canonical" href="{mine}"')
        s = s.replace(f'property="og:url" content="{own}"', f'property="og:url" content="{mine}"')
        def ld(m):
            new = fix_ld(m.group(1), lang)
            return m.group(0) if new is None else '<script type="application/ld+json">' + new + "</script>"
        s = re.sub(r'(?s)<script type="application/ld\+json">(.*?)</script>', ld, s)
        def utm(m):
            u = m.group(1)
            if "utm_content=" in u:
                return m.group(0)
            return 'href="' + u + ("&" if "?" in u else "?") + f'utm_content={lang}"'
        s = re.sub(r'href="(https://t\.me/GameAccountValue_Bot[^"]*)"', utm, s)
        s = re.sub(r'(?s)\s*<a href="[^"]*-news\.html" class="fresh-news-fab".*?</a>', "", s)
        s = re.sub(r'\s*<meta name="google-site-verification" content="DFpki1t_QAVQIUVjut75ixmRHQke0Q7i9VDaP8Y4bxo">', "", s)
        s = s.replace(f'<a href="{SITE}" class="lang-current">', f'<a href="{SITE}">')
        s = s.replace(f'<a href="{SITE}{lang}/">', f'<a href="{SITE}{lang}/" class="lang-current">')
        if lang in KEYWORDS:
            s = re.sub(r'(<meta name="keywords" content=")[^"]*(")', r"\g<1>" + KEYWORDS[lang] + r"\2", s)
        open(f, "w", encoding="utf-8", newline="").write(s)
    print("fixed", len(PAGES), "pages for", lang)


if __name__ == "__main__":
    process(sys.argv[1])
