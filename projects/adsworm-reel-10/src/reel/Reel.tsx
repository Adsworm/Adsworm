import {AbsoluteFill, Html5Audio, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {SafeZoneOverlay} from '../components/SafeZoneOverlay';
import {body} from '../lib/fonts';
import {Bubble, type Token} from './Bubble';
import {Bust, mouthFor} from './Bust';
import {Sfx, SfxOn} from './Sfx';
import {C, V3} from './theme';
import timeline from './timeline.json';
import {Views, type View} from './views';

// Engine v4 (docs/playbook/EDITING-PSYCHOLOGY.md): a teacher (Aman) and a student (Riya) as talking
// heads that act (lip-flap while speaking, full-face reactions while listening), karaoke bubble
// captions, a proof board that builds on the spoken word, sound played by the visuals themselves,
// an open-loop chip that stays on screen until the payoff, and a held breath before that payoff.
type Who = 'AMAN' | 'RIYA';
type Line = {n: number; section: string; who: Who; start: number; end: number; words: {t: number; w: string}[]; tokens: Token[]; pre?: string | null; react?: string | null; reactWord?: string | null};
type Section = {id: string; label: string; tag: string; source: string; start: number; end: number; views: View[]};
type Timeline = {
  fps: number;
  durationInFrames: number;
  env: number[];
  brand: {names?: Record<string, string>; side?: Record<string, 'left' | 'right'>; site?: string};
  loop?: {text: string; answer?: string; until?: string} | null;
  payoff?: {beat: string; frame: number; pauseFrames: number} | null;
  lines: Line[];
  sections: Section[];
  beats: Record<string, number>;
  vars?: Record<string, number | string>;
};
const TL = timeline as unknown as Timeline;
const NAMES = TL.brand.names ?? {AMAN: 'AMAN', RIYA: 'RIYA'};
const SIDE = TL.brand.side ?? {AMAN: 'left', RIYA: 'right'};
const env = (f: number) => TL.env[Math.max(0, Math.min(TL.env.length - 1, f))] ?? 0;
const norm = (w: string) => w.toLowerCase().replace(/[^a-z0-9%]/g, '');
// One punch-in per line at most: on its last highlighted phrase (the stressed word).
const PUNCH = TL.lines.flatMap((l) => {
  const starts = l.tokens.filter((tok, i) => tok.pill && !l.tokens[i - 1]?.pill);
  return starts.length ? [Math.round(starts[starts.length - 1].t * TL.fps)] : [];
});
const TINTS = [V3.paper, '#EEF1EC', '#F1EEF4', '#EDF0F5', '#F3F0EA', '#EDEFF3'];
const LEAD = 10; // frames of pre-roll: frame 0 is a finished composition, not an empty stage
const PAYOFF = TL.payoff?.frame ?? (TL.loop?.until ? TL.beats[TL.loop.until] : undefined);

export type ReelProps = {showSafeZones: boolean; withAudio: boolean};

export const Reel: React.FC<ReelProps> = ({showSafeZones, withAudio}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const idx = Math.max(0, TL.lines.reduce((acc, ln, i) => (ln.start - 0.06 <= t ? i : acc), 0));
  const line = TL.lines[idx];
  const next = TL.lines[idx + 1];
  const si = Math.max(0, TL.sections.reduce((acc, s, i) => (s.start - 0.2 <= t ? i : acc), 0));
  const section = TL.sections[si];
  const talking = t >= line.start - 0.05 && t <= line.end + 0.12;
  const last = TL.lines[TL.lines.length - 1];

  // board motion: a 12% push-in that settles in the first half second, then a whip-in from the right
  // on every new section
  const secF = Math.round((section.start - 0.2) * fps);
  const sp0 = spring({frame: frame + 3, fps, config: {damping: 13, stiffness: 150, mass: 0.7}});
  const sp = spring({frame: frame - secF, fps, config: {damping: 16, stiffness: 150}});
  const sp1 = spring({frame: frame - secF - 1, fps, config: {damping: 16, stiffness: 150}});
  const boardX = si === 0 ? 0 : (1 - sp) * 1100;
  const blur = si === 0 ? 0 : Math.min(18, Math.abs(sp - sp1) * 260);
  const pill = si === 0 ? spring({frame: frame + LEAD, fps, config: {damping: 12, stiffness: 200}}) : spring({frame: frame - secF, fps, config: {damping: 12, stiffness: 200}});
  const sincePunch = PUNCH.reduce((acc, f) => (f <= frame ? frame - f : acc), 99);
  const punch = sincePunch < 12 ? 0.045 * (1 - spring({frame: sincePunch, fps, config: {damping: 9, stiffness: 240}})) : 0;
  const boardScale = (si === 0 ? 1 + 0.12 * (1 - sp0) : 1) * (1 + Math.max(0, punch));

  // cue words: what is spoken plus the caption tokens (for Hinglish the spoken words are Devanagari, so
  // cues are written against the Latin caption: "bleed", "wapas")
  const words = TL.lines
    .filter((l) => l.section === section.id)
    .flatMap((l) => [...l.words, ...l.tokens.map((k) => ({t: k.t, w: k.w}))])
    .sort((a, b) => a.t - b.t)
    .filter((x, i, all) => !all.slice(Math.max(0, i - 3), i).some((y) => norm(y.w) === norm(x.w) && Math.abs(y.t - x.t) < 0.02)); // a word and its identical caption token count once

  // acting: who shows which face, and since when (for the reaction kick)
  const faceOf = (who: Who): [string, number] => {
    if (talking && line.who === who) return [mouthFor(env(frame), env(frame - 1)), 99];
    // the beat before this character's next line (their laugh / gasp is in the audio there)
    if (next && next.who === who && next.pre && t > line.end + 0.06) return [next.pre, frame - Math.round((line.end + 0.06) * fps)];
    if (idx === 0 && line.who === who && line.pre && t < line.start) return [line.pre, frame];
    // listening: react to what the other one is saying (from `reactWord`, if given)
    if (line.who !== who && line.react) {
      const w = line.reactWord ? [...line.words, ...line.tokens].find((x) => norm(x.w).startsWith(norm(line.reactWord!))) : undefined;
      const from = w ? w.t : line.start;
      if (t >= from) return [line.react, frame - Math.round(from * fps)];
    }
    if (who === 'AMAN' && t > last.end + 0.1) return ['wink', frame - Math.round((last.end + 0.1) * fps)];
    return ['closed', 99];
  };
  const talk = (who: Who) => (talking && line.who === who ? env(frame) : 0);
  const [riyaFace, riyaSince] = faceOf('RIYA');
  const [amanFace, amanSince] = faceOf('AMAN');
  const riyaIn = spring({frame: frame + LEAD + 2, fps, config: {damping: 14}});
  const amanIn = spring({frame: frame + LEAD + 4, fps, config: {damping: 14}});
  const B = V3.board;
  const tint = TINTS[si % TINTS.length];

  // open loop: the question the hook raised stays pinned to the board until the payoff answers it
  const loop = TL.loop;
  const loopIn = spring({frame: frame - 20, fps, config: {damping: 11, stiffness: 200}});
  const solved = PAYOFF !== undefined && frame >= PAYOFF + 20;
  const solvedP = PAYOFF !== undefined ? spring({frame: frame - PAYOFF - 20, fps, config: {damping: 10, stiffness: 220}}) : 0;
  const loopGone = PAYOFF !== undefined ? Math.max(0, Math.min(1, (frame - PAYOFF - 75) / 10)) : 0;

  return (
    <SfxOn.Provider value={withAudio}>
      <AbsoluteFill style={{background: tint, overflow: 'hidden'}}>
        <AbsoluteFill style={{backgroundImage: 'radial-gradient(rgba(13,19,32,0.13) 1.6px, transparent 1.8px)', backgroundSize: '30px 30px', backgroundPosition: `${-frame * 0.4}px 0px`}} />
        <Sfx name="thump" t={frame} />
        {si > 0 ? <Sfx name="whoosh" t={frame - secF} /> : null}
        {/* payoff: riser → held breath → hit */}
        {TL.payoff ? <Sfx name="riser" t={frame - (TL.payoff.frame - TL.payoff.pauseFrames - 19)} volume={0.26} /> : null}
        {TL.payoff ? <Sfx name="thump" t={frame - TL.payoff.frame} volume={0.5} /> : null}

        {/* section pill */}
        <div style={{position: 'absolute', left: loop ? 150 * (1 - loopGone) : 0, right: 0, top: V3.pill.y, display: 'flex', justifyContent: 'center'}}>
          <div style={{padding: '10px 28px', borderRadius: 999, background: C.gold, border: V3.outline, boxShadow: '4px 4px 0 #0D1320', fontFamily: body, fontWeight: 800, fontSize: 32, letterSpacing: '0.08em', color: C.ink, whiteSpace: 'nowrap', transform: `scale(${pill}) rotate(${(1 - pill) * -8}deg)`}}>{section.label}</div>
        </div>

        {/* proof board */}
        <div style={{position: 'absolute', left: B.x, top: B.y, width: B.w, height: B.h, transform: `translateX(${boardX}px) scale(${boardScale})`, filter: blur > 0.4 ? `blur(${blur.toFixed(1)}px)` : undefined}}>
          <div style={{position: 'absolute', inset: 0, borderRadius: 34, background: '#fff', border: V3.outline, boxShadow: '9px 9px 0 #0D1320', overflow: 'hidden'}}>
            <div style={{height: 46, borderBottom: V3.outline, display: 'flex', alignItems: 'center', gap: 10, padding: '0 20px', background: '#F7F8FA'}}>
              {['#FF5F57', '#FEBC2E', '#28C840'].map((c) => (
                <span key={c} style={{width: 16, height: 16, borderRadius: '50%', background: c, border: '2px solid #0D1320'}} />
              ))}
              <span style={{marginLeft: 12, fontFamily: body, fontWeight: 700, fontSize: 20, color: C.muted}}>{TL.brand.site ?? 'adsworm.com · explained simply'}</span>
            </div>
            <div style={{position: 'absolute', left: 40, right: 40, top: 62, bottom: 50}}>
              <Views views={section.views ?? []} beats={TL.beats} frame={frame} vars={TL.vars ?? {}} words={words} fps={fps} lead={si === 0 ? LEAD : 0} />
            </div>
            {section.source ? <div style={{position: 'absolute', left: 28, right: 28, bottom: 12, fontFamily: body, fontSize: 18, lineHeight: 1.2, color: C.muted, textAlign: 'center'}}>{section.source}</div> : null}
          </div>
        </div>

        {/* open-loop chip, hanging off the board's top-left corner */}
        {loop && loopGone < 1 ? (
          <div style={{position: 'absolute', left: B.x - 14, top: B.y - 34, zIndex: 6, opacity: 1 - loopGone, transform: `rotate(-5deg) scale(${loopIn * (1 + 0.12 * Math.max(0, 1 - Math.abs(solvedP - 0.5) * 2))})`, transformOrigin: '0 50%'}}>
            {PAYOFF !== undefined ? <Sfx name="ding" t={frame - PAYOFF - 20} volume={0.22} /> : null}
            <div style={{display: 'flex', alignItems: 'center', gap: 10, padding: '8px 18px 8px 10px', borderRadius: 16, background: solved ? C.green : V3.pink, color: '#fff', border: V3.outline, boxShadow: '5px 5px 0 #0D1320', fontFamily: body, fontWeight: 800, fontSize: 30, whiteSpace: 'nowrap'}}>
              <span style={{width: 40, height: 40, borderRadius: '50%', background: '#fff', color: solved ? C.green : V3.pink, fontWeight: 900, fontSize: 30, lineHeight: '40px', textAlign: 'center', transform: solved ? undefined : `rotate(${Math.sin(frame / 9) * 10}deg)`}}>{solved ? '✓' : '?'}</span>
              {solved ? (loop.answer ?? 'answered') : loop.text}
            </div>
          </div>
        ) : null}

        <Bubble tokens={line.tokens} who={line.who} name={NAMES[line.who] ?? line.who} side={SIDE[line.who] ?? 'left'} t={t} fps={fps} />

        <Bust who="riya" x={V3.riya.x} y={V3.riya.y} size={V3.riya.size} face={riyaFace} faceSince={riyaSince} talk={talk('RIYA')} active={line.who === 'RIYA' && talking} t={t} enter={riyaIn} />
        <Bust who="aman" x={V3.aman.x} y={V3.aman.y} size={V3.aman.size} face={amanFace} faceSince={amanSince} talk={talk('AMAN')} active={line.who === 'AMAN' && talking} t={t} enter={amanIn} />

        {withAudio ? <Html5Audio src={staticFile('voice.wav')} /> : null}
        {showSafeZones ? <SafeZoneOverlay /> : null}
      </AbsoluteFill>
    </SfxOn.Provider>
  );
};
