"""Rank candidate fonts against a caption crop. Reference: a coloured caption word on a dark frame gives the cleanest mask (pick the frame with the most contrast).
Each candidate is rendered at weights 500-800, scaled to the reference cap-to-baseline height, and scored by mask IoU after best x/y shift."""
import sys, glob, os, numpy as np
from PIL import Image, ImageDraw, ImageFont
ref_img, text, box = sys.argv[1], sys.argv[2], tuple(map(int, sys.argv[3].split(',')))
im = np.asarray(Image.open(ref_img).convert('RGB')).astype(int)[box[1]:box[3], box[0]:box[2]]
r, g, b = im[..., 0], im[..., 1], im[..., 2]; ref = ((r > 150) & (r - b > 45) & (g > 120))
ys, xs = np.where(ref); ref = ref[ys.min():ys.max() + 1, xs.min():xs.max() + 1]; RH, RW = ref.shape
res = []
for f in sorted(glob.glob(os.path.join(sys.argv[4], '*.ttf'))):
    for wght in (500, 600, 700, 800):
        try:
            font = ImageFont.truetype(f, 200)
            try: font.set_variation_by_axes([wght] if 'opsz' not in f and 'wdth' not in f else ([28, wght] if 'opsz' in f and 'wdth' not in f else [14, 100, wght]))
            except Exception:
                if wght != 600: continue
            c = Image.new('L', (2600, 400), 0); d = ImageDraw.Draw(c); d.text((20, 60), text, font=font, fill=255)
            m = np.asarray(c) > 110; yy, xx = np.where(m); m = m[yy.min():yy.max() + 1, xx.min():xx.max() + 1]
            s = RH / m.shape[0]; mw = int(round(m.shape[1] * s))
            mm = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).resize((mw, RH), Image.LANCZOS)) > 127
            W = max(RW, mw) + 12; A = np.zeros((RH + 12, W), bool); A[6:6 + RH, 6:6 + RW] = ref
            best = 0
            for dx in range(-6, 7, 2):
                for dy in (-2, 0, 2):
                    B = np.zeros_like(A); x0 = 6 + dx; B[6 + dy:6 + dy + RH, max(x0, 0):max(x0, 0) + mw] = mm[:, :W - max(x0, 0)][:, :max(0, min(mw, W - max(x0, 0)))]
                    iou = (A & B).sum() / max(1, (A | B).sum()); best = max(best, iou)
            res.append((best, os.path.basename(f), wght, round(mw / RW, 3)))
        except Exception as e:
            pass
res.sort(reverse=True)
print(f'reference mask {RW}x{RH} px')
for r_ in res[:16]: print(f'  IoU {r_[0]:.3f}  {r_[1]:22s} wght {r_[2]}  width ratio {r_[3]}')
