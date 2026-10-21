import {useCurrentFrame} from 'remotion';
import {display} from '../lib/fonts';
import {ease, progress} from '../lib/motion';
import {C} from './theme';

type Tok = {text: string; color: string};
// "*word*" → electric blue, "^word^" → gold, plain → cream.
const tokens = (line: string): Tok[] =>
  line
    .split(/(\*[^*]+\*|\^[^^]+\^)/)
    .filter(Boolean)
    .flatMap((seg) => {
      const color = seg.startsWith('*') ? C.blue : seg.startsWith('^') ? C.gold : C.paper;
      return seg.replace(/[*^]/g, '').trim().split(/\s+/).filter(Boolean).map((text) => ({text, color}));
    });

// Bebas caps that slam in word by word (one word per `stagger` frames, from `at`), each line on its own row.
// With `set` every word is already landed — used for frame 0.
export const Headline: React.FC<{lines: string[]; size: number; at: number; stagger?: number; set?: boolean; lineGap?: number; color?: string; shine?: number}> = ({
  lines,
  size,
  at,
  stagger = 8,
  set = false,
  lineGap = 0.02,
  color,
  shine,
}) => {
  const frame = useCurrentFrame();
  let n = 0;
  return (
    <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center', gap: size * lineGap}}>
      {lines.map((line, li) => (
        <div key={li} style={{display: 'flex', gap: size * 0.2}}>
          {tokens(line).map((tok, wi) => {
            const p = set ? 1 : progress(frame, at + n++ * stagger, 9, ease.outExpo);
            return (
              <span key={wi} style={{display: 'inline-block', overflow: 'hidden', paddingTop: size * 0.04}}>
                <span
                  style={{
                    display: 'inline-block',
                    fontFamily: display,
                    fontSize: size,
                    lineHeight: 0.9,
                    letterSpacing: '0.005em',
                    color: color ?? tok.color,
                    // `shine` (0–100) runs a light sweep through blue words via background-clip text
                    ...(shine !== undefined && tok.color === C.blue
                      ? {
                          color: 'transparent',
                          backgroundImage: `linear-gradient(100deg, ${C.blue} ${shine - 14}%, #B9CCFF ${shine}%, ${C.blue} ${shine + 14}%)`,
                          WebkitBackgroundClip: 'text',
                          backgroundClip: 'text',
                        }
                      : {}),
                    transform: `translateY(${(1 - p) * 105}%) scale(${1 + (1 - p) * 0.12})`,
                    filter: `blur(${(1 - p) * 6}px)`,
                  }}
                >
                  {tok.text}
                </span>
              </span>
            );
          })}
        </div>
      ))}
    </div>
  );
};
