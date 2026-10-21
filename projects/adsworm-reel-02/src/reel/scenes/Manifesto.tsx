import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import {ease, progress} from '../../lib/motion';
import {Headline} from '../Headline';
import {SAFE} from '../theme';

export const Manifesto: React.FC = () => {
  const frame = useCurrentFrame();
  const recede = progress(frame, 840, 12, ease.outExpo);
  return (
    <AbsoluteFill style={{top: SAFE.top, height: SAFE.bottom - SAFE.top, justifyContent: 'center', alignItems: 'center', gap: 36}}>
      <div style={{opacity: interpolate(recede, [0, 1], [1, 0.38]), transform: `scale(${interpolate(recede, [0, 1], [1, 0.82])})`}}>
        <Headline lines={["WE DON'T", 'RUN ADS.']} size={210} at={810} stagger={6} />
      </div>
      {frame >= 840 ? <Headline lines={['WE BUILD', '^EMPIRES.^']} size={235} at={840} stagger={7} /> : null}
    </AbsoluteFill>
  );
};
