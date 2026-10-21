// Variant matrix: every combination of the axes in a matrix file × each format → out/variants/.
// Names follow CAMPAIGN_AXISIDS_FORMAT so Meta reporting maps straight back to the creative.
//   node scripts/variants.mjs matrix.json            render everything
//   node scripts/variants.mjs matrix.json --dry-run  list names + count, render nothing
// Via npm use `npm run variants -- matrix.json --dry-run`; without `--` npm swallows the flag
// (as npm_config_dry_run), which is honoured too so a dry run can never start a batch render.
import {renderMedia, selectComposition} from '@remotion/renderer';
import fs from 'node:fs';
import {browserExecutable, bundleProject, licenseKey} from './_shared.mjs';

const [matrixFile, ...flags] = process.argv.slice(2);
if (!matrixFile) throw new Error('Usage: node scripts/variants.mjs <matrix.json> [--dry-run]');
const matrix = JSON.parse(fs.readFileSync(matrixFile, 'utf8'));
const base = matrix.base ? JSON.parse(fs.readFileSync(matrix.base, 'utf8')) : {};

// axes: {propName: [{id, value}]} → cartesian product of {ids, props}
const combos = Object.entries(matrix.axes).reduce(
  (acc, [prop, options]) => acc.flatMap((c) => options.map((o) => ({ids: [...c.ids, o.id], props: {...c.props, [prop]: o.value}}))),
  [{ids: [], props: {}}],
);
const jobs = combos.flatMap((c) =>
  matrix.formats.map((format) => ({
    name: `${matrix.campaign}_${c.ids.join('-')}_${format.replace('Ad-', '')}`,
    id: format,
    props: {...base, ...c.props},
  })),
);

console.log(`${combos.length} variants × ${matrix.formats.length} formats = ${jobs.length} renders`);
if (flags.includes('--dry-run') || process.env.npm_config_dry_run === 'true') {
  jobs.forEach((j) => console.log(`  ${j.name}`));
  process.exit(0);
}

fs.mkdirSync('out/variants', {recursive: true});
const serveUrl = await bundleProject();
const rows = [['name', 'format', ...Object.keys(matrix.axes), 'file', 'seconds']];
for (const job of jobs) {
  const composition = await selectComposition({serveUrl, id: job.id, inputProps: job.props, browserExecutable});
  const file = `out/variants/${job.name}.mp4`;
  await renderMedia({
    serveUrl,
    composition,
    inputProps: job.props,
    codec: 'h264',
    crf: 18,
    pixelFormat: 'yuv420p',
    colorSpace: 'bt709',
    outputLocation: file,
    browserExecutable,
    licenseKey,
  });
  rows.push([job.name, job.id, ...Object.keys(matrix.axes).map((k) => JSON.stringify(job.props[k])), file, (composition.durationInFrames / composition.fps).toFixed(1)]);
  console.log(`✓ ${file}`);
}
fs.writeFileSync('out/variants/manifest.csv', rows.map((r) => r.join(',')).join('\n') + '\n');
console.log('manifest → out/variants/manifest.csv');
