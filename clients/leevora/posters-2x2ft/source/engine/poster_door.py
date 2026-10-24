#!/usr/bin/env python3
"""leevorá CoolSculpting 2x2 ft poster: "walk in / walk out" door diptych on licensed photos.

Left: she walks in (back view, oversized sweater, darker). Right: she walks out (fitted dress, light).
Copy is the client's; added only the WALK IN / WALK OUT tags and the stock-licence disclaimer.
MODE=comp  -> uses the watermarked iStock comps, renders a review JPG (not for print)
MODE=final -> uses the licensed XL files, exports CMYK PDF + TIFFs like the other posters
"""
import sys, os, io, math, json, subprocess
import numpy as np, cv2, skia, pikepdf
from PIL import Image, ImageCms

ROOT = '/tmp/claude-0/-home-user-Adsworm/3d8d5e5a-8f36-56e6-be63-644bad3ee2df/scratchpad'
sys.path.insert(0, f'{ROOT}/engine')
from typeset import Font

MODE = os.environ.get('MODE', 'comp')
OUT = f'{ROOT}/out_door'
os.makedirs(OUT, exist_ok=True)
Image.MAX_IMAGE_PIXELS = None

SRC = {
    'comp': dict(before=f'{ROOT}/refs/ist/comp_1182388957_612x612.jpg', after=f'{ROOT}/refs/ist/comp_1687013196_612x612.jpg'),
    'final': dict(before=f'{ROOT}/licensed/iStock-1182388957.jpg', after=f'{ROOT}/licensed/iStock-1687013196.jpg'),
}[MODE]
PPI = 100 if MODE == 'comp' else 150
EXT = 0.6
TW = TH = 24.0
BLEED = 10 / 25.4
SAFE = 40 / 25.4
W = H = round((TW + 2 * EXT) * PPI)
CX = TW / 2
PHOTO_TOP = 5.75                     # photos sit under a dark title band
SEAM = TW / 2


def px(v):
    return (v + EXT) * PPI


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


PAL = dict(night='#0F0D0B', cream='#FBF3E4', gold='#E4BA6E', sage='#B9C2B9', aqua=from_cmyk(55, 0, 22, 0))


def C4(name, a=1.0):
    r, g, b = hx(PAL[name]) if name in PAL else hx(name)
    return skia.Color4f(float(r), float(g), float(b), a)


SERIF = 'Gloock-Regular'
SANS_SB, SANS_M, SANS_R = (f'InstrumentSans-{w}' for w in ('SemiBold', 'Medium', 'Regular'))
F = {n: Font.get(n) for n in (SERIF, SANS_SB, SANS_M, SANS_R)}


def smooth(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0, 1)
    return t * t * (3 - 2 * t)


def gblur(a, s_):
    if s_ <= 0:
        return a
    k = int(s_ * 3) * 2 + 1
    return cv2.GaussianBlur(a, (k, k), s_)


def lerp(a, b, t):
    return a + (b - a) * t


def paint(color, stroke=None, aa=True):
    p = skia.Paint(AntiAlias=aa, Color4f=color)
    if stroke:
        p.setStyle(skia.Paint.kStroke_Style)
        p.setStrokeWidth(stroke)
        p.setStrokeCap(skia.Paint.kRound_Cap)
        p.setStrokeJoin(skia.Paint.kRound_Join)
    return p


def raster_layer(draw_fn):
    surf = skia.Surface(W, H)
    c = surf.getCanvas()
    c.clear(skia.Color4f(0, 0, 0, 0))
    c.scale(PPI, PPI)
    c.translate(EXT, EXT)
    draw_fn(c)
    return surf.makeImageSnapshot().toarray(colorType=skia.kRGBA_8888_ColorType, alphaType=skia.kPremul_AlphaType).astype(np.float32) / 255


def crop_in(arr, margin):
    b0 = int(round((EXT - margin) * PPI))
    return arr[b0:arr.shape[0] - b0, b0:arr.shape[1] - b0]


ys = (np.arange(H, dtype=np.float32)[:, None] / PPI - EXT)
xs = (np.arange(W, dtype=np.float32)[None, :] / PPI - EXT)


def place(path, x0, x1, y0, y1, focus=(0.5, 0.5), zoom=1.0):
    """Cover the box [x0,x1]x[y0,y1] (inches) with the image; return full-canvas rgb + mask."""
    src = cv2.imread(path, cv2.IMREAD_COLOR)[..., ::-1].astype(np.float32) / 255
    sh, sw = src.shape[:2]
    bw, bh = x1 - x0, y1 - y0
    s_in = max(bw / sw, bh / sh) * zoom
    left = (x0 + bw / 2) - focus[0] * sw * s_in
    top = (y0 + bh / 2) - focus[1] * sh * s_in
    left = min(x0, max(x1 - sw * s_in, left))
    top = min(y0, max(y1 - sh * s_in, top))
    s = s_in * PPI
    M = np.float32([[s, 0, px(left)], [0, s, px(top)]])
    img = cv2.warpAffine(src, M, (W, H), flags=cv2.INTER_AREA if s < 1 else cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT)
    m = ((xs >= x0) & (xs < x1) & (ys >= y0) & (ys < y1)).astype(np.float32)
    return img, m


def grade(img, lift=0.0, gain=1.0, warm=(1.0, 1.0, 1.0), sat=1.0):
    img = np.clip(img * np.float32(warm) * gain, 0, 1)
    l = img @ np.float32([0.2126, 0.7152, 0.0722])
    img = l[..., None] + (img - l[..., None]) * sat
    return np.clip(img + (1 - img) * lift, 0, 1)


# ================================================================ RASTER
comp = np.ones((H, W, 3), np.float32) * hx(PAL['night'])
x_l, x_r = -BLEED - 0.05, TW + BLEED + 0.05
bef, mb = place(SRC['before'], x_l, SEAM, PHOTO_TOP, TH + BLEED + 0.05, focus=(0.48, 0.42), zoom=1.0)
aft, ma = place(SRC['after'], SEAM, x_r, PHOTO_TOP, TH + BLEED + 0.05, focus=(0.55, 0.45), zoom=1.0)
bef = grade(bef, gain=0.92, warm=(1.0, 0.99, 0.98), sat=0.88)          # walking in: a little muted
aft = grade(aft, lift=0.02, gain=1.03, warm=(1.02, 1.0, 0.97), sat=1.02)  # walking out: light, warm
comp = lerp(comp, bef, mb[..., None])
comp = lerp(comp, aft, ma[..., None])
del bef, aft
# title band: solid at top, fades into the photos
top_fade = 1 - smooth(PHOTO_TOP - 0.25, PHOTO_TOP + 1.25, ys)
comp = lerp(comp, hx(PAL['night']), (top_fade * np.ones_like(xs))[..., None])
# benefits scrim at the bottom
bot = smooth(17.0, 19.3, ys) * 0.94
comp = lerp(comp, hx(PAL['night']), (bot * np.ones_like(xs))[..., None])
rng = np.random.default_rng(5)
comp = np.clip(comp + gblur(rng.normal(0, 1, (H, W)).astype(np.float32), 0.5)[..., None] * 0.007, 0, 1)

# ================================================================ VECTORS
LOGO = json.load(open(f'{ROOT}/engine/leevora_logo.json'))
LOGO_COL = '#%02X%02X%02X' % tuple(round(v * 255) for v in LOGO['color'])


def draw_logo(c, cx, top, width):
    sc = width / LOGO['w']
    x = cx - width / 2
    for part in ('word', 'desc'):
        p = skia.Path()
        for f in LOGO[part]:
            for sp_ in f['path']:
                for seg in sp_:
                    k, q = seg[0], [(x + a * sc, top + b * sc) for a, b in seg[1:]]
                    if k == 'M':
                        p.moveTo(*q[0])
                    elif k == 'L':
                        p.lineTo(*q[0])
                    elif k == 'C':
                        p.cubicTo(*q[0], *q[1], *q[2])
                    elif k == 'Z':
                        p.close()
        c.drawPath(p, paint(C4(LOGO_COL)))
    return top + LOGO['h'] * sc


def text(c, s_, font, size, x, y, color, align='left', tracking=0.0):
    p, w = F[font].path(s_, size, x, y, align, tracking)
    c.drawPath(p, paint(color))
    return w


def icon(c, kind, cx, cy, r):
    g = C4('gold')
    c.drawCircle(cx, cy, r, paint(g, stroke=0.032))
    st = paint(g, stroke=0.048)
    u = r * 0.52
    if kind == 'target':
        c.drawCircle(cx, cy, u * 0.78, st)
        c.drawCircle(cx, cy, u * 0.16, paint(g))
        for a in range(4):
            dx, dy = math.cos(a * math.pi / 2), math.sin(a * math.pi / 2)
            c.drawLine(cx + dx * u * 0.48, cy + dy * u * 0.48, cx + dx * u * 1.12, cy + dy * u * 1.12, st)
    elif kind == 'snow':
        for a in range(6):
            t = a * math.pi / 3 - math.pi / 2
            dx, dy = math.cos(t), math.sin(t)
            c.drawLine(cx, cy, cx + dx * u, cy + dy * u, st)
            bx, by = cx + dx * u * 0.62, cy + dy * u * 0.62
            for sgn in (-1, 1):
                t2 = t + sgn * math.pi / 4
                c.drawLine(bx, by, bx + math.cos(t2) * u * 0.30, by + math.sin(t2) * u * 0.30, st)
    elif kind == 'clock':
        c.drawCircle(cx, cy, u * 0.92, st)
        c.drawLine(cx, cy, cx, cy - u * 0.58, st)
        c.drawLine(cx, cy, cx + u * 0.42, cy + u * 0.18, st)


def arrow(c, x, y, s, col, stroke=0.05):
    p = skia.Path()
    p.moveTo(x - s, y)
    p.lineTo(x + s, y)
    p.moveTo(x + s * 0.45, y - s * 0.55)
    p.lineTo(x + s, y)
    p.lineTo(x + s * 0.45, y + s * 0.55)
    c.drawPath(p, paint(col, stroke=stroke))


def draw_vectors(c):
    cream, gold = C4('cream'), C4('gold')
    # title band
    lb = draw_logo(c, CX, 0.95, 3.0)
    text(c, 'Benefits of', SANS_R, 0.70, CX, lb + 1.02, C4('cream', 0.92), align='center')
    head = [('Cool', 'aqua'), ('Sculpting', 'cream'), (' Treatment', 'cream')]
    full = ''.join(t for t, _ in head)
    hs = min(1.95, 20.9 / F[SERIF].width(full, 1))
    x = CX - F[SERIF].width(full, hs) / 2
    hy = lb + 1.02 + 0.14 + hs * 0.84
    for t, col in head:
        x += text(c, t, SERIF, hs, x, hy, C4(col))
    text(c, 'Freeze away stubborn fat, without surgery.', SANS_R, 0.52, CX, hy + 0.76, C4('cream', 0.85), align='center')
    # the story: walk in / walk out
    ty = PHOTO_TOP + 1.55
    for label, right in (('WALK IN', False), ('WALK OUT', True)):
        tw_ = F[SANS_SB].width(label, 0.40, 0.22)
        pw_ = tw_ + 1.45
        x0 = TW - SAFE - pw_ if right else SAFE
        pill = skia.RRect.MakeRectXY(skia.Rect(x0, ty - 0.62, x0 + pw_, ty + 0.30), 0.46, 0.46)
        c.drawRRect(pill, paint(C4('night', 0.62)))
        c.drawRRect(pill, paint(C4('gold', 0.75), stroke=0.022))
        if right:
            arrow(c, x0 + 0.55, ty - 0.15, 0.20, gold, 0.04)
            text(c, label, SANS_SB, 0.40, x0 + 1.02, ty, cream, tracking=0.22)
        else:
            text(c, label, SANS_SB, 0.40, x0 + 0.42, ty, cream, tracking=0.22)
            arrow(c, x0 + 0.42 + tw_ + 0.48, ty - 0.15, 0.20, gold, 0.04)
    # seam
    c.drawLine(SEAM, PHOTO_TOP + 0.3, SEAM, 18.2, paint(C4('cream', 0.85), stroke=0.03))
    by = 11.6
    c.drawCircle(SEAM, by, 0.62, paint(C4('night', 0.92)))
    c.drawCircle(SEAM, by, 0.62, paint(gold, stroke=0.04))
    arrow(c, SEAM, by, 0.26, cream, 0.05)
    # benefits row
    cols = [(4.55, 'target', 'Targets stubborn fat'), (CX, 'snow', 'Non-invasive, no needles'), (TW - 4.55, 'clock', 'No downtime required')]
    lsz = min(0.58, 6.8 / max(F[SANS_M].width(l, 1) for _, _, l in cols))
    for cx, kind, label in cols:
        icon(c, kind, cx, 19.55, 0.50)
        text(c, label, SANS_M, lsz, cx, 20.80, cream, align='center')
    for xd in (CX - 3.72, CX + 3.72):
        c.drawLine(xd, 19.15, xd, 20.95, paint(C4('cream', 0.30), stroke=0.022))
    # footnote + licence disclaimer
    foot = 'Results build gradually over 1–3 months.'
    fs = 0.46
    fw = F[SERIF].width(foot, fs)
    fy = 21.82
    text(c, foot, SERIF, fs, CX, fy, C4('cream', 0.96), align='center')
    rl = paint(C4('gold', 0.9), stroke=0.03)
    c.drawLine(CX - fw / 2 - 1.55, fy - fs * 0.34, CX - fw / 2 - 0.40, fy - fs * 0.34, rl)
    c.drawLine(CX + fw / 2 + 0.40, fy - fs * 0.34, CX + fw / 2 + 1.55, fy - fs * 0.34, rl)
    text(c, 'Images are illustrative and posed by models. Individual results vary.', SANS_R, 0.24, CX, TH - SAFE + 0.05,
         C4('sage', 0.85), align='center')


vec = raster_layer(draw_vectors)
final = comp * (1 - vec[..., 3:4]) + vec[..., :3]
final8 = (np.clip(final, 0, 1) * 255 + 0.5).astype(np.uint8)
trim = Image.fromarray(crop_in(final8, 0))
trim.save(f'{OUT}/door_{MODE}_trim.png')
trim.resize((1400, 1400), Image.LANCZOS).save(f'{OUT}/door_{MODE}_preview.jpg', quality=90)
print('done', MODE, trim.size)

if MODE != 'final':
    sys.exit(0)

# ================================================================ EXPORTS (licensed files only)
TAG = 'Leevora_CoolSculpting_WalkIn-WalkOut_2x2ft'
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
doc = skia.PDF.MakeDocument(stream, Title='leevorá CoolSculpting walk in / walk out 2x2 ft', Creator='Adsworm', Producer='Adsworm')
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
slug_p, _ = F[SANS_M].path(f'leevorá · {TAG} · trim 610 x 610 mm · bleed 10 mm · safe 40 mm · CMYK FOGRA39 · raster 150 ppi @ 100% · '
                           f'photos iStock 1182388957 + 1687013196 (licensed)', 0.16, 0, TH + BLEED + 0.42, 'left')
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
cm = ImageCms.applyTransform(Image.fromarray(crop_in(final8, BLEED)), to_cmyk)
cm.save(f'{OUT}/{TAG}_PRINT_CMYK_10mm-bleed.tif', compression='tiff_adobe_deflate', dpi=(PPI, PPI), icc_profile=icc_bytes)
Image.fromarray(crop_in(final8, BLEED)).save(f'{OUT}/{TAG}_RIP-MASTER_sRGB_10mm-bleed.tif', compression='tiff_adobe_deflate',
                                             dpi=(PPI, PPI), icc_profile=srgb_bytes)
tac = np.asarray(cm).astype(np.float32).sum(-1) / 2.55
print('TAC max %.0f p99 %.0f' % (tac.max(), np.percentile(tac, 99)))
print('exports done')
