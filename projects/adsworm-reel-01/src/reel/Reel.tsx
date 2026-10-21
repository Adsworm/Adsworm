import {AbsoluteFill, Html5Audio, staticFile, useCurrentFrame} from 'remotion';
import {Grain} from '../components/Grain';
import {SafeZoneOverlay} from '../components/SafeZoneOverlay';
import {CTA} from './scenes/CTA';
import {End} from './scenes/End';
import {Fix} from './scenes/Fix';
import {Hook} from './scenes/Hook';
import {Problem} from './scenes/Problem';
import {Proof} from './scenes/Proof';
import {Shift} from './scenes/Shift';
import {C} from './theme';

// Scene windows in absolute frames (storyboard.md). Scenes read the absolute frame directly so
// every number in the code matches the storyboard and timeline.json cues.
const SCENES: [number, number, React.FC][] = [
  [0, 120, Hook],
  [120, 300, Problem],
  [300, 420, Shift],
  [420, 660, Fix],
  [660, 780, Proof],
  [780, 960, CTA],
  [960, 1020, End],
];

export type ReelProps = {showSafeZones: boolean; withAudio: boolean};

export const Reel: React.FC<ReelProps> = ({showSafeZones, withAudio}) => {
  const frame = useCurrentFrame();
  const Scene = SCENES.find(([a, b]) => frame >= a && frame < b)?.[2];
  return (
    <AbsoluteFill style={{background: `radial-gradient(120% 70% at 50% 38%, #18181B 0%, ${C.ink} 65%)`}}>
      {Scene ? <Scene /> : null}
      <Grain opacity={0.06} />
      {withAudio ? <Html5Audio src={staticFile('reel-audio.wav')} /> : null}
      {showSafeZones ? <SafeZoneOverlay /> : null}
    </AbsoluteFill>
  );
};
