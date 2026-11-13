"""Single-channel late-reverberation suppression (Lebart-style spectral subtraction). numpy only.
Usage: dereverb.py <in.wav> <out.wav> <rt60_seconds> <strength> <floor_db>"""
import sys, subprocess, numpy as np
src, dst, rt60, gamma, floor_db = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])
sr = 48000; x = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', src, '-ac', '1', '-ar', str(sr), '-f', 'f32le', '-'], capture_output=True).stdout, dtype=np.float32).astype(np.float64)
N, H = 1024, 256; w = np.sqrt(np.hanning(N + 1)[:-1]); n = 1 + (len(x) - N) // H
X = np.stack([np.fft.rfft(x[i * H:i * H + N] * w) for i in range(n)]); P = np.abs(X) ** 2
a = 0.6; Ps = np.empty_like(P); Ps[0] = P[0]                       # temporal smoothing of the power spectrum
for i in range(1, n): Ps[i] = a * Ps[i - 1] + (1 - a) * P[i]
D = int(round(0.05 * sr / H)); delta = 3 * np.log(10) / rt60; alpha = np.exp(-2 * delta * D * H / sr)   # late part starts 50 ms after the direct sound
R = np.zeros_like(P); R[D:] = alpha * Ps[:-D]
G = np.sqrt(np.clip(1 - gamma * R / (P + 1e-12), 10 ** (floor_db / 10), 1))
Gs = G.copy()
for i in range(1, n): Gs[i] = np.where(G[i] > Gs[i - 1], 0.3 * Gs[i - 1] + 0.7 * G[i], 0.7 * Gs[i - 1] + 0.3 * G[i])   # fast open, slower close: no chatter
Y = X * Gs; y = np.zeros(len(x)); wsum = np.zeros(len(x))
for i in range(n): y[i * H:i * H + N] += np.fft.irfft(Y[i], N) * w; wsum[i * H:i * H + N] += w ** 2
y /= np.maximum(wsum, 1e-6)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(sr), '-ac', '1', '-i', '-', '-c:a', 'pcm_f32le', dst], input=y.astype(np.float32).tobytes(), check=True)
