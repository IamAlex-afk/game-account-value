"""Ping IndexNow (Bing, Yandex, Naver, Seznam, Yep) with every URL in the live sitemap.
Google does not support IndexNow - use Search Console for Google.
Usage: python scripts/indexnow.py URL [URL...]  (changed pages only — preferred)
       python scripts/indexnow.py                (every sitemap URL; only after
                                                  a site-wide change, IndexNow
                                                  asks for changed URLs only)
"""
import json, pathlib, re, sys, urllib.error, urllib.request

HOST = "gameaccountvalue.com"
ROOT = pathlib.Path(__file__).resolve().parent.parent
keys = [p.stem for p in ROOT.glob("*.txt") if re.fullmatch(r"[0-9a-f]{32}", p.stem)]
if not keys:
    sys.exit(f"no IndexNow key file (<32 hex chars>.txt) in {ROOT}")
KEY = keys[0]

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
except urllib.error.URLError as e:
    sys.exit(f"network error: {e.reason}")
