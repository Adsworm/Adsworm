"""Code-synthesized score + SFX for the reel. No samples, no AI: every sound is math.

Reads src/reel/timeline.json (shared with the React scenes, so sound and picture can't drift)
and writes public/reel-audio.wav (48 kHz stereo). Loudness is mastered to -14 LUFS at mux time.

    python3 scripts/sound.py
"""
import json
import wave
from pathlib import Path

import numpy as np
from scipy.signal import butter, sosfilt

SR = 48000
ROOT = Path(__file__).resolve().parent.parent
rng = np.random.default_rng(7)  # fixed seed: the mix is deterministic


def secs(n):
    return np.arange(int(n * SR)) / SR


def lp(x, hz, order=2):
    return sosfilt(butter(order, hz, "low", fs=SR, output="sos"), x)


def hp(x, hz, order=2):
    return sosfilt(butter(order, hz, "high", fs=SR, output="sos"), x)


def bp(x, lo, hi, order=2):
    return sosfilt(butter(order, [lo, hi], "band", fs=SR, output="sos"), x)


def noise(dur):
    return rng.standard_normal(int(dur * SR))


# ---------- instruments ----------

def kick():
    t = secs(0.45)
    f = 44 + 90 * np.exp(-t * 32)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7.5)
    click = hp(noise(0.45), 2500) * np.exp(-t * 300) * 0.25
    return body + click


def hat(open_=False):
    dur = 0.18 if open_ else 0.05
    t = secs(dur)
    return hp(noise(dur), 7500, 4) * np.exp(-t * (18 if open_ else 70)) * 0.35


def clap():
    t = secs(0.25)
    n = bp(noise(0.25), 900, 3200)
    bursts = sum(np.exp(-np.clip(t - d, 0, None) * 60) * (t >= d) for d in (0, 0.011, 0.022))
    return n * (bursts * 0.5 + np.exp(-t * 14) * 0.6) * 0.5


def sub(freq, dur):
    t = secs(dur)
    tone = np.sin(2 * np.pi * freq * t) + 0.18 * np.sin(4 * np.pi * freq * t)
    env = np.minimum(1, t / 0.01) * np.minimum(1, (dur - t) / 0.05)
    return tone * env * 0.55


def pad(freqs, dur):
    t = secs(dur)
    x = np.zeros_like(t)
    for f in freqs:
        for detune in (-0.12, 0.0, 0.12):  # semitone cents spread → width
            fd = f * 2 ** (detune / 12)
            x += 2 * ((t * fd) % 1) - 1
    x = lp(x / (len(freqs) * 3), 1400)
    env = np.minimum(1, t / 0.35) * np.minimum(1, (dur - t) / 0.4)
    return x * env * 0.32


# ---------- sfx ----------

def tick():
    t = secs(0.03)
    return (np.sin(2 * np.pi * 2400 * t) * np.exp(-t * 260) + hp(noise(0.03), 4000) * np.exp(-t * 400) * 0.3) * 0.45


def pop():
    t = secs(0.09)
    f = 380 + 700 * np.exp(-t * 55)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 38) * 0.55


def type_click():
    t = secs(0.02)
    return bp(noise(0.02), 2500, 6000) * np.exp(-t * 350) * 0.4


def whoosh(dur=0.4):
    t = secs(dur)
    n = noise(dur)
    out = np.zeros_like(n)
    blocks = np.array_split(np.arange(len(n)), 24)
    for i, idx in enumerate(blocks):  # sweep a band upward block by block
        c = 350 * (12 ** (i / (len(blocks) - 1)))
        out[idx] = bp(n, c * 0.7, min(c * 1.6, SR / 2 - 100))[idx]
    env = np.sin(np.pi * np.clip(t / dur, 0, 1)) ** 2
    return out * env * 0.5


def impact():
    t = secs(1.6)
    f = 34 + 40 * np.exp(-t * 9)
    boom = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 2.6)
    crack = lp(noise(1.6), 600) * np.exp(-t * 9) * 0.6
    return (boom + crack) * 0.8


def riser(dur):
    t = secs(dur)
    f = 180 + 1100 * (t / dur) ** 2
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.25
    hiss = hp(noise(dur), 3000) * 0.35
    return (tone + hiss) * (t / dur) ** 2.2 * 0.6


def braam(dur=2.2):
    """Trailer brass hit: stacked detuned saws on A1/A2/E3 through a closing low-pass."""
    t = secs(dur)
    x = np.zeros_like(t)
    for f in (55.0, 110.0, 164.81):
        for d in (-0.15, 0.0, 0.15):
            x += 2 * ((t * f * 2 ** (d / 12)) % 1) - 1
    x /= 9
    out = np.zeros_like(x)
    blocks = np.array_split(np.arange(len(x)), 32)
    for i, idx in enumerate(blocks):  # filter closes over the tail
        out[idx] = lp(x, 2400 * (0.12 ** (i / len(blocks))) + 120)[idx]
    env = np.minimum(1, t / 0.02) * np.exp(-t * 1.1)
    return np.tanh(out * env * 2.4) * 0.7


def taiko():
    t = secs(1.0)
    f = 48 + 60 * np.exp(-t * 22)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 4.5)
    skin = lp(noise(1.0), 900) * np.exp(-t * 18) * 0.5
    return (body + skin) * 0.9


def reverse_swell(dur=1.0):
    """Reverse cymbal into a downbeat: filtered noise with an exponential rise, cut dead at the end."""
    t = secs(dur)
    return hp(noise(dur), 2500) * (t / dur) ** 3 * 0.55


def drone(dur):
    t = secs(dur)
    x = np.sin(2 * np.pi * 55 * t) * 0.5 + lp(sum(2 * ((t * f) % 1) - 1 for f in (110.0, 110.4, 164.8)) / 3, 500) * 0.35
    env = np.minimum(1, t / 1.2) * np.minimum(1, (dur - t) / 0.6)
    return x * env * 0.45


SFX = {"tick": tick, "pop": pop, "type": type_click, "whoosh": whoosh, "impact": impact, "braam": braam, "taiko": taiko, "swell": reverse_swell}

# A minor → F → C → G, one chord per bar (voiced around A3)
CHORDS = [(220.0, 261.63, 329.63), (174.61, 220.0, 261.63), (196.0, 261.63, 329.63), (196.0, 246.94, 293.66)]
ROOTS = [55.0, 43.65, 65.41, 49.0]


def place(track, clip, at_s, gain=1.0):
    i = int(at_s * SR)
    if i >= len(track):
        return
    j = min(len(track), i + len(clip))
    track[i:j] += clip[: j - i] * gain


def build(tl):
    fps, bpm = tl["fps"], tl["bpm"]
    total = tl["durationInFrames"] / fps
    beat = 60 / bpm
    bar = beat * 4
    n = int((total + 2) * SR)
    drums, bass, harm, fx = (np.zeros(n) for _ in range(4))
    kick_env = np.zeros(n)

    for sec in tl["music"]:  # {"from": frame, "to": frame, "mode": intro|groove|break|outro}
        a, b, mode = sec["from"] / fps, sec["to"] / fps, sec["mode"]
        k = int(round(a / beat))
        while k * beat < b - 1e-6:
            t0 = k * beat
            bar_i = int(t0 // bar)
            if mode == "pulse":
                if k % 2 == 0:
                    place(drums, kick(), t0, 0.8)
                    place(kick_env, np.exp(-secs(0.3) * 9), t0)
                place(drums, hat(), t0 + beat / 2, 0.5)
                for s8 in range(2):
                    place(bass, sub(ROOTS[0], beat / 2 * 0.8), t0 + s8 * beat / 2, 0.7)
            if mode == "drone" and k % 8 == 0:
                place(harm, drone(min(bar * 2, b - t0)), t0)
            if mode in ("groove", "drop"):
                place(drums, kick(), t0)
                place(kick_env, np.exp(-secs(0.3) * 9), t0)
                place(drums, hat(open_=(k % 4 == 3)), t0 + beat / 2)
                if k % 2 == 1:
                    place(drums, clap(), t0)
            if mode == "break":
                place(drums, hat(), t0 + beat / 2, 0.6)
            if k % 4 == 0 and mode in ("groove", "drop", "intro", "break"):
                place(harm, pad(CHORDS[bar_i % 4], bar), t0)
                if mode in ("groove", "intro", "drop"):
                    for s in range(8):  # eighth-note bass
                        place(bass, sub(ROOTS[bar_i % 4], beat / 2 * 0.9), t0 + s * beat / 2, 1.0 if s % 2 == 0 else 0.6)
            if mode == "outro" and k % 4 == 0:
                place(harm, pad(CHORDS[0], bar * 1.5), t0, 0.9)
            k += 1

    for cue in tl["sfx"]:  # {"frame": n, "type": name, "gain"?: x}
        at = cue["frame"] / fps
        if cue["type"] in ("swell",):
            d = cue.get("duration", 1.0)
            place(fx, reverse_swell(d), at - d, cue.get("gain", 1.0))
        elif cue["type"] == "riser":
            d = cue.get("duration", 2.0)
            place(fx, riser(d), at - d, cue.get("gain", 1.0))
        else:
            place(fx, SFX[cue["type"]](), at, cue.get("gain", 1.0))

    duck = 1 - 0.55 * np.clip(kick_env, 0, 1)  # sidechain: bass + pad breathe with the kick
    mono = drums * 0.9 + bass * duck * 0.8 + fx
    # light stereo: pad + hats widened with a short Haas offset
    d = int(0.012 * SR)
    wide = harm * duck
    left = mono + wide
    right = mono + np.concatenate([np.zeros(d), wide[:-d]])
    stereo = np.stack([left, right], axis=1)[: int(total * SR)]
    fade = int(0.3 * SR)
    stereo[-fade:] *= np.linspace(1, 0, fade)[:, None]
    stereo = np.tanh(stereo * 1.2) / np.tanh(1.2)  # gentle glue saturation
    return stereo / (np.max(np.abs(stereo)) + 1e-9) * 0.89


def main():
    tl = json.loads((ROOT / "src/reel/timeline.json").read_text())
    audio = build(tl)
    out = ROOT / "public/reel-audio.wav"
    with wave.open(str(out), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((audio * 32767).astype("<i2").tobytes())
    print(f"{out.relative_to(ROOT)} · {len(audio) / SR:.2f}s · {len(tl['sfx'])} sfx cues")


if __name__ == "__main__":
    main()
