// Light "explainer" variant of the adsworm.com palette: the same blue, navy and gold, on cream.
export const C = {
  bg: '#F4F3EF',
  card: '#FFFFFF',
  ink: '#0D1320',
  blue: '#1B5EF7',
  blueBright: '#2B7BFF',
  blueSoft: '#E6EEFF',
  gold: '#C8A96E',
  goldSoft: '#F6EEDC',
  muted: '#6E7280',
  line: '#E6E6E2',
  green: '#1E9E5A',
  greenSoft: '#E3F5EA',
  red: '#E04545',
};

// Stage geometry (1080×1920). Captions sit inside the Reels-safe band (y 269–1248).
export const CARD = {x: 60, y: 280, w: 960, h: 720, r: 44, pad: 44};
export const BUBBLE = {x: 70, y: 1035, w: 940, minH: 150};
export const PLATFORM = {y: 1690};
export const FEET = 1712; // avatar feet line

// v3 (teacher + student busts, proof board): paper, ink outlines, offset shadows.
export const V3 = {
  paper: '#EDEFF3',
  pink: '#FF4D8D',
  pinkSoft: '#FFE3EE',
  outline: '3px solid #0D1320',
  shadow: '7px 7px 0 #0D1320',
  // v4 layout: everything lifted so both faces sit higher (mouths ≈ y 1430, clear of Instagram's
  // caption/username overlay) and the busts are larger; text stays inside y 269–1248.
  pill: {y: 258},
  board: {x: 54, y: 326, w: 972, h: 650},
  bubble: {y: 988, w: 860},
  aman: {x: -56, y: 1190, size: 730},
  riya: {x: 486, y: 1222, size: 698},
};
