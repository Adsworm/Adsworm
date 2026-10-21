import {useCurrentFrame} from 'remotion';
import {ease, progress} from '../lib/motion';
import {LOGO_PATH, LOGO_VIEWBOX} from './logo-path';
import {C} from './theme';

// Filled mark revealed by a left-to-right wipe. Brand rule: never shown as an outline.
export const LogoWipe: React.FC<{at: number; width: number; color?: string}> = ({at, width, color = C.paper}) => {
  const p = progress(useCurrentFrame(), at, 15, ease.outExpo);
  return (
    <svg width={width} viewBox={LOGO_VIEWBOX} style={{display: 'block', clipPath: `inset(0 ${(1 - p) * 100}% 0 0)`, transform: `translateX(${(1 - p) * -24}px)`}}>
      <path d={LOGO_PATH} fill={color} />
    </svg>
  );
};
