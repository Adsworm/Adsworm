"""Resemble Enhance on CPU. Usage: enh_resemble.py <in.wav> <out_denoise.wav> <out_enhance.wav> [nfe] [lambd] [tau]"""
import sys, warnings, time; warnings.filterwarnings('ignore')
import torch, torchaudio
from resemble_enhance.enhancer.inference import denoise, enhance
src, o1, o2 = sys.argv[1:4]; nfe = int(sys.argv[4]) if len(sys.argv) > 4 else 64; lambd = float(sys.argv[5]) if len(sys.argv) > 5 else 0.9; tau = float(sys.argv[6]) if len(sys.argv) > 6 else 0.5
torch.set_num_threads(4); torch.manual_seed(0)
wav, sr = torchaudio.load(src); wav = wav.mean(0)
t = time.time(); d, dsr = denoise(wav, sr, 'cpu'); torchaudio.save(o1, d[None], dsr); print(f'denoise: {time.time()-t:.0f}s -> {o1} @ {dsr}', flush=True)
t = time.time(); e, esr = enhance(wav, sr, 'cpu', nfe=nfe, solver='midpoint', lambd=lambd, tau=tau); torchaudio.save(o2, e[None], esr); print(f'enhance (nfe={nfe}, lambd={lambd}, tau={tau}): {time.time()-t:.0f}s -> {o2} @ {esr}', flush=True)
