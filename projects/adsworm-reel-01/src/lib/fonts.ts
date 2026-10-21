import {loadFont} from '@remotion/fonts';
import {staticFile} from 'remotion';

// Fonts ship in /public/fonts (SIL OFL): deterministic renders, no network at render time.
// Swap in the client's brand fonts here — keep one grotesk + one accent face.
export const sans = 'Inter Tight';
export const serif = 'Instrument Serif';

loadFont({family: sans, url: staticFile('fonts/InterTight-Variable.woff2'), weight: '100 900'});
// Italic serif accent against a tight grotesk = the "editorial premium" pairing.
loadFont({family: serif, url: staticFile('fonts/InstrumentSerif-Italic.woff2'), style: 'italic', weight: '400'});
