#!/usr/bin/env python3
"""Compose 4 Instagram covers (9:16) + 1:1 grid previews, each with logo + @sitely_studioo."""
import os
from PIL import Image, ImageDraw, ImageFont
ROOT = os.path.dirname(os.path.abspath(__file__)); PROD = os.path.dirname(ROOT)
FONTS = os.path.join(PROD, "_shared", "fonts"); BRAND = os.path.join(PROD, "brand")
W, H = 1080, 1920
CREAM = (245, 239, 224); GREEN = (30, 77, 56); BLACK = (10, 12, 10)
COVERS = [
 ("reel-1-speed", ["YOUR WEBSITE", "LIVE IN 48H"]),
 ("reel-2-invisible", ["STOP BEING", "INVISIBLE ONLINE"]),
 ("reel-3-affordable", ["A WEBSITE THAT", "FITS YOUR BUDGET"]),
 ("reel-4-247", ["SELLS WHILE", "YOU SLEEP"]),
]
font = lambda s, w=900: ImageFont.truetype(os.path.join(FONTS, f"Montserrat-{w}.ttf"), s)


def fit(t, mw, s, w=900):
    while font(s, w).getlength(t) > mw and s > 20: s -= 2
    return font(s, w)


for rid, lines in COVERS:
    rd = os.path.join(ROOT, rid)
    base = Image.open(os.path.join(rd, "keyframes", "hook.png")).convert("RGB").resize((W, H), Image.LANCZOS)
    img = base.convert("RGBA")
    grad = Image.new("L", (1, H), 0)
    for y in range(H):
        grad.putpixel((0, y), int(max(max(0, 1-y/420)*150, max(0, (y-1000)/(H-1000))*205)))
    dark = Image.new("RGBA", (W, H), BLACK+(255,)); dark.putalpha(grad.resize((W, H)))
    img = Image.alpha_composite(img, dark); d = ImageDraw.Draw(img)
    # brand pill: logo + @name
    nf = font(40, 800); name = "@sitely_studioo"; tw = nf.getlength(name)
    pw = int(96 + 18 + tw + 56); ph = 108
    px = (W-pw)/2
    d.rounded_rectangle([px, 92, px+pw, 92+ph], ph//2, fill=(10, 14, 12, 215))
    lg = Image.open(os.path.join(BRAND, "sitely-logo.png")).convert("RGBA").resize((84, 84), Image.LANCZOS)
    img.alpha_composite(lg, (int(px)+12, 92+12))
    d.text((px+96+18, 92+(ph-40)//2-4), name, font=nf, fill=CREAM)
    # headline
    f1 = fit(lines[0], 980, 88); f2 = fit(lines[1], 940, 100)
    w1 = f1.getlength(lines[0]); d.text(((W-w1)/2, 1180), lines[0], font=f1, fill=CREAM)
    w2 = f2.getlength(lines[1]); bx = (W-w2)/2
    d.rounded_rectangle([bx-30, 1300, bx+w2+30, 1440], 22, fill=GREEN+(240,))
    d.text((bx, 1312), lines[1], font=f2, fill=CREAM)
    # CTA bar
    cf = font(44, 800); cta = "DM 'SITE'  •  FREE MOCKUP"; cw = cf.getlength(cta)+72
    d.rounded_rectangle([(W-cw)/2, 1660, (W+cw)/2, 1756], 48, fill=CREAM+(255,))
    d.text(((W-cf.getlength(cta))/2, 1682), cta, font=cf, fill=GREEN)
    img = img.convert("RGB")
    img.save(os.path.join(rd, "cover", "instagram-cover.png"))
    img.crop((0, (H-W)//2, W, (H+W)//2)).save(os.path.join(rd, "cover", "instagram-cover-grid.png"))
    print("cover", rid)
print("COVERS DONE")
