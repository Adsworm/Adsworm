import {zColor} from '@remotion/zod-types';
import {z} from 'zod';

export const adSchema = z.object({
  brandName: z.string(),
  colors: z.object({
    primary: zColor(),
    accent: zColor(),
    ink: zColor(),
    paper: zColor(),
  }),
  hook: z.string().describe('0–2.5s scroll-stopper. Wrap words in *asterisks* for the serif accent.'),
  headline: z.string(),
  subline: z.string(),
  productImage: z.string().describe('File name inside /public, or empty for none'),
  logo: z.string().describe('File name inside /public, or empty to use the wordmark'),
  stats: z
    .array(z.object({value: z.number(), prefix: z.string(), suffix: z.string(), label: z.string()}))
    .max(3),
  offer: z.string(),
  cta: z.string(),
  music: z.string().describe('File name inside /public, or empty for silent'),
  backgroundVideo: z.string().describe('Footage in /public (AI-generated or shot), played full-bleed under the overlays, or empty'),
  showSafeZones: z.boolean(),
});

export type AdProps = z.infer<typeof adSchema>;

// Placeholder brand and claims — replace every stat with substantiated numbers before running ads.
export const defaultAdProps: AdProps = {
  brandName: 'ATELIER NINE',
  colors: {primary: '#1F3D2B', accent: '#C9963F', ink: '#151515', paper: '#F3EEE6'},
  hook: 'Your skin *isn’t* tired. It’s *underfed.*',
  headline: 'Clinical glow in *14 days.*',
  subline: '15% Vitamin C · Ferulic · Zero fragrance',
  productImage: 'product.svg',
  logo: '',
  stats: [
    {value: 94, prefix: '', suffix: '%', label: 'saw brighter skin'},
    {value: 14, prefix: '', suffix: ' days', label: 'to visible results'},
    {value: 4.9, prefix: '', suffix: '★', label: 'average rating'},
  ],
  offer: 'Launch week — *20% off*',
  cta: 'Shop the Serum',
  music: '',
  backgroundVideo: '',
  showSafeZones: false,
};
