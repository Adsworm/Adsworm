export type Token = { t: string; hl: boolean };

export type CaptionPage = {
  startMs: number;
  endMs: number;
  lines: Token[][];
  text: string;
  hero?: boolean; // editorial treatment: the accent words set large in the serif
};

export type OverlayProps = {
  pages: CaptionPage[];
  contentFrames: number; // length of the edited testimonial
  endCardFrames: number; // 0 = no end card
  fps: number;
  label?: { text: string; fromFrame: number; toFrame: number } | null;
};
