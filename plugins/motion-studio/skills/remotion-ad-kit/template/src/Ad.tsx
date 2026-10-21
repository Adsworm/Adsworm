import {linearTiming, type TransitionPresentation, TransitionSeries} from '@remotion/transitions';
import {fade} from '@remotion/transitions/fade';
import {slide} from '@remotion/transitions/slide';
import {wipe} from '@remotion/transitions/wipe';
import {Fragment} from 'react';
import {AbsoluteFill, Html5Audio, interpolate, OffthreadVideo, staticFile, useVideoConfig} from 'remotion';
import {Background} from './components/Background';
import {Grain} from './components/Grain';
import {SafeZoneOverlay} from './components/SafeZoneOverlay';
import {alpha, ease} from './lib/motion';
import type {AdProps} from './schema';
import {EndCard} from './scenes/EndCard';
import {HookScene} from './scenes/HookScene';
import {ProductScene} from './scenes/ProductScene';
import {StatsScene} from './scenes/StatsScene';

export const FPS = 30;
const TRANSITION = 14;

type Scene = {id: string; frames: number; node: React.ReactNode; enter: TransitionPresentation<Record<string, unknown>>};
const presentation = (t: unknown) => t as TransitionPresentation<Record<string, unknown>>;

// Single source of truth for scene order and length; also drives calculateMetadata.
export const buildTimeline = (p: AdProps): Scene[] =>
  [
    {id: 'hook', frames: 75, node: <HookScene p={p} />, enter: presentation(fade())},
    {id: 'product', frames: 120, node: <ProductScene p={p} />, enter: presentation(slide({direction: 'from-bottom'}))},
    ...(p.stats.length ? [{id: 'stats', frames: 105, node: <StatsScene p={p} />, enter: presentation(slide({direction: 'from-right'}))}] : []),
    {id: 'end', frames: 120, node: <EndCard p={p} />, enter: presentation(wipe({direction: 'from-bottom-left'}))},
  ];

export const totalFrames = (p: AdProps) => {
  const t = buildTimeline(p);
  return t.reduce((sum, s) => sum + s.frames, 0) - (t.length - 1) * TRANSITION;
};

export const Ad: React.FC<AdProps> = (p) => {
  const {durationInFrames} = useVideoConfig();
  return (
    <AbsoluteFill>
      <Background paper={p.colors.paper} primary={p.colors.primary} accent={p.colors.accent} />
      {p.backgroundVideo ? (
        // Hybrid lane: generated/shot footage under coded type. The scrim keeps copy legible.
        <AbsoluteFill>
          <OffthreadVideo src={staticFile(p.backgroundVideo)} muted style={{width: '100%', height: '100%', objectFit: 'cover'}} />
          <AbsoluteFill style={{background: `linear-gradient(to bottom, ${alpha(p.colors.paper, 40)}, ${alpha(p.colors.paper, 80)})`}} />
        </AbsoluteFill>
      ) : null}
      <TransitionSeries>
        {buildTimeline(p).map((s, i) => (
          <Fragment key={s.id}>
            {i > 0 ? (
              <TransitionSeries.Transition presentation={s.enter} timing={linearTiming({durationInFrames: TRANSITION, easing: ease.inOutQuart})} />
            ) : null}
            <TransitionSeries.Sequence durationInFrames={s.frames}>{s.node}</TransitionSeries.Sequence>
          </Fragment>
        ))}
      </TransitionSeries>
      {p.music ? (
        <Html5Audio
          src={staticFile(p.music)}
          volume={(f) => interpolate(f, [0, 15, durationInFrames - 30, durationInFrames], [0, 0.8, 0.8, 0], {extrapolateRight: 'clamp'})}
        />
      ) : null}
      <Grain />
      {p.showSafeZones ? <SafeZoneOverlay /> : null}
    </AbsoluteFill>
  );
};
