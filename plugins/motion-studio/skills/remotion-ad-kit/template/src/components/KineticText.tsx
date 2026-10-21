import {useCurrentFrame} from 'remotion';
import {sans, serif} from '../lib/fonts';
import {ease, progress} from '../lib/motion';

type Word = {text: string; accent: boolean};

// "Plain *accent words* plain" → words flagged for the serif-italic accent treatment.
const parse = (text: string): Word[] =>
  text
    .split(/(\*[^*]+\*)/)
    .filter(Boolean)
    .flatMap((seg) => {
      const accent = seg.startsWith('*') && seg.endsWith('*');
      return seg
        .replace(/\*/g, '')
        .trim()
        .split(/\s+/)
        .filter(Boolean)
        .map((w) => ({text: w, accent}));
    });

export const KineticText: React.FC<{
  text: string;
  fontSize: number;
  color: string;
  accentColor: string;
  delay?: number;
  stagger?: number;
  weight?: number;
  align?: 'center' | 'left';
}> = ({text, fontSize, color, accentColor, delay = 0, stagger = 4, weight = 800, align = 'center'}) => {
  const frame = useCurrentFrame();
  return (
    <div
      style={{
        display: 'flex',
        flexWrap: 'wrap',
        justifyContent: align === 'center' ? 'center' : 'flex-start',
        columnGap: fontSize * 0.24,
        rowGap: fontSize * 0.02,
        textAlign: align,
      }}
    >
      {parse(text).map((w, i) => {
        const p = progress(frame, delay + i * stagger, 22, ease.outExpo);
        return (
          // Mask: the word rises out of its own line box.
          <span key={i} style={{display: 'inline-block', overflow: 'hidden', padding: `${fontSize * 0.08}px 0`}}>
            <span
              style={{
                display: 'inline-block',
                transform: `translateY(${(1 - p) * 110}%) rotate(${(1 - p) * 4}deg)`,
                filter: `blur(${(1 - p) * 10}px)`,
                opacity: Math.min(1, p * 1.6),
                fontFamily: w.accent ? serif : sans,
                fontStyle: w.accent ? 'italic' : 'normal',
                fontWeight: w.accent ? 400 : weight,
                fontSize: w.accent ? fontSize * 1.08 : fontSize,
                letterSpacing: w.accent ? '-0.01em' : '-0.045em',
                lineHeight: 1,
                color: w.accent ? accentColor : color,
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
