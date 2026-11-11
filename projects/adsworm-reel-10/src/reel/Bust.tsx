import {Img, staticFile} from 'remotion';

// Talking head. While speaking: three mouth frames (closed / half / open, aligned by scripts/faces.py)
// picked from the speaker's loudness each frame, so the mouth moves with the voice. While listening or
// in the beat before a line: a full-face expression (shock, laugh, doubt…) — the reaction is half the
// joke. A new expression pops (small scale kick) so the eye catches it.
export type Mouth = 'closed' | 'half' | 'open';
export const FACES: Record<string, string[]> = {
  aman: ['closed', 'half', 'open', 'wink', 'laugh', 'surprised'],
  riya: ['closed', 'half', 'open', 'shock', 'laugh', 'doubt', 'worry'],
};
export const mouthFor = (env: number, prev: number): Mouth => {
  const e = (env + prev) / 2;
  return e > 0.42 ? 'open' : e > 0.14 ? 'half' : 'closed';
};

type Props = {who: string; x: number; y: number; size: number; face: string; faceSince: number; talk: number; active: boolean; t: number; enter: number};
export const Bust: React.FC<Props> = ({who, x, y, size, face, faceSince, talk, active, t, enter}) => {
  const frames = FACES[who] ?? ['closed', 'half', 'open'];
  const shown = frames.includes(face) ? face : 'closed';
  const expressive = !['closed', 'half', 'open'].includes(shown);
  const breathe = 1 + 0.006 * Math.sin(t * 2.1 + (who === 'riya' ? 1 : 0));
  const bob = active ? -talk * 10 : 0;
  const tilt = active ? Math.sin(t * 3.1) * 1.4 : Math.sin(t * 0.9) * 0.6;
  // reaction kick: 1.07 → 1 over ~8 frames, with a tiny shake for shock/worry
  const k = expressive && faceSince >= 0 && faceSince < 9 ? 1 - faceSince / 9 : 0;
  const kick = 1 + 0.07 * k * k;
  const shake = (shown === 'shock' || shown === 'worry') && k > 0 ? Math.sin(faceSince * 2.4) * 7 * k : 0;
  const lit = active || expressive;
  return (
    <div
      style={{
        position: 'absolute',
        left: x + shake,
        top: y + (1 - enter) * 420,
        width: size,
        height: size,
        transformOrigin: '50% 100%',
        transform: `translateY(${bob}px) rotate(${tilt}deg) scale(${breathe * (lit ? 1 : 0.95) * kick})`,
        filter: `drop-shadow(0 18px 30px rgba(13,19,32,0.25)) brightness(${lit ? 1 : 0.92})`,
      }}
    >
      {frames.map((m) => (
        <Img key={m} src={staticFile(`faces/${who}-${m}.png`)} style={{position: 'absolute', inset: 0, width: '100%', height: '100%', opacity: m === shown ? 1 : 0}} />
      ))}
    </div>
  );
};
