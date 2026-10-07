# -*- coding: utf-8 -*-
"""Re-render the collector card samples of the site with the bot's own drawer.
    python gav_cards_render.py <bot repo> <out dir> [keys...]"""
import os, sys, time
BOT, OUT = sys.argv[1], sys.argv[2]
os.chdir(BOT); sys.path.insert(0, BOT)
from PIL import Image
from core import drawer
time_strftime = time.strftime
drawer.time.strftime = lambda fmt, *a: "2026-09-30" if fmt == "%Y-%m-%d" else time_strftime(fmt, *a)   # samples keep their date
CARDS = {"wood": ("🪵 WOOD", 2, 5120), "iron": ("⚙️ IRON", 6, 3301), "bronze": ("🥉 BRONZE", 14, 2210), "silver": ("🥈 SILVER", 27, 1802),
         "gold": ("🥇 GOLD", 52, 1407), "platinum": ("🔷 PLATINUM", 88, 1256), "emerald": ("💚 EMERALD", 150, 1105),
         "diamond": ("💎 DIAMOND", 280, 1033), "whale": ("🐋 WHALE", 920, 1012), "genesis": ("💎 DIAMOND", 280, 42), "founder": ("🥇 GOLD", 52, 777)}
LANGS = sys.argv[4].split(",") if len(sys.argv) > 4 else ["en"]
keys = sys.argv[3].split(",")
for lang in LANGS:
    os.makedirs(os.path.join(OUT, lang), exist_ok=True)
    for k in keys:
        badge, total, no = CARDS[k]
        price = {"game_name": "Roblox", "tier_badge": badge, "total": total, "min_price": total * 0.75, "max_price": total * 1.25,
                 "scan_id": f"GAV-SAMPLE-{no:04d}", "cert_number": no, "card_series": 1, "confidence": "HIGH", "is_whale": k == "whale",
                 "breakdown": [("Limiteds", round(total * 0.6)), ("Account age", round(total * 0.2))]}
        ai = {"liquidity": "HIGH", "rare_items": ["Dominus Infernus", "Korblox Deathspeaker"]}
        front, _, _ = drawer._front_image(price, ai, "Player", lang)
        front.convert("RGB").resize((540, 360), Image.LANCZOS).save(os.path.join(OUT, lang, k + ".webp"), "WEBP", quality=82, method=6)
    print("RES", lang, flush=True)
