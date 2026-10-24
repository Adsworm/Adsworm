"""HarfBuzz shaping + fontTools outlines -> skia paths in inch units (y down)."""
import skia, uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.basePen import BasePen

FONT_DIR = '/tmp/claude-0/-home-user-Adsworm/3d8d5e5a-8f36-56e6-be63-644bad3ee2df/scratchpad/fonts'


class _SkiaPen(BasePen):
    def __init__(self, glyphset, path, sx, ox, oy):
        super().__init__(glyphset)
        self.p, self.s, self.ox, self.oy = path, sx, ox, oy

    def _pt(self, pt):
        return self.ox + pt[0] * self.s, self.oy - pt[1] * self.s

    def _moveTo(self, pt): self.p.moveTo(*self._pt(pt))
    def _lineTo(self, pt): self.p.lineTo(*self._pt(pt))
    def _curveToOne(self, a, b, c): self.p.cubicTo(*self._pt(a), *self._pt(b), *self._pt(c))
    def _qCurveToOne(self, a, b): self.p.quadTo(*self._pt(a), *self._pt(b))
    def _closePath(self): self.p.close()


class Font:
    _cache = {}

    def __init__(self, name):
        path = f'{FONT_DIR}/{name}.ttf'
        self.tt = TTFont(path)
        self.gs = self.tt.getGlyphSet()
        self.order = self.tt.getGlyphOrder()
        self.upem = self.tt['head'].unitsPerEm
        os2 = self.tt['OS/2']
        self.cap = getattr(os2, 'sCapHeight', 0.7 * self.upem) / self.upem
        self.xh = getattr(os2, 'sxHeight', 0.5 * self.upem) / self.upem
        blob = hb.Blob.from_file_path(path)
        self.hbfont = hb.Font(hb.Face(blob))

    @classmethod
    def get(cls, name):
        if name not in cls._cache:
            cls._cache[name] = Font(name)
        return cls._cache[name]

    def shape(self, text, size, tracking=0.0, features=None):
        """Return [(glyphname, x_in, y_in)], advance_width_in. tracking in em."""
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(self.hbfont, buf, features or {'kern': True, 'liga': True})
        s = size / self.upem
        x, out = 0.0, []
        n = len(buf.glyph_infos)
        for i, (info, pos) in enumerate(zip(buf.glyph_infos, buf.glyph_positions)):
            out.append((self.order[info.codepoint], x + pos.x_offset * s, -pos.y_offset * s))
            x += pos.x_advance * s + (tracking * size if i < n - 1 else 0)
        return out, x

    def path(self, text, size, x, y, align='left', tracking=0.0, features=None):
        """Outline path; (x, y) = anchor at baseline. align: left|center|right."""
        glyphs, w = self.shape(text, size, tracking, features)
        ox = x - {'left': 0, 'center': w / 2, 'right': w}[align]
        p = skia.Path()
        s = size / self.upem
        for g, gx, gy in glyphs:
            self.gs[g].draw(_SkiaPen(self.gs, p, s, ox + gx, y + gy))
        return p, w

    def width(self, text, size, tracking=0.0):
        return self.shape(text, size, tracking)[1]

    def fit_size(self, text, width, tracking=0.0):
        return width / self.width(text, 1.0, tracking)
