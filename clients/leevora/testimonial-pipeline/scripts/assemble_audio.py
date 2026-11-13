"""Cut the mastered voice track to the EDL (sample-accurate), with short fades at every non-contiguous join.
Usage: assemble_audio.py <voice_full.wav> <edl.json> <out.wav> <target_lufs> [--only id,id] [--tail seconds] [--final-fade seconds]"""
import sys, json, subprocess
voice, edlp, out, target = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4])
arg = lambda f, d=None: sys.argv[sys.argv.index(f) + 1] if f in sys.argv else d
edl = json.load(open(edlp)); only = arg('--only'); tail = float(arg('--tail', '0'))
segs = [next(s for s in edl['segments'] if s['id'] == i) for i in only.split(',')] if only else edl['segments']
runs = []                                    # merge segments that are contiguous in the source: no audio edit there
for s in segs:
    if runs and runs[-1][1] == s['in']: runs[-1][1] = s['out']
    else: runs.append([s['in'], s['out']])
FI, FO, FEND = 0.030, 0.015, float(arg('--final-fade', '0.040')); parts = []; lab = []
for i, (a, b) in enumerate(runs):
    t0, t1 = a / 25, b / 25; d = t1 - t0
    parts.append(f"[0:a]atrim={t0:.4f}:{t1:.4f},asetpts=PTS-STARTPTS,afade=t=in:d={FI},afade=t=out:st={d-(FEND if i == len(runs) - 1 else FO):.4f}:d={FEND if i == len(runs) - 1 else FO}[a{i}]"); lab.append(f'[a{i}]')
fc = ';'.join(parts) + f";{''.join(lab)}concat=n={len(runs)}:v=0:a=1[cat];[cat]apad=pad_dur={tail}[pad]"
tmp = out + '.tmp.wav'
r = subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', voice, '-filter_complex', fc, '-map', '[pad]', '-c:a', 'pcm_f32le', tmp], capture_output=True, text=True); assert r.returncode == 0, r.stderr
t = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', tmp, '-af', 'loudnorm=I=-14:TP=-1.5:print_format=json', '-f', 'null', '-'], capture_output=True, text=True).stderr
i = float(json.loads(t[t.rindex('{'):])['input_i']); g = target - i
r = subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', tmp, '-af', f'volume={g:.2f}dB,alimiter=limit=0.841:attack=5:release=80:level=disabled,aformat=channel_layouts=stereo', '-c:a', 'pcm_s24le', out], capture_output=True, text=True); assert r.returncode == 0, r.stderr
import os; os.remove(tmp)
t = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', out, '-af', 'loudnorm=I=-14:TP=-1.5:print_format=json', '-f', 'null', '-'], capture_output=True, text=True).stderr; j = json.loads(t[t.rindex('{'):])
print(f"{os.path.basename(out)}: source runs {[(a/25, b/25) for a, b in runs]} | {j['input_i']} LUFS, {j['input_tp']} dBTP")
