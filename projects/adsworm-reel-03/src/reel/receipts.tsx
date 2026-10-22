import {interpolate} from 'remotion';
import {body, display} from '../lib/fonts';
import {ease, progress} from '../lib/motion';
import {C} from './theme';

// Receipt primitives. Each takes `t` = frames since its beat (−1 = not yet) and reveals itself.

export const Big: React.FC<{t: number; value: string; sub?: string; color?: string; size?: number}> = ({t, value, sub, color = C.blue, size = 210}) => {
  if (t < 0) return null;
  const p = progress(t, 0, 14, ease.outExpo);
  return (
    <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center', opacity: p, transform: `scale(${0.8 + p * 0.2})`}}>
      <div style={{fontFamily: display, fontSize: size, lineHeight: 0.9, color}}>{value}</div>
      {sub ? <div style={{fontFamily: body, fontWeight: 600, fontSize: 32, color: C.muted, marginTop: 8}}>{sub}</div> : null}
    </div>
  );
};

export const Browser: React.FC<{t: number; url: string; title: string; date?: string; children?: React.ReactNode}> = ({t, url, title, date, children}) => {
  if (t < 0) return null;
  const p = progress(t, 0, 16, ease.outExpo);
  const p2 = progress(t, 10, 16, ease.outExpo);
  return (
    <div style={{borderRadius: 24, overflow: 'hidden', border: `2px solid ${C.line}`, background: '#fff', opacity: p, transform: `translateY(${(1 - p) * 30}px)`, fontFamily: body}}>
      <div style={{display: 'flex', alignItems: 'center', gap: 14, padding: '16px 20px', background: '#F6F6F4', borderBottom: `2px solid ${C.line}`}}>
        {['#FF5F57', '#FEBC2E', '#28C840'].map((c) => (
          <span key={c} style={{width: 14, height: 14, borderRadius: '50%', background: c, display: 'inline-block'}} />
        ))}
        <div style={{flex: 1, marginLeft: 10, height: 36, borderRadius: 10, background: '#fff', border: `1.5px solid ${C.line}`, fontSize: 20, color: C.muted, display: 'flex', alignItems: 'center', padding: '0 14px', gap: 8}}>
          <span style={{color: C.green}}>🔒</span>
          {url}
        </div>
      </div>
      <div style={{padding: '24px 30px 22px'}}>
        <div style={{fontFamily: body, fontWeight: 800, fontSize: 36, lineHeight: 1.15, color: C.ink, letterSpacing: '-0.02em'}}>{title}</div>
        {date ? (
          <div style={{display: 'inline-flex', alignItems: 'center', gap: 10, marginTop: 18, padding: '8px 16px', borderRadius: 999, background: C.blueSoft, color: C.blue, fontSize: 24, fontWeight: 700, opacity: p2, transform: `translateY(${(1 - p2) * 10}px)`}}>
            <span style={{width: 10, height: 10, borderRadius: '50%', background: C.blue, display: 'inline-block'}} />
            {date}
          </div>
        ) : null}
        {children}
      </div>
    </div>
  );
};

export const Phone: React.FC<{t: number; label?: string; adTitle?: string; cta?: string; children?: React.ReactNode; width?: number}> = ({t, label, adTitle, cta = 'Learn more', children, width = 300}) => {
  if (t < 0) return null;
  const p = progress(t, 0, 16, ease.outExpo);
  const h = width * 2.05;
  return (
    <div style={{position: 'relative', width, height: h, borderRadius: width * 0.14, background: '#0D1320', padding: 10, opacity: p, transform: `translateY(${(1 - p) * 40}px)`, boxShadow: '0 30px 60px rgba(13,19,32,0.18)', fontFamily: body}}>
      <div style={{position: 'absolute', left: '50%', top: 8, width: width * 0.3, height: 14, borderRadius: 8, background: '#000', transform: 'translateX(-50%)'}} />
      <div style={{width: '100%', height: '100%', borderRadius: width * 0.11, background: '#fff', overflow: 'hidden', position: 'relative'}}>
        <div style={{height: 54, display: 'flex', alignItems: 'center', padding: '0 18px', gap: 10, borderBottom: `1.5px solid ${C.line}`}}>
          <span style={{width: 26, height: 26, borderRadius: '50%', background: C.blue, display: 'inline-block'}} />
          <span style={{width: 80, height: 10, borderRadius: 5, background: '#E6E6E2', display: 'inline-block'}} />
        </div>
        {children ?? (
          <div style={{padding: 14}}>
            <div style={{height: 10, width: '70%', borderRadius: 5, background: '#ECECEA', marginBottom: 12}} />
            <div style={{height: width * 0.95, borderRadius: 16, background: 'linear-gradient(160deg, #FF9A5A, #D63AC1 55%, #4F46E5)', position: 'relative'}}>
              {label ? <div style={{position: 'absolute', left: 12, top: 12, padding: '6px 10px', borderRadius: 8, background: 'rgba(255,255,255,0.92)', fontSize: 15, fontWeight: 800, color: C.ink}}>{label}</div> : null}
            </div>
            <div style={{marginTop: 12, fontWeight: 800, fontSize: 18, color: C.ink}}>{adTitle ?? 'Your brand · Sponsored'}</div>
            <div style={{marginTop: 10, height: 40, borderRadius: 10, background: C.blue, color: '#fff', fontWeight: 700, fontSize: 16, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>{cta}</div>
          </div>
        )}
      </div>
    </div>
  );
};

export const Chip: React.FC<{t: number; delay?: number; kind?: 'blue' | 'green' | 'gold' | 'ink'; children: React.ReactNode}> = ({t, delay = 0, kind = 'blue', children}) => {
  if (t < delay) return null;
  const p = progress(t, delay, 12, ease.outExpo);
  const bg = {blue: C.blue, green: C.green, gold: C.gold, ink: C.ink}[kind];
  return (
    <div style={{display: 'inline-flex', alignItems: 'center', gap: 10, padding: '12px 20px', borderRadius: 999, background: bg, color: '#fff', fontFamily: body, fontWeight: 700, fontSize: 28, whiteSpace: 'nowrap', opacity: p, transform: `scale(${0.8 + p * 0.2}) translateX(${(1 - p) * -14}px)`, transformOrigin: 'left center'}}>
      {children}
    </div>
  );
};

export const Ring: React.FC<{t: number; value: string; sub: string; size?: number}> = ({t, value, sub, size = 300}) => {
  if (t < 0) return null;
  const p = progress(t, 0, 36, ease.outQuart);
  const r = size / 2 - 16;
  const circ = 2 * Math.PI * r;
  return (
    <div style={{position: 'relative', width: size, height: size, fontFamily: body}}>
      <svg width={size} height={size} style={{transform: 'rotate(-90deg)'}}>
        <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke={C.blueSoft} strokeWidth={22} />
        <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke={C.blue} strokeWidth={22} strokeLinecap="round" strokeDasharray={circ} strokeDashoffset={circ * (1 - p)} />
      </svg>
      <div style={{position: 'absolute', inset: 0, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center'}}>
        <div style={{fontFamily: display, fontSize: size * 0.3, lineHeight: 1, color: C.ink}}>{value}</div>
        <div style={{fontSize: size * 0.075, color: C.muted, fontWeight: 600}}>{sub}</div>
      </div>
    </div>
  );
};

// Line chart that draws itself; `points` are 0–1 normalised (x, y).
export const Chart: React.FC<{t: number; points: [number, number][]; w?: number; h?: number; title?: string; note?: string}> = ({t, points, w = 860, h = 300, title, note}) => {
  if (t < 0) return null;
  const p = progress(t, 0, 40, ease.inOutQuart);
  const n2 = progress(t, 30, 14, ease.outExpo);
  const px = (x: number) => 30 + x * (w - 60);
  const py = (y: number) => h - 30 - y * (h - 70);
  const d = points.map(([x, y], i) => `${i ? 'L' : 'M'} ${px(x)} ${py(y)}`).join(' ');
  const len = 2000;
  return (
    <div style={{fontFamily: body}}>
      {title ? <div style={{fontWeight: 800, fontSize: 30, color: C.ink, marginBottom: 6}}>{title}</div> : null}
      <svg width={w} height={h}>
        <line x1={30} y1={py(0)} x2={w - 30} y2={py(0)} stroke={C.line} strokeWidth={2} />
        <path d={d} fill="none" stroke={C.red} strokeWidth={6} strokeLinecap="round" strokeDasharray={len} strokeDashoffset={len * (1 - p)} />
        {p >= 1 ? <circle cx={px(points[points.length - 1][0])} cy={py(points[points.length - 1][1])} r={10} fill={C.red} /> : null}
      </svg>
      {note ? <div style={{display: 'inline-block', padding: '8px 16px', borderRadius: 999, background: C.greenSoft, color: C.green, fontWeight: 700, fontSize: 24, opacity: n2}}>{note}</div> : null}
    </div>
  );
};

export const Bars: React.FC<{t: number; items: {label: string; value: number; color?: string}[]; max?: number; w?: number}> = ({t, items, max, w = 860}) => {
  if (t < 0) return null;
  const m = max ?? Math.max(...items.map((i) => i.value));
  return (
    <div style={{display: 'flex', flexDirection: 'column', gap: 18, width: w, fontFamily: body}}>
      {items.map((it, i) => {
        const p = progress(t, i * 8, 24, ease.outExpo);
        return (
          <div key={it.label} style={{opacity: Math.min(1, p * 2)}}>
            <div style={{display: 'flex', justifyContent: 'space-between', fontSize: 30, fontWeight: 700, color: C.ink, marginBottom: 8}}>
              <span>{it.label}</span>
              <span style={{color: it.color ?? C.blue}}>+{(it.value * p).toFixed(it.value % 1 ? 1 : 0)}%</span>
            </div>
            <div style={{height: 26, borderRadius: 13, background: '#EFEFEC'}}>
              <div style={{height: '100%', width: `${(it.value / m) * 100 * p}%`, borderRadius: 13, background: it.color ?? C.blue}} />
            </div>
          </div>
        );
      })}
    </div>
  );
};

// Instagram-style comment composer typing a keyword (light theme).
export const CommentUI: React.FC<{t: number; name: string; handle: string; keyword: string; typeFrom?: number; every?: number}> = ({t, name, handle, keyword, typeFrom = 14, every = 4}) => {
  if (t < 0) return null;
  const p = progress(t, 0, 14, ease.outExpo);
  const shown = Math.max(0, Math.min(keyword.length, Math.floor((t - typeFrom) / every) + 1));
  const typed = t >= typeFrom ? keyword.slice(0, shown) : '';
  const sent = shown >= keyword.length && t > typeFrom + every * keyword.length + 6;
  return (
    <div style={{fontFamily: body, opacity: p, transform: `translateY(${(1 - p) * 20}px)`}}>
      <div style={{display: 'flex', alignItems: 'center', gap: 16, padding: '0 6px 22px', borderBottom: `2px solid ${C.line}`}}>
        <div style={{width: 72, height: 72, borderRadius: '50%', background: `linear-gradient(135deg, ${C.blue}, ${C.ink})`}} />
        <div style={{flex: 1}}>
          <div style={{fontWeight: 800, fontSize: 28, color: C.ink}}>{name}</div>
          <div style={{fontSize: 22, color: C.muted}}>{handle}</div>
        </div>
        <div style={{padding: '10px 20px', borderRadius: 12, background: C.green, color: '#fff', fontWeight: 700, fontSize: 22}}>Following ✓</div>
      </div>
      <div style={{marginTop: 22, display: 'flex', alignItems: 'center', gap: 18, height: 88, borderRadius: 999, border: `2px solid ${C.line}`, padding: '0 22px', background: '#fff'}}>
        <div style={{width: 48, height: 48, borderRadius: '50%', background: '#E6E6E2'}} />
        <div style={{flex: 1, fontSize: 34, fontWeight: 700, color: typed ? C.ink : C.muted}}>
          {typed || 'Add a comment…'}
          {typed && !sent ? <span style={{display: 'inline-block', width: 3, height: 34, marginLeft: 4, verticalAlign: 'middle', background: C.blue}} /> : null}
        </div>
        <div style={{fontSize: 26, fontWeight: 800, color: sent ? C.blue : C.muted}}>Post</div>
      </div>
    </div>
  );
};

export const Row: React.FC<{gap?: number; align?: string; children: React.ReactNode; style?: React.CSSProperties}> = ({gap = 28, align = 'center', children, style}) => (
  <div style={{display: 'flex', gap, alignItems: align as React.CSSProperties['alignItems'], ...style}}>{children}</div>
);

export const Col: React.FC<{gap?: number; children: React.ReactNode; style?: React.CSSProperties}> = ({gap = 18, children, style}) => (
  <div style={{display: 'flex', flexDirection: 'column', gap, ...style}}>{children}</div>
);

export const Note: React.FC<{t: number; delay?: number; children: React.ReactNode; size?: number}> = ({t, delay = 0, children, size = 34}) => {
  if (t < delay) return null;
  const p = progress(t, delay, 12, ease.outExpo);
  return <div style={{fontFamily: body, fontWeight: 800, fontSize: size, lineHeight: 1.2, color: C.ink, opacity: p, transform: `translateY(${(1 - p) * 12}px)`}}>{children}</div>;
};

export const fadeOut = (t: number, at: number, dur = 10) => (t < 0 ? 1 : 1 - interpolate(t, [at, at + dur], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}));

// WhatsApp-style thread: an ad card, a customer reply, and a status pill.
export const Chat: React.FC<{t: number; brand: string; adLine: string; reply: string; pill: string; w?: number}> = ({t, brand, adLine, reply, pill, w = 560}) => {
  if (t < 0) return null;
  const p1 = progress(t, 0, 14, ease.outExpo);
  const p2 = progress(t, 12, 14, ease.outExpo);
  const p3 = progress(t, 26, 14, ease.outExpo);
  return (
    <div style={{width: w, borderRadius: 28, background: '#E7E0D4', padding: 22, fontFamily: body, display: 'flex', flexDirection: 'column', gap: 14}}>
      <div style={{alignSelf: 'flex-start', maxWidth: '82%', background: '#fff', borderRadius: '4px 18px 18px 18px', padding: '14px 18px', opacity: p1, transform: `translateY(${(1 - p1) * 14}px)`}}>
        <div style={{height: 110, borderRadius: 12, background: 'linear-gradient(160deg, #FF9A5A, #D63AC1 55%, #4F46E5)', marginBottom: 10}} />
        <div style={{fontWeight: 800, fontSize: 27, color: C.ink}}>{brand}</div>
        <div style={{fontSize: 24, color: C.muted}}>{adLine}</div>
      </div>
      <div style={{alignSelf: 'flex-end', maxWidth: '82%', background: '#D9FDD3', borderRadius: '18px 4px 18px 18px', padding: '14px 18px', fontSize: 29, color: C.ink, fontWeight: 600, opacity: p2, transform: `translateY(${(1 - p2) * 14}px)`}}>
        {reply}
      </div>
      <div style={{alignSelf: 'center', padding: '10px 20px', borderRadius: 999, background: C.green, color: '#fff', fontWeight: 800, fontSize: 26, opacity: p3, transform: `scale(${0.85 + p3 * 0.15})`}}>{pill}</div>
    </div>
  );
};

// A static product image turning into a video player (arrow + play button).
export const ImageToVideo: React.FC<{t: number}> = ({t}) => {
  if (t < 0) return null;
  const p = progress(t, 0, 14, ease.outExpo);
  const p2 = progress(t, 14, 18, ease.outExpo);
  const tile = (video: boolean, prog: number) => (
    <div style={{position: 'relative', width: 250, height: 310, borderRadius: 22, overflow: 'hidden', background: 'linear-gradient(160deg, #FFD27A, #FF8A5B 55%, #C2410C)', opacity: prog, transform: `scale(${0.9 + prog * 0.1})`, boxShadow: '0 18px 40px rgba(13,19,32,0.15)'}}>
      <div style={{position: 'absolute', left: 18, top: 18, padding: '6px 12px', borderRadius: 8, background: 'rgba(255,255,255,0.9)', fontFamily: body, fontWeight: 800, fontSize: 18, color: C.ink}}>{video ? 'VIDEO · 0:06' : 'STATIC'}</div>
      <div style={{position: 'absolute', left: 30, right: 30, bottom: 70, height: 90, borderRadius: 16, background: 'rgba(255,255,255,0.55)'}} />
      {video ? (
        <>
          <div style={{position: 'absolute', left: '50%', top: '50%', width: 86, height: 86, borderRadius: '50%', background: 'rgba(13,19,32,0.75)', transform: 'translate(-50%,-50%)'}} />
          <div style={{position: 'absolute', left: 'calc(50% - 12px)', top: 'calc(50% - 20px)', width: 0, height: 0, borderTop: '20px solid transparent', borderBottom: '20px solid transparent', borderLeft: '34px solid #fff'}} />
          <div style={{position: 'absolute', left: 18, right: 18, bottom: 18, height: 6, borderRadius: 3, background: 'rgba(255,255,255,0.5)'}}>
            <div style={{width: `${30 + 50 * Math.min(1, Math.max(0, (t - 32) / 60))}%`, height: '100%', borderRadius: 3, background: '#fff'}} />
          </div>
        </>
      ) : null}
    </div>
  );
  return (
    <div style={{display: 'flex', alignItems: 'center', gap: 26}}>
      {tile(false, p)}
      <div style={{fontFamily: display, fontSize: 90, color: C.blue, opacity: p2, transform: `translateX(${(1 - p2) * -20}px)`}}>→</div>
      {tile(true, p2)}
    </div>
  );
};

// A "free PDF" tile: document mock with a blue header strip and a few text lines.
export const PdfCard: React.FC<{t: number; title: string; sub: string; lines?: number}> = ({t, title, sub, lines = 4}) => {
  if (t < 0) return null;
  const p = progress(t, 0, 16, ease.outExpo);
  return (
    <div style={{display: 'flex', alignItems: 'center', gap: 28, opacity: p, transform: `translateY(${(1 - p) * 20}px)`, fontFamily: body}}>
      <div style={{width: 160, height: 200, borderRadius: 16, background: '#fff', border: `2px solid ${C.line}`, boxShadow: '0 16px 36px rgba(13,19,32,0.12)', overflow: 'hidden', position: 'relative', transform: 'rotate(-4deg)'}}>
        <div style={{height: 54, background: C.blue, color: '#fff', fontWeight: 800, fontSize: 15, letterSpacing: '0.1em', display: 'flex', alignItems: 'center', padding: '0 14px'}}>META × DIWALI</div>
        <div style={{padding: 14, display: 'flex', flexDirection: 'column', gap: 10}}>
          {Array.from({length: lines}, (_, i) => (
            <div key={i} style={{display: 'flex', gap: 8, alignItems: 'center'}}>
              <div style={{width: 14, height: 14, borderRadius: 4, border: `2px solid ${C.blue}`, background: i === 0 ? C.blue : 'transparent'}} />
              <div style={{flex: 1, height: 10, borderRadius: 5, background: '#E6E6E2', width: `${70 + ((i * 37) % 30)}%`}} />
            </div>
          ))}
        </div>
        <div style={{position: 'absolute', right: 12, bottom: 12, padding: '4px 10px', borderRadius: 6, background: C.gold, color: C.ink, fontWeight: 800, fontSize: 14}}>PDF</div>
      </div>
      <div>
        <div style={{fontWeight: 800, fontSize: 34, color: C.ink, lineHeight: 1.15}}>{title}</div>
        <div style={{fontWeight: 600, fontSize: 24, color: C.muted, marginTop: 8}}>{sub}</div>
      </div>
    </div>
  );
};
