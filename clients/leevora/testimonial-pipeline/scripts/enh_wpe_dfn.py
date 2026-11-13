"""WPE de-reverberation (2 phone mics) followed by DeepFilterNet3. Usage: enh_wpe_dfn.py <model_dir> <stereo_in.wav 48k> <out.wav> <atten_lim_db|none> <post_filter 0|1>"""
import sys, warnings; warnings.filterwarnings('ignore')
import numpy as np, soundfile as sf, torch
from nara_wpe.wpe import wpe
from nara_wpe.utils import stft, istft
from df.enhance import init_df, enhance
model_dir, src, dst, lim, pf = sys.argv[1:6]
x, sr = sf.read(src, dtype='float64', always_2d=True); assert sr == 48000
size, shift = 2048, 512
Y = stft(x.T, size=size, shift=shift).transpose(2, 0, 1)            # (freq, channels, frames)
Z = wpe(Y, taps=12, delay=3, iterations=4, statistics_mode='full').transpose(1, 2, 0)
z = istft(Z, size=size, shift=shift)[:, :len(x)]
mono = z.mean(0).astype(np.float32)
sf.write(dst.replace('.wav', '_wpeonly.wav'), mono, sr, subtype='FLOAT')
model, state, _ = init_df(model_base_dir=model_dir, post_filter=bool(int(pf)), log_level='ERROR')
y = enhance(model, state, torch.from_numpy(mono[None]), atten_lim_db=None if lim == 'none' else float(lim))
sf.write(dst, y.numpy().T, sr, subtype='FLOAT'); print('wrote', dst)
