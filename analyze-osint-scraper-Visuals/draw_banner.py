#!/usr/bin/env python3
"""analyze-osint-scraper wordmark banner: open water over a reef slope at mid depth, green gold shafts from the
surface, a shoal of reef squid holding station mid distance with the nearest carrying a travelling krill pink
wash, farther squid answering with shorter flashes, tube worm crowns and a lost pearl strand below, anglerfish
lure pairs deep behind. One pale sounding board at the right edge carries the name in Averia Serif Libre,
glacier melt cyan letters darkening toward the board's foot. No other readable mark."""
import math, random, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
random.seed(23)
A = sys.argv[1] if len(sys.argv) > 1 else ""
W, H = 1200, 420
CYAN = (120, 220, 230); GREEN = (110, 230, 160); PINK = (240, 110, 150)
img = Image.new("RGB", (W, H), (10, 30, 54)); d = ImageDraw.Draw(img, "RGBA")
for y in range(H):
    t = y / H; d.line([(0, y), (W, y)], fill=(int(28 - 16 * t), int(78 - 44 * t), int(100 - 46 * t)))
for gx, wd in [(120, 80), (430, 110), (760, 84)]:
    d.polygon([(gx, 0), (gx + wd, 0), (gx + wd + 100, H), (gx + 30, H)], fill=(220, 220, 150, 24))
# reef slope and furniture
d.polygon([(0, 356), (420, 322), (820, 344), (1200, 312), (1200, H), (0, H)], fill=(15, 34, 50))
def worm(x, y, s):
    d.line([(x, y), (x, y - 12 * s)], fill=(150, 140, 120), width=3)
    for a in range(-70, 71, 20):
        r = math.radians(a); d.line([(x, y - 12 * s), (x + math.sin(r) * 11 * s, y - 12 * s - math.cos(r) * 8 * s)], fill=(232, 190, 160), width=2)
for (x, y, s) in [(180, 368, 1.0), (214, 372, .8), (520, 356, 1.1), (560, 360, .7), (700, 366, .9)]:
    worm(x, y, s)
# pearl strand caught on a coral spur, hanging from a fixed point
d.polygon([(610, 330), (626, 306), (642, 330)], fill=(90, 60, 70))
for i in range(6):
    x, y = 626 + math.sin(i * .8) * 5, 318 + i * 11
    d.ellipse([x - 5, y - 5, x + 5, y + 5], fill=(232, 228, 214), outline=(180, 176, 160))
# anglerfish lure pairs in the deep background
for (x, y) in [(980, 392), (1105, 400)]:
    d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=(250, 200, 90)); d.ellipse([x + 11, y - 2, x + 16, y + 3], fill=(250, 200, 90))
def squid(cx, cy, ln, mode):
    ht = ln * .30
    d.polygon([(cx + ln * .28, cy), (cx + ln * .52, cy - ht * .85), (cx + ln * .46, cy), (cx + ln * .52, cy + ht * .8)], fill=(28, 74, 104))
    d.polygon([(cx - ln * .5, cy), (cx - ln * .3, cy - ht * .55), (cx + ln * .3, cy - ht * .42), (cx + ln * .5, cy), (cx + ln * .3, cy + ht * .42), (cx - ln * .3, cy + ht * .55)], fill=(24, 66, 98))
    if mode in ("wash", "bands"):
        for i, bx in enumerate([-.28, -.02, .22]):
            c = PINK if mode == "wash" and i == 2 else (CYAN if i != 1 else GREEN)
            x = cx + ln * bx
            d.polygon([(x - ln * .07, cy - ht * .5), (x + ln * .07, cy - ht * .44), (x + ln * .07, cy + ht * .44), (x - ln * .07, cy + ht * .5)], fill=c + (190,))
        if mode == "wash":  # the pink wash travelling from mantle to arm tips
            d.polygon([(cx - ln * .52, cy - ht * .3), (cx - ln * .18, cy - ht * .42), (cx - ln * .18, cy + ht * .42), (cx - ln * .52, cy + ht * .3)], fill=PINK + (110,))
    if mode == "speck":
        for _ in range(18):
            sx, sy = cx + random.uniform(-ln * .4, ln * .35), cy + random.uniform(-ht * .4, ht * .4)
            d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=GREEN + (150,))
    d.ellipse([cx - ln * .58, cy - ht * .42, cx - ln * .36, cy + ht * .42], fill=(24, 66, 98))
    for k in range(5):
        ay = cy - ht * .3 + k * ht * .15
        d.arc([cx - ln * .78, ay - 9, cx - ln * .52, ay + 12], 90, 300, fill=(34, 84, 116), width=3)
    er = max(3, int(ht * .2)); ex, ey = cx - ln * .47, cy
    d.ellipse([ex - er, ey - er, ex + er, ey + er], fill=(8, 14, 20), outline=(210, 230, 235))
# the shoal mid distance, angled the same way; nearest carries the picture
squid(330, 190, 175, "wash")
for (x, y, ln, m) in [(560, 150, 120, "bands"), (730, 205, 110, "speck"), (610, 255, 95, "speck"), (830, 140, 90, "bands"), (470, 285, 85, "dark"), (880, 250, 80, "dark")]:
    squid(x, y, ln, m)
# particles in the shafts
for _ in range(80):
    x, y = random.uniform(0, W), random.uniform(16, 360); r = random.uniform(1, 3)
    d.ellipse([x - r, y - r, x + r, y + r], fill=(235, 240, 200, 60))
# the single sounding board at the right edge, name cut into it, letters darkening toward its foot
bx0, by0, bx1, by1 = 950, 92, 1176, 330
if A == "--v1":  # v1 flaw: board at the centre, competing with the shoal instead of hung at the edge
    bx0, bx1 = 480, 706
d.rounded_rectangle([bx0, by0, bx1, by1], 8, fill=(196, 216, 208), outline=(120, 220, 230), width=3)
d.line([(bx0 + 14, by0 + 18), (bx0 + 14, by1 - 18)], fill=(90, 140, 150), width=3)
for i in range(9):  # depth ticks down the board edge, no numerals
    y = by0 + 30 + i * 26; d.line([(bx0 + 8, y), (bx0 + (22 if i % 3 == 0 else 16), y)], fill=(90, 140, 150), width=2)
try:
    f = ImageFont.truetype(__file__.rsplit("/", 1)[0] + "/fonts/AveriaSerifLibre.ttf", 25)
except Exception:
    f = ImageFont.load_default()
name = "analyze-osint-scraper"
if A == "--v2":
    d.text(((bx0 + bx1) / 2, (by0 + by1) / 2), name, font=f, fill=(16, 70, 86), anchor="mm")  # v2 flaw: one flat line, no darkening, no hung board feel
else:
    words = ["analyze-", "osint-", "scraper"]
    for i, wtxt in enumerate(words):
        t = i / 2; col = (int(46 + 60 * (1 - t) * .4), int(120 - 50 * t), int(140 - 46 * t))
        col = (30, int(128 - 58 * t), int(146 - 52 * t))  # glacier cyan darkening toward the foot
        d.text(((bx0 + bx1) / 2 + 8, by0 + 74 + i * 62), wtxt, font=f, fill=col, anchor="mm")
img = img.filter(ImageFilter.GaussianBlur(0.5))
out = {"--v1": "scratch/banner-v1.png", "--v2": "scratch/banner-v2.png"}.get(A, "banner.png")
img.save(__file__.rsplit("/", 1)[0] + "/" + out); print("saved", out)
