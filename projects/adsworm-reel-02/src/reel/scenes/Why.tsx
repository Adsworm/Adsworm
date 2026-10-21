import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import {body, display} from '../../lib/fonts';
import {ease, progress} from '../../lib/motion';
import {Headline} from '../Headline';
import {C, SAFE} from '../theme';

const Line: React.FC<{at: number; text: string}> = ({at, text}) => {
  const p = progress(useCurrentFrame(), at, 16, ease.outExpo);
  return (
    <div style={{fontFamily: body, fontWeight: 500, fontSize: 54, color: C.paper, opacity: p * 0.85, transform: `translateY(${(1 - p) * 30}px)`, letterSpacing: '-0.01em'}}>
      {text}
    </div>
  );
};

export const Why: React.FC = () => {
  const frame = useCurrentFrame();
  if (frame < 180) {
    const shrink = progress(frame, 150, 14, ease.outExpo);
    const slam = progress(frame, 120, 8, ease.outExpo);
    return (
      <AbsoluteFill style={{top: SAFE.top, height: SAFE.bottom - SAFE.top, justifyContent: 'center', alignItems: 'center', gap: 30}}>
        <div
          style={{
            fontFamily: display,
            fontSize: 440,
            lineHeight: 0.85,
            color: C.paper,
            transform: `scale(${interpolate(shrink, [0, 1], [1, 0.5]) * (1 + (1 - slam) * 0.25)}) translateY(${shrink * -120}px)`,
            opacity: slam,
          }}
        >
          WHY?
        </div>
        {frame >= 150 ? (
          <div style={{marginTop: -260 * shrink}}>
            <Line at={150} text="Buyers can't judge quality upfront." />
          </div>
        ) : null}
      </AbsoluteFill>
    );
  }
  // "SIGNALS." gets a light sweep across the letters
  const sweep = interpolate(frame, [196, 226], [-60, 160], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{top: SAFE.top, height: SAFE.bottom - SAFE.top, justifyContent: 'center', alignItems: 'center', gap: 40}}>
      <div style={{fontFamily: body, fontWeight: 500, fontSize: 46, color: C.muted}}>Buyers can't judge quality upfront.</div>
      <Headline lines={['SO THEY JUDGE']} size={180} at={180} />
      <Headline lines={['*SIGNALS.*']} size={250} at={194} shine={sweep} />
    </AbsoluteFill>
  );
};
