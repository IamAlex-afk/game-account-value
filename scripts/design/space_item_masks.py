# -*- coding: utf-8 -*-
"""Rebuild the alpha masks of the floating GAV images (assets/space/item-*, phone-*, g-*).
The colour data under the old masks is intact, so the mask is rebuilt from it:
  - parts of the object the old mask cut out are restored,
  - black leftovers of the old background are removed,
  - the dark smudge around objects becomes a clean edge (real glow stays as light),
  - glow no longer ends in a straight line at the picture border.
    python gav_fix.py <src dir> <out dir>"""
import sys, glob, os
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

SRC, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)

# T: pixels darker than this, connected to the outside, are background. Lower for objects that are dark themselves.
DARK = {"robot": 26, "astronaut": 22,
        "phone-4": 21, "phone-5": 14, "phone-6": 14, "g-fortnite-5": 14, "g-free-fire-2": 16, "g-minecraft-4": 16, "item-lootcrate": 18,
        "item-headset": 15, "item-backpack": 18, "g-free-fire-5": 18, "g-fortnite-2": 18, "g-clash-of-clans-2": 20, "item-gamepad": 20,
        "g-mobile-legends-5": 20, "phone-1": 20, "g-mobile-legends-2": 26, "phone-2": 20, "item-helmet": 22, "g-free-fire-1": 20, "item-airdrop": 20}
TOP = {"robot": (90, 70), "astronaut": (112, 26)}
ENCLOSED = {"item-headset", "phone-4"}
HULL_A = {"phone-4": 0.10}          # outline taken from the faint parts too: the old mask had made the front of the body see-through
ROUGH = {"item-helmet": 30, "g-free-fire-5": 30}   # restore only smooth areas here: the rest under the old mask is noise          # also remove big black areas fully surrounded by the object
RESTORE = {"item-backpack", "g-minecraft-4", "phone-4", "g-mobile-legends-5"}
NO_GLOW = {"item-helmet", "g-free-fire-2", "g-free-fire-5", "item-backpack"}   # faint leftovers of the old cut are not light: drop them
BRIGHT = {"item-trophy": 62, "item-coins": 62, "item-crystal": 50, "item-potion": 50, "item-sword": 46, "g-clash-royale-2": 62, "g-clash-royale-3": 66, "g-brawl-stars-4": 52,
          "g-brawl-stars-1": 50, "g-brawl-stars-2": 62, "g-brawl-stars-5": 50, "g-brawl-stars-6": 62, "g-free-fire-6": 62, "g-genshin-impact-1": 62,
          "g-genshin-impact-5": 50, "g-minecraft-3": 62, "g-mobile-legends-3": 55, "g-mobile-legends-4": 40, "g-roblox-1": 62, "g-roblox-2": 62,
          "g-roblox-3": 55, "g-clash-of-clans-3": 50, "g-clash-of-clans-4": 55, "g-genshin-impact-6": 40}


def smooth(x, a, b):
    t = np.clip((x - a) / float(b - a), 0, 1)
    return t * t * (3 - 2 * t)


def fix(path):
    name = os.path.basename(path)[:-5]
    a = np.array(Image.open(path).convert("RGBA")).astype(np.float32)
    rgb, a0 = a[..., :3], a[..., 3] / 255.0
    lum = rgb[..., 0] * 0.30 + rgb[..., 1] * 0.59 + rgb[..., 2] * 0.11
    rough = np.sqrt(np.maximum(ndi.uniform_filter(lum ** 2, 5) - ndi.uniform_filter(lum, 5) ** 2, 0))
    h, w = lum.shape
    T = DARK.get(name, BRIGHT.get(name, 34))

    core = a0 > 0.55
    # 1. restore object parts the old mask cut out: non-black pixels inside the object's own outline
    if name in RESTORE:
        r = max(6, int(0.11 * max(h, w)))
        pad = np.pad(a0 > HULL_A.get(name, 0.55), r)
        hull = ndi.binary_erosion(ndi.binary_dilation(pad, iterations=r), iterations=r)[r:-r, r:-r]
        cand = hull & ~core & (lum > max(T, 24)) & (rough < ROUGH.get(name, 999))
        cand = ndi.binary_opening(cand, iterations=2)
        lab, n = ndi.label(cand | core)
        keep = np.unique(lab[core])
        core = np.isin(lab, keep[keep > 0])
        core = ndi.binary_closing(core, iterations=1) & ((lum > max(T, 24)) | (a0 > 0.55))

    # 2. black leftovers: dark pixels connected to the outside (or big enclosed ones where asked)
    dark = lum < T
    if name in TOP:                                            # a leftover block of the old backdrop above the head
        t2, rows = TOP[name]
        dark[:rows] |= lum[:rows] < t2
    outside = ~core
    lab, n = ndi.label(dark | outside)
    ids = np.unique(lab[outside])
    bg = np.isin(lab, ids[ids > 0])
    if name in ENCLOSED:
        lab2, n2 = ndi.label(dark & core & ~bg)
        sizes = ndi.sum(np.ones_like(lab2), lab2, range(1, n2 + 1))
        big = [int(np.argmax(sizes)) + 1] if n2 else []
        bg |= np.isin(lab2, big)
    solid = core & ~bg
    solid = ndi.binary_opening(solid, iterations=1) | (solid & ndi.binary_dilation(ndi.binary_opening(solid, iterations=2), iterations=2))
    lab, n = ndi.label(solid)                                  # drop specks far from the object
    if n > 1:
        sizes = ndi.sum(np.ones_like(lab), lab, range(1, n + 1))
        solid = np.isin(lab, [i + 1 for i, s in enumerate(sizes) if s > 0.004 * h * w])

    # 3. edge: solid object opaque; around it only real light survives, as light
    glow = a0 * smooth(rgb.max(axis=2), 70, 170) * 0.8
    dist = ndi.distance_transform_edt(~solid)
    if name in NO_GLOW:
        glow *= 0
    glow *= np.clip(1 - dist / (0.16 * max(h, w)), 0, 1)       # glow fades out with distance from the object
    yy, xx = np.mgrid[0:h, 0:w]
    border = np.minimum.reduce([yy, xx, h - 1 - yy, w - 1 - xx]).astype(np.float32)
    glow *= smooth(border, 0, 0.07 * max(h, w))                # and never ends in a straight line at the border
    alpha = np.where(solid, 1.0, glow)
    soft = ndi.gaussian_filter(solid.astype(np.float32), 0.8)  # anti-aliased outline
    alpha = np.where(solid, np.maximum(soft * 1.6 - 0.3, 0.55), np.maximum(glow, np.clip(soft * 1.6 - 0.3, 0, 1) * (lum > T)))
    alpha = np.clip(alpha, 0, 1)
    inner = ndi.binary_erosion(solid, iterations=1)
    alpha[inner] = 1.0

    out_rgb = rgb.copy()
    g = (~solid) & (alpha > 0)                                  # light pixels keep their colour at full brightness
    k = np.clip(rgb.max(axis=2)[g] / 255.0, 0.45, 1)[:, None]
    out_rgb[g] = np.clip(out_rgb[g] / k, 0, 255)
    out_rgb[alpha <= 0] = 0
    res = np.dstack([out_rgb, alpha * 255]).round().astype(np.uint8)
    Image.fromarray(res, "RGBA").save(os.path.join(OUT, name + ".webp"), "WEBP", quality=88, method=6, alpha_quality=95)
    return name, int((a0 > 0.55).sum()), int(solid.sum())


files = sorted(glob.glob(SRC + "/item-*.webp") + glob.glob(SRC + "/phone-*.webp") + glob.glob(SRC + "/g-*.webp"))
BIG = ["robot", "astronaut"]               # the two figures had a dark block of the old backdrop above the head
files += [os.path.join(SRC, n + ".webp") for n in BIG]
only = sys.argv[3:]
# these five look right on the dark sky as they are (their soft parts are the object itself); rebuilding made them worse
SKIP = {"item-helmet", "item-backpack", "g-free-fire-2", "g-free-fire-5", "g-minecraft-4"}
files = [f for f in files if os.path.basename(f)[:-5] not in SKIP]
for f in files:
    if only and os.path.basename(f)[:-5] not in only:
        continue
    n, before, after = fix(f)
    print(f"{n:26s} object px {before:6d} -> {after:6d}  ({(after - before) * 100 // max(1, before):+d}%)")
