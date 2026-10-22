import {AbsoluteFill} from 'remotion';
import {body} from '../lib/fonts';
import {C, PLATFORM} from './theme';

// Cream paper with a faint dot grid, and the blue platform the characters stand on.
export const Stage: React.FC<{footer: string}> = ({footer}) => (
  <AbsoluteFill style={{background: C.bg}}>
    <AbsoluteFill style={{backgroundImage: `radial-gradient(circle, rgba(13,19,32,0.07) 1.5px, transparent 2px)`, backgroundSize: '28px 28px', opacity: 0.9}} />
    <AbsoluteFill style={{background: `linear-gradient(180deg, rgba(27,94,247,0) 60%, rgba(27,94,247,0.10) 100%)`}} />
    {/* platform */}
    <div style={{position: 'absolute', left: -60, right: -60, top: PLATFORM.y, height: 400, borderRadius: '50% 50% 0 0 / 120px 120px 0 0', background: `linear-gradient(180deg, ${C.blueBright}, ${C.blue})`}} />
    <div style={{position: 'absolute', left: 240, right: 240, top: PLATFORM.y + 100, height: 90, borderRadius: '50%', background: 'rgba(13,19,32,0.25)', filter: 'blur(26px)'}} />
    <div style={{position: 'absolute', left: 0, right: 0, top: PLATFORM.y + 115, textAlign: 'center', fontFamily: body, fontWeight: 600, fontSize: 30, color: 'rgba(255,255,255,0.92)', letterSpacing: '0.02em'}}>{footer}</div>
  </AbsoluteFill>
);
