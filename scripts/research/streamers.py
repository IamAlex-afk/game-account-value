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
# per-language search hints: region + words that make the query itself be in that language
HINT = {
    "pt": ("BR", "{g} melhor deck"), "es": ("MX", "{g} mejor mazo"), "ar": ("SA", "{g} {ar}"), "id": ("ID", "{g} terbaik"),
    "tr": ("TR", "{g} en iyi"), "vi": ("VN", "{g} hay nhất"), "hi": ("IN", "{g} हिंदी"), "th": ("TH", "{g} ไทย"),
    "ru": ("RU", "{g} лучшая колода"), "fr": ("FR", "{g} meilleur deck"), "de": ("DE", "{g} bestes deck"), "it": ("IT", "{g} miglior mazzo"),
    "ja": ("JP", "{g} 最強"), "ko": ("KR", "{g} 공략"), "pl": ("PL", "{g} najlepszy"), "zh": ("TW", "{g} 攻略"),
}
AR_NAME = {"roblox": "روبلوكس", "brawl-stars": "براول ستارز", "clash-of-clans": "كلاش اوف كلانس", "clash-royale": "كلاش رويال",
           "free-fire": "فري فاير", "genshin-impact": "جينشن", "mobile-legends": "موبايل ليجند", "fortnite": "فورتنايت", "minecraft": "ماين كرافت"}
# title-based language evidence (used only when YouTube gives no language): script or exclusive common words
import unicodedata
SCRIPT = {"ar": "ARABIC", "hi": "DEVANAGARI", "th": "THAI", "ru": "CYRILLIC", "ja": "HIRAGANA", "ko": "HANGUL", "zh": "CJK"}
WORDS = {
    "pt": {"não", "você", "melhor", "com", "é", "nunca", "meu", "esse", "essa", "jogando", "joguei", "muito", "mais", "pra", "jogo"},
    "es": {"el", "mejor", "mazo", "con", "nunca", "este", "jugando", "muy", "más", "los", "las", "cómo", "juego"},
    "id": {"yang", "dan", "ini", "aku", "main", "terbaik", "banget", "gak", "bisa", "akun", "cara", "dengan"},
    "tr": {"ve", "bir", "bu", "için", "ile", "iyi", "oynadım", "nasıl", "çok", "hesap", "oyun"},
    "vi": {"và", "của", "nhất", "chơi", "cách", "là", "không", "những", "này", "tôi"},
    "fr": {"le", "la", "les", "avec", "et", "est", "meilleur", "jamais", "mon", "pour", "comment"},
    "de": {"der", "die", "das", "und", "mit", "ist", "bestes", "nie", "mein", "wie", "für"},
    "it": {"il", "gli", "con", "è", "miglior", "mai", "mio", "come", "per", "della", "questo"},
    "pl": {"jest", "najlepszy", "nie", "mój", "jak", "dla", "się", "jestem", "gram"},
}


OFFICIAL = ("garena", "supercell", "roblox", "mojang", "minecraft official", "epic games", "fortnite", "hoyoverse",
            "genshin impact", "moonton", "mobile legends: bang bang", "brawl stars", "clash royale", "clash of clans", "free fire")


def about_game(v, kws):
    sn = v["snippet"]
    return any(k in (sn["title"] + " " + " ".join(sn.get("tags", []))).lower() for k in kws)


def _in_title(v, kws):
    return any(k in v["snippet"]["title"].lower() for k in kws)


def on_topic(last, game):
    """>= 6 of the last 10 uploads name the game in title or tags, >= 2 titles name it, and no other tracked game
    is named in more titles (tags are often stuffed with other games, titles are not)."""
    kw = lambda g: GAMES[g][1] + ([AR_NAME[g]] if g in AR_NAME else [])
    if sum(about_game(v, kw(game)) for v in last) < 6:
        return False
    mine = sum(_in_title(v, kw(game)) for v in last)
    return mine >= 2 and all(sum(_in_title(v, kw(g)) for v in last) <= mine for g in GAMES if g != game)


def is_official(name):
    n = name.lower().strip()
    return any(n == o or n.startswith(o + " ") for o in OFFICIAL)


def title_lang(title, lang):
    t = title.lower()
    if lang in SCRIPT:
        names = [unicodedata.name(ch, "") for ch in t if ch.isalpha()]
        hits = sum(SCRIPT[lang] in n for n in names)
        return hits >= 3
    if lang in WORDS:
        toks = set(re.findall(r"[^\W\d_]+", t))
        return len(toks & WORDS[lang]) >= 2      # two distinct marker words, so one shared word is not enough
    return False


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
    kws = kws + [AR_NAME[game]] if game in AR_NAME else kws      # Arabic titles spell the game in Arabic
    since = (datetime.datetime.utcnow() - datetime.timedelta(days=120)).strftime("%Y-%m-%dT00:00:00Z")
    region, tpl = HINT.get(lang, (None, "{g}"))
    q = tpl.format(g=query, ar=AR_NAME.get(game, ""))
    params = dict(part="snippet", type="video", q=q, relevanceLanguage=lang, order="relevance", publishedAfter=since, maxResults=50)
    if region:
        params["regionCode"] = region
    vids = []
    for order in ("relevance", "viewCount"):          # two searches: active creators + biggest recent videos
        params["order"] = order
        vids += [i["id"]["videoId"] for i in yt("search", **params).get("items", []) if i["id"]["videoId"] not in vids]
    if not vids:
        return
    vmeta = []
    for i in range(0, len(vids), 50):
        vmeta += yt("videos", part="snippet", id=",".join(vids[i:i + 50])).get("items", [])
    audio = {}
    for v in vmeta:
        sn = v["snippet"]; l = (sn.get("defaultAudioLanguage") or sn.get("defaultLanguage") or "").split("-")[0].lower()
        audio.setdefault(sn["channelId"], set()).add(l)
    ids = list(audio)
    chans = []
    for i in range(0, len(ids), 50):
        chans += yt("channels", part="snippet,statistics,contentDetails", id=",".join(ids[i:i + 50])).get("items", [])
    rows = store.setdefault(game, {}).setdefault(lang, {}).setdefault("youtube", {})
    for c in chans:
        st, sn = c["statistics"], c["snippet"]
        if st.get("hiddenSubscriberCount"):
            continue
        if is_official(sn["title"]):
            continue
        langs = set(audio.get(c["id"], set())) | {(sn.get("defaultLanguage") or "").split("-")[0].lower()}
        langs.discard("")
        up = c["contentDetails"]["relatedPlaylists"]["uploads"]
        items = yt("playlistItems", part="snippet", playlistId=up, maxResults=10).get("items", [])
        titles = [i["snippet"]["title"] for i in items]
        last = yt("videos", part="snippet", id=",".join(i["snippet"]["resourceId"]["videoId"] for i in items)).get("items", []) if items else []
        # "about the game": the game named in the upload's own title
        about = sum(about_game(v, kws) for v in last)
        if not on_topic(last, game):
            continue
        up_lang = [(v["snippet"].get("defaultAudioLanguage") or "").split("-")[0].lower() for v in last]
        in_lang = sum(title_lang(t, lang) for t in titles)
        own = sum(l == lang for l in up_lang)          # uploads YouTube marks as this language
        other = sum(bool(l) and l != lang for l in up_lang)
        chan_lang = (sn.get("defaultLanguage") or "").split("-")[0].lower()
        # language evidence comes from the uploads themselves (a channel-level language setting alone is not enough:
        # e.g. an English-speaking channel with defaultLanguage=pt): most recent uploads marked in this language by
        # YouTube, or titles written in it with few uploads marked as another language
        if not (own >= 6 or (other <= 2 and in_lang >= 4)):
            continue
        langs = {x for x in (("channel" if chan_lang == lang else ""), (f"{own}/10 uploads" if own else ""), (f"{in_lang}/10 titles" if in_lang else "")) if x}
        rows[c["id"]] = {
            "name": sn["title"], "url": "https://www.youtube.com/channel/" + c["id"],
            "handle": sn.get("customUrl"), "country": sn.get("country"),
            "subscribers": int(st["subscriberCount"]), "videos": int(st.get("videoCount", 0)),
            "about_game_last10": about, "titles_in_language_last10": in_lang, "language_evidence": sorted(l for l in langs if l),
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
    ap.add_argument("--recheck", action="store_true", help="re-apply the topic rules to stored channels")
    ap.add_argument("--refresh", action="store_true",
                    help="re-read statistics of every stored channel (cheap: 1 unit per 50 channels); run at least every 30 days")
    a = ap.parse_args()
    store = json.load(open(OUT, encoding="utf-8")) if os.path.exists(OUT) else {}
    if a.recheck:   # re-apply topic / official / one-game rules to stored YouTube channels (2 units per channel)
        owner = {}
        for g, byl in store.items():
            _, kws, _ = GAMES[g]
            kws = kws + [AR_NAME[g]] if g in AR_NAME else kws
            for L, d in byl.items():
                for cid, r in list(d.get("youtube", {}).items()):
                    if is_official(r["name"]):
                        del d["youtube"][cid]; print("official", g, L, r["name"]); continue
                    ch = yt("channels", part="contentDetails", id=cid).get("items", [])
                    if not ch:
                        del d["youtube"][cid]; continue
                    it = yt("playlistItems", part="snippet", playlistId=ch[0]["contentDetails"]["relatedPlaylists"]["uploads"], maxResults=10).get("items", [])
                    last = yt("videos", part="snippet", id=",".join(i["snippet"]["resourceId"]["videoId"] for i in it)).get("items", []) if it else []
                    n = sum(about_game(v, kws) for v in last)
                    r["about_game_last10"] = n
                    if not on_topic(last, g):
                        del d["youtube"][cid]; print("off-topic", g, L, r["name"], n); continue
                    owner.setdefault((L, cid), []).append((n, g))
        for (L, cid), lst in owner.items():   # a channel is listed under one game only: the one most of its uploads are about
            if len(lst) > 1:
                best = max(lst)[1]
                for n, g in lst:
                    if g != best:
                        print("dup", L, store[g][L]["youtube"][cid]["name"], g, "->", best); del store[g][L]["youtube"][cid]
        json.dump(store, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        raise SystemExit
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
    if not (KEYS.get("twitch_client_id") and KEYS.get("twitch_client_secret")):
        a.youtube_only = True            # Twitch keys are optional; YouTube alone is enough to start
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
