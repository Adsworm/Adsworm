import {createContext, useContext} from 'react';
import {Html5Audio, Sequence, staticFile, useCurrentFrame} from 'remotion';

// Sound follows picture: a component that draws something plays its own effect.
//   <Sfx name="pop" t={t} />        t = frames since the thing appeared (−1 = not yet)
// Files come from scripts/sfx.py (public/sfx/*.wav). Lengths in frames at 30 fps.
const LEN = {pop: 4, tick: 3, whoosh: 13, swish: 6, thump: 15, ding: 18, buzz: 7, riser: 18, huh: 6, gasp: 7, cash: 16} as const;
export type SfxName = keyof typeof LEN;
// Levels: effects peak at least 6 dB under the voice (voice peaks ≈ 0.9, files peak 0.8).
const VOL: Record<SfxName, number> = {pop: 0.28, tick: 0.16, whoosh: 0.24, swish: 0.18, thump: 0.5, ding: 0.18, buzz: 0.22, riser: 0.2, huh: 0.22, gasp: 0.18, cash: 0.18};
// Listeners tune out a repeated effect, so pops and dings never play at the same pitch twice running.
const PITCH = [1, 1.12, 0.94, 1.19, 1.06];
const VARY: SfxName[] = ['pop', 'ding', 'swish', 'tick'];

export const SfxOn = createContext(true);

export const Sfx: React.FC<{name: SfxName; t: number; delay?: number; volume?: number; rate?: number}> = ({name, t, delay = 0, volume, rate}) => {
  const frame = useCurrentFrame();
  const on = useContext(SfxOn);
  if (!on || t < 0) return null;
  const at = frame - t + delay;
  const r = rate ?? (VARY.includes(name) ? PITCH[Math.abs(Math.round(at / 7)) % PITCH.length] : 1);
  const len = Math.ceil(LEN[name] / r);
  if (at < 0 || frame < at || frame >= at + len) return null;
  return (
    <Sequence from={at} durationInFrames={len} layout="none">
      <Html5Audio src={staticFile(`sfx/${name}.wav`)} volume={volume ?? VOL[name]} playbackRate={r} />
    </Sequence>
  );
};
