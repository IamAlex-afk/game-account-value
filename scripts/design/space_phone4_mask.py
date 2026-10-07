# -*- coding: utf-8 -*-
"""phone-4 (rotary phone): cut by contrast.
On a black page the picture is clean (its see-through parts read as black bakelite), so that view is taken
as the source and the phone is separated from the black by brightness: what is brighter than the backdrop is
the phone, big black areas (between the cord and the body) are backdrop, small dark spots inside are shadows.
    python gav_phone4.py <in.webp> <out.webp>"""
import sys
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

a = np.array(Image.open(sys.argv[1]).convert("RGBA")).astype(np.float32)
a0 = a[..., 3] / 255.0
baked = a[..., :3] * a0[..., None]                              # the picture as seen on black
h, w = a0.shape
big = Image.fromarray(baked.round().astype(np.uint8)).resize((w * 3, h * 3), Image.BICUBIC)   # work at 3x for a smooth outline
B = np.array(big).astype(np.float32)
L = ndi.gaussian_filter(B[..., 0] * 0.30 + B[..., 1] * 0.59 + B[..., 2] * 0.11, 1.5)
H, W = L.shape
# warm glow above the handset is light, not the phone: faint pixels of the old mask in the top strip
A3 = np.array(Image.fromarray((a0 * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC)).astype(np.float32) / 255
top = (A3 < 0.6) & (np.arange(H)[:, None] < int(H * 0.20))

obj = L > 17
weak = ~obj | top
lab, n = ndi.label(weak)
edge_ids = np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))
outside = np.isin(lab, edge_ids[edge_ids > 0])
obj = ~outside
# enclosed dark areas: small ones are shadows of the phone (keep), big ones are backdrop (cut)
lab, n = ndi.label(~obj | (L < 9))
sizes = ndi.sum(np.ones_like(lab), lab, range(1, n + 1))
for i, s in enumerate(sizes):
    comp = lab == i + 1
    if s > 0.004 * H * W or (comp & outside).any():
        obj &= ~comp
    else:
        obj |= comp
# two patches of dark backdrop glow that touch the phone and are too close to it in brightness for the rule above;
# boxes in source pixels (x0, y0, x1, y1) with the brightness below which a pixel there is backdrop
for (x0, y0, x1, y1), limit in (((62, 8, 124, 31), 44), ((70, 70, 95, 122), 30)):
    box = np.zeros((H, W), bool); box[y0 * 3:y1 * 3, x0 * 3:x1 * 3] = True
    obj &= ~(box & (L < limit))
obj = ndi.binary_opening(obj, iterations=2)
lab, n = ndi.label(obj)
sizes = ndi.sum(np.ones_like(lab), lab, range(1, n + 1))
obj = np.isin(lab, [i + 1 for i, s in enumerate(sizes) if s > 0.002 * H * W])
alpha3 = ndi.gaussian_filter(obj.astype(np.float32), 1.6)
alpha3 = np.clip((alpha3 - 0.35) / 0.3, 0, 1)
alpha = np.array(Image.fromarray((alpha3 * 255).astype(np.uint8)).resize((w, h), Image.LANCZOS)).astype(np.float32) / 255
out = np.dstack([np.clip(baked, 0, 255), alpha * 255]).round().astype(np.uint8)
out[alpha <= 0] = 0
Image.fromarray(out, "RGBA").save(sys.argv[2], "WEBP", quality=92, method=6, alpha_quality=100)
print("kept", int(obj.sum() / 9), "px")
