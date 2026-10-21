import {useCurrentFrame} from 'remotion';
import {sans} from '../lib/fonts';
import {C} from './theme';

// Instagram-style comment composer typing a keyword, one letter every `every` frames from `at`.
export const CommentField: React.FC<{text: string; at: number; every?: number; sendAt: number}> = ({text, at, every = 5, sendAt}) => {
  const frame = useCurrentFrame();
  const shown = Math.max(0, Math.min(text.length, Math.floor((frame - at) / every) + 1));
  const typed = frame >= at ? text.slice(0, shown) : '';
  const caretOn = Math.floor(frame / 8) % 2 === 0;
  const sent = frame >= sendAt;
  return (
    <div
      style={{
        width: 900,
        height: 116,
        borderRadius: 999,
        background: '#1A1A1C',
        border: '2px solid rgba(255,255,255,0.18)',
        display: 'flex',
        alignItems: 'center',
        padding: '0 22px',
        gap: 22,
        fontFamily: sans,
      }}
    >
      <div style={{width: 72, height: 72, borderRadius: '50%', background: 'linear-gradient(135deg, #5A5A5F, #2C2C30)'}} />
      <div style={{flex: 1, fontSize: 46, fontWeight: 700, color: typed ? C.paper : C.muted, letterSpacing: '0.02em'}}>
        {typed || 'Add a comment…'}
        {typed && !sent ? <span style={{display: 'inline-block', width: 4, height: 46, marginLeft: 6, verticalAlign: 'middle', background: C.lime, opacity: caretOn ? 1 : 0}} /> : null}
      </div>
      <div
        style={{
          width: 76,
          height: 76,
          borderRadius: '50%',
          background: sent ? C.lime : 'rgba(255,255,255,0.12)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          transform: `scale(${sent ? 1.06 : 1})`,
        }}
      >
        <svg width={34} height={34} viewBox="0 0 24 24">
          <path d="M3 12 L21 4 L14 21 L11 13 Z" fill={sent ? C.ink : C.muted} />
        </svg>
      </div>
    </div>
  );
};
