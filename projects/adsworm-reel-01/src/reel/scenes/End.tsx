import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {progress} from '../../lib/motion';
import {LogoDraw} from '../LogoDraw';
import {C} from '../theme';
import {Words} from '../Words';
import {HookStill} from './Hook';

export const End: React.FC = () => {
  const frame = useCurrentFrame();
  const loop = progress(frame, 1012, 8); // last 8 frames return to frame 0 so the reel loops
  return (
    <AbsoluteFill>
      <div style={{position: 'absolute', top: 440, width: '100%', display: 'flex', justifyContent: 'center'}}>
        <LogoDraw at={960} width={540} />
      </div>
      <div style={{position: 'absolute', top: 900, width: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 22}}>
        <Words text="@adsworm" size={66} at={975} />
        <Words text="The clinic growth agency" size={46} at={985} color={C.muted} weight={600} />
        <div style={{opacity: 0.7}}>
          <Words text="Made 100% in code." size={32} at={995} color={C.muted} weight={500} />
        </div>
      </div>
      {loop > 0 ? (
        <AbsoluteFill style={{background: C.ink, opacity: loop}}>
          <HookStill />
        </AbsoluteFill>
      ) : null}
    </AbsoluteFill>
  );
};
