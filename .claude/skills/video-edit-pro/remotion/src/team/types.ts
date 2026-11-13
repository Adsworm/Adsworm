export type TeamLine = { text: string; gold: boolean };
export type TeamPage = { startMs: number; endMs: number; lines: TeamLine[]; logo?: boolean };
export type TeamProps = {
  fps: number;
  contentFrames: number;
  endCardFrames: number;
  pages: TeamPage[];
  pill?: { text: string; fromMs: number; toMs: number } | null;
};
