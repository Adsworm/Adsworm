import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import {Headline} from '../Headline';
import {SAFE} from '../theme';

const Center: React.FC<{children: React.ReactNode; scale?: number}> = ({children, scale = 1}) => (
  <AbsoluteFill style={{top: SAFE.top, height: SAFE.bottom - SAFE.top, justifyContent: 'center', alignItems: 'center', transform: `scale(${scale})`}}>
    {children}
  </AbsoluteFill>
);

// Exactly what frame 0 shows (also the loop-back target).
export const HookStill: React.FC<{scale?: number}> = ({scale = 1}) => (
  <Center scale={scale}>
    <Headline lines={['THE BEST', '*NEVER WINS.*']} size={215} at={0} set />
  </Center>
);

export const Hook: React.FC = () => {
  const frame = useCurrentFrame();
  if (frame < 60) return <HookStill scale={interpolate(frame, [0, 59], [1, 1.05])} />;
  return (
    <Center scale={interpolate(frame, [60, 119], [1, 1.04])}>
      <Headline lines={['WORSE PRODUCT.', '*MORE CUSTOMERS.*']} size={170} at={60} stagger={9} />
    </Center>
  );
};
