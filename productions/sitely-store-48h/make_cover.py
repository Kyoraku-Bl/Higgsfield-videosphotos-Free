#!/usr/bin/env python3
"""Compose the Instagram Reel cover (1080x1920) + a 1:1 grid preview."""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(ROOT, "fonts")
W, H = 1080, 1920
CREAM = (245, 239, 224); GREEN = (30, 77, 56); BLACK = (10, 12, 10)

base = Image.open(os.path.join(ROOT, "cover", "cover-base.png")).convert("RGB")
base = base.resize((W, H), Image.LANCZOS)
img = base.convert("RGBA")

# legibility gradients (top + bottom)
grad = Image.new("L", (1, H), 0)
for y in range(H):
    top = max(0, 1 - y / 420) * 150
    bot = max(0, (y - 1000) / (H - 1000)) * 205
    grad.putpixel((0, y), int(max(top, bot)))
grad = grad.resize((W, H))
dark = Image.new("RGBA", (W, H), BLACK + (255,)); dark.putalpha(grad)
img = Image.alpha_composite(img, dark)
d = ImageDraw.Draw(img)


def font(sz, w=900): return ImageFont.truetype(os.path.join(FONTS, f"Montserrat-{w}.ttf"), sz)


def fit(text, max_w, start, w=900):
    sz = start
    while font(sz, w).getlength(text) > max_w and sz > 20:
        sz -= 2
    return font(sz, w)


def center(text, y, fnt, fill):
    wpx = fnt.getlength(text); d.text(((W - wpx) / 2, y), text, font=fnt, fill=fill)


# top brand pill
pill_f = font(34, 800); pill_txt = "SITELY STUDIO  •  WEB DESIGN"
pw = pill_f.getlength(pill_txt) + 64
d.rounded_rectangle([(W - pw) / 2, 96, (W + pw) / 2, 168], radius=36, fill=GREEN + (235,))
center(pill_txt, 112, pill_f, CREAM)

# main headline (grid-safe, lower third over gradient, below the face)
l1 = "YOUR STORE ONLINE"; l2 = "IN 48 HOURS"
f1 = fit(l1, 980, 92); f2 = fit(l2, 980, 108)
center(l1, 1180, f1, CREAM)
# green highlight box behind line 2
w2 = f2.getlength(l2); bx = (W - w2) / 2
d.rounded_rectangle([bx - 30, 1300, bx + w2 + 30, 1440], radius=22, fill=GREEN + (240,))
center(l2, 1312, f2, CREAM)

# bottom CTA bar
cta_f = font(44, 800); cta = "DM '48H'  •  FREE MOCKUP"
cw = cta_f.getlength(cta) + 72
d.rounded_rectangle([(W - cw) / 2, 1660, (W + cw) / 2, 1756], radius=48, fill=CREAM + (255,))
center(cta, 1682, cta_f, GREEN)

img = img.convert("RGB")
img.save(os.path.join(ROOT, "cover", "instagram-cover.png"))
# 1:1 grid preview (center crop)
img.crop((0, (H - W) // 2, W, (H + W) // 2)).save(os.path.join(ROOT, "cover", "instagram-cover-grid.png"))
print("cover written")
