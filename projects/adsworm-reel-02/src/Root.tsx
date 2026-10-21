import {Composition} from 'remotion';
import {Reel, type ReelProps} from './reel/Reel';
import timeline from './reel/timeline.json';

export const RemotionRoot: React.FC = () => (
  <Composition
    id="TheBestNeverWins"
    component={Reel}
    width={1080}
    height={1920}
    fps={timeline.fps}
    durationInFrames={timeline.durationInFrames}
    defaultProps={{showSafeZones: false, withAudio: true} satisfies ReelProps}
  />
);
