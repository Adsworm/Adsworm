import {AbsoluteFill} from 'remotion';
import {CTAButton} from '../components/CTAButton';
import {KineticText} from '../components/KineticText';
import {Wordmark} from '../components/Wordmark';
import {useLayout} from '../lib/layout';
import type {AdProps} from '../schema';

export const EndCard: React.FC<{p: AdProps}> = ({p}) => {
  const {pad, type} = useLayout();
  return (
    <AbsoluteFill
      style={{
        background: p.colors.primary,
        padding: `${pad.top}px ${pad.side}px ${pad.bottom}px`,
        justifyContent: 'center',
        alignItems: 'center',
        gap: type.h1 * 0.7,
      }}
    >
      <Wordmark name={p.brandName} logo={p.logo} size={type.h2 * 0.8} color={p.colors.paper} delay={4} />
      <KineticText text={p.offer} fontSize={type.h1} color={p.colors.paper} accentColor={p.colors.accent} delay={12} />
      <CTAButton label={p.cta} fontSize={type.body * 1.1} bg={p.colors.paper} color={p.colors.ink} delay={26} />
    </AbsoluteFill>
  );
};
