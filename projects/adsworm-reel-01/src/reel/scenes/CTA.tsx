import {AbsoluteFill, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {sans} from '../../lib/fonts';
import {progress, springs} from '../../lib/motion';
import {CommentField} from '../CommentField';
import {C, SAFE} from '../theme';
import {Words} from '../Words';

export const CTA: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  if (frame < 840) {
    return (
      <AbsoluteFill style={{top: SAFE.top, height: SAFE.bottom - SAFE.top, justifyContent: 'center', alignItems: 'center'}}>
        <Words text="Want us to check *your ads?*" size={108} at={780} stagger={4} />
      </AbsoluteFill>
    );
  }
  const pop = spring({frame: frame - 840, fps, config: springs.pop}); // one pop, no pulse (house rule)
  const sub = progress(frame, 885, 18);
  return (
    <AbsoluteFill>
      {/* Column layout: the headline can never overlap the subline, whatever the copy length. */}
      <div style={{position: 'absolute', top: 440, width: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 34}}>
        <div style={{transform: `scale(${0.6 + pop * 0.4})`, opacity: Math.min(1, pop * 1.5)}}>
          <Words text="Comment *AUDIT*" size={116} at={840} set maxWidth={1000} />
        </div>
        <div style={{fontFamily: sans, fontWeight: 600, fontSize: 42, color: C.muted, opacity: sub, transform: `translateY(${(1 - sub) * 20}px)`}}>
          Free 20-min teardown · Clinic owners only
        </div>
      </div>
      <div style={{position: 'absolute', top: 880, width: '100%', display: 'flex', justifyContent: 'center'}}>
        <CommentField text="AUDIT" at={850} sendAt={876} />
      </div>
    </AbsoluteFill>
  );
};
