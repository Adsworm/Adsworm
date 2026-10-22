import {body} from '../lib/fonts';
import {C, L} from './theme';
import type {Line} from './tl';

// Word-by-word captions. Aman: cream with gold keywords. THE ALGORITHM: uppercase, cyan keywords.
// The speaker tag tells you who's talking without a second avatar.
export const Captions: React.FC<{line: Line; t: number; fps: number}> = ({line, t, fps}) => {
  const algo = line.who === 'ALGO';
  const accent = algo ? C.cyan : C.goldBright;
  const lineIn = Math.min(1, Math.max(0, (t - line.start + 0.12) * fps) / 5);
  return (
    <div style={{position: 'absolute', left: (1080 - L.caption.w) / 2, top: L.caption.y, width: L.caption.w, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 14, fontFamily: body}}>
      <div style={{display: 'flex', alignItems: 'center', gap: 10, padding: '6px 16px', borderRadius: 999, background: algo ? 'rgba(95,225,255,0.12)' : 'rgba(200,169,110,0.14)', border: `1px solid ${algo ? 'rgba(95,225,255,0.4)' : 'rgba(200,169,110,0.45)'}`, opacity: lineIn, transform: `translateY(${(1 - lineIn) * 8}px)`}}>
        <div style={{width: 10, height: 10, borderRadius: '50%', background: accent, boxShadow: `0 0 12px ${accent}`}} />
        <div style={{fontWeight: 800, fontSize: 22, letterSpacing: '0.16em', color: accent}}>{algo ? 'THE ALGORITHM' : 'AMAN RAI'}</div>
      </div>
      <div style={{textAlign: 'center', fontWeight: 800, fontSize: algo ? 54 : 56, lineHeight: 1.12, letterSpacing: algo ? '0.01em' : '-0.015em', textTransform: algo ? 'uppercase' : 'none', textShadow: '0 4px 24px rgba(0,0,0,0.7)'}}>
        {line.words.map((w, i) => {
          const p = Math.min(1, Math.max(0, (t - w.s + 0.06) * fps) / 4);
          const live = t >= w.s - 0.06 && t < w.e + 0.08;
          return (
            <span key={i} style={{display: 'inline-block', marginRight: '0.26em', color: w.hi ? accent : C.cream, opacity: 0.18 + 0.82 * p, transform: `translateY(${(1 - p) * 10}px) scale(${live && w.hi ? 1.06 : 1})`}}>
              {w.w}
            </span>
          );
        })}
      </div>
    </div>
  );
};
