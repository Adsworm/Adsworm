import {AbsoluteFill, Easing, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {progress, springs} from '../../lib/motion';
import {AdCard} from '../AdCard';
import {Words} from '../Words';

const TREATMENTS = ['Hair PRP', 'Laser', 'Teeth Whitening', 'HydraFacial', 'Hair PRP', 'Skin Peel', 'Laser', 'Whitening', 'HydraFacial'];
const TINTS = ['#9C9C9C', '#8F9499', '#A39A92', '#959A92', '#9C9C9C', '#9A9298', '#8F9499', '#A39A92', '#959A92'];
const CARD_W = 520;
const CARD_H = 680;
const S = 0.36; // grid scale
const GAP = 22;
const CELL_W = CARD_W * S;
const CELL_H = CARD_H * S;
const GRID_TOP = 440;
const cell = (i: number) => ({
  x: 540 - (3 * CELL_W + 2 * GAP) / 2 + (i % 3) * (CELL_W + GAP) + CELL_W / 2,
  y: GRID_TOP + Math.floor(i / 3) * (CELL_H + GAP) + CELL_H / 2,
});
const ORDER = [1, 3, 5, 7, 0, 2, 6, 8]; // edges first, corners last

export const Problem: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const enter = spring({frame: frame - 120, fps, config: springs.snappy});
  const toGrid = progress(frame, 180, 16);
  const grey = progress(frame, 240, 15);
  const flick = interpolate(frame, [270, 288], [0, -1500], {easing: Easing.bezier(0.7, 0, 0.84, 0), extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const centre = cell(4);
  const bigY = 470 + CARD_H / 2;
  const header =
    frame < 180 ? <Words key="a" text="Most clinic ads look like this:" size={66} at={120} /> :
    frame < 240 ? <Words key="b" text="Every clinic. *Same ad.*" size={78} at={180} /> :
    <Words key="c" text="Patients scroll right past." size={78} at={240} />;
  return (
    <AbsoluteFill>
      <div style={{position: 'absolute', top: 300, width: '100%', display: 'flex', justifyContent: 'center'}}>{header}</div>
      <div style={{position: 'absolute', inset: 0, transform: `translateY(${flick}px)`, filter: `grayscale(${grey})`, opacity: 1 - grey * 0.65}}>
        {frame >= 180
          ? ORDER.map((i, k) => {
              const s = spring({frame: frame - 182 - k * 2, fps, config: springs.pop}) * S;
              const p = cell(i);
              return (
                <div key={i} style={{position: 'absolute', left: p.x - CARD_W / 2, top: p.y - CARD_H / 2, transform: `scale(${s})`}}>
                  <AdCard treatment={TREATMENTS[i]} photoTint={TINTS[i]} />
                </div>
              );
            })
          : null}
        <div
          style={{
            position: 'absolute',
            left: 540 - CARD_W / 2,
            top: interpolate(toGrid, [0, 1], [bigY, centre.y]) - CARD_H / 2 + (1 - enter) * 420,
            opacity: enter,
            transform: `scale(${interpolate(toGrid, [0, 1], [1, S])})`,
          }}
        >
          <AdCard treatment="Hair PRP" />
        </div>
      </div>
    </AbsoluteFill>
  );
};
