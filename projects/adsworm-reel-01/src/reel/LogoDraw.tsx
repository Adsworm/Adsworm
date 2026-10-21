import {getLength} from '@remotion/paths';
import {useCurrentFrame} from 'remotion';
import {ease, progress} from '../lib/motion';
import {LOGO_PATH, LOGO_VIEWBOX} from './logo-path';
import {C} from './theme';

const LENGTH = getLength(LOGO_PATH);

// Outline draws on, then the fill lands — the mark "writes itself".
export const LogoDraw: React.FC<{at: number; width: number}> = ({at, width}) => {
  const frame = useCurrentFrame();
  const draw = progress(frame, at, 30, ease.inOutQuart);
  const fill = progress(frame, at + 24, 14, ease.outQuart);
  return (
    <svg width={width} viewBox={LOGO_VIEWBOX} style={{overflow: 'visible'}}>
      <path
        d={LOGO_PATH}
        fill={C.paper}
        fillOpacity={fill}
        stroke={C.paper}
        strokeWidth={4}
        strokeDasharray={LENGTH}
        strokeDashoffset={LENGTH * (1 - draw)}
        strokeOpacity={1 - fill * 0.8}
      />
    </svg>
  );
};
