// Static ads: renders the settled last frame of Static-<format> to out/static/<id>.png.
import {renderStill, selectComposition} from '@remotion/renderer';
import {ALL, browserExecutable, bundleProject, parseArgs} from './_shared.mjs';

const {inputProps, ids} = parseArgs();
const serveUrl = await bundleProject();
for (const id of (ids.length === ALL.length ? ALL : ids).map((i) => i.replace('Ad-', 'Static-'))) {
  const composition = await selectComposition({serveUrl, id, inputProps, browserExecutable});
  const output = `out/static/${id}.png`;
  await renderStill({serveUrl, composition, inputProps, output, browserExecutable, frame: composition.durationInFrames - 1});
  console.log(`${id} → ${output}`);
}
