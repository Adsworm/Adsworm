import {loadFont} from '@remotion/fonts';
import {staticFile} from 'remotion';

// Adsworm brand type (adsworm.com): Bebas Neue for headlines and numbers, DM Sans for everything else.
export const display = 'Bebas Neue';
export const body = 'DM Sans';

loadFont({family: display, url: staticFile('fonts/BebasNeue-Regular.woff2'), weight: '400'});
loadFont({family: body, url: staticFile('fonts/DMSans-Variable.woff2'), weight: '100 1000'});

// Hindi in Devanagari on the board (the key message for viewers who read little English). Same family names,
// Devanagari range only, so any text set in `display` or `body` just works. Teko and Mukta are SIL OFL.
const DEVANAGARI = 'U+0900-097F, U+1CD0-1CF9, U+200C-200D, U+20A8, U+20B9, U+25CC, U+A830-A839, U+A8E0-A8FF';
loadFont({family: display, url: staticFile('fonts/Teko-Devanagari-600.woff2'), weight: '400', unicodeRange: DEVANAGARI});
// The weight range must be IDENTICAL to the Latin face's ('100 1000'): faces only combine by unicode-range when
// their other descriptors match. With a different range the browser picked this face alone and Latin text
// fell back to a serif.
loadFont({family: body, url: staticFile('fonts/Mukta-Devanagari-700.woff2'), weight: '100 1000', unicodeRange: DEVANAGARI});

