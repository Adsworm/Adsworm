import {AbsoluteFill, Html5Audio, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {SafeZoneOverlay} from '../components/SafeZoneOverlay';
import {Avatar, type Pose} from './Avatars';
import {Caption, captionAlpha, type Line} from './Caption';
import {Card} from './Card';
import {Stage} from './Stage';
import {Views, type View} from './views';
import timeline from './timeline.json';

type Section = {id: string; label: string; tag: string; source: string; start: number; end: number; views: View[]};
type Timeline = {
  fps: number;
  durationInFrames: number;
  brand: {footer?: string; names?: Record<string, string>; side?: Record<string, 'left' | 'right'>};
  lines: Line[];
  sections: Section[];
  beats: Record<string, number>;
  vars?: Record<string, number | string>;
};
const TL = timeline as unknown as Timeline;
const NAMES = TL.brand.names ?? {AMAN: 'AMAN', RIYA: 'RIYA'};
const SIDE = TL.brand.side ?? {AMAN: 'right', RIYA: 'left'};
const SPEAK_POSES: Pose[] = ['point', 'palms'];
const LISTEN_POSES: Record<string, Pose[]> = {AMAN: ['idle'], RIYA: ['idle']};

export type ReelProps = {showSafeZones: boolean; withAudio: boolean};

export const Reel: React.FC<ReelProps> = ({showSafeZones, withAudio}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const idx = Math.max(0, TL.lines.reduce((acc, ln, i) => (ln.start <= t ? i : acc), -1)); // line 1 shows from frame 0
  const line = idx >= 0 ? TL.lines[idx] : undefined;
  const next = idx >= 0 ? TL.lines[idx + 1] : undefined;
  const section = TL.sections.find((s) => t >= s.start - 0.3 && (t < s.end + 0.45 || s === TL.sections[TL.sections.length - 1])) ?? TL.sections[0];
  const alpha = captionAlpha(frame, fps, line, next);
  const speaker = line?.who;
  const sinceF = line ? (idx === 0 ? -6 : Math.round(line.start * fps)) : 0; // line 1's pose is settled on frame 0 (the cover)
  const poseFor = (who: string): Pose => {
    if (!line) return 'idle';
    if (who === speaker) return (line.pose as Pose) ?? SPEAK_POSES[idx % SPEAK_POSES.length];
    const l = LISTEN_POSES[who] ?? ['idle'];
    return l[idx % l.length];
  };
  return (
    <AbsoluteFill>
      <Stage footer={TL.brand.footer ?? ''} />
      <Card label={section.label} tag={section.tag} source={section.source} sectionStartF={Math.round(section.start * fps)}>
        <Views views={section.views ?? []} beats={TL.beats} frame={frame} vars={TL.vars ?? {}} />
      </Card>
      {line ? (
        <div style={{opacity: alpha}}>
          <Caption line={line} names={NAMES} sideOf={SIDE} settled={idx === 0} />
        </div>
      ) : null}
      <Avatar who="RIYA" x={290} height={455} pose={poseFor('RIYA')} talking={speaker === 'RIYA'} flip since={sinceF} />
      <Avatar who="AMAN" x={790} height={472} pose={poseFor('AMAN')} talking={speaker === 'AMAN'} since={sinceF} />
      {withAudio ? <Html5Audio src={staticFile('voice.wav')} /> : null}
      {showSafeZones ? <SafeZoneOverlay /> : null}
    </AbsoluteFill>
  );
};
