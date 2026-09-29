"""Acceptance fixes (2026-09-29):
1. dead source links → working primary pages (checked the same day):
   - Wikipedia has no articles on Mohamed Light / Two9 → Liquipedia player pages
     (existence confirmed via the Liquipedia API);
   - zh pages carried outdated Eldorado/igitems catalogue URLs → the working
     URLs every other language already uses;
   - clashos.in guide moved to its .html address.
2. WCAG 2.5.3 "label in name": links/tiles whose aria-label didn't contain the
   visible text (e.g. English "Open GameAccountValue Bot on Telegram" on a
   Russian "Открыть бота" button) now use the visible text as their label.
Run: python scripts/fix_links_labels.py"""
import re, subprocess

LINKS = {
    "https://en.wikipedia.org/wiki/Mohamed_Light": "https://liquipedia.net/clashroyale/Mohamed_Light",
    "https://en.wikipedia.org/wiki/Two9": "https://liquipedia.net/freefire/Two9",
    "https://www.eldorado.gg/fortnite-accounts/a/40-1-0": "https://www.eldorado.gg/fortnite-accounts-for-sale/a/16-1-0",
    "https://www.eldorado.gg/minecraft-accounts/a/45-1-0": "https://www.eldorado.gg/minecraft-accounts/a/61-1-0",
    "https://igitems.com/minecraft-account\"": "https://igitems.com/mc-account\"",
    "https://www.clashos.in/guides/clash-of-clans-upgrade-guide\"": "https://www.clashos.in/guides/clash-of-clans-upgrade-guide.html\"",
}
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿️‍]")
TAG = re.compile(r'<(a|button)\b([^>]*?)\saria-label="([^"]*)"([^>]*)>(.*?)</\1>', re.S)


def fix_label(m):
    tag, pre, label, post, inner = m.groups()
    visible = re.sub(r"\s+", " ", EMOJI.sub("", re.sub(r"<[^>]+>", " ", inner))).strip()
    if not visible or label.lower().find(visible.lower()) >= 0 or 'lang' in (pre + post):
        return m.group(0)            # already fine, icon-only, or the language menu
    return f'<{tag}{pre} aria-label="{visible}"{post}>{inner}</{tag}>'


files = [f for f in subprocess.run(["git", "ls-files", "*.html"], capture_output=True, text=True).stdout.split()
         if not f.startswith("scripts/")]
changed = 0
for f in files:
    s = open(f, encoding="utf-8").read()
    t = s
    for a, b in LINKS.items():
        t = t.replace(a, b)
    t = TAG.sub(fix_label, t)
    if t != s:
        open(f, "w", encoding="utf-8", newline="").write(t)
        changed += 1
print("pages changed:", changed)
