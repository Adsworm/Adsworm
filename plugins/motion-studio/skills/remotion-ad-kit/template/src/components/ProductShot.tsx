import {Img, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {springIn, springs} from '../lib/motion';

// Spring entrance + idle float + shadow that breathes with the float.
export const ProductShot: React.FC<{src: string; height: number; delay?: number}> = ({src, height, delay = 0}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const s = springIn(frame, fps, delay, springs.snappy);
  const float = Math.sin((frame - delay) / 18) * height * 0.012;
  return (
    <div style={{position: 'relative', height, display: 'flex', alignItems: 'flex-end', justifyContent: 'center'}}>
      <div
        style={{
          position: 'absolute',
          bottom: -height * 0.02,
          width: height * 0.42,
          height: height * 0.06,
          borderRadius: '50%',
          background: 'radial-gradient(closest-side, rgba(0,0,0,0.35), transparent)',
          transform: `scale(${(0.6 + s * 0.4) * (1 - float / height)})`,
          opacity: s,
        }}
      />
      <Img
        src={staticFile(src)}
        style={{
          height: height * 0.96,
          objectFit: 'contain',
          transform: `translateY(${(1 - s) * height * 0.25 + float}px) scale(${0.82 + s * 0.18}) rotate(${(1 - s) * -8}deg)`,
          opacity: Math.min(1, s * 1.4),
          filter: 'drop-shadow(0 30px 40px rgba(0,0,0,0.18))',
        }}
      />
    </div>
  );
};
