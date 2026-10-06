"""HTML validity/a11y hygiene (html-validate recommended rules), idempotent, all pages:
- header <nav> gets an accessible name (several landmarks per page must be distinguishable);
- footer links / homepage tiles: plain <div> (no role="navigation" div — html-validate prefers native <nav>,
  but every <nav> here is styled as the header bar; they sit inside <footer> / the hero anyway);
- raw " & " in text (not inside <script>/<style>) -> " &amp; ";
- self-closing void tags in <head> (<meta ... />) -> <meta ...>; trailing whitespace stripped.
Run: python scripts/design/html_hygiene.py"""
import glob, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + os.sep
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nav_menu as N

SPLIT = re.compile(r'(<script\b.*?</script>|<style\b.*?</style>)', re.S | re.I)


def amp(text):
    parts = SPLIT.split(text)
    for i in range(0, len(parts), 2):
        parts[i] = parts[i].replace(" & ", " &amp; ")
    return "".join(parts)


n = 0
for f in glob.glob(ROOT + "**/*.html", recursive=True):
    rp = os.path.relpath(f, ROOT).replace(os.sep, "/")
    if rp.startswith(("scripts/", "_", "node_modules/")):
        continue
    s = open(f, encoding="utf-8").read()
    t = s
    lang = rp.split("/")[0] if "/" in rp else "en"
    if lang in N.L:
        g, gd, news, _, _ = N.L[lang]
        t = t.replace("<nav>\n", f'<nav aria-label="{g} · {gd} · {news}">\n', 1)
    t = t.replace('<div class="foot-nav" role="navigation" aria-label="GameAccountValue">', '<div class="foot-nav">')
    t = re.sub(r'<div class="g-quick" role="navigation" aria-label="[^"]*">', '<div class="g-quick">', t)
    t = amp(t)
    t = re.sub(r"(<meta [^>]*?)\s*/>", r"\1>", t)
    t = re.sub(r"[ \t]+\n", "\n", t)
    if t != s:
        open(f, "w", encoding="utf-8", newline="").write(t)
        n += 1
print("pages cleaned:", n)
