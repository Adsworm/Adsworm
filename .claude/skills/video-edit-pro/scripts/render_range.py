"""Render a frame range of one segment to PNGs (for A/B and flicker tests). Usage: render_range.py <src> <wd> <edl> <seg> <a> <b> <outdir>"""
import sys, os, numpy as np
from PIL import Image
here = os.path.dirname(os.path.abspath(__file__)); src_code = open(os.path.join(here, 'render_base.py')).read().replace('\nmain()\n', '\n')
ns = {'__name__': 'rb'}; exec(compile(src_code, 'render_base', 'exec'), ns)
import json
src, wd, edlp, sid, a, b, out = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], int(sys.argv[5]), int(sys.argv[6]), sys.argv[7]
os.makedirs(out, exist_ok=True); edl = json.load(open(edlp)); P = ns['Plan'](wd, edl); seg = P.seg(sid)
p = ns['decode'](src, a, b)
for f in range(a, b):
    buf = p.stdout.read(ns['SW'] * ns['SH'] * 3); x, _ = P.render(buf, seg, f, 1080, 1920, True)
    Image.fromarray((x * 255 + 0.5).astype(np.uint8)).save(os.path.join(out, f'{f:04d}.png'))
p.wait(); print('rendered', b - a, 'frames ->', out)
