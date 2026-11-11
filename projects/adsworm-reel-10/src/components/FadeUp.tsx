import {useCurrentFrame} from 'remotion';
import {ease, progress} from '../lib/motion';

export const FadeUp: React.FC<{delay?: number; distance?: number; children: React.ReactNode; style?: React.CSSProperties}> = ({
  delay = 0,
  distance = 40,
  children,
  style,
}) => {
  const p = progress(useCurrentFrame(), delay, 24, ease.outExpo);
  return <div style={{opacity: p, transform: `translateY(${(1 - p) * distance}px)`, ...style}}>{children}</div>;
};
