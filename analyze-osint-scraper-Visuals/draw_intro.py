#!/usr/bin/env python3
"""analyze-osint-scraper intro: reef squid shoal signalling in graded water over a reef slope, no readable mark.
Close squid head lower left with a huge eye and cyan bands stopping at the mantle edge, shoal at varied flash
phases midground, tube worm crowns on dark rock, anglerfish lure pairs deep below, particles in light shafts."""
import math, random, sys
from PIL import Image, ImageDraw, ImageFilter
random.seed(41)
A = sys.argv[1] if len(sys.argv) > 1 else ""
W, H = 1200, 520
CYAN = (120, 220, 230); GREEN = (110, 230, 160); PINK = (240, 110, 150); DARK = (10, 30, 54)
img = Image.new("RGB", (W, H), DARK); d = ImageDraw.Draw(img, "RGBA")
# graded water: glowing top thinning to blue hush at the bottom
for y in range(H):
    t = y / H
    d.line([(0, y), (W, y)], fill=(int(26 - 14 * t), int(74 - 40 * t), int(96 - 42 * t)))
# green gold shafts from far above
for gx, wd in [(180, 90), (470, 130), (820, 100), (1060, 70)]:
    d.polygon([(gx, 0), (gx + wd, 0), (gx + wd + 130, H), (gx + 40, H)], fill=(220, 220, 150, 26))
# reef slope: dark rock rising from lower right
d.polygon([(0, 470), (420, 420), (760, 448), (1200, 392), (1200, H), (0, H)], fill=(16, 36, 52))
d.polygon([(0, 486), (520, 438), (1200, 420), (1200, H), (0, H)], fill=(12, 28, 44))
# tube worm clusters: anchored tubes, crowns fanned open, still
def worm(x, y, s):
    d.line([(x, y), (x, y - 14 * s)], fill=(150, 140, 120), width=max(2, int(3 * s)))
    for a in range(-70, 71, 20):
        r = math.radians(a); ex, ey = x + math.sin(r) * 13 * s, y - 14 * s - math.cos(r) * 9 * s
        d.line([(x, y - 14 * s), (ex, ey)], fill=(232, 190, 160), width=max(1, int(2 * s)))
for (x, y, s) in [(520, 462, 1.0), (556, 468, .8), (700, 470, 1.1), (742, 476, .7), (950, 452, 1.0), (990, 458, .8), (300, 484, .9)]:
    worm(x, y, s)
# anglerfish lure pairs deep below the slope fall
for (x, y) in [(880, 500), (1040, 508)]:
    d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=(250, 200, 90)); d.ellipse([x + 12, y - 2, x + 17, y + 3], fill=(250, 200, 90))
# one squid, drawn in this program only: horizontal mantle, tail fins, short arms, one big eye, band pattern
def squid(cx, cy, ln, phase, bright=1.0, eye=True):
    ht = ln * 0.30
    # fins flaring at the tail (right end)
    d.polygon([(cx + ln * .28, cy), (cx + ln * .52, cy - ht * .85), (cx + ln * .46, cy + ht * .2), (cx + ln * .52, cy + ht * .8)], fill=(28, 74, 104))
    # mantle: long torpedo body
    d.polygon([(cx - ln * .5, cy), (cx - ln * .30, cy - ht * .55), (cx + ln * .30, cy - ht * .42), (cx + ln * .5, cy), (cx + ln * .30, cy + ht * .42), (cx - ln * .30, cy + ht * .55)], fill=(24, 66, 98))
    # chromatophore bands: three broad lit bands with a pink stripe between band two and three
    cols = [CYAN, GREEN, CYAN]
    for i, bx in enumerate([-.28, -.02, .24]):
        if phase == "dark":
            continue
        c = cols[i] if phase != "pink" else PINK
        a = int(190 * bright) if phase != "fade" or i < 1 else int(60 * bright)
        x = cx + ln * bx
        d.polygon([(x - ln * .07, cy - ht * .5), (x + ln * .07, cy - ht * .44), (x + ln * .07, cy + ht * .44), (x - ln * .07, cy + ht * .5)], fill=c + (a,))
    if phase != "dark":
        x = cx + ln * .11  # narrow krill pink stripe between second and third band
        d.polygon([(x - ln * .02, cy - ht * .46), (x + ln * .02, cy - ht * .44), (x + ln * .02, cy + ht * .44), (x - ln * .02, cy + ht * .46)], fill=PINK + (int(200 * bright),))
        # speckle field of plankton green dots
        for _ in range(int(16 * bright)):
            sx, sy = cx + random.uniform(-ln * .45, ln * .4), cy + random.uniform(-ht * .45, ht * .45)
            d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=GREEN + (140,))
    # head and short gathered arms at the left end
    d.ellipse([cx - ln * .58, cy - ht * .42, cx - ln * .36, cy + ht * .42], fill=(24, 66, 98))
    for k in range(5):
        ay = cy - ht * .3 + k * ht * .15
        d.arc([cx - ln * .78, ay - 9, cx - ln * .52, ay + 12], 90, 300, fill=(34, 84, 116), width=3)
    # the large watchful eye
    if eye:
        ex, ey, er = cx - ln * .47, cy - ht * .05, max(3, int(ht * .20))
        d.ellipse([ex - er, ey - er, ex + er, ey + er], fill=(8, 14, 20), outline=(210, 230, 235), width=1)
        d.ellipse([ex - er // 3, ey - er // 3, ex + er // 3, ey + er // 3], fill=(2, 4, 6))
# midground shoal: each animal at a different point in its flash cycle
shoal = [(430, 150, 120, "lit"), (600, 120, 105, "pink"), (760, 165, 130, "fade"), (930, 130, 100, "lit"),
         (520, 235, 110, "fade"), (700, 250, 95, "dark"), (880, 240, 115, "lit"), (1030, 215, 90, "fade"),
         (350, 260, 85, "dark"), (1080, 300, 105, "lit")]
for (x, y, ln, ph) in shoal:
    squid(x, y, ln, "lit" if A == "--v2" else ph)  # v2 flaw: every animal lit at once, a display not an exchange
if A == "--v1":
    pass  # v1 flaw below: foreground squid missing entirely, shoal floats without its close speaker
else:
    # foreground: head and arms of one squid at close range, lower left, bands stopping at the mantle edge
    squid(268, 415, 330, "lit", 1.0, eye=False)
    d.ellipse([76, 374, 154, 452], fill=(6, 12, 18), outline=(215, 235, 240), width=3)  # one eye, huge and dark
    d.ellipse([96, 394, 134, 434], fill=(1, 3, 5))
    d.ellipse([104, 402, 118, 416], fill=(190, 225, 235))
# drifting particles lit inside the shafts
for _ in range(110):
    x, y = random.uniform(0, W), random.uniform(20, 470); r = random.uniform(1, 3)
    near_shaft = min(abs(x - s) for s in (220, 540, 880, 1090)) < 90
    d.ellipse([x - r, y - r, x + r, y + r], fill=(235, 240, 200, 120 if near_shaft else 45))
img = img.filter(ImageFilter.GaussianBlur(0.5))
out = {"--v1": "scratch/intro-v1.png", "--v2": "scratch/intro-v2.png"}.get(A, "intro-banner.png")
img.save(__file__.rsplit("/", 1)[0] + "/" + out); print("saved", out)
