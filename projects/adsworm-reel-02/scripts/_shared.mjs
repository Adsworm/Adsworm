import {bundle} from '@remotion/bundler';
import path from 'node:path';

export const ID = 'FullChairs01';
export const browserExecutable = process.env.REMOTION_BROWSER_EXECUTABLE ?? null;
// Remotion Company License key (needed for 4+ headcount orgs) — https://remotion.pro
export const licenseKey = process.env.REMOTION_LICENSE_KEY ?? null;
export const bundleProject = () => bundle({entryPoint: path.resolve('src/index.ts')});
