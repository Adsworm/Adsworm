import {interpolate, spring} from 'remotion';
import {body, display} from '../lib/fonts';
import {ease, progress} from '../lib/motion';
import {Sfx} from './Sfx';
import {C, V3} from './theme';

// v4 board pieces: generic enough to stage any everyday analogy without new code per reel.
// Times are frames since the thing's cue (−1 = not yet).
const pop = (t: number) => (t < 0 ? 0 : spring({frame: t, fps: 30, config: {damping: 11, stiffness: 220, mass: 0.7}}));
const tone = {red: C.red, green: C.green, blue: C.blue, gold: C.gold, pink: V3.pink, ink: C.ink} as const;
type Tone = keyof typeof tone;

// Hook headline: stacked display lines that slam in one after another.
export type HeadLine = {text: string; tone?: Tone; t: number};
export const Headline: React.FC<{lines: HeadLine[]; emoji?: string; emojiT?: number}> = ({lines, emoji, emojiT = -1}) => {
  const longest = Math.max(...lines.map((l) => l.text.length));
  const size = Math.min(190, Math.floor(1560 / longest));
  const e = pop(emojiT);
  return (
    <div style={{position: 'relative', width: 880, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 6}}>
      {lines.map((l, i) => {
        const p = pop(l.t);
        const col = tone[l.tone ?? 'ink'];
        return l.t < 0 ? (
          <div key={i} style={{height: size * 0.92}} />
        ) : (
          <div key={i} style={{fontFamily: display, fontSize: size, lineHeight: 0.92, color: col, whiteSpace: 'nowrap', WebkitTextStroke: l.tone && l.tone !== 'ink' ? '3px #0D1320' : undefined, textShadow: l.tone && l.tone !== 'ink' ? '6px 6px 0 #0D1320' : undefined, transform: `scale(${0.4 + 0.6 * p}) rotate(${(1 - p) * (i % 2 ? 5 : -5)}deg)`, opacity: Math.min(1, p * 2)}}>
            <Sfx name={i === 0 ? 'pop' : 'thump'} t={l.t} volume={i === 0 ? undefined : 0.35} />
            {l.text}
          </div>
        );
      })}
      {emoji && emojiT >= 0 ? <div style={{position: 'absolute', right: -6, top: -40, fontSize: 130, transform: `scale(${e}) rotate(${(1 - e) * 90 + 10}deg)`}}>{emoji}</div> : null}
    </div>
  );
};

// A drawn shop front (striped awning, sign, door) — `emoji: "SHOP"` in a scene.
const ShopFront: React.FC<{size: number; sign?: string}> = ({size, sign}) => (
  <div style={{position: 'relative', width: size * 1.25, height: size, background: '#fff', border: V3.outline, boxShadow: '6px 6px 0 #0D1320', borderRadius: 14, overflow: 'hidden'}}>
    <div style={{height: size * 0.2, background: `repeating-linear-gradient(90deg, ${C.blue} 0 ${size * 0.11}px, #fff ${size * 0.11}px ${size * 0.22}px)`, borderBottom: V3.outline}} />
    {sign ? <div style={{margin: `${size * 0.05}px auto 0`, width: 'fit-content', padding: `2px ${size * 0.06}px`, borderRadius: 8, background: C.gold, border: '2.5px solid #0D1320', fontFamily: display, fontSize: size * 0.13, color: C.ink, whiteSpace: 'nowrap'}}>{sign}</div> : null}
    <div style={{position: 'absolute', left: '37%', bottom: 0, width: '26%', height: '46%', background: C.goldSoft, border: V3.outline, borderBottom: 'none', borderRadius: '10px 10px 0 0'}} />
    <div style={{position: 'absolute', left: '8%', bottom: '14%', width: '20%', height: '26%', background: C.blueSoft, border: '2.5px solid #0D1320', borderRadius: 6}} />
    <div style={{position: 'absolute', right: '8%', bottom: '14%', width: '20%', height: '26%', background: C.blueSoft, border: '2.5px solid #0D1320', borderRadius: 6}} />
  </div>
);

// A little stage for analogies: emoji actors that walk in, speak, and leave on spoken words.
export type Actor = {disc?: Tone; emoji: string; sign?: string; label?: string; x: number; y: number; size?: number; enter?: 'pop' | 'left' | 'right' | 'drop'; t: number; outT?: number; say?: string; sayT?: number; sayTone?: Tone; flip?: boolean; badge?: string; badgeT?: number; badgeTone?: Tone};
export const Scene: React.FC<{actors: Actor[]; height?: number; ground?: boolean}> = ({actors, height = 520, ground = true}) => (
  <div style={{position: 'relative', width: 880, height}}>
    {ground ? <div style={{position: 'absolute', left: 20, right: 20, bottom: 26, height: 5, borderRadius: 3, background: C.ink, opacity: 0.85}} /> : null}
    {actors.map((a, i) => {
      if (a.t < 0) return null;
      const size = a.size ?? 150;
      const p = a.enter === 'pop' || !a.enter ? pop(a.t) : progress(a.t, 0, 16, ease.outQuart);
      const out = a.outT !== undefined && a.outT >= 0 ? progress(a.outT, 0, 16, ease.inOutQuart) : 0;
      const goRight = a.x > 440;
      const dx = a.enter === 'left' ? (1 - p) * -(a.x + 220) : a.enter === 'right' ? (1 - p) * (900 - a.x + 60) : 0;
      const dy = a.enter === 'drop' ? (1 - p) * -260 : 0;
      const walk = a.enter === 'left' || a.enter === 'right' ? Math.abs(Math.sin(p * 11)) * -12 * (1 - p) : 0;
      const exitX = out * (goRight ? 700 : -700);
      const scale = a.enter === 'pop' || !a.enter ? p : 1;
      const s = pop(a.sayT ?? a.t - 6);
      const b = pop(a.badgeT ?? -1);
      return (
        <div key={i} style={{position: 'absolute', left: a.x + dx + exitX, top: a.y + dy + walk, opacity: 1 - out, transform: `scale(${scale})`, transformOrigin: '50% 100%', textAlign: 'center'}}>
          <Sfx name={a.enter === 'left' || a.enter === 'right' ? 'swish' : 'pop'} t={a.t} />
          {a.outT !== undefined ? <Sfx name="swish" t={a.outT} /> : null}
          {a.disc ? <div style={{position: 'absolute', left: '50%', top: size * 0.56, width: size * 1.3, height: size * 1.3, marginLeft: -size * 0.65, marginTop: -size * 0.65, borderRadius: '50%', background: `${tone[a.disc]}30`, border: `3px solid ${tone[a.disc]}`}} /> : null}
          {a.emoji === 'SHOP' ? <ShopFront size={size} sign={a.sign} /> : <div style={{position: 'relative', fontSize: size, lineHeight: 1.05, transform: a.flip ? 'scaleX(-1)' : undefined}}>{a.emoji}</div>}
          {a.label ? <div style={{marginTop: 2, display: 'inline-block', padding: '5px 14px', borderRadius: 999, background: '#fff', border: '2.5px solid #0D1320', fontFamily: body, fontWeight: 800, fontSize: 24, color: C.ink, whiteSpace: 'nowrap'}}>{a.label}</div> : null}
          {a.say && (a.sayT ?? a.t) >= 0 ? (
            <div style={{position: 'absolute', left: '50%', bottom: '100%', marginBottom: 6, transform: `translateX(-50%) scale(${s})`, transformOrigin: '50% 100%', padding: '8px 16px', borderRadius: 16, background: a.sayTone ? tone[a.sayTone] : '#fff', color: a.sayTone && a.sayTone !== 'gold' ? '#fff' : C.ink, border: V3.outline, boxShadow: '4px 4px 0 #0D1320', fontFamily: body, fontWeight: 800, fontSize: 28, whiteSpace: 'nowrap'}}>
              <Sfx name="pop" t={a.sayT ?? a.t} delay={a.sayT === undefined ? 6 : 0} />
              {a.say}
            </div>
          ) : null}
          {a.badge && (a.badgeT ?? -1) >= 0 ? (
            <div style={{position: 'absolute', right: -18, top: -10, width: 58, height: 58, borderRadius: '50%', background: tone[a.badgeTone ?? 'red'], color: '#fff', border: V3.outline, fontFamily: body, fontWeight: 900, fontSize: 34, lineHeight: '54px', transform: `scale(${b})`}}>
              <Sfx name={a.badgeTone === 'green' ? 'ding' : 'buzz'} t={a.badgeT ?? -1} />
              {a.badge}
            </div>
          ) : null}
        </div>
      );
    })}
  </div>
);

// Phone DM thread: messages land on spoken words; timestamps tell the story ("9:02 PM" … "next day").
export type Msg = {from: 'them' | 'me'; text: string; time?: string; t: number; ghost?: boolean};
export const ChatThread: React.FC<{t: number; name: string; msgs: Msg[]; status?: string; statusT?: number; statusTone?: Tone}> = ({t, name, msgs, status, statusT = -1, statusTone = 'red'}) => {
  const p = pop(t);
  const st = pop(statusT);
  return (
    <div style={{position: 'relative', width: 680, height: 520, borderRadius: 44, background: C.ink, padding: 12, boxShadow: V3.shadow, transform: `scale(${0.7 + 0.3 * p})`, opacity: Math.min(1, p * 2)}}>
      <div style={{position: 'relative', width: '100%', height: '100%', borderRadius: 34, background: '#F4F5F8', overflow: 'hidden', fontFamily: body}}>
        <div style={{height: 70, background: '#fff', borderBottom: '2.5px solid #0D1320', display: 'flex', alignItems: 'center', gap: 14, padding: '0 20px'}}>
          <div style={{width: 44, height: 44, borderRadius: '50%', background: `linear-gradient(135deg, ${V3.pink}, ${C.gold})`, border: '2.5px solid #0D1320'}} />
          <div style={{fontWeight: 800, fontSize: 26, color: C.ink}}>{name}</div>
          <div style={{marginLeft: 'auto', fontWeight: 700, fontSize: 18, color: C.muted}}>new enquiry</div>
        </div>
        <div style={{padding: '16px 18px', display: 'flex', flexDirection: 'column', gap: 12}}>
          {msgs.map((m, i) => {
            if (m.t < 0) return null;
            const q = pop(m.t);
            const me = m.from === 'me';
            return (
              <div key={i} style={{alignSelf: me ? 'flex-end' : 'flex-start', maxWidth: '82%', transform: `scale(${q})`, transformOrigin: me ? '100% 100%' : '0 100%'}}>
                <Sfx name="pop" t={m.t} />
                <div style={{padding: '12px 20px', borderRadius: me ? '24px 24px 6px 24px' : '24px 24px 24px 6px', background: me ? C.blue : '#fff', color: me ? '#fff' : C.ink, border: '2.5px solid #0D1320', fontWeight: 700, fontSize: 36, lineHeight: 1.18, opacity: m.ghost ? 0.55 : 1}}>{m.text}</div>
                {m.time ? <div style={{marginTop: 4, fontWeight: 800, fontSize: 24, color: C.muted, textAlign: me ? 'right' : 'left'}}>{m.time}</div> : null}
              </div>
            );
          })}
        </div>
        {status && statusT >= 0 ? (
          <div style={{position: 'absolute', left: 0, right: 0, bottom: 22, display: 'flex', justifyContent: 'center'}}>
            <Sfx name={statusTone === 'green' ? 'ding' : 'buzz'} t={statusT} />
            <div style={{padding: '10px 24px', borderRadius: 999, background: tone[statusTone], color: '#fff', border: V3.outline, boxShadow: '4px 4px 0 #0D1320', fontWeight: 800, fontSize: 34, whiteSpace: 'nowrap', transform: `scale(${st}) rotate(-3deg)`}}>{status}</div>
          </div>
        ) : null}
      </div>
    </div>
  );
};

// AI-assistant chat (generic look, no product chrome): a typed question, an answer that writes itself,
// then a labelled "Sponsored" card below it.
export const AiChat: React.FC<{t: number; question: string; adT: number; brand: string; adLine: string; note?: string}> = ({t, question, adT, brand, adLine, note}) => {
  const p = pop(t);
  const typed = question.slice(0, Math.max(0, Math.floor((t - 4) * 1.6)));
  const done = (t - 4) * 1.6 >= question.length;
  const ansT = t - 4 - question.length / 1.6 - 6;
  const ad = pop(adT);
  return (
    <div style={{position: 'relative', width: 800, height: 540, borderRadius: 30, background: '#fff', border: V3.outline, boxShadow: V3.shadow, overflow: 'hidden', fontFamily: body, transform: `scale(${0.7 + 0.3 * p})`, opacity: Math.min(1, p * 2)}}>
      <div style={{height: 60, borderBottom: '2.5px solid #0D1320', display: 'flex', alignItems: 'center', gap: 12, padding: '0 22px', background: '#F7F8FA'}}>
        <div style={{width: 34, height: 34, borderRadius: 10, background: C.ink, color: '#fff', fontWeight: 900, fontSize: 20, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>✦</div>
        <div style={{fontWeight: 800, fontSize: 24, color: C.ink}}>AI assistant</div>
        {note ? <div style={{marginLeft: 'auto', fontWeight: 700, fontSize: 16, letterSpacing: '0.08em', color: C.muted, border: '2px solid #C9CDD6', borderRadius: 8, padding: '3px 10px'}}>{note}</div> : null}
      </div>
      <div style={{padding: '20px 24px', display: 'flex', flexDirection: 'column', gap: 16}}>
        <div style={{alignSelf: 'flex-end', maxWidth: '86%', padding: '14px 20px', borderRadius: '22px 22px 6px 22px', background: C.blueSoft, border: '2.5px solid #0D1320', fontWeight: 700, fontSize: 30, lineHeight: 1.2, color: C.ink, minHeight: 40}}>
          {typed}
          {!done && t % 10 < 6 ? <span style={{color: C.blue}}>|</span> : null}
          {!done && t >= 4
            ? [0, 1].map((j) => {
                const k = Math.floor((t - 4) / 3) - j; // a soft key click every 3 frames while typing
                return k >= 0 ? <Sfx key={k} name="tick" t={t - 4 - 3 * k} volume={0.1} /> : null;
              })
            : null}
        </div>
        {ansT >= 0 ? (
          <div style={{display: 'flex', flexDirection: 'column', gap: 12, marginTop: 4}}>
            {[92, 78, 86, 54].map((w, i) => (
              <div key={i} style={{height: 20, borderRadius: 10, background: '#E3E6EC', width: `${w * progress(ansT, i * 5, 12, ease.outQuart)}%`}} />
            ))}
          </div>
        ) : null}
      </div>
      {adT >= 0 ? (
        <div style={{position: 'absolute', left: 24, right: 24, bottom: 22, padding: '16px 20px', borderRadius: 22, background: C.goldSoft, border: V3.outline, boxShadow: '5px 5px 0 #0D1320', display: 'flex', alignItems: 'center', gap: 18, transform: `translateY(${(1 - ad) * 160}px) scale(${0.9 + 0.1 * ad})`}}>
          <Sfx name="swish" t={adT} />
          <Sfx name="cash" t={adT} delay={5} />
          <div style={{width: 76, height: 76, borderRadius: 18, background: `linear-gradient(135deg, ${C.blue}, ${V3.pink})`, border: '2.5px solid #0D1320', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 44}}>🛍️</div>
          <div style={{flex: 1}}>
            <div style={{fontWeight: 800, fontSize: 18, letterSpacing: '0.12em', color: C.muted}}>SPONSORED</div>
            <div style={{fontWeight: 800, fontSize: 32, color: C.ink, lineHeight: 1.1}}>{brand}</div>
            <div style={{fontWeight: 600, fontSize: 22, color: C.muted}}>{adLine}</div>
          </div>
          <div style={{padding: '12px 20px', borderRadius: 14, background: C.ink, color: '#fff', fontWeight: 800, fontSize: 24}}>Shop</div>
        </div>
      ) : null}
    </div>
  );
};

// A clock whose hands race while a counter climbs ("replied after 14 hours").
export const Clock: React.FC<{t: number; to: number; unit: string; label: string; toneAfter?: Tone}> = ({t, to, unit, label, toneAfter = 'red'}) => {
  const p = pop(t);
  const run = progress(t, 4, 40, ease.inOutQuart);
  const hours = to * run;
  const done = run >= 1;
  return (
    <div style={{display: 'flex', alignItems: 'center', gap: 44, transform: `scale(${0.6 + 0.4 * p})`, opacity: Math.min(1, p * 2)}}>
      <Sfx name="riser" t={t} delay={24} />
      <Sfx name="buzz" t={t} delay={44} />
      <div style={{position: 'relative', width: 300, height: 300, borderRadius: '50%', background: '#fff', border: '8px solid #0D1320', boxShadow: V3.shadow}}>
        {Array.from({length: 12}).map((_, i) => (
          <div key={i} style={{position: 'absolute', left: 141, top: 10, width: 6, height: 22, borderRadius: 3, background: C.ink, transformOrigin: '3px 132px', transform: `rotate(${i * 30}deg)`}} />
        ))}
        <div style={{position: 'absolute', left: 143, top: 62, width: 10, height: 86, borderRadius: 5, background: C.ink, transformOrigin: '5px 86px', transform: `rotate(${hours * 30}deg)`}} />
        <div style={{position: 'absolute', left: 145, top: 34, width: 6, height: 114, borderRadius: 3, background: tone[toneAfter], transformOrigin: '3px 114px', transform: `rotate(${hours * 360}deg)`}} />
        <div style={{position: 'absolute', left: 134, top: 134, width: 24, height: 24, borderRadius: '50%', background: C.ink}} />
      </div>
      <div style={{fontFamily: body}}>
        <div style={{fontWeight: 800, fontSize: 30, color: C.muted}}>{label}</div>
        <div style={{fontFamily: display, fontSize: 190, lineHeight: 0.95, color: done ? tone[toneAfter] : C.ink, WebkitTextStroke: done ? '3px #0D1320' : undefined, textShadow: done ? '6px 6px 0 #0D1320' : undefined, transform: `translateX(${done && t - 44 < 10 ? Math.sin((t - 44) * 2.6) * (10 - (t - 44)) : 0}px)`}}>
          {Math.round(hours)}
          <span style={{fontSize: 90}}> {unit}</span>
        </div>
      </div>
    </div>
  );
};

// Two plans against one deadline: bars grow on spoken words; a bar that crosses the flag turns red.
export type PlanSeg = {len: number; text: string; t: number};
export type PlanRow = {label: string; start: number; segs: PlanSeg[]; t: number; verdict?: string; verdictT?: number};
export const Plan: React.FC<{from: number; to: number; deadline: number; deadlineLabel: string; unit?: string; rows: PlanRow[]; t: number}> = ({from, to, deadline, deadlineLabel, unit = '', rows, t}) => {
  const W = 860;
  const L = 0;
  const px = (d: number) => L + ((d - from) / (to - from)) * (W - L);
  const p = pop(t);
  const ticks = Array.from({length: to - from + 1}, (_, i) => from + i);
  return (
    <div style={{position: 'relative', width: W, height: 500, fontFamily: body, opacity: Math.min(1, p * 2)}}>
      {/* axis: dates, with the deadline in red */}
      <div style={{position: 'absolute', left: 0, right: 0, top: 58, height: 5, background: C.ink, borderRadius: 3}} />
      {ticks.map((d) => {
        const show = d === deadline || (Math.abs(d - deadline) > 1 && (d - from) % (to - from > 10 ? 3 : 1) === 0);
        return show ? (
          <div key={d} style={{position: 'absolute', left: px(d) - 40, top: d === deadline ? 0 : 12, width: 80, textAlign: 'center', fontFamily: d === deadline ? display : body, fontWeight: 800, fontSize: d === deadline ? 52 : 28, lineHeight: 1, color: d === deadline ? C.red : C.ink}}>
            {d}
            {d === from ? <span style={{fontSize: 20}}> {unit}</span> : null}
          </div>
        ) : null;
      })}
      {/* deadline flag */}
      <div style={{position: 'absolute', left: px(deadline) - 4, top: 50, bottom: 0, width: 8, background: C.red, borderRadius: 4, transform: `scaleY(${progress(t, 4, 14, ease.outQuart)})`, transformOrigin: '50% 0'}} />
      <div style={{position: 'absolute', left: px(deadline) - 330, width: 316, textAlign: 'right', bottom: -4, fontFamily: display, fontSize: 44, color: C.red, opacity: progress(t, 12, 8)}}>{deadlineLabel} ▶</div>
      {rows.map((r, ri) => {
        if (r.t < 0) return null;
        const top = 92 + ri * 184;
        let cursor = r.start;
        const end = r.start + r.segs.reduce((acc, s) => acc + (s.t >= 0 ? s.len : 0), 0);
        const late = end > deadline;
        const v = pop(r.verdictT ?? -1);
        return (
          <div key={ri}>
            <Sfx name="pop" t={r.t} />
            <div style={{position: 'absolute', left: 0, top, fontWeight: 800, fontSize: 38, color: C.ink, opacity: progress(r.t, 0, 8)}}>{r.label}</div>
            {r.segs.map((s, si) => {
              const x0 = px(cursor);
              cursor += s.len;
              if (s.t < 0) return null;
              const g = progress(s.t, 0, 14, ease.outQuart);
              const w = (px(cursor) - x0) * g;
              const over = cursor > deadline;
              return (
                <div key={si} style={{position: 'absolute', left: x0, top: top + 52, width: Math.max(0, w), height: 88, borderRadius: 18, background: over ? C.red : si % 2 ? C.gold : C.blue, border: V3.outline, boxShadow: '4px 4px 0 #0D1320', overflow: 'hidden', display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
                  <Sfx name={over ? 'buzz' : 'swish'} t={s.t} />
                  <span style={{fontWeight: 800, fontSize: 32, color: over || si % 2 === 0 ? '#fff' : C.ink, whiteSpace: 'nowrap', opacity: g}}>{s.text}</span>
                </div>
              );
            })}
            {r.verdict && (r.verdictT ?? -1) >= 0 ? (
              <div style={{position: 'absolute', right: 0, top: top - 8, zIndex: 3, padding: '8px 20px', borderRadius: 14, background: late ? C.red : C.green, color: '#fff', border: V3.outline, boxShadow: '4px 4px 0 #0D1320', fontWeight: 800, fontSize: 36, transform: `rotate(${late ? 4 : -4}deg) scale(${v})`}}>
                <Sfx name={late ? 'buzz' : 'ding'} t={r.verdictT ?? -1} />
                {r.verdict}
              </div>
            ) : null}
          </div>
        );
      })}
    </div>
  );
};

// Three or four tall bars that tell a before / during / after story (cost in Sep → Oct → after Diwali).
// Each bar grows on its spoken word; its value label lands on top; an optional stamp follows.
export type Col = {label: string; value: number; display: string; tone?: Tone; t: number; stamp?: string; stampT?: number};
export const Columns: React.FC<{t: number; title?: string; cols: Col[]; note?: string}> = ({t, title, cols, note}) => {
  const max = Math.max(...cols.map((c) => c.value));
  const H = cols.some((c) => c.stamp) ? 262 : 300;
  const p = pop(t);
  const W = cols.length > 3 ? 172 : 190; // four columns still fit the board
  const gap = cols.length > 3 ? 40 : 46;
  return (
    <div style={{width: 860, fontFamily: body, opacity: Math.min(1, p * 2)}}>
      {title ? <div style={{fontWeight: 800, fontSize: 36, color: C.ink, textAlign: 'center', marginBottom: 8}}>{title}</div> : null}
      <div style={{position: 'relative', height: H + 70, marginTop: cols.some((c) => c.stamp) ? 68 : 0, display: 'flex', justifyContent: 'center', alignItems: 'flex-end', gap, borderBottom: '5px solid #0D1320'}}>
        {cols.map((c, i) => {
          const g = c.t < 0 ? 0 : spring({frame: c.t, fps: 30, config: {damping: 13, stiffness: 120}});
          const h = Math.max(6, (c.value / max) * H * g);
          const col = tone[c.tone ?? 'blue'];
          const s = pop(c.stampT ?? -1);
          return (
            <div key={i} style={{position: 'relative', width: W, display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
              <Sfx name={c.tone === 'red' ? 'buzz' : c.tone === 'green' ? 'ding' : 'pop'} t={c.t} delay={8} />
              <div style={{fontFamily: display, fontSize: 64, lineHeight: 1, color: col, opacity: c.t < 0 ? 0 : progress(c.t, 8, 8), marginBottom: 6, WebkitTextStroke: '2px #0D1320'}}>{c.display}</div>
              <div style={{width: '100%', height: h, background: col, border: V3.outline, borderBottom: 'none', borderRadius: '16px 16px 0 0', boxShadow: '5px 0 0 #0D1320'}} />
              {c.stamp && (c.stampT ?? -1) >= 0 ? (
                <div style={{position: 'absolute', top: -52, left: '50%', padding: '5px 13px', borderRadius: 12, background: '#fff', color: col, border: V3.outline, boxShadow: '4px 4px 0 #0D1320', fontWeight: 800, fontSize: 26, whiteSpace: 'nowrap', transform: `translateX(-50%) rotate(-4deg) scale(${s})`}}>
                  <Sfx name="pop" t={c.stampT ?? -1} />
                  {c.stamp}
                </div>
              ) : null}
            </div>
          );
        })}
      </div>
      <div style={{display: 'flex', justifyContent: 'center', gap, marginTop: 10}}>
        {cols.map((c, i) => (
          <div key={i} style={{width: W, textAlign: 'center', fontWeight: 800, fontSize: 30, lineHeight: 1.1, color: C.ink}}>{c.label}</div>
        ))}
      </div>
      {note ? <div style={{marginTop: 12, textAlign: 'center', fontWeight: 700, fontSize: 24, color: C.muted}}>{note}</div> : null}
    </div>
  );
};

// A formula card worth saving: a small title, the expression in big type, what it equals, a worked example.
export const Formula: React.FC<{t: number; title: string; top: string; bottom: string; equals: string; example?: string; exampleT?: number}> = ({t, title, top, bottom, equals, example, exampleT = -1}) => {
  const p = pop(t);
  const e = pop(exampleT);
  return (
    <div style={{width: 840, padding: '22px 30px 26px', borderRadius: 28, background: C.goldSoft, border: V3.outline, boxShadow: V3.shadow, fontFamily: body, textAlign: 'center', transform: `scale(${0.7 + 0.3 * p})`, opacity: Math.min(1, p * 2)}}>
      <Sfx name="pop" t={t} />
      <div style={{fontWeight: 800, fontSize: 26, letterSpacing: '0.1em', color: C.muted}}>{title}</div>
      <div style={{marginTop: 12, fontWeight: 800, fontSize: 46, lineHeight: 1.1, color: C.ink}}>{top}</div>
      <div style={{margin: '10px auto', width: '86%', height: 6, borderRadius: 3, background: C.ink}} />
      <div style={{fontWeight: 800, fontSize: 46, lineHeight: 1.1, color: C.ink}}>{bottom}</div>
      <div style={{marginTop: 14, fontFamily: display, fontSize: 62, lineHeight: 1, color: C.blue}}>= {equals}</div>
      {example && exampleT >= 0 ? (
        <div style={{marginTop: 16, display: 'inline-block', padding: '10px 22px', borderRadius: 999, background: C.ink, color: '#fff', fontWeight: 800, fontSize: 30, transform: `scale(${e})`}}>
          <Sfx name="ding" t={exampleT} />
          {example}
        </div>
      ) : null}
    </div>
  );
};

// Keep `interpolate` available to scenes that want custom paths later.
export const lerp = (v: number, a: number, b: number) => interpolate(v, [0, 1], [a, b]);
