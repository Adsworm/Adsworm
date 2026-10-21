import {AbsoluteFill} from 'remotion';
import {Background} from './components/Background';
import {CTAButton} from './components/CTAButton';
import {Grain} from './components/Grain';
import {KineticText} from './components/KineticText';
import {ProductShot} from './components/ProductShot';
import {SafeZoneOverlay} from './components/SafeZoneOverlay';
import {sans} from './lib/fonts';
import {useLayout} from './lib/layout';
import type {AdProps} from './schema';

// Static feed ad from the same props. Its composition is STATIC_FRAMES long and the PNG is its
// last frame: every entrance settled and the CTA shimmer parked off the button.
export const STATIC_FRAMES = 111;

export const StaticAd: React.FC<AdProps> = (p) => {
  const {pad, type, height, stacked} = useLayout();
  const contentH = height - pad.top - pad.bottom;
  const align = stacked ? 'center' : 'left';
  return (
    <AbsoluteFill>
      <Background paper={p.colors.paper} primary={p.colors.primary} accent={p.colors.accent} />
      <AbsoluteFill
        style={{
          padding: `${pad.top}px ${pad.side}px ${pad.bottom}px`,
          flexDirection: stacked ? 'column' : 'row',
          justifyContent: 'center',
          alignItems: 'center',
          gap: type.h1 * 0.5,
        }}
      >
        {p.productImage ? <ProductShot src={p.productImage} height={contentH * (stacked ? 0.4 : 0.78)} /> : null}
        <div style={{display: 'flex', flexDirection: 'column', alignItems: stacked ? 'center' : 'flex-start', gap: type.body * 0.8, maxWidth: stacked ? '100%' : '55%'}}>
          <div style={{fontFamily: sans, fontWeight: 600, fontSize: type.caption, letterSpacing: '0.32em', color: p.colors.primary}}>{p.brandName}</div>
          <KineticText text={p.headline} fontSize={type.h1} color={p.colors.ink} accentColor={p.colors.primary} align={align} />
          <div style={{fontFamily: sans, fontWeight: 500, fontSize: type.body, color: p.colors.ink, opacity: 0.72, textAlign: align}}>{p.subline}</div>
          <KineticText text={p.offer} fontSize={type.h2} color={p.colors.ink} accentColor={p.colors.accent} align={align} weight={700} />
          <div style={{marginTop: type.body * 0.4}}>
            <CTAButton label={p.cta} fontSize={type.body} bg={p.colors.primary} color={p.colors.paper} />
          </div>
        </div>
      </AbsoluteFill>
      <Grain />
      {p.showSafeZones ? <SafeZoneOverlay /> : null}
    </AbsoluteFill>
  );
};
