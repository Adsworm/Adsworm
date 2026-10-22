import {spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {body} from '../lib/fonts';
import {ease, progress, springs} from '../lib/motion';
import {BUBBLE, C} from './theme';

export type Line = {n: number; who: string; show: string; pills: [number, number][]; start: number; end: number; beat: string | null; pose: string | null};

// Speech bubble with a speaker tag; highlighted words sit in blue pills. The tail points at whoever is talking.
export const Caption: React.FC<{line: Line; names: Record<string, string>; sideOf: Record<string, 'left' | 'right'>; settled?: boolean}> = ({line, names, sideOf, settled = false}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const startF = Math.round(line.start * fps);
  const s = settled ? 1 : spring({frame: frame - startF, fps, config: springs.snappy});
  const side = sideOf[line.who] ?? 'right';
  const words = line.show.split(' ');
  const inPill = (i: number) => line.pills.some(([a, b]) => i >= a && i < b);
  const pillStart = (i: number) => line.pills.some(([a]) => a === i);
  const pillEnd = (i: number) => line.pills.some(([, b]) => b === i + 1);
  const tagLeft = side === 'left';
  return (
    <div style={{position: 'absolute', left: BUBBLE.x, top: BUBBLE.y, width: BUBBLE.w, opacity: Math.min(1, s * 1.4), transform: `translateY(${(1 - s) * 26}px) scale(${0.96 + s * 0.04})`, transformOrigin: 'center bottom'}}>
      <div
        style={{
          position: 'relative',
          minHeight: BUBBLE.minH,
          background: C.card,
          borderRadius: 34,
          boxShadow: '0 18px 50px rgba(13,19,32,0.10)',
          padding: '38px 44px 34px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          textAlign: 'center',
          fontFamily: body,
          fontWeight: 700,
          fontSize: line.show.length > 52 ? 44 : 50,
          lineHeight: 1.3,
          color: C.ink,
          letterSpacing: '-0.015em',
        }}
      >
        <div>
          {words.map((raw, i) => {
            const pill = inPill(i);
            // Trailing punctuation on a pill's last word is drawn outside the pill.
            const m = pill && pillEnd(i) ? /^(.*?)([.,!?;:…]*)$/.exec(raw) : null;
            const w = m ? m[1] : raw;
            const tail = m ? m[2] : '';
            const last = i === words.length - 1;
            return (
              <span key={i}>
                <span
                  style={
                    pill
                      ? {
                          background: C.blue,
                          color: '#fff',
                          padding: '2px 0',
                          paddingLeft: pillStart(i) ? 14 : 0,
                          paddingRight: pillEnd(i) ? 14 : 0,
                          borderRadius: pillStart(i) && pillEnd(i) ? 14 : pillStart(i) ? '14px 0 0 14px' : pillEnd(i) ? '0 14px 14px 0' : 0,
                          boxDecorationBreak: 'clone',
                          WebkitBoxDecorationBreak: 'clone',
                        }
                      : {}
                  }
                >
                  {w}
                  {pill && !pillEnd(i) ? ' ' : ''}
                </span>
                {tail}
                {!last && !(pill && !pillEnd(i)) ? ' ' : ''}
              </span>
            );
          })}
        </div>
        {/* speaker tag */}
        <div
          style={{
            position: 'absolute',
            top: -22,
            [tagLeft ? 'left' : 'right']: 36,
            padding: '8px 18px 7px',
            borderRadius: 999,
            background: tagLeft ? C.ink : C.blue,
            color: '#fff',
            fontSize: 24,
            fontWeight: 800,
            letterSpacing: '0.12em',
          }}
        >
          {names[line.who] ?? line.who}
        </div>
        {/* tail */}
        <div
          style={{
            position: 'absolute',
            bottom: -18,
            [tagLeft ? 'left' : 'right']: 180,
            width: 40,
            height: 40,
            background: C.card,
            transform: 'rotate(45deg)',
            borderRadius: 6,
            boxShadow: '8px 8px 18px rgba(13,19,32,0.06)',
          }}
        />
      </div>
    </div>
  );
};

// Quiet fade for the gap between lines so the bubble never pops to empty.
export const captionAlpha = (frame: number, fps: number, line: Line | undefined, next: Line | undefined) => {
  if (!line) return 0;
  const endF = Math.round(line.end * fps);
  if (!next) return 1 - progress(frame, endF + 10, 12, ease.outQuart);
  return 1;
};
