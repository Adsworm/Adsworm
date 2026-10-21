import {AbsoluteFill, Html5Audio, interpolate, staticFile, useCurrentFrame} from 'remotion';
import {Grain} from '../components/Grain';
import {SafeZoneOverlay} from '../components/SafeZoneOverlay';
import {body} from '../lib/fonts';
import {progress} from '../lib/motion';
import {End} from './scenes/End';
import {Hook} from './scenes/Hook';
import {Lesson} from './scenes/Lesson';
import {Manifesto} from './scenes/Manifesto';
import {Proof} from './scenes/Proof';
import {Signals} from './scenes/Signals';
import {Stats} from './scenes/Stats';
import {Why} from './scenes/Why';
import {Stage} from './Stage';
import {C} from './theme';

// Scene windows in absolute frames (storyboard.md); scenes read the absolute frame directly.
const SCENES: [number, number, React.FC][] = [
  [0, 120, Hook],
  [120, 240, Why],
  [240, 420, Signals],
  [420, 600, Lesson],
  [600, 720, Proof],
  [720, 810, Stats],
  [810, 900, Manifesto],
  [900, 1020, End],
];

export type ReelProps = {showSafeZones: boolean; withAudio: boolean};

export const Reel: React.FC<ReelProps> = ({showSafeZones, withAudio}) => {
  const frame = useCurrentFrame();
  const Scene = SCENES.find(([a, b]) => frame >= a && frame < b)?.[2];
  // Lighting cues: a hit of light on frame 0, a lift on "CHOSEN.", a full bloom on "EMPIRES."
  const flare =
    interpolate(frame, [0, 24], [0.6, 0], {extrapolateRight: 'clamp'}) +
    progress(frame, 465, 6) * (1 - progress(frame, 475, 40)) * 0.4 +
    progress(frame, 840, 8) * (1 - progress(frame, 852, 45));
  const dim = frame >= 420 && frame < 600 ? 0.5 : 0;
  const gridGlow = frame >= 600 && frame < 810 ? progress(frame, 606, 30) : 0;
  return (
    <AbsoluteFill style={{background: C.bg}}>
      <Stage flare={Math.min(1, flare)} dim={dim} gridGlow={gridGlow} />
      {Scene ? <Scene /> : null}
      {frame < 900 ? (
        <div style={{position: 'absolute', top: 276, width: '100%', textAlign: 'center', fontFamily: body, fontWeight: 600, fontSize: 28, letterSpacing: '0.24em', color: C.muted, opacity: 0.8}}>
          @ADSWORM
        </div>
      ) : null}
      <Grain opacity={0.05} />
      {withAudio ? <Html5Audio src={staticFile('reel-audio.wav')} /> : null}
      {showSafeZones ? <SafeZoneOverlay /> : null}
    </AbsoluteFill>
  );
};
