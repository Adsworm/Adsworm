import {AbsoluteFill} from 'remotion';
import {StatCounter} from '../components/StatCounter';
import {useLayout} from '../lib/layout';
import type {AdProps} from '../schema';

export const StatsScene: React.FC<{p: AdProps}> = ({p}) => {
  const {pad, type, stacked, width} = useLayout();
  const gap = stacked ? type.h1 * 0.55 : type.h1 * 0.6;
  // Row layouts: size numbers so the longest one fits its column on a single line.
  const longest = Math.max(...p.stats.map((s) => `${s.prefix}${s.value}${s.suffix}`.length));
  const column = (width - pad.side * 2 - gap * (p.stats.length - 1)) / p.stats.length;
  const numberSize = stacked ? type.display * 0.82 : Math.min(type.h1 * 1.15, column / (longest * 0.58));
  return (
    <AbsoluteFill style={{padding: `${pad.top}px ${pad.side}px ${pad.bottom}px`, justifyContent: 'center', alignItems: 'center'}}>
      {/* Row: top-aligned so numbers share a line even when labels wrap differently. */}
      <div style={{display: 'flex', flexDirection: stacked ? 'column' : 'row', alignItems: stacked ? 'center' : 'flex-start', gap}}>
        {p.stats.map((s, i) => (
          <StatCounter
            key={s.label}
            {...s}
            numberSize={numberSize}
            width={stacked ? undefined : column}
            labelSize={stacked ? type.body : Math.min(type.body, numberSize * 0.4)}
            color={p.colors.primary}
            labelColor={p.colors.ink}
            lineColor={p.colors.accent}
            delay={4 + i * 9}
          />
        ))}
      </div>
    </AbsoluteFill>
  );
};
