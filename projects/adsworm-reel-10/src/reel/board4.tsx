import {spring} from 'remotion';
import {body, display} from '../lib/fonts';
import {ease, progress} from '../lib/motion';
import {Sfx} from './Sfx';
import {C, V3} from './theme';

// Literal pictures for the plain-language reels: the screen shows the thing the sentence names (a phone, a Boost
// button, ad cards, people), never a stand-in. Times are frames since the cue (−1 = not yet).
const pop = (t: number) => (t < 0 ? 0 : spring({frame: t, fps: 30, config: {damping: 11, stiffness: 220, mass: 0.7}}));
const INK = '#0D1320';
const PEOPLE = ['🧑', '👩', '👨', '👵', '🧔', '👩‍🦱'];

// One ad card: a coloured tile with a big glyph. `same` cards share one look.
const AdCard: React.FC<{glyph: string; bg: string; size?: number; label?: string; dim?: boolean}> = ({glyph, bg, size = 120, label, dim}) => (
  <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 6, opacity: dim ? 0.35 : 1}}>
    <div style={{position: 'relative', width: size, height: size * 1.12, borderRadius: size * 0.14, background: bg, border: V3.outline, boxShadow: `5px 5px 0 ${INK}`, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: size * 0.5, lineHeight: 1}}>
      {glyph}
      {/* every card carries the small "Ad" mark a paid post carries, so it is not read as an ordinary post */}
      <div style={{position: 'absolute', left: size * 0.06, top: size * 0.06, padding: `${size * 0.015}px ${size * 0.06}px`, borderRadius: size * 0.06, background: INK, color: '#fff', fontFamily: body, fontWeight: 800, fontSize: Math.max(13, size * 0.13), lineHeight: 1.25}}>Ad</div>
    </div>
    {label ? <div style={{fontFamily: body, fontWeight: 800, fontSize: 26, color: C.ink, whiteSpace: 'nowrap'}}>{label}</div> : null}
  </div>
);

const PhoneFrame: React.FC<{children: React.ReactNode; width?: number; height?: number}> = ({children, width = 300, height = 470}) => (
  <div style={{width, height, borderRadius: 38, background: INK, padding: 10, boxShadow: V3.shadow}}>
    <div style={{position: 'relative', width: '100%', height: '100%', borderRadius: 28, background: '#fff', overflow: 'hidden', fontFamily: body}}>{children}</div>
  </div>
);

const PostHead: React.FC<{name: string; sub?: string}> = ({name, sub}) => (
  <div style={{height: 58, display: 'flex', alignItems: 'center', gap: 10, padding: '0 12px', borderBottom: '2px solid #E6E8EE'}}>
    <div style={{width: 36, height: 36, borderRadius: '50%', background: `linear-gradient(135deg, ${V3.pink}, ${C.gold})`, border: `2px solid ${INK}`}} />
    <div>
      <div style={{fontWeight: 800, fontSize: 19, color: C.ink, lineHeight: 1.1}}>{name}</div>
      {sub ? <div style={{fontWeight: 700, fontSize: 15, color: C.muted, lineHeight: 1.1}}>{sub}</div> : null}
    </div>
  </div>
);

// A shop's Instagram page (`mode: 'page'`), or one of its posts running as an ad (`mode: 'ad'`: "Sponsored").
export const InstaPhone: React.FC<{t: number; mode: 'page' | 'ad'; name: string; markT?: number}> = ({t, mode, name, markT = 0}) => {
  const p = pop(t);
  const m = pop(markT);
  return (
    <div style={{transform: `scale(${0.7 + 0.3 * p}) rotate(${(1 - p) * -6}deg)`, opacity: Math.min(1, p * 2)}}>
      <Sfx name="pop" t={t} />
      <PhoneFrame>
        <PostHead name={name} sub={mode === 'ad' ? 'Sponsored' : 'Shop · Instagram'} />
        {mode === 'page' ? (
          <div style={{display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 4, padding: 6}}>
            {['👗', '💇‍♀️', '🧁', '👜', '💍', '🪴', '👟', '☕', '🎁'].map((g, i) => (
              <div key={i} style={{height: 84, borderRadius: 8, background: i % 2 ? C.blueSoft : V3.pinkSoft, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 44, transform: `scale(${pop(t - i * 0.6)})`}}>{g}</div>
            ))}
          </div>
        ) : (
          <>
            <div style={{height: 270, background: C.goldSoft, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 130}}>👗</div>
            <div style={{margin: '14px 12px 0', height: 46, borderRadius: 12, background: C.blue, color: '#fff', fontWeight: 800, fontSize: 22, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>Shop now</div>
            <div style={{position: 'absolute', left: 54, top: 30, padding: '2px 10px', borderRadius: 8, background: C.gold, border: `2.5px solid ${INK}`, fontWeight: 800, fontSize: 18, color: C.ink, transform: `scale(${0.6 + 0.4 * m})`}}>Sponsored = ad</div>
          </>
        )}
      </PhoneFrame>
    </div>
  );
};

// The Boost button is pressed, a coin drops in, the post travels to more phones.
export const BoostPhone: React.FC<{t: number; pressT: number; payT: number; goT: number}> = ({t, pressT, payT, goT}) => {
  const p = pop(t);
  const press = pressT < 0 ? 0 : Math.sin(Math.min(1, pressT / 8) * Math.PI);
  const coin = payT < 0 ? 0 : progress(payT, 0, 12, ease.outQuart);
  return (
    <div style={{position: 'relative', width: 880, height: 480, display: 'flex', alignItems: 'center', justifyContent: 'center', opacity: Math.min(1, p * 2)}}>
      <div style={{transform: `scale(${0.75 + 0.25 * p}) translateX(${goT >= 0 ? -150 * progress(goT, 0, 12, ease.outQuart) : 0}px)`}}>
        <PhoneFrame>
          <PostHead name="aapki_dukaan" />
          <div style={{height: 230, background: V3.pinkSoft, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 120}}>👗</div>
          <div style={{margin: '16px 14px 0', height: 60, borderRadius: 14, background: C.blue, border: `3px solid ${INK}`, color: '#fff', fontWeight: 800, fontSize: 28, display: 'flex', alignItems: 'center', justifyContent: 'center', transform: `scale(${1 - press * 0.1})`, boxShadow: press > 0.1 ? 'none' : `4px 4px 0 ${INK}`}}>
            <Sfx name="tick" t={pressT} />
            Boost post
          </div>
          <div style={{position: 'absolute', left: 150, top: 290 - press * 6, fontSize: 60, transform: `translate(${(1 - Math.min(1, Math.max(0, pressT) / 6)) * 60}px, ${(1 - Math.min(1, Math.max(0, pressT) / 6)) * 60}px)`, opacity: pressT < 0 ? 0 : 1}}>👆</div>
          {payT >= 0 ? (
            <div style={{position: 'absolute', left: 30, top: -70 + coin * 370, width: 62, height: 62, borderRadius: '50%', background: C.gold, border: `3px solid ${INK}`, fontFamily: display, fontSize: 44, lineHeight: '62px', textAlign: 'center', color: C.ink, opacity: 1 - progress(payT, 14, 6)}}>
              <Sfx name="cash" t={payT} volume={0.5} />₹
            </div>
          ) : null}
        </PhoneFrame>
      </div>
      {goT >= 0
        ? PEOPLE.slice(0, 5).map((g, i) => {
            const q = pop(goT - 4 - i * 4);
            const x = 560 + (i % 2) * 150;
            const y = 40 + i * 84;
            return (
              <div key={i} style={{position: 'absolute', left: x, top: y, display: 'flex', alignItems: 'center', gap: 6, transform: `scale(${q})`}}>
                <Sfx name="pop" t={goT} delay={4 + i * 4} volume={0.5} />
                <span style={{fontSize: 58}}>{g}</span>
                <span style={{fontSize: 40}}>📱</span>
              </div>
            );
          })
        : null}
    </div>
  );
};

const PILE = Array.from({length: 28}, (_, i) => ({x: (i % 7) * 30 + ((i * 37) % 11) - 5, y: Math.floor(i / 7) * 46 + ((i * 53) % 13) - 6, r: ((i * 29) % 21) - 10, c: [C.blue, V3.pink, C.gold, C.green, C.red, '#9AA1B2'][i % 6]}));
// The sorter: a pile of ads goes into a box, a few come out, towards one person. `nameT` puts the name on the box.
export const Sorter: React.FC<{t: number; name: string; sub?: string; nameT: number; pileLabel?: string; fewLabel?: string}> = ({t, name, sub, nameT, pileLabel, fewLabel}) => {
  const p = pop(t);
  const n = pop(nameT);
  const flow = t < 0 ? 0 : (t % 40) / 40;
  return (
    <div style={{position: 'relative', width: 880, height: 440, fontFamily: body, opacity: Math.min(1, p * 2)}}>
      <Sfx name="swish" t={t} />
      {/* pile */}
      <div style={{position: 'absolute', left: 6, top: 110, width: 230, height: 210}}>
        {PILE.map((c, i) => (
          <div key={i} style={{position: 'absolute', left: c.x, top: c.y, width: 36, height: 44, borderRadius: 7, background: c.c, border: `2.5px solid ${INK}`, transform: `rotate(${c.r}deg) scale(${pop(t - i * 0.6)})`}} />
        ))}
      </div>
      {pileLabel ? <div style={{position: 'absolute', left: 0, top: 326, width: 240, textAlign: 'center', fontWeight: 800, fontSize: 28, color: C.ink}}>{pileLabel}</div> : null}
      {/* moving card + arrows */}
      <div style={{position: 'absolute', left: 236 + flow * 60, top: 196, width: 30, height: 38, borderRadius: 6, background: C.blue, border: `2.5px solid ${INK}`, opacity: flow < 0.9 ? 1 : 0}} />
      <div style={{position: 'absolute', left: 244, top: 150, fontFamily: display, fontSize: 70, color: INK, lineHeight: 1}}>→</div>
      {/* the box */}
      <div style={{position: 'absolute', left: 320, top: 96, width: 280, height: 236, borderRadius: 26, background: C.ink, border: V3.outline, boxShadow: V3.shadow, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', transform: `scale(${1 + Math.sin(Math.max(0, t) / 6) * 0.012})`}}>
        <div style={{fontSize: 80, lineHeight: 1, opacity: nameT >= 0 ? 0.25 : 1}}>⚙️</div>
        {nameT >= 0 ? (
          <div style={{position: 'absolute', inset: 0, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', transform: `scale(${0.6 + 0.4 * n})`}}>
            <Sfx name="thump" t={nameT} volume={0.45} />
            <div style={{fontFamily: display, fontSize: 60, lineHeight: 0.95, color: '#fff', textAlign: 'center', whiteSpace: 'pre-line'}}>{name}</div>
            {sub ? <div style={{marginTop: 6, fontWeight: 800, fontSize: 30, color: C.gold}}>{sub}</div> : null}
          </div>
        ) : null}
      </div>
      <div style={{position: 'absolute', left: 612, top: 150, fontFamily: display, fontSize: 70, color: INK, lineHeight: 1}}>→</div>
      {/* the few */}
      <div style={{position: 'absolute', left: 676, top: 150, display: 'flex', gap: 6}}>
        {[C.blue, V3.pink, C.gold].map((c, i) => (
          <div key={i} style={{width: 40, height: 50, borderRadius: 8, background: c, border: `2.5px solid ${INK}`, transform: `scale(${pop(t - 14 - i * 5)})`}} />
        ))}
      </div>
      {fewLabel ? <div style={{position: 'absolute', left: 640, top: 326, width: 240, textAlign: 'center', fontWeight: 800, fontSize: 28, color: C.ink}}>{fewLabel}</div> : null}
      <div style={{position: 'absolute', left: 716, top: 214, display: 'flex', alignItems: 'center', transform: `scale(${pop(t - 22)})`}}>
        <span style={{fontSize: 84}}>🧑</span>
        <span style={{fontSize: 50, marginLeft: -8}}>📱</span>
      </div>
    </div>
  );
};

// Five ads that look the same = one ad (as the system may see them).
export const SameIsOne: React.FC<{t: number; eqT: number; glyph?: string; tag?: string}> = ({t, eqT, glyph = '👗', tag}) => {
  const e = pop(eqT);
  return (
    <div style={{width: 880, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 18, fontFamily: body}}>
      <div style={{display: 'flex', alignItems: 'center', gap: 10}}>
        {Array.from({length: 5}).map((_, i) => (
          <div key={i} style={{transform: `scale(${pop(t - i)})`}}>
            <Sfx name="pop" t={t} delay={i} volume={0.5} />
            <AdCard glyph={glyph} bg={V3.pinkSoft} size={112} />
          </div>
        ))}
        <div style={{fontFamily: display, fontSize: 120, lineHeight: 0.8, color: C.red, margin: '0 2px', transform: `scale(${e})`}}>
          <Sfx name="buzz" t={eqT} />=
        </div>
        <div style={{transform: `scale(${pop(eqT - 6)})`}}>
          <AdCard glyph={glyph} bg={V3.pinkSoft} size={150} />
        </div>
      </div>
      {tag && eqT >= 0 ? <div style={{padding: '8px 20px', borderRadius: 999, background: C.ink, color: '#fff', fontWeight: 800, fontSize: 30, transform: `scale(${pop(eqT - 10)})`}}>{tag}</div> : null}
    </div>
  );
};

// One card, a crowd, and only a couple of people lit up: fewer people reached.
export const Reach: React.FC<{t: number; lit?: number; tag?: string}> = ({t, lit = 2, tag}) => {
  const cols = 8;
  const total = 24;
  const litAt = [9, 14, 3, 20, 6, 17];
  return (
    <div style={{width: 880, display: 'flex', alignItems: 'center', gap: 34, fontFamily: body, opacity: Math.min(1, pop(t) * 2)}}>
      <Sfx name="huh" t={t} volume={0.4} />
      <AdCard glyph="👗" bg={V3.pinkSoft} size={150} />
      <div style={{fontFamily: display, fontSize: 80, color: INK, lineHeight: 1}}>→</div>
      <div>
        <div style={{display: 'grid', gridTemplateColumns: `repeat(${cols}, 1fr)`, gap: 6}}>
          {Array.from({length: total}).map((_, i) => {
            const on = litAt.slice(0, lit).includes(i);
            return (
              <div key={i} style={{fontSize: 54, lineHeight: 1.05, filter: on ? 'none' : 'grayscale(1)', opacity: on ? 1 : 0.28, transform: `scale(${on ? 0.9 + 0.25 * pop(t - 12) : pop(t - i * 0.5)})`}}>{PEOPLE[i % PEOPLE.length]}</div>
            );
          })}
        </div>
        {tag ? <div style={{marginTop: 12, display: 'inline-block', padding: '8px 20px', borderRadius: 999, background: C.red, color: '#fff', border: V3.outline, fontWeight: 800, fontSize: 30, transform: `scale(${pop(t - 16)})`}}>{tag}</div> : null}
      </div>
    </div>
  );
};

// Three ads that differ, each named as it appears, each reaching a different person.
export type Kind = {glyph: string; bg?: string; label: string; t: number; person?: string};
export const ThreeAds: React.FC<{items: Kind[]; compact?: boolean}> = ({items, compact}) => (
  <div style={{width: 880, display: 'flex', justifyContent: 'center', gap: 40, fontFamily: body}}>
    {items.map((k, i) => {
      const p = pop(k.t);
      const bg = k.bg ?? [C.blueSoft, C.goldSoft, C.greenSoft][i % 3];
      return (
        <div key={i} style={{display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 8, opacity: k.t < 0 ? 0.001 : 1, transform: `scale(${0.6 + 0.4 * p}) rotate(${(1 - p) * (i - 1) * 8}deg)`}}>
          <Sfx name="pop" t={k.t} />
          <AdCard glyph={k.glyph} bg={bg} size={compact ? 130 : 170} label={compact ? undefined : k.label} />
          {compact ? null : (
            <>
              <div style={{fontFamily: display, fontSize: 54, lineHeight: 0.8, color: INK, opacity: progress(k.t, 8, 6)}}>↓</div>
              <div style={{fontSize: 80, lineHeight: 1, transform: `scale(${pop(k.t - 10)})`}}>
                <Sfx name="ding" t={k.t} delay={10} volume={0.45} />
                {k.person ?? PEOPLE[i]}
              </div>
            </>
          )}
        </div>
      );
    })}
  </div>
);

// The save (bookmark) icon is tapped and fills in.
export const SaveTap: React.FC<{t: number; tapT: number; label?: string}> = ({t, tapT, label}) => {
  const f = pop(tapT);
  return (
    <div style={{display: 'flex', alignItems: 'center', gap: 40, fontFamily: body, opacity: Math.min(1, pop(t) * 2)}}>
      <div style={{position: 'relative', width: 190, height: 250}}>
        <Sfx name="ding" t={tapT} />
        <svg viewBox="0 0 76 100" width={190} height={250}>
          <path d="M8 6 H68 V94 L38 70 L8 94 Z" fill={tapT >= 0 ? C.ink : '#fff'} stroke={INK} strokeWidth={7} strokeLinejoin="round" />
        </svg>
        <div style={{position: 'absolute', right: -50, bottom: -20, fontSize: 96, transform: `translate(${(1 - Math.min(1, Math.max(0, tapT + 8) / 8)) * 50}px, ${(1 - Math.min(1, Math.max(0, tapT + 8) / 8)) * 50}px)`}}>👆</div>
      </div>
      {label ? <div style={{fontFamily: display, fontSize: 110, lineHeight: 0.95, color: C.ink, whiteSpace: 'pre-line', transform: `scale(${0.7 + 0.3 * f})`}}>{label}</div> : null}
    </div>
  );
};

// The keyword is typed slowly, letter by letter, large enough to copy; then a message lands in the inbox.
export const TypeWord: React.FC<{t: number; word: string; typeT: number; dmT: number; dm?: string; hint?: string}> = ({t, word, typeT, dmT, dm, hint}) => {
  const n = typeT < 0 ? 0 : Math.min(word.length, Math.floor(typeT / 4) + 1);
  const d = pop(dmT);
  return (
    <div style={{width: 860, fontFamily: body, opacity: Math.min(1, pop(t) * 2)}}>
      {hint ? <div style={{fontWeight: 800, fontSize: 30, color: C.muted, marginBottom: 10}}>{hint}</div> : null}
      <div style={{height: 150, borderRadius: 26, background: '#fff', border: V3.outline, boxShadow: V3.shadow, display: 'flex', alignItems: 'center', padding: '0 26px', gap: 16}}>
        <span style={{fontSize: 56}}>💬</span>
        <span style={{fontFamily: display, fontSize: 112, lineHeight: 1, letterSpacing: '0.04em', color: C.blue}}>
          {word.slice(0, n)}
          {Array.from({length: n}).map((_, i) => (
            <Sfx key={i} name="tick" t={typeT} delay={i * 4} volume={0.5} />
          ))}
        </span>
        {typeT >= 0 && n < word.length ? <span style={{width: 6, height: 96, background: C.ink}} /> : null}
      </div>
      {dm && dmT >= 0 ? (
        <div style={{marginTop: 22, marginLeft: 120, padding: '16px 24px', borderRadius: '26px 26px 26px 8px', background: C.greenSoft, border: V3.outline, boxShadow: `5px 5px 0 ${INK}`, fontWeight: 800, fontSize: 36, lineHeight: 1.2, color: C.ink, transform: `translateY(${(1 - d) * -40}px) scale(${0.8 + 0.2 * d})`, transformOrigin: '0 0'}}>
          <Sfx name="ding" t={dmT} />
          {dm}
        </div>
      ) : null}
    </div>
  );
};
