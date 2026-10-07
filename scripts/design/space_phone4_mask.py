# -*- coding: utf-8 -*-
"""phone-4 (rotary phone): the picture looks right on black because its body is partly see-through.
Bake that black into the body, then cut out the black backdrop left between the cord and the phone.
    python gav_phone4.py <in.webp> <out.webp>"""
import sys
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

a = np.array(Image.open(sys.argv[1]).convert("RGBA")).astype(np.float32)
rgb, a0 = a[..., :3], a[..., 3] / 255.0
sil = ndi.binary_fill_holes(ndi.binary_closing(a0 > 0.10, iterations=3))
sil = ndi.binary_opening(sil, iterations=2)
# the faint smudge around the outline is not the phone: keep faint pixels only where they are enclosed by solid ones
solid = a0 > 0.5
r = 22
near = ndi.binary_erosion(ndi.binary_dilation(np.pad(solid, r), iterations=r), iterations=r)[r:-r, r:-r]
top = np.zeros_like(sil); top[: int(a0.shape[0] * 0.42)] = True      # the smudge sits above the handset; the faint front of the body below is the phone
sil &= near | solid | ~top
baked = rgb * a0[..., None]                                   # what the eye sees on a black page
lum = baked[..., 0] * 0.30 + baked[..., 1] * 0.59 + baked[..., 2] * 0.11
dark = sil & (ndi.uniform_filter(lum, 3) < 12) & (a0 > 0.6)
dark = ndi.binary_opening(dark, iterations=1)
lab, n = ndi.label(dark)
sizes = ndi.sum(np.ones_like(lab), lab, range(1, n + 1))
h, w = lum.shape
cut = np.isin(lab, [i + 1 for i, s in enumerate(sizes) if s > 0.004 * h * w])
print("black areas removed:", [int(s) for s in sizes if s > 0.004 * h * w])
alpha = ndi.gaussian_filter((sil & ~ndi.binary_dilation(cut, iterations=1)).astype(np.float32), 0.9)
alpha = np.clip(alpha * 1.5 - 0.25, 0, 1)
out = np.dstack([np.clip(baked, 0, 255), alpha * 255]).round().astype(np.uint8)
out[alpha <= 0] = 0
Image.fromarray(out, "RGBA").save(sys.argv[2], "WEBP", quality=90, method=6, alpha_quality=95)
