"""Creators per game and language, from the OFFICIAL YouTube Data API v3 and Twitch Helix API only
(no page scraping). Keys live outside the repo in %USERPROFILE%\\.gav-keys.json:
  {"youtube_api_key": "...", "twitch_client_id": "...", "twitch_client_secret": "..."}
Output: scripts/research/streamers.json (merged across runs; every number has its source + date).

Selection rules (written on the page too):
- YouTube: channels found through videos about the game published in the last 120 days, with
  relevanceLanguage = the page language. A channel is kept only if (a) at least 6 of its last 10
  uploads mention the game in the title, and (b) the language is evidenced: video defaultAudioLanguage
  or channel defaultLanguage equals the page language. Ranked by subscriberCount (YouTube's own,
  rounded public figure). Hidden subscriber counts are skipped.
- Twitch: channels seen live in the game's category with stream language = page language
  (snapshots accumulate across runs), ranked by follower total from /helix/channels/followers.
Quota: YouTube search costs 100 units, so discovery runs a few languages per day:
  python scripts/research/streamers.py --langs ru,en --games clash-royale
  python scripts/research/streamers.py --twitch-only            (cheap, run often)
"""
import argparse, datetime, json, os, re, time, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "streamers.json")
KEYS = json.load(open(os.path.join(os.path.expanduser("~"), ".gav-keys.json"), encoding="utf-8"))
TODAY = datetime.date.today().isoformat()

GAMES = {  # page slug: (YouTube search query, title keywords, Twitch category name)
    "roblox": ("Roblox", ["roblox"], "Roblox"),
    "brawl-stars": ("Brawl Stars", ["brawl stars", "brawlstars", "бравл", "brawl"], "Brawl Stars"),
    "clash-of-clans": ("Clash of Clans", ["clash of clans", "clashofclans", "coc", "клеш оф кленс", "клэш оф клэнс"], "Clash of Clans"),
    "clash-royale": ("Clash Royale", ["clash royale", "clashroyale", "клеш рояль", "клэш рояль"], "Clash Royale"),
    "free-fire": ("Free Fire", ["free fire", "freefire", "ff "], "Garena Free Fire"),
    "genshin-impact": ("Genshin Impact", ["genshin", "геншин", "原神"], "Genshin Impact"),
    "mobile-legends": ("Mobile Legends", ["mobile legends", "mlbb", "ml "], "Mobile Legends: Bang Bang"),
    "fortnite": ("Fortnite", ["fortnite", "фортнайт"], "Fortnite"),
    "minecraft": ("Minecraft", ["minecraft", "майнкрафт", "マイクラ", "마인크래프트"], "Minecraft"),
}
# order = priority: fewer competing pages first (owner, 2026-10-06), English last
LANGS = ["pt", "ar", "es", "id", "tr", "vi", "hi", "th", "ru", "fr", "de", "it", "ja", "ko", "pl", "zh", "tl", "sw", "ms", "uz", "kk", "tk", "ky", "en"]


def get(url, headers=None):
    for a in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=headers or {}), timeout=30) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 503) and a < 2:
                time.sleep(3 * (a + 1)); continue
            raise


def yt(path, **q):
    q["key"] = KEYS["youtube_api_key"]
    return get("https://www.googleapis.com/youtube/v3/" + path + "?" + urllib.parse.urlencode(q))


def youtube(game, lang, store):
    query, kws, _ = GAMES[game]
    since = (datetime.datetime.utcnow() - datetime.timedelta(days=120)).strftime("%Y-%m-%dT00:00:00Z")
    found = yt("search", part="snippet", type="video", q=query, relevanceLanguage=lang, order="viewCount",
               publishedAfter=since, maxResults=50)
    vids = [i["id"]["videoId"] for i in found.get("items", [])]
    if not vids:
        return
    vmeta = yt("videos", part="snippet", id=",".join(vids)).get("items", [])
    audio = {}
    for v in vmeta:
        sn = v["snippet"]; l = (sn.get("defaultAudioLanguage") or sn.get("defaultLanguage") or "").split("-")[0].lower()
        audio.setdefault(sn["channelId"], set()).add(l)
    ids = list(audio)[:50]
    chans = yt("channels", part="snippet,statistics,contentDetails", id=",".join(ids)).get("items", [])
    rows = store.setdefault(game, {}).setdefault(lang, {}).setdefault("youtube", {})
    for c in chans:
        st, sn = c["statistics"], c["snippet"]
        if st.get("hiddenSubscriberCount"):
            continue
        langs = set(audio.get(c["id"], set())) | {(sn.get("defaultLanguage") or "").split("-")[0].lower()}
        if lang not in langs:
            continue
        up = c["contentDetails"]["relatedPlaylists"]["uploads"]
        items = yt("playlistItems", part="snippet", playlistId=up, maxResults=10).get("items", [])
        titles = [i["snippet"]["title"].lower() for i in items]
        about = sum(any(k in t for k in kws) for t in titles)
        if about < 6:
            continue
        rows[c["id"]] = {
            "name": sn["title"], "url": "https://www.youtube.com/channel/" + c["id"],
            "handle": sn.get("customUrl"), "country": sn.get("country"),
            "subscribers": int(st["subscriberCount"]), "videos": int(st.get("videoCount", 0)),
            "about_game_last10": about, "language_evidence": sorted(l for l in langs if l),
            "source": "YouTube Data API v3 (channels.list statistics)", "checked": TODAY,
        }


_tw = {}
def tw(path, **q):
    if "token" not in _tw:
        t = urllib.request.urlopen(urllib.request.Request("https://id.twitch.tv/oauth2/token?" + urllib.parse.urlencode(
            {"client_id": KEYS["twitch_client_id"], "client_secret": KEYS["twitch_client_secret"], "grant_type": "client_credentials"}),
            method="POST"), timeout=30)
        _tw["token"] = json.load(t)["access_token"]
    return get("https://api.twitch.tv/helix/" + path + "?" + urllib.parse.urlencode(q, doseq=True),
               {"Client-Id": KEYS["twitch_client_id"], "Authorization": "Bearer " + _tw["token"]})


def twitch(game, langs, store):
    cat = tw("games", name=GAMES[game][2]).get("data", [])
    if not cat:
        return
    gid = cat[0]["id"]
    for lang in langs:
        live = tw("streams", game_id=gid, language=lang, first=100).get("data", [])
        rows = store.setdefault(game, {}).setdefault(lang, {}).setdefault("twitch", {})
        for s in live:
            uid = s["user_id"]
            f = tw("channels/followers", broadcaster_id=uid).get("total")
            r = rows.setdefault(uid, {"name": s["user_name"], "url": "https://www.twitch.tv/" + s["user_login"], "seen_live": []})
            r.update(followers=f, source="Twitch Helix API (channels/followers total)", checked=TODAY)
            if TODAY not in r["seen_live"]:
                r["seen_live"].append(TODAY)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--games", default=",".join(GAMES))
    ap.add_argument("--langs", default=",".join(LANGS))
    ap.add_argument("--twitch-only", action="store_true")
    ap.add_argument("--youtube-only", action="store_true")
    ap.add_argument("--refresh", action="store_true",
                    help="re-read statistics of every stored channel (cheap: 1 unit per 50 channels); run at least every 30 days")
    a = ap.parse_args()
    store = json.load(open(OUT, encoding="utf-8")) if os.path.exists(OUT) else {}
    if a.refresh:   # YouTube policy: stored statistics must be refreshed (or deleted) within 30 days
        ids = [cid for g in store.values() for l in g.values() for cid in l.get("youtube", {})]
        for i in range(0, len(ids), 50):
            for c in yt("channels", part="statistics", id=",".join(ids[i:i + 50])).get("items", []):
                for g in store.values():
                    for l in g.values():
                        r = l.get("youtube", {}).get(c["id"])
                        if r and not c["statistics"].get("hiddenSubscriberCount"):
                            r.update(subscribers=int(c["statistics"]["subscriberCount"]), checked=TODAY)
        json.dump(store, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("refreshed", len(ids), "channels"); raise SystemExit
    games, langs = a.games.split(","), a.langs.split(",")
    for g in games:
        if not a.youtube_only:
            twitch(g, langs, store)
        if not a.twitch_only:
            for l in langs:
                try:
                    youtube(g, l, store)
                except urllib.error.HTTPError as e:
                    if e.code == 403:
                        print("YouTube quota reached — continue tomorrow"); a.twitch_only = True; break
                    raise
        json.dump(store, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(g, {l: (len(store.get(g, {}).get(l, {}).get("youtube", {})), len(store.get(g, {}).get(l, {}).get("twitch", {}))) for l in langs})
