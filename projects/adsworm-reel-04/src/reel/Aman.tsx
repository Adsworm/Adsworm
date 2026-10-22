import {Img, staticFile} from 'remotion';
import {AVATARS} from './avatars';
import {L} from './theme';

export type Pose = 'idle' | 'point' | 'palms';
// Face-matched 3D Aman (brands/adsworm/avatar-refs/aman-3d-sheet-v2.png, keyed by scripts/avatars.py).
// `enter` 0..1 slides him in from the left; `talk` (loudness) drives a small bob; a pose change pops.
export const Aman: React.FC<{pose: Pose; talk: number; enter: number; sincePose: number}> = ({pose, talk, enter, sincePose}) => {
  const {x, h, feet} = L.aman;
  const w = (h * 793) / 1467;
  const pop = sincePose >= 0 && sincePose < 6 ? 1 + 0.025 * Math.sin((sincePose / 6) * Math.PI) : 1;
  return (
    <div style={{position: 'absolute', left: x + (enter - 1) * (w + 60), top: feet - h, width: w, height: h, opacity: Math.min(1, enter * 1.5)}}>
      <div style={{position: 'absolute', left: '10%', right: '10%', bottom: 18, height: 40, borderRadius: '50%', background: 'radial-gradient(rgba(0,0,0,0.55), transparent 70%)'}} />
      <Img
        src={staticFile(AVATARS.aman[pose] ?? AVATARS.aman.idle!)}
        style={{
          width: '100%',
          height: '100%',
          transformOrigin: '50% 100%',
          transform: `translateY(${-talk * 9}px) rotate(${talk * 1.2}deg) scale(${pop})`,
          filter: 'drop-shadow(0 0 28px rgba(43,123,255,0.35)) drop-shadow(0 10px 30px rgba(0,0,0,0.5))',
        }}
      />
    </div>
  );
};
