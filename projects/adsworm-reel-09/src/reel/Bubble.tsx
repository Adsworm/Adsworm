import {spring} from 'remotion';
import {body} from '../lib/fonts';
import {C, V3} from './theme';

export type Token = {w: string; t: number; pill: boolean};
// Karaoke speech bubble: 2–4 words at a time, the word being said lights up, words not yet said are
// grey. The tail points at whoever is talking; nothing to read ahead, you hear and see the same word.
const chunk = (tokens: Token[]) => {
  const out: Token[][] = [];
  let cur: Token[] = [];
  tokens.forEach((tok) => {
    cur.push(tok);
    const end = /[.!?,…:]$/.test(tok.w) || /^\[/.test(tok.w);
    if (cur.length >= 4 || (end && cur.length >= 2)) {
      out.push(cur);
      cur = [];
    }
  });
  if (cur.length) out.length && cur.length === 1 ? out[out.length - 1].push(...cur) : out.push(cur);
  return out;
};

export const Bubble: React.FC<{tokens: Token[]; who: string; name: string; side: 'left' | 'right'; t: number; fps: number}> = ({tokens, who, name, side, t, fps}) => {
  const chunks = chunk(tokens);
  const ci = Math.max(0, chunks.reduce((acc, c, i) => (c[0].t - 0.04 <= t ? i : acc), 0));
  const c = chunks[ci];
  const s = spring({frame: Math.round((t - c[0].t + 0.04) * fps), fps, config: {damping: 14, stiffness: 260, mass: 0.6}});
  const accent = who === 'AMAN' ? C.blue : V3.pink;
  const live = c.reduce((acc, tok, i) => (tok.t - 0.03 <= t ? i : acc), -1);
  const w = V3.bubble.w;
  const left = (1080 - w) / 2;
  return (
    <div style={{position: 'absolute', left, top: V3.bubble.y, width: w, fontFamily: body}}>
      <div style={{display: 'inline-block', marginLeft: side === 'left' ? 30 : w - 450, width: 420, textAlign: side === 'left' ? 'left' : 'right'}}>
        <span style={{display: 'inline-block', padding: '6px 16px', borderRadius: 999, background: accent, color: '#fff', fontWeight: 800, fontSize: 22, letterSpacing: '0.12em', border: V3.outline, whiteSpace: 'nowrap'}}>{name}</span>
      </div>
      <div style={{position: 'relative', marginTop: 8, background: '#fff', border: V3.outline, borderRadius: 32, boxShadow: V3.shadow, padding: '26px 34px', minHeight: 96, display: 'flex', flexWrap: 'wrap', justifyContent: 'center', alignItems: 'center', gap: '6px 14px', transform: `scale(${0.92 + 0.08 * s})`, transformOrigin: side === 'left' ? '20% 100%' : '80% 100%'}}>
        {c.map((tok, i) => {
          const said = i <= live;
          const now = i === live;
          return (
            <span key={`${ci}-${i}`} style={{fontWeight: 800, fontSize: 64, lineHeight: 1.08, letterSpacing: '-0.02em', color: tok.pill && said ? '#fff' : said ? C.ink : '#B4B9C4', background: tok.pill && said ? accent : 'transparent', borderRadius: 14, padding: tok.pill && said ? '2px 12px' : '2px 0', transform: `scale(${now ? 1.06 : 1})`, display: 'inline-block'}}>
              {tok.w}
            </span>
          );
        })}
        <div style={{position: 'absolute', bottom: -26, [side === 'left' ? 'left' : 'right']: 150, width: 0, height: 0, borderLeft: '20px solid transparent', borderRight: '20px solid transparent', borderTop: `26px solid #0D1320`}} />
        <div style={{position: 'absolute', bottom: -19, [side === 'left' ? 'left' : 'right']: 154, width: 0, height: 0, borderLeft: '16px solid transparent', borderRight: '16px solid transparent', borderTop: '21px solid #fff'}} />
      </div>
    </div>
  );
};
