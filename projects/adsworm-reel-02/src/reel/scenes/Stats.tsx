import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import {body, display} from '../../lib/fonts';
import {ease, progress} from '../../lib/motion';
import {Headline} from '../Headline';
import {Skyline} from '../Skyline';
import {C} from '../theme';

// 24–27 s: retention + reach, with the risen skyline holding underneath.
export const Stats: React.FC = () => {
  const frame = useCurrentFrame();
  const p = progress(frame, 720, 9, ease.outExpo);
  const n = Math.round(interpolate(frame, [720, 736], [0, 98], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}));
  return (
    <AbsoluteFill>
      <Skyline at={-100} lit={1} dim={0.3} scale={0.6} />
      <div style={{position: 'absolute', top: 330, width: '100%', textAlign: 'center', fontFamily: display, fontSize: 250, lineHeight: 0.9, color: C.gold, opacity: p, transform: `scale(${1 + (1 - p) * 0.2})`, fontVariantNumeric: 'tabular-nums'}}>
        {n}%
      </div>
      <div style={{position: 'absolute', top: 570, width: '100%', textAlign: 'center', fontFamily: body, fontWeight: 600, fontSize: 40, letterSpacing: '0.2em', color: C.paper, opacity: p}}>
        CLIENT RETENTION
      </div>
      <div style={{position: 'absolute', top: 680, width: '100%', display: 'flex', justifyContent: 'center'}}>
        {frame >= 750 ? <Headline lines={['INDIA · UK · UAE']} size={130} at={750} stagger={6} /> : null}
      </div>
    </AbsoluteFill>
  );
};
