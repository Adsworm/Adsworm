import {Img, staticFile} from 'remotion';

// Talking head: three mouth frames (closed / half / open, aligned by scripts/faces.py) picked from the
// speaker's loudness each frame, so the mouth moves with the voice. Wink frame for the sign-off.
export type Mouth = 'closed' | 'half' | 'open' | 'wink';
export const mouthFor = (env: number, prev: number): Mouth => {
  const e = (env + prev) / 2;
  return e > 0.42 ? 'open' : e > 0.14 ? 'half' : 'closed';
};

export const Bust: React.FC<{who: string; x: number; y: number; size: number; mouth: Mouth; talk: number; active: boolean; t: number; enter: number; flip?: boolean}> = ({who, x, y, size, mouth, talk, active, t, enter, flip}) => {
  const breathe = 1 + 0.006 * Math.sin(t * 2.1 + (flip ? 1 : 0));
  const bob = active ? -talk * 10 : 0;
  const tilt = active ? Math.sin(t * 3.1) * 1.4 : Math.sin(t * 0.9) * 0.6;
  const dim = active ? 1 : 0.9;
  return (
    <div style={{position: 'absolute', left: x, top: y + (1 - enter) * 420, width: size, height: size, transformOrigin: '50% 100%', transform: `translateY(${bob}px) rotate(${tilt}deg) scale(${breathe * (active ? 1 : 0.95)}) scaleX(${flip ? -1 : 1})`, filter: `drop-shadow(0 18px 30px rgba(13,19,32,0.25)) brightness(${dim})`}}>
      {(['closed', 'half', 'open', 'wink'] as Mouth[]).map((m) => (
        <Img key={m} src={staticFile(`faces/${who}-${m === 'wink' && who !== 'aman' ? 'half' : m}.png`)} style={{position: 'absolute', inset: 0, width: '100%', height: '100%', opacity: m === mouth ? 1 : 0}} />
      ))}
    </div>
  );
};
