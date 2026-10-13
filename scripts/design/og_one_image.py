"""One social image per page (was two og:image tags in a row).
Game pages and the news of a game: that game's og/<game>.jpg (og + twitter).
Every other page: og-image.jpg only. Run from the site repo root; --apply writes."""
import glob, io, re, sys, collections

APPLY = "--apply" in sys.argv
B = "https://gameaccountvalue.com/"
IMG = r'<meta property="og:image" content="%s">'
W = r'\s*<meta property="og:image:width" content="1200">'
H = r'\s*<meta property="og:image:height" content="630">'
ALT = r'(\s*<meta property="og:image:alt" content="[^"]*">)'
FIRST = re.compile((IMG % (re.escape(B) + r'og-image\.jpg\?v=\d+')) + W + H + ALT + r'(\s*)' +
                   '(' + (IMG % (re.escape(B) + r'og/([a-z-]+)\.jpg\?v=\d+')) + ')' + '(' + W + H + ')')
TW = re.compile(r'(<meta name="twitter:image" content=")' + re.escape(B) + r'og-image\.jpg\?v=\d+(">)')

stat = collections.Counter()
for p in sorted(glob.glob("*.html") + glob.glob("*/*.html")):
    s = io.open(p, encoding="utf-8", newline="").read()
    m = FIRST.search(s)
    if not m:
        stat["no pair"] += 1
        continue
    alt, gap, game, wh = m.group(1), m.group(2), m.group(4), m.group(5)
    first_block = s[m.start():m.start(1)]                      # og-image.jpg + width + height
    if game == "default":
        # keep the general cover, drop the second image
        new = first_block + alt
        stat["general"] += 1
    else:
        new = (IMG % (B + "og/" + game + ".jpg?v=4")) + wh + alt
        s2, k = TW.subn(lambda t: t.group(1) + B + "og/" + game + ".jpg?v=4" + t.group(2), s)
        assert k == 1, (p, k)
        s = s2
        m = FIRST.search(s)
        stat["game"] += 1
    s = s[:m.start()] + new + s[m.end():]
    assert len(re.findall(r'<meta property="og:image" content=', s)) == 1, p
    if APPLY:
        io.open(p, "w", encoding="utf-8", newline="").write(s)
print(dict(stat))
