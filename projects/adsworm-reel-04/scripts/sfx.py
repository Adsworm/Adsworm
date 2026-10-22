"""Sound design from the timeline → public/sfx.wav (sits under the voice; the master is loudnormed).

Whoosh on every camera move, a low thump on every number punch, a digital crunch on the two glitches,
UI ticks on clicks, and a quiet drone bed that starts and ends at the same level so the loop is seamless.
"""
import json
import re
import subprocess
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
SR = 48000
tl = json.loads((ROOT / "src/reel/timeline.json").read_text())
dur = tl["durationInFrames"] / tl["fps"]
n = int(dur * SR)
mix = np.zeros(n, np.float32)
rng = np.random.default_rng(4)


def norm(w):
    return re.sub(r"[^a-z0-9%.+,]", "", w.lower())


def word(room, prefix):
    for ln in tl["lines"]:
        if ln["room"] == room:
            for w in ln["words"]:
                if norm(w["w"]).startswith(prefix):
                    return w["s"]
    return None


def add(t, sig, gain):
    if t is None:
        return
    i = int(t * SR)
    if i >= n:
        return
    j = min(n, i + len(sig))
    mix[max(0, i) : j] += gain * sig[max(0, -i) : j - i]


def whoosh(d=0.6):
    m = int(d * SR)
    x = rng.standard_normal(m).astype(np.float32)
    # moving one-pole low-pass: cutoff sweeps up then down
    cut = np.sin(np.linspace(0, np.pi, m)) ** 1.5
    y = np.zeros(m, np.float32)
    acc = 0.0
    for k in range(m):
        a = 0.02 + 0.35 * cut[k]
        acc += a * (x[k] - acc)
        y[k] = acc
    env = np.sin(np.linspace(0, np.pi, m)) ** 2
    return y * env / (np.abs(y).max() + 1e-6)


def thump(d=0.35):
    tt = np.arange(int(d * SR)) / SR
    f = 50 + 70 * np.exp(-tt * 30)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 11)
    click = rng.standard_normal(len(tt)) * np.exp(-tt * 250) * 0.4
    return (s + click).astype(np.float32)


def tick():
    tt = np.arange(int(0.05 * SR)) / SR
    return (np.sin(2 * np.pi * 2400 * tt) * np.exp(-tt * 120)).astype(np.float32)


def crunch(d=0.38):
    m = int(d * SR)
    x = rng.standard_normal(m)
    x = np.repeat(x[::40], 40)[:m]  # sample-and-hold = bitcrush
    tt = np.arange(m) / SR
    gate = (np.sin(2 * np.pi * 23 * tt) > -0.2).astype(float)
    return (x * gate * np.exp(-tt * 5)).astype(np.float32) / 3


# drone bed
tt = np.arange(n) / SR
bed = 0.5 * np.sin(2 * np.pi * 55 * tt) + 0.35 * np.sin(2 * np.pi * 82.6 * tt + 1) + 0.2 * np.sin(2 * np.pi * 110.3 * tt)
bed *= 0.8 + 0.2 * np.sin(2 * np.pi * 0.25 * tt)
mix += (0.05 * bed).astype(np.float32)

MOVE = 0.55
for r in tl["rooms"][1:]:
    add(r["start"] - MOVE / 2 - 0.05, whoosh(), 0.32)
for room, w in [("hook", "black"), ("one", "video"), ("two", "18.9%"), ("two", "20"), ("three", "cost"), ("three", "7"), ("cta", "q4")]:
    add(word(room, w), thump(), 0.45)
for i in (6, 12):
    add(tl["lines"][i]["start"] - 0.04, crunch(), 0.35)
add(word("one", "video"), tick(), 0.25)
add(word("cta", "q4"), tick(), 0.25)
add((word("cta", "q4") or 0) + 0.55, tick(), 0.2)
add(0.0, thump(0.6), 0.35)  # cold-open hit

peak = np.abs(mix).max()
mix = (mix / peak * 0.5).astype(np.float32)
out = ROOT / "public/sfx.wav"
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af", "volume=-6dB", str(out)], input=mix.tobytes(), check=True)
print(f"sfx.wav {dur:.1f}s")
