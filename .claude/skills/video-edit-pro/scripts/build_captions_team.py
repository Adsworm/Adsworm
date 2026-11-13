"""Team-style caption pages (two-tier white/gold lines, optional logo) mapped from source time onto the edit timeline.
Usage: build_captions_team.py <edl.json> <phrases_team.json> <out_props.json> <out.srt> [--endcard seconds]"""
import sys, json
edl, ph, outp, srtp = json.load(open(sys.argv[1])), json.load(open(sys.argv[2])), sys.argv[3], sys.argv[4]
endcard = float(sys.argv[sys.argv.index('--endcard') + 1]) if '--endcard' in sys.argv else 0
fps = edl['fps']; tl = []; pos = 0
for s in edl['segments']: tl.append((s['in'] / fps, s['out'] / fps, pos / fps)); pos += s['out'] - s['in']
def span(a, b):
    best = max(tl, key=lambda q: min(b, q[1]) - max(a, q[0])); s0, s1, off = best
    return (off + max(a, s0) - s0, off + min(b, s1) - s0) if min(b, s1) > max(a, s0) else (None, None)
pages = []
for p in ph['pages']:
    a, b = span(p['s'], p['e'])
    if a is None: continue
    pages.append({'startMs': round(a * 1000), 'endMs': round(b * 1000), 'lines': [{'text': l.lstrip('*'), 'gold': l.startswith('*')} for l in p['lines']], 'logo': bool(p.get('logo'))})
pages.sort(key=lambda x: x['startMs'])
pill = ph.get('pill'); props = {'fps': fps, 'contentFrames': pos, 'endCardFrames': round(endcard * fps), 'pages': pages,
        'pill': {'text': pill['text'], 'fromMs': round(pill['from_edit_s'] * 1000), 'toMs': round(pill['to_edit_s'] * 1000)} if pill else None}
json.dump(props, open(outp, 'w'), ensure_ascii=False, indent=1)
def ts(ms): return f'{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}'
with open(srtp, 'w', encoding='utf-8') as f:
    for i, p in enumerate(pages, 1): f.write(f"{i}\n{ts(p['startMs'])} --> {ts(p['endMs'])}\n" + '\n'.join(l['text'] + (' leevorá.' if p['logo'] and j == len(p['lines']) - 1 else '') for j, l in enumerate(p['lines'])) + '\n\n')
print(f'{len(pages)} team pages, content {pos} frames + end card {props["endCardFrames"]}'); [print(f"  {p['startMs']/1000:6.2f}-{p['endMs']/1000:6.2f}  " + ' / '.join(('*' if l['gold'] else '') + l['text'] for l in p['lines']) + (' [logo]' if p['logo'] else '')) for p in pages]
