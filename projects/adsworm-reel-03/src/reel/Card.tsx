import {spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {body} from '../lib/fonts';
import {springs} from '../lib/motion';
import {C, CARD} from './theme';

// The "receipt" card: section label + tag on top, source line at the bottom, builders in between.
export const Card: React.FC<{label: string; tag: string; source: string; sectionStartF: number; children: React.ReactNode}> = ({label, tag, source, sectionStartF, children}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const s = spring({frame: frame - sectionStartF, fps, config: springs.smooth});
  return (
    <div style={{position: 'absolute', left: CARD.x, top: CARD.y, width: CARD.w, height: CARD.h, borderRadius: CARD.r, background: C.card, boxShadow: '0 24px 70px rgba(13,19,32,0.12)', overflow: 'hidden', fontFamily: body}}>
      <div style={{position: 'absolute', inset: 0, backgroundImage: 'radial-gradient(circle, rgba(13,19,32,0.045) 1.2px, transparent 1.8px)', backgroundSize: '22px 22px'}} />
      <div style={{position: 'absolute', left: CARD.pad, right: CARD.pad, top: 34, display: 'flex', justifyContent: 'space-between', alignItems: 'center', opacity: s}}>
        <div style={{display: 'flex', alignItems: 'center', gap: 12, fontSize: 26, fontWeight: 800, letterSpacing: '0.12em', color: C.blue}}>
          {label ? <span style={{width: 12, height: 12, borderRadius: '50%', background: C.green, display: 'inline-block'}} /> : null}
          {label}
        </div>
        <div style={{fontSize: 22, fontWeight: 600, color: C.muted, letterSpacing: '0.04em'}}>{tag}</div>
      </div>
      <div style={{position: 'absolute', left: CARD.pad, right: CARD.pad, top: 100, bottom: 80}}>{children}</div>
      <div style={{position: 'absolute', left: CARD.pad, bottom: 28, fontSize: 20, color: C.muted, opacity: s * 0.9}}>{source}</div>
    </div>
  );
};

// Frames since a beat started (−1 if it hasn't). Builders use this for their reveal.
export const useBeat = (beats: Record<string, number>, id: string) => {
  const frame = useCurrentFrame();
  const at = beats[id];
  return at === undefined || frame < at ? -1 : frame - at;
};

export const Rise: React.FC<{t: number; delay?: number; children: React.ReactNode; style?: React.CSSProperties}> = ({t, delay = 0, children, style}) => {
  const {fps} = useVideoConfig();
  if (t < 0) return null;
  const s = spring({frame: t - delay, fps, config: springs.snappy});
  return <div style={{opacity: Math.min(1, s * 1.3), transform: `translateY(${(1 - s) * 30}px) scale(${0.94 + s * 0.06})`, ...style}}>{children}</div>;
};
