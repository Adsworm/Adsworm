import {interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {springs} from '../lib/motion';
import {C} from './theme';

// The empire, drawn: a night skyline rising off the grid floor; windows light as it completes.
const SLOTS = 9;
const TG = 14;
const BASE = 1176;
const TOWERS = [
  {w: 88, h: 250},
  {w: 70, h: 360},
  {w: 96, h: 300},
  {w: 78, h: 420, antenna: true},
  {w: 110, h: 340},
  {w: 74, h: 460, antenna: true},
  {w: 92, h: 280},
  {w: 70, h: 380},
  {w: 90, h: 240},
];
const ORDER = [4, 3, 5, 2, 6, 1, 7, 0, 8]; // grows outward from the centre
const total = TOWERS.reduce((a, t) => a + t.w, 0) + (SLOTS - 1) * TG;
const xs = TOWERS.reduce<number[]>((acc, t, i) => [...acc, i === 0 ? 540 - total / 2 : acc[i - 1] + TOWERS[i - 1].w + TG], []);

export const Skyline: React.FC<{at: number; every?: number; lit?: number; dim?: number; scale?: number}> = ({at, every = 5, lit = 0, dim = 0, scale = 1}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const glow = interpolate(lit, [0, 1], [0.12, 0.85]);
  return (
    <div style={{position: 'absolute', inset: 0, opacity: 1 - dim * 0.55, transform: `scale(${scale})`, transformOrigin: `540px ${BASE}px`}}>
      {ORDER.map((i, k) => {
        const t = TOWERS[i];
        const rise = spring({frame: frame - at - k * every, fps, config: springs.snappy});
        return (
          <div key={i} style={{position: 'absolute', left: xs[i], top: BASE - t.h, width: t.w, height: t.h, transform: `scaleY(${rise})`, transformOrigin: 'bottom'}}>
            {t.antenna ? <div style={{position: 'absolute', left: t.w / 2 - 2, top: -70, width: 4, height: 70, background: '#2A3550'}} /> : null}
            {t.antenna ? <div style={{position: 'absolute', left: t.w / 2 - 6, top: -78, width: 12, height: 12, borderRadius: '50%', background: C.blueBright, opacity: 0.5 + lit * 0.5, boxShadow: `0 0 ${10 + lit * 20}px ${C.blueBright}`}} /> : null}
            <div
              style={{
                position: 'absolute',
                inset: 0,
                background: 'linear-gradient(90deg, #1A2440 0%, #121A30 55%, #0D1320 100%)',
                borderTop: '3px solid #2A3550',
                boxShadow: `0 0 ${lit * 40}px rgba(27,94,247,${lit * 0.25})`,
              }}
            />
            <div
              style={{
                position: 'absolute',
                left: 10,
                right: 10,
                top: 16,
                bottom: 10,
                backgroundImage: `radial-gradient(circle, rgba(240,238,232,${glow}) 0 3px, transparent 3.5px)`,
                backgroundSize: '16px 22px',
              }}
            />
          </div>
        );
      })}
    </div>
  );
};
