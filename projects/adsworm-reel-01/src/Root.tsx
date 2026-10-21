import {Composition, Folder} from 'remotion';
import {Carousel} from './carousel/Carousel';
import {Reel, type ReelProps} from './reel/Reel';
import timeline from './reel/timeline.json';

export const RemotionRoot: React.FC = () => (
  <>
    <Composition
      id="FullChairs01"
      component={Reel}
      width={1080}
      height={1920}
      fps={timeline.fps}
      durationInFrames={timeline.durationInFrames}
      defaultProps={{showSafeZones: false, withAudio: true} satisfies ReelProps}
    />
    <Folder name="Carousel">
      {[1, 2, 3, 4, 5].map((n) => (
        <Composition key={n} id={`Carousel-${n}`} component={Carousel} width={1080} height={1350} fps={30} durationInFrames={1} defaultProps={{slide: n}} />
      ))}
    </Folder>
  </>
);
