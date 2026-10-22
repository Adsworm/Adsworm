import {interpolate, spring} from 'remotion';
import {body, display} from '../lib/fonts';
import {ease, progress} from '../lib/motion';
import {C, V3} from './theme';

// v3 board pieces. `t` = frames since the piece appeared; extra *At values are frames since a later
// word/beat (−1 before it). Everything springs in with a little overshoot and lands on the voice.
const pop = (t: number, fps = 30) => (t < 0 ? 0 : spring({frame: t, fps, config: {damping: 11, stiffness: 220, mass: 0.7}}));
const tone = {red: C.red, green: C.green, blue: C.blue, gold: C.gold, pink: V3.pink, ink: C.ink} as const;
export type Tone = keyof typeof tone;

// Tilted stamp sticker — the reel's punctuation.
export const Sticker: React.FC<{t: number; text: string; color?: Tone; x: number; y: number; rotate?: number}> = ({t, text, color = 'gold', x, y, rotate = 5}) => {
  if (t < 0) return null;
  const p = pop(t);
  return (
    <div style={{position: 'absolute', left: x, top: y, zIndex: 5, padding: '14px 22px', borderRadius: 18, background: tone[color], color: color === 'gold' ? C.ink : '#fff', border: V3.outline, boxShadow: '5px 5px 0 #0D1320', fontFamily: body, fontWeight: 800, fontSize: 34, whiteSpace: 'nowrap', transform: `rotate(${rotate}deg) scale(${p})`, transformOrigin: 'center'}}>
      {text}
    </div>
  );
};

// Count-up number that lands with a small shake.
const Count: React.FC<{t: number; value: number; prefix?: string; suffix?: string; color: string; size: number}> = ({t, value, prefix = '', suffix = '', color, size}) => {
  const p = progress(t, 0, 22, ease.outQuart);
  const after = t - 22;
  const shake = after > 0 && after < 10 ? Math.sin(after * 2.6) * (10 - after) * 0.9 : 0;
  return (
    <div style={{fontFamily: display, fontSize: size, lineHeight: 0.85, color, transform: `translateX(${shake}px)`, WebkitTextStroke: '3px #0D1320', textShadow: '6px 6px 0 #0D1320'}}>
      {prefix}
      {Math.round(value * p)}
      {suffix}
    </div>
  );
};

export const Stat: React.FC<{t: number; value: number; prefix?: string; suffix?: string; label: string; color?: Tone; arrow?: 'up' | 'down'}> = ({t, value, prefix, suffix, label, color = 'red', arrow}) => {
  const p = pop(t);
  return (
    <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center', transform: `scale(${0.6 + 0.4 * p})`, opacity: Math.min(1, p * 2)}}>
      <div style={{display: 'flex', alignItems: 'center', gap: 18}}>
        <Count t={t} value={value} prefix={prefix} suffix={suffix} color={tone[color]} size={250} />
        {arrow ? <div style={{fontSize: 150, color: tone[color], transform: `translateY(${(1 - progress(t, 6, 14)) * (arrow === 'up' ? 60 : -60)}px)`, opacity: progress(t, 6, 10)}}>{arrow === 'up' ? '▲' : '▼'}</div> : null}
      </div>
      <div style={{fontFamily: body, fontWeight: 800, fontSize: 34, color: C.ink, textAlign: 'center', marginTop: 10, opacity: progress(t, 8, 10)}}>{label}</div>
    </div>
  );
};

export const Versus: React.FC<{t: number; qT: number; left: {value: number; prefix?: string; suffix?: string; label: string; color?: Tone; arrow?: 'up' | 'down'}; right: {value: number; prefix?: string; suffix?: string; label: string; color?: Tone; arrow?: 'up' | 'down'}}> = ({t, qT, left, right}) => {
  const col = (s: typeof left, tt: number) => {
    const p = pop(tt);
    return (
      <div style={{flex: 1, borderRadius: 28, border: V3.outline, boxShadow: V3.shadow, background: s.color === 'green' ? C.greenSoft : '#FDECEC', padding: '26px 10px 22px', display: 'flex', flexDirection: 'column', alignItems: 'center', transform: `scale(${0.7 + 0.3 * p})`, opacity: Math.min(1, p * 2)}}>
        <div style={{display: 'flex', alignItems: 'center', gap: 8}}>
          <Count t={tt} value={s.value} prefix={s.prefix} suffix={s.suffix} color={tone[s.color ?? 'red']} size={150} />
          <div style={{fontSize: 80, color: tone[s.color ?? 'red']}}>{s.arrow === 'up' ? '▲' : '▼'}</div>
        </div>
        <div style={{fontFamily: body, fontWeight: 800, fontSize: 34, color: C.ink, marginTop: 6}}>{s.label}</div>
      </div>
    );
  };
  const q = pop(qT);
  return (
    <div style={{position: 'relative', width: 880, display: 'flex', gap: 34, alignItems: 'stretch'}}>
      {col(left, t)}
      {col(right, t - 10)}
      <div style={{position: 'absolute', left: '50%', top: '50%', width: 110, height: 110, marginLeft: -55, marginTop: -55, borderRadius: '50%', background: C.gold, border: V3.outline, boxShadow: '5px 5px 0 #0D1320', fontFamily: display, fontSize: 90, lineHeight: '118px', textAlign: 'center', color: C.ink, transform: `scale(${q}) rotate(${(1 - q) * -90 + Math.sin(qT / 5) * 6}deg)`}}>?</div>
    </div>
  );
};

// Opening visual: AD PRICES + a chart that shoots up; on the "happy" word a smiley lands on the peak.
export const HookPrice: React.FC<{t: number; smileT: number}> = ({t, smileT}) => {
  const d = 'M 30 330 C 180 320, 300 300, 400 250 S 560 120, 640 40';
  const draw = progress(t, 2, 20, ease.inOutQuart);
  const s = pop(smileT);
  return (
    <div style={{position: 'relative', width: 880, height: 560}}>
      <div style={{position: 'absolute', left: 0, top: 0, fontFamily: display, fontSize: 150, lineHeight: 0.9, color: C.ink, transform: `scale(${pop(t)})`, transformOrigin: '0 0'}}>
        AD PRICES
        <div style={{fontSize: 110, color: C.red, WebkitTextStroke: '3px #0D1320'}}>SHOOT UP ▲</div>
      </div>
      <svg width={700} height={380} style={{position: 'absolute', right: -10, bottom: 10, overflow: 'visible'}}>
        <path d="M 30 340 L 680 340" stroke="#0D1320" strokeWidth={4} />
        <path d={d} fill="none" stroke="#0D1320" strokeWidth={22} strokeLinecap="round" strokeDasharray={1000} strokeDashoffset={1000 * (1 - draw)} />
        <path d={d} fill="none" stroke={C.red} strokeWidth={14} strokeLinecap="round" strokeDasharray={1000} strokeDashoffset={1000 * (1 - draw)} />
      </svg>
      <div style={{position: 'absolute', right: 0, top: 150, width: 140, height: 140, borderRadius: '50%', background: C.gold, border: V3.outline, boxShadow: '5px 5px 0 #0D1320', fontSize: 96, lineHeight: '138px', textAlign: 'center', transform: `scale(${s}) rotate(${(1 - s) * 120}deg)`}}>😄</div>
    </div>
  );
};

// "PAUSE ALL ADS" button with a cursor drifting in; at `strikeT` it's crossed out.
export const PauseButton: React.FC<{t: number; strikeT: number; text: string}> = ({t, strikeT, text}) => {
  const p = pop(t);
  const cur = progress(t, 4, 26, ease.inOutQuart);
  const press = t > 30 && t < 36 ? 0.94 : 1;
  const x = pop(strikeT);
  return (
    <div style={{position: 'relative', width: 760, height: 420, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
      <div style={{padding: '44px 70px', borderRadius: 999, background: strikeT >= 0 ? '#C9CDD6' : C.red, color: '#fff', fontFamily: display, fontSize: 110, letterSpacing: '0.02em', border: V3.outline, boxShadow: V3.shadow, transform: `scale(${(0.6 + 0.4 * p) * press})`, whiteSpace: 'nowrap'}}>⏸ {text}</div>
      <svg width={70} height={84} viewBox="0 0 24 30" style={{position: 'absolute', left: 620 - 200 * cur, top: 360 - 140 * cur, opacity: strikeT >= 0 ? 0 : 1}}>
        <path d="M2 2 L2 24 L8 18 L12 28 L16 26 L12 17 L20 17 Z" fill="#fff" stroke="#0D1320" strokeWidth={1.6} />
      </svg>
      {strikeT >= 0 ? <div style={{position: 'absolute', left: 30, right: 30, top: '50%', height: 22, marginTop: -11, borderRadius: 11, background: C.ink, transform: `rotate(-8deg) scaleX(${x})`, transformOrigin: 'left center'}} /> : null}
    </div>
  );
};

// Festival-weekend shop: "RENT ▲" tag on the word "rent", shoppers walk in on "buy".
export const Shop: React.FC<{t: number; rentT: number; buyT: number; chip: string}> = ({t, rentT, buyT, chip}) => {
  const p = pop(t);
  const people = ['🧍‍♀️', '🧍', '🧍‍♂️', '🧍‍♀️', '🧍'];
  return (
    <div style={{position: 'relative', width: 880, height: 560, transform: `scale(${0.7 + 0.3 * p})`, opacity: Math.min(1, p * 2)}}>
      <div style={{position: 'absolute', left: 170, top: 40, width: 540, height: 400, background: '#fff', border: V3.outline, boxShadow: V3.shadow, borderRadius: 18, overflow: 'hidden'}}>
        <div style={{height: 90, background: `repeating-linear-gradient(90deg, ${C.blue} 0 54px, #fff 54px 108px)`, borderBottom: V3.outline}} />
        <div style={{textAlign: 'center', fontFamily: display, fontSize: 64, marginTop: 14, color: C.ink}}>🪔 FESTIVAL SALE 🪔</div>
        <div style={{position: 'absolute', left: 205, bottom: 0, width: 130, height: 190, background: C.goldSoft, border: V3.outline, borderBottom: 'none', borderRadius: '14px 14px 0 0'}} />
      </div>
      <div style={{position: 'absolute', right: 20, top: 0, padding: '12px 22px', background: C.red, color: '#fff', borderRadius: 14, border: V3.outline, boxShadow: '5px 5px 0 #0D1320', fontFamily: display, fontSize: 64, transform: `rotate(8deg) scale(${pop(rentT)})`}}>RENT ▲</div>
      {people.map((e, i) => {
        const w = progress(buyT, i * 5, 22, ease.outQuart);
        const fromLeft = i % 2 === 0;
        const x = fromLeft ? interpolate(w, [0, 1], [-140, 300 + i * 18]) : interpolate(w, [0, 1], [1000, 420 + i * 14]);
        return buyT < 0 ? null : (
          <div key={i} style={{position: 'absolute', left: x, top: 330, fontSize: 110, transform: `translateY(${Math.abs(Math.sin(w * 12)) * -10}px)`}}>
            {e}
            <span style={{fontSize: 56, marginLeft: -24}}>🛍️</span>
          </div>
        );
      })}
      <div style={{position: 'absolute', left: 0, right: 0, bottom: -10, textAlign: 'center', opacity: progress(buyT, 26, 10)}}>
        <span style={{display: 'inline-block', padding: '12px 24px', borderRadius: 999, background: C.green, color: '#fff', fontFamily: body, fontWeight: 800, fontSize: 30, border: V3.outline}}>{chip}</span>
      </div>
    </div>
  );
};

// Checklist rows that tick on the spoken word.
export const Checks: React.FC<{t: number; items: {text: string; at: number}[]}> = ({t, items}) => (
  <div style={{display: 'flex', flexDirection: 'column', gap: 22, width: 760}}>
    {items.map((it, i) => {
      const p = pop(t - i * 3);
      const tick = pop(it.at);
      return (
        <div key={i} style={{display: 'flex', alignItems: 'center', gap: 24, padding: '20px 28px', borderRadius: 24, background: tick > 0.5 ? C.greenSoft : '#fff', border: V3.outline, boxShadow: '5px 5px 0 #0D1320', transform: `translateX(${(1 - p) * -80}px)`, opacity: Math.min(1, p * 2)}}>
          <div style={{width: 64, height: 64, borderRadius: 16, border: V3.outline, background: tick > 0.5 ? C.green : '#fff', color: '#fff', fontSize: 48, fontWeight: 900, display: 'flex', alignItems: 'center', justifyContent: 'center', transform: `scale(${0.6 + 0.4 * Math.max(tick, 0.5)})`}}>{tick > 0.3 ? '✓' : ''}</div>
          <div style={{fontFamily: body, fontWeight: 800, fontSize: 54, color: C.ink}}>{it.text}</div>
        </div>
      );
    })}
  </div>
);

// Sign-off: profile row whose Follow button flips, plus a share prompt.
export const Follow: React.FC<{t: number; share: string}> = ({t, share}) => {
  const p = pop(t);
  const flip = progress(t, 26, 8);
  return (
    <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 36, transform: `scale(${0.7 + 0.3 * p})`, opacity: Math.min(1, p * 2)}}>
      <div style={{display: 'flex', alignItems: 'center', gap: 20, padding: '20px 26px', borderRadius: 28, background: '#fff', border: V3.outline, boxShadow: V3.shadow}}>
        <div style={{width: 84, height: 84, borderRadius: '50%', background: C.ink, color: '#fff', fontFamily: display, fontSize: 48, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>A</div>
        <div style={{fontFamily: body}}>
          <div style={{fontWeight: 800, fontSize: 36, color: C.ink}}>@adsworm</div>
          <div style={{fontWeight: 600, fontSize: 24, color: C.muted}}>Meta ads, explained simply</div>
        </div>
        <div style={{marginLeft: 20, padding: '14px 26px', borderRadius: 14, border: V3.outline, background: flip > 0.5 ? '#fff' : C.blue, color: flip > 0.5 ? C.ink : '#fff', fontFamily: body, fontWeight: 800, fontSize: 30, transform: `rotateX(${Math.sin(flip * Math.PI) * 80}deg)`}}>{flip > 0.5 ? 'Following ✓' : 'Follow'}</div>
      </div>
      <div style={{maxWidth: 820, textAlign: 'center', fontFamily: body, fontWeight: 800, fontSize: 46, lineHeight: 1.2, color: C.ink, opacity: progress(t, 10, 12)}}>{share}</div>
    </div>
  );
};

// Phone: an ad, a tap, then an in-app product sheet slides up; "your website" waits below, greyed.
export const InApp: React.FC<{t: number; tapT: number; webT: number}> = ({t, tapT, webT}) => {
  const p = pop(t);
  const sheet = tapT < 0 ? 0 : spring({frame: tapT - 6, fps: 30, config: {damping: 16, stiffness: 160}});
  const ring = tapT >= 0 && tapT < 18 ? tapT / 18 : 0;
  return (
    <div style={{display: 'flex', alignItems: 'center', gap: 40, transform: `scale(${0.7 + 0.3 * p})`, opacity: Math.min(1, p * 2)}}>
      <div style={{position: 'relative', width: 300, height: 540, borderRadius: 46, background: C.ink, padding: 12, boxShadow: V3.shadow}}>
        <div style={{position: 'relative', width: '100%', height: '100%', borderRadius: 36, background: '#fff', overflow: 'hidden'}}>
          <div style={{padding: 16, fontFamily: body, fontWeight: 800, fontSize: 18, color: C.ink}}>Your brand · Sponsored</div>
          <div style={{margin: '0 16px', height: 250, borderRadius: 18, background: 'linear-gradient(160deg, #FFD27A, #FF8A5B 55%, #C2410C)', border: '2px solid #0D1320', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 110}}>👟</div>
          <div style={{margin: '14px 16px', height: 50, borderRadius: 12, background: C.blue, color: '#fff', fontFamily: body, fontWeight: 800, fontSize: 22, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>Shop now</div>
          {ring > 0 ? <div style={{position: 'absolute', left: 150 - 40 * (1 + ring), top: 200 - 40 * (1 + ring), width: 80 * (1 + ring), height: 80 * (1 + ring), borderRadius: '50%', border: `6px solid ${C.blue}`, opacity: 1 - ring}} /> : null}
          <div style={{position: 'absolute', left: 0, right: 0, bottom: 0, height: 330, transform: `translateY(${(1 - sheet) * 340}px)`, background: '#fff', borderTop: V3.outline, borderRadius: '28px 28px 0 0', padding: 18, fontFamily: body}}>
            <div style={{width: 60, height: 6, borderRadius: 3, background: '#C9CDD6', margin: '0 auto 14px'}} />
            <div style={{fontWeight: 800, fontSize: 24, color: C.ink}}>Product info</div>
            <div style={{fontWeight: 600, fontSize: 18, color: C.muted, marginTop: 6}}>price · photos · sizes</div>
            <div style={{marginTop: 18, height: 50, borderRadius: 12, background: C.ink, color: '#fff', fontWeight: 800, fontSize: 20, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>opens inside the app</div>
          </div>
        </div>
      </div>
      <div style={{display: 'flex', flexDirection: 'column', gap: 18, fontFamily: body}}>
        <div style={{padding: '18px 24px', borderRadius: 22, border: V3.outline, background: C.blueSoft, fontWeight: 800, fontSize: 36, opacity: progress(tapT, 10, 10), transform: `translateX(${(1 - progress(tapT, 10, 12)) * 40}px)`}}>① In-app page</div>
        <div style={{padding: '18px 24px', borderRadius: 22, border: V3.outline, background: '#F1F2F5', color: C.muted, fontWeight: 800, fontSize: 36, opacity: webT < 0 ? 0 : 0.4 + 0.6 * progress(webT, 0, 10)}}>② Your website</div>
      </div>
    </div>
  );
};

// Calendar page for a deadline, with a red circle drawn around the date.
export const Deadline: React.FC<{t: number; month: string; day: string; note: string}> = ({t, month, day, note}) => {
  const p = pop(t);
  const circle = progress(t, 10, 18, ease.inOutQuart);
  return (
    <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 24}}>
      <div style={{position: 'relative', width: 360, borderRadius: 30, background: '#fff', border: V3.outline, boxShadow: V3.shadow, overflow: 'hidden', transform: `scale(${0.5 + 0.5 * p}) rotate(${(1 - p) * -12}deg)`}}>
        <div style={{background: C.red, color: '#fff', fontFamily: display, fontSize: 70, textAlign: 'center', borderBottom: V3.outline, padding: '6px 0 2px'}}>{month}</div>
        <div style={{fontFamily: display, fontSize: 230, lineHeight: 1.05, textAlign: 'center', color: C.ink}}>{day}</div>
        <svg width={360} height={300} style={{position: 'absolute', left: 0, top: 70}}>
          <ellipse cx={180} cy={135} rx={140} ry={112} fill="none" stroke={C.red} strokeWidth={10} strokeLinecap="round" strokeDasharray={800} strokeDashoffset={800 * (1 - circle)} transform="rotate(-8 180 135)" />
        </svg>
      </div>
      <div style={{fontFamily: body, fontWeight: 800, fontSize: 36, color: C.ink, opacity: progress(t, 14, 10)}}>{note}</div>
    </div>
  );
};

// Two places a shopper can go (analogy): people split between them.
export const Split: React.FC<{t: number; left: {emoji: string; label: string}; right: {emoji: string; label: string}}> = ({t, left, right}) => {
  const p = pop(t);
  const card = (s: {emoji: string; label: string}, bg: string, d: number) => (
    <div style={{flex: 1, borderRadius: 28, border: V3.outline, boxShadow: V3.shadow, background: bg, padding: '24px 12px', textAlign: 'center', transform: `scale(${0.6 + 0.4 * pop(t - d)})`}}>
      <div style={{fontSize: 130, lineHeight: 1.1}}>{s.emoji}</div>
      <div style={{fontFamily: body, fontWeight: 800, fontSize: 34, color: C.ink, marginTop: 8}}>{s.label}</div>
    </div>
  );
  return (
    <div style={{width: 860, opacity: Math.min(1, p * 2)}}>
      <div style={{display: 'flex', gap: 30}}>
        {card(left, C.blueSoft, 0)}
        {card(right, C.goldSoft, 8)}
      </div>
      <div style={{position: 'relative', height: 120}}>
        {['🧍‍♀️', '🧍', '🧍‍♂️', '🧍‍♀️'].map((e, i) => {
          const w = progress(t, 16 + i * 6, 22, ease.outQuart);
          const goLeft = i % 2 === 0;
          return <div key={i} style={{position: 'absolute', top: 10, left: interpolate(w, [0, 1], [400, goLeft ? 120 + i * 30 : 560 + i * 30]), fontSize: 80, transform: `translateY(${Math.abs(Math.sin(w * 10)) * -8}px)`}}>{e}</div>;
        })}
      </div>
    </div>
  );
};
