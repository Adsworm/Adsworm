"""Reframe + stabilise + grade renderer for a single-take testimonial. numpy + Pillow + ffmpeg only.
  render_base.py prep  <src> <workdir>                       -> motion.json (camera drift) ; expects track.json from face_track.py
  render_base.py still <src> <workdir> <edl> <frame> <seg_id> <out.png> [--nograde] [--size WxH]
  render_base.py video <src> <workdir> <edl> <out.mov> [--size WxH] [--only id,id] [--nograde]
Colour: decodes Rec.709 limited -> full-range RGB, works in float, writes 16-bit RGB, encodes 10-bit Rec.709 ProRes 422 HQ."""
import sys, json, subprocess, os, numpy as np
from PIL import Image
SW, SH = 2160, 3840
def gblur(a, sigma):
    """Separable Gaussian blur on a float32 2-D array (Pillow cannot blur float images)."""
    r = max(1, int(np.ceil(3 * sigma))); k = np.exp(-0.5 * (np.arange(-r, r + 1) / sigma) ** 2).astype(np.float32); k /= k.sum()
    p = np.pad(a, ((r, r), (0, 0)), mode='reflect'); out = np.zeros_like(a)
    for i, w in enumerate(k): out += w * p[i:i + a.shape[0], :]
    p = np.pad(out, ((0, 0), (r, r)), mode='reflect'); out2 = np.zeros_like(a)
    for i, w in enumerate(k): out2 += w * p[:, i:i + a.shape[1]]
    return out2
def boxf(a, r):
    """Mean over a (2r+1)^2 window via summed-area table, edge-padded."""
    c = np.cumsum(np.cumsum(np.pad(a, ((r + 1, r), (r + 1, r)), mode='edge'), 0, dtype=np.float64), 1)
    n = 2 * r + 1
    return ((c[n:, n:] - c[:-n, n:] - c[n:, :-n] + c[:-n, :-n]) / (n * n)).astype(np.float32)
def guided(I, p, r, eps):
    """He et al. guided filter: edge-aware smoothing of p using guide I (both 2-D float32)."""
    mI, mp = boxf(I, r), boxf(p, r); a = (boxf(I * p, r) - mI * mp) / (boxf(I * I, r) - mI * mI + eps); b = mp - a * mI
    return boxf(a, r) * I + boxf(b, r)
def minfilt(a, r):
    from numpy.lib.stride_tricks import sliding_window_view as swv
    a = swv(np.pad(a, ((r, r), (0, 0)), mode='edge'), 2 * r + 1, axis=0).min(-1)
    return swv(np.pad(a, ((0, 0), (r, r)), mode='edge'), 2 * r + 1, axis=1).min(-1)
LUMW = np.array([0.2126, 0.7152, 0.0722], dtype=np.float32)
def dehaze(x, s, airlight, tmin=0.45):
    """Dark-channel veil removal (He et al.), computed at 1/4 resolution and refined edge-aware with a guided filter so no halo
    forms around her hair. s = how much of the estimated veil to remove (0 = none)."""
    H, W, _ = x.shape; d = 4; sm = x[::d, ::d]
    A = np.array(airlight, dtype=np.float32)
    dark = minfilt((sm / A).min(axis=2), max(2, W // 180))
    V = np.clip(guided(sm @ LUMW, dark, max(4, W // 90), 1e-3), 0, 1)
    V = np.asarray(Image.fromarray(V, mode='F').resize((W, H), Image.BICUBIC), dtype=np.float32)
    t = np.maximum(1 - s * V, tmin)[..., None]
    return (x - A * (1 - t)) / t
def arg(flag, default=None):
    return sys.argv[sys.argv.index(flag) + 1] if flag in sys.argv else default
def smooth(v, k):
    w = np.hanning(k + 2)[1:-1]; w /= w.sum(); return np.convolve(np.pad(np.asarray(v, float), k // 2, mode='edge'), w, mode='valid')
def prep(src, wd):
    W, H = 540, 960
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', src, '-vf', f'scale={W}:{H},format=gray', '-f', 'rawvideo', '-'], capture_output=True).stdout
    n = len(raw) // (W * H); fr = np.frombuffer(raw, dtype=np.uint8)[:n * W * H].reshape(n, H, W).astype(np.float32)
    top = fr[:, :int(H * 0.40), :]; win = np.outer(np.hanning(top.shape[1]), np.hanning(W)).astype(np.float32); R0 = 225
    ref = np.fft.rfft2((top[R0] - top[R0].mean()) * win); d = np.zeros((n, 2))
    for i in range(n):
        F = np.fft.rfft2((top[i] - top[i].mean()) * win); R = F * np.conj(ref); R /= np.abs(R) + 1e-9; c = np.fft.irfft2(R, s=top[0].shape)
        py, px = np.unravel_index(np.argmax(c), c.shape)
        def sub(v, p, m): a, b, e = v[(p - 1) % m], v[p], v[(p + 1) % m]; q = a - 2 * b + e; return 0 if q == 0 else 0.5 * (a - e) / q
        dy = py + sub(c[:, px], py, c.shape[0]); dx = px + sub(c[py, :], px, c.shape[1])
        if dy > c.shape[0] / 2: dy -= c.shape[0]
        if dx > c.shape[1] / 2: dx -= c.shape[1]
        d[i] = (dx * 4, dy * 4)
    # sign calibration: content of frame i should equal ref shifted by +d
    i = int(np.argmax(np.abs(d[:, 0]) + np.abs(d[:, 1]))); sx, sy = int(round(d[i, 0] / 4)), int(round(d[i, 1] / 4))
    a = top[R0][20:-20, 20:-20]; e_pos = np.mean((np.roll(top[R0], (sy, sx), (0, 1))[20:-20, 20:-20] - top[i][20:-20, 20:-20]) ** 2); e_neg = np.mean((np.roll(top[R0], (-sy, -sx), (0, 1))[20:-20, 20:-20] - top[i][20:-20, 20:-20]) ** 2)
    if e_neg < e_pos: d = -d
    out = {'ref': R0, 'dx': [round(float(v), 2) for v in d[:, 0]], 'dy': [round(float(v), 2) for v in d[:, 1]], 'dxs': [round(float(v), 2) for v in smooth(d[:, 0], 13)], 'dys': [round(float(v), 2) for v in smooth(d[:, 1], 13)]}
    json.dump(out, open(os.path.join(wd, 'motion.json'), 'w'))
    print(f'motion: {n} frames, sign check err +{e_pos:.1f} / -{e_neg:.1f} (kept {"flipped" if e_neg < e_pos else "as measured"}), drift x {d[:,0].min():.0f}..{d[:,0].max():.0f}, y {d[:,1].min():.0f}..{d[:,1].max():.0f} src px')
class Plan:
    def __init__(self, wd, edl):
        self.edl = edl; t = json.load(open(os.path.join(wd, 'track.json'))); m = json.load(open(os.path.join(wd, 'motion.json')))
        self.fx, self.fy = np.array(t['xs']), np.array(t['ys']); self.dx, self.dy = np.array(m['dxs']), np.array(m['dys'])
        if edl.get('plates_dir'): self.plate_meta = json.load(open(os.path.join(edl['plates_dir'], 'plates.json')))
        g = edl['grade']; xs = np.linspace(0, 1, 4097); cp = np.array(g['curve']); self.lut = self.pchip(cp[:, 0], cp[:, 1], xs).astype(np.float32)
        self.g = g
    @staticmethod
    def pchip(x, y, xi):
        h = np.diff(x); dlt = np.diff(y) / h; m = np.zeros_like(y); m[0], m[-1] = dlt[0], dlt[-1]
        for k in range(1, len(x) - 1):
            m[k] = 0 if dlt[k - 1] * dlt[k] <= 0 else 2 * dlt[k - 1] * dlt[k] / (dlt[k - 1] + dlt[k])
        idx = np.clip(np.searchsorted(x, xi) - 1, 0, len(x) - 2); t = (xi - x[idx]) / h[idx]
        return (2 * t**3 - 3 * t**2 + 1) * y[idx] + (t**3 - 2 * t**2 + t) * h[idx] * m[idx] + (-2 * t**3 + 3 * t**2) * y[idx + 1] + (t**3 - t**2) * h[idx] * m[idx + 1]
    def seg(self, sid): return next(s for s in self.edl['segments'] if s['id'] == sid)
    def plate_mask(self, size):
        """Feature mask for restored plates: eyes, brows, nose and lips only (hair and outer cheeks stay untouched),
        scaled by plate_strength. The face centre sits at (0.5, 0.42) of the plate, as cut by sr_plates.py."""
        if getattr(self, '_pm_size', None) != size:
            w, h = size; yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
            rx, ry = self.edl.get('plate_rx', 0.15) * w, self.edl.get('plate_ry', 0.16) * h
            r = np.sqrt(((xx - w / 2) / rx) ** 2 + ((yy - 0.43 * h) / ry) ** 2)
            m = np.clip((1.25 - r) / 0.55, 0, 1) ** 1.6 * self.edl.get('plate_strength', 0.45)
            self._pm = Image.fromarray((m * 255).astype(np.uint8), 'L'); self._pm_size = size
        return self._pm
    def box(self, s, f):
        a, b = s['in'], s['out']
        if 'zoom' in s:                                   # keyframes [[source_frame, scale], ...], eased between each pair
            kf = s['zoom']; sc = kf[-1][1] if f >= kf[-1][0] else kf[0][1]
            for (f0, s0), (f1, s1) in zip(kf, kf[1:]):
                if f0 <= f < f1:
                    u = (f - f0) / (f1 - f0); e = u * u * u * (u * (u * 6 - 15) + 10)      # smootherstep: no visible start/stop
                    sc = s0 * (s1 / s0) ** e; break                                   # geometric, so the push feels even
        else:
            u = (f - a) / max(1, b - a - 1); e = u * u * (3 - 2 * u); sc = s['scale'][0] + (s['scale'][1] - s['scale'][0]) * e
        w, h = SW / sc, SH / sc
        r = slice(a, b); ax = np.median(self.fx[r] - self.dx[r]); ay = np.median(self.fy[r] - self.dy[r])   # face anchor in background-locked coords
        x0 = ax - s['face_at'][0] * w + self.dx[f]; y0 = ay - s['face_at'][1] * h + self.dy[f]
        cx0, cy0 = min(max(x0, 0), SW - w), min(max(y0, 0), SH - h)
        return (cx0, cy0, cx0 + w, cy0 + h), sc, (abs(cx0 - x0) > 0.01 or abs(cy0 - y0) > 0.01)
    def render(self, rgb8, s, f, OW, OH, grade=True):
        box, sc, clamped = self.box(s, f)
        src = Image.frombuffer('RGB', (SW, SH), rgb8, 'raw', 'RGB', 0, 1)
        pd = self.edl.get('plates_dir') if grade else None
        if pd and os.path.exists(os.path.join(pd, f'{f:04d}.png')):                                   # restored face plate at source resolution
            meta = self.plate_meta[str(f)]; pl = Image.open(os.path.join(pd, f'{f:04d}.png')).convert('RGB')
            src = src.copy(); src.paste(pl, (meta[0], meta[1]), self.plate_mask(pl.size))
        im = src.resize((OW, OH), Image.LANCZOS, box=box)
        x = np.asarray(im, dtype=np.float32) * (1.0 / 255.0)
        if grade:
            g = self.g
            if g.get('dehaze', 0) > 0: x = np.clip(dehaze(x, g['dehaze'], g.get('airlight', [1.0, 0.97, 0.92])), 0, 1)
            x *= np.array(g['wb_gain'], dtype=np.float32)
            x = self.lut[np.clip(x * 4096.0 + 0.5, 0, 4096).astype(np.int32)]                       # tone curve via lookup table
            luma = (x @ np.array([0.2126, 0.7152, 0.0722], dtype=np.float32))[..., None]; x = luma + (x - luma) * np.float32(g['saturation'])
            if g.get('glare_desat', 0) > 0:
                wgt = np.clip((luma - 0.70) / 0.25, 0, 1) ** 1.5; x = x - (x - luma) * (g['glare_desat'] * wgt)
            k = OW / (box[2] - box[0]); px, py = (self.fx[f] - box[0]) * k, (self.fy[f] - box[1]) * k; fw, fh = 150 * k, 200 * k   # face size in output px
            D = 8; key = (OW, OH)                                                                    # masks are smooth: build at 1/8 res, upsample
            if getattr(self, '_grid_key', None) != key:
                self._grid = np.mgrid[0:OH // D, 0:OW // D].astype(np.float32) * D + D / 2; self._grid_key = key
            yy, xx = self._grid
            mf = np.exp(-0.5 * (((xx - px) / (0.95 * fw)) ** 2 + ((yy - (py + 0.05 * fh)) / (0.95 * fh)) ** 2))
            ms = np.exp(-0.5 * (((xx - px) / (3.2 * fw)) ** 2 + ((yy - (py + 1.9 * fh)) / (4.6 * fh)) ** 2))
            vg = 1 - g.get('vignette', 0) * np.clip((((xx - OW / 2) / (OW * 0.62)) ** 2 + ((yy - OH * 0.46) / (OH * 0.62)) ** 2), 0, 1.6)
            gain = (1 + g['face_lift'] * mf) * (1 - g['background_dim'] * (1 - ms)) * vg
            gain = np.asarray(Image.fromarray(gain.astype(np.float32), mode='F').resize((OW, OH), Image.BICUBIC), dtype=np.float32)
            mf_full = np.asarray(Image.fromarray(mf.astype(np.float32), mode='F').resize((OW, OH), Image.BICUBIC), dtype=np.float32) if g.get('face_detail', 0) > 0 else None
            x *= gain[..., None]
            if 'shadow_tint' in g:                                                                   # split tone: cool-green shadows, warm highlights
                lum = np.clip(x @ np.array([0.2126, 0.7152, 0.0722], dtype=np.float32), 0, 1)[..., None]
                x += ((1 - lum) ** 2) * np.array(g['shadow_tint'], dtype=np.float32) + (lum ** 2) * np.array(g['highlight_tint'], dtype=np.float32)
            k1 = OW / 1080.0; lum = np.clip(x @ np.array([0.2126, 0.7152, 0.0722], dtype=np.float32), 0, 1); L = Image.fromarray(lum, mode='F')
            if g.get('sharpen', 0) > 0:                                                              # detail on luma only: no colour fringing
                fine = lum - gblur(lum, g.get('sharpen_radius', 1.1) * k1)
                x += (g['sharpen'] * np.clip(fine, -0.06, 0.06))[..., None]
            for rad, amt in g.get('detail', []):                                                     # multi-band luma detail: fine, mid
                band = lum - gblur(lum, rad * k1); lim = 0.045 if rad < 1.5 else 0.09
                w_ = amt + (g.get('face_detail', 0) * mf_full if (mf_full is not None and rad >= 1.5) else 0)
                x += (w_ * np.clip(band, -lim, lim))[..., None]
            if g.get('clarity', 0) > 0:
                small = Image.fromarray(gblur(np.asarray(L.resize((OW // 4, OH // 4), Image.BILINEAR), dtype=np.float32), 6 * k1), mode='F').resize((OW, OH), Image.BICUBIC)
                x += (g['clarity'] * np.clip(lum - np.asarray(small, dtype=np.float32), -0.12, 0.12))[..., None]
            if g.get('glow', 0) > 0:                                                                 # soft bloom around the cove lighting
                hi = Image.fromarray(gblur(np.asarray(Image.fromarray(np.clip((lum - 0.82) / 0.18, 0, 1).astype(np.float32), mode='F').resize((OW // 8, OH // 8), Image.BILINEAR), dtype=np.float32), 5 * k1), mode='F').resize((OW, OH), Image.BICUBIC)
                x = 1 - (1 - np.clip(x, 0, 1)) * (1 - g['glow'] * np.asarray(hi, dtype=np.float32)[..., None])
            if g.get('grain', 0) > 0:
                x += (np.random.default_rng(f).standard_normal((OH, OW), dtype=np.float32) * g['grain'])[..., None]
        return np.clip(x, 0, 1), clamped
def decode(src, a, b):
    vf = f"select='between(n\\,{a}\\,{b-1})',scale=in_color_matrix=bt709:in_range=tv:out_range=pc,format=rgb24"
    return subprocess.Popen(['ffmpeg', '-v', 'error', '-i', src, '-vf', vf, '-fps_mode', 'passthrough', '-f', 'rawvideo', '-'], stdout=subprocess.PIPE, bufsize=SW * SH * 3)
def main():
    mode, src, wd = sys.argv[1], sys.argv[2], sys.argv[3]
    if mode == 'prep': return prep(src, wd)
    edl = json.load(open(sys.argv[4])); P = Plan(wd, edl); OW, OH = map(int, arg('--size', '1080x1920').split('x')); grade = '--nograde' not in sys.argv
    if mode == 'still':
        f, sid, out = int(sys.argv[5]), sys.argv[6], sys.argv[7]; p = decode(src, f, f + 1); buf = p.stdout.read(SW * SH * 3); p.wait()
        x, _ = P.render(buf, P.seg(sid), f, OW, OH, grade); Image.fromarray((x * 255 + 0.5).astype(np.uint8)).save(out); return
    out = sys.argv[5]; only = arg('--only'); segs = [s for s in edl['segments'] if not only or s['id'] in only.split(',')]
    if only: segs = [P.seg(i) for i in only.split(',')]
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb48le', '-s', f'{OW}x{OH}', '-r', '25', '-i', '-',
                            '-vf', 'scale=out_color_matrix=bt709:out_range=tv,format=yuv422p10le', '-c:v', 'prores_ks', '-profile:v', '3', '-vendor', 'apl0',
                            '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709', '-color_range', 'tv', out], stdin=subprocess.PIPE)
    total = 0; nclamp = 0
    for s in segs:
        p = decode(src, s['in'], s['out'])
        for f in range(s['in'], s['out']):
            buf = p.stdout.read(SW * SH * 3)
            if len(buf) < SW * SH * 3: raise SystemExit(f'short read at frame {f}')
            x, c = P.render(buf, s, f, OW, OH, grade); nclamp += c; enc.stdin.write((x * 65535 + 0.5).astype('<u2').tobytes()); total += 1
        p.wait(); print(f"  {s['id']}: source frames {s['in']}-{s['out']-1} ({s['out']-s['in']} frames) done", flush=True)
    enc.stdin.close(); enc.wait(); print(f'wrote {out}: {total} frames ({total/25:.2f}s), crop clamped on {nclamp} frames')
main()
