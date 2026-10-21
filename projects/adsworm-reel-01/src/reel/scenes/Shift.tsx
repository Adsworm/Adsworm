import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import {progress} from '../../lib/motion';
import {SAFE} from '../theme';
import {Words} from '../Words';

export const Shift: React.FC = () => {
  const frame = useCurrentFrame();
  const dim = interpolate(progress(frame, 360, 12), [0, 1], [1, 0.35]);
  return (
    <AbsoluteFill style={{top: SAFE.top, height: SAFE.bottom - SAFE.top, justifyContent: 'center', alignItems: 'center', gap: 40}}>
      <div style={{opacity: dim}}>
        <Words text="Patients don't book discounts." size={104} at={300} stagger={4} />
      </div>
      {frame >= 360 ? <Words text="They book ~certainty.~" size={116} at={360} stagger={5} /> : null}
    </AbsoluteFill>
  );
};
