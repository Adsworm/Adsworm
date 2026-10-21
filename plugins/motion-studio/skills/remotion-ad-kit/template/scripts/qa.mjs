// Visual QA: renders 5 stills per placement and tiles them into out/qa/<id>-sheet.png.
// Open the sheets and check: safe zones, text overflow, contrast, hierarchy, brand colors.
import {renderStill, selectComposition} from '@remotion/renderer';
import {execFileSync} from 'node:child_process';
import fs from 'node:fs';
import {browserExecutable, bundleProject, parseArgs} from './_shared.mjs';

const MARKS = [0.12, 0.33, 0.58, 0.8, 0.99];
const {inputProps, ids} = parseArgs();
const qaProps = {...inputProps, showSafeZones: true};
const serveUrl = await bundleProject();
fs.mkdirSync('out/qa', {recursive: true});

for (const id of ids) {
  const composition = await selectComposition({serveUrl, id, inputProps: qaProps, browserExecutable});
  const files = [];
  for (const m of MARKS) {
    const frame = Math.min(composition.durationInFrames - 1, Math.round(composition.durationInFrames * m));
    const output = `out/qa/${id}-f${frame}.png`;
    await renderStill({serveUrl, composition, inputProps: qaProps, frame, output, browserExecutable});
    files.push(output);
  }
  const sheet = `out/qa/${id}-sheet.png`;
  const scaled = files.map((_, i) => `[${i}]scale=-2:640[s${i}]`).join(';');
  const stack = `${files.map((_, i) => `[s${i}]`).join('')}hstack=inputs=${files.length}`;
  execFileSync('ffmpeg', ['-y', '-loglevel', 'error', ...files.flatMap((f) => ['-i', f]), '-filter_complex', `${scaled};${stack}`, sheet]);
  console.log(`${id} → ${sheet}`);
}
