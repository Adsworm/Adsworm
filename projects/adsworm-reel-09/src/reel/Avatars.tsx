import {Img, interpolate, staticFile, useCurrentFrame} from 'remotion';
import {AVATARS} from './avatars';
import {C, FEET} from './theme';

export type Pose = 'idle' | 'point' | 'palms' | 'ask' | 'wow' | 'thumbs' | 'think';

// A character on the platform: generated 3D-style PNG per pose (public/avatars/<who>-<pose>.png),
// idle bob, a small lean + scale pulse while talking, 6-frame crossfade on pose change.
export const Avatar: React.FC<{who: string; x: number; height: number; pose: Pose; talking: boolean; flip?: boolean; since: number}> = ({who, x, height, pose, talking, flip = false, since}) => {
  const frame = useCurrentFrame();
  const files = AVATARS[who.toLowerCase()] ?? {};
  const bob = Math.sin((frame / 30) * 2.6 + (flip ? 1.7 : 0)) * 5;
  const pulse = talking ? 1 + Math.sin(frame / 2.2) * 0.008 : 1;
  const lean = talking ? (flip ? 2 : -2) : 0;
  const fade = interpolate(frame - since, [0, 6], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const file = files[pose] ?? files.idle;
  const prev = files.idle;
  const w = height * 0.62;
  return (
    <div style={{position: 'absolute', left: x - w / 2, top: FEET - height + bob, width: w, height, transform: `scale(${flip ? -1 : 1}, 1) scale(${pulse}) rotate(${lean}deg)`, transformOrigin: 'bottom center'}}>
      <div style={{position: 'absolute', left: '15%', right: '15%', bottom: -14, height: 28, borderRadius: '50%', background: 'rgba(13,19,32,0.28)', filter: 'blur(8px)'}} />
      {file ? (
        <>
          {prev && prev !== file && fade < 1 ? <Img src={staticFile(prev)} style={{position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'contain', objectPosition: 'bottom', opacity: 1 - fade}} /> : null}
          <Img src={staticFile(file)} style={{position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'contain', objectPosition: 'bottom', opacity: prev && prev !== file ? fade : 1}} />
        </>
      ) : (
        <Silhouette w={w} h={height} />
      )}
    </div>
  );
};

// Placeholder while the generated avatars aren't in public/avatars yet.
const Silhouette: React.FC<{w: number; h: number}> = ({w, h}) => (
  <svg width={w} height={h} viewBox="0 0 100 160" style={{position: 'absolute', inset: 0}}>
    <circle cx={50} cy={28} r={22} fill={C.ink} />
    <rect x={22} y={56} width={56} height={62} rx={18} fill={C.blue} />
    <rect x={30} y={112} width={16} height={44} rx={8} fill={C.ink} />
    <rect x={54} y={112} width={16} height={44} rx={8} fill={C.ink} />
  </svg>
);
