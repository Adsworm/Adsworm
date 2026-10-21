import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import {C} from './theme';

// The world every scene sits in: navy-black ground, a slow electric-blue light beam, and a
// perspective grid floor receding to the horizon. `flare` (0–1) opens the beam up for big moments.
export const Stage: React.FC<{flare?: number; dim?: number; gridGlow?: number}> = ({flare = 0, dim = 0, gridGlow = 0}) => {
  const f = useCurrentFrame();
  const sweep = Math.sin(f / 70) * 9 - 14; // degrees
  const drift = (f * 1.4) % 120; // grid moves toward camera
  const beam = 0.22 + flare * 0.35;
  return (
    <AbsoluteFill style={{background: `radial-gradient(110% 65% at 50% 42%, ${C.bg2} 0%, ${C.bg} 70%)`}}>
      <AbsoluteFill style={{opacity: 1 - dim * 0.7}}>
        {/* light beam */}
        <div
          style={{
            position: 'absolute',
            left: -400,
            top: -300,
            width: 1900,
            height: 900,
            transform: `rotate(${sweep}deg) translateX(${Math.sin(f / 90) * 80}px)`,
            transformOrigin: '50% 0%',
            background: `linear-gradient(90deg, transparent 30%, rgba(27,94,247,${beam}) 50%, transparent 70%)`,
            filter: 'blur(60px)',
          }}
        />
        <div
          style={{
            position: 'absolute',
            inset: 0,
            background: `radial-gradient(45% 22% at 50% 44%, rgba(27,94,247,${0.1 + flare * 0.18}), transparent 70%)`,
          }}
        />
        {/* perspective grid floor */}
        <div style={{position: 'absolute', left: 0, right: 0, top: 1180, height: 740, perspective: 600, overflow: 'hidden'}}>
          <div
            style={{
              position: 'absolute',
              left: -900,
              right: -900,
              top: 0,
              height: 2200,
              transform: `rotateX(72deg) translateY(${-drift}px)`,
              transformOrigin: '50% 0%',
              backgroundImage: `linear-gradient(rgba(43,123,255,${0.12 + gridGlow * 0.33}) 2px, transparent 2px), linear-gradient(90deg, rgba(43,123,255,${0.12 + gridGlow * 0.33}) 2px, transparent 2px)`,
              backgroundSize: '120px 120px',
              maskImage: 'linear-gradient(to bottom, transparent 0%, black 18%, black 60%, transparent 100%)',
            }}
          />
        </div>
        <div style={{position: 'absolute', left: 0, right: 0, top: 1176, height: 3, background: `linear-gradient(90deg, transparent, rgba(43,123,255,${0.25 + gridGlow * 0.45 + flare * 0.3}), transparent)`}} />
      </AbsoluteFill>
      <AbsoluteFill style={{background: `radial-gradient(120% 90% at 50% 45%, transparent 55%, rgba(0,0,0,${interpolate(dim, [0, 1], [0.55, 0.75])}) 100%)`}} />
    </AbsoluteFill>
  );
};
