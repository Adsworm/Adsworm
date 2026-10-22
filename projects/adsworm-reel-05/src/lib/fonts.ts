import {loadFont} from '@remotion/fonts';
import {staticFile} from 'remotion';

// Adsworm brand type (adsworm.com): Bebas Neue for headlines and numbers, DM Sans for everything else.
export const display = 'Bebas Neue';
export const body = 'DM Sans';

loadFont({family: display, url: staticFile('fonts/BebasNeue-Regular.woff2'), weight: '400'});
loadFont({family: body, url: staticFile('fonts/DMSans-Variable.woff2'), weight: '100 1000'});
