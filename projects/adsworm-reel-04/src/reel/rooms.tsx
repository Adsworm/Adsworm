import {body, display} from '../lib/fonts';
import {ease} from '../lib/motion';
import {C} from './theme';
import {sinceLine, sinceWord, TL} from './tl';

// The four "rooms" on the canvas. Each builds on the spoken word (sinceWord / sinceLine are seconds
// since that word or line, −1 before it). Facts and receipts: script/sources.md.
export const ROOM_W = 900;
export const ROOM_H = 700;
const clamp01 = (v: number) => Math.max(0, Math.min(1, v));
const ip = (s: number, dur = 0.5, e = ease.outExpo) => (s < 0 ? 0 : e(clamp01(s / dur)));
const mono = 'ui-monospace, "DejaVu Sans Mono", monospace';

const Chip: React.FC<{p: number; color?: string; bg?: string; children: React.ReactNode; size?: number}> = ({p, color = C.cream, bg = 'rgba(240,238,232,0.08)', children, size = 20}) => (
  <div style={{display: 'inline-flex', alignItems: 'center', gap: 8, padding: '8px 16px', borderRadius: 999, background: bg, border: '1px solid rgba(240,238,232,0.14)', color, fontFamily: body, fontWeight: 700, fontSize: size, letterSpacing: '0.04em', whiteSpace: 'nowrap', opacity: p, transform: `translateY(${(1 - p) * 12}px) scale(${0.92 + 0.08 * p})`}}>{children}</div>
);

const Panel: React.FC<{n: string; title: string; tag?: string; receipt: string; t: number; start: number; children: React.ReactNode}> = ({n, title, tag, receipt, t, start, children}) => (
  <div style={{width: ROOM_W, height: ROOM_H, borderRadius: 40, padding: '34px 40px 40px', boxSizing: 'border-box', background: 'linear-gradient(180deg, rgba(26,36,56,0.96), rgba(13,19,32,0.96))', border: '1px solid rgba(240,238,232,0.13)', boxShadow: '0 50px 140px rgba(0,0,0,0.6), inset 0 1px 0 rgba(255,255,255,0.07)', display: 'flex', flexDirection: 'column', gap: 14, position: 'relative', fontFamily: body, color: C.cream}}>
    <div style={{display: 'flex', alignItems: 'center', gap: 16}}>
      <div style={{fontFamily: display, fontSize: 54, lineHeight: 0.9, color: C.gold, paddingTop: 4}}>{n}</div>
      <div style={{fontWeight: 800, fontSize: 27, letterSpacing: '0.08em'}}>{title}</div>
      {tag ? <div style={{marginLeft: 'auto', fontSize: 15, fontWeight: 700, letterSpacing: '0.14em', color: C.muted, border: '1px solid rgba(240,238,232,0.2)', borderRadius: 8, padding: '4px 10px'}}>{tag}</div> : null}
    </div>
    <div>
      <Chip p={ip(t - start - 0.35)} size={18} color={C.muted}>
        <span style={{color: C.blueBright}}>●</span> SOURCE · {receipt}
      </Chip>
    </div>
    <div style={{flex: 1, position: 'relative'}}>{children}</div>
  </div>
);

// "AMAN TRANSLATES" stamp: the money version of what the algorithm just said.
const Translate: React.FC<{s: number; text: string}> = ({s, text}) => {
  const p = ip(s, 0.35);
  if (s < 0) return null;
  return (
    <div style={{position: 'absolute', left: 36, right: 36, bottom: -46, padding: '18px 26px', borderRadius: 22, background: `linear-gradient(100deg, ${C.gold}, ${C.goldBright})`, color: C.bg, fontFamily: body, boxShadow: '0 24px 60px rgba(0,0,0,0.55)', opacity: p, transform: `translateY(${(1 - p) * 40}px) rotate(${-1.6 * p}deg) scale(${1.15 - 0.15 * p})`}}>
      <div style={{fontSize: 17, fontWeight: 800, letterSpacing: '0.18em', opacity: 0.75}}>AMAN TRANSLATES →</div>
      <div style={{fontSize: 36, fontWeight: 800, lineHeight: 1.1, letterSpacing: '-0.01em', marginTop: 4}}>{text}</div>
    </div>
  );
};

// A CSS-drawn hero product (generic perfume bottle — no real brand).
const Product: React.FC<{t: number; moving: number}> = ({t, moving}) => {
  const sweep = ((t * 0.9) % 1.6) - 0.3;
  return (
    <div style={{position: 'absolute', inset: 0, overflow: 'hidden', background: 'radial-gradient(circle at 50% 38%, #34405E, #0D1424 75%)'}}>
      <div style={{position: 'absolute', inset: 0, transform: `scale(${1 + moving * (0.12 + 0.05 * Math.sin(t * 1.3))}) rotate(${moving * 3 * Math.sin(t * 0.9)}deg)`}}>
        <div style={{position: 'absolute', left: '39%', top: '20%', width: '22%', height: '13%', borderRadius: 8, background: 'linear-gradient(#262C3B, #4A5268)'}} />
        <div style={{position: 'absolute', left: '27%', top: '32%', width: '46%', height: '52%', borderRadius: 30, background: `linear-gradient(135deg, ${C.goldBright}, rgba(200,169,110,0.75) 45%, #6E5428)`, boxShadow: '0 30px 50px rgba(0,0,0,0.5), inset 0 0 0 2px rgba(255,255,255,0.25)', display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
          <div style={{fontFamily: display, fontSize: 'clamp(10px, 4vw, 60px)', color: C.bg, letterSpacing: '0.1em'}}>AURUM</div>
        </div>
        <div style={{position: 'absolute', left: '20%', right: '20%', bottom: '8%', height: '6%', borderRadius: '50%', background: 'radial-gradient(rgba(0,0,0,0.6), transparent 70%)'}} />
      </div>
      {moving > 0 ? <div style={{position: 'absolute', top: '-20%', bottom: '-20%', width: '30%', left: `${sweep * 100}%`, background: 'linear-gradient(90deg, transparent, rgba(255,255,255,0.28), transparent)', transform: 'rotate(18deg)', opacity: moving}} /> : null}
    </div>
  );
};

export const HookRoom: React.FC<{t: number}> = ({t}) => {
  const b = sinceLine(t, 1);
  const out = ip(b + 0.1, 0.35);
  const inB = ip(b, 0.5);
  const cpa = sinceWord(t, 'hook', 'cpa');
  const days = TL.vars.days ?? 36;
  const roll = b < 0 ? 0 : Math.min(1, b / 0.9);
  const shown = Math.round(99 - (99 - days) * ease.outExpo(roll));
  return (
    <div style={{width: ROOM_W, height: ROOM_H, position: 'relative', fontFamily: display, color: C.cream}}>
      {/* A: the cover — the orb sits between these two lines */}
      <div style={{position: 'absolute', left: 0, right: 0, top: -10, textAlign: 'center', fontSize: 104, lineHeight: 0.95, opacity: 1 - out, transform: `translateY(${-out * 60}px)`}}>
        META QUIETLY CHANGED
      </div>
      <div style={{position: 'absolute', left: -40, right: -40, bottom: -10, textAlign: 'center', fontSize: 118, lineHeight: 0.9, whiteSpace: 'nowrap', opacity: 1 - out, transform: `translateY(${out * 60}px)`}}>
        <span style={{color: C.gold}}>3 THINGS</span> BEFORE Q4
      </div>
      {/* B: the stake */}
      {b >= 0 ? (
        <div style={{position: 'absolute', inset: 0, opacity: inB, transform: `scale(${0.94 + 0.06 * inB})`}}>
          <div style={{position: 'absolute', left: 40, right: 40, top: 10, height: 300, borderRadius: 32, background: 'rgba(17,24,39,0.9)', border: '1px solid rgba(240,238,232,0.12)', overflow: 'hidden'}}>
            <div style={{position: 'absolute', left: 32, top: 24, fontFamily: body, fontWeight: 800, fontSize: 22, letterSpacing: '0.14em', color: C.muted}}>YOUR CPA · IF NOTHING CHANGES</div>
            <svg width={740} height={220} style={{position: 'absolute', left: 40, top: 66}}>
              <path d="M0 190 C 120 185, 220 178, 320 165 S 520 120, 600 70 S 700 18, 740 8" fill="none" stroke={C.red} strokeWidth={7} strokeLinecap="round" strokeDasharray={1000} strokeDashoffset={1000 * (1 - ip(cpa, 1.1, ease.inOutQuart))} style={{filter: `drop-shadow(0 0 12px ${C.red})`}} />
            </svg>
            <div style={{position: 'absolute', right: 30, top: 20, fontSize: 78, color: C.red, opacity: ip(cpa - 0.6, 0.4)}}>CPA ↑</div>
          </div>
          <div style={{position: 'absolute', left: 0, right: 0, bottom: 0, display: 'flex', alignItems: 'flex-end', justifyContent: 'center', gap: 26}}>
            <div style={{fontSize: 330, lineHeight: 0.78, color: C.gold, textShadow: '0 0 60px rgba(200,169,110,0.35)'}}>{shown}</div>
            <div style={{fontSize: 74, lineHeight: 0.92, paddingBottom: 8}}>
              DAYS TO
              <br />
              {TL.vars.countdownLabel || 'BLACK FRIDAY'}
            </div>
          </div>
        </div>
      ) : null}
    </div>
  );
};

export const OneRoom: React.FC<{t: number; start: number}> = ({t, start}) => {
  const st = sinceWord(t, 'one', 'static');
  const click = sinceWord(t, 'one', 'video');
  const vid = ip(click - 0.1, 0.6);
  const cursorP = ip(st, 0.9, ease.inOutQuart);
  const press = click >= 0 && click < 0.18 ? 0.92 : 1;
  return (
    <Panel n="01" title="ADVANTAGE+ CREATIVE" tag="ILLUSTRATIVE UI" receipt="META FOR BUSINESS · 6 OCT 2026" t={t} start={start}>
      <div style={{position: 'absolute', left: 0, top: 10, width: 300, height: 300, borderRadius: 24, overflow: 'hidden', border: `3px solid ${st >= 0 ? C.blueBright : 'rgba(240,238,232,0.2)'}`, boxShadow: st >= 0 ? `0 0 40px rgba(43,123,255,0.45)` : undefined}}>
        <Product t={t} moving={0} />
      </div>
      <div style={{position: 'absolute', left: 0, top: 326}}>
        <Chip p={1} size={18} color={C.muted}>static.jpg · 1 image</Chip>
      </div>
      {/* the button + cursor */}
      <div style={{position: 'absolute', left: 318, top: 128, padding: '16px 22px', borderRadius: 16, background: click >= 0 ? C.blueBright : 'rgba(43,123,255,0.18)', border: `1px solid ${C.blueBright}`, fontWeight: 800, fontSize: 24, transform: `scale(${press})`, whiteSpace: 'nowrap'}}>✦ Generate video</div>
      <svg width={40} height={48} viewBox="0 0 24 30" style={{position: 'absolute', left: 520 - 130 * cursorP, top: 300 - 128 * cursorP, opacity: st >= 0 ? 1 - ip(click - 0.4, 0.3) : 0, transform: `scale(${press})`}}>
        <path d="M2 2 L2 24 L8 18 L12 28 L16 26 L12 17 L20 17 Z" fill="#fff" stroke={C.bg} strokeWidth={1.5} />
      </svg>
      {/* the result: a 9:16 video built from the same image */}
      <div style={{position: 'absolute', right: 0, top: -6, width: 250, height: 444, borderRadius: 26, overflow: 'hidden', border: '3px solid rgba(240,238,232,0.85)', boxShadow: '0 30px 70px rgba(0,0,0,0.6)', opacity: vid, transform: `translateX(${(1 - vid) * -160}px) scale(${0.6 + 0.4 * vid}) rotate(${(1 - vid) * -8}deg)`, transformOrigin: 'left center'}}>
        <Product t={t} moving={vid} />
        <div style={{position: 'absolute', left: 14, top: 14, padding: '4px 10px', borderRadius: 8, background: 'rgba(8,12,20,0.7)', fontSize: 16, fontWeight: 800, letterSpacing: '0.1em'}}>VIDEO · 9:16</div>
        <div style={{position: 'absolute', left: 14, right: 14, bottom: 16, height: 6, borderRadius: 3, background: 'rgba(255,255,255,0.25)'}}>
          <div style={{width: `${((click < 0 ? 0 : click) / 6) * 100 % 100}%`, height: '100%', borderRadius: 3, background: '#fff'}} />
        </div>
      </div>
      <div style={{position: 'absolute', left: 318, top: 214}}>
        <Chip p={ip(click - 0.5)} color={C.green} bg="rgba(61,220,132,0.12)">✓ LIVE FOR EVERYONE</Chip>
      </div>
      <Translate s={sinceLine(t, 4)} text="Your best static = your cheapest video." />
    </Panel>
  );
};

const TILES = ['UGC', 'STATIC', 'REEL', 'CAROUSEL', 'DEMO', 'REVIEW', 'MEME', 'BEFORE/AFTER', 'FOUNDER', 'OFFER', 'UNBOXING', 'TESTIMONIAL', 'HOW-TO', 'POV', 'COMPARISON', 'GREEN SCREEN', 'STORY', 'FAQ', 'STAT', 'CREATOR'];
const TILE_BG = [C.blueBright, C.gold, '#7A5CFF', '#FF7A59', C.green, '#E04594', C.cyan, '#F2C14E'];

export const TwoRoom: React.FC<{t: number; start: number}> = ({t, start}) => {
  const num = sinceWord(t, 'two', '18.9%');
  const algo = sinceLine(t, 6);
  const many = sinceWord(t, 'two', '20');
  const gem = ip(t - start, 0.5);
  const n = ip(num, 1.0, ease.outQuart);
  const up = ip(algo, 0.45);
  return (
    <Panel n="02" title="GEM · META'S NEW AD MODEL" receipt="ENGINEERING.FB.COM · 13 OCT 2026 · META'S OWN NUMBERS" t={t} start={start}>
      {/* before the number: GEM wordmark */}
      <div style={{position: 'absolute', left: 0, right: 0, top: 40, textAlign: 'center', fontFamily: display, fontSize: 220, lineHeight: 1, color: 'transparent', WebkitTextStroke: `3px ${C.cyan}`, opacity: gem * (1 - ip(num, 0.3)), transform: `scale(${0.85 + 0.15 * gem})`, filter: `drop-shadow(0 0 24px rgba(95,225,255,0.5))`}}>GEM</div>
      {/* the number: big, then parked top-left when the algorithm cuts in */}
      {num >= 0 ? (
        <div style={{position: 'absolute', left: 0, top: 0, transformOrigin: '0 0', transform: `translate(${(1 - up) * 70}px, ${(1 - up) * 20}px) scale(${1 - 0.62 * up})`}}>
          <div style={{fontFamily: display, fontSize: 250, lineHeight: 0.85, color: C.gold, textShadow: '0 0 60px rgba(200,169,110,0.35)'}}>+{(18.9 * n).toFixed(1)}%</div>
          <div style={{display: 'flex', gap: 22, alignItems: 'baseline', marginTop: 10}}>
            <div style={{fontWeight: 800, fontSize: 34, letterSpacing: '0.12em'}}>CONVERSIONS</div>
            <div style={{fontWeight: 700, fontSize: 30, color: C.muted, opacity: ip(num - 0.7)}}>+12% CTR</div>
          </div>
        </div>
      ) : null}
      {/* the catch: three versions of one ad get struck out… */}
      {algo >= 0 ? (
        <div style={{position: 'absolute', left: 0, right: 0, top: 150, display: 'flex', gap: 14, justifyContent: 'center', opacity: 1 - ip(many, 0.3)}}>
          {[0, 1, 2].map((i) => {
            const p = ip(algo - i * 0.08, 0.3);
            return (
              <div key={i} style={{width: 200, height: 250, borderRadius: 18, overflow: 'hidden', position: 'relative', opacity: p, transform: `translateY(${(1 - p) * 30}px)`}}>
                <Product t={t} moving={0} />
                <div style={{position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: display, fontSize: 200, color: C.red, opacity: ip(algo - 0.5 - i * 0.1, 0.2), transform: `scale(${1.6 - 0.6 * ip(algo - 0.5 - i * 0.1, 0.2)})`}}>×</div>
              </div>
            );
          })}
        </div>
      ) : null}
      {/* …and twenty different ones pop in */}
      {many >= 0 ? (
        <div style={{position: 'absolute', left: 0, right: 0, top: 128, display: 'grid', gridTemplateColumns: 'repeat(5, 1fr)', gap: 10}}>
          {TILES.map((label, i) => {
            const p = ip(many - i * 0.035, 0.35);
            return (
              <div key={label} style={{height: 76, borderRadius: 14, background: `linear-gradient(135deg, ${TILE_BG[i % TILE_BG.length]}, rgba(8,12,20,0.5))`, display: 'flex', alignItems: 'flex-end', padding: '0 0 8px 10px', fontWeight: 800, fontSize: 14, letterSpacing: '0.06em', color: '#fff', opacity: p, transform: `scale(${0.4 + 0.6 * p}) rotate(${(1 - p) * (i % 2 ? 10 : -10)}deg)`}}>
                {label}
              </div>
            );
          })}
        </div>
      ) : null}
      <Translate s={sinceWord(t, 'two', 'creatives')} text="Ship 20 different creatives, not 3 versions of one." />
    </Panel>
  );
};

export const ThreeRoom: React.FC<{t: number; start: number}> = ({t, start}) => {
  const cost = sinceWord(t, 'three', 'cost');
  const ad = sinceLine(t, 9);
  const week = sinceLine(t, 10);
  const count = Math.round(994 + 10 * ip(t - start - 0.6, 2.4, ease.inOutQuart));
  const over = count > 1000;
  const swap = ip(week, 0.4);
  const Bubble: React.FC<{me?: boolean; text: string; delay: number}> = ({me, text, delay}) => {
    const p = ip(t - start - delay, 0.35);
    const tag = ad >= 0 ? 'FREE' : over && me ? '$' : '';
    return (
      <div style={{alignSelf: me ? 'flex-end' : 'flex-start', maxWidth: 290, padding: '12px 16px', borderRadius: 18, background: me ? C.blue : 'rgba(240,238,232,0.1)', fontSize: 21, fontWeight: 600, position: 'relative', opacity: p, transform: `translateY(${(1 - p) * 14}px)`}}>
        {text}
        {me && tag ? <div style={{position: 'absolute', right: -12, top: -12, padding: '2px 9px', borderRadius: 999, background: tag === 'FREE' ? C.green : C.red, color: C.bg, fontSize: 15, fontWeight: 800}}>{tag}</div> : null}
      </div>
    );
  };
  return (
    <Panel n="03" title="WHATSAPP BUSINESS PRICING" tag="ILLUSTRATIVE UI" receipt="DEVELOPERS.FACEBOOK.COM · FROM 1 OCT 2026" t={t} start={start}>
      {/* chat */}
      <div style={{position: 'absolute', left: 0, top: 0, width: 410, height: 430, borderRadius: 26, background: 'rgba(8,12,20,0.6)', border: '1px solid rgba(240,238,232,0.12)', padding: 18, boxSizing: 'border-box', display: 'flex', flexDirection: 'column', gap: 12, overflow: 'hidden'}}>
        <div style={{display: 'flex', alignItems: 'center', gap: 10, paddingBottom: 10, borderBottom: '1px solid rgba(240,238,232,0.1)'}}>
          <div style={{width: 34, height: 34, borderRadius: '50%', background: C.gold}} />
          <div style={{fontWeight: 800, fontSize: 20}}>Your Brand</div>
          <div style={{marginLeft: 'auto', fontSize: 15, color: C.muted}}>business chat</div>
        </div>
        {ad >= 0 ? (
          <div style={{padding: '10px 14px', borderRadius: 14, border: `2px solid ${C.cyan}`, background: 'rgba(95,225,255,0.08)', fontSize: 17, fontWeight: 700, opacity: ip(ad, 0.3), transform: `scale(${0.9 + 0.1 * ip(ad, 0.3)})`}}>
            <span style={{color: C.cyan}}>SPONSORED</span> · started from a click-to-WhatsApp ad
          </div>
        ) : null}
        <Bubble text="Hi! Is this still available?" delay={0.2} />
        <Bubble me text="Yes! Want the link?" delay={0.7} />
        <Bubble me text="Here you go →" delay={1.3} />
      </div>
      {/* meter → free window */}
      <div style={{position: 'absolute', right: 0, top: 0, width: 370, height: 430, borderRadius: 26, background: 'rgba(8,12,20,0.6)', border: `1px solid ${over && week < 0 ? 'rgba(255,90,90,0.5)' : 'rgba(240,238,232,0.12)'}`, padding: 24, boxSizing: 'border-box', overflow: 'hidden'}}>
        <div style={{opacity: 1 - swap, transform: `translateY(${-swap * 30}px)`}}>
          <div style={{fontWeight: 800, fontSize: 17, letterSpacing: '0.14em', color: C.muted}}>SERVICE REPLIES · THIS MONTH</div>
          <div style={{fontFamily: display, fontSize: 130, lineHeight: 1, marginTop: 12, color: over ? C.red : C.cream}}>{count.toLocaleString('en-US')}</div>
          <div style={{height: 14, borderRadius: 7, background: 'rgba(240,238,232,0.12)', position: 'relative', marginTop: 16}}>
            <div style={{position: 'absolute', left: 0, top: 0, bottom: 0, width: `${Math.min(100, (count / 1010) * 100)}%`, borderRadius: 7, background: over ? C.red : C.green}} />
            <div style={{position: 'absolute', left: `${(1000 / 1010) * 100}%`, top: -10, bottom: -10, width: 3, background: C.cream}} />
          </div>
          <div style={{display: 'flex', justifyContent: 'space-between', marginTop: 12, fontSize: 17, fontWeight: 700, color: C.muted}}>
            <span>1,000 FREE</span>
            <span style={{color: over ? C.red : C.muted}}>then billed per message</span>
          </div>
          <div style={{marginTop: 26}}>
            <Chip p={ip(cost, 0.4)} color={C.red} bg="rgba(255,90,90,0.12)" size={22}>$ EVERY REPLY AFTER 1,000</Chip>
          </div>
        </div>
        {week >= 0 ? (
          <div style={{position: 'absolute', left: 24, right: 24, top: 24, opacity: swap}}>
            <div style={{fontWeight: 800, fontSize: 17, letterSpacing: '0.14em', color: C.cyan}}>CHAT STARTED FROM AN AD</div>
            <div style={{fontFamily: display, fontSize: 104, lineHeight: 1, marginTop: 12, color: C.green}}>FREE WINDOW</div>
            <div style={{display: 'flex', gap: 8, marginTop: 18}}>
              {Array.from({length: 7}).map((_, i) => {
                const p = ip(week - 0.25 - i * 0.12, 0.25);
                return (
                  <div key={i} style={{flex: 1, height: 74, borderRadius: 12, background: p > 0.5 ? C.green : 'rgba(240,238,232,0.1)', color: C.bg, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: display, fontSize: 34, transform: `scale(${0.85 + 0.15 * p})`}}>
                    {i + 1}
                  </div>
                );
              })}
            </div>
            <div style={{marginTop: 14, fontWeight: 800, fontSize: 22, letterSpacing: '0.1em'}}>UP TO 7 DAYS</div>
          </div>
        ) : null}
      </div>
      <Translate s={sinceWord(t, 'three', 'days')} text="Start chats from ads → up to 7 days free." />
    </Panel>
  );
};

export const CtaRoom: React.FC<{t: number; start: number}> = ({t, start}) => {
  const q = sinceWord(t, 'cta', 'q4');
  const sent = sinceWord(t, 'cta', 'checklist');
  const typed = q < 0 ? '' : q < 0.15 ? 'Q' : 'Q4';
  const posted = ip(q - 0.55, 0.35);
  const enter = ip(t - start + 0.2, 0.5);
  return (
    <div style={{width: ROOM_W, height: ROOM_H, position: 'relative', fontFamily: body, color: C.cream, opacity: enter}}>
      <div style={{textAlign: 'center', fontFamily: display, lineHeight: 0.85, paddingTop: 40}}>
        <div style={{fontSize: 96}}>COMMENT</div>
        <div style={{fontSize: 290, color: C.gold, textShadow: '0 0 70px rgba(200,169,110,0.4)', transform: `scale(${1 + 0.08 * Math.max(0, 1 - Math.abs(q - 0.1) * 5)})`}}>Q4</div>
      </div>
      <div style={{position: 'absolute', left: 30, right: 30, bottom: 10, borderRadius: 28, background: 'rgba(17,24,39,0.95)', border: '1px solid rgba(240,238,232,0.14)', padding: 22, display: 'flex', flexDirection: 'column', gap: 16}}>
        {posted > 0 ? (
          <div style={{display: 'flex', gap: 14, alignItems: 'center', opacity: posted, transform: `translateY(${(1 - posted) * 16}px)`}}>
            <div style={{width: 46, height: 46, borderRadius: '50%', background: 'linear-gradient(135deg,#7A5CFF,#FF7A59)'}} />
            <div style={{fontSize: 24}}>
              <b>you</b> <span style={{color: C.gold, fontWeight: 800}}>Q4</span>
            </div>
            <div style={{marginLeft: 'auto', fontSize: 26, color: C.red}}>♥</div>
          </div>
        ) : null}
        {sent >= 0 ? (
          <div style={{display: 'flex', gap: 14, alignItems: 'center', marginLeft: 46, opacity: ip(sent, 0.35), transform: `translateY(${(1 - ip(sent, 0.35)) * 16}px)`}}>
            <div style={{width: 40, height: 40, borderRadius: '50%', background: C.gold, color: C.bg, fontFamily: display, fontSize: 26, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>A</div>
            <div style={{fontSize: 22, lineHeight: 1.25}}>
              <b>Aman Rai</b> <span style={{color: C.muted}}>· creator</span>
              <br />
              Sent! Checklist + every source → your DMs
            </div>
          </div>
        ) : null}
        <div style={{display: 'flex', alignItems: 'center', gap: 14, padding: '14px 18px', borderRadius: 999, border: '1px solid rgba(240,238,232,0.2)', opacity: posted > 0 ? 0.5 : 1}}>
          <div style={{fontSize: 24, color: typed && posted === 0 ? C.cream : C.muted, fontWeight: 600}}>
            {posted > 0 ? 'Add a comment…' : typed || 'Add a comment…'}
            {typed && posted === 0 && Math.floor(t * 4) % 2 ? '|' : ''}
          </div>
          <div style={{marginLeft: 'auto', fontWeight: 800, fontSize: 22, color: C.blueBright}}>Post</div>
        </div>
      </div>
    </div>
  );
};
