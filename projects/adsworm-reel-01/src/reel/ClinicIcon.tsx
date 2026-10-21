import {C} from './theme';

// Minimal clinic mark: a building with a medical cross. Stroke scales with size.
export const ClinicIcon: React.FC<{size: number; color?: string; fill?: string}> = ({size, color = C.paper, fill = 'none'}) => (
  <svg width={size} height={size} viewBox="0 0 100 100" style={{display: 'block'}}>
    <path d="M14 88 V40 L50 14 L86 40 V88 Z" fill={fill} stroke={color} strokeWidth={6} strokeLinejoin="round" />
    <path d="M50 44 V72 M36 58 H64" stroke={fill === 'none' ? color : C.ink} strokeWidth={8} strokeLinecap="round" />
  </svg>
);
