import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {body, display} from '../../lib/fonts';
import {ease, progress, springs} from '../../lib/motion';
import {Headline} from '../Headline';
import {C} from '../theme';

const Title: React.FC<{n: string; text: string; label: string; at: number}> = ({n, text, label, at}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const s = spring({frame: frame - at, fps, config: springs.pop});
  const l = progress(frame, at + 10, 14, ease.outExpo);
  return (
    <>
    <div style={{position: 'absolute', top: 470, width: '100%', textAlign: 'center', fontFamily: body, fontWeight: 600, fontSize: 40, color: C.blueBright, letterSpacing: '0.04em', opacity: l, transform: `translateY(${(1 - l) * 16}px)`}}>
      {label}
    </div>
    <div style={{position: 'absolute', top: 330, width: '100%', display: 'flex', justifyContent: 'center', alignItems: 'center', gap: 28}}>
      <div style={{width: 96, height: 96, borderRadius: '50%', background: C.blue, color: C.paper, fontFamily: display, fontSize: 70, lineHeight: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', paddingTop: 6, transform: `scale(${s})`}}>
        {n}
      </div>
      <Headline lines={[text]} size={124} at={at + 2} stagger={5} />
    </div>
    </>
  );
};

// ① SEEN EVERYWHERE — one abstract mark stamps in on 8th notes, each repeat more solid:
// repetition reads as familiarity, familiarity as safety (mere-exposure effect).
const Mark: React.FC<{size: number; fill: number}> = ({size, fill}) => (
  <svg width={size} height={size} viewBox="0 0 100 100" style={{display: 'block', overflow: 'visible'}}>
    <rect x={4} y={4} width={92} height={92} rx={26} fill={C.blue} fillOpacity={fill} stroke={C.blueBright} strokeWidth={3} />
    <path d="M28 70 L42 52 L54 62 L72 34" fill="none" stroke={C.paper} strokeOpacity={0.35 + fill * 0.65} strokeWidth={8} strokeLinecap="round" strokeLinejoin="round" />
    <circle cx={72} cy={34} r={7} fill={C.paper} fillOpacity={0.35 + fill * 0.65} />
  </svg>
);
const STAMPS = [
  {at: 246, x: 290, y: 640, s: 150},
  {at: 254, x: 800, y: 720, s: 180},
  {at: 262, x: 380, y: 990, s: 165},
  {at: 270, x: 760, y: 1070, s: 215},
  {at: 278, x: 230, y: 830, s: 190},
  {at: 286, x: 860, y: 920, s: 200},
  {at: 294, x: 540, y: 840, s: 330},
];
const Seen: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill>
      <Title n="1" text="SEEN EVERYWHERE." label="Mere-exposure effect" at={240} />
      {STAMPS.map((st, i) => {
        const p = progress(frame, st.at, 6, ease.outExpo);
        if (frame < st.at) return null;
        const fill = 0.1 + (0.9 * i) / (STAMPS.length - 1);
        const settle = i === STAMPS.length - 1 ? 1 : interpolate(frame, [st.at, st.at + 30], [1, 0.55], {extrapolateRight: 'clamp'});
        return (
          <div key={i} style={{position: 'absolute', left: st.x - st.s / 2, top: st.y - st.s / 2, opacity: p * settle, transform: `scale(${1.6 - p * 0.6}) rotate(${(i % 2 ? 1 : -1) * 6 * (1 - p)}deg)`}}>
            <Mark size={st.s} fill={fill} />
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

// ② TALKED ABOUT — two identical doors; a queue forms at one, and that's the one everyone picks
// (social proof / the busy-restaurant effect).
const Door: React.FC<{x: number; active: number; dim: number}> = ({x, active, dim}) => (
  <svg width={220} height={360} viewBox="0 0 220 360" style={{position: 'absolute', left: x - 110, top: 640, opacity: 1 - dim * 0.6, overflow: 'visible'}}>
    <path d="M10 350 V110 A100 100 0 0 1 210 110 V350 Z" fill="rgba(240,238,232,0.04)" stroke={C.paper} strokeOpacity={0.85} strokeWidth={5} />
    <path d="M10 350 V110 A100 100 0 0 1 210 110 V350 Z" fill="none" stroke={C.blueBright} strokeWidth={9} strokeDasharray={1000} strokeDashoffset={1000 * (1 - active)} style={{filter: `drop-shadow(0 0 ${active * 18}px rgba(43,123,255,0.9))`}} />
    <circle cx={178} cy={235} r={7} fill={C.paper} fillOpacity={0.85} />
  </svg>
);
// Side-on queue standing beside the chosen door, feet on the door's threshold line.
const QUEUE = [
  {at: 308, x: 768, y: 1000, k: 1.1},
  {at: 316, x: 838, y: 1000, k: 1.1},
  {at: 324, x: 908, y: 1000, k: 1.1},
  {at: 332, x: 978, y: 1000, k: 1.1},
];
const Person: React.FC<{x: number; y: number; s: number}> = ({x, y, s}) => (
  <div style={{position: 'absolute', left: x - 22, top: y - 120, transform: `scale(${s})`, transformOrigin: 'bottom center', filter: 'drop-shadow(0 10px 18px rgba(0,0,0,0.6))'}}>
    <div style={{width: 40, height: 40, borderRadius: '50%', background: C.paper, margin: '0 auto 6px'}} />
    <div style={{width: 44, height: 74, borderRadius: 22, background: C.paper}} />
  </div>
);
const Talked: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const doors = spring({frame: frame - 302, fps, config: springs.snappy});
  const active = progress(frame, 346, 10, ease.outExpo);
  return (
    <AbsoluteFill>
      <Title n="2" text="TALKED ABOUT." label="Social proof" at={300} />
      <div style={{position: 'absolute', inset: 0, opacity: doors, transform: `translateY(${(1 - doors) * 60}px)`}}>
        <Door x={250} active={0} dim={active} />
        <Door x={590} active={active} dim={0} />
      </div>
      {QUEUE.map((q, i) => (
        <Person key={i} x={q.x} y={q.y} s={q.k * spring({frame: frame - q.at, fps, config: springs.pop})} />
      ))}
    </AbsoluteFill>
  );
};

// ③ LOOKS THE PART — a cluttered discount flyer gets wiped into a premium frame.
const Cheap: React.FC = () => (
  <div style={{position: 'absolute', inset: 0, borderRadius: 24, background: '#FFE14D', border: '6px dashed #E02424', overflow: 'hidden', fontFamily: body}}>
    <svg width={640} height={800} style={{position: 'absolute', inset: 0}}>
      <polygon points="520,60 545,120 610,110 565,160 600,215 535,195 500,250 485,185 420,175 475,140" fill="#E02424" />
      <polygon points="90,560 110,610 165,605 125,640 150,690 100,670 70,715 62,660 10,650 55,625" fill="#1E5BFF" />
    </svg>
    <div style={{position: 'absolute', top: 150, width: '100%', textAlign: 'center', color: '#E02424', fontWeight: 900, fontStyle: 'italic', fontSize: 104, lineHeight: 0.95, transform: 'rotate(-4deg)'}}>
      MEGA
      <br />
      SALE!!!
    </div>
    <div style={{position: 'absolute', top: 420, width: '100%', textAlign: 'center', color: '#111', fontWeight: 900, fontSize: 96}}>50% OFF*</div>
    <div style={{position: 'absolute', top: 560, width: '100%', textAlign: 'center', color: '#1E5BFF', fontWeight: 800, fontSize: 52, textDecoration: 'underline'}}>CALL NOW!!</div>
    <div style={{position: 'absolute', bottom: 22, width: '100%', textAlign: 'center', color: '#333', fontSize: 22}}>*T&C apply. Limited period. Hurry!!</div>
  </div>
);
const Premium: React.FC = () => (
  <div style={{position: 'absolute', inset: 0, borderRadius: 24, background: `radial-gradient(90% 70% at 50% 30%, #16203A, ${C.bg2})`, overflow: 'hidden'}}>
    <div style={{position: 'absolute', inset: 26, border: `2px solid ${C.paper}`, borderRadius: 12, opacity: 0.5}} />
    <div style={{position: 'absolute', top: 170, width: '100%', display: 'flex', justifyContent: 'center'}}>
      <div style={{width: 120, height: 120, borderRadius: '50%', border: `2px solid ${C.paper}`, color: C.paper, fontFamily: display, fontSize: 84, display: 'flex', alignItems: 'center', justifyContent: 'center', paddingTop: 8}}>S</div>
    </div>
    <div style={{position: 'absolute', top: 350, width: '100%', textAlign: 'center', fontFamily: display, fontSize: 118, letterSpacing: '0.06em', color: C.paper}}>SIGNATURE</div>
    <div style={{position: 'absolute', top: 480, width: '100%', textAlign: 'center', fontFamily: body, fontSize: 34, letterSpacing: '0.24em', color: C.blueBright}}>DERMATOLOGY</div>
    <div style={{position: 'absolute', top: 560, left: 220, right: 220, height: 2, background: C.paper, opacity: 0.4}} />
    <div style={{position: 'absolute', top: 600, width: '100%', textAlign: 'center', fontFamily: body, fontSize: 30, color: C.muted}}>By appointment · Since 2009</div>
  </div>
);
const LooksPart: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const enter = spring({frame: frame - 362, fps, config: springs.snappy});
  const wipe = progress(frame, 372, 20, ease.inOutQuart);
  return (
    <AbsoluteFill>
      <Title n="3" text="LOOKS THE PART." label="Halo effect" at={360} />
      <div style={{position: 'absolute', left: 220, top: 540 + (1 - enter) * 300, width: 640, height: 800, opacity: enter, transform: `scale(${0.85 * interpolate(wipe, [0, 1], [0.95, 1])})`, transformOrigin: 'center top'}}>
        <Cheap />
        <div style={{position: 'absolute', inset: 0, clipPath: `inset(0 ${(1 - wipe) * 100}% 0 0)`}}>
          <Premium />
        </div>
        {wipe > 0 && wipe < 1 ? (
          <div style={{position: 'absolute', top: -20, bottom: -20, left: `${wipe * 100}%`, width: 6, background: C.blueBright, boxShadow: `0 0 40px 10px rgba(43,123,255,0.8)`}} />
        ) : null}
      </div>
    </AbsoluteFill>
  );
};

export const Signals: React.FC = () => {
  const frame = useCurrentFrame();
  if (frame < 300) return <Seen />;
  if (frame < 360) return <Talked />;
  return <LooksPart />;
};
