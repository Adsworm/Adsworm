import {useCurrentFrame} from 'remotion';
import {sans} from '../lib/fonts';
import {ease, progress} from '../lib/motion';

export const StatCounter: React.FC<{
  value: number;
  prefix: string;
  suffix: string;
  label: string;
  numberSize: number;
  labelSize: number;
  color: string;
  labelColor: string;
  lineColor: string;
  width?: number;
  delay?: number;
}> = ({value, prefix, suffix, label, numberSize, labelSize, color, labelColor, lineColor, width, delay = 0}) => {
  const frame = useCurrentFrame();
  const p = progress(frame, delay, 42, ease.outExpo);
  const decimals = (String(value).split('.')[1] ?? '').length;
  const enter = progress(frame, delay, 18);
  return (
    <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center', width, opacity: enter}}>
      <div
        style={{
          fontFamily: sans,
          fontWeight: 800,
          fontSize: numberSize,
          letterSpacing: '-0.05em',
          lineHeight: 1,
          color,
          fontVariantNumeric: 'tabular-nums',
          whiteSpace: 'nowrap',
          transform: `translateY(${(1 - enter) * 30}px)`,
        }}
      >
        {prefix}
        {(value * p).toFixed(decimals)}
        {suffix}
      </div>
      <div style={{height: 3, width: numberSize * 1.2 * progress(frame, delay + 10, 30), background: lineColor, margin: `${labelSize * 0.6}px 0`}} />
      <div style={{fontFamily: sans, fontWeight: 600, fontSize: labelSize, color: labelColor, letterSpacing: '0.01em', textAlign: 'center', opacity: progress(frame, delay + 14, 20)}}>
        {label}
      </div>
    </div>
  );
};
