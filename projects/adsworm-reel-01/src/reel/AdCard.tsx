import {sans} from '../lib/fonts';
import {C} from './theme';

// A deliberately generic local-clinic ad: the category's default, not anyone's real creative.
export const AdCard: React.FC<{
  treatment: string;
  subline?: string;
  altSubline?: string;
  swap?: number; // 0→1 crossfade subline → altSubline
  strike?: number; // 0→1 lime strike across the discount badge
  badge?: number; // discount badge opacity — fade to 0 once the strike has made its point
  city?: number; // 0→1 city tag pop
  week?: string; // W1/W2/W3 chip
  photoTint?: string;
}> = ({treatment, subline = 'Clinic Name', altSubline, swap = 0, strike = 0, badge = 1, city = 0, week, photoTint = '#9C9C9C'}) => (
  <div
    style={{
      position: 'relative',
      width: 520,
      height: 680,
      borderRadius: 28,
      background: '#FFFFFF',
      boxShadow: '0 30px 80px rgba(0,0,0,0.45)',
      overflow: 'visible',
      fontFamily: sans,
    }}
  >
    <div style={{height: 360, borderRadius: '28px 28px 0 0', overflow: 'hidden', position: 'relative', background: `linear-gradient(160deg, #C9C9C9, ${photoTint})`}}>
      {/* faceless placeholder "model" */}
      <div style={{position: 'absolute', left: 190, top: 70, width: 140, height: 140, borderRadius: '50%', background: 'rgba(255,255,255,0.35)'}} />
      <div style={{position: 'absolute', left: 120, top: 230, width: 280, height: 220, borderRadius: '140px 140px 0 0', background: 'rgba(255,255,255,0.35)'}} />
      <div
        style={{
          position: 'absolute',
          left: 26,
          top: 26,
          padding: '10px 18px',
          borderRadius: 10,
          background: '#E53935',
          color: '#fff',
          fontWeight: 800,
          fontSize: 34,
          letterSpacing: '-0.02em',
          transform: 'rotate(-3deg)',
          opacity: badge,
        }}
      >
        FLAT 20% OFF
        <div style={{position: 'absolute', left: -6, top: '50%', height: 7, borderRadius: 4, width: `${strike * 104}%`, background: C.lime, transform: 'translateY(-50%) rotate(-4deg)'}} />
      </div>
    </div>
    <div style={{padding: '26px 30px'}}>
      <div style={{fontSize: 48, fontWeight: 800, color: '#111', letterSpacing: '-0.03em'}}>{treatment}</div>
      <div style={{position: 'relative', height: 44, marginTop: 6}}>
        <div style={{position: 'absolute', fontSize: 30, color: '#777', opacity: 1 - swap}}>{subline}</div>
        {altSubline ? (
          <div style={{position: 'absolute', fontSize: 32, fontWeight: 700, color: '#111', opacity: swap, transform: `translateY(${(1 - swap) * 16}px)`}}>
            {altSubline}
          </div>
        ) : null}
      </div>
      <div style={{marginTop: 30, height: 78, borderRadius: 14, background: '#1877F2', color: '#fff', fontWeight: 700, fontSize: 32, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
        Book now
      </div>
    </div>
    {city > 0 ? (
      <div
        style={{
          position: 'absolute',
          right: -26,
          top: 300,
          display: 'flex',
          alignItems: 'center',
          gap: 10,
          padding: '14px 24px',
          borderRadius: 999,
          background: C.lime,
          color: C.ink,
          fontWeight: 800,
          fontSize: 38,
          letterSpacing: '0.04em',
          transform: `scale(${city}) rotate(-6deg)`,
          boxShadow: '0 12px 30px rgba(0,0,0,0.35)',
        }}
      >
        <svg width={30} height={36} viewBox="0 0 30 36">
          <path d="M15 34 C15 34 3 21 3 13 A12 12 0 0 1 27 13 C27 21 15 34 15 34 Z" fill={C.ink} />
          <circle cx={15} cy={13} r={4.5} fill={C.lime} />
        </svg>
        PUNE
      </div>
    ) : null}
    {week ? (
      <div style={{position: 'absolute', left: 22, top: -26, padding: '8px 20px', borderRadius: 999, background: C.ink, color: C.lime, fontWeight: 800, fontSize: 36, border: `3px solid ${C.lime}`}}>
        {week}
      </div>
    ) : null}
  </div>
);
