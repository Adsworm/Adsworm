import {useCurrentFrame, useVideoConfig} from 'remotion';
import {sans} from '../lib/fonts';
import {springIn, springs} from '../lib/motion';

// Pop-in, then a gentle pulse and a shimmer pass every 1.5s to pull the eye to the action.
export const CTAButton: React.FC<{label: string; fontSize: number; bg: string; color: string; delay?: number}> = ({
  label,
  fontSize,
  bg,
  color,
  delay = 0,
}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const s = springIn(frame, fps, delay, springs.pop);
  const local = Math.max(0, frame - delay - 20);
  const pulse = 1 + Math.sin(local / 7) * 0.018 * Math.min(1, local / 15);
  const sweep = ((local % 45) / 45) * 260 - 80;
  return (
    <div
      style={{
        position: 'relative',
        overflow: 'hidden',
        display: 'inline-flex',
        alignItems: 'center',
        gap: fontSize * 0.5,
        padding: `${fontSize * 0.7}px ${fontSize * 1.4}px`,
        borderRadius: 999,
        background: bg,
        color,
        fontFamily: sans,
        fontWeight: 700,
        fontSize,
        letterSpacing: '-0.01em',
        transform: `scale(${s * pulse})`,
        boxShadow: `0 ${fontSize * 0.4}px ${fontSize * 1.2}px rgba(0,0,0,0.25)`,
      }}
    >
      {label}
      <span style={{fontSize: fontSize * 0.9}}>→</span>
      <div
        style={{
          position: 'absolute',
          inset: 0,
          background: 'linear-gradient(100deg, transparent 30%, rgba(255,255,255,0.45) 50%, transparent 70%)',
          transform: `translateX(${sweep}%)`,
        }}
      />
    </div>
  );
};
