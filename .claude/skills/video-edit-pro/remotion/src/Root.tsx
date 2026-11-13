import React from "react";
import { CalculateMetadataFunction, Composition } from "remotion";
import { Overlay } from "./Overlay";
import { TeamOverlay } from "./team/TeamOverlay";
import type { TeamProps } from "./team/types";
import type { OverlayProps } from "./types";

const calculateMetadata: CalculateMetadataFunction<OverlayProps> = async ({ props }) => ({
  durationInFrames: props.contentFrames + props.endCardFrames,
  fps: props.fps,
  defaultCodec: "prores",
  defaultVideoImageFormat: "png",
  defaultPixelFormat: "yuva444p10le",
  defaultProResProfile: "4444",
});

const sample: OverlayProps = {
  fps: 25,
  contentFrames: 100,
  endCardFrames: 65,
  pages: [{ startMs: 200, endMs: 3000, text: "Sample caption line", lines: [[{ t: "Sample", hl: false }, { t: "caption", hl: true }, { t: "line", hl: false }]] }],
};

const teamMeta: CalculateMetadataFunction<TeamProps> = async ({ props }) => ({
  durationInFrames: props.contentFrames + props.endCardFrames,
  fps: props.fps,
  defaultCodec: "prores",
  defaultVideoImageFormat: "png",
  defaultPixelFormat: "yuva444p10le",
  defaultProResProfile: "4444",
});

const teamSample: TeamProps = { fps: 25, contentFrames: 100, endCardFrames: 65, pill: { text: "Client Testimonial", fromMs: 100, toMs: 1700 }, pages: [{ startMs: 200, endMs: 3000, lines: [{ text: "The staff is", gold: false }, { text: "amazing", gold: true }] }] };

export const Root: React.FC = () => (
  <>
    <Composition id="TeamOverlay" component={TeamOverlay} width={1080} height={1920} fps={25} durationInFrames={165} defaultProps={teamSample} calculateMetadata={teamMeta} />
    <Composition id="TeamOverlay4K" component={TeamOverlay} width={2160} height={3840} fps={25} durationInFrames={165} defaultProps={teamSample} calculateMetadata={teamMeta} />
    <Composition id="Overlay" component={Overlay} width={1080} height={1920} fps={25} durationInFrames={165} defaultProps={sample} calculateMetadata={calculateMetadata} />
    <Composition id="Overlay4K" component={Overlay} width={2160} height={3840} fps={25} durationInFrames={165} defaultProps={sample} calculateMetadata={calculateMetadata} />
  </>
);
