# -*- coding: utf-8 -*-
"""Cut a scene image by contrast against black.

The originals were made to sit on a black page: there they look right, because their faint parts read as the
object's own dark surface. So the picture as seen on black is the source, and the object is whatever is brighter
than the backdrop. Big black areas are backdrop (also when the object surrounds them), small dark spots inside
the object are its shadows. The outline is traced at triple resolution.

    python gav_contrast.py <originals dir> <out dir> name[:thr[:hole[:glow[:out]]]] ...
      thr   brightness (0-255) below which a pixel is backdrop            (default 17)
      hole  enclosed dark areas larger than this share of the picture are cut, smaller are kept   (default 0.004;
            1 = keep every enclosed dark area: screens, visors, black parts of the object)
      glow  brightness below which a pixel counts as glow, not object, when it lies outside the old solid mask (default 0 = off)
      out   pixels darker than this that can be reached from outside the object are backdrop shadow (default 0 = off)"""
import sys, os
import numpy as np
from PIL import Image
from scipy import ndimage as ndi


def cut(src, dst, thr=17.0, hole=0.004, glow=0.0, out=0.0):
    a = np.array(Image.open(src).convert("RGBA")).astype(np.float32)
    a0 = a[..., 3] / 255.0
    baked = a[..., :3] * a0[..., None]
    h, w = a0.shape
    B = np.array(Image.fromarray(baked.round().astype(np.uint8)).resize((w * 3, h * 3), Image.BICUBIC)).astype(np.float32)
    A3 = np.array(Image.fromarray((a0 * 255).astype(np.uint8)).resize((w * 3, h * 3), Image.BICUBIC)).astype(np.float32) / 255
    L = ndi.gaussian_filter(B[..., 0] * 0.30 + B[..., 1] * 0.59 + B[..., 2] * 0.11, 1.5)
    H, W = L.shape
    obj = L > thr
    if glow:
        obj &= ~((A3 < 0.6) & (L < glow))
    if out:                                   # a dark shadow of the old backdrop that touches the outline: darker than `out` and reachable from outside
        lab, n = ndi.label(~obj | (L < out))
        ids = np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))
        obj &= ~np.isin(lab, ids[ids > 0])
    lab, n = ndi.label(~obj)
    ids = np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))
    outside = np.isin(lab, ids[ids > 0])
    sizes = ndi.sum(np.ones_like(lab), lab, range(1, n + 1))
    keep_holes = np.isin(lab, [i + 1 for i, s in enumerate(sizes) if s <= hole * H * W]) & ~outside
    obj = obj | keep_holes
    obj = ndi.binary_opening(obj, iterations=2)
    lab, n = ndi.label(obj)
    if n > 1:
        sizes = ndi.sum(np.ones_like(lab), lab, range(1, n + 1))
        obj = np.isin(lab, [i + 1 for i, s in enumerate(sizes) if s > 0.0015 * H * W])
    al = ndi.gaussian_filter(obj.astype(np.float32), 1.6)
    al = np.clip((al - 0.35) / 0.3, 0, 1)
    alpha = np.array(Image.fromarray((al * 255).astype(np.uint8)).resize((w, h), Image.LANCZOS)).astype(np.float32) / 255
    out = np.dstack([np.clip(baked, 0, 255), alpha * 255]).round().astype(np.uint8)
    out[alpha <= 0] = 0
    Image.fromarray(out, "RGBA").save(dst, "WEBP", quality=90, method=6, alpha_quality=100)


if __name__ == "__main__":
    SRC, OUT = sys.argv[1], sys.argv[2]
    os.makedirs(OUT, exist_ok=True)
    for spec in sys.argv[3:]:
        p = spec.split(":")
        kw = {}
        if len(p) > 1 and p[1]: kw["thr"] = float(p[1])
        if len(p) > 2 and p[2]: kw["hole"] = float(p[2])
        if len(p) > 3 and p[3]: kw["glow"] = float(p[3])
        if len(p) > 4 and p[4]: kw["out"] = float(p[4])
        cut(os.path.join(SRC, p[0] + ".webp"), os.path.join(OUT, p[0] + ".webp"), **kw)
        print("cut", spec)
