"""Strip the baked-in transparency checkerboard from osha.jpg and save real alpha.

The checkerboard is white (255) / light grey (237). The character has white areas of
its own, but they sit inside a dark outline, so a flood fill from the image border
reaches the checkerboard and nothing else.
"""
from collections import deque
from PIL import Image

SRC = r"C:\Users\Admin\Downloads\osha.jpg"
OUT = r"C:\Users\Admin\Documents\soysoysoy\osha-cut.webp"

im = Image.open(SRC).convert("RGBA")
w, h = im.size
px = im.load()


def neutral_bright(p, lo):
    r, g, b, _ = p
    return max(r, g, b) - min(r, g, b) <= 14 and min(r, g, b) >= lo


# ── flood fill the checkerboard from every border pixel
seen = bytearray(w * h)
q = deque()
for x in range(w):
    for y in (0, h - 1):
        if not seen[y * w + x] and neutral_bright(px[x, y], 224):
            seen[y * w + x] = 1
            q.append((x, y))
for y in range(h):
    for x in (0, w - 1):
        if not seen[y * w + x] and neutral_bright(px[x, y], 224):
            seen[y * w + x] = 1
            q.append((x, y))

while q:
    x, y = q.popleft()
    for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
        if 0 <= nx < w and 0 <= ny < h and not seen[ny * w + nx]:
            if neutral_bright(px[nx, ny], 224):
                seen[ny * w + nx] = 1
                q.append((nx, ny))

# ── eat the JPEG fringe: pixels touching a hole that are still nearly background
for _ in range(3):
    edge = []
    for y in range(h):
        base = y * w
        for x in range(w):
            if seen[base + x]:
                continue
            touching = ((x > 0 and seen[base + x - 1]) or (x < w - 1 and seen[base + x + 1]) or
                        (y > 0 and seen[base - w + x]) or (y < h - 1 and seen[base + w + x]))
            if touching and neutral_bright(px[x, y], 203):
                edge.append((x, y))
    if not edge:
        break
    for x, y in edge:
        seen[y * w + x] = 1

cleared = 0
for y in range(h):
    base = y * w
    for x in range(w):
        if seen[base + x]:
            r, g, b, _ = px[x, y]
            px[x, y] = (r, g, b, 0)
            cleared += 1

im = im.crop(im.getbbox())                       # trim the empty margin
im.thumbnail((460, 460), Image.LANCZOS)          # display size is ~130px; 460 is plenty
im.save(OUT, "WEBP", quality=90, method=6)

print("cleared %d of %d px (%.1f%%)" % (cleared, w * h, 100.0 * cleared / (w * h)))
print("final size", im.size)
