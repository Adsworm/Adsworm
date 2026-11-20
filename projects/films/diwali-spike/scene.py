"""The Diwali Spike: what 18 ad accounts showed (Adsworm, Nov 2026).

One board: a four-bar chart of the cost of one enquiry (September, October, Diwali week, the three days
after), a row of four detail clusters under it, the title above and the end slate below. The camera opens
on the peak, goes back to September, and travels forward in time.

Every number is in script.json `fact_notes`; the source is docs/pipeline/2026-11-12/02-account-data.md.
Frames keep the hero in the top 74%: burn_captions.py uses the bottom 26%.
"""
import skia

from engine import (BigText, Film, Item, PenMark, Stamp, clamp, draw_text, ease_in_out, ease_out_back,
                    ease_out_cubic, paint, ramp, text_width)

# Adsworm brand (brands/adsworm/brand.json): navy ground, cream type, blue for energy, gold for proof
NAVY, PANEL = (8, 12, 20), (17, 25, 44)
CREAM, MUTED = (240, 238, 232), (170, 174, 186)
BLUE, GOLD, STEEL = (43, 123, 255), (200, 169, 110), (92, 108, 138)

XB = [0, 5200, 10400, 15600]            # bar centres; the detail clusters sit in the same columns
VAL = [147, 165, 210, 164]              # rupees per enquiry, pooled across the 18 accounts
HB = [v * 18 for v in VAL]              # bar heights in world px
BW = 1700
MID = (XB[0] + XB[-1]) / 2
ROW = 1500                              # the detail row and the end slate sit this much lower than the chart needs


def mix(a, b, u):
    return tuple(a[i] + (b[i] - a[i]) * u for i in range(3))


class Bar(Item):
    """A bar that grows from one edge. grow="up": (x, y) is the middle of its base. grow="right": (x, y) is
    the middle of its left edge. resize=(t, new_length, dur) changes its length later and leaves an outline
    of the old one."""
    z = 20

    def __init__(self, x, y, w, h, t_in, dur=1.0, rgb=BLUE, grow="up", resize=None, t_out=None, sfx=True):
        super().__init__(t_in, t_out, None, sfx)
        self.x, self.y, self.w, self.h, self.dur, self.rgb, self.grow, self.resize = x, y, w, h, dur, rgb, grow, resize

    def rect(self, length):
        if self.grow == "up":
            return skia.Rect.MakeXYWH(self.x - self.w / 2, self.y - length, self.w, length)
        return skia.Rect.MakeXYWH(self.x, self.y - self.h / 2, length, self.h)

    def bounds(self, res):
        return self.rect(self.h if self.grow == "up" else self.w).makeOutset(300, 300)

    def cues(self):
        return [("slide", self.t_in, 0.45, {})]

    def draw(self, c, res, t):
        full = self.h if self.grow == "up" else self.w
        length = full * ease_out_cubic(ramp(t, self.t_in, self.dur))
        a = self.fade(t)
        if length <= 1 or a <= 0:
            return
        if self.resize and t > self.resize[0]:
            rt, new, rd = self.resize
            length = full + (new - full) * ease_in_out(ramp(t, rt, rd))
            c.drawRect(self.rect(full), paint(self.rgb, 0.55 * a, stroke=7))
        r = self.rect(length)
        c.drawRect(r.makeOutset(40, 40), paint(self.rgb, 0.16 * a, blur=70))
        p = skia.Paint(AntiAlias=True)
        dark = mix(self.rgb, NAVY, 0.5)
        ends = [skia.Point(r.left(), r.top()), skia.Point(r.left(), r.bottom())] if self.grow == "up" else \
               [skia.Point(r.right(), r.top()), skia.Point(r.left(), r.top())]
        p.setShader(skia.GradientShader.MakeLinear(ends, [skia.Color(*map(int, self.rgb), int(255 * a)), skia.Color(*map(int, dark), int(255 * a))]))
        c.drawRect(r, p)


class Line(Item):
    """A straight line drawn on from (x0, y) to (x1, y); dash=(on, off) makes it dashed."""
    z = 30

    def __init__(self, x0, x1, y, t_in, dur=0.9, rgb=CREAM, width=10, dash=None, alpha=1.0, t_out=None, sfx=False):
        super().__init__(t_in, t_out, None, sfx)
        self.x0, self.x1, self.y, self.dur, self.rgb, self.wd, self.dash, self.alpha = x0, x1, y, dur, rgb, width, dash, alpha

    def bounds(self, res):
        return skia.Rect.MakeLTRB(min(self.x0, self.x1) - 100, self.y - 100, max(self.x0, self.x1) + 100, self.y + 100)

    def cues(self):
        return [("pencil", self.t_in, 0.4, {})]

    def draw(self, c, res, t):
        u = ease_in_out(ramp(t, self.t_in, self.dur))
        if u <= 0:
            return
        p = paint(self.rgb, self.alpha * self.fade(t), stroke=self.wd)
        if self.dash:
            p.setStrokeCap(skia.Paint.kButt_Cap)
            p.setPathEffect(skia.DashPathEffect.Make([float(self.dash[0]), float(self.dash[1])], 0.0))
        path = skia.Path(); path.moveTo(self.x0, self.y); path.lineTo(self.x0 + (self.x1 - self.x0) * u, self.y)
        c.drawPath(path, p)


class Num(Item):
    """A clean number that rolls from `start` to `value`."""
    z = 70

    def __init__(self, x, y, size, value, t_in, dur=1.0, prefix="", suffix="", rgb=CREAM, start=0, t_out=None, sfx=True):
        super().__init__(t_in, t_out, None, sfx)
        self.x, self.y, self.size, self.value, self.dur = x, y, size, value, dur
        self.prefix, self.suffix, self.rgb, self.start = prefix, suffix, rgb, start

    def bounds(self, res):
        r = self.size * 4
        return skia.Rect.MakeLTRB(self.x - r, self.y - self.size * 1.5, self.x + r, self.y + self.size)

    def cues(self):
        return [("ticks", self.t_in, 0.5, {})]

    def draw(self, c, res, t):
        a = ramp(t, self.t_in, 0.25) * self.fade(t)
        if a <= 0:
            return
        v = int(round(self.start + (self.value - self.start) * ease_out_cubic(ramp(t, self.t_in, self.dur))))
        txt = f"{self.prefix}{v:,}{self.suffix}"
        c.save(); c.translate(8, 16)
        draw_text(c, res, txt, self.x, self.y, self.size, "cond", (0, 0, 0), 0.5 * a, 0.02, "center")
        c.restore()
        draw_text(c, res, txt, self.x, self.y, self.size, "cond", self.rgb, a, 0.02, "center")


class Dots(Item):
    """One dot per ad account. They pop in from t0; from t_mark the first `n_mark` turn gold one by one and
    the last `n_out` go hollow (not comparable)."""
    z = 25

    def __init__(self, pts, t0, t_mark, n_mark, n_out, r=170, t_out=None, sfx=True):
        super().__init__(t0, t_out, None, sfx)
        self.pts, self.t0, self.t_mark, self.n_mark, self.n_out, self.r = list(pts), t0, t_mark, n_mark, n_out, r
        xs = [p[0] for p in self.pts]; ys = [p[1] for p in self.pts]
        self.box = skia.Rect.MakeLTRB(min(xs) - 400, min(ys) - 400, max(xs) + 400, max(ys) + 400)

    def bounds(self, res):
        return self.box

    def cues(self):
        return [("shimmer", self.t0, 0.5, {}), ("ticks", self.t_mark, 0.5, {})]

    def draw(self, c, res, t):
        a = self.fade(t); n = len(self.pts)
        for i, (x, y) in enumerate(self.pts):
            u = ramp(t, self.t0 + i * 0.06, 0.25)
            if u <= 0:
                continue
            r = self.r * ease_out_back(u)
            if i >= n - self.n_out:                      # could not be compared: an empty ring after the mark
                h = ramp(t, self.t_mark, 0.4)
                c.drawCircle(x, y, r, paint(BLUE, (1 - h) * a))
                c.drawCircle(x, y, r - 9, paint(MUTED, h * a, stroke=18))
                continue
            g = ramp(t, self.t_mark + i * 0.07, 0.22) if i < self.n_mark else 0.0
            rgb = mix(BLUE, GOLD, g)
            rr = r * (1 + 0.18 * (1 - abs(2 * g - 1)) if 0 < g < 1 else 1)
            c.drawCircle(x, y, rr * 1.9, paint(rgb, 0.16 * a, blur=40))
            c.drawCircle(x, y, rr, paint(rgb, a))


class Panel(Item):
    """A dark rounded panel with a thin accent edge; text is added on top of it as BigText."""
    z = 12

    def __init__(self, x, y, w, h, t_in, accent=BLUE, t_out=None, sfx=True):
        super().__init__(t_in, t_out, None, sfx)
        self.x, self.y, self.w, self.h, self.accent = x, y, w, h, accent

    def bounds(self, res):
        return skia.Rect.MakeXYWH(self.x - self.w / 2, self.y - self.h / 2, self.w, self.h).makeOutset(300, 300)

    def cues(self):
        return [("pop", self.t_in, 0.5, {})]

    def draw(self, c, res, t):
        u = ease_out_cubic(ramp(t, self.t_in, 0.45))
        a = ramp(t, self.t_in, 0.2) * self.fade(t)
        if a <= 0:
            return
        c.save(); c.translate(self.x, self.y + (1 - u) * 110)
        rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-self.w / 2, -self.h / 2, self.w, self.h), 40, 40)
        c.save(); c.translate(0, 30); c.drawRRect(rr, paint((0, 0, 0), 0.45 * a, blur=50)); c.restore()
        c.drawRRect(rr, paint(PANEL, a))
        c.drawRRect(rr, paint(self.accent, 0.5 * a, stroke=6))
        c.save(); c.clipRRect(rr, skia.ClipOp.kIntersect, True)
        c.drawRect(skia.Rect.MakeXYWH(-self.w / 2, -self.h / 2, self.w * 0.022, self.h), paint(self.accent, a))
        c.restore(); c.restore()


def build_film(doc):
    L, E, W = doc.L, doc.E, doc.W
    R = doc.res()
    film = Film(doc.duration, fps=30, look="night")
    film.look["bg"] = NAVY
    film.fade_out = 1.6

    def text(s, x, y, size, t, rgb=CREAM, max_w=None, **kw):
        """Clean condensed caps, centred on x, baseline y; shrinks to fit max_w."""
        track = kw.pop("track", 0.04)
        if max_w:
            size = min(size, size * max_w / text_width(R, s, size, "cond", track))
        return film.add(BigText(s, x, y, size, t, rgb=rgb, track=track, grunge=False, shadow=kw.pop("shadow", False), **kw))

    def cam(t, x, top, zoom, rot=0.0, fx=None, fy=None, radius=None, strength=0.5):
        """Camera key by the frame's top edge; the spotlight sits in the middle of the caption-free area."""
        film.cam(t, x, top + 1080 / zoom, zoom, rot)
        film.focus(t, x if fx is None else fx, top + 800 / zoom if fy is None else fy, radius or 1500 / zoom, strength)

    def bar_top(i, size=900):
        """Baselines for the number above bar i and the name above the number."""
        num = -HB[i] - 240
        return num, num - size * 0.72 - 190

    # ------------------------------------------------------------------ cold open: the peak, before anything else
    num3, name3 = bar_top(2, 1100)
    date_y = name3 - 420
    t_title = E(3) + 0.6
    text("1–8 NOV 2026", XB[2], date_y, 400, L(1) + 0.15, GOLD, track=0.1, type_on=0.6, t_out=E(3) + 0.1)
    text("COST OF ONE ENQUIRY · 18 ACCOUNTS, BLENDED", XB[2], name3 + 10, 230, L(2) + 0.1, MUTED, track=0.1, t_out=E(3) + 0.1)
    film.add(Num(XB[2], num3, 1100, 210, W(3, "two hundred") - 0.1, dur=1.2, prefix="₹"))
    film.cue("impact", W(3, "two hundred") + 1.0, 0.4)
    text("ENQUIRY = A CHAT STARTED FROM THE AD. NOT A BOOKING.", XB[2], num3 + 330, 190, W(3, "new chat") - 0.1, MUTED, track=0.1, t_out=E(3) + 0.1)

    text("THE DIWALI SPIKE", MID, -6300, 1300, t_title, hit=0.5, shadow=True)
    text("WHAT 18 AD ACCOUNTS SHOWED", MID, -5790, 340, t_title + 0.45, GOLD, track=0.14)
    film.cue("boom", t_title, 0.5)

    # ------------------------------------------------------------------ the chart: four bars on one baseline
    film.add(Line(XB[0] - 1500, XB[3] + 1500, 0, L(4) - 0.1, dur=1.6, rgb=MUTED, width=8, alpha=0.6))
    text("COST OF ONE ENQUIRY · 18 ACCOUNTS BLENDED · ENQUIRY = A CHAT STARTED FROM THE AD", MID, 860, 190, L(4) + 0.8, MUTED, track=0.1)

    def bar(i, t_bar, t_num, name, dates, rgb, note=None, t_note=None, start=0, dur=1.0, note_y=330):
        num, nm = bar_top(i, 1100 if i == 2 else 900)
        film.add(Bar(XB[i], 0, BW, HB[i], t_bar, dur=dur, rgb=rgb))
        if t_num is not None:
            film.add(Num(XB[i], num, 900, VAL[i], t_num, dur=0.9, prefix="₹", start=start))
        text(name, XB[i], nm, 300, t_bar + 0.15, CREAM, track=0.12)
        text(dates, XB[i], 330, 200, t_bar + 0.3, MUTED, track=0.1)
        for k, ln in enumerate(note or ()):
            text(ln, XB[i], -HB[i] + note_y + 260 * k, 205, t_note + 0.12 * k, NAVY, max_w=BW - 220, track=0.06)

    bar(0, L(4) + 0.25, W(4, "one forty") - 0.15, "SEPTEMBER", "1–30 SEP", STEEL)
    bar(1, L(5) + 0.2, W(5, "one sixty") - 0.15, "OCTOBER", "1–31 OCT", BLUE, start=147)
    bar(2, L(13) + 0.25, None, "DIWALI WEEK", "1–8 NOV", GOLD, ("HIGHER IN 13 OF 17", "ACCOUNTS VS OCTOBER"), W(13, "peak") + 0.5, dur=1.4)
    bar(3, W(14, "fell") - 0.35, W(14, "one sixty") - 0.15, "9–11 NOV", "3 DAYS AFTER DIWALI", BLUE,
        ("LOWER IN 13 OF 16", "ACCOUNTS VS PEAK"), W(14, "thirteen") - 0.1, start=210, note_y=720)   # clear of the level lines
    film.cue("riser", L(13) - 1.1, 0.4, dur=1.2)
    film.cue("impact", L(13) + 1.5, 0.45)

    # line 15: about October's level, still above September, and only three days
    film.add(Line(XB[1] + BW / 2, XB[3] + BW / 2 + 250, -HB[1], W(15, "October") - 0.15, dur=1.0, rgb=CREAM, width=26, dash=(170, 120)))
    film.add(Line(XB[0] + BW / 2, XB[3] + BW / 2 + 250, -HB[0], W(15, "Still") - 0.1, dur=1.2, rgb=MUTED, width=26, dash=(170, 120)))
    film.add(Stamp("3 DAYS OF DATA", XB[3] - 100, -1250, size=400, rot=-7, t_in=W(15, "three days") + 0.05, rgb=CREAM))

    # ------------------------------------------------------------------ A  the accounts (under September)
    ax = XB[0]
    text("18 AD ACCOUNTS", ax, ROW + 1900, 420, W(6, "eighteen") - 0.1, CREAM, track=0.1)
    text("8 CLINICS · 3 SALONS · 2 ONLINE STORES · 5 OTHERS", ax, ROW + 2250, 190, W(6, "eighteen") + 0.45, MUTED, track=0.1)
    pts = [(ax - 1400 + 560 * col, ROW + 2800 + 560 * row) for row in range(3) for col in range(6)]
    film.add(Dots(pts, W(6, "eighteen"), W(7, "fifteen") - 0.1, n_mark=15, n_out=1))
    text("15 OF 17", ax, ROW + 4850, 620, W(7, "fifteen") + 0.5, GOLD, track=0.06, hit=0.35)
    text("COST PER ENQUIRY ROSE · SEP TO OCT", ax, ROW + 5150, 185, W(7, "fifteen") + 0.8, MUTED, track=0.1)
    text("1 HAD TOO FEW ENQUIRIES TO COMPARE", ax, ROW + 5420, 165, W(7, "fifteen") + 1.0, MUTED, track=0.1)

    # ------------------------------------------------------------------ B  the first guess, struck out (under October)
    bx = XB[1]
    film.add(Panel(bx, ROW + 2350, 4400, 1500, L(8) + 0.1))
    text("THE FIRST GUESS", bx, ROW + 2010, 210, L(8) + 0.3, MUTED, track=0.16)
    text("FESTIVE SEASON = COSTLIER ADS", bx, ROW + 2660, 420, W(8, "festive") - 0.1, CREAM, max_w=3800)
    film.add(PenMark("strike", bx, ROW + 2540, 4000, 120, t_in=W(9, "not") - 0.2, dur=0.45, width=44, rgb=BLUE, z=80))
    text("SHOWN 1,000 TIMES", bx - 1050, ROW + 3620, 240, W(10, "thousand") - 0.1, CREAM, track=0.12)
    film.add(Num(bx - 1050, ROW + 4420, 800, 5, W(10, "five") - 0.25, dur=0.8, prefix="−", suffix="%", rgb=BLUE))
    text("ONE CLICK", bx + 1050, ROW + 3620, 240, W(10, "So did") - 0.1, CREAM, track=0.12)
    film.add(Num(bx + 1050, ROW + 4420, 800, 5, W(10, "click") - 0.3, dur=0.8, prefix="−", suffix="%", rgb=BLUE))
    text("OCT VS SEP · MEDIAN OF 18 ACCOUNTS", bx, ROW + 4800, 180, W(10, "five") + 0.7, MUTED, track=0.1)

    # ------------------------------------------------------------------ C  saw, clicked, messaged (under Diwali week)
    cx = XB[2]
    rows = [("VIEWS", 2300, STEEL, W(11, "saw") - 0.15, None),
            ("CLICKS", 1450, BLUE, W(11, "clicked") - 0.15, None),
            ("MESSAGES PER CLICK", 820, GOLD, W(11, "clicked") + 0.55, (W(11, "smaller") + 0.1, 640, 0.7))]
    for k, (name, length, rgb, t0, rs) in enumerate(rows):
        y = ROW + 2080 + 600 * k
        text(name, cx - 1320, y + 75, 215, t0, CREAM, max_w=1750, track=0.1)
        film.add(Bar(cx - 300, y, length, 330, t0 + 0.1, dur=0.6, rgb=rgb, grow="right", resize=rs))
    film.add(Panel(cx, ROW + 4560, 4300, 1120, L(12) + 0.1, accent=GOLD))
    text("OUR READING", cx, ROW + 4370, 220, L(12) + 0.3, GOLD, track=0.16)
    text("NOT A MEASURED CAUSE", cx, ROW + 4820, 320, W(12, "busy") - 0.1, CREAM, track=0.08)

    # ------------------------------------------------------------------ D  two numbers, one moved up (under the last bar)
    dx = XB[3]
    text("PRICE TO SHOW THE AD", dx - 1100, ROW + 2250, 260, W(16, "price") - 0.2, CREAM, max_w=1950, track=0.1)
    film.add(Num(dx - 1100, ROW + 3250, 900, 5, W(16, "price") - 0.1, dur=0.7, prefix="−", suffix="%", rgb=BLUE))
    text("COST PER ENQUIRY", dx + 1100, ROW + 2250, 260, W(16, "cost of") - 0.2, CREAM, max_w=1950, track=0.1)
    film.add(Num(dx + 1100, ROW + 3250, 900, 12, W(16, "cost of") - 0.1, dur=0.7, prefix="+", suffix="%", rgb=GOLD))
    film.add(PenMark("ellipse", dx + 1100, ROW + 2930, 2250, 1250, t_in=W(17, "enquiries") - 0.25, dur=0.6, width=30, rgb=CREAM, z=80))
    text("SEP TO OCT · −5% IS THE MEDIAN ACCOUNT · +12% IS ALL 18 BLENDED", dx, ROW + 4080, 175, W(16, "cost of") + 0.4, MUTED, max_w=4300, track=0.08)

    # ------------------------------------------------------------------ end slate (below the detail row)
    t_end, sy = E(17) + 0.3, ROW + 6900
    text("NUMBERS THAT DON'T LIE.", MID, sy, 300, t_end, GOLD, track=0.16)
    text("ADSWORM", MID, sy + 660, 760, t_end + 0.15, CREAM, track=0.1, shadow=True)
    text("SOURCE: 18 META AD ACCOUNTS, READ ON 12 NOV 2026 · NO CLIENT IS NAMED", MID, sy + 1060, 180, t_end + 0.3, MUTED, track=0.1)
    text("AN ENQUIRY IS A CHAT STARTED FROM AN AD. IT IS NOT A BOOKING.", MID, sy + 1330, 180, t_end + 0.4, MUTED, track=0.1)

    # ------------------------------------------------------------------ camera
    cam(0.0, XB[2], date_y - 1050, 0.92, rot=-0.5)                     # the dates, close
    cam(L(2) - 0.1, XB[2], date_y - 1020, 0.9)
    cam(E(2), XB[2], date_y - 1150, 0.74)
    cam(L(3) + 0.9, XB[2], name3 - 1150, 0.6, rot=0.2)
    cam(W(3, "two hundred") + 1.0, XB[2], name3 - 880, 0.68, rot=0.3)   # the number
    cam(E(3) + 0.25, XB[2], name3 - 860, 0.7)
    cam(t_title + 0.45, MID, -7560, 0.44, fy=-6250, radius=5000, strength=0.3)
    cam(L(4) - 0.15, MID, -7530, 0.43, fy=-6250, radius=5000, strength=0.3)

    cam(L(4) + 0.5, XB[0], -4300, 0.42, rot=-0.4)                      # September
    cam(E(4), XB[0] + 300, -4250, 0.44)
    cam(L(5) + 0.5, XB[0] + 2900, -4600, 0.42, rot=0.4, fx=XB[1])      # October, with September beside it
    cam(E(5) + 0.1, XB[0] + 3100, -4550, 0.43, fx=XB[1])
    cam(L(6) + 0.5, ax, ROW + 1300, 0.52, rot=-0.3)                    # the accounts
    cam(E(6), ax, ROW + 1400, 0.54)
    cam(L(7) + 0.45, ax, ROW + 2560, 0.56, rot=0.2)
    cam(E(7) + 0.4, ax + 150, ROW + 2590, 0.58)

    cam(L(8) + 0.5, bx, ROW + 1330, 0.72, rot=0.3)                     # the first guess
    cam(E(8), bx, ROW + 1360, 0.74)
    cam(W(9, "not") + 0.35, bx, ROW + 1420, 0.8, rot=-0.2)
    cam(E(9), bx, ROW + 1440, 0.81)
    cam(L(10) + 0.45, bx, ROW + 3200, 0.72, rot=0.2)
    cam(E(10) + 0.1, bx + 80, ROW + 3220, 0.74)
    cam(L(11) + 0.45, cx + 100, ROW + 1440, 0.7, rot=-0.3)             # saw, clicked, messaged
    cam(E(11), cx + 100, ROW + 1480, 0.72)
    cam(L(12) + 0.45, cx, ROW + 3760, 0.68, rot=0.2)
    cam(E(12) + 0.4, cx + 80, ROW + 3790, 0.7)

    cam(L(13) + 0.5, XB[2] + 300, name3 - 560, 0.5, rot=0.3)           # the peak
    cam(W(13, "peak") + 0.5, XB[2] + 700, name3 - 520, 0.45)
    cam(E(13) + 0.1, XB[2] + 900, name3 - 500, 0.44)
    cam(L(14) + 0.45, 13000, name3 - 520, 0.36, rot=-0.2, fx=XB[3], fy=-2600, radius=4200)   # peak and after, side by side
    cam(E(14), 13200, name3 - 480, 0.37, fx=XB[3], fy=-2600, radius=4200)
    cam(L(15) + 0.6, MID, -7900, 0.2, fy=-2600, radius=12000, strength=0.2)                   # the title and the whole chart
    cam(E(15) + 0.4, MID, -7860, 0.204, fy=-2600, radius=12000, strength=0.2)

    cam(L(16) + 0.5, dx, ROW + 1640, 0.74, rot=0.3)                    # two numbers
    cam(E(16) + 0.1, dx + 100, ROW + 1670, 0.76)
    cam(W(17, "enquiries") + 0.3, dx + 220, ROW + 1690, 0.78, fx=dx + 1100)
    cam(E(17) + 0.2, dx + 240, ROW + 1700, 0.79, fx=dx + 1100)
    cam(E(17) + 1.4, MID, -7800, 0.139, fy=0, radius=22000, strength=0.1)                     # the whole board
    cam(E(17) + 2.9, MID, -7780, 0.141, fy=0, radius=22000, strength=0.1)
    cam(E(17) + 4.3, MID, sy - 1050, 0.5, fy=sy + 500, radius=4400, strength=0.45)            # the end slate
    cam(film.duration, MID, sy - 1000, 0.52, fy=sy + 500, radius=4400, strength=0.45)
    return film
