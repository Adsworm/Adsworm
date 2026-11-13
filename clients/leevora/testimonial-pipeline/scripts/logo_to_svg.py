"""Convert the client's extracted vector logo (leevora_logo.json) to SVG. Paths are copied 1:1; nothing is redrawn."""
import json, sys
src, out, fill = sys.argv[1], sys.argv[2], sys.argv[3]
d = json.load(open(src))
S = 100.0  # px per source inch
def path_d(item):
    parts = []
    for sub in item['path']:
        for seg in sub:
            op = seg[0]
            if op == 'Z':
                parts.append('Z'); continue
            pts = ' '.join(f'{p[0]*S:.3f},{p[1]*S:.3f}' for p in seg[1:])
            parts.append(f'{op}{pts}')
    return ' '.join(parts)
els = []
for grp in ('word', 'desc'):
    for it in d[grp]:
        rule = 'evenodd' if it.get('evenodd') else 'nonzero'
        els.append(f'<path fill-rule="{rule}" d="{path_d(it)}"/>')
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {d["w"]*S:.3f} {d["h"]*S:.3f}" fill="{fill}">' + ''.join(els) + '</svg>')
open(out, 'w').write(svg)
print('logo colour in source (RGB 0-1):', d['color'], '| size in:', round(d['w'],3), 'x', round(d['h'],3), '| word paths', len(d['word']), '| descriptor paths', len(d['desc']))
