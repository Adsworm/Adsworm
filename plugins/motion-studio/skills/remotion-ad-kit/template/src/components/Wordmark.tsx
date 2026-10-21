import {Img, staticFile, useCurrentFrame} from 'remotion';
import {sans} from '../lib/fonts';
import {ease, progress} from '../lib/motion';

// Logo file if provided, otherwise a tracked-out wordmark that tightens into place.
export const Wordmark: React.FC<{name: string; logo: string; size: number; color: string; delay?: number}> = ({
  name,
  logo,
  size,
  color,
  delay = 0,
}) => {
  const p = progress(useCurrentFrame(), delay, 36, ease.outExpo);
  if (logo) {
    return <Img src={staticFile(logo)} style={{height: size * 1.6, opacity: p, transform: `scale(${0.9 + p * 0.1})`}} />;
  }
  return (
    <div
      style={{
        fontFamily: sans,
        fontWeight: 600,
        fontSize: size,
        letterSpacing: `${0.6 - p * 0.38}em`,
        color,
        opacity: p,
        filter: `blur(${(1 - p) * 8}px)`,
        whiteSpace: 'nowrap',
      }}
    >
      {name}
    </div>
  );
};
