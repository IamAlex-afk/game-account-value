"""Add the deep-space backdrop (assets/space-background.js) to every page, all 24 languages.
The script itself picks the scene by URL: homepage view, or the game's own view + loot set on
game pages, game news hubs and game news articles. Idempotent; bump V when the script changes.
Run: python scripts/design/space_rollout.py"""
import glob, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + os.sep
V = "20261006a"

n = 0
for f in glob.glob(ROOT + "**/*.html", recursive=True):
    rp = os.path.relpath(f, ROOT).replace(os.sep, "/")
    if rp.startswith(("scripts/", "_", "node_modules/", "google")) or rp == "404.html":
        continue
    s = open(f, encoding="utf-8").read()
    pre = "../" if "/" in rp else "./"
    tag = f'<script src="{pre}assets/space-background.js?v={V}" defer></script>'
    t = re.sub(r'<script src="[^"]*assets/space-background\.js[^"]*" defer></script>\n?', "", s)
    t = t.replace("</body>", tag + "\n</body>", 1)
    if t != s:
        open(f, "w", encoding="utf-8", newline="").write(t)
        n += 1
print("space backdrop on", n, "pages changed")
