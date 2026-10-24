#!/usr/bin/env python3
"""leevorá 2x4 ft LED standee — compositor v4.

Layout built on reading order and trust: brand -> hook -> real person (framed photo, real setting)
-> scan loupe (proof) -> offer -> trust strip -> action. No cut-outs, no recoloured faces.
Exports: CMYK FOGRA39 vector PDF (outlined type, 10 mm bleed, crop marks), CMYK + sRGB TIFFs,
flex-wrap TIFF, day / lit-at-night previews.   Usage: build4.py A|B   (PREVIEW=1 for a quick look)
"""
import sys, os, io, math, json, subprocess
import numpy as np, cv2, skia, qrcode, pikepdf
from PIL import Image, ImageCms

ROOT = '/tmp/claude-0/-home-user-Adsworm/3d8d5e5a-8f36-56e6-be63-644bad3ee2df/scratchpad'
sys.path.insert(0, f'{ROOT}/engine')
from typeset import Font

SIDE = sys.argv[1] if len(sys.argv) > 1 else 'A'
OUT = f'{ROOT}/out'
os.makedirs(OUT, exist_ok=True)
Image.MAX_IMAGE_PIXELS = None

# ---------------------------------------------------------------- geometry (inches, trim origin top-left)
PPI = 150
EXT = 3.0
TW, TH = 24.0, 48.0
BLEED = 10 / 25.4
SAFE = 40 / 25.4
CW, CH = TW + 2 * EXT, TH + 2 * EXT
W, H = round(CW * PPI), round(CH * PPI)
CX = TW / 2


def px(v):
    return (v + EXT) * PPI


# ---------------------------------------------------------------- colour
ICC_CMYK = f'{ROOT}/icc/FOGRA39.icc'
ICC_SRGB = '/usr/share/color/icc/sRGB.icc'
srgb_p, cmyk_p = ImageCms.getOpenProfile(ICC_SRGB), ImageCms.getOpenProfile(ICC_CMYK)
to_cmyk = ImageCms.buildTransform(srgb_p, cmyk_p, 'RGB', 'CMYK', renderingIntent=1, flags=ImageCms.Flags.BLACKPOINTCOMPENSATION)
to_rgb = ImageCms.buildTransform(cmyk_p, srgb_p, 'CMYK', 'RGB', renderingIntent=1, flags=ImageCms.Flags.BLACKPOINTCOMPENSATION)


def from_cmyk(c, m, y, k):
    im = Image.new('CMYK', (1, 1), tuple(round(v * 2.55) for v in (c, m, y, k)))
    return '#%02X%02X%02X' % ImageCms.applyTransform(im, to_rgb).getpixel((0, 0))


def hx(h):
    return np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)], np.float32) / 255


PAL = dict(
    bg_core='#163A33', bg_mid='#0E2723', bg_edge='#07171A',
    cream='#FBF3E4', gold='#E4BA6E', sage='#A3B7AD', ink='#0D2622',
    aqua=from_cmyk(55, 0, 22, 0), aqua_hot=from_cmyk(14, 0, 6, 0),
    qr_tile=from_cmyk(8, 8, 20, 25),
)


def C4(name, a=1.0):
    r, g, b = hx(PAL[name]) if name in PAL else hx(name)
    return skia.Color4f(float(r), float(g), float(b), a)


SERIF = 'Gloock-Regular'
SANS_B, SANS_SB, SANS_M, SANS_R = (f'InstrumentSans-{w}' for w in ('Bold', 'SemiBold', 'Medium', 'Regular'))

# ---------------------------------------------------------------- side config
WA = 'https://wa.me/918076467352?text='
CFG = {
    'A': dict(
        photo='hero/woman4.png', npz='hero/woman4.npz', face_w=6.9, face_dx=-1.55,
        head=['Your mirror', 'only shows half.'], accent='half.',
        offer='Free Skin & Hair Analysis',
        trust=['8-spectrum AI skin scan', 'Expert-led plan', 'Free, no obligation'],
        loupe_title='WHAT THE SCAN SEES', loupe_sub='Pigment & UV damage',
        qr=WA + 'Hi%21%20I%27d%20like%20my%20free%20skin%20analysis',
    ),
    'B': dict(
        photo='hero/man4.png', npz='hero/man4.npz', face_w=6.9, face_dx=-1.55,
        head=['Hair fall', 'has a reason.'], accent='reason.',
        offer='Free Hair & Skin Analysis',
        trust=['Hair & scalp imaging', 'Expert-led plan', 'Free, no obligation'],
        loupe_title='WHAT THE SCAN SEES', loupe_sub='Thinning at the temples', loupe_img='hero/tricho.png',
        qr=WA + 'Hi%21%20I%27d%20like%20my%20free%20hair%20analysis',
    ),
}[SIDE]

# vertical rhythm (shared by both faces)
Y_NOW, LOGO_TOP, LOGO_W = 2.55, 3.22, 8.8
HS = 2.72
HL1 = 6.95 + 0.75 * HS
HL2 = HL1 + 0.93 * HS
FR = (SAFE, 12.40, TW - SAFE, 31.80)          # photo frame
FR_R = 0.55
OFFER_TOP = 32.70
TRUST_Y = 37.80
QR_TOP = 39.45


def smooth(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0, 1)
    return t * t * (3 - 2 * t)


def gblur(a, sigma_px):
    if sigma_px <= 0:
        return a
    k = int(sigma_px * 3) * 2 + 1
    return cv2.GaussianBlur(a, (k, k), sigma_px)


def lerp(a, b, t):
    return a + (b - a) * t


def paint(color, stroke=None, aa=True):
    p = skia.Paint(AntiAlias=aa, Color4f=color)
    if stroke:
        p.setStyle(skia.Paint.kStroke_Style)
        p.setStrokeWidth(stroke)
        p.setStrokeCap(skia.Paint.kRound_Cap)
    return p


def raster_layer(draw_fn, ppi=PPI, margin=EXT, alpha_only=False):
    w, h = round((TW + 2 * margin) * ppi), round((TH + 2 * margin) * ppi)
    surf = skia.Surface.MakeRaster(skia.ImageInfo.MakeA8(w, h)) if alpha_only else skia.Surface(w, h)
    c = surf.getCanvas()
    c.clear(skia.Color4f(0, 0, 0, 0))
    c.scale(ppi, ppi)
    c.translate(margin, margin)
    draw_fn(c)
    img = surf.makeImageSnapshot()
    if alpha_only:
        return img.toarray(colorType=skia.kAlpha_8_ColorType).astype(np.float32) / 255
    return img.toarray(colorType=skia.kRGBA_8888_ColorType, alphaType=skia.kPremul_AlphaType).astype(np.float32) / 255


def crop_in(arr, margin, ppi=PPI, ext=EXT):
    b0 = int(round((ext - margin) * ppi))
    return arr[b0:arr.shape[0] - b0, b0:arr.shape[1] - b0]


# ================================================================ RASTER PLATE
ys = (np.arange(H, dtype=np.float32)[:, None] / PPI - EXT)
xs = (np.arange(W, dtype=np.float32)[None, :] / PPI - EXT)

# brand background
d = np.sqrt(((xs - CX) / 15.0) ** 2 + ((ys - 20.0) / 19.0) ** 2)
tb = smooth(0.0, 1.25, d)[..., None]
bg = lerp(hx(PAL['bg_core']), hx(PAL['bg_mid']), np.clip(tb * 1.6, 0, 1))
bg = lerp(bg, hx(PAL['bg_edge']), np.clip(tb * 1.6 - 0.6, 0, 1))
comp = bg * (1 - 0.15 * smooth(32, 50, ys))[..., None]
del d, tb, bg

# --- the photo, whole and real, in a rounded frame
P = np.load(f'{ROOT}/{CFG["npz"]}')
pts = P['pts'][:, :2].astype(np.float64)
src = cv2.imread(f'{ROOT}/{CFG["photo"]}', cv2.IMREAD_COLOR)[..., ::-1].astype(np.float32) / 255
sh, sw = src.shape[:2]
fx0, fy0, fx1, fy1 = FR
fw, fh = fx1 - fx0, fy1 - fy0
eye = (pts[468] + pts[473]) / 2
s_in = CFG['face_w'] / np.linalg.norm(pts[454] - pts[234])       # inches per source px
# eyes at 40% of frame height, face a little left of centre (room for the loupe on the right)
ex_t, ey_t = CX + CFG['face_dx'], fy0 + 0.40 * fh
# make sure the photo covers the frame; grow the scale if needed
for _ in range(20):
    left, top = ex_t - eye[0] * s_in, ey_t - eye[1] * s_in
    right, bottom = left + sw * s_in, top + sh * s_in
    if left <= fx0 and top <= fy0 and right >= fx1 and bottom >= fy1:
        break
    s_in *= 1.03
s = s_in * PPI
tx, ty = px(left), px(top)
M = np.float32([[s, 0, tx], [0, s, ty]])


def T(i):
    return pts[i] * s + np.array([tx, ty])


def Ti(i):
    p = T(i) / PPI - EXT
    return float(p[0]), float(p[1])


photo = cv2.warpAffine(src, M, (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT)
# grade: true and gentle. Tiny warmth, very slight lift, soft vignette inside the frame
photo = np.clip(photo * np.float32([1.01, 1.0, 0.985]), 0, 1)
photo = photo + (1 - photo) * 0.03
vig = 1 - 0.16 * smooth(0.55, 1.15, np.sqrt(((xs - (fx0 + fx1) / 2) / (fw / 2)) ** 2 + ((ys - (fy0 + fy1) / 2) / (fh / 2)) ** 2))
photo *= vig[..., None]
del vig


def frame_path():
    p = skia.Path()
    p.addRRect(skia.RRect.MakeRectXY(skia.Rect(fx0, fy0, fx1, fy1), FR_R, FR_R))
    return p


fmask = raster_layer(lambda c: c.drawPath(frame_path(), paint(skia.Color4f(1, 1, 1, 1))), alpha_only=True)
comp = lerp(comp, photo, fmask[..., None])
del photo

# --- the loupe: a magnified "what the scan sees" view of a real spot on this face
LR = 3.30                                     # loupe radius (in)
LC = (fx1 - LR + 0.55, fy0 + 0.60 * fh)       # breaks the frame edge slightly: depth
if SIDE == 'A':
    sp = pts[425] * 0.92 + pts[280] * 0.08    # viewer-right cheek, clear of the nose, where the pigment sits
    zoom = 2.5
else:
    facem_src = P['face'].astype(np.float32)
    xq = int(pts[332, 0] + 0.35 * (pts[454, 0] - pts[332, 0]))
    ytop = int(np.argmax(facem_src[:, xq] > 0.5))
    sp = np.array([xq, ytop - 0.012 * sh])    # the receding temple, just behind the hairline
    zoom = 1.75
SPOT = ((sp[0] * s + tx) / PPI - EXT, (sp[1] * s + ty) / PPI - EXT)
zs = s * zoom
Mz = np.float32([[zs, 0, px(LC[0]) - sp[0] * zs], [0, zs, px(LC[1]) - sp[1] * zs]])
lz = cv2.warpAffine(src, Mz, (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT)
lz = np.clip(lz + (lz - gblur(lz, 2.2)) * 0.7, 0, 1)              # restore crispness after magnifying
if SIDE == 'A':
    # UV channel the way an analyser renders it: smooth skin, pigment and UV damage read as dark spots
    uv = lz @ np.float32([0.08, 0.32, 0.60])
    y0, y1 = int(px(LC[1] - LR - 0.2)), int(px(LC[1] + LR + 0.2))
    x0, x1 = int(px(LC[0] - LR - 0.2)), int(px(LC[0] + LR + 0.2))
    cl = cv2.createCLAHE(clipLimit=2.2, tileGridSize=(6, 6)).apply((np.clip(uv[y0:y1, x0:x1], 0, 1) * 255).astype(np.uint8))
    v = np.zeros_like(uv)
    v[y0:y1, x0:x1] = gblur(cl.astype(np.float32) / 255, 1.2)
    view = v[..., None] * np.float32([0.62, 1.0, 0.98]) * 1.22 + np.float32([0.0, 0.04, 0.05])
    dog = gblur(uv, 3.0) - gblur(uv, 14.0)
    del uv, cl, v
else:
    # trichoscope view of that temple: the scalp at ~20x, as the clinic's hair analysis shows it
    tri = cv2.imread(f'{ROOT}/{CFG["loupe_img"]}', cv2.IMREAD_COLOR)[..., ::-1].astype(np.float32) / 255
    dpx = int(round(2 * (LR + 0.1) * PPI))
    tri = cv2.resize(tri, (dpx, dpx), interpolation=cv2.INTER_AREA if tri.shape[0] > dpx else cv2.INTER_CUBIC)
    view = np.zeros((H, W, 3), np.float32)
    cy0, cx0 = int(round(px(LC[1]))) - dpx // 2, int(round(px(LC[0]))) - dpx // 2
    view[cy0:cy0 + dpx, cx0:cx0 + dpx] = tri * np.float32([0.97, 1.0, 1.02])
    dog = None
    del tri
rr = np.sqrt((xs - LC[0]) ** 2 + (ys - LC[1]) ** 2)
view *= (1 - 0.35 * smooth(0.55 * LR, LR, rr))[..., None]          # lens fall-off
lmask = (1 - smooth(LR - 0.012, LR + 0.012, rr))
# soft shadow under the lens
sh_m = gblur((1 - smooth(LR - 0.02, LR + 0.02, np.sqrt((xs - LC[0] - 0.10) ** 2 + (ys - LC[1] - 0.22) ** 2))).astype(np.float32), 0.22 * PPI)
comp *= (1 - 0.45 * sh_m * (1 - lmask))[..., None]
comp = lerp(comp, np.clip(view, 0, 1), lmask[..., None])
LOUPE_SPOTS = []
if dog is not None:
    sc = np.where(rr < LR * 0.72, -dog, 0)
    mx = cv2.dilate(sc, np.ones((int(0.55 * PPI),) * 2, np.uint8))
    cand = sorted(np.argwhere((sc == mx) & (sc > 0.01)), key=lambda q: -sc[q[0], q[1]])
    for yv, xv in cand:
        q = (xv / PPI - EXT, yv / PPI - EXT)
        if all(math.dist(q, o) > 1.0 for o in LOUPE_SPOTS):
            LOUPE_SPOTS.append(q)
        if len(LOUPE_SPOTS) >= 3:
            break
    del sc, mx
del lz, view, rr, sh_m, src

rng = np.random.default_rng(7)
comp = np.clip(comp + gblur(rng.normal(0, 1, (H, W)).astype(np.float32), 0.5)[..., None] * 0.008, 0, 1)

# ================================================================ VECTORS
F = {n: Font.get(n) for n in (SERIF, SANS_B, SANS_SB, SANS_M, SANS_R)}


def text(c, s_, font, size, x, y, color, align='center', tracking=0.0):
    p, w = F[font].path(s_, size, x, y, align, tracking)
    c.drawPath(p, paint(color))
    return w


LOGO = json.load(open(f'{ROOT}/engine/leevora_logo.json'))
LOGO_COL = '#%02X%02X%02X' % tuple(round(v * 255) for v in LOGO['color'])


def logo_path(parts, sc, ox, oy):
    p = skia.Path()
    for f in parts:
        for sp_ in f['path']:
            for seg in sp_:
                k, q = seg[0], [(ox + a * sc, oy + b * sc) for a, b in seg[1:]]
                if k == 'M':
                    p.moveTo(*q[0])
                elif k == 'L':
                    p.lineTo(*q[0])
                elif k == 'C':
                    p.cubicTo(*q[0], *q[1], *q[2])
                elif k == 'Z':
                    p.close()
    return p


def draw_logo(c, cx, top, width):
    sc = width / LOGO['w']
    for part in ('word', 'desc'):
        c.drawPath(logo_path(LOGO[part], sc, cx - width / 2, top), paint(C4(LOGO_COL)))


def check_icon(c, x, y, r, col):
    c.drawCircle(x, y, r, paint(col, stroke=0.035))
    p = skia.Path()
    p.moveTo(x - r * 0.45, y + r * 0.02)
    p.lineTo(x - r * 0.10, y + r * 0.38)
    p.lineTo(x + r * 0.50, y - r * 0.32)
    pp = paint(col, stroke=0.045)
    pp.setStrokeJoin(skia.Paint.kRound_Join)
    c.drawPath(p, pp)


LAY = {}


def draw_vectors(c):
    gold = C4('gold')
    # 1. brand (eye level): new clinic, real logo
    nw = text(c, 'NOW OPEN', SANS_B, 0.90, CX, Y_NOW, gold, tracking=0.24)
    rl = paint(C4('gold', 0.9), stroke=0.032)
    for sg in (-1, 1):
        c.drawLine(CX + sg * (nw / 2 + 0.55), Y_NOW - 0.32, CX + sg * (nw / 2 + 3.4), Y_NOW - 0.32, rl)
    draw_logo(c, CX, LOGO_TOP, LOGO_W)

    # 2. hook
    l1, l2 = CFG['head']
    text(c, l1, SERIF, HS, CX, HL1, C4('cream'))
    acc = CFG['accent']
    pre = l2[:-len(acc)]
    x0_ = CX - F[SERIF].width(l2, HS) / 2
    text(c, pre, SERIF, HS, x0_, HL2, C4('cream'), align='left')
    text(c, acc, SERIF, HS, x0_ + F[SERIF].width(pre, HS), HL2, C4('aqua'), align='left')

    # 3. photo frame line
    c.drawPath(frame_path(), paint(C4('gold', 0.9), stroke=0.035))

    # 4. loupe: rings, the spot it reads, leader, caption badge
    aqua = C4('aqua')
    c.drawCircle(*LC, LR, paint(C4('aqua_hot'), stroke=0.07))
    c.drawCircle(*LC, LR + 0.16, paint(C4('aqua', 0.7), stroke=0.022))
    c.drawCircle(*SPOT, 0.30, paint(C4('aqua_hot'), stroke=0.045))
    ang = math.atan2(LC[1] - SPOT[1], LC[0] - SPOT[0])
    c.drawLine(SPOT[0] + 0.30 * math.cos(ang), SPOT[1] + 0.30 * math.sin(ang),
               LC[0] - (LR + 0.16) * math.cos(ang), LC[1] - (LR + 0.16) * math.sin(ang), paint(C4('aqua_hot', 0.95), stroke=0.03))
    for q in LOUPE_SPOTS:
        c.drawCircle(*q, 0.26, paint(C4('cream', 0.95), stroke=0.04))
    # caption badge sitting on the bottom of the lens
    t1, t2 = CFG['loupe_title'], CFG['loupe_sub']
    w1 = F[SANS_SB].width(t1, 0.34, 0.16)
    w2 = F[SERIF].width(t2, 0.60)
    bw = max(w1, w2) + 0.9
    by0 = LC[1] + LR - 0.55
    badge = skia.RRect.MakeRectXY(skia.Rect(LC[0] - bw / 2, by0, LC[0] + bw / 2, by0 + 1.42), 0.30, 0.30)
    c.drawRRect(badge, paint(C4('ink', 0.94)))
    c.drawRRect(badge, paint(C4('aqua', 0.8), stroke=0.022))
    text(c, t1, SANS_SB, 0.34, LC[0], by0 + 0.52, aqua, tracking=0.16)
    text(c, t2, SERIF, 0.60, LC[0], by0 + 1.13, C4('cream'))
    LAY['loupe'] = (LC[0], LC[1], LR)

    # 5. offer in a thin gold outline frame
    osz = 17.4 / F[SERIF].width(CFG['offer'], 1)
    oy = OFFER_TOP + 0.62 + osz * 0.75
    text(c, CFG['offer'], SERIF, osz, CX, oy, gold)
    text(c, 'LAUNCH MONTH ONLY', SANS_SB, 0.66, CX, oy + 1.30, gold, tracking=0.22)
    fr = skia.Rect(CX - 10.0, OFFER_TOP, CX + 10.0, oy + 1.30 + 0.62)
    c.drawRRect(skia.RRect.MakeRectXY(fr, 1.0, 1.0), paint(C4('gold', 0.95), stroke=0.045))

    # 6. trust strip, right where people decide
    items = CFG['trust']
    tsz = 0.56
    gap = 0.95
    ir = 0.24
    widths = [F[SANS_M].width(t, tsz) for t in items]
    total = sum(widths) + len(items) * (2 * ir + 0.22) + gap * (len(items) - 1)
    if total > 20.6:
        tsz *= 20.6 / total
        widths = [F[SANS_M].width(t, tsz) for t in items]
        total = sum(widths) + len(items) * (2 * ir + 0.22) + gap * (len(items) - 1)
    x = CX - total / 2
    for t, w_ in zip(items, widths):
        check_icon(c, x + ir, TRUST_Y - tsz * 0.36, ir, gold)
        text(c, t, SANS_M, tsz, x + 2 * ir + 0.22, TRUST_Y, C4('cream', 0.95), align='left')
        x += 2 * ir + 0.22 + w_ + gap

    # 7. action: QR + call + walk-in direction
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, border=0)
    qr.add_data(CFG['qr'])
    qr.make(fit=True)
    mat = np.array(qr.get_matrix(), bool)
    n = mat.shape[0]
    mod = math.floor(4.15 / n * PPI) / PPI
    pad = 0.45
    q = n * mod + 2 * pad
    qx0 = round((SAFE + 0.05) * PPI) / PPI
    qy0 = round(QR_TOP * PPI) / PPI
    LAY['qr'] = (qx0, qy0, q, n, mod)
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(qx0, qy0, qx0 + q, qy0 + q), 0.26, 0.26), paint(C4('qr_tile')))
    qpath = skia.Path()
    for r_ in range(n):
        for c_ in range(n):
            if mat[r_, c_]:
                qpath.addRect(skia.Rect(qx0 + pad + c_ * mod, qy0 + pad + r_ * mod,
                                        qx0 + pad + (c_ + 1) * mod, qy0 + pad + (r_ + 1) * mod))
    c.drawPath(qpath, paint(C4('ink'), aa=False))
    rx = qx0 + q + 0.8
    rw = TW - SAFE - rx
    text(c, 'Scan or call to book', SANS_SB, 0.66, rx, qy0 + 0.95, C4('cream'), align='left')
    num = '+91 80764 67352'
    nsz = min(1.45, rw / F[SANS_B].width(num, 1))
    text(c, num, SANS_B, nsz, rx, qy0 + 0.95 + 0.50 + nsz * 0.80, C4('cream'), align='left')
    fy = qy0 + q - 0.06
    text(c, 'Or visit us directly at', SANS_SB, 0.50, rx, fy - 1.09, C4('cream', 0.9), align='left')
    aw = text(c, '↑', SANS_SB, 0.82, rx, fy + 0.02, gold, align='left')
    text(c, '2ND FLOOR, THIS BUILDING', SANS_SB, 0.60, rx + aw + 0.22, fy, gold, align='left', tracking=0.12)

    # fine print
    text(c, 'Posed by models. Scan imagery is illustrative. Free analysis during our launch month; T&C apply.',
         SANS_R, 0.335, CX, TH - SAFE - 0.22, C4('sage', 0.9))


# ================================================================ COMPOSE
vec = raster_layer(draw_vectors)
final = comp * (1 - vec[..., 3:4]) + vec[..., :3]
final8 = (np.clip(final, 0, 1) * 255 + 0.5).astype(np.uint8)
del vec, final
json.dump({'spot': SPOT, 'loupe': LAY['loupe'], 'qr': LAY['qr']}, open(f'{OUT}/side{SIDE}_layout.json', 'w'), indent=1)
Image.fromarray(crop_in(final8, 0)).resize((720, 1440), Image.LANCZOS).save(f'{OUT}/side{SIDE}_small.png')
print('compose done', SIDE, 'spot', tuple(round(v, 2) for v in SPOT), 'loupe spots', len(LOUPE_SPOTS), 'qr', LAY['qr'][3])
if os.environ.get('PREVIEW'):
    Image.fromarray(crop_in(final8, 0)).save(f'{OUT}/side{SIDE}_trim_preview.png')
    sys.exit(0)

# ================================================================ EXPORTS
TAG = f'LEEVORA_Standee_2x4ft_Side{SIDE}'
icc_bytes = open(ICC_CMYK, 'rb').read()
srgb_bytes = open(ICC_SRGB, 'rb').read()

SLUG = 0.75
pw, ph = TW + 2 * (BLEED + SLUG), TH + 2 * (BLEED + SLUG)
plate = Image.fromarray((np.clip(crop_in(comp, BLEED), 0, 1) * 255 + 0.5).astype(np.uint8))
buf = io.BytesIO()
plate.save(buf, 'JPEG', quality=97, subsampling=0, dpi=(PPI, PPI))
plate_img = skia.Image.MakeFromEncoded(skia.Data.MakeWithCopy(buf.getvalue()))
rgb_pdf = f'{OUT}/{TAG}_rgb_tmp.pdf'
stream = skia.FILEWStream(rgb_pdf)
doc = skia.PDF.MakeDocument(stream, Title=f'leevorá standee 2x4 ft Side {SIDE}', Creator='Adsworm', Producer='Adsworm')
pc = doc.beginPage(pw * 72, ph * 72)
pc.scale(72, 72)
pc.translate(SLUG + BLEED, SLUG + BLEED)
pc.save()
pc.clipRect(skia.Rect(-BLEED, -BLEED, TW + BLEED, TH + BLEED))
pc.drawImageRect(plate_img, skia.Rect(-BLEED, -BLEED, TW + BLEED, TH + BLEED), skia.SamplingOptions(skia.FilterMode.kLinear))
draw_vectors(pc)
pc.restore()
mk = paint(skia.Color4f(0, 0, 0, 1), stroke=0.25 / 72)
off, ln = BLEED + 0.12, 0.45
for (x, y) in ((0, 0), (TW, 0), (0, TH), (TW, TH)):
    sx, sy = (-1 if x == 0 else 1), (-1 if y == 0 else 1)
    pc.drawLine(x + sx * off, y, x + sx * (off + ln), y, mk)
    pc.drawLine(x, y + sy * off, x, y + sy * (off + ln), mk)
slug_p, _ = F[SANS_M].path(f'leevorá · 2 x 4 ft LED standee · SIDE {SIDE} · trim 610 x 1219 mm · bleed 10 mm · safe 40 mm · '
                           f'CMYK FOGRA39 · raster 150 ppi @ 100%', 0.16, 0, TH + BLEED + 0.42, 'left')
pc.drawPath(slug_p, paint(skia.Color4f(0, 0, 0, 1)))
doc.endPage()
doc.close()
del stream
cmyk_pdf = f'{OUT}/{TAG}_PRINT_CMYK.pdf'
subprocess.run(['gs', '-q', '-dSAFER', '-dBATCH', '-dNOPAUSE', '-sDEVICE=pdfwrite', '-dCompatibilityLevel=1.6',
                '-sColorConversionStrategy=CMYK', '-sProcessColorModel=DeviceCMYK',
                f'-sOutputICCProfile={ICC_CMYK}', f'-sDefaultRGBProfile={ICC_SRGB}', '-dRenderIntent=1', '-dBlackPtComp=1',
                '-dAutoFilterColorImages=false', '-dColorImageFilter=/DCTEncode',
                '-dDownsampleColorImages=false', '-dEncodeColorImages=true', f'-sOutputFile={cmyk_pdf}', '-c',
                '<< /ColorImageDict << /QFactor 0.08 /Blend 1 /HSamples [1 1 1 1] /VSamples [1 1 1 1] >> '
                '/ColorACSImageDict << /QFactor 0.08 /Blend 1 /HSamples [1 1 1 1] /VSamples [1 1 1 1] >> >> setdistillerparams',
                '-f', rgb_pdf], check=True)
os.remove(rgb_pdf)
pdf = pikepdf.open(cmyk_pdf, allow_overwriting_input=True)
pg = pdf.pages[0]
pt = lambda v: v * 72
pg.TrimBox = pikepdf.Array([pt(SLUG + BLEED), pt(SLUG + BLEED), pt(SLUG + BLEED + TW), pt(SLUG + BLEED + TH)])
pg.BleedBox = pikepdf.Array([pt(SLUG), pt(SLUG), pt(SLUG + 2 * BLEED + TW), pt(SLUG + 2 * BLEED + TH)])
icc_stream = pikepdf.Stream(pdf, icc_bytes)
icc_stream.N = 4
pdf.Root.OutputIntents = pikepdf.Array([pikepdf.Dictionary(
    Type=pikepdf.Name.OutputIntent, S=pikepdf.Name.GTS_PDFX, OutputConditionIdentifier='FOGRA39',
    Info='Coated FOGRA39 (ISO 12647-2:2004)', RegistryName='http://www.color.org', DestOutputProfile=icc_stream)])
pdf.save(cmyk_pdf)
pdf.close()

proof = None
for name, margin in (('PRINT_CMYK_10mm-bleed', BLEED), ('FLEX-WRAP_CMYK_75mm-extension', 75 / 25.4)):
    cm = ImageCms.applyTransform(Image.fromarray(crop_in(final8, margin)), to_cmyk)
    cm.save(f'{OUT}/{TAG}_{name}.tif', compression='tiff_adobe_deflate', dpi=(PPI, PPI), icc_profile=icc_bytes)
    if margin == BLEED:
        proof = ImageCms.applyTransform(cm, to_rgb)
        proof.save(f'{OUT}/{TAG}_softproof.png')
        tac = np.asarray(cm).astype(np.float32).sum(-1) / 2.55
        print('TAC max %.0f p99 %.0f' % (tac.max(), np.percentile(tac, 99)))
        del tac
    del cm
Image.fromarray(crop_in(final8, BLEED)).save(f'{OUT}/{TAG}_RIP-MASTER_sRGB_10mm-bleed.tif', compression='tiff_adobe_deflate',
                                             dpi=(PPI, PPI), icc_profile=srgb_bytes)

pr = np.asarray(proof).astype(np.float32) / 255
lin = pr ** 2.2
em = 1 - np.exp(-lin * 3.2)
night = np.clip(em + gblur(em ** 2, 0.25 * PPI) * 0.55 + gblur(em ** 2, 1.2 * PPI) * 0.35, 0, 1) ** (1 / 2.2)
Image.fromarray((night * 255).astype(np.uint8)).resize((900, round(900 * night.shape[0] / night.shape[1])), Image.LANCZOS) \
    .save(f'{OUT}/{TAG}_night_preview.jpg', quality=90)
proof.resize((900, round(900 * proof.height / proof.width)), Image.LANCZOS).save(f'{OUT}/{TAG}_day_preview.jpg', quality=90)

qx0, qy0, qs = LAY['qr'][:3]
qcrop = np.asarray(proof)[int((qy0 + BLEED - 0.3) * PPI):int((qy0 + BLEED + qs + 0.3) * PPI),
                          int((qx0 + BLEED - 0.3) * PPI):int((qx0 + BLEED + qs + 0.3) * PPI)]
det = cv2.QRCodeDetector()
for scale in (1.0, 0.30):
    q_ = cv2.resize(qcrop, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
    val, _, _ = det.detectAndDecode(cv2.cvtColor(q_, cv2.COLOR_RGB2BGR))
    print('QR scale', scale, 'OK' if val == CFG['qr'] else f'FAIL {val!r}')
print('exports done', SIDE)
