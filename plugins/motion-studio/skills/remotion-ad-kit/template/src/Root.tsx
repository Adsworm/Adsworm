import {Composition, Folder} from 'remotion';
import {Ad, FPS, totalFrames} from './Ad';
import {adSchema, defaultAdProps} from './schema';
import {STATIC_FRAMES, StaticAd} from './StaticAd';

// One prop set → every Meta placement, as video and as static. Compose for 9:16 first; the layout adapts.
export const FORMATS = [
  {id: '9x16', width: 1080, height: 1920},
  {id: '4x5', width: 1080, height: 1350},
  {id: '1x1', width: 1080, height: 1080},
  {id: '16x9', width: 1920, height: 1080},
];

export const RemotionRoot: React.FC = () => (
  <>
    <Folder name="Ads">
      {FORMATS.map((f) => (
        <Composition
          key={f.id}
          id={`Ad-${f.id}`}
          component={Ad}
          width={f.width}
          height={f.height}
          fps={FPS}
          durationInFrames={totalFrames(defaultAdProps)}
          schema={adSchema}
          defaultProps={defaultAdProps}
          calculateMetadata={({props}) => ({durationInFrames: totalFrames(props)})}
        />
      ))}
    </Folder>
    <Folder name="Statics">
      {FORMATS.map((f) => (
        <Composition
          key={f.id}
          id={`Static-${f.id}`}
          component={StaticAd}
          width={f.width}
          height={f.height}
          fps={FPS}
          durationInFrames={STATIC_FRAMES}
          schema={adSchema}
          defaultProps={defaultAdProps}
        />
      ))}
    </Folder>
  </>
);
