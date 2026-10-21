import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import {ease, progress} from '../../lib/motion';
import {Headline} from '../Headline';
import {C, SAFE} from '../theme';

// 14–18 s payoff (the open loop closes here), then the 18–20 s bridge into Adsworm.
export const Lesson: React.FC = () => {
  const frame = useCurrentFrame();
  if (frame >= 540) {
    return (
      <AbsoluteFill style={{top: SAFE.top, height: SAFE.bottom - SAFE.top, justifyContent: 'center', alignItems: 'center'}}>
        <Headline lines={['WE ENGINEER', 'ALL *THREE.*']} size={185} at={540} stagger={7} />
      </AbsoluteFill>
    );
  }
  const recede = progress(frame, 465, 12, ease.outExpo);
  return (
    <AbsoluteFill style={{top: SAFE.top, height: SAFE.bottom - SAFE.top, justifyContent: 'center', alignItems: 'center', gap: 46}}>
      <div style={{opacity: interpolate(recede, [0, 1], [1, 0.4]), transform: `scale(${interpolate(recede, [0, 1], [1, 0.88])})`}}>
        <Headline lines={['QUALITY GETS YOU', 'CONSIDERED.']} size={140} at={420} stagger={6} color={C.paper} />
      </div>
      {frame >= 465 ? <Headline lines={['TRUST GETS YOU', '*CHOSEN.*']} size={170} at={465} stagger={7} /> : null}
    </AbsoluteFill>
  );
};
