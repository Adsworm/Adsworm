"""Characterise noise vs speech in a mono 16-bit WAV. numpy only."""
import sys, wave, numpy as np
w = wave.open(sys.argv[1]); sr = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64) / 32768.0
N, H = 4096, 1024
win = np.hanning(N)
frames = np.lib.stride_tricks.sliding_window_view(x, N)[::H]
S = np.abs(np.fft.rfft(frames * win, axis=1)) ** 2
f = np.fft.rfftfreq(N, 1 / sr); t = (np.arange(len(S)) * H + N / 2) / sr
def band(lo, hi): return 10 * np.log10(S[:, (f >= lo) & (f < hi)].sum(axis=1) + 1e-20)
# speech activity from 1-4 kHz band where the drone is weak
sp = band(1000, 4000)
lo_p, hi_p = np.percentile(sp, 8), np.percentile(sp, 92)
thr = lo_p + 0.30 * (hi_p - lo_p)
act = sp > thr
print(f'speech-band (1-4k) energy: quiet p8={lo_p:.1f} dB, loud p92={hi_p:.1f} dB, span={hi_p-lo_p:.1f} dB, thr={thr:.1f}')
# segments
segs = []; start = None
for i, a in enumerate(act):
    if a and start is None: start = t[i]
    if not a and start is not None: segs.append([start, t[i]]); start = None
if start is not None: segs.append([start, t[-1]])
# merge gaps < 0.18 s, drop blips < 0.10 s
m = []
for s in segs:
    if m and s[0] - m[-1][1] < 0.18: m[-1][1] = s[1]
    else: m.append(s)
m = [s for s in m if s[1] - s[0] >= 0.10]
print('\nSPEECH ACTIVITY (energy-based, 1-4 kHz) and gaps:')
prev = 0.0
for a, b in m:
    gap = a - prev
    flag = '  <-- pause %.2fs' % gap if gap >= 0.35 else ''
    print(f'  {a:6.2f} - {b:6.2f}  ({b-a:4.2f}s)  fr {int(a*25):4d}-{int(b*25):4d}{flag}')
    prev = b
print(f'  tail after last speech: {t[-1]-prev:.2f}s')
quiet = ~act
# dilate speech mask by 0.15s to get clean noise-only frames
k = int(0.15 * sr / H); q = quiet.copy()
for i in range(len(act)):
    if act[max(0, i - k): i + k + 1].any(): q[i] = False
print(f'\nnoise-only frames: {q.sum()} ({q.sum()*H/sr:.1f}s) | speech frames: {act.sum()} ({act.sum()*H/sr:.1f}s)')
Pn = S[q].mean(axis=0); Ps = S[act].mean(axis=0)
print('\nBAND LEVELS dB (noise-only | during speech | speech+noise minus noise):')
for lo, hi in [(20,60),(60,120),(120,250),(250,400),(400,600),(600,1000),(1000,2000),(2000,4000),(4000,8000),(8000,16000)]:
    b = (f >= lo) & (f < hi); n = 10*np.log10(Pn[b].sum()+1e-20); s = 10*np.log10(Ps[b].sum()+1e-20)
    print(f'  {lo:5d}-{hi:5d} Hz  {n:7.1f} | {s:7.1f} | {s-n:+5.1f}')
tot_n = 10*np.log10(Pn.sum()); tot_s = 10*np.log10(Ps.sum())
est = 10*np.log10(max(Ps.sum()-Pn.sum(), 1e-20)/Pn.sum())
b2 = f >= 150
est_hp = 10*np.log10(max(Ps[b2].sum()-Pn[b2].sum(), 1e-20)/Pn[b2].sum())
print(f'\nbroadband SNR estimate (speech vs noise power): {est:+.1f} dB full-band, {est_hp:+.1f} dB above 150 Hz')
# tonal peaks in the noise spectrum (fine resolution)
N2 = 32768; fr2 = np.lib.stride_tricks.sliding_window_view(x, N2)[::N2 // 4]
S2 = (np.abs(np.fft.rfft(fr2 * np.hanning(N2), axis=1)) ** 2); f2 = np.fft.rfftfreq(N2, 1 / sr)
med = np.median(S2, axis=0); db = 10*np.log10(med + 1e-20)
from numpy.lib.stride_tricks import sliding_window_view as swv
pad = 60; base = np.median(swv(np.pad(db, pad, mode='edge'), 2*pad+1), axis=1)
prom = db - base
peaks = [i for i in range(2, len(db)-2) if db[i] == db[i-2:i+3].max() and prom[i] > 9 and 30 < f2[i] < 12000]
peaks = sorted(peaks, key=lambda i: -db[i])[:22]
print('\nSTEADY TONAL PEAKS in time-median spectrum (freq Hz, level dB, prominence dB):')
for i in sorted(peaks): print(f'  {f2[i]:8.1f} Hz  {db[i]:7.1f}  +{prom[i]:.1f}')
# stationarity of the drone band over time
dr = band(280, 600); print(f'\ndrone band 280-600 Hz over time: mean {dr.mean():.1f} dB, std {dr.std():.2f} dB, min {dr.min():.1f}, max {dr.max():.1f}  (low std = steady)')
lf = band(30, 120); thump = [(round(t[i],2), round(lf[i],1)) for i in range(1,len(lf)-1) if lf[i] > np.median(lf)+12 and lf[i] >= lf[i-1] and lf[i] >= lf[i+1]]
print('low-frequency thumps (30-120 Hz, >12 dB over median):', thump[:20])
# reverb: decay of 1-4 kHz envelope after speech offsets
hop = 240; e = np.array([np.sum(x[i:i+hop]**2) for i in range(0, len(x)-hop, hop)])
# bandpass via FFT mask for the envelope
X = np.fft.rfft(x); ff = np.fft.rfftfreq(len(x), 1/sr); X[(ff < 1000) | (ff > 4000)] = 0; xb = np.fft.irfft(X, len(x))
e = 10*np.log10(np.array([np.mean(xb[i:i+hop]**2) for i in range(0, len(xb)-hop, hop)]) + 1e-20); te = np.arange(len(e))*hop/sr
floor = np.percentile(e, 5); rts = []
for a, b in m:
    i0 = np.searchsorted(te, b - 0.10); seg = e[i0:i0 + int(0.6*sr/hop)]
    if len(seg) < 20: continue
    pk = seg[:8].max(); 
    if pk - floor < 18: continue
    j = np.where(seg < pk - 5)[0]; k2 = np.where(seg < max(pk - 15, floor + 3))[0]
    if len(j) and len(k2) and k2[0] > j[0]:
        slope = 10.0 / ((k2[0]-j[0])*hop/sr); rts.append(60.0/slope)
if rts: print(f'\nreverb (1-4 kHz decay after phrase ends): median RT60-equivalent ~{np.median(rts):.2f}s from {len(rts)} offsets (range {min(rts):.2f}-{max(rts):.2f})')
else: print('\nreverb: not enough clean offsets above noise to estimate')
# last second tones
print('\nfinal 1.2 s vs rest, 2-12 kHz level:', round(float(band(2000,12000)[t > t[-1]-1.2].mean()),1), 'vs', round(float(np.median(band(2000,12000))),1))
