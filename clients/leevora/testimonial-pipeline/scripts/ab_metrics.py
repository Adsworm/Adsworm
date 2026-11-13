"""Objective comparison of cleanup candidates against the original. numpy + soundfile-free (ffmpeg decodes to f32 mono 48k raw)."""
import sys, subprocess, numpy as np
def load(p):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-ac', '1', '-ar', '48000', '-f', 'f32le', '-'], capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.float32).astype(np.float64)
sr, N, H = 48000, 2048, 512
def spec(x):
    fr = np.lib.stride_tricks.sliding_window_view(x, N)[::H]; return np.abs(np.fft.rfft(fr * np.hanning(N), axis=1)) ** 2
f = np.fft.rfftfreq(N, 1 / sr)
ref = load(sys.argv[1]); S0 = spec(ref)
sp = 10 * np.log10(S0[:, (f >= 1000) & (f < 4000)].sum(1) + 1e-20); lo, hi = np.percentile(sp, 8), np.percentile(sp, 92)
act = sp > lo + 0.45 * (hi - lo)                       # confident speech frames
quiet = sp < lo + 0.12 * (hi - lo)                     # confident pause frames
k = 6; q = quiet.copy()
for i in range(len(act)):
    if act[max(0, i - k): i + k + 1].any(): q[i] = False
print(f'speech frames {act.sum()} ({act.sum()*H/sr:.1f}s), pause frames {q.sum()} ({q.sum()*H/sr:.2f}s)\n')
def bands(P): return [10 * np.log10(P[(f >= a) & (f < b)].sum() + 1e-20) for a, b in [(120, 300), (300, 1000), (1000, 4000), (4000, 8000), (8000, 16000)]]
print(f"{'candidate':34s} {'SNR dB':>7s} {'noise cut':>9s} | speech-band change vs original (dB): 120-300  300-1k  1-4k  4-8k  8-16k | pause 'flutter'")
base = None
for p in sys.argv[1:]:
    x = load(p)[:len(ref)]; S = spec(x); n = min(len(S), len(act)); S = S[:n]; a, qq = act[:n], q[:n]
    Ps, Pn = S[a].mean(0), S[qq].mean(0); m = f >= 120
    snr = 10 * np.log10(Ps[m].sum() / Pn[m].sum())
    # normalise by speech level in 1-4k so gain differences do not matter
    g = 10 * np.log10(Ps[(f >= 1000) & (f < 4000)].sum()); bs = np.array(bands(Ps)) - g; nlev = 10 * np.log10(Pn[m].sum()) - g
    # flutter: frame-to-frame std (dB) of 1-8 kHz residual during pauses -> watery / musical-noise proxy
    r = 10 * np.log10(S[qq][:, (f >= 1000) & (f < 8000)].sum(1) + 1e-20); fl = r.std()
    if base is None: base = (bs, nlev)
    d = bs - base[0]
    print(f"{p.split('/')[-1]:34s} {snr:7.1f} {base[1]-nlev:8.1f}  |  {d[0]:+6.1f} {d[1]:+6.1f} {d[2]:+5.1f} {d[3]:+5.1f} {d[4]:+6.1f}  | {fl:5.2f}")
