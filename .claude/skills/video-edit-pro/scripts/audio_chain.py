"""Leevorá testimonial voice chain. Reproducible: prefilter -> DeepFilterNet3 (limited) -> EQ -> compressor -> loudness -> limiter.
Usage: audio_chain.py <in.wav|mov> <out.wav> <atten_lim_db|0=no denoise> <target_lufs> [--no-finish]"""
import sys, subprocess, json, os, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.environ.get('VEP_WORK', os.path.dirname(HERE))   # workdir made by setup/bootstrap.sh
DFN_PY = os.path.join(ROOT, 'venvs/dfn/bin/python'); DFN_MODEL = os.path.join(ROOT, 'models/dfn/DeepFilterNet3')
# Measured on IMG_5776.MOV: hum lines at 101.1 / 200.7 Hz, AC drone lines at 392.6 / 418.9 Hz; her fundamental sits near 200 Hz,
# so the 200 Hz notch is narrow and shallow. High-pass at 115 Hz (24 dB/oct) is below her voice.
PRE = ('pan=mono|c0=0.5*c0+0.5*c1,highpass=f=115:p=2,highpass=f=115:p=2,'
       'equalizer=f=101.1:t=q:w=14:g=-30,equalizer=f=200.7:t=q:w=35:g=-9,equalizer=f=392.6:t=q:w=40:g=-8,equalizer=f=418.9:t=q:w=40:g=-8,volume=18dB')
# Finishing: small low-mid dip for room boxiness, presence + air to offset the distant mic and the ~2.5 dB HF loss measured after denoise,
# then gentle 2.5:1 compression. No de-esser: sibilance band is already weak in this recording.
FINISH = ('equalizer=f=320:t=q:w=1.1:g=-2.0,equalizer=f=3400:t=q:w=0.9:g=2.0,highshelf=f=6500:g=3.0:t=s:w=0.7,'
          'acompressor=threshold=0.063:ratio=2.5:attack=12:release=160:knee=4:makeup=1')
def run(*a): return subprocess.run(a, capture_output=True, text=True)
def lufs(p):
    t = run('ffmpeg', '-hide_banner', '-nostats', '-i', p, '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json', '-f', 'null', '-').stderr
    j = json.loads(t[t.rindex('{'):]); return float(j['input_i']), float(j['input_tp']), float(j['input_lra'])
def main():
    src, dst, lim, target = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4]); finish = '--no-finish' not in sys.argv
    tmp = tempfile.mkdtemp(prefix='chain_', dir=os.path.dirname(os.path.abspath(dst)))
    a, b, c = (os.path.join(tmp, n) for n in ('pre.wav', 'dfn.wav', 'fin.wav'))
    if lim > 0:
        r = run('ffmpeg', '-v', 'error', '-y', '-i', src, '-map', '0:a:0', '-af', PRE, '-ar', '48000', '-c:a', 'pcm_f32le', a); assert r.returncode == 0, r.stderr
        r = run(DFN_PY, os.path.join(HERE, 'dfn_enhance.py'), DFN_MODEL, a, b, str(lim)); assert r.returncode == 0, r.stderr[-800:]
    else:
        r = run('ffmpeg', '-v', 'error', '-y', '-i', src, '-map', '0:a:0', '-af', 'pan=mono|c0=0.5*c0+0.5*c1', '-ar', '48000', '-c:a', 'pcm_f32le', b); assert r.returncode == 0, r.stderr
    if finish and lim > 0:
        r = run('ffmpeg', '-v', 'error', '-y', '-i', b, '-af', FINISH, '-c:a', 'pcm_f32le', c); assert r.returncode == 0, r.stderr
    else: c = b
    i, tp, lra = lufs(c); g = target - i
    # gain to target, then a transparent brick-wall limiter at -1.5 dBFS (only catches peaks the gain pushes over)
    out_tmp = os.path.join(tmp, 'out.wav')
    r = run('ffmpeg', '-v', 'error', '-y', '-i', c, '-af', f'volume={g:.2f}dB,alimiter=limit=0.841:attack=5:release=80:level=disabled', '-c:a', 'pcm_s24le', out_tmp); assert r.returncode == 0, r.stderr
    i2, tp2, lra2 = lufs(out_tmp)
    if abs(i2 - target) > 0.3:   # limiter took some loudness back: one correction pass
        g += target - i2
        run('ffmpeg', '-v', 'error', '-y', '-i', c, '-af', f'volume={g:.2f}dB,alimiter=limit=0.841:attack=5:release=80:level=disabled', '-c:a', 'pcm_s24le', out_tmp); i2, tp2, lra2 = lufs(out_tmp)
    os.replace(out_tmp, dst)
    for f in os.listdir(tmp): os.remove(os.path.join(tmp, f))
    os.rmdir(tmp)
    print(f'{os.path.basename(dst)}: denoise_limit={lim:g} dB finish={finish and lim>0} | before gain {i:.1f} LUFS / {tp:.1f} dBTP -> gain {g:+.1f} dB -> {i2:.1f} LUFS, {tp2:.1f} dBTP, LRA {lra2:.1f}')
main()
