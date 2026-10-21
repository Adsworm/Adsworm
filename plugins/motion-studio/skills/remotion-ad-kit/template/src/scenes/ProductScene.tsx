import {AbsoluteFill} from 'remotion';
import {FadeUp} from '../components/FadeUp';
import {KineticText} from '../components/KineticText';
import {ProductShot} from '../components/ProductShot';
import {sans} from '../lib/fonts';
import {useLayout} from '../lib/layout';
import type {AdProps} from '../schema';

export const ProductScene: React.FC<{p: AdProps}> = ({p}) => {
  const {pad, type, height, stacked} = useLayout();
  const contentH = height - pad.top - pad.bottom;
  const align = stacked ? 'center' : 'left';
  return (
    <AbsoluteFill
      style={{
        padding: `${pad.top}px ${pad.side}px ${pad.bottom}px`,
        flexDirection: stacked ? 'column' : 'row',
        justifyContent: 'center',
        alignItems: 'center',
        gap: type.h1 * 0.6,
      }}
    >
      {p.productImage ? <ProductShot src={p.productImage} height={contentH * (stacked ? 0.52 : 0.82)} /> : null}
      <div style={{display: 'flex', flexDirection: 'column', alignItems: stacked ? 'center' : 'flex-start', gap: type.body, maxWidth: stacked ? '100%' : '52%'}}>
        <KineticText text={p.headline} fontSize={type.h1} color={p.colors.ink} accentColor={p.colors.primary} delay={10} align={align} />
        <FadeUp delay={24}>
          <div style={{fontFamily: sans, fontWeight: 500, fontSize: type.body, color: p.colors.ink, opacity: 0.72, textAlign: align}}>
            {p.subline}
          </div>
        </FadeUp>
      </div>
    </AbsoluteFill>
  );
};
