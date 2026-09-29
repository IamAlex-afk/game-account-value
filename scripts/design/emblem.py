"""The GAV emblem cut out of favicon.png (512x512: emblem + "GAV" wordmark).
Measured bounds of the emblem artwork: x 119-392, y 104-373; the wordmark
starts at y 376. Crop is centred on those bounds, rows from the wordmark are
blanked, then an even margin is added, so the emblem is optically centred.
python scripts/design/emblem.py  -> rebuilds assets/emblem.webp, favicon.ico, favicon-192.png"""
import os
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CX, CY, ART = 256, 240.5, 278   # centre and size of the measured artwork
TEXT_Y = 375                     # first source row of the wordmark
MARGIN = 0.07                    # even margin on every side


def emblem(size):
    src = Image.open(os.path.join(ROOT, 'favicon.png')).convert('RGB')
    side = round(ART * (1 + 2 * MARGIN))
    x0, y0 = round(CX - side / 2), round(CY - side / 2)
    c = src.crop((x0, y0, x0 + side, y0 + side))
    # replace the wordmark rows with background rows from the top of the crop,
    # so the margin keeps the source's own dark texture (no visible seam)
    cut = TEXT_Y - y0
    filler = c.crop((0, 0, side, side - cut)).transpose(Image.FLIP_TOP_BOTTOM)
    c.paste(filler, (0, cut))
    return c.resize((size, size), Image.LANCZOS)


if __name__ == '__main__':
    emblem(128).save(os.path.join(ROOT, 'assets', 'emblem.webp'), quality=85, method=6)
    emblem(192).quantize(256).save(os.path.join(ROOT, 'favicon-192.png'), optimize=True)
    emblem(192).save(os.path.join(ROOT, 'favicon.ico'), sizes=[(16, 16), (32, 32), (48, 48)])
    print('emblem assets rebuilt')
