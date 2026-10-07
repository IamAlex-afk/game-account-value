# -*- coding: utf-8 -*-
"""satellite: black patches of the old backdrop sit on the solar panels and next to the dish.
Patches inside the craft are painted over from the surrounding panel, the one on the outline is cut away.
    python gav_satellite.py <in.webp> <out.webp>"""
import sys
import numpy as np
import cv2
from PIL import Image
from scipy import ndimage as ndi

a = np.array(Image.open(sys.argv[1]).convert("RGBA"))
rgb, al = a[..., :3].copy(), a[..., 3].astype(np.float32) / 255
L = rgb[..., 0] * 0.30 + rgb[..., 1] * 0.59 + rgb[..., 2] * 0.11
solid = al > 0.5
black = solid & (ndi.uniform_filter(L, 3) < 17)
black = black
lab, n = ndi.label(black)
sizes = ndi.sum(np.ones_like(lab), lab, range(1, n + 1))
outside = ndi.binary_dilation(~solid, iterations=2)
paint = np.zeros_like(black); cut = np.zeros_like(black)
for i, s in enumerate(sizes):
    comp = lab == i + 1
    if s < 5:
        continue
    touch = (comp & outside).sum() / s
    (cut if touch > 0.08 else paint)[comp] = True
print("painted over:", int(paint.sum()), "px; cut:", int(cut.sum()), "px")
paint = ndi.binary_dilation(paint, iterations=3)
rgb = cv2.inpaint(rgb, paint.astype(np.uint8) * 255, 4, cv2.INPAINT_TELEA)
al2 = al * (1 - ndi.gaussian_filter(ndi.binary_dilation(cut, iterations=1).astype(np.float32), 0.7))
out = np.dstack([rgb, np.clip(al2 * 255, 0, 255).astype(np.uint8)])
Image.fromarray(out, "RGBA").save(sys.argv[2], "WEBP", quality=90, method=6, alpha_quality=100)
