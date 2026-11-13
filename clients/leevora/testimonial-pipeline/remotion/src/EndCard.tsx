import React from "react";
import { AbsoluteFill, Easing, Img, interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { BRAND } from "./brand";

// Logo only. No client name, treatment, claim or call to action unless confirmed.
export const EndCard: React.FC<{ dissolveFrames: number }> = ({ dissolveFrames }) => {
  const frame = useCurrentFrame(); // local to the end-card sequence
  const { width } = useVideoConfig();
  const bg = interpolate(frame, [0, dissolveFrames], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.inOut(Easing.cubic) });
  const logo = interpolate(frame, [dissolveFrames - 2, dissolveFrames + 14], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
  const scale = interpolate(frame, [0, 90], [1.0, 1.025], { extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ backgroundColor: BRAND.petrol, opacity: bg, justifyContent: "center", alignItems: "center" }}>
      <Img src={staticFile("leevora-logo-ivory.svg")} style={{ width: width * 0.5, opacity: logo, transform: `scale(${scale})` }} />
    </AbsoluteFill>
  );
};
