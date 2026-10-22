"""Talking-head frames: align AI-edited expression shots to the base bust and paste only the changed
region (mouth, or the whole face for a wink) so swapping frames never jitters. Output is keyed PNG.

    python3 scripts/faces.py aman base.png closed=a.png half=base.png open=b.png wink=c.png --mouth 400,300,600,420 --face 360,170,660,450
"""
import argparse
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "public/faces"


def gray(im):
    return np.asarray(im.convert("L"), dtype=np.float32)


def shift_of(a, b):
    """Translation (dy, dx) that maps b onto a — phase correlation on edges."""
    fa, fb = np.fft.fft2(np.gradient(a)[0]), np.fft.fft2(np.gradient(b)[0])
    r = fa * np.conj(fb)
    r /= np.abs(r) + 1e-9
    c = np.abs(np.fft.ifft2(r))
    dy, dx = np.unravel_index(np.argmax(c), c.shape)
    h, w = a.shape
    return (dy - h if dy > h // 2 else dy), (dx - w if dx > w // 2 else dx)


def key(im):
    a = np.asarray(im.convert("RGB")).astype(np.int16)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    bg = (g > 90) & (g > r * 1.35) & (g > b * 1.35)
    alpha = np.where(bg, 0, 255).astype(np.uint8)
    soft = np.asarray(Image.fromarray(alpha).filter(ImageFilter.GaussianBlur(1)))
    alpha = np.minimum(alpha, soft).astype(np.uint8)
    spill = (~bg) & (g > np.maximum(r, b) + 12)
    g2 = np.where(spill, np.maximum(r, b), g)
    return Image.fromarray(np.dstack([np.stack([r, g2, b], -1).clip(0, 255).astype(np.uint8), alpha]), "RGBA")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("who")
    ap.add_argument("base")
    ap.add_argument("states", nargs="+")
    ap.add_argument("--mouth", required=True)
    ap.add_argument("--face", required=True)
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    base = Image.open(a.base).convert("RGB")
    W, H = base.size
    for spec in a.states:
        name, path = spec.split("=")
        ed = Image.open(path).convert("RGB").resize((W, H), Image.LANCZOS)
        box = [int(v) for v in (a.face if name == "wink" else a.mouth).split(",")]
        dy, dx = shift_of(gray(base), gray(ed))
        ed = ed.transform((W, H), Image.AFFINE, (1, 0, -dx, 0, 1, -dy), resample=Image.BICUBIC)
        mask = Image.new("L", (W, H), 0)
        x0, y0, x1, y1 = box
        m = Image.new("L", (x1 - x0, y1 - y0), 0)
        from PIL import ImageDraw
        ImageDraw.Draw(m).ellipse((6, 6, x1 - x0 - 6, y1 - y0 - 6), fill=255)
        mask.paste(m.filter(ImageFilter.GaussianBlur(10)), (x0, y0))
        out = Image.composite(ed, base, mask)
        key(out).save(OUT / f"{a.who}-{name}.png", optimize=True)
        print(f"{a.who}-{name}: shift dx={dx} dy={dy}")


if __name__ == "__main__":
    main()
