// adsworm.com palette, dark: navy-black stage, cream type, blue + gold accents. ALGO = electric cyan.
export const C = {
  bg: '#080C14',
  bg2: '#0E1422',
  panel: '#111827',
  panelHi: '#182235',
  line: 'rgba(240,238,232,0.10)',
  cream: '#F0EEE8',
  muted: 'rgba(240,238,232,0.55)',
  blue: '#1B5EF7',
  blueBright: '#2B7BFF',
  gold: '#C8A96E',
  goldBright: '#E2C78E',
  cyan: '#5FE1FF',
  green: '#3DDC84',
  red: '#FF5A5A',
};

// 1080×1920 layout. Reels-safe text band is y 269–1248; IG's right rail lives at x > 960.
export const L = {
  rail: {y: 262},
  room: {cx: 540, cy: 650, w: 900, h: 700}, // room viewport on screen
  caption: {y: 1040, w: 900},
  aman: {x: 18, h: 640, feet: 1955},
  orbSeat: {x: 760, y: 1470, r: 92}, // where the orb sits and listens
  orbStage: {x: 540, y: 640, r: 210}, // where it takes over when it speaks
};
