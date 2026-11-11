import {Easing, interpolate, spring} from 'remotion';

// Fast attack, long soft settle — reads as "expensive". Never use linear for UI motion.
export const ease = {
  outExpo: Easing.bezier(0.16, 1, 0.3, 1),
  outQuart: Easing.bezier(0.25, 1, 0.5, 1),
  inOutQuart: Easing.bezier(0.76, 0, 0.24, 1),
  inExpo: Easing.bezier(0.7, 0, 0.84, 0),
};

export const springs = {
  smooth: {damping: 200},
  snappy: {damping: 20, stiffness: 200},
  pop: {damping: 12, stiffness: 180, mass: 0.6},
};

/** Eased, clamped 0→1 progress over `duration` frames starting at `delay`. */
export const progress = (frame: number, delay: number, duration: number, easing = ease.outExpo) =>
  interpolate(frame, [delay, delay + duration], [0, 1], {
    easing,
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

export const springIn = (frame: number, fps: number, delay = 0, config: Record<string, number> = springs.smooth) =>
  spring({frame: frame - delay, fps, config});

/** Mix a CSS color with transparency (Chrome 111+). */
export const alpha = (color: string, pct: number) => `color-mix(in srgb, ${color} ${pct}%, transparent)`;
