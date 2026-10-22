// voice.py (TTS + mix + timeline) → render → two-pass loudness master → out/<NAME>.mp4 + out/cover.png
import {renderMedia, renderStill, selectComposition} from '@remotion/renderer';
import {execFileSync, spawnSync} from 'node:child_process';
import fs from 'node:fs';
import {browserExecutable, bundleProject, ID, licenseKey} from './_shared.mjs';

const PAID = process.argv.includes('--paid'); // boosted-post variant: DM keyword instead of the comment UI
const NAME = process.env.REEL_NAME ?? (PAID ? 'REEL-03_PAID_9x16' : 'REEL-03_9x16');
if (!process.argv.includes('--no-voice')) execFileSync('python3', ['scripts/voice.py', ...(PAID ? ['--variant', 'paid'] : [])], {stdio: 'inherit'});
fs.mkdirSync('out', {recursive: true});
const serveUrl = await bundleProject();
const inputProps = {showSafeZones: false, withAudio: true};
const composition = await selectComposition({serveUrl, id: ID, inputProps, browserExecutable});
let last = -1;
const started = Date.now();
await renderMedia({
  serveUrl,
  composition,
  inputProps,
  codec: 'h264',
  crf: 18,
  pixelFormat: 'yuv420p',
  colorSpace: 'bt709',
  outputLocation: 'out/raw.mp4',
  browserExecutable,
  licenseKey,
  onProgress: ({progress}) => {
    const pct = Math.floor(progress * 10) * 10;
    if (pct > last) console.log(`render ${(last = pct)}%`);
  },
});
console.log(`rendered in ${((Date.now() - started) / 1000).toFixed(1)}s`);
const target = 'I=-14:TP=-1.5:LRA=11';
const {stderr} = spawnSync('ffmpeg', ['-hide_banner', '-i', 'out/raw.mp4', '-af', `loudnorm=${target}:print_format=json`, '-f', 'null', '-'], {encoding: 'utf8'});
const m = JSON.parse(stderr.slice(stderr.lastIndexOf('{')));
execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-i', 'out/raw.mp4', '-c:v', 'copy', '-af', `loudnorm=${target}:measured_I=${m.input_i}:measured_TP=${m.input_tp}:measured_LRA=${m.input_lra}:measured_thresh=${m.input_thresh}:offset=${m.target_offset}:linear=true`, '-ar', '48000', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', `out/${NAME}.mp4`]);
await renderStill({serveUrl, composition, inputProps: {...inputProps, withAudio: false}, frame: 0, output: 'out/cover.png', browserExecutable});
console.log(`→ out/${NAME}.mp4 · out/cover.png`);
