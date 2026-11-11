import {AbsoluteFill} from 'remotion';
import {useLayout} from '../lib/layout';

// Dev-only guide (props.showSafeZones). Red = platform UI covers it; keep text and logos out.
export const SafeZoneOverlay: React.FC = () => {
  const {pad} = useLayout();
  const red = 'rgba(255,0,60,0.28)';
  const label: React.CSSProperties = {color: 'white', fontFamily: 'monospace', fontSize: 22, padding: 12};
  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      <div style={{position: 'absolute', top: 0, left: 0, right: 0, height: pad.top, background: red, ...label}}>UNSAFE · platform UI</div>
      <div style={{position: 'absolute', bottom: 0, left: 0, right: 0, height: pad.bottom, background: red, ...label}}>UNSAFE · caption / CTA overlay</div>
      <div style={{position: 'absolute', top: pad.top, bottom: pad.bottom, left: 0, width: pad.side, background: red}} />
      <div style={{position: 'absolute', top: pad.top, bottom: pad.bottom, right: 0, width: pad.side, background: red}} />
    </AbsoluteFill>
  );
};
