import {AbsoluteFill, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {body, display} from '../../lib/fonts';
import {ease, progress, springs} from '../../lib/motion';
import {LogoWipe} from '../LogoWipe';
import {C} from '../theme';
import {HookStill} from './Hook';

export const End: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const handle = progress(frame, 908, 14, ease.outExpo);
  const cta = spring({frame: frame - 915, fps, config: springs.pop});
  const sub = progress(frame, 925, 16, ease.outExpo);
  const loop = progress(frame, 1012, 8); // the last 8 frames return to frame 0 so the reel loops
  return (
    <AbsoluteFill>
      <div style={{position: 'absolute', top: 400, width: '100%', display: 'flex', justifyContent: 'center'}}>
        <LogoWipe at={900} width={430} />
      </div>
      <div style={{position: 'absolute', top: 720, width: '100%', textAlign: 'center', fontFamily: body, fontWeight: 600, fontSize: 52, color: C.paper, opacity: handle}}>@adsworm</div>
      <div style={{position: 'absolute', top: 820, width: '100%', display: 'flex', justifyContent: 'center'}}>
        <div style={{padding: '22px 48px 14px', borderRadius: 999, background: C.gold, color: C.bg, fontFamily: display, fontSize: 92, lineHeight: 1, letterSpacing: '0.02em', transform: `scale(${cta})`}}>
          COMMENT “EMPIRE”
        </div>
      </div>
      <div style={{position: 'absolute', top: 975, width: '100%', textAlign: 'center', fontFamily: body, fontWeight: 600, fontSize: 40, color: C.paper, opacity: sub}}>
        We'll audit your 3 signals. Free.
      </div>
      {loop > 0 ? (
        <AbsoluteFill style={{background: C.bg, opacity: loop}}>
          <HookStill />
        </AbsoluteFill>
      ) : null}
    </AbsoluteFill>
  );
};
