import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {sans} from '../../lib/fonts';
import {springs} from '../../lib/motion';
import {ClinicIcon} from '../ClinicIcon';
import {C} from '../theme';
import {Words} from '../Words';

const COLS = 6;
const ICON = 84;
const GAP = 26;
const TOP = 330;
const pos = (i: number) => ({
  x: 540 - (COLS * ICON + (COLS - 1) * GAP) / 2 + (i % COLS) * (ICON + GAP),
  y: TOP + Math.floor(i / COLS) * (ICON + GAP),
});

// The hook's 15 come back; 15 more pop in one per tick; the count lands on the downbeat (f720).
export const Proof: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const n = Math.round(interpolate(frame, [675, 717], [15, 30], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}));
  const land = spring({frame: frame - 720, fps, config: springs.pop});
  const punch = frame >= 720 ? interpolate(land, [0, 1], [1.18, 1]) : 1;
  return (
    <AbsoluteFill>
      {Array.from({length: 30}, (_, i) => {
        const at = i < 15 ? 660 + i : 675 + (i - 15) * 3;
        const s = spring({frame: frame - at, fps, config: springs.pop});
        const p = pos(i);
        return (
          <div key={i} style={{position: 'absolute', left: p.x, top: p.y, transform: `scale(${s})`}}>
            <ClinicIcon size={ICON} color={i < 15 ? C.paper : C.lime} />
          </div>
        );
      })}
      <div style={{position: 'absolute', top: 880, width: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 6}}>
        <div style={{fontFamily: sans, fontWeight: 800, fontSize: 230, lineHeight: 1, letterSpacing: '-0.06em', color: C.lime, transform: `scale(${punch})`, fontVariantNumeric: 'tabular-nums'}}>
          {n}
          <span style={{opacity: frame >= 720 ? 1 : 0}}>+</span>
        </div>
        <Words text="clinics scaled across India." size={60} at={664} />
      </div>
    </AbsoluteFill>
  );
};
