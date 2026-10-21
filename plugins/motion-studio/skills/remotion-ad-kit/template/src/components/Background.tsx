import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {alpha} from '../lib/motion';

// Two slow-drifting glows over the paper tone. Deterministic: driven by frame only.
export const Background: React.FC<{paper: string; primary: string; accent: string}> = ({paper, primary, accent}) => {
  const t = useCurrentFrame() / 30;
  const a = {x: 28 + Math.sin(t * 0.5) * 8, y: 22 + Math.cos(t * 0.4) * 6};
  const b = {x: 74 + Math.cos(t * 0.45) * 8, y: 78 + Math.sin(t * 0.35) * 6};
  return (
    <AbsoluteFill
      style={{
        backgroundColor: paper,
        backgroundImage: [
          `radial-gradient(55% 40% at ${a.x}% ${a.y}%, ${alpha(accent, 30)}, transparent 70%)`,
          `radial-gradient(60% 45% at ${b.x}% ${b.y}%, ${alpha(primary, 18)}, transparent 70%)`,
        ].join(', '),
      }}
    />
  );
};
