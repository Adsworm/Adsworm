import {Composition} from 'remotion';
import {Reel, type ReelProps} from './reel/Reel';
import {TL} from './reel/tl';

export const RemotionRoot: React.FC = () => (
  <Composition id="Explainer" component={Reel} width={1080} height={1920} fps={TL.fps} durationInFrames={TL.durationInFrames} defaultProps={{showSafeZones: false, withAudio: true} satisfies ReelProps} />
);
