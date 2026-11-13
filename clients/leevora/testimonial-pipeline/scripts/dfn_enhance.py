"""DeepFilterNet3 speech enhancement, CPU. Usage: dfn_enhance.py <model_dir> <in.wav 48k mono> <out.wav> <atten_lim_db|none>"""
import sys, warnings; warnings.filterwarnings('ignore')
import numpy as np, soundfile as sf, torch, time
from df.enhance import init_df, enhance
model_dir, src, dst, lim = sys.argv[1:5]
model, state, _ = init_df(model_base_dir=model_dir, post_filter=False, log_level='ERROR')
x, sr = sf.read(src, dtype='float32', always_2d=True); assert sr == state.sr() == 48000, (sr, state.sr())
t = time.time(); y = enhance(model, state, torch.from_numpy(x.T.copy()), atten_lim_db=None if lim == 'none' else float(lim))
sf.write(dst, y.numpy().T, sr, subtype='FLOAT'); print(f'{dst}: atten_lim={lim} done in {time.time()-t:.1f}s for {len(x)/sr:.1f}s audio')
