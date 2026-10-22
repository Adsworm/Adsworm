import {C} from './theme';

// THE ALGORITHM: a coded character. The body is a blob whose outline is a sum of sines, so it breathes
// at rest and churns with the voice (`talk` = loudness 0..1). One eye: it looks at whoever is talking,
// blinks, and the whole thing RGB-splits when `glitch` > 0.
type Props = {x: number; y: number; r: number; t: number; talk: number; gaze: [number, number]; glitch: number};

const blob = (r: number, t: number, talk: number, n = 120) => {
  const pts: string[] = [];
  for (let i = 0; i < n; i++) {
    const a = (i / n) * Math.PI * 2;
    const k = 1 + 0.035 * Math.sin(3 * a + 1.1 * t) + 0.025 * Math.sin(5 * a - 1.7 * t) + talk * (0.08 * Math.sin(6 * a + 7 * t) + 0.05 * Math.sin(9 * a - 9 * t));
    pts.push(`${(Math.cos(a) * r * k).toFixed(1)},${(Math.sin(a) * r * k).toFixed(1)}`);
  }
  return `M${pts.join('L')}Z`;
};

export const Orb: React.FC<Props> = ({x, y, r, t, talk, gaze, glitch}) => {
  const S = r * 3.4;
  const blinkPhase = (t + 0.7) % 3.3;
  const blink = blinkPhase < 0.12 ? 0.12 : 1;
  const eyeR = r * 0.27 * (1 + talk * 0.08);
  const gx = gaze[0] * r * 0.2;
  const gy = gaze[1] * r * 0.16;
  const g = glitch;
  const slice = g > 0 ? Math.round((Math.sin(t * 91) * 0.5 + 0.5) * 6) : 0;
  return (
    <div
      style={{
        position: 'absolute',
        left: x - S / 2,
        top: y - S / 2,
        width: S,
        height: S,
        filter: g > 0 ? `drop-shadow(${10 * g}px 0 0 rgba(255,70,110,0.85)) drop-shadow(${-10 * g}px 0 0 rgba(70,240,255,0.85))` : undefined,
        transform: g > 0 ? `translateX(${Math.sin(t * 157) * 14 * g}px) skewX(${Math.sin(t * 73) * 8 * g}deg)` : undefined,
      }}
    >
      <svg width={S} height={S} viewBox={`${-S / 2} ${-S / 2} ${S} ${S}`} style={{overflow: 'visible'}}>
        <defs>
          <radialGradient id="orb-glow">
            <stop offset="0%" stopColor={C.cyan} stopOpacity={0.55} />
            <stop offset="45%" stopColor={C.blueBright} stopOpacity={0.22} />
            <stop offset="100%" stopColor={C.blue} stopOpacity={0} />
          </radialGradient>
          <radialGradient id="orb-body" cx="40%" cy="35%" r="75%">
            <stop offset="0%" stopColor="#D9F7FF" />
            <stop offset="28%" stopColor={C.cyan} />
            <stop offset="62%" stopColor={C.blueBright} />
            <stop offset="100%" stopColor="#0A1E5C" />
          </radialGradient>
        </defs>
        <circle r={r * (1.65 + talk * 0.35)} fill="url(#orb-glow)" />
        {Array.from({length: 12}).map((_, i) => {
          const a = (i / 12) * Math.PI * 2 + t * (0.6 + (i % 3) * 0.15) * (i % 2 ? 1 : -1);
          const rr = r * (1.22 + 0.08 * Math.sin(t * 2 + i));
          return <circle key={i} cx={Math.cos(a) * rr} cy={Math.sin(a) * rr * 0.92} r={r * (0.018 + (i % 3) * 0.008)} fill={i % 4 ? C.cyan : C.gold} opacity={0.75} />;
        })}
        <path d={blob(r, t, talk)} fill="url(#orb-body)" stroke={C.cyan} strokeOpacity={0.6} strokeWidth={2} />
        <circle r={r * 0.8} fill="none" stroke="#fff" strokeOpacity={0.25} strokeWidth={1.5} strokeDasharray={`${r * 0.05} ${r * 0.09}`} transform={`rotate(${t * 40})`} />
        <circle r={r * 0.64} fill="none" stroke="#0A1E5C" strokeOpacity={0.35} strokeWidth={r * 0.03} strokeDasharray={`${r * 0.6} ${r * 0.25}`} transform={`rotate(${-t * 65})`} />
        <g transform={`translate(${gx} ${gy}) scale(1 ${blink})`}>
          <ellipse rx={eyeR * 1.25} ry={eyeR} fill="#F4FCFF" />
          <circle cx={gx * 0.35} cy={gy * 0.35} r={eyeR * 0.55} fill="#0A1E5C" />
          <circle cx={gx * 0.35 - eyeR * 0.18} cy={gy * 0.35 - eyeR * 0.2} r={eyeR * 0.14} fill="#fff" />
        </g>
        <ellipse cx={-r * 0.35} cy={-r * 0.45} rx={r * 0.28} ry={r * 0.12} fill="#fff" opacity={0.35} transform={`rotate(-30 ${-r * 0.35} ${-r * 0.45})`} />
      </svg>
      {slice ? <div style={{position: 'absolute', left: 0, right: 0, top: `${30 + slice * 7}%`, height: 10 * g, background: 'rgba(95,225,255,0.5)', mixBlendMode: 'screen'}} /> : null}
    </div>
  );
};
