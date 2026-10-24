#!/usr/bin/env python3
"""leevorá 2x4 ft LED standee — compositor.

One scene definition renders to: raster master (150 ppi, 75 mm extension), vector PDF
(outlined type, 10 mm bleed), CMYK PDF/TIFF (FOGRA39), blockout mask, previews.
Usage: build.py A|B
"""
import sys, os, io, math, json
import numpy as np, cv2, skia, qrcode
from PIL import Image, ImageCms

ROOT = '/tmp/claude-0/-home-user-Adsworm/3d8d5e5a-8f36-56e6-be63-644bad3ee2df/scratchpad'
sys.path.insert(0, f'{ROOT}/engine')
from typeset import Font
from mediapipe.tasks.python.vision.face_landmarker import FaceLandmarksConnections as FLC

SIDE = sys.argv[1] if len(sys.argv) > 1 else 'A'
OUT = f'{ROOT}/out'
os.makedirs(OUT, exist_ok=True)

# ---------------------------------------------------------------- geometry
PPI = 150
EXT = 3.0                      # canvas extension around trim (covers 75 mm flex wrap)
TW, TH = 24.0, 48.0            # trim, inches (610 x 1219 mm)
BLEED = 10 / 25.4              # 10 mm
SAFE = 40 / 25.4               # 40 mm
CW, CH = TW + 2 * EXT, TH + 2 * EXT
W, H = round(CW * PPI), round(CH * PPI)
CX = TW / 2


def px(v):                      # trim inches -> canvas px
    return (v + EXT) * PPI


# ---------------------------------------------------------------- palette (sRGB)
def hx(h):
    return np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)], np.float32) / 255


PAL = dict(
    bg_core='#163A33', bg_mid='#0E2723', bg_edge='#07171A',
    cream='#FBF3E4', cream_dim='#D9D3C6', gold='#E4BA6E', gold_deep='#B8914B', qr_tile='#E3DDCF',
    aqua='#79C8CF', aqua_hot='#E2F2F3', aqua_deep='#0B4D52', sage='#A3B7AD',
    ink='#0D2622',
)


def C4(name, a=1.0):
    r, g, b = hx(PAL[name]) if name in PAL else hx(name)
    return skia.Color4f(float(r), float(g), float(b), a)


SERIF = 'Gloock-Regular'
SANS_B, SANS_SB, SANS_M, SANS_R = (f'InstrumentSans-{w}' for w in ('Bold', 'SemiBold', 'Medium', 'Regular'))

# ---------------------------------------------------------------- side config
WA = 'https://wa.me/918076467352?text=' + 'Hi%2C%20I%27d%20like%20to%20book%20my%20free%20skin%20%26%20hair%20analysis.'
CFG = {
    'A': dict(
        photo='hero/v1_1.png', npz='hero/woman.npz',
        face_w=10.0, eye_y=20.35, scan='below',
        head=['Your mirror', 'only shows half.'], accent_word='half.',
        offer='Free Skin & Hair Analysis',
        proof=[('See it', '8-light AI imaging'), ('Measure it', '17 skin concerns'), ('Treat it', 'Expert-led plan')],
        tag='8-LIGHT SKIN SCAN',
        labels=[('PIGMENTATION', '34'), ('PORES', '52'), ('UV SPOTS', '27'), ('TEXTURE', '46')],
    ),
    'B': dict(
        photo='hero/up_man.png', npz='hero/man.npz',
        face_w=9.2, eye_y=22.6, scan='above',
        head=['Hair fall', 'has a reason.'], accent_word='reason.',
        offer='Free Hair & Skin Analysis',
        proof=[('See it', 'Hair & scalp imaging'), ('Measure it', 'Density & thickness'), ('Treat it', 'Expert-led plan')],
        tag='HAIR & SCALP SCAN',
        labels=[('FOLLICLE DENSITY', '138/cm²'), ('TEMPLE DENSITY', '104/cm²'), ('THIN HAIRS', '24%')],
    ),
}[SIDE]

# ---------------------------------------------------------------- helpers
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


def surface_to_np(surf):
    """skia RGBA premul surface -> float32 premultiplied rgba."""
    img = surf.makeImageSnapshot()
    arr = img.toarray(colorType=skia.kRGBA_8888_ColorType, alphaType=skia.kPremul_AlphaType)
    return arr.astype(np.float32) / 255


def raster_layer(draw_fn):
    """Draw with a canvas in trim-inch coordinates on a full-canvas raster; return premul rgba."""
    surf = skia.Surface(W, H)
    c = surf.getCanvas()
    c.clear(skia.Color4f(0, 0, 0, 0))
    c.scale(PPI, PPI)
    c.translate(EXT, EXT)
    draw_fn(c)
    return surface_to_np(surf)


def paint(color, stroke=None, aa=True):
    p = skia.Paint(AntiAlias=aa, Color4f=color)
    if stroke:
        p.setStyle(skia.Paint.kStroke_Style)
        p.setStrokeWidth(stroke)
        p.setStrokeCap(skia.Paint.kRound_Cap)
    return p


# ================================================================ RASTER: background + photo + scan
P = np.load(f'{ROOT}/{CFG["npz"]}')
pts = P['pts'][:, :2].astype(np.float64)
src = cv2.imread(f'{ROOT}/{CFG["photo"]}', cv2.IMREAD_COLOR)[..., ::-1].astype(np.float32) / 255

face_w_src = np.linalg.norm(pts[454] - pts[234])
eye_src = (pts[468] + pts[473]) / 2
s = CFG['face_w'] * PPI / face_w_src
tx = px(CX) - s * eye_src[0]
ty = px(CFG['eye_y']) - s * eye_src[1]
M = np.float32([[s, 0, tx], [0, s, ty]])


def warp(a, interp=cv2.INTER_CUBIC):
    return cv2.warpAffine(a, M, (W, H), flags=interp, borderMode=cv2.BORDER_CONSTANT, borderValue=0)


def T(i):                       # landmark i -> canvas px
    return pts[i] * s + np.array([tx, ty])


def Ti(i):                      # landmark -> trim inches
    p = T(i) / PPI - EXT
    return float(p[0]), float(p[1])


photo = warp(src)
fg = warp(P['fg'].astype(np.float32)).clip(0, 1)
hair = warp(P['hair'].astype(np.float32)).clip(0, 1)
facem = warp(P['face'].astype(np.float32)).clip(0, 1)
del src

ys = (np.arange(H, dtype=np.float32)[:, None] / PPI - EXT)    # trim inches, column vector
xs = (np.arange(W, dtype=np.float32)[None, :] / PPI - EXT)

# --- brand background: deep bottle-green, light pooled behind the head, darker toward base
face_c = np.array(Ti(1))
d = np.sqrt(((xs - CX) / 15.0) ** 2 + ((ys - (CFG['eye_y'] - 1.5)) / 17.0) ** 2)
tb = smooth(0.0, 1.25, d)[..., None]
bg = lerp(hx(PAL['bg_core']), hx(PAL['bg_mid']), np.clip(tb * 1.6, 0, 1))
bg = lerp(bg, hx(PAL['bg_edge']), np.clip(tb * 1.6 - 0.6, 0, 1))
bg = bg * (1 - 0.18 * smooth(30, 50, ys))[..., None]
del d, tb

# --- portrait grade: keep it true, nudge shadows into the brand green, slight lift for backlight
lum = photo @ np.float32([0.2126, 0.7152, 0.0722])
shadow = (1 - smooth(0.0, 0.35, lum))[..., None]
graded = lerp(photo, photo * 0.6 + hx(PAL['bg_mid']) * 0.4, shadow * 0.35)
graded = np.clip(graded * 1.04, 0, 1) ** 0.96

# fade the body into darkness below the chin; keep shoulders soft
chin_y = Ti(152)[1]
fade = (1 - smooth(chin_y + 0.8, chin_y + 4.6, ys)) * np.ones_like(xs)
fade *= 1 - smooth(9.5, 12.5, np.abs(xs - CX))
alpha = (fg * fade)[..., None]
comp = lerp(bg, graded, alpha)
del graded

# --- scan region
eyes_low = max(Ti(145)[1], Ti(374)[1])
if CFG['scan'] == 'below':
    beam_y = eyes_low + 0.42 * (Ti(1)[1] - eyes_low)
    reg = smooth(beam_y, beam_y + 0.02, ys) * np.ones_like(xs)
else:
    brow = min(Ti(105)[1], Ti(334)[1])
    beam_y = brow - 0.55
    reg = (1 - smooth(beam_y - 0.02, beam_y, ys)) * np.ones_like(xs)
reg_person = reg * alpha[..., 0]

# UV-style view: melanin absorbs blue, so blue-weighted luminance + local contrast reveals spots/pores
uv = photo @ np.float32([0.10, 0.30, 0.60])
y0, y1 = int(px(4)), int(px(36))
x0, x1 = int(px(1)), int(px(23))
crop = (np.clip(gblur(uv[y0:y1, x0:x1], 1.2), 0, 1) * 255).astype(np.uint8)
cl = cv2.createCLAHE(clipLimit=1.9, tileGridSize=(10, 10)).apply(crop).astype(np.float32) / 255
base = gblur(cl, 2.0)
band = base - gblur(cl, 11)            # mid-frequency: spots + pores, not sensor noise
v = np.clip(base * 0.95 + band * 1.05 + 0.03, 0, 1)
uvv = np.zeros_like(uv)
uvv[y0:y1, x0:x1] = v
lipm = np.zeros((H, W), np.uint8)
cv2.fillPoly(lipm, [cv2.convexHull(np.array([T(i) for i in (61, 40, 37, 0, 267, 270, 291, 321, 314, 17, 84, 91)], np.int32))], 1)
lipm = gblur(cv2.dilate(lipm, np.ones((9, 9), np.uint8)).astype(np.float32), 6)
uvv = lerp(uvv, gblur(uvv, 7) * 0.85, lipm)
del lipm
del cl, band, base, crop

# hologram duotone: mostly deep teal, detail and form-light glow aqua
t1 = np.clip(uvv, 0, 1)
gx = cv2.Sobel(gblur(t1, 4.0), cv2.CV_32F, 1, 0, ksize=3)
gy = cv2.Sobel(gblur(t1, 4.0), cv2.CV_32F, 0, 1, ksize=3)
edge = np.clip(np.sqrt(gx * gx + gy * gy) * 3.0, 0, 1)
del gx, gy
tt = np.clip(t1 ** 1.75 * 1.0 + edge * 0.30, 0, 1)[..., None]
duo = lerp(hx('#020D0E'), hx('#0A4C50'), np.clip(tt * 2.0, 0, 1))
duo = lerp(duo, hx('#8FF0E6'), np.clip(tt * 2.0 - 1.0, 0, 1))
# faint scan lines (0.045 in period)
period = 0.045 * PPI
yl = np.arange(H, dtype=np.float32)[:, None]
lines = 1 - 0.09 * (np.sin(2 * np.pi * yl / period) > 0.55)
duo *= lines[..., None]
del t1, tt, edge

hairline = []
if SIDE == 'B':
    # hairline = top edge of the face-skin mask across the forehead
    fx0, fx1 = Ti(234)[0] + 0.6, Ti(454)[0] - 0.6
    for xv in np.linspace(fx0, fx1, 60):
        col = facem[:, int(px(xv))]
        hairline.append((float(xv), np.argmax(col > 0.5) / PPI - EXT))
    # density: how much dark hair sits in a 1 in neighbourhood
    dark = (1 - smooth(0.05, 0.45, lum)) * hair
    dens = gblur(dark, 0.45 * PPI)
    dmax = np.percentile(dens[(hair > 0.5) & (ys < beam_y)], 95)
    densn = np.clip(dens / (dmax + 1e-6), 0, 1)
    del dark, dens
    # strands glow like a trichoscope view; scalp keeps the UV skin view underneath
    Lh = gblur(lum, 0.8)
    strand = np.clip((Lh - gblur(Lh, 3.5)) * 9.0 + Lh * 1.4, 0, 1)
    hd = np.clip(strand, 0, 1)[..., None]
    hair_duo = lerp(hx('#020C0D'), hx('#0C5A5E'), np.clip(hd * 1.7, 0, 1))
    hair_duo = lerp(hair_duo, hx('#A6F7EE'), np.clip(hd * 1.7 - 0.7, 0, 1))
    duo = lerp(duo, hair_duo, np.clip(hair * 1.1, 0, 1)[..., None])
    del Lh, strand, hd, hair_duo

if CFG['scan'] == 'below':
    fall = 1 - 0.85 * smooth(chin_y - 0.5, chin_y + 3.5, ys)
else:
    fall = np.ones_like(ys)
duo *= (fall * np.ones_like(xs))[..., None]
comp = lerp(comp, duo, reg_person[..., None] * 0.93)
del duo

# light spill from the beam: brighter leading edge on the scan side, soft wash on the other side
dist = (ys - beam_y) if CFG['scan'] == 'below' else (beam_y - ys)
lead = np.exp(-np.clip(dist, 0, None) / 0.55) * (dist >= 0)
spill = np.exp(-np.clip(-dist, 0, None) / 0.30) * (dist < 0)
aq = hx(PAL['aqua'])
comp += (aq * 0.30)[None, None, :] * (lead * alpha[..., 0])[..., None]
comp += (aq * 0.16)[None, None, :] * (spill * alpha[..., 0])[..., None]
del lead, spill, dist

# ---------------------------------------------------------------- mesh + dots in the scan zone (raster, glowing)
conns = [(c.start, c.end) for c in FLC.FACE_LANDMARKS_TESSELATION]
tp = {i: Ti(i) for i in range(len(pts))}


def in_scan(p):
    return p[1] > beam_y + 0.05 if CFG['scan'] == 'below' else p[1] < beam_y - 0.05


def draw_mesh(c):
    pl = paint(C4('aqua_hot', 0.12), stroke=0.011)
    for a, b in conns:
        if in_scan(tp[a]) and in_scan(tp[b]) and math.dist(tp[a], tp[b]) > 0.32:
            c.drawLine(*tp[a], *tp[b], pl)
    pd = paint(C4('aqua_hot', 0.50))
    for i in range(0, 468, 2):
        if in_scan(tp[i]):
            c.drawCircle(*tp[i], 0.018, pd)


mesh = raster_layer(draw_mesh) if SIDE == 'A' else None

# hair: follicle dot field coloured by density (B)
if SIDE == 'B':
    hl = sorted(hairline, key=lambda q: q[0])
    n3 = len(hl) // 3
    ltemp, rtemp = max(hl[:n3], key=lambda q: q[1]), max(hl[-n3:], key=lambda q: q[1])
    TEMPLES = [(ltemp[0] + 0.15, ltemp[1] - 0.45), (rtemp[0] - 0.15, rtemp[1] - 0.45)]
    warm = np.zeros((H, W), np.float32)
    for (qx, qy) in TEMPLES:
        warm += np.exp(-(((xs - qx) / 1.25) ** 2 + ((ys - qy) / 0.95) ** 2))
    warm = np.clip(warm, 0, 1) * (ys < beam_y - 0.1) * alpha[..., 0]
    comp = lerp(comp, comp * 0.55 + hx(PAL['gold']) * 0.55, (warm * 0.55)[..., None])
    del warm

if mesh is not None:
    a = mesh[..., 3:4]
    glow = gblur(mesh, 0.06 * PPI)
    comp = comp * (1 - a) + mesh[..., :3] + glow[..., :3] * 0.8

# ---------------------------------------------------------------- spot detection (A) / hairline (B)
markers = []
if SIDE == 'A':
    g = uv.copy()
    dog = gblur(g, 0.035 * PPI) - gblur(g, 0.14 * PPI)
    nose_x = Ti(1)[0]
    mouth_y = (Ti(61)[1] + Ti(291)[1]) / 2
    cheeks = (np.abs(xs - nose_x) > 1.35) & (ys > beam_y + 0.35) & (ys < mouth_y - 0.1)
    chin = (np.abs(xs - nose_x) < 1.6) & (ys > Ti(17)[1] + 0.45) & (ys < Ti(152)[1] - 0.45)
    valid = (facem > 0.75) & (cheeks | chin)
    oval_idx = [10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288, 397, 365, 379, 378, 400, 377, 152,
                148, 176, 149, 150, 136, 172, 58, 132, 93, 234, 127, 162, 21, 54, 103, 67, 109]
    ov = np.zeros((H, W), np.uint8)
    cv2.fillPoly(ov, [np.array([T(i) for i in oval_idx], np.int32)], 1)
    inner = cv2.erode(ov, np.ones((int(0.6 * PPI),) * 2, np.uint8)) > 0
    del ov
    ex = np.zeros((H, W), np.uint8)
    for idx in ((61, 40, 37, 0, 267, 270, 291, 321, 314, 17, 84, 91), (129, 98, 97, 2, 326, 327, 358, 279, 49, 48, 64, 294, 278)):
        cv2.fillPoly(ex, [cv2.convexHull(np.array([T(i) for i in idx], np.int32))], 1)
    ex = cv2.dilate(ex, np.ones((int(0.9 * PPI),) * 2, np.uint8))
    valid &= inner & (ex == 0)
    score = np.where(valid, -dog, 0)
    mx = cv2.dilate(score, np.ones((int(0.5 * PPI), int(0.5 * PPI)), np.uint8))
    cand = np.argwhere((score == mx) & (score > 0.01))
    cand = sorted(cand, key=lambda p: -score[p[0], p[1]])
    for yv, xv in cand:
        p = (xv / PPI - EXT, yv / PPI - EXT)
        if all(math.dist(p, q) > 0.85 for q in markers):
            markers.append(p)
        if len(markers) >= 8:
            break
    del g, dog, score, mx

# ---------------------------------------------------------------- beam (raster glow part)
def draw_beam(c):
    for wdt, a in ((0.9, 0.10), (0.36, 0.22), (0.12, 0.55)):
        c.drawRect(skia.Rect(-EXT, beam_y - wdt / 2, TW + EXT, beam_y + wdt / 2), paint(C4('aqua', a)))


beam = raster_layer(draw_beam)
beam = gblur(beam, 0.16 * PPI)
taper = (0.55 + 0.45 * np.exp(-((xs - CX) / 9.0) ** 2))[..., None]
comp = comp + beam[..., :3] * taper * 1.25
del beam

# grain (stops banding on flex, adds photographic tooth)
rng = np.random.default_rng(7)
grain = gblur(rng.normal(0, 1, (H, W)).astype(np.float32), 0.5) * 0.010
comp = np.clip(comp + grain[..., None], 0, 1)
del grain

# ================================================================ VECTORS
F = {n: Font.get(n) for n in (SERIF, SANS_B, SANS_SB, SANS_M, SANS_R)}


def text(c, s_, font, size, x, y, color, align='center', tracking=0.0):
    p, w = F[font].path(s_, size, x, y, align, tracking)
    c.drawPath(p, paint(color))
    return w


def value_text(c, val, size, x, y, color, align):
    if '²' not in val:
        return text(c, val, SANS_M, size, x, y, color, align=align)
    base = val.replace('²', '')
    wb = F[SANS_M].width(base, size)
    w2 = F[SANS_M].width('2', size * 0.55)
    x0 = x if align == 'left' else x - (wb + w2 + 0.02)
    text(c, base, SANS_M, size, x0, y, color, align='left')
    text(c, '2', SANS_M, size * 0.55, x0 + wb + 0.02, y - size * 0.36, color, align='left')
    return wb + w2 + 0.02


def hud_label(c, name, val, sd, ly, mxv, myv, ring_r=0.17):
    aqua = C4('aqua')
    lx = SAFE + 0.05 if sd == 'L' else TW - SAFE - 0.05
    al = 'left' if sd == 'L' else 'right'
    text(c, name, SANS_SB, 0.26, lx, ly - 0.50, aqua, align=al, tracking=0.16)
    vw = value_text(c, val, 0.74, lx, ly + 0.33, C4('aqua_hot'), al)
    sg = 1 if sd == 'L' else -1
    ex_ = lx + sg * (vw + 0.22)
    path = skia.Path()
    path.moveTo(ex_, ly + 0.07)
    elbow = mxv - sg * 0.75
    if sg * (elbow - ex_) < 0.3:
        elbow = ex_ + sg * 0.3
    path.lineTo(elbow, ly + 0.07)
    ang = math.atan2(myv - (ly + 0.07), mxv - elbow)
    path.lineTo(mxv - ring_r * math.cos(ang), myv - ring_r * math.sin(ang))
    c.drawPath(path, paint(C4('aqua', 0.85), stroke=0.022))
    c.drawCircle(ex_, ly + 0.07, 0.045, paint(aqua))


LAY = {}


def draw_vectors(c, for_mask=False):
    # top lockup
    gold = C4('gold')
    text(c, 'NOW OPEN  ·  SUBHASH NAGAR', SANS_SB, 0.50, CX, 2.30, gold, tracking=0.24)
    logo_size = 8.2 / F[SERIF].width('leevorá', 1)
    text(c, 'leevorá', SERIF, logo_size, CX, 5.05, C4('cream'))
    text(c, 'AESTHETIC CLINIC', SANS_M, 0.36, CX, 5.92, C4('cream', 0.85), tracking=0.50)

    # headline
    l1, l2 = CFG['head']
    hs = min(20.6 / F[SERIF].width(l2, 1), 20.6 / F[SERIF].width(l1, 1))
    y1 = 6.75 + hs * 0.75
    y2 = y1 + hs * 0.93
    LAY['head'] = (hs, y1, y2)
    text(c, l1, SERIF, hs, CX, y1, C4('cream'))
    acc = CFG['accent_word']
    if l2.endswith(acc):
        pre = l2[:-len(acc)]
        wt = F[SERIF].width(l2, hs)
        xs0 = CX - wt / 2
        wpre = F[SERIF].width(pre, hs)
        text(c, pre, SERIF, hs, xs0, y2, C4('cream'), align='left')
        text(c, acc, SERIF, hs, xs0 + wpre, y2, C4('aqua'), align='left')
    else:
        text(c, l2, SERIF, hs, CX, y2, C4('cream'))

    # scan HUD -------------------------------------------------------
    aqua = C4('aqua')
    # beam core (vector, crisp)
    c.drawRect(skia.Rect(-BLEED, beam_y - 0.022, TW + BLEED, beam_y + 0.022), paint(C4('aqua_hot')))
    # tag sitting on the beam, right side
    tag_y = beam_y - 0.24 if CFG['scan'] == 'below' else beam_y + 0.50
    text(c, CFG['tag'], SANS_SB, 0.27, SAFE + 0.32, tag_y, aqua, align='left', tracking=0.22)
    c.drawCircle(SAFE + 0.09, tag_y - 0.10, 0.075, paint(aqua))

    # corner brackets around the head
    if SIDE == 'A':
        bx0, bx1 = Ti(234)[0] - 0.9, Ti(454)[0] + 0.9
        by0, by1 = Ti(10)[1] - 0.9, Ti(152)[1] + 0.7
    else:
        bx0, bx1 = Ti(234)[0] - 1.1, Ti(454)[0] + 1.1
        by0, by1 = Ti(10)[1] - 3.4, Ti(152)[1] + 0.6
    LAY['bracket'] = (bx0, by0, bx1, by1)
    arm = 1.0
    pb = paint(C4('aqua', 0.8), stroke=0.04)
    pb.setStrokeCap(skia.Paint.kSquare_Cap)
    for (x, y, dx, dy) in ((bx0, by0, 1, 1), (bx1, by0, -1, 1), (bx0, by1, 1, -1), (bx1, by1, -1, -1)):
        path = skia.Path()
        path.moveTo(x, y + dy * arm)
        path.lineTo(x, y)
        path.lineTo(x + dx * arm, y)
        c.drawPath(path, pb)

    ring = paint(C4('aqua_hot', 0.95), stroke=0.035)
    lead = paint(C4('aqua', 0.85), stroke=0.022)
    if SIDE == 'A':
        for m in markers:
            c.drawCircle(m[0], m[1], 0.17, ring)
        labels = CFG['labels']
        slots = []
        for sd in ('L', 'R'):
            ms = sorted([m for m in markers if (m[0] < CX - 1.0 if sd == 'L' else m[0] > CX + 1.0)], key=lambda m: m[1])
            if len(ms) >= 2:
                pair = max(((a, b) for i, a in enumerate(ms) for b in ms[i + 1:]), key=lambda ab: ab[1][1] - ab[0][1])
            else:
                pair = tuple(ms) or ((CX, beam_y + 1.5),)
            ly_prev = beam_y + 0.55
            for m in pair:
                ly = max(m[1], ly_prev + 1.85) if slots and slots[-1][0] == sd else max(m[1], beam_y + 1.05)
                slots.append((sd, ly, m))
                ly_prev = ly
        slots = [x for x in slots if x[0] == 'L'][:2] + [x for x in slots if x[0] == 'R'][:2]
        slots = [slots[0], slots[1], slots[2], slots[3]] if len(slots) == 4 else slots
        order = [0, 1, 2, 3][:len(slots)]
        labels = [labels[0], labels[1], labels[2], labels[3]]
        for (name, val), (sd, ly, (mxv, myv)) in zip(labels, slots):
            hud_label(c, name, val, sd, ly, mxv, myv)
    else:
        # hairline trace
        hp = skia.Path()
        hp.moveTo(*hairline[0])
        for q in hairline[1:]:
            hp.lineTo(*q)
        ph = paint(C4('aqua_hot', 0.95), stroke=0.04)
        ph.setPathEffect(skia.DashPathEffect.Make([0.16, 0.10], 0))
        c.drawPath(hp, ph)
        # rings: dense front-crown point, both temple recessions
        mid = hl[len(hl) // 2]
        dense = (mid[0] - 1.2, mid[1] - 1.6)
        lt, rt = TEMPLES
        c.drawCircle(*dense, 0.17, ring)
        warm_ring = paint(C4('gold', 0.95), stroke=0.035)
        for q in (lt, rt):
            c.drawCircle(*q, 0.17, warm_ring)
            c.drawCircle(*q, 0.42, paint(C4('gold', 0.55), stroke=0.018))
        (n1, v1), (n2, v2), (n3_, v3) = CFG['labels']
        hud_label(c, n1, v1, 'L', beam_y - 5.3, *dense)
        hud_label(c, n3_, v3, 'L', beam_y - 2.0, *lt)
        hud_label(c, n2, v2, 'R', beam_y - 3.6, *rt)

    # offer ----------------------------------------------------------
    oy = 34.55
    osz = min(1.95, 20.4 / F[SERIF].width(CFG['offer'], 1))
    text(c, CFG['offer'], SERIF, osz, CX, oy, gold)
    sc = 'LAUNCH MONTH ONLY'
    ssz = 0.46
    sw = F[SANS_SB].width(sc, ssz, 0.30)
    sy = oy + 1.18
    text(c, sc, SANS_SB, ssz, CX, sy, gold, tracking=0.30)
    rl = paint(C4('gold', 0.85), stroke=0.03)
    c.drawLine(CX - sw / 2 - 2.6, sy - 0.13, CX - sw / 2 - 0.45, sy - 0.13, rl)
    c.drawLine(CX + sw / 2 + 0.45, sy - 0.13, CX + sw / 2 + 2.6, sy - 0.13, rl)

    # proof strip ----------------------------------------------------
    py = 38.55
    colw = (TW - 2 * SAFE) / 3
    for k, (t1_, t2_) in enumerate(CFG['proof']):
        cxk = SAFE + colw * (k + 0.5)
        text(c, t1_, SERIF, 0.98, cxk, py, C4('cream'))
        text(c, t2_.upper(), SANS_M, 0.27, cxk, py + 0.66, C4('aqua', 0.92), tracking=0.10)
        if k:
            xd = SAFE + colw * k
            c.drawLine(xd, py - 0.80, xd, py + 0.72, paint(C4('sage', 0.45), stroke=0.025))

    # CTA ------------------------------------------------------------
    qy0 = 40.25
    q = 5.15
    qx0 = SAFE
    LAY['qr'] = (qx0, qy0, q)
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(qx0, qy0, qx0 + q, qy0 + q), 0.28, 0.28), paint(C4('qr_tile')))
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_Q, border=0)
    qr.add_data(WA)
    qr.make(fit=True)
    mat = np.array(qr.get_matrix(), bool)
    n = mat.shape[0]
    pad = 0.42
    mod = (q - 2 * pad) / n
    LAY['qr_mod'] = (n, mod)
    qp = paint(C4('ink'), aa=False)
    qpath = skia.Path()
    for r_ in range(n):
        for c_ in range(n):
            if mat[r_, c_]:
                qpath.addRect(skia.Rect(qx0 + pad + c_ * mod, qy0 + pad + r_ * mod,
                                        qx0 + pad + (c_ + 1) * mod + 1e-4, qy0 + pad + (r_ + 1) * mod + 1e-4))
    c.drawPath(qpath, paint(C4('ink')))

    rx = qx0 + q + 0.75
    rw = TW - SAFE - rx
    text(c, 'Scan to book on WhatsApp', SANS_SB, 0.62, rx, qy0 + 0.95, C4('cream'), align='left')
    c.drawLine(rx, qy0 + 1.55, rx + rw, qy0 + 1.55, paint(C4('sage', 0.4), stroke=0.025))
    text(c, 'CALL OR WHATSAPP', SANS_SB, 0.30, rx, qy0 + 2.35, C4('aqua'), align='left', tracking=0.16)
    num = '80764 67352'
    pre = '+91 '
    nsz = min(1.55, rw / F[SANS_B].width(pre + num, 1))
    wpre = text(c, pre, SANS_M, nsz, rx, qy0 + 2.35 + nsz * 0.86, C4('cream', 0.75), align='left')
    text(c, num, SANS_B, nsz, rx + wpre, qy0 + 2.35 + nsz * 0.86, C4('cream'), align='left')

    # fine print
    text(c, 'Scan imagery is illustrative. Free analysis during our launch month only. T&C apply.',
         SANS_R, 0.21, CX, TH - SAFE + 0.02, C4('sage', 0.85))


# ================================================================ COMPOSE
vec = raster_layer(draw_vectors)
final = comp * (1 - vec[..., 3:4]) + vec[..., :3]
final8 = (np.clip(final, 0, 1) * 255 + 0.5).astype(np.uint8)
json.dump({'beam_y_in': beam_y, 'markers': markers, 'lay': {k: list(map(float, np.ravel(v))) for k, v in LAY.items()}},
          open(f'{OUT}/side{SIDE}_layout.json', 'w'), indent=1)


def crop_in(arr, margin):
    a0, b0 = int(round((EXT - margin) * PPI)), int(round((EXT - margin) * PPI))
    return arr[b0:H - b0, a0:W - a0]


Image.fromarray(crop_in(final8, 0)).save(f'{OUT}/side{SIDE}_trim_preview.png')
Image.fromarray(crop_in(final8, 0)).resize((720, 1440), Image.LANCZOS).save(f'{OUT}/side{SIDE}_small.png')
np.save(f'{OUT}/side{SIDE}_comp.npy', (np.clip(comp, 0, 1) * 65535).astype(np.uint16))
print('done', SIDE, 'beam', round(beam_y, 2), 'markers', len(markers), 'head', LAY['head'])

# ================================================================ EXPORTS
import subprocess, pikepdf

ICC_CMYK = f'{ROOT}/icc/FOGRA39.icc'
ICC_SRGB = '/usr/share/color/icc/sRGB.icc'
TAG = f'LEEVORA_Standee_2x4ft_Side{SIDE}'
srgb_p = ImageCms.getOpenProfile(ICC_SRGB)
cmyk_p = ImageCms.getOpenProfile(ICC_CMYK)
to_cmyk = ImageCms.buildTransform(srgb_p, cmyk_p, 'RGB', 'CMYK', renderingIntent=1,
                                  flags=ImageCms.Flags.BLACKPOINTCOMPENSATION)
to_rgb = ImageCms.buildTransform(cmyk_p, srgb_p, 'CMYK', 'RGB', renderingIntent=1,
                                 flags=ImageCms.Flags.BLACKPOINTCOMPENSATION)
icc_bytes = open(ICC_CMYK, 'rb').read()

# --- 1. vector PDF: raster plate + outlined vectors, 10 mm bleed, crop marks in a slug
SLUG = 0.75
pw, ph = TW + 2 * (BLEED + SLUG), TH + 2 * (BLEED + SLUG)
plate = Image.fromarray((np.clip(crop_in(comp, BLEED), 0, 1) * 255 + 0.5).astype(np.uint8))
buf = io.BytesIO()
plate.save(buf, 'JPEG', quality=96, subsampling=0, dpi=(PPI, PPI))
plate_img = skia.Image.MakeFromEncoded(skia.Data.MakeWithCopy(buf.getvalue()))
rgb_pdf = f'{OUT}/{TAG}_rgb_tmp.pdf'
stream = skia.FILEWStream(rgb_pdf)
doc = skia.PDF.MakeDocument(stream, Title=f'leevorá standee 2x4 ft Side {SIDE}', Creator='Adsworm', Producer='Adsworm')
pc = doc.beginPage(pw * 72, ph * 72)
pc.scale(72, 72)
pc.translate(SLUG + BLEED, SLUG + BLEED)           # origin = trim top-left
pc.save()
pc.clipRect(skia.Rect(-BLEED, -BLEED, TW + BLEED, TH + BLEED))
pc.drawImageRect(plate_img, skia.Rect(-BLEED, -BLEED, TW + BLEED, TH + BLEED),
                 skia.SamplingOptions(skia.FilterMode.kLinear))
draw_vectors(pc)
pc.restore()
# crop marks + slug info (registration black)
mk = paint(skia.Color4f(0, 0, 0, 1), stroke=0.25 / 72)
off, ln = BLEED + 0.12, 0.45
for (x, y) in ((0, 0), (TW, 0), (0, TH), (TW, TH)):
    sx = -1 if x == 0 else 1
    sy = -1 if y == 0 else 1
    pc.drawLine(x + sx * off, y, x + sx * (off + ln), y, mk)
    pc.drawLine(x, y + sy * off, x, y + sy * (off + ln), mk)
slug_txt = (f'leevorá · 2 x 4 ft LED standee · SIDE {SIDE} · trim 610 x 1219 mm · bleed 10 mm · '
            f'safe 40 mm · CMYK FOGRA39 · raster 150 ppi @ 100%')
text(pc, slug_txt, SANS_M, 0.16, 0, TH + BLEED + 0.42, skia.Color4f(0, 0, 0, 1), align='left')
doc.endPage()
doc.close()
del stream

# --- 2. Ghostscript: convert everything to CMYK through FOGRA39 (relative colorimetric, BPC)
cmyk_pdf = f'{OUT}/{TAG}_PRINT_CMYK.pdf'
subprocess.run(['gs', '-q', '-dSAFER', '-dBATCH', '-dNOPAUSE', '-sDEVICE=pdfwrite', '-dCompatibilityLevel=1.6',
                '-sColorConversionStrategy=CMYK', '-sProcessColorModel=DeviceCMYK',
                f'-sOutputICCProfile={ICC_CMYK}', f'-sDefaultRGBProfile={ICC_SRGB}', '-dRenderIntent=1',
                '-dBlackPtComp=1',
                '-dAutoFilterColorImages=false', '-dColorImageFilter=/DCTEncode', '-dJPEGQ=95',
                '-dDownsampleColorImages=false', '-dEncodeColorImages=true',
                f'-sOutputFile={cmyk_pdf}', '-c',
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

# --- 3. flattened CMYK TIFFs (exact bleed size, and flex-wrap size with 75 mm extension)
for name, margin in (('PRINT_CMYK_10mm-bleed', BLEED), ('FLEX-WRAP_CMYK_75mm-extension', 75 / 25.4)):
    im = Image.fromarray(crop_in(final8, margin))
    cm = ImageCms.applyTransform(im, to_cmyk)
    cm.save(f'{OUT}/{TAG}_{name}.tif', compression='tiff_adobe_deflate', dpi=(PPI, PPI), icc_profile=icc_bytes)
    if margin == BLEED:
        proof = ImageCms.applyTransform(cm, to_rgb)          # soft proof of the print gamut
        proof.save(f'{OUT}/{TAG}_softproof.png')
        cmyk_arr = np.asarray(cm).astype(np.float32) / 255 * 100
        tac = cmyk_arr.sum(-1)
        print('TAC max %.0f  p99 %.0f' % (tac.max(), np.percentile(tac, 99)))
        bgpx = cmyk_arr[int(1.0 * PPI), int(1.0 * PPI)]
        print('bg corner CMYK', np.round(bgpx).astype(int))

# --- 4. day/night blockout (white-ink) mask: ink everywhere except what should glow, openings spread 2.5 mm
lumf = (final8.astype(np.float32) / 255) @ np.float32([0.2126, 0.7152, 0.0722])
openm = smooth(0.10, 0.24, lumf)                                       # 1 = let light through
openm = cv2.dilate(openm, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * int(2.5 / 25.4 * PPI) + 1,) * 2))
openm = gblur(openm, 0.04 * PPI)
block = crop_in(((1 - openm) * 255).astype(np.uint8), BLEED)          # 255 = full blockout ink
Image.fromarray(255 - block).save(f'{OUT}/{TAG}_DAYNIGHT-BLOCKOUT_black-is-ink.tif', compression='tiff_adobe_deflate', dpi=(PPI, PPI))

# --- 5. previews: soft-proof day + simulated night (backlit), with and without blockout
pr = np.asarray(proof).astype(np.float32) / 255
lin = pr ** 2.2
def night(lin_, blocked):
    tr = lin_.copy()
    if blocked is not None:
        tr = tr * (1 - 0.92 * blocked[..., None])
    em = 1 - np.exp(-tr * 3.2)                                 # backlight through the print, soft saturation
    bloom = gblur(em ** 2, 0.25 * PPI) * 0.55 + gblur(em ** 2, 1.2 * PPI) * 0.35
    return np.clip(em + bloom, 0, 1) ** (1 / 2.2)
bk = (block.astype(np.float32) / 255)
for nm, arr in (('night', night(lin, None)), ('night-blockout', night(lin, bk))):
    Image.fromarray((arr * 255).astype(np.uint8)).resize((900, int(900 * arr.shape[0] / arr.shape[1])), Image.LANCZOS).save(f'{OUT}/{TAG}_{nm}_preview.jpg', quality=90)
proof.resize((900, int(900 * proof.height / proof.width)), Image.LANCZOS).save(f'{OUT}/{TAG}_day_preview.jpg', quality=90)

# --- 6. QR check on the soft proof (full size and phone-at-1.5 m size)
qx0, qy0, qs = LAY['qr']
qcrop = np.asarray(proof)[int((qy0 + BLEED - 0.3) * PPI):int((qy0 + BLEED + qs + 0.3) * PPI),
                          int((qx0 + BLEED - 0.3) * PPI):int((qx0 + BLEED + qs + 0.3) * PPI)]
det = cv2.QRCodeDetector()
for scale in (1.0, 0.35):
    q_ = cv2.resize(qcrop, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
    val, _, _ = det.detectAndDecode(cv2.cvtColor(q_, cv2.COLOR_RGB2BGR))
    print('QR scale', scale, 'OK' if val == WA else f'FAIL {val!r}')
print('exports done', SIDE)
