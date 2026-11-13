import {spring} from 'remotion';
import {body, display} from '../lib/fonts';
import {ease, progress} from '../lib/motion';
import {Sfx} from './Sfx';
import {C, V3} from './theme';

// Board pieces added for the Andromeda / "ad is the targeting" reels. Times are frames since the cue (−1 = not yet).
const pop = (t: number) => (t < 0 ? 0 : spring({frame: t, fps: 30, config: {damping: 11, stiffness: 220, mass: 0.7}}));
const INK = '#0D1320';

const Box: React.FC<{children: React.ReactNode; bg?: string; color?: string; width?: number; size?: number; pad?: string}> = ({children, bg = '#fff', color = C.ink, width, size = 28, pad = '8px 16px'}) => (
  <div style={{width, padding: pad, borderRadius: 14, background: bg, color, border: V3.outline, boxShadow: `4px 4px 0 ${INK}`, fontFamily: body, fontWeight: 800, fontSize: size, textAlign: 'center', whiteSpace: 'nowrap'}}>{children}</div>
);

// Campaign structure, old way → new way. Old: one campaign, several ad sets (one audience each), the same grey
// ads under every set. New (from `switchT`): one wide audience, a row of ads that each look different.
const NEW_ADS: {bg: string; glyph: string; label: string}[] = [
  {bg: C.blue, glyph: '▶', label: 'video'},
  {bg: V3.pink, glyph: '🙂', label: 'chehra'},
  {bg: C.gold, glyph: '₹', label: 'offer'},
  {bg: C.green, glyph: '★', label: 'review'},
  {bg: C.red, glyph: '▦', label: 'carousel'},
];
export const OldNew: React.FC<{t: number; switchT: number; old: {title: string; sets: string[]; ads?: number}; next: {title: string; label: string}; setT?: number[]}> = ({t, switchT, old, next, setT}) => {
  const sw = switchT < 0 ? 0 : progress(switchT, 0, 10, ease.inOutQuart);
  const n = old.sets.length;
  const colW = Math.min(164, Math.floor((880 - (n - 1) * 12) / n));
  return (
    <div style={{position: 'relative', width: 880, height: 500, fontFamily: body, transform: 'scale(1.08)', transformOrigin: '50% 40%'}}>
      <Sfx name="whoosh" t={switchT} volume={0.5} />
      {/* old way */}
      <div style={{position: 'absolute', inset: 0, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 14, opacity: 1 - sw, transform: `translateX(${-sw * 120}px) scale(${1 - sw * 0.12})`}}>
        <div style={{padding: '6px 20px', borderRadius: 999, background: C.ink, color: '#fff', fontWeight: 800, fontSize: 26, letterSpacing: '0.08em', transform: `scale(${pop(t)})`}}>{old.title}</div>
        <Box bg={C.blueSoft} width={300}>1 Campaign</Box>
        <div style={{width: 5, height: 18, background: INK, marginTop: -14, marginBottom: -14}} />
        <div style={{width: (colW + 12) * (n - 1), height: 5, background: INK}} />
        <div style={{display: 'flex', gap: 12, marginTop: -14}}>
          {old.sets.map((s, i) => {
            const st = setT ? setT[i] : t; // un-cued: all sets are there on frame 0 (a finished hook board)
            const p = pop(st);
            return (
              <div key={i} style={{width: colW, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 8, opacity: st < 0 ? 0.001 : 1, transform: `scale(${0.6 + 0.4 * p})`}}>
                {setT ? <Sfx name="pop" t={st} /> : null}
                <div style={{width: 5, height: 16, background: INK}} />
                <Box bg={V3.pinkSoft} width={colW - 18} size={19} pad="8px 4px">{s}</Box>
                <div style={{display: 'flex', flexDirection: 'column', gap: 6}}>
                  {Array.from({length: old.ads ?? 3}).map((_, k) => (
                    <div key={k} style={{width: colW - 46, height: 36, borderRadius: 9, background: '#C9CDD6', border: `2.5px solid ${INK}`, display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 800, fontSize: 18, color: '#5B6170'}}>same ad</div>
                  ))}
                </div>
              </div>
            );
          })}
        </div>
      </div>
      {/* new way */}
      {switchT >= 0 ? (
        <div style={{position: 'absolute', inset: 0, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 14, opacity: sw, transform: `translateX(${(1 - sw) * 120}px)`}}>
          <div style={{padding: '6px 20px', borderRadius: 999, background: C.green, color: '#fff', fontWeight: 800, fontSize: 26, letterSpacing: '0.08em', border: V3.outline}}>{next.title}</div>
          <Box bg={C.blueSoft} width={300}>1 Campaign</Box>
          <div style={{width: 5, height: 18, background: INK, marginTop: -14, marginBottom: -14}} />
          <Box bg={C.greenSoft} width={560}>{next.label}</Box>
          <div style={{width: 5, height: 18, background: INK, marginTop: -14, marginBottom: -14}} />
          <div style={{display: 'flex', gap: 16}}>
            {NEW_ADS.map((a, i) => {
              const p = pop(switchT - 8 - i * 4);
              return (
                <div key={i} style={{width: 146, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 6, transform: `scale(${p}) rotate(${(i - 2) * 2}deg)`}}>
                  <Sfx name="pop" t={switchT} delay={8 + i * 4} />
                  <div style={{width: 146, height: 150, borderRadius: 18, background: a.bg, border: V3.outline, boxShadow: `5px 5px 0 ${INK}`, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 70, color: '#fff', fontFamily: display}}>{a.glyph}</div>
                  <div style={{fontWeight: 800, fontSize: 24, color: C.ink}}>{a.label}</div>
                </div>
              );
            })}
          </div>
        </div>
      ) : null}
    </div>
  );
};

// A receipt you can watch: a page from the source, then a find-in-page bar types the query and shows the count.
export const Find: React.FC<{t: number; url: string; source: string; title: string; query: string; typeT: number; result: string; resultT: number; stamp?: string; stampT?: number}> = ({t, url, source, title, query, typeT, result, resultT, stamp, stampT = -1}) => {
  const p = pop(t);
  const typed = typeT < 0 ? '' : query.slice(0, Math.max(1, Math.ceil(progress(typeT, 0, 10) * query.length)));
  const r = pop(resultT);
  const s = pop(stampT);
  return (
    <div style={{position: 'relative', width: 860, borderRadius: 24, background: '#fff', border: V3.outline, boxShadow: V3.shadow, overflow: 'visible', fontFamily: body, transform: `scale(${0.8 + 0.2 * p})`, opacity: Math.min(1, p * 2)}}>
      <Sfx name="pop" t={t} />
      <div style={{height: 54, borderBottom: `2.5px solid ${INK}`, display: 'flex', alignItems: 'center', gap: 10, padding: '0 20px', background: '#F4F5F8', borderRadius: '21px 21px 0 0', fontWeight: 700, fontSize: 22, color: C.muted}}>
        <span>🔒</span>
        {url}
      </div>
      <div style={{padding: '22px 30px 26px'}}>
        <div style={{fontWeight: 800, fontSize: 26, letterSpacing: '0.06em', color: C.blue}}>{source}</div>
        <div style={{marginTop: 10, fontWeight: 800, fontSize: 58, lineHeight: 1.1, color: C.ink, letterSpacing: '-0.01em'}}>{title}</div>
        <div style={{marginTop: 22, display: 'flex', alignItems: 'center', gap: 14, opacity: typeT < 0 ? 0.35 : 1}}>
          <div style={{flex: 1, height: 96, borderRadius: 18, border: V3.outline, background: '#FFFBEA', display: 'flex', alignItems: 'center', gap: 14, padding: '0 22px', fontWeight: 800, fontSize: 54, color: C.ink}}>
            <Sfx name="tick" t={typeT} />
            <Sfx name="tick" t={typeT} delay={4} />
            <Sfx name="tick" t={typeT} delay={8} />
            <span style={{fontSize: 30}}>🔍</span>
            <span style={{fontWeight: 700, fontSize: 28, color: C.muted}}>Find in page:</span>
            <span>{typed}</span>
            {typeT >= 0 && typeT % 16 < 8 ? <span style={{width: 5, height: 54, background: C.ink}} /> : null}
          </div>
          <div style={{minWidth: 290, height: 96, borderRadius: 18, border: V3.outline, background: resultT >= 0 ? C.red : '#EDEEF2', color: '#fff', display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: display, fontSize: 60, transform: `scale(${resultT >= 0 ? 0.7 + 0.3 * r : 1})`}}>
            <Sfx name="buzz" t={resultT} />
            {resultT >= 0 ? result : ''}
          </div>
        </div>
      </div>
      {stamp && stampT >= 0 ? (
        <div style={{position: 'absolute', right: -14, top: 62, padding: '10px 22px', borderRadius: 16, background: C.gold, color: C.ink, border: V3.outline, boxShadow: `5px 5px 0 ${INK}`, fontWeight: 800, fontSize: 40, transform: `rotate(7deg) scale(${s})`}}>
          <Sfx name="thump" t={stampT} volume={0.4} />
          {stamp}
        </div>
      ) : null}
    </div>
  );
};

// Two lists side by side: what is true and what is only a rumour. The closing card people save.
export const Truths: React.FC<{t: number; left: {title: string; lines: string[]}; right: {title: string; lines: string[]}; rightT: number}> = ({t, left, right, rightT}) => {
  const col = (side: {title: string; lines: string[]}, ok: boolean, ct: number) => (
    <div style={{flex: 1, padding: '20px 20px 24px', borderRadius: 22, background: ok ? C.greenSoft : V3.pinkSoft, border: V3.outline, boxShadow: `5px 5px 0 ${INK}`, opacity: ct < 0 ? 0 : 1, transform: `scale(${0.8 + 0.2 * pop(ct)})`}}>
      <Sfx name={ok ? 'ding' : 'buzz'} t={ct} />
      <div style={{fontFamily: display, fontSize: 64, lineHeight: 1, color: ok ? C.green : C.red, WebkitTextStroke: `1.5px ${INK}`, textAlign: 'center'}}>{side.title}</div>
      <div style={{marginTop: 16, display: 'flex', flexDirection: 'column', gap: 16}}>
        {side.lines.map((l, i) => (
          <div key={i} style={{display: 'flex', alignItems: 'flex-start', gap: 12, fontWeight: 800, fontSize: 34, lineHeight: 1.15, color: C.ink, opacity: progress(ct, 6 + i * 6, 8)}}>
            <span style={{flex: 'none', width: 40, height: 40, borderRadius: '50%', background: ok ? C.green : C.red, color: '#fff', fontSize: 26, display: 'flex', alignItems: 'center', justifyContent: 'center', marginTop: -1}}>{ok ? '✓' : '✕'}</span>
            {l}
          </div>
        ))}
      </div>
    </div>
  );
  return (
    <div style={{width: 880, display: 'flex', gap: 16, fontFamily: body}}>
      {col(left, true, t)}
      {col(right, false, rightT)}
    </div>
  );
};
