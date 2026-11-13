"""AI face-region restoration plates with Real-ESRGAN (no face prior: it sharpens and cleans, it does not redraw a face).
For each source frame: crop a box around the tracked face, run the model, bring the result back to the crop's own size,
save it as a plate that render_base.py pastes in with a feathered mask before reframing.
Usage: sr_plates.py <src.mov> <track.json> <model.safetensors> <out_dir> <mode: native|half> <frames: a-b,c-d,...> [box WxH]

Detail-max fusion (default): the plate keeps the ORIGINAL low frequencies and, at each pixel, whichever fine detail is stronger,
original or AI. Edges the model sharpens (lashes, lid and lip lines) come through; skin texture the model would erase stays.
No smoothing, no change of shape or tone."""
import sys, os, json, subprocess, time, warnings; warnings.filterwarnings('ignore')
import numpy as np, torch
from PIL import Image
import spandrel
src, trackp, modelp, out, mode, spans = sys.argv[1:7]; BW, BH = map(int, (sys.argv[7] if len(sys.argv) > 7 else '480x600').split('x'))
SW, SH = 2160, 3840; torch.set_num_threads(4)
t = json.load(open(trackp)); fx, fy = np.array(t['xs']), np.array(t['ys'])
m = spandrel.ModelLoader().load_from_file(modelp).model.eval()
os.makedirs(out, exist_ok=True); metap = os.path.join(out, 'plates.json'); meta = json.load(open(metap)) if os.path.exists(metap) else {}
frames = [f for sp in spans.split(',') for f in range(int(sp.split('-')[0]), int(sp.split('-')[1]))]
t0 = time.time(); done = 0
for a, b in [tuple(map(int, sp.split('-'))) for sp in spans.split(',')]:
    vf = f"select='between(n\\,{a}\\,{b-1})',scale=in_color_matrix=bt709:in_range=tv:out_range=pc,format=rgb24"
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', src, '-vf', vf, '-fps_mode', 'passthrough', '-f', 'rawvideo', '-'], stdout=subprocess.PIPE, bufsize=SW * SH * 3)
    for f in range(a, b):
        buf = p.stdout.read(SW * SH * 3)
        if os.path.exists(os.path.join(out, f'{f:04d}.png')): continue
        fr = np.frombuffer(buf, np.uint8).reshape(SH, SW, 3)
        x0 = int(np.clip(round(fx[f] - BW / 2), 0, SW - BW)); y0 = int(np.clip(round(fy[f] - BH * 0.42), 0, SH - BH))
        crop = Image.fromarray(fr[y0:y0 + BH, x0:x0 + BW])
        inp = crop if mode == 'native' else crop.resize((BW // 2, BH // 2), Image.LANCZOS)
        with torch.no_grad():
            y = m(torch.from_numpy(np.asarray(inp, np.float32) / 255.0).permute(2, 0, 1)[None]).clamp(0, 1)[0].permute(1, 2, 0).numpy()
        ai = np.asarray(Image.fromarray((y * 255 + 0.5).astype(np.uint8)).resize((BW, BH), Image.LANCZOS), np.float32)
        org = np.asarray(crop, np.float32)
        def lp(a):                                                     # low-pass at about 2 source px
            im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)); return np.asarray(im.resize((BW // 3, BH // 3), Image.BILINEAR).resize((BW, BH), Image.BICUBIC), np.float32)
        lo = lp(org); d_o = org - lo; d_a = ai - lp(ai)
        lum = lambda d: d @ np.array([0.2126, 0.7152, 0.0722], np.float32)
        w = np.clip((np.abs(lum(d_a)) - np.abs(lum(d_o))) / 10.0 + 0.5, 0, 1)        # soft choice: no per-frame switching
        w = np.asarray(Image.fromarray((w * 255).astype(np.uint8)).resize((BW // 2, BH // 2), Image.BILINEAR).resize((BW, BH), Image.BILINEAR), np.float32)[..., None] / 255.0
        fused = lo + w * d_a + (1 - w) * d_o
        Image.fromarray(np.clip(fused + 0.5, 0, 255).astype(np.uint8)).save(os.path.join(out, f'{f:04d}.png'))
        meta[str(f)] = [x0, y0, BW, BH]; done += 1
        if done % 25 == 0:
            json.dump(meta, open(metap, 'w')); print(f'  {done} plates, {(time.time()-t0)/done:.2f}s each', flush=True)
    p.wait()
json.dump(meta, open(metap, 'w')); print(f'{done} plates in {time.time()-t0:.0f}s ({(time.time()-t0)/max(done,1):.2f}s each) -> {out}')
