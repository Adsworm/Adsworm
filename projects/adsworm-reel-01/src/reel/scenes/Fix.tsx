import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {sans} from '../../lib/fonts';
import {ease, progress, springs} from '../../lib/motion';
import {AdCard} from '../AdCard';
import {C} from '../theme';
import {Words} from '../Words';

const SCALE = 0.8;
const CARD_TOP = 540;

const SaveTag: React.FC<{s: number}> = ({s}) => (
  <div
    style={{
      display: 'inline-flex',
      alignItems: 'center',
      gap: 10,
      padding: '10px 22px',
      borderRadius: 999,
      background: C.lime,
      color: C.ink,
      fontFamily: sans,
      fontWeight: 800,
      fontSize: 32,
      letterSpacing: '0.08em',
      transform: `scale(${s})`,
    }}
  >
    <svg width={22} height={28} viewBox="0 0 22 28">
      <path d="M2 2 H20 V26 L11 19 L2 26 Z" fill={C.ink} />
    </svg>
    SAVE THIS
  </div>
);

const Check: React.FC<{n: string; text: string; at: number}> = ({n, text, at}) => (
  <div style={{display: 'flex', alignItems: 'center', gap: 22}}>
    <div style={{flexShrink: 0, width: 76, height: 76, borderRadius: '50%', background: C.lime, color: C.ink, fontFamily: sans, fontWeight: 800, fontSize: 44, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
      {n}
    </div>
    <Words text={text} size={54} at={at} align="left" maxWidth={820} />
  </div>
);

// One card, fixed one check per bar: strike the discount → name the city + problem → fan into weekly creatives.
export const Fix: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const enter = spring({frame: frame - 435, fps, config: springs.snappy});
  const save = spring({frame: frame - 450, fps, config: springs.pop});
  const strike = progress(frame, 495, 12, ease.inOutQuart);
  const badge = 1 - progress(frame, 508, 12); // gone by f520
  const city = frame >= 555 ? spring({frame: frame - 555, fps, config: springs.pop}) : 0;
  const swap = progress(frame, 570, 10);
  const fan = (at: number) => spring({frame: frame - at, fps, config: springs.snappy});
  const w1 = fan(615);
  const w2 = fan(620);
  const w3 = fan(625);
  const check =
    frame < 480 ? null :
    frame < 540 ? <Check key="1" n="1" text="One treatment per ad." at={480} /> :
    frame < 600 ? <Check key="2" n="2" text="Name the city. Name the problem." at={540} /> :
    <Check key="3" n="3" text="New creative every week." at={600} />;
  const card = (props: React.ComponentProps<typeof AdCard>, x: number, rot: number, s: number, z: number) => (
    <div
      style={{
        position: 'absolute',
        left: 540 - 260 + x,
        top: CARD_TOP + (1 - enter) * 420,
        opacity: enter,
        transform: `rotate(${rot}deg) scale(${s})`,
        transformOrigin: 'center top',
        zIndex: z,
      }}
    >
      <AdCard {...props} />
    </div>
  );
  const fanning = frame >= 615;
  const recede = progress(frame, 480, 18, ease.outExpo);
  return (
    <AbsoluteFill>
      <div style={{position: 'absolute', top: 285, width: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 18, opacity: 1 - recede * 0.55, transform: `scale(${1 - recede * 0.12})`, transformOrigin: 'center top'}}>
        <SaveTag s={save} />
        <Words text="3 checks before your next ad" size={62} at={420} />
      </div>
      {fanning ? (
        <>
          {card({treatment: 'Hair PRP', altSubline: 'Crown thinning, explained', swap: 1, badge: 0, city: 1, week: 'W2'}, 0, 0, SCALE * interpolate(w2, [0, 1], [0.9, 0.86]), 3)}
          {card({treatment: 'Hair PRP', altSubline: 'PRP for early thinning', swap: 1, badge: 0, city: 1, week: 'W1'}, -225 * w1, -8 * w1, SCALE * 0.8, 2)}
          {card({treatment: 'Hair PRP', altSubline: 'PRP or transplant?', swap: 1, badge: 0, city: 1, week: 'W3'}, 225 * w3, 8 * w3, SCALE * 0.8 * Math.min(1, w3 * 1.2), 1)}
        </>
      ) : (
        card({treatment: 'Hair PRP', altSubline: 'PRP for early thinning', swap, strike, badge, city}, 0, 0, SCALE, 1)
      )}
      <div style={{position: 'absolute', top: 1120, left: 80, right: 80, display: 'flex', justifyContent: 'center'}}>{check}</div>
    </AbsoluteFill>
  );
};
