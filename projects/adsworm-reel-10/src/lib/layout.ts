import {useVideoConfig} from 'remotion';

export type Format = 'vertical' | 'portrait' | 'square' | 'landscape';

// Fractions of frame height/width kept free of text and logos.
// vertical = Meta Reels guidance (top 14%, bottom 35%, sides 6%) — UI overlays live there.
export const SAFE: Record<Format, {top: number; bottom: number; side: number}> = {
  vertical: {top: 0.14, bottom: 0.35, side: 0.06},
  portrait: {top: 0.06, bottom: 0.06, side: 0.06},
  square: {top: 0.06, bottom: 0.06, side: 0.06},
  landscape: {top: 0.07, bottom: 0.07, side: 0.05},
};

export const useLayout = () => {
  const {width, height} = useVideoConfig();
  const ratio = height / width;
  const format: Format = ratio > 1.5 ? 'vertical' : ratio > 1.1 ? 'portrait' : ratio > 0.9 ? 'square' : 'landscape';
  const safe = SAFE[format];
  const base = Math.min(width, height);
  return {
    width,
    height,
    format,
    safe,
    stacked: format === 'vertical' || format === 'portrait',
    pad: {top: height * safe.top, bottom: height * safe.bottom, side: width * safe.side},
    // Type scale keyed to the short edge so every placement reads at the same visual weight.
    type: {display: base * 0.12, h1: base * 0.08, h2: base * 0.056, body: base * 0.036, caption: base * 0.026},
    unit: base / 100,
  };
};
