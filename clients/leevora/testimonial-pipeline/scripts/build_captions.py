"""Map caption phrases (source time) onto the edit timeline. Writes Remotion props, word-level Caption[] JSON and an SRT.
Usage: build_captions.py <edl.json> <phrases.json> <whisper_words.json> <outdir> <name> [--only id,id] [--endcard seconds]"""
import sys, json, os, re
edl, ph, ww, outdir, name = json.load(open(sys.argv[1])), json.load(open(sys.argv[2]))['phrases'], json.load(open(sys.argv[3])), sys.argv[4], sys.argv[5]
arg = lambda f, d=None: sys.argv[sys.argv.index(f) + 1] if f in sys.argv else d
only = arg('--only'); endcard = float(arg('--endcard', '0')); fps = edl['fps']
segs = [next(s for s in edl['segments'] if s['id'] == i) for i in only.split(',')] if only else edl['segments']
tl = []; pos = 0
for s in segs: tl.append((s['in'] / fps, s['out'] / fps, pos / fps, s['id'])); pos += s['out'] - s['in']
total = pos
def to_edit(t):
    for a, b, e, _ in tl:
        if a - 1e-6 <= t <= b + 1e-6: return e + (t - a)
    return None
pages = []
for p in ph:
    a, b = to_edit(p['s']), to_edit(p['e'])
    if a is None or b is None: continue
    lines = []
    for ln in p['text'].split('|'):
        toks = []
        for w in ln.split(' '):
            core = re.sub(r'[.,!?]+$', '', w); toks.append({'t': w, 'hl': core in p.get('hl', [])})
        lines.append(toks)
    pages.append({'startMs': round(a * 1000), 'endMs': round(b * 1000), 'lines': lines, 'text': p['text'].replace('|', ' ')})
pages.sort(key=lambda x: x['startMs'])
words = []                                   # word-level, Remotion Caption type, for reference / future word-synced styles
for s in ww['segments']:
    for w in s['words']:
        a, b = to_edit(w['s']), to_edit(w['e'])
        if a is not None and b is not None: words.append({'text': w['w'], 'startMs': round(a * 1000), 'endMs': round(b * 1000), 'timestampMs': round((a + b) * 500), 'confidence': round(w['p'], 3)})
words.sort(key=lambda x: x['startMs'])
os.makedirs(outdir, exist_ok=True)
props = {'pages': pages, 'contentFrames': total, 'endCardFrames': round(endcard * fps), 'fps': fps}
json.dump(props, open(os.path.join(outdir, f'{name}.props.json'), 'w'), ensure_ascii=False, indent=1)
json.dump(words, open(os.path.join(outdir, f'{name}.words.json'), 'w'), ensure_ascii=False, indent=1)
def ts(ms): return f'{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}'
with open(os.path.join(outdir, f'{name}.srt'), 'w', encoding='utf-8') as f:
    for i, p in enumerate(pages, 1): f.write(f"{i}\n{ts(p['startMs'])} --> {ts(p['endMs'])}\n" + '\n'.join(' '.join(t['t'] for t in ln) for ln in p['lines']) + '\n\n')
print(f'{name}: {len(pages)} caption pages, {len(words)} words, content {total} frames ({total/fps:.2f}s) + end card {props["endCardFrames"]} frames')
for p in pages: print(f"  {p['startMs']/1000:6.2f}-{p['endMs']/1000:6.2f}  {p['text']}")
