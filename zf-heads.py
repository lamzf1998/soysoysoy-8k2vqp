"""Cut the four ZF photos down to head sprites with real alpha.

The photos are ordinary snapshots — a barracks ceiling, a Seoul side street, an office,
a pink bedroom — so there's no flat background to flood-fill the way osha and psyduck
were done. rembg (u2net_human_seg, running locally on CPU) lifts the person off the
background, then a hand-picked box per photo keeps the head and drops the torso, only the
blob the head lives in is kept, and the result is trimmed to whatever alpha survived,
padded and saved as webp.

The boxes are fractions of the source size, not pixels, so they survive a re-crop of the
originals. Run with the originals still in Downloads:

    python zf-heads.py
"""
import io
import os

import numpy as np
from PIL import Image, ImageFilter
from rembg import new_session, remove
from scipy import ndimage

SRC = r"C:\Users\Admin\Downloads"
OUT = os.path.dirname(os.path.abspath(__file__))

# (source file, output name, head box as l/t/r/b fractions of the full photo, and
# optionally rectangles to rub out first, in those same fractions)
SHOTS = [
    # helmet and chin strap, straight to camera — the default face
    ("zf.jpg",          "zf-cut.webp",      (0.03, 0.16, 0.90, 1.00)),
    # sunglasses on a Seoul street; keep a little of the scarf so the chin has a base
    ("win zf.jpg",      "zf-win-cut.webp",  (0.24, 0.31, 0.75, 0.90)),
    # finger up the nose — the hand is the joke, so the box keeps it
    ("lose zf.jpg",     "zf-lose-cut.webp", (0.00, 0.02, 0.98, 0.88)),
    # grinning with the flower dome; cut off at the jaw, the only line that misses the
    # dome he's holding up. The cushion behind his shoulder reads as person to u2net and
    # touches his hair, so neither the box nor the blob test separates it. The jaw pulls
    # left as it drops, so it takes a staircase of rectangles to clear the headboard and
    # the bedding without shaving the hair or the earring
    ("zf defeated.jpg", "zf-beat-cut.webp", (0.18, 0.04, 0.82, 0.555),
     [(0.795, 0.30, 1, 1), (0.76, 0.40, 1, 1), (0.725, 0.485, 1, 1), (0.70, 0.53, 1, 1)]),
]

MAX = 460          # sprites draw around 110px wide, so this covers 4x screens
PAD = 6            # a little breathing room so the soft edge isn't clipped

session = new_session("u2net_human_seg")

for name, out, box, *rest in SHOTS:
    erase = rest[0] if rest else []
    im = Image.open(os.path.join(SRC, name)).convert("RGB")
    w, h = im.size

    # matting first, on the whole frame: u2net wants to see the body it's cutting out
    cut = remove(im, session=session, alpha_matting=True,
                 alpha_matting_foreground_threshold=240,
                 alpha_matting_background_threshold=12,
                 alpha_matting_erode_size=6)

    for l, t, r, b in erase:
        cut.paste((0, 0, 0, 0), (int(l * w), int(t * h), int(r * w), int(b * h)))

    l, t, r, b = box
    cut = cut.crop((int(l * w), int(t * h), int(r * w), int(b * h)))

    # matting keeps whatever else reads as a person, and the box catches some of it.
    # Whatever the head isn't touching survives as its own island, so keeping only the
    # largest blob drops the lot without needing a rectangle for each
    alpha = np.array(cut.getchannel("A"))
    lab, n = ndimage.label(alpha > 8)
    if n > 1:
        head = 1 + int(np.argmax(ndimage.sum(lab > 0, lab, range(1, n + 1))))
        alpha[lab != head] = 0
        cut.putalpha(Image.fromarray(alpha))

    # the box is deliberately loose; the real edges are wherever alpha ended up
    bbox = cut.getchannel("A").point(lambda a: 255 if a > 8 else 0).getbbox()
    if bbox:
        cut = cut.crop(bbox)

    # feather by a hair: matting leaves a few hard stair-steps along the jaw
    a = cut.getchannel("A").filter(ImageFilter.GaussianBlur(0.6))
    cut.putalpha(a)

    pad = Image.new("RGBA", (cut.width + PAD * 2, cut.height + PAD * 2), (0, 0, 0, 0))
    pad.paste(cut, (PAD, PAD))
    cut = pad

    if max(cut.size) > MAX:
        s = MAX / max(cut.size)
        cut = cut.resize((round(cut.width * s), round(cut.height * s)), Image.LANCZOS)

    path = os.path.join(OUT, out)
    cut.save(path, "WEBP", quality=88, method=6)
    print(f"{out}  {cut.size[0]}x{cut.size[1]}  {os.path.getsize(path) / 1024:.1f} KB")
