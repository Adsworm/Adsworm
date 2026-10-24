#!/usr/bin/env python3
"""Build the audit + vendor spec PDFs (HTML -> Chromium PDF) and the comparison images."""
import json, os, subprocess
from PIL import Image

ROOT = '/tmp/claude-0/-home-user-Adsworm/3d8d5e5a-8f36-56e6-be63-644bad3ee2df/scratchpad'
OUT, DOCS, FONTS = f'{ROOT}/out', f'{ROOT}/docs', f'{ROOT}/fonts'
os.makedirs(f'{DOCS}/img', exist_ok=True)
Image.MAX_IMAGE_PIXELS = None
L = {s: json.load(open(f'{OUT}/side{s}_layout.json')) for s in 'AB'}

# ---------------------------------------------------------------- images
def thumb(path, w):
    im = Image.open(path).convert('RGB')
    return im.resize((w, round(w * im.height / im.width)), Image.LANCZOS)

orig = thumb(f'{ROOT}/src/orig_100-1.png', 600)
a = thumb(f'{OUT}/LEEVORA_Standee_2x4ft_SideA_softproof.png', 600)
b = thumb(f'{OUT}/LEEVORA_Standee_2x4ft_SideB_softproof.png', 600)
for nm, im in (('orig', orig), ('A', a), ('B', b)):
    im.save(f'{DOCS}/img/{nm}.jpg', quality=88)
for s in 'AB':
    for v in ('day', 'night'):
        thumb(f'{OUT}/LEEVORA_Standee_2x4ft_Side{s}_{v}_preview.jpg', 420).save(f'{DOCS}/img/{s}_{v}.jpg', quality=86)
# original's AI tells: crop of the embedded photo
ph = Image.open(f'{ROOT}/src/img-000.png').convert('RGB')
ph.crop((840, 380, 1254, 820)).resize((360, 383), Image.LANCZOS).save(f'{DOCS}/img/orig_tell.jpg', quality=88)
ph.resize((360, 360), Image.LANCZOS).save(f'{DOCS}/img/orig_photo.jpg', quality=88)

FONT_CSS = f'''
@font-face {{ font-family: Gloock; src: url(file://{FONTS}/Gloock-Regular.ttf); }}
@font-face {{ font-family: Inst; src: url(file://{FONTS}/InstrumentSans-Regular.ttf); font-weight: 400; }}
@font-face {{ font-family: Inst; src: url(file://{FONTS}/InstrumentSans-Medium.ttf); font-weight: 500; }}
@font-face {{ font-family: Inst; src: url(file://{FONTS}/InstrumentSans-SemiBold.ttf); font-weight: 600; }}
@font-face {{ font-family: Inst; src: url(file://{FONTS}/InstrumentSans-Bold.ttf); font-weight: 700; }}
@font-face {{ font-family: Deva; src: url(file://{FONTS}/NotoSansDevanagari-VF.ttf); }}
'''
BASE_CSS = FONT_CSS + '''
@page { size: A4; margin: 14mm 15mm 14mm; }
* { box-sizing: border-box; }
body { margin: 0; font-family: Inst, Deva, sans-serif; color: #17211F; font-size: 9.6pt; line-height: 1.45; }
.page { break-before: page; }
.page:first-child { break-before: auto; }
tr, .box, .fig, .row { break-inside: avoid; }
h2, h3 { break-after: avoid; }
h1 { font-family: Gloock; font-weight: 400; font-size: 27pt; line-height: 1.05; margin: 0 0 4mm; color: #0D2622; }
h2 { font-family: Gloock; font-weight: 400; font-size: 15.5pt; margin: 6mm 0 2.5mm; color: #0D2622; }
h3 { font-size: 9.6pt; font-weight: 700; margin: 3.5mm 0 1mm; text-transform: uppercase; letter-spacing: .08em; color: #8A6A2F; }
.kicker { font-weight: 600; letter-spacing: .18em; text-transform: uppercase; font-size: 7.6pt; color: #8A6A2F; }
.lede { font-size: 11pt; color: #33413E; max-width: 160mm; }
table { width: 100%; border-collapse: collapse; margin: 1.5mm 0 3mm; }
th { text-align: left; font-size: 7.4pt; letter-spacing: .1em; text-transform: uppercase; color: #6B7A76; font-weight: 600; border-bottom: 1px solid #C9D1CE; padding: 1.4mm 2mm; }
td { vertical-align: top; padding: 1.6mm 2mm; border-bottom: 1px solid #E3E8E6; }
td.n { width: 7mm; color: #8A6A2F; font-weight: 700; }
.sev { display: inline-block; font-size: 6.8pt; font-weight: 700; letter-spacing: .06em; padding: .3mm 1.6mm; border-radius: 2mm; text-transform: uppercase; }
.s1 { background: #F6D9D4; color: #8E2A1C; } .s2 { background: #F7EBCF; color: #7A5A12; } .s3 { background: #E1ECE8; color: #2D5A4E; }
.row { display: flex; gap: 5mm; align-items: flex-start; }
.col { flex: 1; }
.fig { text-align: center; font-size: 7.6pt; color: #6B7A76; }
.fig img { width: 100%; border-radius: 1.5mm; display: block; margin-bottom: 1.5mm; }
.box { background: #F3F6F5; border-left: 3px solid #B8914B; padding: 3mm 4mm; margin: 3mm 0; }
.dark { background: #0D2622; color: #EDE7DA; }
.dark h1, .dark h2 { color: #FBF3E4; }
.foot { display: none; }
.hi { font-family: Deva, Inst; }
ul { margin: 1mm 0 2mm 4.5mm; padding: 0; } li { margin: .6mm 0; }
code { font-family: Inst; font-weight: 600; background: #EEF1F0; padding: 0 1mm; border-radius: 1mm; }
'''

def page(inner, foot, cls=''):
    return f'<section class="page {cls}">{inner}<div class="foot"><span>leevorá · 2 × 4 ft LED standee</span><span>{foot}</span></div></section>'

# ================================================================ AUDIT
MISTAKES = [
    ('Stopping power', [
        ('s1', 'No stopper. The hero is a woman in profile with her head inside a machine. There is no eye contact and no emotion, and from 8 m it reads as a white appliance. Faces looking at you stop people. Machines don\'t.'),
        ('s1', 'Not planned for a backlit box. Lighter inks let more light through, and the biggest light area here is the cream CTA box at knee height. At night it turns into a glaring white slab, and the sage-grey headline glows weakly above it.'),
        ('s1', 'No hook. "Complimentary Skin & hair analysis." is a label, not a reason to stop. It has no curiosity, no problem and no payoff.'),
        ('s1', 'The offer is diluted. "Free" appears five times in five styles: Complimentary, the FREE pill, the Free 1 Month badge, "Book your free…" and the *Complimentary footnote. It reads as desperate rather than premium, and the eye can\'t tell which one is the offer.'),
        ('s2', '"For the first month" is vague. A passer-by doesn\'t know when you opened, so the deadline means nothing. Fixed: "Launch month only".'),
        ('s2', 'One audience on a two-faced unit. Only women and skin are shown, though the offer includes hair. Men\'s hair fall is one of the biggest clinic categories in Delhi, and the second face of the standee is wasted on a copy.'),
    ]),
    ('Hierarchy & layout', [
        ('s1', 'Ten blocks compete for attention: NOW OPEN, logo, Complimentary, headline, pill, arch photo, badge, three features, CTA box and footnote. There is no single entry point.'),
        ('s2', 'The circular badge text ("· HAIR · LIMITED PERIOD · SKIN ·") can\'t be read beyond 1 m. It is a template cliché and it collides with the arch.'),
        ('s2', 'The feature row is jargon. "8-Spectrum" and "17 Concerns precisely mapped" mean nothing to a passer-by, and the 7 mm sublabels can only be read within about 1 m.'),
        ('s2', 'The arch-frame photo is the 2023–24 Canva clinic look. It makes the piece feel template-built, and the client said this must not look generic.'),
        ('s2', 'The thin gold border sits about 33 mm from the edge. The frame lip (15–25 mm) will crop it unevenly, so it will look crooked in a light box, and its hairline weight disappears on flex.'),
    ]),
    ('Copy', [
        ('s3', 'Casing is inconsistent: "Skin & hair" has a capital S and a lower-case h, and the pill mixes caps sans ("FREE") with lower-case serif.'),
        ('s2', 'The phone number is printed as an unbroken 10-digit block (8076467352). Indians chunk numbers 5-5, so set it as 80764 67352. That is easier to read, remember and dial.'),
        ('s1', 'No WhatsApp and no QR code. WhatsApp is the main booking channel in India and the only way to capture someone who won\'t cold-call. With no QR, you also can\'t measure what the standee brings in.'),
        ('s3', 'The footnote has about 6 mm caps, so nobody can read it, and it repeats the offer a fifth time.'),
    ]),
    ('"Looks AI-generated" (the client\'s #1 concern)', [
        ('s1', 'The button on the device reads "B33°". Gibberish text is the classic AI-image tell, and people spot it.'),
        ('s1', 'The tablet UI is fake: the icons are nonsense, and the face on the screen is a different woman (frontal, blue-tinted) from the one being scanned (in profile).'),
        ('s2', 'Her posture doesn\'t fit the device: her chin floats above the chin-rest. The plastic, unbranded machine and the generic "luxury clinic" blur add to the synthetic feel.'),
        ('s2', 'The photo is a screenshot of an older layout. The embedded image still contains the old arch ring, the green corners and half of the old "Free 1 MONTH" badge, which creates a risk of ghost edges.'),
    ]),
    ('Print production', [
        ('s1', 'Resolution: a 1254 × 1254 px photo is stretched to about 375 mm, which is 85 ppi. Backlighting shows pixelation and JPEG blocks because light passes through them. You need 150 ppi or more at 100%.'),
        ('s1', 'The file is RGB (sRGB) with no CMYK build, so the deep green and the gold will shift unpredictably on Delhi RIPs, which often run unmanaged.'),
        ('s1', 'There is no bleed (the page is exactly 24 × 48 in) and no safe area. Frames hide 15–25 mm and anything near the edge is at risk.'),
        ('s2', 'The fonts are live, not outlined. CorelDRAW-based shops will substitute Gloock and Instrument Sans.'),
        ('s2', 'There is no backlit prep: no ink-density plan, no LED colour temperature, and nothing stopping the light areas from burning out.'),
    ]),
]

FIXES = [
    ('Stop from 10 m', 'A face at 1.5× life size makes direct eye contact, and a glowing scan line cuts across it. Below the line the skin is shown the way the clinic\'s machine sees it. That curiosity gap is the stopper.'),
    ('One idea, one line', '"Your mirror only shows half." pays off the picture in one look. Side B uses the man\'s own words: "Hair fall has a reason."'),
    ('Built for a backlit box', 'The whole sheet is lit from behind, and lighter inks let more light through. So the picture is planned that way: the face, cream headline and gold offer are the lightest areas and read first, and the deep-green surround stays rich. Skin highlights are rolled off and the QR tile is warm grey, so nothing burns out into a white patch.'),
    ('3D inside the picture', 'The depth is in the creative itself, with no add-ons. Side A\'s head sits in front of the headline, the beam throws light onto the skin above and below it, and the scanned half is lit differently from the natural half.'),
    ('Two faces, two audiences', 'Side A is a woman and skin. Side B is a man and hair, with the scan above the line on the scalp and the thin temples flagged in gold. The offer word order flips ("Hair & Skin") so the first noun matches the face.'),
    ('"Free" once, premium tone', 'One gold offer line: "Free Skin & Hair Analysis / LAUNCH MONTH ONLY". The proof line uses the clinic\'s own device wording: "8-spectrum AI skin imaging · 17 concerns mapped · Expert-led plan".'),
    ('A measurable CTA', 'A 123 mm QR code (37 modules, 2.7 mm each) opens WhatsApp with a pre-filled message. The message says "skin" on Side A and "hair" on Side B, so staff can tell which face brought the lead. It was tested and decodes at full size and at phone-at-1.5 m scale. Below it: "Scan or call to book", one number (+91 80764 67352), then "Or visit us directly at ↑ 2ND FLOOR, THIS BUILDING".'),
    ('Nothing synthetic to spot', 'No machines, screens, invented UI text, face meshes or template brackets. The UV view and the rings are computed from the photo\'s own skin, so the rings sit on real spots. Labels use words, not fake numbers, and the fine print says "Posed by models. Scan imagery is illustrative."'),
    ('Print-grade files', 'CMYK FOGRA39 with TAC ≤ 300%, 150 ppi at 100%, 10 mm bleed, 40 mm safe area, outlined type, crop marks with TrimBox and BleedBox, a flex-wrap version and an sRGB master for RIPs with a media profile.'),
]

DECISIONS = [
    ('Value anchor', 'Add <b>"Worth ₹____"</b> under the offer. It is the strongest single upgrade to a "free" offer. I left it out because I won\'t print an invented price. Send me the real number and the change takes 2 minutes.'),
    ('WhatsApp', 'The QR opens <code>wa.me/918076467352</code>. Confirm that this number is on WhatsApp (ideally WhatsApp Business with a greeting message) <b>before printing</b>.'),
    ('Hair claim', 'Side B says "Hair & scalp imaging · Density mapped". Confirm that the hair analysis includes close-up scalp imaging. If it doesn\'t, I swap the line.'),
    ('Exact dates', 'If the launch month has fixed dates, "TILL 30 NOV" beats "LAUNCH MONTH ONLY" for urgency. Send me the dates and I\'ll swap it.'),
    ('Launch month', 'If you want to reuse the panel after launch, ask the vendor to print "LAUNCH MONTH ONLY" as a separate vinyl strip, so it can be peeled off later.'),
    ('Which face faces the traffic', 'Side A (woman/skin) should face the direction most of the footfall comes from. If the unit stands side-on to the road, it doesn\'t matter.'),
    ('Photos', 'Both portraits are photoreal generated models with no model release needed, and the fine print says "Scan imagery is illustrative". The best long-term upgrade is a real 30-minute shoot of your own clients or staff at your own scanner, which the engine can re-render the same day.'),
]


def audit_html():
    p1 = f'''
<div class="kicker">Design audit &amp; redesign · Adsworm</div>
<h1>leevorá standee:<br>what was wrong, and the fix.</h1>
<p class="lede">The original is clean but quiet. It works as a flyer, not as a street stopper. It has no hook, no night plan, a diluted offer and an AI photo with visible tells, and the print file isn't backlit-ready (85 ppi, RGB, no bleed). The redesign makes one idea readable from 10 m, and it reads just as strongly when the box is lit at night.</p>
<div class="row" style="margin-top:6mm">
  <div class="col fig"><img src="img/orig.jpg">Before: original</div>
  <div class="col fig"><img src="img/A.jpg">After: Side A (skin)</div>
  <div class="col fig"><img src="img/B.jpg">After: Side B (hair)</div>
</div>'''
    rows = ''
    k = 0
    pages = [p1]
    groups_p2 = MISTAKES[:3]
    groups_p3 = MISTAKES[3:]

    def table(groups):
        nonlocal k
        out = ''
        for g, items in groups:
            out += f'<h3>{g}</h3><table>'
            for sev, txt in items:
                k += 1
                lab = {'s1': 'Critical', 's2': 'Major', 's3': 'Minor'}[sev]
                out += f'<tr><td class="n">{k:02d}</td><td>{txt}</td><td style="width:20mm;text-align:right"><span class="sev {sev}">{lab}</span></td></tr>'
            out += '</table>'
        return out
    p2 = '<div class="kicker">Part 1</div><h2>24 mistakes in the original</h2>' + table(groups_p2)
    p3 = table(groups_p3) + '''<div class="row" style="margin-top:2mm"><div class="col fig" style="max-width:62mm"><img src="img/orig_photo.jpg">Embedded photo: the old arch and badge are baked in</div>
<div class="col fig" style="max-width:62mm"><img src="img/orig_tell.jpg">"B33°" gibberish and a different face on the screen</div></div>'''
    fx = ''.join(f'<tr><td style="width:42mm"><b>{t}</b></td><td>{d}</td></tr>' for t, d in FIXES)
    p4 = f'<div class="kicker">Part 2</div><h2>What changed, and why it works</h2><table>{fx}</table>'
    dn = ''.join(f'''<div class="col fig"><img src="img/{s}_{v}.jpg">{s} · {lab}</div>''' for s in 'AB' for v, lab in (('day', 'day'), ('night', 'lit at night')))
    p5 = f'''<div class="kicker">Part 3</div><h2>Day vs lit at night (backlit box, simulated)</h2>
<div class="row">{dn}</div>
<div class="box"><b>How it behaves lit.</b> The whole sheet is lit from behind. Light inks let more light through, so the face, headline and gold offer read first and the deep green stays rich and dark around them. The QR tile is warm grey (C8 M8 Y20 K25), not white, so it doesn't flare, and skin highlights are rolled off so faces don't burn out.</div>'''
    dc = ''.join(f'<tr><td style="width:36mm"><b>{t}</b></td><td>{d}</td></tr>' for t, d in DECISIONS)
    p6 = f'<div class="kicker">Part 4</div><h2>Confirm before printing</h2><table>{dc}</table>'
    return f'<html><head><meta charset="utf-8"><style>{BASE_CSS}</style></head><body>' + \
        page(p1, '') + page(p2 + p3, '') + page(p4, '') + page(p5, '') + page(p6, '') + '</body></html>'


# ================================================================ VENDOR SPEC
def vendor_html():
    files = [
        ('SideA_PRINT_CMYK.pdf / SideB_PRINT_CMYK.pdf', '<b>Master print file.</b> 1:1, CMYK FOGRA39 (output intent embedded), type outlined, 10 mm bleed, crop marks, TrimBox/BleedBox set.'),
        ('Side*_PRINT_CMYK_10mm-bleed.tif', 'Same artwork, flattened. 630 × 1239 mm, 150 ppi, CMYK, ICC embedded. Use it if your RIP prefers TIFF.'),
        ('Side*_FLEX-WRAP_CMYK_75mm-extension.tif', 'Only for flex that wraps around the frame: 760 × 1369 mm. The artwork is centred and the extra 75 mm per side is background only.'),
        ('Side*_RIP-MASTER_sRGB_10mm-bleed.tif', 'The same artwork in sRGB. Use it <b>only</b> if your RIP has an ICC profile for the actual backlit media. Otherwise print the CMYK files.'),
        ('Side*_softproof.png, *_day/_night previews', 'Colour reference only. Do not print these.'),
    ]
    ft = ''.join(f'<tr><td style="width:62mm"><code>{a}</code></td><td>{b}</td></tr>' for a, b in files)
    spec = [
        ('Unit', 'Double-sided LED light-box standee, 2 × 4 ft (610 × 1219 mm visible face), portrait, outdoor. <b>Two different artworks</b>: Side A (woman/skin) and Side B (man/hair).'),
        ('Build (recommended)', 'Aluminium profile box, 100–125 mm deep, hinged faces. Each face: 2 mm clear UV-stable polycarbonate → <b>backlit PET film 175–200 µm</b> printed 2× density → 3 mm opal acrylic. A 3 mm white ACP <b>centre divider</b> stops light and image bleeding between faces. Est. ₹14–25k.'),
        ('Build (budget)', '"LED glow sign" frame with 440–510 gsm <b>backlit flex</b> (not frontlit/star flex), Konica solvent in <b>backlit mode</b>, the same LEDs and the divider. Use the FLEX-WRAP file. Est. ₹6–11k.'),
        ('Print', '150 ppi at 100% (supplied). Backlit mode / 2-pass double-strike. Eco-solvent 720×1440, 8+ pass for film. Let solvent prints dry ≥24 h before sealing.'),
        ('Colour', 'Files are already CMYK FOGRA39 (TAC ≤ 300%). <b>Don\'t re-convert or "boost" them.</b> If you have a media ICC profile for backlit film or flex, print the sRGB master through it instead. Run a strip test (dark green, gold, cream, aqua, skin, QR) on the real media in the real box, lit and unlit, and send me a photo before the full run.'),
        ('Size & margins', 'Trim 610 × 1219 mm. Bleed 10 mm per side. All type, logo and the QR sit ≥40 mm inside the trim. Send me the frame drawing if the lip is wider than 25 mm.'),
        ('LEDs', 'Back-lit modules (not edge-lit): 12 V, 3 × SMD2835 lensed (160–175°), IP65+, on a 90–110 mm grid with the edge row ≤50 mm from the frame. <b>4000 K neutral white, CRI ≥80, one bin for both faces.</b> Avoid 6500 K: it greys the cream and turns the gold green. Fit a PWM dimmer, photocell, timer (off 23:00), 30 mA RCCB and earthing.'),
        ('Evenness test', 'Light the box with a blank face: no LED dots visible at 1 m and no dark corners.'),
    ]
    st = ''.join(f'<tr><td style="width:36mm"><b>{a}</b></td><td>{b}</td></tr>' for a, b in spec)
    check = ['Frame drawing: outer size, visible area, lip, depth', 'Printer, media, mode and ICC named in writing',
             'Strip test photo (lit + unlit) approved', 'A 1:1 face crop proof approved', 'Side A / Side B confirmed, and which faces the street',
             'QR on the printed proof scans with two phones (Android + iPhone)', 'Blank-face LED test: no dots, matched 4000 K',
             'IP65, RCCB, earthing, timer set, 2-hour burn-in', 'Base ballasted or anchored against wind']
    ct = ''.join(f'<li>☐ {c}</li>' for c in check)
    hindi = '''<div class="box hi"><b>वेंडर के लिए ज़रूरी बातें:</b> (1) फ़ाइल पहले से CMYK में है, दोबारा convert या colour "boost" मत करना। (2) Backlit flex/film ही लगाना, frontlit/star flex नहीं। (3) LED 4000K (neutral white) लगाना, 6500K नहीं। (4) पूरी printing से पहले strip test का lit और unlit फ़ोटो भेजना। (5) बीच में divider ज़रूर लगाना, ताकि एक side की light दूसरी side पर न दिखे। (6) Text, logo और QR को frame के lip के नीचे मत छुपाना, ये किनारे से 40 mm अंदर हैं।</div>'''
    p1 = f'''<div class="kicker">Production spec · for the print vendor</div>
<h1>leevorá LED standee, 2 × 4 ft, double-sided</h1>
<p class="lede">Print-ready files are supplied. Please follow this sheet exactly and confirm the checklist on page 2 before the full run.</p>
<h2>Files supplied</h2><table>{ft}</table>
<h2>Specification</h2><table>{st}</table>'''
    p2 = f'''{hindi}
<div class="row"><div class="col"><h2>Pre-press checklist</h2><ul style="list-style:none;margin-left:0">{ct}</ul></div>
<div class="col fig" style="max-width:38mm;margin-top:8mm"><img src="img/A.jpg">Side A</div><div class="col fig" style="max-width:38mm;margin-top:8mm"><img src="img/B.jpg">Side B</div></div>
<p style="font-size:7.6pt;color:#6B7A76">Price figures are estimates from Delhi listings (ex-GST, ex-installation), not quotes.</p>'''
    return f'<html><head><meta charset="utf-8"><style>{BASE_CSS}</style></head><body>' + page(p1, '') + page(p2, '') + '</body></html>'


for name, html in (('leevora_standee_DESIGN-AUDIT', audit_html()), ('leevora_standee_VENDOR-SPEC', vendor_html())):
    hp = f'{DOCS}/{name}.html'
    open(hp, 'w').write(html)
    subprocess.run(['node', f'{ROOT}/engine/render_pdf.js', hp, f'{DOCS}/{name}.pdf'], check=True)
    print('wrote', name)
