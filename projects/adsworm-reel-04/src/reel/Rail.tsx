import {body, display} from '../lib/fonts';
import {C, L} from './theme';
import type {Room} from './tl';

// "3 things" progress rail. Each segment fills while its room plays.
const SEGS = [
  {id: 'one', label: 'IMAGE → VIDEO'},
  {id: 'two', label: 'GEM'},
  {id: 'three', label: 'WHATSAPP'},
];
export const Rail: React.FC<{rooms: Room[]; t: number; show: number}> = ({rooms, t, show}) => (
  <div style={{position: 'absolute', left: 90, right: 150, top: L.rail.y, display: 'flex', gap: 12, opacity: show, transform: `translateY(${(1 - show) * -16}px)`}}>
    {SEGS.map((s, i) => {
      const r = rooms.find((x) => x.id === s.id);
      const p = r ? Math.min(1, Math.max(0, (t - r.start) / (r.end - r.start))) : 0;
      const on = p > 0 && p < 1;
      return (
        <div key={s.id} style={{flex: 1, display: 'flex', flexDirection: 'column', gap: 8}}>
          <div style={{height: 6, borderRadius: 3, background: 'rgba(240,238,232,0.14)', overflow: 'hidden'}}>
            <div style={{width: `${p * 100}%`, height: '100%', background: p >= 1 ? C.gold : C.blueBright, boxShadow: on ? `0 0 14px ${C.blueBright}` : undefined}} />
          </div>
          <div style={{display: 'flex', gap: 8, alignItems: 'baseline', opacity: on ? 1 : p >= 1 ? 0.75 : 0.4}}>
            <span style={{fontFamily: display, fontSize: 28, color: p >= 1 ? C.gold : C.cream, lineHeight: 1}}>0{i + 1}</span>
            <span style={{fontFamily: body, fontWeight: 700, fontSize: 18, letterSpacing: '0.1em', color: C.cream}}>{s.label}</span>
          </div>
        </div>
      );
    })}
  </div>
);
