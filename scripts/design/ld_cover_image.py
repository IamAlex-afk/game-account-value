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

# news pages: NewsArticle already lists its share card; the cover goes in front of it
m2 = 0
for root, dirs, files in os.walk("."):
    dirs[:] = [d for d in dirs if d not in (".git", "scripts", "_tmp_check", "node_modules")]
    for f in files:
        if not f.endswith(".html"): continue
        p = os.path.join(root, f)
        s = io.open(p, encoding="utf-8", newline="").read()
        if '"@type": "NewsArticle"' not in s or COVER in s: continue
        s2 = re.sub(r'"image": \["(https://gameaccountvalue\.com/og/[^"]+)"\]', lambda m: '"image": ["' + COVER + '", "' + m.group(1) + '"]', s, count=1)
        if s2 != s:
            for blk in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s2, re.S):
                json.loads(blk)
            io.open(p, "w", encoding="utf-8", newline="").write(s2); m2 += 1
print("news pages updated:", m2)

# every other page: service pages, news lists, pages whose structured data is written on one line
TYPES = ("Article", "NewsArticle", "CollectionPage", "WebPage", "AboutPage", "SoftwareApplication")
m3 = 0; skipped = []
for root, dirs, files in os.walk("."):
    dirs[:] = [d for d in dirs if d not in (".git", "scripts", "_tmp_check", "node_modules")]
    for f in files:
        if not f.endswith(".html"): continue
        p = os.path.join(root, f)
        s = io.open(p, encoding="utf-8", newline="").read()
        og = re.search(r'property="og:image" content="([^"]+)"', s)
        if COVER in s or not og: continue
        done = False
        for blk in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
            if done: break
            if "\n" in blk.strip():                       # pretty-printed block: add a line after the type
                def add(m):
                    return m.group(0) + m.group(1) + '"image": ["' + COVER + '", "' + og.group(1) + '"],' + m.group(3)
                nb = re.sub(r'([ \t]*)"@type": "(' + "|".join(TYPES) + r')",(\r?\n)(?![ \t]*"image")', add, blk, count=1)
            else:                                          # one-line block: edit the data, write it back the same way
                data = json.loads(blk)
                if json.dumps(data, ensure_ascii=False) != blk.strip(): continue
                items = data.get("@graph") if isinstance(data, dict) and "@graph" in data else [data]
                hit = [it for it in items if isinstance(it, dict) and it.get("@type") in TYPES]
                if not hit: continue
                it = hit[0]; cur = it.get("image") or [og.group(1)]
                cur = [cur] if isinstance(cur, str) else list(cur)
                new = {}
                for k, v in it.items():
                    if k == "image": continue
                    new[k] = v
                    if k == "@type": new["image"] = [COVER] + cur
                it.clear(); it.update(new)
                nb = blk.replace(blk.strip(), json.dumps(data, ensure_ascii=False))
            if nb != blk:
                json.loads(nb); s = s.replace(blk, nb, 1); done = True
        if done:
            io.open(p, "w", encoding="utf-8", newline="").write(s); m3 += 1
        else:
            skipped.append(p)
print("other pages updated:", m3, "| without a suitable block:", len(skipped), skipped[:6])
