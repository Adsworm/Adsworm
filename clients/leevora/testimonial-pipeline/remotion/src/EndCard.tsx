import React from "react";
import { AbsoluteFill, Easing, Img, interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { BRAND, EASE_OUT } from "./brand";

// Logo only. No client name, treatment, claim or call to action unless confirmed.
export const EndCard: React.FC<{ dissolveFrames: number }> = ({ dissolveFrames }) => {
  const frame = useCurrentFrame(); // local to the end-card sequence
  const { width } = useVideoConfig();
  const k = width / 1080;
  const ease = Easing.bezier(...EASE_OUT);
  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(circle at 50% 46%, #1F4C49 0%, ${BRAND.petrol} 46%, #102B29 100%)`,
        opacity: interpolate(frame, [0, dissolveFrames], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.inOut(Easing.cubic) }),
        justifyContent: "center",
        alignItems: "center",
        flexDirection: "column",
      }}
    >
      <Img
        src={staticFile("leevora-logo-ivory.svg")}
        style={{
          width: width * 0.54,
          opacity: interpolate(frame, [dissolveFrames - 2, dissolveFrames + 16], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease }),
          scale: interpolate(frame, [dissolveFrames - 2, dissolveFrames + 70], [0.965, 1.0], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease }),
        }}
      />
      <div
        style={{
          marginTop: 44 * k,
          height: 1.5 * k,
          backgroundColor: BRAND.champagne,
          width: interpolate(frame, [dissolveFrames + 8, dissolveFrames + 34], [0, 132 * k], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease }),
        }}
      />
    </AbsoluteFill>
  );
};
