// Re-render only the cover still from the current timeline: COVER_FRAME=72 REEL=<slug> node scripts/cover.mjs
import {renderStill, selectComposition} from '@remotion/renderer';
import fs from 'node:fs';
import {browserExecutable, bundleProject, ID} from './_shared.mjs';

const NAME = process.env.REEL_NAME ?? (process.env.REEL ? `ADSWORM_${process.env.REEL}_9x16` : 'REEL_9x16');
const frame = Number(process.env.COVER_FRAME ?? 100);
fs.mkdirSync('out', {recursive: true});
const serveUrl = await bundleProject();
const inputProps = {showSafeZones: false, withAudio: false};
const composition = await selectComposition({serveUrl, id: ID, inputProps, browserExecutable});
await renderStill({serveUrl, composition, inputProps, frame, output: `out/${NAME}_cover.png`, browserExecutable});
console.log(`→ out/${NAME}_cover.png (frame ${frame})`);
