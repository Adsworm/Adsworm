import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import {body, display} from '../../lib/fonts';
import {ease, progress} from '../../lib/motion';
import {Skyline} from '../Skyline';
import {C} from '../theme';

// 20–24 s: the empire rises — 280+ brands. (The Perfect 5 branch beat waits until the owner
// confirms one branch count across adsworm.com / .in / Instagram — see brands/adsworm/claims.md.)
export const Proof: React.FC = () => {
  const frame = useCurrentFrame();
  const n = Math.round(interpolate(frame, [606, 650], [0, 280], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}));
  const p = progress(frame, 600, 10, ease.outExpo);
  const label = progress(frame, 612, 14, ease.outExpo);
  const done = frame >= 650;
  return (
    <AbsoluteFill>
      <div style={{position: 'absolute', top: 360, width: '100%', textAlign: 'center', fontFamily: display, fontSize: 290, lineHeight: 0.9, color: C.gold, opacity: p, transform: `scale(${done ? 1 + Math.max(0, 1 - (frame - 650) / 8) * 0.08 : 1})`, fontVariantNumeric: 'tabular-nums'}}>
        {n}
        <span style={{opacity: done ? 1 : 0}}>+</span>
      </div>
      <div style={{position: 'absolute', top: 640, width: '100%', textAlign: 'center', fontFamily: body, fontWeight: 600, fontSize: 40, letterSpacing: '0.2em', color: C.paper, opacity: label}}>
        BRANDS SCALED
      </div>
      <Skyline at={606} every={5} lit={progress(frame, 650, 20)} scale={0.85} />
    </AbsoluteFill>
  );
};
