import {AbsoluteFill, Html5Audio, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {SafeZoneOverlay} from '../components/SafeZoneOverlay';
import {body} from '../lib/fonts';
import {Bubble, type Token} from './Bubble';
import {Bust, mouthFor} from './Bust';
import {C, V3} from './theme';
import timeline from './timeline.json';
import {Views, type View} from './views';

// Engine v3: a teacher (Aman) and a student (Riya) as talking heads, karaoke bubble captions, and a
// proof board on top that builds on the spoken word. One section = one board; boards whip in.
type Line = {n: number; section: string; who: 'AMAN' | 'RIYA'; start: number; end: number; words: {t: number; w: string}[]; tokens: Token[]};
type Section = {id: string; label: string; tag: string; source: string; start: number; end: number; views: View[]};
type Timeline = {fps: number; durationInFrames: number; env: number[]; brand: {names?: Record<string, string>; side?: Record<string, 'left' | 'right'>}; lines: Line[]; sections: Section[]; beats: Record<string, number>; vars?: Record<string, number | string>};
const TL = timeline as unknown as Timeline;
const NAMES = TL.brand.names ?? {AMAN: 'AMAN', RIYA: 'RIYA'};
const SIDE = TL.brand.side ?? {AMAN: 'left', RIYA: 'right'};
const env = (f: number) => TL.env[Math.max(0, Math.min(TL.env.length - 1, f))] ?? 0;

export type ReelProps = {showSafeZones: boolean; withAudio: boolean};

export const Reel: React.FC<ReelProps> = ({showSafeZones, withAudio}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const idx = Math.max(0, TL.lines.reduce((acc, ln, i) => (ln.start - 0.06 <= t ? i : acc), 0));
  const line = TL.lines[idx];
  const si = Math.max(0, TL.sections.reduce((acc, s, i) => (s.start - 0.2 <= t ? i : acc), 0));
  const section = TL.sections[si];
  const talking = t >= line.start - 0.05 && t <= line.end + 0.12;
  const last = TL.lines[TL.lines.length - 1];

  // board motion: zoom-punch on frame 0, whip-in from the right on every new section
  const secF = Math.round((section.start - 0.2) * fps);
  const sp = spring({frame: si === 0 ? frame : frame - secF, fps, config: si === 0 ? {damping: 10, stiffness: 170, mass: 0.7} : {damping: 16, stiffness: 150}});
  const sp1 = spring({frame: (si === 0 ? frame : frame - secF) - 1, fps, config: si === 0 ? {damping: 10, stiffness: 170, mass: 0.7} : {damping: 16, stiffness: 150}});
  const boardX = si === 0 ? 0 : (1 - sp) * 1100;
  const blur = si === 0 ? 0 : Math.min(18, Math.abs(sp - sp1) * 260);
  const boardScale = si === 0 ? 0.55 + 0.45 * sp : 1;
  const pill = spring({frame: frame - secF, fps, config: {damping: 12, stiffness: 200}});

  const words = TL.lines.filter((l) => l.section === section.id).flatMap((l) => l.words);
  const mouth = (who: 'AMAN' | 'RIYA') => (talking && line.who === who ? mouthFor(env(frame), env(frame - 1)) : who === 'AMAN' && t > last.end + 0.1 ? 'wink' : 'closed');
  const talk = (who: string) => (talking && line.who === who ? env(frame) : 0);
  const riyaIn = spring({frame: frame - 2, fps, config: {damping: 14}});
  const amanIn = spring({frame, fps, config: {damping: 14}});
  const B = V3.board;

  return (
    <AbsoluteFill style={{background: V3.paper, overflow: 'hidden'}}>
      <AbsoluteFill style={{backgroundImage: 'radial-gradient(rgba(13,19,32,0.13) 1.6px, transparent 1.8px)', backgroundSize: '30px 30px', backgroundPosition: `${-frame * 0.4}px 0px`}} />

      {/* section pill */}
      <div style={{position: 'absolute', left: 0, right: 0, top: 254, display: 'flex', justifyContent: 'center'}}>
        <div style={{padding: '10px 26px', borderRadius: 999, background: C.gold, border: V3.outline, boxShadow: '4px 4px 0 #0D1320', fontFamily: body, fontWeight: 800, fontSize: 26, letterSpacing: '0.1em', color: C.ink, transform: `scale(${pill}) rotate(${(1 - pill) * -8}deg)`}}>{section.label}</div>
      </div>

      {/* proof board */}
      <div style={{position: 'absolute', left: B.x, top: B.y, width: B.w, height: B.h, transform: `translateX(${boardX}px) scale(${boardScale})`, filter: blur > 0.4 ? `blur(${blur.toFixed(1)}px)` : undefined}}>
        <div style={{position: 'absolute', inset: 0, borderRadius: 34, background: '#fff', border: V3.outline, boxShadow: '9px 9px 0 #0D1320', overflow: 'hidden'}}>
          <div style={{height: 46, borderBottom: V3.outline, display: 'flex', alignItems: 'center', gap: 10, padding: '0 20px', background: '#F7F8FA'}}>
            {['#FF5F57', '#FEBC2E', '#28C840'].map((c) => (
              <span key={c} style={{width: 16, height: 16, borderRadius: '50%', background: c, border: '2px solid #0D1320'}} />
            ))}
            <span style={{marginLeft: 12, fontFamily: body, fontWeight: 700, fontSize: 20, color: C.muted}}>adsworm.com · explained simply</span>
          </div>
          <div style={{position: 'absolute', left: 40, right: 40, top: 70, bottom: 56}}>
            <Views views={section.views ?? []} beats={TL.beats} frame={frame} vars={TL.vars ?? {}} words={words} fps={fps} />
          </div>
          {section.source ? <div style={{position: 'absolute', left: 28, right: 28, bottom: 14, fontFamily: body, fontSize: 18, lineHeight: 1.2, color: C.muted, textAlign: 'center'}}>{section.source}</div> : null}
        </div>
      </div>

      <Bubble tokens={line.tokens} who={line.who} name={NAMES[line.who] ?? line.who} side={SIDE[line.who] ?? 'left'} t={t} fps={fps} />

      <Bust who="riya" x={V3.riya.x} y={V3.riya.y} size={V3.riya.size} mouth={mouth('RIYA')} talk={talk('RIYA')} active={line.who === 'RIYA' && talking} t={t} enter={riyaIn} />
      <Bust who="aman" x={V3.aman.x} y={V3.aman.y} size={V3.aman.size} mouth={mouth('AMAN')} talk={talk('AMAN')} active={line.who === 'AMAN' && talking} t={t} enter={amanIn} />

      {withAudio ? <Html5Audio src={staticFile('voice.wav')} /> : null}
      {showSafeZones ? <SafeZoneOverlay /> : null}
    </AbsoluteFill>
  );
};
