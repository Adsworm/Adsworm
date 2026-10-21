// Contact sheets at the storyboard's key frames, safe zones on: out/qa/sheet-1.png, sheet-2.png.
import {renderStill, selectComposition} from '@remotion/renderer';
import {execFileSync} from 'node:child_process';
import fs from 'node:fs';
import {browserExecutable, bundleProject, ID} from './_shared.mjs';

const FRAMES = [0, 45, 100, 150, 200, 255, 330, 400, 470, 520, 580, 645, 735, 820, 900, 1000];
const only = process.argv.slice(2).map(Number).filter((n) => !Number.isNaN(n));
const frames = only.length ? only : FRAMES;
const inputProps = {showSafeZones: true, withAudio: false};
const serveUrl = await bundleProject();
const composition = await selectComposition({serveUrl, id: ID, inputProps, browserExecutable});
fs.mkdirSync('out/qa', {recursive: true});
const files = [];
for (const frame of frames) {
  const output = `out/qa/f${String(frame).padStart(4, '0')}.png`;
  await renderStill({serveUrl, composition, inputProps, frame, output, browserExecutable});
  files.push(output);
}
for (let s = 0; s * 8 < files.length; s++) {
  const chunk = files.slice(s * 8, s * 8 + 8);
  const sheet = `out/qa/sheet-${s + 1}.png`;
  const scaled = chunk.map((_, i) => `[${i}]scale=-2:720,drawtext=text='f${frames[s * 8 + i]}':x=12:y=12:fontsize=28:fontcolor=white:box=1:boxcolor=black@0.6[s${i}]`).join(';');
  execFileSync('ffmpeg', ['-y', '-loglevel', 'error', ...chunk.flatMap((f) => ['-i', f]), '-filter_complex', `${scaled};${chunk.map((_, i) => `[s${i}]`).join('')}hstack=inputs=${chunk.length}`, sheet]);
  console.log(`→ ${sheet}`);
}
