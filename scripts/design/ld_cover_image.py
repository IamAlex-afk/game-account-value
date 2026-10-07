# -*- coding: utf-8 -*-
"""Structured-data image of the game pages and homepages (Article / SoftwareApplication):
the site cover (og-image.jpg: the gamepad with the site name) first, the page's own share card second.
Search engines then have one and the same cover for every page; nothing is removed, og:image is untouched."""
import io, os, re, json
COVER = "https://gameaccountvalue.com/og-image.jpg"
n = 0; bad = []
for root, dirs, files in os.walk("."):
    dirs[:] = [d for d in dirs if d not in (".git", "scripts", "_tmp_check", "node_modules")]
    for f in files:
        if not f.endswith(".html"): continue
        p = os.path.join(root, f)
        s = io.open(p, encoding="utf-8", newline="").read()
        og = re.search(r'property="og:image" content="([^"]+)"', s)
        if not og: continue
        want = '"image": ["' + COVER + '", "' + og.group(1) + '"],'
        def add(m):
            return m.group(1) + '"@type": "' + m.group(2) + '",' + m.group(3) + m.group(1) + want + m.group(3)
        s2 = re.sub(r'([ \t]*)"@type": "(Article|SoftwareApplication)",(\r?\n)(?:[ \t]*"image": [^\n]*\n)?', add, s)
        if s2 != s:
            for blk in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s2, re.S):
                try: json.loads(blk)
                except Exception as e: bad.append((p, str(e)[:60]))
            io.open(p, "w", encoding="utf-8", newline="").write(s2); n += 1
print("pages updated:", n, "| broken JSON:", bad[:5])
