"""Screen candidate instrumental tracks by measurable properties (I cannot judge mood by ear):
percussiveness, brightness, tempo, major/minor leaning, level stability over the first 40 s."""
import sys, json, subprocess, numpy as np, os, html
cat = json.load(open(sys.argv[1])); want = sys.argv[2].split(','); outdir = sys.argv[3]; os.makedirs(outdir, exist_ok=True)
sr = 22050; rows = []
MAJ = np.array([6.35,2.23,3.48,2.33,4.38,4.09,2.52,5.19,2.39,3.66,2.29,2.88]); MIN = np.array([6.33,2.68,3.52,5.38,2.60,3.53,2.54,4.75,3.98,2.69,3.34,3.17])
for url, v in cat.items():
    pages = set(v['pages']); 
    if not all(any(w in p for p in pages) for w in want[:1]) or not any(any(w in p for p in pages) for w in want[1:]): continue
    fn = os.path.join(outdir, url.split('/')[-1])
    if not os.path.exists(fn): subprocess.run(['curl', '-sS', '-m', '90', '-L', '-A', 'Mozilla/5.0', '-o', fn, url])
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-t', '60', '-i', fn, '-ac', '1', '-ar', str(sr), '-f', 'f32le', '-'], capture_output=True).stdout
    x = np.frombuffer(raw, dtype=np.float32).astype(np.float64)
    if len(x) < sr * 36: continue
    dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', fn], capture_output=True, text=True).stdout or 0)
    N, H = 2048, 512; fr = np.lib.stride_tricks.sliding_window_view(x[:sr * 40], N)[::H]; S = np.abs(np.fft.rfft(fr * np.hanning(N), axis=1)); f = np.fft.rfftfreq(N, 1 / sr)
    P = S ** 2; cent = (P * f).sum(1) / (P.sum(1) + 1e-12)
    flux_hi = np.maximum(np.diff(np.log1p(S[:, f > 3000] * 50), axis=0), 0).sum(1); flux_all = np.maximum(np.diff(np.log1p(S * 50), axis=0), 0).sum(1)
    perc = float(np.percentile(flux_hi, 95) / (np.median(flux_all) + 1e-9))         # sharp high-frequency hits = drums / hats / claps
    o = flux_all - flux_all.mean(); ac = np.correlate(o, o, 'full')[len(o) - 1:]; lag = np.arange(len(ac)) * H / sr; m = (lag > 0.33) & (lag < 1.2); bpm = 60 / lag[m][np.argmax(ac[m])]
    chroma = np.zeros(12)
    for k in range(12):
        for octv in range(2, 7):
            fc = 440 * 2 ** ((k - 9) / 12 + octv - 4); chroma[k] += P[:, (f > fc * 0.972) & (f < fc * 1.029)].sum()
    chroma /= chroma.sum(); cm = max(np.corrcoef(np.roll(MAJ, k), chroma)[0, 1] for k in range(12)); cn = max(np.corrcoef(np.roll(MIN, k), chroma)[0, 1] for k in range(12))
    e = np.array([10 * np.log10(np.mean(x[i:i + sr] ** 2) + 1e-12) for i in range(0, sr * 36, sr)])
    rows.append(dict(title=html.unescape(v['title']), file=os.path.basename(fn), dur=round(dur), perc=round(perc, 2), centroid=int(np.median(cent)), bpm=int(round(bpm)), major_minus_minor=round(cm - cn, 2), first2s_dB=round(float(e[:2].mean()), 1), level_dB=round(float(np.median(e)), 1), level_spread=round(float(e[3:].std()), 1), pages=sorted(pages)))
rows.sort(key=lambda r: (r['perc'], r['centroid']))
json.dump(rows, open(os.path.join(outdir, 'screen.json'), 'w'), indent=1)
print(f"{'title':28s} {'file':9s} dur  perc  centroid bpm  maj-min  first2s  level  spread")
for r in rows: print(f"{r['title'][:28]:28s} {r['file']:9s} {r['dur']:3d}  {r['perc']:4.2f}  {r['centroid']:6d}  {r['bpm']:3d}   {r['major_minus_minor']:+.2f}   {r['first2s_dB']:6.1f} {r['level_dB']:6.1f}  {r['level_spread']:4.1f}")
