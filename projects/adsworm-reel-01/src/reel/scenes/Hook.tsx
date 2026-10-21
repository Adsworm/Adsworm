import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {sans} from '../../lib/fonts';
import {ease, progress, springs} from '../../lib/motion';
import {ClinicIcon} from '../ClinicIcon';
import {C} from '../theme';
import {Words} from '../Words';

// 5×3 grid of clinic icons; the centre cell (row 1, col 2) is the original "1 clinic".
const COLS = 5;
const ROWS = 3;
const ICON = 100;
const GAP = 34;
const GRID_W = COLS * ICON + (COLS - 1) * GAP;
const GRID_TOP = 400;
const cellCenter = (i: number) => ({
  x: 540 - GRID_W / 2 + (i % COLS) * (ICON + GAP) + ICON / 2,
  y: GRID_TOP + Math.floor(i / COLS) * (ICON + GAP) + ICON / 2,
});
const CENTER = 7;
const order = Array.from({length: COLS * ROWS}, (_, i) => i)
  .filter((i) => i !== CENTER)
  .sort((a, b) => Math.hypot(cellCenter(a).x - 540, cellCenter(a).y - cellCenter(CENTER).y) - Math.hypot(cellCenter(b).x - 540, cellCenter(b).y - cellCenter(CENTER).y));

const BIG = 250;

export const SeriesTag: React.FC<{opacity?: number}> = ({opacity = 1}) => (
  <div style={{position: 'absolute', top: 290, width: '100%', textAlign: 'center', fontFamily: sans, fontWeight: 600, fontSize: 34, letterSpacing: '0.18em', color: C.muted, opacity}}>
    ADSWORM · FULL CHAIRS 01
  </div>
);

// Exactly what frame 0 shows — also reused for the loop-back at the end.
export const HookStill: React.FC = () => (
  <AbsoluteFill>
    <SeriesTag />
    <div style={{position: 'absolute', left: 540 - BIG / 2, top: cellCenter(CENTER).y - BIG / 2 - 40}}>
      <ClinicIcon size={BIG} />
    </div>
    <div style={{position: 'absolute', top: 860, width: '100%', display: 'flex', justifyContent: 'center'}}>
      <Words text="1 clinic." size={150} at={0} set />
    </div>
  </AbsoluteFill>
);

export const Hook: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  if (frame < 30) return <HookStill />; // frame 0 is the thumbnail: fully set, no fade-in
  const morph = progress(frame, 30, 16, ease.outExpo);
  const c = cellCenter(CENTER);
  const size = interpolate(morph, [0, 1], [BIG, ICON]);
  const cy = interpolate(morph, [0, 1], [c.y - 40, c.y]);
  const dim = interpolate(progress(frame, 60, 15), [0, 1], [1, 0.25]);
  const count = Math.round(interpolate(frame, [30, 45], [1, 15], {extrapolateRight: 'clamp'}));
  const tagOut = 1 - progress(frame, 110, 9);
  return (
    <AbsoluteFill>
      <SeriesTag opacity={tagOut} />
      <div style={{opacity: dim}}>
        {order.map((i, k) => {
          const s = spring({frame: frame - 31 - k, fps, config: springs.pop});
          const p = cellCenter(i);
          return (
            <div key={i} style={{position: 'absolute', left: p.x - ICON / 2, top: p.y - ICON / 2, transform: `scale(${s})`}}>
              <ClinicIcon size={ICON} />
            </div>
          );
        })}
        <div style={{position: 'absolute', left: 540 - size / 2, top: cy - size / 2}}>
          <ClinicIcon size={size} color={C.lime} />
        </div>
      </div>
      <div style={{position: 'absolute', top: 860, width: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 18}}>
        {frame < 60 ? (
          <Words text={`*${count}* branches.`} size={140} at={30} />
        ) : (
          <>
            <Words text="Same city." size={130} at={60} />
            {frame >= 90 ? <Words text="Here's what changed." size={84} at={90} color={C.muted} weight={700} /> : null}
          </>
        )}
      </div>
    </AbsoluteFill>
  );
};
