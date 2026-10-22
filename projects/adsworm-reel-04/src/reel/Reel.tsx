import {AbsoluteFill, Html5Audio, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {Grain} from '../components/Grain';
import {SafeZoneOverlay} from '../components/SafeZoneOverlay';
import {ease} from '../lib/motion';
import {Aman, type Pose} from './Aman';
import {Captions} from './Captions';
import {Orb} from './Orb';
import {Rail} from './Rail';
import {CtaRoom, HookRoom, OneRoom, ROOM_H, ROOM_W, ThreeRoom, TwoRoom} from './rooms';
import {C, L} from './theme';
import {lineIndexAt, sinceLine, talkEnv, TL} from './tl';

// Engine v2: one infinite canvas, a flying camera. Rooms sit at world positions; the camera whips
// between them (0.55 s, speed blur), drifts while it dwells, and punches in on key numbers.
type Cam = {x: number; y: number; z: number; ry: number; rx: number};
const POS: Record<string, Omit<Cam, 'z'>> = {
  hook: {x: 0, y: 0, ry: 0, rx: 0},
  one: {x: 1350, y: -760, ry: -7, rx: 3},
  two: {x: 2700, y: -120, ry: 7, rx: -3},
  three: {x: 1500, y: 860, ry: -6, rx: -2},
  cta: {x: 160, y: 1320, ry: 0, rx: 4},
};
const MOVE = 0.55;
const PUNCH: [string, string][] = [['hook', 'black'], ['one', 'video'], ['two', '18.9%'], ['two', '20'], ['three', 'cost'], ['three', '7'], ['cta', 'q4']];
const punchTimes = PUNCH.map(([room, w]) => TL.lines.filter((l) => l.room === room).flatMap((l) => l.words).find((x) => x.w.toLowerCase().replace(/[^a-z0-9%.+,]/g, '').startsWith(w))?.s ?? -9);
const clamp01 = (v: number) => Math.max(0, Math.min(1, v));

const camAt = (t: number): Cam => {
  const rooms = TL.rooms;
  let i = 0;
  rooms.forEach((r, k) => {
    if (r.start - MOVE / 2 <= t) i = k;
  });
  const r = rooms[i];
  const dwell = clamp01((t - r.start) / (r.end - r.start));
  const P = POS[r.id];
  const here: Cam = {x: P.x, y: P.y, ry: P.ry + 3 * (dwell - 0.5), rx: P.rx, z: 1 + 0.04 * dwell};
  const m = clamp01((t - (r.start - MOVE / 2)) / MOVE);
  if (i === 0 || m >= 1) return here;
  const Q = POS[rooms[i - 1].id];
  const there: Cam = {x: Q.x, y: Q.y, ry: Q.ry + 1.5, rx: Q.rx, z: 1.04};
  const e = ease.inOutQuart(m);
  const lerp = (a: number, b: number) => a + (b - a) * e;
  return {x: lerp(there.x, here.x), y: lerp(there.y, here.y), ry: lerp(there.ry, here.ry), rx: lerp(there.rx, here.rx), z: lerp(there.z, here.z) * (1 - 0.22 * Math.sin(Math.PI * m))};
};
const punchAt = (t: number) => punchTimes.reduce((acc, p) => {
  const d = t - p;
  return acc + (d < 0 ? 0 : d < 0.08 ? d / 0.08 : Math.exp(-(d - 0.08) / 0.22));
}, 0);

const ROOMS: Record<string, React.FC<{t: number; start: number}>> = {hook: HookRoom, one: OneRoom, two: TwoRoom, three: ThreeRoom, cta: CtaRoom};
// moments the frame "glitches": the pattern interrupt (~20 s) and the sign-off
const GLITCH = [6, 12].map((i) => TL.lines[i].start);

export type ReelProps = {showSafeZones: boolean; withAudio: boolean};

export const Reel: React.FC<ReelProps> = ({showSafeZones, withAudio}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const idx = lineIndexAt(t);
  const line = TL.lines[idx];
  const algoSpeaking = line.who === 'ALGO' && t < line.end + 0.25;
  const g = GLITCH.reduce((acc, s) => Math.max(acc, t >= s - 0.04 && t < s + 0.4 ? 1 - (t - s) / 0.4 : 0), 0);

  // camera + takeover (the world steps back while THE ALGORITHM speaks; not on the cover line)
  const cam = camAt(t);
  const prev = camAt(t - 1 / fps);
  const speed = Math.hypot(cam.x - prev.x, cam.y - prev.y) + Math.abs(cam.ry - prev.ry) * 30;
  const take = idx === 0 ? 0 : algoSpeaking ? clamp01((t - line.start + 0.15) / 0.3) : clamp01(1 - (t - line.end - 0.25) / 0.3) * (line.who === 'ALGO' ? 1 : 0);
  const shake = g * Math.sin(t * 95) * 22;
  const z = cam.z * (1 + 0.05 * punchAt(t)) * (1 - 0.07 * take);
  const blur = Math.min(14, speed / 16) + take * 5;

  // orb: on stage for its lines (and the cover), in its seat otherwise
  const onStage = idx === 0 || algoSpeaking;
  const lastStageSwitch = TL.lines.reduce((acc, l, i) => (l.start <= t && ((l.who === 'ALGO') !== (TL.lines[i - 1]?.who === 'ALGO')) ? l.start : acc), 0);
  const sw = ease.outExpo(clamp01((t - lastStageSwitch + 0.12) / 0.35));
  const from = onStage ? L.orbSeat : L.orbStage;
  const to = onStage ? L.orbStage : L.orbSeat;
  const orbPos = idx === 0 ? L.orbStage : {x: from.x + (to.x - from.x) * sw, y: from.y + (to.y - from.y) * sw, r: from.r + (to.r - from.r) * sw};
  const algoTalk = talkEnv(frame, 'ALGO');
  const amanTalk = talkEnv(frame, 'AMAN');
  const gaze: [number, number] = onStage ? [0.25 * Math.sin(t * 0.8), 0.2 * Math.sin(t * 1.1)] : line.who === 'AMAN' ? [-0.9, -0.15] : [0, -0.6];

  // Aman: in after the cover line, out for the sign-off so the last frame loops into the first
  const enterAman = clamp01((t - TL.lines[1].start + 0.1) / 0.45);
  const exitAman = clamp01((t - TL.lines[12].start) / 0.4);
  const amanIn = ease.outExpo(enterAman) * (1 - ease.inOutQuart(exitAman));
  const pose: Pose = line.who === 'AMAN' && t < line.end + 0.2 ? (line.snap === 'translates' ? 'palms' : 'point') : 'idle';
  const poseSince = Math.round((t - (line.who === 'AMAN' ? line.start : line.end + 0.2)) * fps);
  const ctaStart = TL.rooms.find((r) => r.id === 'cta')?.start ?? 1e9;
  const railIn = ease.outExpo(clamp01(sinceLine(t, 2) < 0 ? (t - (TL.lines[1].words.at(-1)?.s ?? 5)) / 0.4 : 1)) * (1 - ease.inOutQuart(clamp01((t - ctaStart + 0.3) / 0.4)));

  return (
    <AbsoluteFill style={{background: C.bg, overflow: 'hidden'}}>
      {/* parallax background: dot grid + two colour fields */}
      <AbsoluteFill style={{backgroundImage: 'radial-gradient(rgba(240,238,232,0.10) 1.6px, transparent 1.6px)', backgroundSize: '54px 54px', backgroundPosition: `${-cam.x * 0.35}px ${-cam.y * 0.35}px`}} />
      <div style={{position: 'absolute', width: 1300, height: 1300, left: -300 - cam.x * 0.12, top: -200 - cam.y * 0.12, borderRadius: '50%', background: 'radial-gradient(rgba(27,94,247,0.28), transparent 65%)'}} />
      <div style={{position: 'absolute', width: 1100, height: 1100, left: 500 - cam.x * 0.08, top: 900 - cam.y * 0.08, borderRadius: '50%', background: 'radial-gradient(rgba(200,169,110,0.16), transparent 65%)'}} />

      {/* the world */}
      <div style={{position: 'absolute', inset: 0, perspective: 1800, perspectiveOrigin: `${L.room.cx}px ${L.room.cy}px`}}>
        <div
          style={{
            position: 'absolute',
            left: L.room.cx + shake,
            top: L.room.cy,
            transformStyle: 'preserve-3d',
            transform: `rotateX(${cam.rx}deg) rotateY(${cam.ry}deg) scale(${z}) translate(${-cam.x}px, ${-cam.y}px)`,
            filter: blur > 0.3 ? `blur(${blur.toFixed(1)}px)` : undefined,
            opacity: 1 - 0.55 * take,
          }}
        >
          {TL.rooms.map((r) => {
            if (t < r.start - 1.2 || t > r.end + 1.2) return null;
            const R = ROOMS[r.id];
            const P = POS[r.id];
            return (
              <div key={r.id} style={{position: 'absolute', left: P.x - ROOM_W / 2, top: P.y - ROOM_H / 2, width: ROOM_W, height: ROOM_H}}>
                <R t={t} start={r.start} />
              </div>
            );
          })}
        </div>
      </div>

      <Rail rooms={TL.rooms} t={t} show={railIn} />
      <Aman pose={pose} talk={amanTalk} enter={amanIn} sincePose={poseSince} />
      <Orb x={orbPos.x} y={orbPos.y} r={orbPos.r} t={t} talk={algoTalk} gaze={gaze} glitch={g} />
      <Captions line={line} t={t} fps={fps} />

      {/* glitch overlay: scanlines + RGB flash */}
      {g > 0 ? (
        <AbsoluteFill style={{background: `repeating-linear-gradient(0deg, rgba(95,225,255,${0.08 * g}) 0 3px, transparent 3px 9px)`, mixBlendMode: 'screen'}}>
          <AbsoluteFill style={{background: g > 0.85 ? 'rgba(240,238,232,0.18)' : undefined}} />
        </AbsoluteFill>
      ) : null}
      <AbsoluteFill style={{background: 'radial-gradient(ellipse at 50% 45%, transparent 55%, rgba(0,0,0,0.55))', pointerEvents: 'none'}} />
      <Grain opacity={0.06} />
      {withAudio ? <Html5Audio src={staticFile('voice.wav')} /> : null}
      {withAudio ? <Html5Audio src={staticFile('sfx.wav')} /> : null}
      {showSafeZones ? <SafeZoneOverlay /> : null}
    </AbsoluteFill>
  );
};
