# -*- coding: utf-8 -*-
"""2026-10-08 rollout on every page:
1. Messenger / social preview: the site cover (og-image.jpg, the gamepad with the site name) becomes the first
   og:image and the twitter:image; the page's own share card stays as a second og:image.
2. New versions of style.css, glass.css and nav.js in the pages (scroll reveal moved from CSS to nav.js)."""
import io, os, re
COVER = "https://gameaccountvalue.com/og-image.jpg?v=4"
V = "20261008a"
n = 0
for root, dirs, files in os.walk("."):
    dirs[:] = [d for d in dirs if d not in (".git", "scripts", "_tmp_check", "node_modules")]
    for f in files:
        if not f.endswith(".html"): continue
        p = os.path.join(root, f)
        s = io.open(p, encoding="utf-8", newline="").read(); o = s
        m = re.search(r'<meta property="og:image" content="(https://gameaccountvalue\.com/og/[^"]+)">(\r?\n)', s)
        if m and "og-image.jpg?v=4" not in s:
            card, nl = m.group(1), m.group(2)
            s = s.replace(m.group(0), f'<meta property="og:image" content="{COVER}">{nl}', 1)
            alt = re.search(r'<meta property="og:image:alt" content="[^"]*">(\r?\n)', s)
            extra = f'<meta property="og:image" content="{card}">{nl}<meta property="og:image:width" content="1200">{nl}<meta property="og:image:height" content="630">{nl}'
            if alt:
                s = s.replace(alt.group(0), alt.group(0) + extra, 1)
            else:
                s = s.replace(f'<meta property="og:image" content="{COVER}">{nl}', f'<meta property="og:image" content="{COVER}">{nl}' + extra, 1)
            s = re.sub(r'<meta name="twitter:image" content="https://gameaccountvalue\.com/og/[^"]+">', f'<meta name="twitter:image" content="{COVER}">', s, count=1)
        s = re.sub(r'(assets/style\.css)(\?v=[0-9a-z]+)?"', r'\1?v=' + V + '"', s)
        s = re.sub(r'(assets/glass\.css)\?v=[0-9a-z]+"', r'\1?v=' + V + '"', s)
        s = re.sub(r'(assets/nav\.js)\?v=[0-9a-z]+"', r'\1?v=' + V + '"', s)
        if s != o:
            io.open(p, "w", encoding="utf-8", newline="").write(s); n += 1
print("pages updated:", n)
