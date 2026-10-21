import {AbsoluteFill} from 'remotion';
import {FadeUp} from '../components/FadeUp';
import {KineticText} from '../components/KineticText';
import {sans} from '../lib/fonts';
import {useLayout} from '../lib/layout';
import type {AdProps} from '../schema';

export const HookScene: React.FC<{p: AdProps}> = ({p}) => {
  const {pad, type} = useLayout();
  return (
    <AbsoluteFill
      style={{
        padding: `${pad.top}px ${pad.side}px ${pad.bottom}px`,
        justifyContent: 'center',
        alignItems: 'center',
        gap: type.display * 0.35,
      }}
    >
      <FadeUp delay={2}>
        <div style={{fontFamily: sans, fontWeight: 600, fontSize: type.caption, letterSpacing: '0.32em', color: p.colors.primary}}>
          {p.brandName}
        </div>
      </FadeUp>
      <KineticText text={p.hook} fontSize={type.display} color={p.colors.ink} accentColor={p.colors.primary} delay={6} stagger={5} />
    </AbsoluteFill>
  );
};
