import {useCurrentFrame} from 'remotion';
import {sans, serif} from '../lib/fonts';
import {ease, progress} from '../lib/motion';
import {C} from './theme';

type Word = {text: string; kind: 'plain' | 'lime' | 'serif'};

// "*word*" → lime grotesk, "~word~" → lime serif italic.
const parse = (text: string): Word[] =>
  text
    .split(/(\*[^*]+\*|~[^~]+~)/)
    .filter(Boolean)
    .flatMap((seg) => {
      const kind: Word['kind'] = seg.startsWith('*') ? 'lime' : seg.startsWith('~') ? 'serif' : 'plain';
      return seg
        .replace(/[*~]/g, '')
        .trim()
        .split(/\s+/)
        .filter(Boolean)
        .map((w) => ({text: w, kind}));
    });

// Words rise out of their own line box. `at` is the absolute frame the first word starts;
// with `set` the block renders fully set from the first frame (the frame-0 hook).
export const Words: React.FC<{
  text: string;
  size: number;
  at: number;
  color?: string;
  stagger?: number;
  set?: boolean;
  weight?: number;
  align?: 'center' | 'left';
  maxWidth?: number;
}> = ({text, size, at, color = C.paper, stagger = 3, set = false, weight = 800, align = 'center', maxWidth = 950}) => {
  const frame = useCurrentFrame();
  return (
    <div style={{display: 'flex', flexWrap: 'wrap', justifyContent: align === 'center' ? 'center' : 'flex-start', columnGap: size * 0.24, maxWidth}}>
      {parse(text).map((w, i) => {
        const p = set ? 1 : progress(frame, at + i * stagger, 18, ease.outExpo);
        const serifWord = w.kind === 'serif';
        return (
          <span key={i} style={{display: 'inline-block', overflow: 'hidden', padding: `${size * 0.1}px 0`}}>
            <span
              style={{
                display: 'inline-block',
                transform: `translateY(${(1 - p) * 110}%)`,
                opacity: Math.min(1, p * 1.5),
                fontFamily: serifWord ? serif : sans,
                fontStyle: serifWord ? 'italic' : 'normal',
                fontWeight: serifWord ? 400 : weight,
                fontSize: serifWord ? size * 1.12 : size,
                letterSpacing: serifWord ? '-0.01em' : '-0.045em',
                lineHeight: 1,
                color: w.kind === 'plain' ? color : C.lime,
              }}
            >
              {w.text}
            </span>
          </span>
        );
      })}
    </div>
  );
};
