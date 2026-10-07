# -*- coding: utf-8 -*-
"""Declare the page's cover (og:image) as its image in the structured data of pages that did not say so,
so search engines stop picking a decorative picture (the joystick) as the page thumbnail."""
import io, os, re, json
n = 0; bad = []
for root, dirs, files in os.walk("."):
    dirs[:] = [d for d in dirs if d not in (".git", "scripts", "_tmp_check", "node_modules")]
    for f in files:
        if not f.endswith(".html"): continue
        p = os.path.join(root, f)
        s = io.open(p, encoding="utf-8", newline="").read()
        og = re.search(r'property="og:image" content="([^"]+)"', s)
        if not og: continue
        def add(m):
            if re.match(r'\s*"image"', s[m.end():m.end() + 40]): return m.group(0)
            return m.group(0) + m.group(1) + '"image": "' + og.group(1) + '",' + m.group(3)
        s2 = re.sub(r'([ \t]*)"@type": "(Article|SoftwareApplication)",(\r?\n)', add, s)
        if s2 != s:
            for blk in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s2, re.S):
                try: json.loads(blk)
                except Exception as e: bad.append((p, str(e)[:60]))
            io.open(p, "w", encoding="utf-8", newline="").write(s2); n += 1
print("pages updated:", n, "| broken JSON:", bad[:5])
