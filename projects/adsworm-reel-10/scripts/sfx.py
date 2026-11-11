"""Synthesize the reel's sound effects → public/sfx/*.wav (no samples, no licences: numpy only).

Each effect is triggered from the component that draws the thing it belongs to (src/reel/Sfx.tsx), so
sound and picture can't drift. Peaks are normalised to 0.8; the per-use volume is set in the TSX.

    python3 scripts/sfx.py
"""
import wave
from pathlib import Path

import numpy as np
from scipy.signal import butter, sosfilt

SR = 48000
OUT = Path(__file__).resolve().parent.parent / "public/sfx"
rng = np.random.default_rng(7)


def T(d):
    return np.arange(int(d * SR)) / SR


def lp(x, hz):
    return sosfilt(butter(2, hz, "low", fs=SR, output="sos"), x)


def hp(x, hz):
    return sosfilt(butter(2, hz, "high", fs=SR, output="sos"), x)


def sweep(f0, f1, d, curve=1.0):
    t = T(d)
    f = f0 + (f1 - f0) * (t / d) ** curve
    return np.sin(2 * np.pi * np.cumsum(f) / SR)


def pop():  # a soft "bloop": something landed
    t = T(0.09)
    f = 360 + 620 * np.exp(-t * 55)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 40)


def tick():  # a checkbox, a typed key
    t = T(0.045)
    return (np.sin(2 * np.pi * 2300 * t) + 0.4 * rng.standard_normal(len(t))) * np.exp(-t * 130)


def whoosh():  # a board flying in
    t = T(0.38)
    return lp(rng.standard_normal(len(t)), 2400) * np.sin(np.pi * t / 0.38) ** 2


def swish():  # a sticker slapping on
    t = T(0.16)
    return hp(lp(rng.standard_normal(len(t)), 5200), 900) * np.sin(np.pi * t / 0.16) ** 1.5


def thump():  # the hook's zoom-punch, a number landing
    t = T(0.45)
    f = 48 + 90 * np.exp(-t * 28)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9) + rng.standard_normal(len(t)) * np.exp(-t * 220) * 0.3


def ding():  # good news: a tick turning green, the fix
    t = T(0.55)
    return (np.sin(2 * np.pi * 1046.5 * t) + 0.6 * np.sin(2 * np.pi * 1568 * t) + 0.25 * np.sin(2 * np.pi * 2093 * t)) * np.exp(-t * 7.5)


def buzz():  # the wrong move: a strike-through, a cross
    t = T(0.2)
    x = np.sign(np.sin(2 * np.pi * 118 * t)) * 0.6 + np.sin(2 * np.pi * 59 * t)
    return lp(x, 900) * np.minimum(1, t / 0.008) * np.exp(-t * 14)


def riser():  # tension before a reveal; cut off dead at the end
    d = 0.55
    t = T(d)
    x = 0.5 * sweep(220, 880, d, 2.0) + lp(rng.standard_normal(len(t)), 3000) * 0.7
    return x * (t / d) ** 2


def huh():  # a question mark, a raised eyebrow
    d = 0.16
    return sweep(330, 620, d, 0.7) * np.sin(np.pi * T(d) / d) ** 0.6


def gasp():  # a shock reaction: quick up-chirp with a noise breath
    d = 0.2
    t = T(d)
    return (0.7 * sweep(500, 1150, d, 0.5) + 0.5 * hp(rng.standard_normal(len(t)), 1800)) * np.sin(np.pi * t / d)


def cash():  # money: two bright coins
    t = T(0.5)
    a = np.sin(2 * np.pi * 1975 * t) * np.exp(-t * 16)
    b = np.concatenate([np.zeros(int(0.07 * SR)), np.sin(2 * np.pi * 2637 * T(0.43)) * np.exp(-T(0.43) * 11)])
    return a + b


FX = {"pop": pop, "tick": tick, "whoosh": whoosh, "swish": swish, "thump": thump, "ding": ding, "buzz": buzz, "riser": riser, "huh": huh, "gasp": gasp, "cash": cash}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    lens = {}
    for name, fn in FX.items():
        x = fn()
        f = int(0.004 * SR)
        x[:f] *= np.linspace(0, 1, f)
        x[-f:] *= np.linspace(1, 0, f)
        x = x / np.max(np.abs(x)) * 0.8
        with wave.open(str(OUT / f"{name}.wav"), "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(SR)
            w.writeframes((x * 32767).astype("<i2").tobytes())
        lens[name] = int(np.ceil(len(x) / SR * 30)) + 1
    print("sfx:", ", ".join(f"{k} {v}f" for k, v in lens.items()))


if __name__ == "__main__":
    main()
