// Contact sheets: one still 8 frames into every spoken line (caption + card state visible),
// safe zones on → out/qa/sheet-N.png
import {renderStill, selectComposition} from '@remotion/renderer';
import {execFileSync} from 'node:child_process';
import fs from 'node:fs';
import {browserExecutable, bundleProject, ID} from './_shared.mjs';

const tl = JSON.parse(fs.readFileSync('src/reel/timeline.json', 'utf8'));
const only = process.argv.slice(2).map(Number).filter((n) => !Number.isNaN(n));
const frames = only.length ? only : [0, ...tl.lines.map((l) => Math.round(l.start * tl.fps) + 8), tl.durationInFrames - 1];
const inputProps = {showSafeZones: true, withAudio: false};
const serveUrl = await bundleProject();
const composition = await selectComposition({serveUrl, id: ID, inputProps, browserExecutable});
fs.rmSync('out/qa', {recursive: true, force: true});
fs.mkdirSync('out/qa', {recursive: true});
const files = [];
for (const frame of frames) {
  const output = `out/qa/f${String(frame).padStart(4, '0')}.png`;
  await renderStill({serveUrl, composition, inputProps, frame, output, browserExecutable});
  files.push(output);
}
const per = 6;
for (let s = 0; s * per < files.length; s++) {
  const chunk = files.slice(s * per, s * per + per);
  const sheet = `out/qa/sheet-${s + 1}.png`;
  const scaled = chunk.map((_, i) => `[${i}]scale=-2:900,drawtext=text='f${frames[s * per + i]}':x=12:y=12:fontsize=30:fontcolor=white:box=1:boxcolor=black@0.6[s${i}]`).join(';');
  execFileSync('ffmpeg', ['-y', '-loglevel', 'error', ...chunk.flatMap((f) => ['-i', f]), '-filter_complex', `${scaled};${chunk.map((_, i) => `[s${i}]`).join('')}hstack=inputs=${chunk.length}`, sheet]);
  console.log(`→ ${sheet}`);
}
