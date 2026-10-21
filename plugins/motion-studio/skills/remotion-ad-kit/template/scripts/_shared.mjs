import {bundle} from '@remotion/bundler';
import fs from 'node:fs';
import path from 'node:path';

export const ALL = ['Ad-9x16', 'Ad-4x5', 'Ad-1x1', 'Ad-16x9'];

// CLI: [props.json] [Ad-9x16 ...]  — props are shallow-merged over defaultProps.
export const parseArgs = () => {
  const args = process.argv.slice(2);
  const propsFile = args.find((a) => a.endsWith('.json'));
  const ids = args.filter((a) => ALL.includes(a));
  return {
    inputProps: propsFile ? JSON.parse(fs.readFileSync(propsFile, 'utf8')) : {},
    ids: ids.length ? ids : ALL,
  };
};

export const browserExecutable = process.env.REMOTION_BROWSER_EXECUTABLE ?? null;

export const bundleProject = () => bundle({entryPoint: path.resolve('src/index.ts')});

// Remotion Company License key (needed for 4+ headcount orgs) — https://remotion.pro
export const licenseKey = process.env.REMOTION_LICENSE_KEY ?? null;
