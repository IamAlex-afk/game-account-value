"""Ping IndexNow (Bing, Yandex, Naver, Seznam, Yep) with every URL in the live sitemap.
Google does not support IndexNow - use Search Console for Google.
Usage: python scripts/indexnow.py            (all sitemap URLs)
       python scripts/indexnow.py URL [URL...] (only these, e.g. new pages)
"""
import glob, json, re, sys, urllib.request

HOST = "gameaccountvalue.com"
KEY = next(p[:-4] for p in glob.glob("*.txt") if re.fullmatch(r"[0-9a-f]{32}\.txt", p))

urls = sys.argv[1:] or re.findall(
    r"<loc>([^<]+)</loc>",
    urllib.request.urlopen(f"https://{HOST}/sitemap.xml").read().decode())
body = json.dumps({"host": HOST, "key": KEY,
                   "keyLocation": f"https://{HOST}/{KEY}.txt",
                   "urlList": urls}).encode()
req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body,
                             headers={"Content-Type": "application/json; charset=utf-8"})
try:
    with urllib.request.urlopen(req) as r:
        print(len(urls), "URLs ->", r.status)
except urllib.error.HTTPError as e:
    print(len(urls), "URLs ->", e.code, e.read().decode()[:300])
