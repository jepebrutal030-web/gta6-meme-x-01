#!/usr/bin/env python3
"""Draw the GTA 6 meme-x entry: VICE CITY MARKET receipt.

Style follows the top 1 entry (receipt format, GTA timeline on top,
sunset skyline, make.fun ghost mascot, pink accents) but every line of
content is original: different store, different line items, different
stamp and footer. No em dash or en dash anywhere in the image.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
CREAM = (245, 240, 230)
INK = (20, 20, 30)
PINK = (214, 51, 132)
PINK_DK = (176, 32, 104)
GOLD = (212, 160, 60)
WHITE = (255, 255, 255)

F_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
F_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
F_M = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
F_MB = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def star4(d, cx, cy, r, fill):
    """Four-pointed sparkle star."""
    pts = []
    for i in range(8):
        ang = math.pi / 2 + i * math.pi / 4
        rr = r if i % 2 == 0 else r * 0.28
        pts.append((cx + rr * math.cos(ang), cy - rr * math.sin(ang)))
    d.polygon(pts, fill=fill)


def star5(d, cx, cy, r, fill):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=fill)


def draw_ghost(d, cx, cy, s):
    """make.fun ghost: white capsule body, black outline, sparkle eyes,
    round hand holding a magenta coin with a white star.
    s = overall scale (body width ~ s)."""
    w = s
    h = s * 1.15
    x0, y0 = cx - w / 2, cy - h / 2
    x1, y1 = cx + w / 2, cy + h / 2
    # capsule body: white, thick black outline
    d.rounded_rectangle([x0, y0, x1, y1], radius=w * 0.45,
                        fill=WHITE, outline=INK, width=7)
    # eyes: two black four-pointed sparkles
    star4(d, cx - w * 0.20, cy - h * 0.12, w * 0.11, INK)
    star4(d, cx + w * 0.20, cy - h * 0.12, w * 0.11, INK)
    # hand + magenta coin with white star (right side)
    hx, hy = cx + w * 0.52, cy + h * 0.08
    d.ellipse([hx - w * 0.10, hy - w * 0.10, hx + w * 0.10, hy + w * 0.10],
              fill=WHITE, outline=INK, width=6)
    cr = w * 0.17
    ccx, ccy = hx + w * 0.16, hy - w * 0.06
    d.ellipse([ccx - cr, ccy - cr, ccx + cr, ccy + cr],
              fill=PINK, outline=INK, width=6)
    star5(d, ccx, ccy, cr * 0.62, WHITE)


def sunset_sky(d, x0, y0, x1, y1):
    """Vertical gradient sky: orange top to pink to purple bottom."""
    steps = 60
    top = (255, 150, 80)
    mid = (255, 110, 150)
    bot = (120, 70, 160)
    for i in range(steps):
        t = i / (steps - 1)
        if t < 0.5:
            u = t / 0.5
            c = tuple(int(top[k] + (mid[k] - top[k]) * u) for k in range(3))
        else:
            u = (t - 0.5) / 0.5
            c = tuple(int(mid[k] + (bot[k] - mid[k]) * u) for k in range(3))
        yy0 = y0 + (y1 - y0) * i / steps
        yy1 = y0 + (y1 - y0) * (i + 1) / steps
        d.rectangle([x0, yy0, x1, yy1], fill=c)


def skyline(d, x0, y0, x1, y1, seed=7):
    """Dark building silhouettes with lit windows."""
    import random
    rnd = random.Random(seed)
    x = x0
    while x < x1:
        bw = rnd.randint(46, 92)
        bh = rnd.randint(60, 170)
        by1 = y1
        by0 = y1 - bh
        d.rectangle([x, by0, x + bw, by1], fill=(28, 22, 48))
        # lit windows
        for wy in range(int(by0) + 10, int(by1) - 8, 18):
            for wx in range(int(x) + 8, int(x) + bw - 8, 16):
                if rnd.random() < 0.35:
                    d.rectangle([wx, wy, wx + 7, wy + 9],
                                fill=(255, 214, 120))
        x += bw + rnd.randint(2, 10)


def dotted_leader(d, x0, x1, y, fill=(120, 110, 100)):
    x = x0
    while x < x1:
        d.ellipse([x, y - 2, x + 4, y + 2], fill=fill)
        x += 10


def main():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)

    # ---------- top timeline strip ----------
    games = [
        ("GTA", "1997", (200, 60, 60)),
        ("GTA II", "1999", (190, 120, 40)),
        ("GTA III", "2001", (60, 90, 180)),
        ("VICE CITY", "2002", (40, 160, 140)),
        ("SAN ANDREAS", "2004", (90, 170, 60)),
        ("GTA IV", "2008", (90, 90, 120)),
        ("GTA V", "2011", (210, 140, 40)),
        ("GTA VI", "2026", (214, 51, 132)),
    ]
    strip_y0, strip_y1 = 18, 128
    cell_w = (W - 36) / len(games)
    for i, (name, year, col) in enumerate(games):
        cx0 = 18 + i * cell_w
        cx1 = cx0 + cell_w - 6
        d.rounded_rectangle([cx0, strip_y0, cx1, strip_y1], radius=8,
                            fill=col, outline=INK, width=3)
        # tiny skyline icon
        d.rectangle([cx0 + 10, strip_y0 + 34, cx0 + 22, strip_y0 + 58],
                    fill=(255, 255, 255))
        d.rectangle([cx0 + 26, strip_y0 + 26, cx0 + 40, strip_y0 + 58],
                    fill=(255, 255, 255))
        d.rectangle([cx0 + 44, strip_y0 + 40, cx0 + 54, strip_y0 + 58],
                    fill=(255, 255, 255))
        d.ellipse([cx0 + cell_w - 30, strip_y0 + 12, cx0 + cell_w - 12,
                   strip_y0 + 30], fill=(255, 230, 120))
        f1 = font(F_B, 13)
        f2 = font(F_B, 15)
        d.text((cx0 + cell_w / 2, strip_y0 + 66), name, font=f1,
               fill=WHITE, anchor="mt")
        d.text((cx0 + cell_w / 2, strip_y0 + 86), year, font=f2,
               fill=WHITE, anchor="mt")
        if name == "GTA VI":
            d.rounded_rectangle([cx1 - 52, strip_y0 - 2, cx1 + 2, strip_y0 + 20],
                                radius=9, fill=PINK, outline=WHITE, width=2)
            d.text((cx1 - 25, strip_y0 + 9), "NEW", font=font(F_B, 13),
                   fill=WHITE, anchor="mm")

    # ---------- hero band: sunset skyline ----------
    hx0, hy0, hx1, hy1 = 18, 140, W - 18, 450
    sunset_sky(d, hx0, hy0, hx1, hy1)
    # sun
    d.ellipse([hx1 - 150, hy0 + 26, hx1 - 70, hy0 + 106],
              fill=(255, 224, 130), outline=(255, 200, 90), width=3)
    skyline(d, hx0, hy0, hx1, hy1)
    d.rectangle([hx0, hy0, hx1, hy1], outline=INK, width=4)
    # ghost in pink disc, center
    gx, gy = W // 2, 300
    d.ellipse([gx - 118, gy - 118, gx + 118, gy + 118],
              fill=PINK, outline=INK, width=6)
    draw_ghost(d, gx, gy + 6, 150)
    # make.fun pill
    pill = font(F_B, 30)
    d.rounded_rectangle([gx - 105, 392, gx + 105, 436], radius=20,
                        fill=WHITE, outline=INK, width=4)
    d.text((gx, 414), "make.fun", font=pill, fill=INK, anchor="mm")
    # NOW SERVING badge
    d.rounded_rectangle([hx1 - 262, 400, hx1 - 14, 440], radius=12,
                        fill=(20, 20, 30), outline=GOLD, width=3)
    d.text((hx1 - 138, 420), "NOW SERVING #13", font=font(F_B, 20),
           fill=GOLD, anchor="mm")

    # ---------- receipt card ----------
    rx0, ry0, rx1, ry1 = 30, 470, W - 30, 920
    d.rounded_rectangle([rx0, ry0, rx1, ry1], radius=10,
                        fill=WHITE, outline=INK, width=4)
    # header
    d.text((rx0 + 26, ry0 + 34), "VICE CITY MARKET",
           font=font(F_B, 40), fill=INK)
    d.text((rx1 - 26, ry0 + 34), "CUSTOMER RECEIPT",
           font=font(F_B, 22), fill=PINK, anchor="ra")
    d.line([rx0 + 26, ry0 + 78, rx1 - 26, ry0 + 78], fill=PINK, width=4)

    items = [
        ("Years in line", "13"),
        ("Delays survived", "2"),
        ("Trailer rewatches", "200M"),
        ("Sick days saved", "5"),
        ("GTA VI", "$79.99"),
    ]
    y = ry0 + 112
    f_item = font(F_R, 30)
    f_val = font(F_MB, 30)
    for label, val in items:
        pink = (label == "GTA VI")
        col = PINK if pink else INK
        f_l = font(F_B, 30) if pink else f_item
        d.text((rx0 + 26, y), label, font=f_l, fill=col)
        vw = d.textlength(val, font=f_val)
        d.text((rx1 - 26 - vw, y), val, font=f_val, fill=col)
        lw = d.textlength(label, font=f_l)
        dotted_leader(d, rx0 + 26 + lw + 14, rx1 - 26 - vw - 14, y + 18)
        y += 48

    # total
    y += 6
    d.line([rx0 + 26, y, rx1 - 26, y], fill=INK, width=3)
    y += 16
    d.text((rx0 + 26, y), "TOTAL DUE", font=font(F_B, 40), fill=INK)
    tot = "$79.99"
    tw = d.textlength(tot, font=font(F_B, 44))
    d.text((rx1 - 26 - tw, y - 2), tot, font=font(F_B, 44), fill=PINK)
    # stamp (rotated), tucked over the total row, inside the card
    stamp = Image.new("RGBA", (300, 84), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stamp)
    sd.rounded_rectangle([4, 4, 296, 80], radius=8,
                         outline=PINK, width=5)
    sd.text((150, 30), "PAID BY MY AGENT", font=font(F_B, 24),
            fill=PINK, anchor="mm")
    sd.text((150, 58), "ON MAKE.FUN", font=font(F_B, 24),
            fill=PINK, anchor="mm")
    stamp = stamp.rotate(-9, expand=True, resample=Image.BICUBIC)
    img.paste(stamp, (rx0 + 330, y - 26), stamp)

    # ---------- footer ----------
    fy0, fy1 = 934, H - 18
    d.rounded_rectangle([18, fy0, W - 18, fy1], radius=12,
                        fill=(20, 20, 30))
    d.text((W // 2, (fy0 + fy1) // 2),
           "Paid by my AI agent on make.fun. Agents earn real money there.",
           font=font(F_B, 24), fill=WHITE, anchor="mm")

    img.save("/home/hatch/workspace/makefun/gta6-meme-x-01/meme.png")
    print("saved /home/hatch/workspace/makefun/gta6-meme-x-01/meme.png")


if __name__ == "__main__":
    main()
