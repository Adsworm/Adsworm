"""Track her head position through the shot with normalised cross-correlation on a head template (numpy only).
Reads gray frames 540x960 from ffmpeg. Writes track.json: per-frame face centre in SOURCE px (2160x3840) + smoothed path."""
import sys, json, subprocess, numpy as np
src, out = sys.argv[1], sys.argv[2]
W, H, SC = 540, 960, 4.0
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', src, '-vf', f'scale={W}:{H},format=gray', '-f', 'rawvideo', '-'], capture_output=True).stdout
n = len(raw) // (W * H); fr = np.frombuffer(raw, dtype=np.uint8)[:n * W * H].reshape(n, H, W).astype(np.float32)
# template: head box picked on frame 225 (t=9.0s) from the inspected still: face centre ~ (920,1590) source px -> (230,397) here
cx0, cy0, tw, th = 230, 395, 56, 72
ref_i = 225
def patch(f, cx, cy): return f[int(cy - th // 2): int(cy - th // 2) + th, int(cx - tw // 2): int(cx - tw // 2) + tw]
tpl = patch(fr[ref_i], cx0, cy0); tz = (tpl - tpl.mean()) / (tpl.std() + 1e-6)
def locate(f, cx, cy, R=14):
    best, bx, by = -9, cx, cy; sc = {}
    for dy in range(-R, R + 1):
        for dx in range(-R, R + 1):
            p = patch(f, cx + dx, cy + dy)
            if p.shape != tpl.shape: continue
            v = float(((p - p.mean()) / (p.std() + 1e-6) * tz).mean()); sc[(dx, dy)] = v
            if v > best: best, bx, by = v, cx + dx, cy + dy
    # sub-pixel refine (parabola)
    dx, dy = bx - cx, by - cy
    def ref(a, b, c): d = a - 2 * b + c; return 0.0 if abs(d) < 1e-9 else 0.5 * (a - c) / d
    sx = ref(sc.get((dx - 1, dy), best), best, sc.get((dx + 1, dy), best)); sy = ref(sc.get((dx, dy - 1), best), best, sc.get((dx, dy + 1), best))
    return bx + sx, by + sy, best
pos = [None] * n; cx, cy = cx0, cy0
for i in range(ref_i, n):
    x, y, s = locate(fr[i], round(cx), round(cy)); pos[i] = (x, y, s); cx, cy = x, y
cx, cy = cx0, cy0
for i in range(ref_i - 1, -1, -1):
    x, y, s = locate(fr[i], round(cx), round(cy)); pos[i] = (x, y, s); cx, cy = x, y
p = np.array(pos); xs, ys, sc = p[:, 0] * SC, p[:, 1] * SC, p[:, 2]
def smooth(v, k=25):
    w = np.hanning(k + 2)[1:-1]; w /= w.sum(); return np.convolve(np.pad(v, k // 2, mode='edge'), w, mode='valid')
sx, sy = smooth(xs), smooth(ys)
json.dump({'fps': 25, 'frames': n, 'x': [round(float(v), 1) for v in xs], 'y': [round(float(v), 1) for v in ys], 'xs': [round(float(v), 1) for v in sx], 'ys': [round(float(v), 1) for v in sy], 'score': [round(float(v), 3) for v in sc]}, open(out, 'w'))
print(f'frames {n} | match score min {sc.min():.2f} mean {sc.mean():.2f} | face centre x {xs.min():.0f}-{xs.max():.0f}, y {ys.min():.0f}-{ys.max():.0f} (source px)')
for t in (0, 1, 2, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36): 
    i = min(int(t * 25), n - 1); print(f'  t={t:2d}s  face=({xs[i]:.0f},{ys[i]:.0f})  score {sc[i]:.2f}')
low = np.where(sc < 0.55)[0]; print('frames with weak match (<0.55):', len(low), list(low[:20]))
