// "The 3 checks" carousel → out/carousel/slide-1..5.png (4:5, 1080×1350).
import {renderStill, selectComposition} from '@remotion/renderer';
import {browserExecutable, bundleProject} from './_shared.mjs';

const serveUrl = await bundleProject();
for (const n of [1, 2, 3, 4, 5]) {
  const composition = await selectComposition({serveUrl, id: `Carousel-${n}`, inputProps: {slide: n}, browserExecutable});
  const output = `out/carousel/slide-${n}.png`;
  await renderStill({serveUrl, composition, inputProps: {slide: n}, output, browserExecutable});
  console.log(`→ ${output}`);
}
