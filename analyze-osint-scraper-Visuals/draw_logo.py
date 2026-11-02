#!/usr/bin/env python3
"""analyze-osint-scraper logo: reef squid in profile on open dark blue water, mantle torpedo shaped, fins at the
tail, arms gathered short under a large eye, three broad chromatophore bands lit on the left half and fading on
the right, one narrow krill pink stripe between the second and third band. Name lettered in Averia Serif Libre
in glacier melt cyan below, ticks notched from the strokes like depth marks on a sounding line."""
import math, random, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
random.seed(7)
A = sys.argv[1] if len(sys.argv) > 1 else ""
W, H = 900, 520
CYAN = (120, 220, 230); GREEN = (110, 230, 160); PINK = (240, 110, 150); BG = (10, 30, 54)
img = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(img, "RGBA")
cx, cy, ln, ht = 450, 205, 560, 168
fine = A == "--v1"  # v1 flaw: bands drawn thin and speckled, they vanish at small size
# tail fins flaring at the right end
d.polygon([(cx + ln * .26, cy), (cx + ln * .52, cy - ht * .92), (cx + ln * .44, cy), (cx + ln * .52, cy + ht * .88)], fill=(30, 80, 112))
# mantle
d.polygon([(cx - ln * .5, cy), (cx - ln * .3, cy - ht * .55), (cx + ln * .3, cy - ht * .42), (cx + ln * .5, cy), (cx + ln * .3, cy + ht * .42), (cx - ln * .3, cy + ht * .55)], fill=(26, 70, 102))
# bands: left half lit, right half fading into dark skin; pink stripe between band 2 and 3
bands = [(-.30, CYAN, 215), (-.06, GREEN, 205), (.16, CYAN, 120)]
for bx, c, al in bands:
    x = cx + ln * bx; wdt = ln * (.015 if fine else .075)
    d.polygon([(x - wdt, cy - ht * .5), (x + wdt, cy - ht * .44), (x + wdt, cy + ht * .44), (x - wdt, cy + ht * .5)], fill=c + (al,))
x = cx + ln * .05
d.polygon([(x - ln * .018, cy - ht * .47), (x + ln * .018, cy - ht * .45), (x + ln * .018, cy + ht * .45), (x - ln * .018, cy + ht * .47)], fill=PINK + (220,))
if fine:
    for _ in range(120):  # fine speckle instead of coarse bands
        sx, sy = cx + random.uniform(-ln * .45, ln * .4), cy + random.uniform(-ht * .45, ht * .45)
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=GREEN + (130,))
else:
    for _ in range(46):  # coarse chromatophore dots gathered into the bands
        bx = random.choice([-.30, -.06, .16]); sx, sy = cx + ln * bx + random.uniform(-16, 16), cy + random.uniform(-ht * .42, ht * .42)
        d.ellipse([sx - 5, sy - 5, sx + 5, sy + 5], fill=random.choice([CYAN, GREEN]) + (150,))
# head with arms gathered short beneath the eye
d.ellipse([cx - ln * .60, cy - ht * .44, cx - ln * .34, cy + ht * .44], fill=(26, 70, 102))
for k in range(6):
    ay = cy - ht * .30 + k * ht * .12
    d.arc([cx - ln * .82, ay - 12, cx - ln * .52, ay + 16], 90, 300, fill=(38, 90, 122), width=5)
# large watchful eye, a third of the head
er = 34
d.ellipse([cx - ln * .47 - er, cy - 8 - er, cx - ln * .47 + er, cy - 8 + er], fill=(8, 14, 20), outline=(215, 235, 240), width=3)
d.ellipse([cx - ln * .47 - 13, cy - 21, cx - ln * .47 + 13, cy + 5], fill=(1, 3, 5))
d.ellipse([cx - ln * .47 - 5, cy - 16, cx - ln * .47 + 5, cy - 6], fill=(200, 230, 240))
# name in Averia Serif Libre, glacier melt cyan, notched at depth intervals: small dark ticks cut from strokes
try:
    f = ImageFont.truetype(__file__.rsplit("/", 1)[0] + "/fonts/AveriaSerifLibre.ttf", 40)
except Exception:
    f = ImageFont.load_default()
name = "analyze-osint-scraper"
d.text((450, 432), name, font=f, fill=CYAN, anchor="mm")
if A != "--v2":  # v2 flaw: ticks omitted, plain printed name with no sounding line marks
    tw = d.textlength(name, font=f); x0 = 450 - tw / 2
    step = tw / 14
    for i in range(14):
        x = x0 + step * i + step * .5
        d.rectangle([x - 2, 414, x + 2, 424], fill=BG)  # tick taken out of the stroke zone above the baseline
        d.rectangle([x - 2, 446, x + 2, 452], fill=BG)
img = img.filter(ImageFilter.GaussianBlur(0.3))
out = {"--v1": "scratch/logo-v1.png", "--v2": "scratch/logo-v2.png"}.get(A, "logo.png")
img.save(__file__.rsplit("/", 1)[0] + "/" + out)
if A == "":
    img.resize((64, 37)).save(__file__.rsplit("/", 1)[0] + "/scratch/logo64-ship.png")
print("saved", out)
