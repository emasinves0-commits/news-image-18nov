from PIL import Image, ImageDraw, ImageFont
import math
W = H = 1024
B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
f = lambda p, s: ImageFont.truetype(p, s)
img = Image.new("RGB", (W, H), (14, 22, 40))
d = ImageDraw.Draw(img)
boxes = []
def text(xy, s, font, fill, anchor="la"):
    d.text(xy, s, font=font, fill=fill, anchor=anchor)
    boxes.append((s, d.textbbox(xy, s, font=font, anchor=anchor)))

# header
d.rectangle([0, 0, W, 190], fill=(200, 30, 45))
text((W//2, 22), "WORLD NEWS · WEDNESDAY", f(B, 32), (255, 255, 255), "ma")
text((W//2, 112), "18 November 2026", f(B, 88), (255, 255, 255), "mm")
text((W//2, 165), "Five stories of the day", f(R, 26), (255, 220, 225), "mm")

stories = [
 ("APEC summit opens in Shenzhen", "Xi greets Trump on arrival in China", (30, 120, 200), "globe"),
 ("Iran and US trade strikes in Gulf", "Kuwait and Bahrain bases targeted", (210, 90, 30), "blast"),
 ("Putin 'not ready' for Ukraine peace", "Per NYT sources; war goes on", (40, 150, 90), "dove"),
 ("Peltola wins Alaska Senate seat", "Democrats reach 56-44 majority", (120, 70, 190), "vote"),
 ("US loses measles elimination status", "Confirmed by HHS Secretary", (190, 50, 110), "virus"),
]
top, ph, gap = 203, 146, 10
def icon(kind, cx, cy, c):
    w = (255, 255, 255)
    if kind == "globe":
        d.ellipse([cx-48, cy-48, cx+48, cy+48], outline=w, width=6)
        d.ellipse([cx-20, cy-48, cx+20, cy+48], outline=w, width=5)
        d.line([cx-48, cy, cx+48, cy], fill=w, width=5)
    elif kind == "blast":
        pts = []
        for i in range(16):
            r = 52 if i % 2 == 0 else 24
            a = i * math.pi / 8
            pts.append((cx + r*math.cos(a), cy + r*math.sin(a)))
        d.polygon(pts, fill=w)
    elif kind == "dove":
        d.ellipse([cx-40, cy-12, cx+30, cy+30], fill=w)
        d.polygon([(cx-10, cy-6), (cx-40, cy-50), (cx+10, cy-14)], fill=w)
        d.polygon([(cx-38, cy+4), (cx-62, cy+22), (cx-34, cy+22)], fill=w)
        d.ellipse([cx+16, cy-30, cx+44, cy-2], fill=w)
        d.polygon([(cx+42, cy-18), (cx+58, cy-12), (cx+42, cy-8)], fill=c)
    elif kind == "vote":
        d.rectangle([cx-44, cy-6, cx+44, cy+40], fill=w)
        d.rectangle([cx-26, cy-44, cx+26, cy-6], outline=w, width=5)
        d.line([cx-18, cy+14, cx-4, cy+28, cx+22, cy+2], fill=c, width=8)
    elif kind == "virus":
        d.ellipse([cx-30, cy-30, cx+30, cy+30], fill=w)
        for i in range(10):
            a = i * math.pi / 5
            x1, y1 = cx+30*math.cos(a), cy+30*math.sin(a)
            x2, y2 = cx+48*math.cos(a), cy+48*math.sin(a)
            d.line([x1, y1, x2, y2], fill=w, width=5)
            d.ellipse([x2-7, y2-7, x2+7, y2+7], fill=w)
for i, (h, sub, col, ic) in enumerate(stories):
    y = top + i*(ph+gap)
    d.rounded_rectangle([24, y, W-24, y+ph], 18, fill=col)
    d.rounded_rectangle([40, y+20, 40+110, y+ph-20], 14, fill=tuple(int(v*0.65) for v in col))
    icon(ic, 95, y+ph//2, col)
    text((178, y+18), "18 Nov", f(B, 24), (255, 255, 255, ), "la")
    text((178, y+52), h, f(B, 36), (255, 255, 255))
    text((178, y+100), sub, f(R, 26), (240, 240, 245))
text((W//2, 1008), "Sources: Just Security, Anadolu, SCMP - see README", f(R, 18), (160, 170, 190), "ms")
# overlap check
bad = 0
for i in range(len(boxes)):
    for j in range(i+1, len(boxes)):
        a, b = boxes[i][1], boxes[j][1]
        if a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]:
            bad += 1; print("OVERLAP", boxes[i][0], "|", boxes[j][0])
for s, b in boxes:
    if b[0] < 0 or b[2] > W or b[3] > H: print("OUT OF BOUNDS", s, b); bad += 1
    if s != "Sources: Just Security, Anadolu, SCMP - see README" and b[2] > W-30: print("TOO WIDE", s, b); bad += 1
print("overlaps/out-of-bounds:", bad)
img.save("entry.png", optimize=True)
