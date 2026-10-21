// Renders every placement to out/<id>.mp4 — H.264 High, yuv420p, BT.709: what Meta re-encodes cleanly.
import {renderMedia, selectComposition} from '@remotion/renderer';
import {browserExecutable, bundleProject, licenseKey, parseArgs} from './_shared.mjs';

const {inputProps, ids} = parseArgs();
const serveUrl = await bundleProject();

for (const id of ids) {
  const composition = await selectComposition({serveUrl, id, inputProps, browserExecutable});
  const outputLocation = `out/${id}.mp4`;
  const started = Date.now();
  let last = -1;
  await renderMedia({
    serveUrl,
    composition,
    inputProps,
    codec: 'h264',
    crf: 18,
    pixelFormat: 'yuv420p',
    colorSpace: 'bt709',
    outputLocation,
    browserExecutable,
    licenseKey,
    onProgress: ({progress}) => {
      const pct = Math.floor(progress * 10) * 10;
      if (pct > last) process.stdout.write(`${id} ${(last = pct)}%\n`);
    },
  });
  console.log(`${id} → ${outputLocation} (${((Date.now() - started) / 1000).toFixed(1)}s)`);
}
