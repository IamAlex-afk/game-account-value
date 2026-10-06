"""Per-language sitemaps for Search Console monitoring: sitemaps/sitemap-<lang>.xml, generated from the
single source sitemap.xml (which stays the main sitemap). Submitting them in Search Console shows how many
URLs of each language are indexed. A URL may appear in both files - Google allows that.
Run after sitemap changes (sitemap_lastmod.py calls it): python scripts/sitemap_split.py"""
import os, re

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SITE = "https://gameaccountvalue.com/"
s = open("sitemap.xml", encoding="utf-8").read()
entries = re.findall(r"  <url>.*?</url>", s, re.S)
by = {}
for e in entries:
    loc = re.search(r"<loc>([^<]+)</loc>", e).group(1)
    path = loc[len(SITE):]
    m = re.match(r"([a-z]{2})/", path)
    by.setdefault(m.group(1) if m else "en", []).append(e)
os.makedirs("sitemaps", exist_ok=True)
for f in os.listdir("sitemaps"):
    if f.startswith("sitemap-") and f.endswith(".xml"):
        os.remove(os.path.join("sitemaps", f))
for lang, es in sorted(by.items()):
    body = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(es) + "\n</urlset>\n"
    open(f"sitemaps/sitemap-{lang}.xml", "w", encoding="utf-8", newline="\n").write(body)
print(len(by), "language sitemaps,", sum(len(v) for v in by.values()), "URLs")
