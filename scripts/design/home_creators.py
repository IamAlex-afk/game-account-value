"""Homepage creators block (owner, 2026-10-06): the most-subscribed verified YouTube creator per game in the page
language (creators.render_home_creators), placed before the 'Everything on the site' hub. Only languages with
verified data for at least 3 games get the block. Idempotent via <!--creators--> markers.
Run after scripts/research/streamers.py: python scripts/design/home_creators.py"""
import os, re
import nav_menu as N
from creators import render_home_creators

n = 0
for lang in N.L:
    p = N.ROOT + ("" if lang == "en" else lang + os.sep) + "index.html"
    if not os.path.exists(p):
        continue
    s = open(p, encoding="utf-8").read()
    t = re.sub(r"<!--creators-->.*?<!--/creators-->\n", "", s, flags=re.S)
    block = render_home_creators(lang)
    if block:
        anchor = '<section class="section g-hub"'
        if anchor in t:
            t = t.replace(anchor, "<!--creators-->" + block + "<!--/creators-->\n" + anchor, 1)
    if t != s:
        open(p, "w", encoding="utf-8", newline="").write(t)
        n += 1
print("homepages updated:", n)
