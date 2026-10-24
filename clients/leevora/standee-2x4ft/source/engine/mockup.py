#!/usr/bin/env python3
"""Simple honest mockup: both faces in an aluminium light-box standee, day and night."""
import numpy as np, cv2
from PIL import Image

ROOT = '/tmp/claude-0/-home-user-Adsworm/3d8d5e5a-8f36-56e6-be63-644bad3ee2df/scratchpad'
OUT = f'{ROOT}/out'
Image.MAX_IMAGE_PIXELS = None
S = 22                       # px per inch in the mockup
PW, PH = 24, 48              # visible face
FR = 1.1                     # frame width
POLE, BASE = 16, 2.2         # pole height, base plate height (in)


def load(path):
    im = Image.open(path).convert('RGB')
    w, h = im.size
    b = round(w * (10 / 25.4) / (24 + 2 * 10 / 25.4))          # strip 10 mm bleed if present
    if abs(h / w - 2) > 0.01:
        im = im.crop((b, b, w - b, h - b))
    return np.asarray(im.resize((PW * S, PH * S), Image.LANCZOS)).astype(np.float32) / 255


def blur(a, s):
    k = int(s * 3) * 2 + 1
    return cv2.GaussianBlur(a, (k, k), s)


def scene(faces, night):
    gap = 14
    W = int((len(faces) * (PW + 2 * FR) + (len(faces) + 1) * gap) * S)
    Hs = int((PH + 2 * FR + POLE + BASE + 16) * S)
    yy = np.linspace(0, 1, Hs)[:, None, None]
    ground_y = int((8 + PH + 2 * FR + POLE + BASE) * S)
    if night:
        img = np.ones((Hs, W, 3), np.float32) * np.array([0.020, 0.026, 0.034])
        img[ground_y:] = np.array([0.035, 0.038, 0.042])
    else:
        img = np.ones((Hs, W, 3), np.float32) * (np.array([0.80, 0.78, 0.74]) - 0.06 * yy)
        img[ground_y:] = np.array([0.62, 0.60, 0.57])
    light = np.zeros_like(img)
    for i, f in enumerate(faces):
        x0 = int(((i + 1) * gap + i * (PW + 2 * FR)) * S)
        y0 = int(8 * S)
        fw, fh = int((PW + 2 * FR) * S), int((PH + 2 * FR) * S)
        # pole + base
        pc = x0 + fw // 2
        img[y0 + fh:ground_y - int(BASE * S), pc - S: pc + S] = [0.10, 0.11, 0.12] if night else [0.28, 0.29, 0.30]
        img[ground_y - int(BASE * S):ground_y, pc - int(9 * S):pc + int(9 * S)] = [0.08, 0.09, 0.10] if night else [0.24, 0.25, 0.26]
        # frame
        img[y0:y0 + fh, x0:x0 + fw] = [0.16, 0.17, 0.18] if night else [0.42, 0.43, 0.44]
        img[y0:y0 + 3, x0:x0 + fw] += 0.15
        face = f
        if night:
            lin = face ** 2.2
            em = 1 - np.exp(-lin * 3.2)
            face = np.clip(em + blur(em ** 2, 0.25 * S) * 0.5, 0, 1) ** (1 / 2.2)
            m = face.mean((0, 1))
            spill = np.zeros_like(img)
            spill[y0 - S * 4:y0 + fh + S * 4, x0 - S * 4:x0 + fw + S * 4] = m * 0.55
            light += blur(spill, 9 * S)
            gy = np.arange(ground_y, Hs)
            pool = np.exp(-((np.arange(W) - pc) / (16 * S)) ** 2)[None, :] * np.exp(-(gy - ground_y) / (6 * S))[:, None]
            light[ground_y:] += pool[..., None] * m * 0.6
        else:
            shade = np.zeros_like(img)
            shade[y0 + 6:y0 + fh + 6, x0 + 10:x0 + fw + 10] = 0.18
            img -= blur(shade, 1.2 * S)
        img[y0 + int(FR * S):y0 + int(FR * S) + PH * S, x0 + int(FR * S):x0 + int(FR * S) + PW * S] = face
    img = np.clip(img + light * (1 if night else 0), 0, 1)
    return Image.fromarray((img * 255).astype(np.uint8))


for mode in ('day', 'night'):
    faces = [load(f'{OUT}/LEEVORA_Standee_2x4ft_Side{s}_softproof.png') for s in 'AB']
    scene(faces, mode == 'night').save(f'{OUT}/MOCKUP_standee_{mode}.jpg', quality=90)
print('ok')
