"""Pull the real leevorá logo (vector paths) out of the client's original PDF -> logo_paths.json."""
import json, pikepdf, numpy as np

ROOT = '/tmp/claude-0/-home-user-Adsworm/3d8d5e5a-8f36-56e6-be63-644bad3ee2df/scratchpad'
pdf = pikepdf.open(f'{ROOT}/src/orig.pdf')
page = pdf.pages[0]
PH = float(page.MediaBox[3])
fills = []          # (color, [subpaths of [('M'|'L'|'C', pts...)]], bbox)


def mat(a, b, c, d, e, f):
    return np.array([[a, b, 0], [c, d, 0], [e, f, 1]], float)


def walk(obj, ctm, res, depth=0):
    stack, cur, path, color = [], ctm.copy(), [], (0, 0, 0)
    sub = []

    def T(x, y):
        v = np.array([x, y, 1.0]) @ cur
        return float(v[0]), float(v[1])
    for operands, op in pikepdf.parse_content_stream(obj):
        op = str(op)
        if op == 'q':
            stack.append((cur.copy(), color))
        elif op == 'Q':
            cur, color = stack.pop()
        elif op == 'cm':
            cur = mat(*map(float, operands)) @ cur
        elif op in ('rg', 'sc', 'scn') and len(operands) == 3:
            color = tuple(float(x) for x in operands)
        elif op == 'g':
            color = (float(operands[0]),) * 3
        elif op == 'm':
            sub = [('M', T(*map(float, operands)))]
            path.append(sub)
        elif op == 'l':
            sub.append(('L', T(*map(float, operands))))
        elif op == 'c':
            v = list(map(float, operands))
            sub.append(('C', T(v[0], v[1]), T(v[2], v[3]), T(v[4], v[5])))
        elif op == 'v':
            v = list(map(float, operands))
            p0 = sub[-1][-1]
            sub.append(('C', p0, T(v[0], v[1]), T(v[2], v[3])))
        elif op == 'y':
            v = list(map(float, operands))
            sub.append(('C', T(v[0], v[1]), T(v[2], v[3]), T(v[2], v[3])))
        elif op == 'h':
            sub.append(('Z',))
        elif op == 're':
            x, y, w, h = map(float, operands)
            path.append([('M', T(x, y)), ('L', T(x + w, y)), ('L', T(x + w, y + h)), ('L', T(x, y + h)), ('Z',)])
        elif op in ('f', 'F', 'f*', 'B', 'b'):
            if path:
                fills.append((color, path, op))
            path = []
        elif op in ('n', 'S', 's', 'W', 'W*'):
            if op in ('n', 'S', 's'):
                path = []
        elif op == 'Do':
            name = operands[0]
            xo = res.XObject[name]
            if xo.Subtype == '/Form':
                m = xo.get('/Matrix', [1, 0, 0, 1, 0, 0])
                walk(xo, mat(*map(float, m)) @ cur, xo.get('/Resources', res), depth + 1)


walk(page, np.eye(3), page.Resources)
out = []
for color, path, op in fills:
    pts = [p for sp in path for seg in sp for p in seg[1:]]
    if not pts:
        continue
    xs = [p[0] for p in pts]
    ys = [PH - p[1] for p in pts]
    bb = (min(xs) / 72, min(ys) / 72, max(xs) / 72, max(ys) / 72)
    out.append({'color': color, 'bbox_in': bb, 'evenodd': op == 'f*',
                'path': [[[seg[0]] + [[q[0] / 72, (PH - q[1]) / 72] for q in seg[1:]] for seg in sp] for sp in path]})
print(len(out), 'filled paths')
for o in out:
    b = o['bbox_in']
    if b[1] < 9 and b[3] - b[1] < 5:
        print([round(c, 3) for c in o['color']], [round(v, 2) for v in b], len(o['path']))
json.dump(out, open(f'{ROOT}/chk/orig_fills.json', 'w'))
