import timeline from './timeline.json';

export type Word = {w: string; s: number; e: number; hi: boolean};
export type Line = {who: 'AMAN' | 'ALGO'; room: string; snap: 'says' | 'translates' | null; start: number; end: number; words: Word[]};
export type Room = {id: string; start: number; end: number};
type TL = {fps: number; durationInFrames: number; lines: Line[]; rooms: Room[]; env: number[]; vars: {days: number | null; countdownLabel: string}};
export const TL = timeline as unknown as TL;

/** Index of the line being spoken (or the last one spoken) at time t. */
export const lineIndexAt = (t: number) => Math.max(0, TL.lines.reduce((acc, ln, i) => (ln.start - 0.05 <= t ? i : acc), 0));
export const roomAt = (t: number) => TL.rooms.reduce((acc, r) => (r.start - 0.25 <= t ? r : acc), TL.rooms[0]);
/** Seconds since the first word in `room` that matches `word` (−1 before it). */
export const sinceWord = (t: number, room: string, word: string, nth = 0) => {
  const hits = TL.lines.filter((l) => l.room === room).flatMap((l) => l.words).filter((w) => w.w.toLowerCase().replace(/[^a-z0-9%.+,]/g, '').startsWith(word.toLowerCase()));
  const w = hits[nth];
  return w && t >= w.s ? t - w.s : -1;
};
/** Seconds since line `i` started (−1 before). */
export const sinceLine = (t: number, i: number) => (TL.lines[i] && t >= TL.lines[i].start ? t - TL.lines[i].start : -1);
export const envAt = (frame: number) => TL.env[Math.max(0, Math.min(TL.env.length - 1, frame))] ?? 0;
/** Smoothed loudness of one speaker only (0 when the other one talks). */
export const talkEnv = (frame: number, who: 'AMAN' | 'ALGO') => {
  const t = frame / TL.fps;
  const ln = TL.lines[lineIndexAt(t)];
  if (!ln || ln.who !== who || t > ln.end + 0.1) return 0;
  return (envAt(frame) + envAt(frame - 1) + envAt(frame - 2)) / 3;
};
