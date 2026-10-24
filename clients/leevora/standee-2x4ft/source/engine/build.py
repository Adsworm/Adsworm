#!/usr/bin/env python3
"""leevorá 2x4 ft LED standee — compositor (v2).

One scene definition renders to: raster plate (150 ppi), vector PDF (outlined type, 10 mm bleed,
crop marks) converted to CMYK FOGRA39, CMYK + sRGB TIFF masters, flex-wrap TIFF, a 1-bit 300 ppi
and day / lit-at-night previews.
Usage: build.py A|B
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
EXT = 3.0                      # canvas extension around trim (covers the 75 mm flex wrap)
TW, TH = 24.0, 48.0            # trim 610 x 1219 mm
BLEED = 10 / 25.4
SAFE = 40 / 25.4
LBL = 55 / 25.4                # HUD labels sit >= 55 mm from trim
CW, CH = TW + 2 * EXT, TH + 2 * EXT
W, H = round(CW * PPI), round(CH * PPI)
CX = TW / 2
MM = 1 / 25.4


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
        photo='hero/woman3.png', npz='hero/woman3.npz', face_w=9.6, scan='below', crown=-0.30,
        head=['Your mirror', 'only shows half.'], accent='half.',
        offer='Free Skin & Hair Analysis',
        proof='8-spectrum AI skin imaging  ·  17 concerns mapped  ·  Expert-led plan',
        tag='8-SPECTRUM SCAN',
        labels=[('UV DAMAGE', 'Hidden', 'aqua'), ('PIGMENTATION', 'Uneven', 'aqua')],
        qr=WA + 'Hi%21%20I%27d%20like%20my%20free%20skin%20analysis',
    ),
    'B': dict(
        photo='hero/man3.png', npz='hero/man3.npz', face_w=9.8, scan='above', crown=1.0,
        head=['Hair fall', 'has a reason.'], accent='reason.',
        offer='Free Hair & Skin Analysis',
        proof='Hair & scalp imaging  ·  Density mapped  ·  Expert-led plan',
        tag='SCALP SCAN',
        labels=[('TEMPLE DENSITY', 'Low', 'gold'), ('CROWN DENSITY', 'Normal', 'aqua')],
        qr=WA + 'Hi%21%20I%27d%20like%20my%20free%20hair%20analysis',
    ),
}[SIDE]

# type system (shared by both sides)
HS = 2.72                                  # headline size -> ~52 mm cap
Y_NOW, LOGO_TOP, LOGO_W = 2.55, 3.30, 9.6
HL1 = 7.38 + 0.75 * HS
HL2 = HL1 + 0.93 * HS
CROWN_Y = HL2 + CFG['crown']             # A: head overlaps line 2 (depth); B: wide head sits clear of it


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
        return img.toarray(colorType=skia.kAlpha_8_ColorType)
    return img.toarray(colorType=skia.kRGBA_8888_ColorType, alphaType=skia.kPremul_AlphaType).astype(np.float32) / 255


# ================================================================ RASTER PLATE
P = np.load(f'{ROOT}/{CFG["npz"]}')
pts = P['pts'][:, :2].astype(np.float64)
src = cv2.imread(f'{ROOT}/{CFG["photo"]}', cv2.IMREAD_COLOR)[..., ::-1].astype(np.float32) / 255
sh, sw = src.shape[:2]

fg_src = P['fg'].astype(np.float32)
cxs = int(pts[1, 0])
crown_src = int(np.argmax((fg_src[:, cxs - 300:cxs + 300] > 0.5).any(1)))
s = CFG['face_w'] * PPI / np.linalg.norm(pts[454] - pts[234])
tx = px(CX) - s * pts[1, 0]
ty = px(CROWN_Y) - s * crown_src
M = np.float32([[s, 0, tx], [0, s, ty]])


def warp(a):
    return cv2.warpAffine(a, M, (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_CONSTANT, borderValue=0)


def T(i):
    return pts[i] * s + np.array([tx, ty])


def Ti(i):
    p = T(i) / PPI - EXT
    return float(p[0]), float(p[1])


photo = warp(src).clip(0, 1)
fg = warp(fg_src).clip(0, 1)
hair = warp(P['hair'].astype(np.float32)).clip(0, 1)
facem = warp(P['face'].astype(np.float32)).clip(0, 1)
valid = gblur(warp(np.ones((sh, sw), np.float32)), 0.25 * PPI)       # feather the photo's own frame edge
del src, fg_src

ys = (np.arange(H, dtype=np.float32)[:, None] / PPI - EXT)
xs = (np.arange(W, dtype=np.float32)[None, :] / PPI - EXT)
chin_y = Ti(152)[1]
eye_y = (Ti(468)[1] + Ti(473)[1]) / 2

# --- brand background
d = np.sqrt(((xs - CX) / 15.0) ** 2 + ((ys - (eye_y - 1.5)) / 17.0) ** 2)
tb = smooth(0.0, 1.25, d)[..., None]
bg = lerp(hx(PAL['bg_core']), hx(PAL['bg_mid']), np.clip(tb * 1.6, 0, 1))
bg = lerp(bg, hx(PAL['bg_edge']), np.clip(tb * 1.6 - 0.6, 0, 1))
bg = bg * (1 - 0.15 * smooth(32, 50, ys))[..., None]
del d, tb

# --- portrait grade: soft and true. Gentle lift in the shadows, gentle shoulder on the top highlights only
lum = photo @ np.float32([0.2126, 0.7152, 0.0722])
graded = photo + (1 - photo) * 0.06 * (1 - smooth(0.0, 0.5, lum))[..., None]     # open shadows, lower contrast
gl = graded @ np.float32([0.2126, 0.7152, 0.0722])
knee = 0.76
roll = np.where(gl > knee, (knee + (gl - knee) * 0.55) / np.maximum(gl, 1e-4), 1.0)
graded *= roll[..., None]
del gl, roll

# --- matte: core segmentation + luminance key at the edge so real flyaways survive
ring_m = (cv2.dilate((fg > 0.3).astype(np.uint8), np.ones((int(0.6 * PPI),) * 2, np.uint8)) > 0) & (fg < 0.02) & (valid > 0.99)
bgc = np.median(photo[ring_m], axis=0)
key = smooth(0.06, 0.17, np.linalg.norm(gblur(photo, 0.8) - bgc, axis=-1))
del ring_m
# inside the hair region, backdrop showing through thin hair becomes transparent (colour key), strands stay
core = np.clip(fg * (1 - hair * (1 - key)), 0, 1) if SIDE == 'B' else fg      # B: thin hair over a mid-green backdrop
a_e = np.clip(core, 0.04, 1)[..., None]
dec = np.clip((photo - (1 - a_e) * bgc) / a_e, 0, 1)
edge_w = ((a_e[..., 0] > 0.04) & (a_e[..., 0] < 0.97)).astype(np.float32)[..., None]
graded = lerp(graded, dec + (1 - dec) * 0.0, edge_w)
del a_e, dec, edge_w
alpha_p = np.clip(gblur(core, 0.6), 0, 1)
# body fades evenly (elliptical, no horizontal shelf), photo frame edges feathered
r = np.sqrt(((xs - CX) / 10.5) ** 2 + ((ys - (chin_y - 2.5)) / 6.8) ** 2)
fade = 1 - smooth(0.78, 1.18, r)
fade = np.where(ys < chin_y - 2.5, 1 - smooth(9.6, 11.6, np.abs(xs - CX)), fade)
alpha = (alpha_p * fade * valid).clip(0, 1)
del key, r, core

# light wrap: background bleeds 3 mm into the subject edge so it sits in the scene
wrap = (alpha * (1 - gblur(alpha, 0.045 * PPI))).clip(0, 1)[..., None] * 1.6
comp = lerp(bg, graded, alpha[..., None])
comp = lerp(comp, gblur(bg, 0.05 * PPI) * 1.15 + hx(PAL['aqua']) * 0.04, np.clip(wrap, 0, 0.6))
del wrap

# --- scan geometry
eyes_low = max(Ti(145)[1], Ti(374)[1])
if CFG['scan'] == 'below':
    beam_y = eyes_low + 0.42 * (Ti(1)[1] - eyes_low)
    reg = smooth(beam_y, beam_y + 0.02, ys) * np.ones_like(xs)
else:
    beam_y = min(Ti(105)[1], Ti(334)[1]) - 0.55
    reg = (1 - smooth(beam_y - 0.02, beam_y, ys)) * np.ones_like(xs)
reg_person = reg * alpha


def poly_mask(idx, dil_in=0.0):
    m = np.zeros((H, W), np.uint8)
    cv2.fillPoly(m, [cv2.convexHull(np.array([T(i) for i in idx], np.int32))], 1)
    if dil_in:
        m = cv2.dilate(m, np.ones((int(dil_in * PPI),) * 2, np.uint8))
    return m


LIPS = (61, 40, 37, 0, 267, 270, 291, 321, 314, 17, 84, 91)
NOSE = (129, 98, 97, 2, 326, 327, 358, 279, 49, 48, 64, 294, 278)
OVAL = (10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288, 397, 365, 379, 378, 400, 377, 152,
        148, 176, 149, 150, 136, 172, 58, 132, 93, 234, 127, 162, 21, 54, 103, 67, 109)
markers, hairline, TEMPLES = [], [], []

if SIDE == 'A':
    # bright scanner view: the real skin in clean aqua light, pigment spots gently deepened
    uv = photo @ np.float32([0.10, 0.30, 0.60])
    ov = np.zeros((H, W), np.uint8)
    cv2.fillPoly(ov, [np.array([T(i) for i in OVAL], np.int32)], 1)
    inner = cv2.erode(ov, np.ones((int(0.6 * PPI),) * 2, np.uint8)).astype(np.float32)
    lipz = poly_mask(LIPS, 0.9).astype(np.float32)
    nosez = poly_mask(NOSE, 0.7).astype(np.float32)
    mouth_y = (Ti(61)[1] + Ti(291)[1]) / 2
    zone = inner * (1 - lipz) * (1 - nosez) * (ys > beam_y + 0.3) * (ys < mouth_y - 0.1)
    bridge = (np.abs(xs - Ti(6)[0]) < 0.45) * (ys > beam_y + 0.05) * (ys < Ti(4)[1] - 0.25)
    zone = gblur(np.clip(zone + bridge * inner, 0, 1).astype(np.float32), 0.08 * PPI)
    dog = gblur(uv, 0.03 * PPI) - gblur(uv, 0.12 * PPI)
    gsk = gblur(graded @ np.float32([0.2126, 0.7152, 0.0722]), 0.8)
    aquav = gsk[..., None] * np.float32([0.60, 1.0, 0.97]) * 1.18 + np.float32([0.0, 0.04, 0.05])
    aquav -= (np.clip(-dog, 0, 0.12) * 2.4 * zone)[..., None] * np.float32([0.45, 0.75, 0.75])
    scan = lerp(graded, np.clip(aquav, 0, 1), 0.78)
    strength = 0.95 - 0.45 * smooth(chin_y - 0.4, chin_y + 3.0, ys)
    comp = lerp(comp, scan, (reg_person * strength)[..., None])
    del aquav, scan, gsk, strength
    # markers: strongest pigment spots inside the zone, at least one per cheek
    zx = (xs > Ti(234)[0] + 1.8) & (xs < Ti(454)[0] - 1.8)
    score = np.where((zone > 0.5) & zx, -dog, 0)
    mx = cv2.dilate(score, np.ones((int(0.6 * PPI),) * 2, np.uint8))
    cand = sorted(np.argwhere((score == mx) & (score > 0.004)), key=lambda p: -score[p[0], p[1]])
    pts_all = [(xv / PPI - EXT, yv / PPI - EXT) for yv, xv in cand]
    right, left = [], []
    for p in pts_all:                       # labels live on the open right side: two spots there, one on the left
        bucket, need = (right, 2) if p[0] > Ti(1)[0] + 0.6 else (left, 1)
        if len(bucket) < need and all(math.dist(p, q) > 0.8 for q in right + left):
            bucket.append(p)
    markers = right + left
    del uv, dog, score, mx, zone, ov, inner, lipz, nosez
else:
    # hair: the real photo in scanner light (teal tint) + two-tone density map (gold = thin, teal = dense)
    fx0, fx1 = Ti(234)[0] + 0.6, Ti(454)[0] - 0.6
    for xv in np.linspace(fx0, fx1, 60):
        hairline.append((float(xv), np.argmax(facem[:, int(px(xv))] > 0.5) / PPI - EXT))
    hl = sorted(hairline)
    n3 = len(hl) // 3
    lt, rt = max(hl[:n3], key=lambda q: q[1]), max(hl[-n3:], key=lambda q: q[1])
    TEMPLES = [(lt[0] + 0.2, lt[1] - 0.45), (rt[0] - 0.2, rt[1] - 0.45)]
    gl = gblur(comp @ np.float32([0.2126, 0.7152, 0.0722]), 0.8)
    teal = gl[..., None] * np.float32([0.50, 1.0, 1.0]) * 1.22 + np.float32([0.0, 0.04, 0.05])
    skin_w = np.clip(1 - gblur(hair, 0.25 * PPI) * 1.1, 0, 1)
    tinted = lerp(comp, np.clip(teal, 0, 1), (0.22 + 0.36 * skin_w)[..., None])
    tinted = lerp(tinted, tinted * np.float32([0.78, 0.96, 1.0]), (hair * 0.9)[..., None])
    del skin_w
    dark = (1 - smooth(0.05, 0.45, lum)) * hair
    dens = gblur(dark, 0.4 * PPI)
    dmax = np.percentile(dens[(hair > 0.5) & (ys < beam_y)], 95)
    densn = np.clip(dens / (dmax + 1e-6), 0, 1)
    warm = np.zeros((H, W), np.float32)
    for (qx, qy) in TEMPLES:
        warm += np.exp(-(((xs - qx) / 1.2) ** 2 + ((ys - qy) / 0.9) ** 2))
    warm = np.clip(warm, 0, 1)
    cool = gblur(hair * densn, 0.05 * PPI) * (1 - warm) * alpha
    screen = lambda a, b: 1 - (1 - a) * (1 - b)
    tinted = lerp(tinted, tinted * 0.5 + hx(PAL['gold']) * 0.6, (warm * 0.7)[..., None])
    comp = lerp(comp, tinted, reg_person[..., None])
    hl_mid = hl[len(hl) // 2]
    zone = (hair > 0.6) & (xs > CX + 0.8) & (xs < CX + 3.4) & (ys > CROWN_Y + 0.5) & (ys < hl_mid[1] - 0.2)
    sc = np.where(zone, densn, -1)
    iy, ix = np.unravel_index(np.argmax(gblur(sc.astype(np.float32), 0.15 * PPI)), sc.shape)
    CROWN_PT = (ix / PPI - EXT, iy / PPI - EXT)
    del zone, sc
    markers = [TEMPLES[0], CROWN_PT]
    del gl, teal, tinted, dark, dens, densn, warm, cool

# light spill from the beam onto the skin
dist = (ys - beam_y) if CFG['scan'] == 'below' else (beam_y - ys)
lead = np.exp(-np.clip(dist, 0, None) / 0.55) * (dist >= 0)
spill = np.exp(-np.clip(-dist, 0, None) / 0.30) * (dist < 0)
aq = hx(PAL['aqua'])
comp += (aq * 0.14)[None, None, :] * (lead * alpha)[..., None]
comp += (aq * 0.08)[None, None, :] * (spill * alpha)[..., None]
del lead, spill, dist


# beam glow (raster part; the crisp core is vector)
def draw_beam(c):
    for wdt, a in ((0.9, 0.10), (0.36, 0.22), (0.12, 0.55)):
        c.drawRect(skia.Rect(-EXT, beam_y - wdt / 2, TW + EXT, beam_y + wdt / 2), paint(C4('aqua', a)))


beam = gblur(raster_layer(draw_beam), 0.16 * PPI)
taper = (0.55 + 0.45 * np.exp(-((xs - CX) / 9.0) ** 2))[..., None]
comp = comp + beam[..., :3] * taper * 1.25
del beam

rng = np.random.default_rng(7)
comp = np.clip(comp + gblur(rng.normal(0, 1, (H, W)).astype(np.float32), 0.5)[..., None] * 0.010, 0, 1)

# occluder for the headline: the head in front of the type (only above the eyes)
occ = ((alpha > 0.5) & (ys < eye_y - 2.0)).astype(np.uint8)
cnts, _ = cv2.findContours(occ, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
OCC = skia.Path()
for cn in cnts:
    if cv2.contourArea(cn) < 2000:
        continue
    cn = cv2.approxPolyDP(cn, 1.0, True)[:, 0, :] / PPI - EXT
    OCC.moveTo(*cn[0])
    for q in cn[1:]:
        OCC.lineTo(*q)
    OCC.close()
del occ

# ================================================================ VECTORS
F = {n: Font.get(n) for n in (SERIF, SANS_B, SANS_SB, SANS_M, SANS_R)}


def text(c, s_, font, size, x, y, color, align='center', tracking=0.0):
    p, w = F[font].path(s_, size, x, y, align, tracking)
    c.drawPath(p, paint(color))
    return w


def hud_label(c, name, val, col, sd, ly, mxv, myv, ring_r=0.17):
    lx = LBL if sd == 'L' else TW - LBL
    al = 'left' if sd == 'L' else 'right'
    accent = C4(col)
    text(c, name, SANS_SB, 0.44, lx, ly - 0.95, accent, align=al, tracking=0.14)
    vw = text(c, val, SERIF, 0.95, lx, ly + 0.10, C4('cream'), align=al)
    sg = 1 if sd == 'L' else -1
    ex_ = lx + sg * (vw + 0.28)
    ly0 = ly - 0.22
    path = skia.Path()
    path.moveTo(ex_, ly0)
    elbow = mxv - sg * 0.8
    if sg * (elbow - ex_) < 0.3:
        elbow = ex_ + sg * 0.3
    path.lineTo(elbow, ly0)
    ang = math.atan2(myv - ly0, mxv - elbow)
    path.lineTo(mxv - ring_r * math.cos(ang), myv - ring_r * math.sin(ang))
    c.drawPath(path, paint(C4(col, 0.9), stroke=0.028))
    c.drawCircle(ex_, ly0, 0.055, paint(accent))


LOGO = json.load(open(f'{ROOT}/engine/leevora_logo.json'))
LOGO_COL = '#%02X%02X%02X' % tuple(round(v * 255) for v in LOGO['color'])


def logo_path(parts, sc, ox, oy):
    p = skia.Path()
    for f in parts:
        for sp in f['path']:
            for seg in sp:
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
    ox = cx - width / 2
    for part in ('word', 'desc'):
        c.drawPath(logo_path(LOGO[part], sc, ox, top), paint(C4(LOGO_COL)))
    return top + LOGO['h'] * sc


LAY = {}


def draw_vectors(c):
    gold = C4('gold')
    # lockup
    nw = text(c, 'NOW OPEN', SANS_B, 0.90, CX, Y_NOW, gold, tracking=0.24)
    rl = paint(C4('gold', 0.9), stroke=0.032)
    for sg in (-1, 1):
        c.drawLine(CX + sg * (nw / 2 + 0.55), Y_NOW - 0.32, CX + sg * (nw / 2 + 3.4), Y_NOW - 0.32, rl)
    draw_logo(c, CX, LOGO_TOP, LOGO_W)

    # headline, line 2 sits behind the head
    l1, l2 = CFG['head']
    text(c, l1, SERIF, HS, CX, HL1, C4('cream'))
    c.save()
    c.clipPath(OCC, skia.ClipOp.kDifference, True)
    acc = CFG['accent']
    pre = l2[:-len(acc)]
    x0_ = CX - F[SERIF].width(l2, HS) / 2
    text(c, pre, SERIF, HS, x0_, HL2, C4('cream'), align='left')
    text(c, acc, SERIF, HS, x0_ + F[SERIF].width(pre, HS), HL2, C4('aqua'), align='left')
    c.restore()

    # beam core + tag (same place on both sides: left, just above the beam)
    c.drawRect(skia.Rect(-BLEED, beam_y - 0.024, TW + BLEED, beam_y + 0.024), paint(C4('aqua_hot')))
    tgw = text(c, CFG['tag'], SANS_SB, 0.34, TW - LBL, beam_y - 0.30, C4('aqua'), align='right', tracking=0.18)
    c.drawCircle(TW - LBL - tgw - 0.24, beam_y - 0.30 - 0.12, 0.075, paint(C4('aqua')))

    # rings + two labels
    for i, m in enumerate(markers):
        col = 'gold' if (SIDE == 'B' and i == 0) else 'aqua_hot'
        c.drawCircle(m[0], m[1], 0.17, paint(C4(col, 0.95), stroke=0.04))
        if SIDE == 'B' and i == 0:
            c.drawCircle(m[0], m[1], 0.45, paint(C4('gold', 0.55), stroke=0.025))
    (n1, v1, c1), (n2, v2, c2) = CFG['labels']
    if SIDE == 'A':
        rms = sorted([m for m in markers if m[0] > CX], key=lambda m: m[1])[:2]
        y_a = max(rms[0][1] + 0.6, beam_y + 1.45)
        hud_label(c, n1, v1, c1, 'R', y_a, *rms[0])
        hud_label(c, n2, v2, c2, 'R', max(rms[-1][1] + 2.2, y_a + 2.3), *rms[-1])
    else:
        hud_label(c, n1, v1, c1, 'L', TEMPLES[0][1] + 0.2, *TEMPLES[0])
        hud_label(c, n2, v2, c2, 'R', markers[1][1] + 0.9, *markers[1])

    # offer + urgency
    oy = 34.75
    osz = 17.4 / F[SERIF].width(CFG['offer'], 1)
    text(c, CFG['offer'], SERIF, osz, CX, oy, gold)
    text(c, 'LAUNCH MONTH ONLY', SANS_SB, 0.66, CX, oy + 1.30, gold, tracking=0.22)
    fr = skia.Rect(CX - 10.0, oy - osz * 0.75 - 0.62, CX + 10.0, oy + 1.30 + 0.62)
    LAY['offer_frame'] = (fr.left(), fr.top(), fr.right(), fr.bottom())
    c.drawRRect(skia.RRect.MakeRectXY(fr, 1.0, 1.0), paint(C4('gold', 0.95), stroke=0.045))

    # proof line
    psz = min(0.575, 19.0 / F[SANS_M].width(CFG['proof'], 1))
    text(c, CFG['proof'], SANS_M, psz, CX, 37.95, C4('cream', 0.9))

    # CTA: QR (modules snapped to the pixel grid) + one label + one number
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, border=0)
    qr.add_data(CFG['qr'])
    qr.make(fit=True)
    mat = np.array(qr.get_matrix(), bool)
    n = mat.shape[0]
    mod = math.floor(4.15 / n * PPI) / PPI
    pad = 0.45
    q = n * mod + 2 * pad
    qx0 = round((SAFE + 0.05) * PPI) / PPI
    qy0 = round(39.30 * PPI) / PPI
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
    LAY['num'] = (rx, nsz)
    # walk-in line + wayfinding, last line aligned to the bottom of the QR tile
    fy = qy0 + q - 0.06
    text(c, 'Or visit us directly at', SANS_SB, 0.50, rx, fy - 1.09, C4('cream', 0.9), align='left')
    aw = text(c, '↑', SANS_SB, 0.82, rx, fy + 0.02, gold, align='left')
    text(c, '2ND FLOOR, THIS BUILDING', SANS_SB, 0.60, rx + aw + 0.22, fy, gold, align='left', tracking=0.12)

    # fine print (>= 6 mm cap, lifted clear of the safe line)
    text(c, 'Posed by models. Scan imagery is illustrative. Free analysis during our launch month; T&C apply.',
         SANS_R, 0.335, CX, TH - SAFE - 0.22, C4('sage', 0.9))


# ================================================================ COMPOSE
vec = raster_layer(draw_vectors)
final = comp * (1 - vec[..., 3:4]) + vec[..., :3]
final8 = (np.clip(final, 0, 1) * 255 + 0.5).astype(np.uint8)
del vec, final


def crop_in(arr, margin, ppi=PPI, ext=EXT):
    b0 = int(round((ext - margin) * ppi))
    return arr[b0:arr.shape[0] - b0, b0:arr.shape[1] - b0]


json.dump({'beam_y_in': beam_y, 'markers': markers, 'lay': {k: list(map(float, np.ravel(v))) for k, v in LAY.items()}},
          open(f'{OUT}/side{SIDE}_layout.json', 'w'), indent=1)
Image.fromarray(crop_in(final8, 0)).resize((720, 1440), Image.LANCZOS).save(f'{OUT}/side{SIDE}_small.png')
print('compose done', SIDE, 'beam', round(beam_y, 2), 'markers', [tuple(round(v, 2) for v in m) for m in markers],
      'qr', LAY['qr'][3], 'modules', round(LAY['qr'][4] * 25.4, 2), 'mm')

if os.environ.get('PREVIEW'):
    Image.fromarray(crop_in(final8, 0)).save(f'{OUT}/side{SIDE}_trim_preview.png')
    sys.exit(0)

# ================================================================ EXPORTS
TAG = f'LEEVORA_Standee_2x4ft_Side{SIDE}'
icc_bytes = open(ICC_CMYK, 'rb').read()
srgb_bytes = open(ICC_SRGB, 'rb').read()

# --- 1. vector PDF -> CMYK FOGRA39 via Ghostscript, Trim/Bleed boxes + output intent via pikepdf
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
                           f'CMYK FOGRA39 · raster 150 ppi @ 100% · neon/scan line {round(beam_y * 25.4)} mm from top trim',
                           0.16, 0, TH + BLEED + 0.42, 'left')
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

# --- 2. flattened TIFFs: CMYK (10 mm bleed), CMYK flex wrap (75 mm), sRGB master for RIPs with a media profile
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

# --- 3. previews: day (soft proof) and lit at night (whole sheet backlit)
pr = np.asarray(proof).astype(np.float32) / 255
lin = pr ** 2.2


def night(lin_, blocked):
    tr = lin_ * (1 - 0.95 * blocked[..., None]) if blocked is not None else lin_
    em = 1 - np.exp(-tr * 3.2)
    bloom = gblur(em ** 2, 0.25 * PPI) * 0.55 + gblur(em ** 2, 1.2 * PPI) * 0.35
    return np.clip(em + bloom, 0, 1) ** (1 / 2.2)


for nm, arr in (('night', night(lin, None)),):
    Image.fromarray((arr * 255).astype(np.uint8)).resize((900, round(900 * arr.shape[0] / arr.shape[1])), Image.LANCZOS) \
        .save(f'{OUT}/{TAG}_{nm}_preview.jpg', quality=90)
proof.resize((900, round(900 * proof.height / proof.width)), Image.LANCZOS).save(f'{OUT}/{TAG}_day_preview.jpg', quality=90)

# --- 4. QR check on the soft proof: full size and a phone at ~1.5 m
qx0, qy0, qs = LAY['qr'][:3]
qcrop = np.asarray(proof)[int((qy0 + BLEED - 0.3) * PPI):int((qy0 + BLEED + qs + 0.3) * PPI),
                          int((qx0 + BLEED - 0.3) * PPI):int((qx0 + BLEED + qs + 0.3) * PPI)]
det = cv2.QRCodeDetector()
for scale in (1.0, 0.30):
    q_ = cv2.resize(qcrop, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
    val, _, _ = det.detectAndDecode(cv2.cvtColor(q_, cv2.COLOR_RGB2BGR))
    print('QR scale', scale, 'OK' if val == CFG['qr'] else f'FAIL {val!r}')
print('exports done', SIDE)
