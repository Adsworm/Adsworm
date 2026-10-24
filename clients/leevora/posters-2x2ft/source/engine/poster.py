#!/usr/bin/env python3
"""leevorá 2x2 ft treatment posters (CoolSculpting, Laser Hair Reduction) in the standee's visual system.

Text column left (real logo, serif headline with one aqua accent, gold line icons), real photo in a
rounded gold-line frame on the right. Copy is the client's, word for word. No QR / phone.
Exports: CMYK FOGRA39 vector PDF (outlined type, 10 mm bleed, crop marks), CMYK + sRGB TIFFs, preview.
Usage: poster.py cool|laser   (PREVIEW=1 for a quick look)
"""
import sys, os, io, math, json, subprocess
import numpy as np, cv2, skia, pikepdf
from PIL import Image, ImageCms

ROOT = '/tmp/claude-0/-home-user-Adsworm/3d8d5e5a-8f36-56e6-be63-644bad3ee2df/scratchpad'
sys.path.insert(0, f'{ROOT}/engine')
from typeset import Font

KEY = sys.argv[1] if len(sys.argv) > 1 else 'cool'
OUT = f'{ROOT}/out_posters'
os.makedirs(OUT, exist_ok=True)
Image.MAX_IMAGE_PIXELS = None

PPI = 150
EXT = 1.0
TW, TH = 24.0, 24.0
BLEED = 10 / 25.4
SAFE = 40 / 25.4
W, H = round((TW + 2 * EXT) * PPI), round((TH + 2 * EXT) * PPI)


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


PAL = dict(bg_core='#163A33', bg_mid='#0E2723', bg_edge='#07171A', cream='#FBF3E4', gold='#E4BA6E',
           sage='#A3B7AD', ink='#0D2622', aqua=from_cmyk(55, 0, 22, 0), aqua_hot=from_cmyk(14, 0, 6, 0))


def C4(name, a=1.0):
    r, g, b = hx(PAL[name]) if name in PAL else hx(name)
    return skia.Color4f(float(r), float(g), float(b), a)


SERIF = 'Gloock-Regular'
SANS_SB, SANS_M, SANS_R = (f'InstrumentSans-{w}' for w in ('SemiBold', 'Medium', 'Regular'))

CFG = {
    'cool': dict(
        tag='Leevora_Benefits_of_CoolSculpting_Treatment_2x2ft',
        photo='hero/cool.png', focus=(0.5, 0.5), zoom=1.0,
        pre='Benefits of', big=[[('Cool', 'aqua'), ('Sculpting', 'cream')]], post='Treatment',
        sub=['Freeze away stubborn fat,', 'without surgery.'],
        bens=[('target', 'Targets stubborn fat'), ('snow', 'Non-invasive, no needles'), ('clock', 'No downtime required')],
        foot='Results build gradually over 1–3 months.',
        ring=None,
    ),
    'laser': dict(
        tag='Leevora_Laser_Hair_Reduction_Poster_2x2ft',
        photo='hero/laser.png', focus=(0.5, 0.5), zoom=1.0,
        pre='what', big=[[('laser', 'aqua'), (' hair', 'cream')], [('reduction', 'cream')]], post='can do for you.',
        sub=[],
        bens=[('hair', 'Long-term hair reduction'), ('razor', 'Less frequent shaving'), ('clock', 'Minimal downtime')],
        foot='Multiple sessions. Results vary.',
        ring=None,
    ),
}[KEY]
over = json.load(open(f'{ROOT}/engine/poster_photo.json')).get(KEY, {}) if os.path.exists(f'{ROOT}/engine/poster_photo.json') else {}
CFG.update(over)

X0 = SAFE
COL_R = 11.95
FR = (12.75, SAFE, TW - SAFE, TH - SAFE)
FR_R = 0.55


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


def raster_layer(draw_fn, alpha_only=False):
    surf = skia.Surface.MakeRaster(skia.ImageInfo.MakeA8(W, H)) if alpha_only else skia.Surface(W, H)
    c = surf.getCanvas()
    c.clear(skia.Color4f(0, 0, 0, 0))
    c.scale(PPI, PPI)
    c.translate(EXT, EXT)
    draw_fn(c)
    img = surf.makeImageSnapshot()
    if alpha_only:
        return img.toarray(colorType=skia.kAlpha_8_ColorType).astype(np.float32) / 255
    return img.toarray(colorType=skia.kRGBA_8888_ColorType, alphaType=skia.kPremul_AlphaType).astype(np.float32) / 255


def crop_in(arr, margin):
    b0 = int(round((EXT - margin) * PPI))
    return arr[b0:arr.shape[0] - b0, b0:arr.shape[1] - b0]


# ================================================================ RASTER
ys = (np.arange(H, dtype=np.float32)[:, None] / PPI - EXT)
xs = (np.arange(W, dtype=np.float32)[None, :] / PPI - EXT)
d = np.sqrt(((xs - 8.0) / 15.0) ** 2 + ((ys - 9.0) / 15.0) ** 2)
tb = smooth(0.0, 1.25, d)[..., None]
bg = lerp(hx(PAL['bg_core']), hx(PAL['bg_mid']), np.clip(tb * 1.6, 0, 1))
comp = lerp(bg, hx(PAL['bg_edge']), np.clip(tb * 1.6 - 0.6, 0, 1))
del d, tb, bg

src = cv2.imread(f'{ROOT}/{CFG["photo"]}', cv2.IMREAD_COLOR)[..., ::-1].astype(np.float32) / 255
sh, sw = src.shape[:2]
fx0, fy0, fx1, fy1 = FR
fw, fh = fx1 - fx0, fy1 - fy0
s_in = max(fw / sw, fh / sh) * CFG['zoom']                     # cover the frame
fxn, fyn = CFG['focus']                                       # focus point in the source (0..1)
left = (fx0 + fw / 2) - fxn * sw * s_in
top = (fy0 + fh / 2) - fyn * sh * s_in
left = min(fx0, max(fx1 - sw * s_in, left))
top = min(fy0, max(fy1 - sh * s_in, top))
s = s_in * PPI
M = np.float32([[s, 0, px(left)], [0, s, px(top)]])
photo = cv2.warpAffine(src, M, (W, H), flags=cv2.INTER_AREA if s < 1 else cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT)
photo = np.clip(photo * np.float32([1.01, 1.0, 0.985]), 0, 1)
photo = photo + (1 - photo) * 0.025
vig = 1 - 0.14 * smooth(0.55, 1.2, np.sqrt(((xs - (fx0 + fx1) / 2) / (fw / 2)) ** 2 + ((ys - (fy0 + fy1) / 2) / (fh / 2)) ** 2))
photo *= vig[..., None]
del vig, src


def frame_path():
    p = skia.Path()
    p.addRRect(skia.RRect.MakeRectXY(skia.Rect(fx0, fy0, fx1, fy1), FR_R, FR_R))
    return p


fmask = raster_layer(lambda c: c.drawPath(frame_path(), paint(skia.Color4f(1, 1, 1, 1))), alpha_only=True)
# soft drop shadow so the photo sits on the board
shadow = gblur(fmask, 0.28 * PPI)
shadow = np.roll(shadow, (int(0.10 * PPI), int(0.06 * PPI)), (0, 1))
comp *= (1 - 0.45 * shadow * (1 - fmask))[..., None]
comp = lerp(comp, photo, fmask[..., None])
del photo, shadow
rng = np.random.default_rng(11)
comp = np.clip(comp + gblur(rng.normal(0, 1, (H, W)).astype(np.float32), 0.5)[..., None] * 0.008, 0, 1)

# ================================================================ VECTORS
F = {n: Font.get(n) for n in (SERIF, SANS_SB, SANS_M, SANS_R)}


def text(c, s_, font, size, x, y, color, align='left', tracking=0.0):
    p, w = F[font].path(s_, size, x, y, align, tracking)
    c.drawPath(p, paint(color))
    return w


LOGO = json.load(open(f'{ROOT}/engine/leevora_logo.json'))
LOGO_COL = '#%02X%02X%02X' % tuple(round(v * 255) for v in LOGO['color'])


def draw_logo(c, x, top, width):
    sc = width / LOGO['w']
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


def icon(c, kind, cx, cy, r):
    g = C4('gold')
    c.drawCircle(cx, cy, r, paint(g, stroke=0.032))
    st = paint(g, stroke=0.050)
    u = r * 0.52                                        # icon half-size
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
    elif kind == 'hair':
        base = cy + u * 0.72
        c.drawLine(cx - u, base, cx + u, base, st)
        for i, (hx_, hgt) in enumerate(((-0.55, 1.45), (0.0, 1.05), (0.55, 0.65))):
            p = skia.Path()
            x_ = cx + hx_ * u
            p.moveTo(x_, base)
            p.cubicTo(x_ - 0.22 * u, base - hgt * u * 0.35, x_ + 0.22 * u, base - hgt * u * 0.7, x_, base - hgt * u)
            c.drawPath(p, st)
    elif kind == 'razor':
        head = skia.RRect.MakeRectXY(skia.Rect(cx - u * 0.85, cy - u * 0.95, cx + u * 0.85, cy - u * 0.42), u * 0.12, u * 0.12)
        c.drawRRect(head, st)
        c.drawLine(cx - u * 0.55, cy - u * 0.68, cx + u * 0.55, cy - u * 0.68, paint(g, stroke=0.03))
        c.drawLine(cx, cy - u * 0.42, cx, cy + u * 1.0, st)
        c.drawLine(cx - u * 0.12, cy + u * 0.35, cx + u * 0.12, cy + u * 0.35, paint(g, stroke=0.03))


LAY = {}


def draw_vectors(c):
    # brand, top-left
    lb = draw_logo(c, X0, SAFE + 0.02, 4.6)
    # headline block
    colw = COL_R - X0
    pre_sz, post_sz, sub_sz = 1.02, 1.02, 0.70
    big_lines = CFG['big']
    big_sz = min(colw / F[SERIF].width(''.join(t for t, _ in ln), 1) for ln in big_lines)
    big_sz = min(big_sz, 2.35)

    def head_block(c_, y0):
        y = y0 + pre_sz * 0.72
        if c_:
            text(c_, CFG['pre'], SANS_R, pre_sz, X0 + 0.04, y, C4('cream', 0.92))
        for ln in big_lines:
            y += big_sz * (0.98 if ln is big_lines[0] else 0.86)
            x = X0
            for t, col in ln:
                w_ = F[SERIF].width(t, big_sz)
                if c_:
                    text(c_, t, SERIF, big_sz, x, y, C4(col))
                x += w_
        y += post_sz * 1.32
        if c_:
            text(c_, CFG['post'], SANS_R, post_sz, X0 + 0.04, y, C4('cream', 0.92))
        if CFG['sub']:
            y += sub_sz * 1.90
            for i, ln in enumerate(CFG['sub']):
                if c_:
                    text(c_, ln, SANS_R, sub_sz, X0 + 0.04, y + i * sub_sz * 1.36, C4('sage'))
            y += (len(CFG['sub']) - 1) * sub_sz * 1.36
        return y

    # benefits, laid out from the bottom up so both posters share the same baseline grid
    r = 0.60
    foot_y = TH - SAFE - 0.10
    step = 1.80
    first = foot_y - 1.95 - step * (len(CFG['bens']) - 1)
    rule_y = first - 1.30
    # headline block centred between the logo and the benefits rule
    h_ = head_block(None, 0.0)
    top_free, bot_free = lb + 1.15, rule_y - 1.05
    y = head_block(c, top_free + max(0.0, (bot_free - top_free - h_) / 2))
    LAY['head_bottom'] = y
    c.drawLine(X0, rule_y, X0 + 1.6, rule_y, paint(C4('gold', 0.9), stroke=0.03))
    for i, (kind, label) in enumerate(CFG['bens']):
        cy = first + i * step
        icon(c, kind, X0 + r, cy, r)
        text(c, label, SANS_M, 0.66, X0 + 2 * r + 0.50, cy + 0.66 * 0.36, C4('cream'))
    # footnote
    rl = paint(C4('gold', 0.9), stroke=0.03)
    fsz = min(0.56, (COL_R - X0 - 1.25) / F[SERIF].width(CFG['foot'], 1))
    c.drawLine(X0, foot_y - fsz * 0.34, X0 + 0.95, foot_y - fsz * 0.34, rl)
    text(c, CFG['foot'], SERIF, fsz, X0 + 1.25, foot_y, C4('cream', 0.95))
    # photo frame
    c.drawPath(frame_path(), paint(C4('gold', 0.9), stroke=0.035))
    if CFG.get('ring'):
        rx, ry, rr = CFG['ring']
        c.drawCircle(rx, ry, rr, paint(C4('aqua_hot', 0.95), stroke=0.045))
        c.drawCircle(rx, ry, rr + 0.16, paint(C4('aqua', 0.6), stroke=0.02))


vec = raster_layer(draw_vectors)
final = comp * (1 - vec[..., 3:4]) + vec[..., :3]
final8 = (np.clip(final, 0, 1) * 255 + 0.5).astype(np.uint8)
del vec, final
Image.fromarray(crop_in(final8, 0)).resize((1200, 1200), Image.LANCZOS).save(f'{OUT}/{KEY}_small.png')
print('compose done', KEY, LAY)
if os.environ.get('PREVIEW'):
    Image.fromarray(crop_in(final8, 0)).save(f'{OUT}/{KEY}_trim_preview.png')
    sys.exit(0)

# ================================================================ EXPORTS
TAG = CFG['tag']
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
doc = skia.PDF.MakeDocument(stream, Title=f'leevorá poster 2x2 ft {KEY}', Creator='Adsworm', Producer='Adsworm')
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
slug_p, _ = F[SANS_M].path(f'leevorá · {TAG} · trim 610 x 610 mm · bleed 10 mm · safe 40 mm · CMYK FOGRA39 · raster 150 ppi @ 100%',
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

cm = ImageCms.applyTransform(Image.fromarray(crop_in(final8, BLEED)), to_cmyk)
cm.save(f'{OUT}/{TAG}_PRINT_CMYK_10mm-bleed.tif', compression='tiff_adobe_deflate', dpi=(PPI, PPI), icc_profile=icc_bytes)
proof = ImageCms.applyTransform(cm, to_rgb)
proof.save(f'{OUT}/{TAG}_softproof.png')
tac = np.asarray(cm).astype(np.float32).sum(-1) / 2.55
print('TAC max %.0f p99 %.0f' % (tac.max(), np.percentile(tac, 99)))
Image.fromarray(crop_in(final8, BLEED)).save(f'{OUT}/{TAG}_RIP-MASTER_sRGB_10mm-bleed.tif', compression='tiff_adobe_deflate',
                                             dpi=(PPI, PPI), icc_profile=srgb_bytes)
b0 = int(round(BLEED * PPI))
proof.crop((b0, b0, proof.width - b0, proof.height - b0)).resize((1200, 1200), Image.LANCZOS).save(f'{OUT}/{TAG}_preview.jpg', quality=90)
print('exports done', KEY)
