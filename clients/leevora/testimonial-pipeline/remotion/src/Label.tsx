import React from "react";
import { AbsoluteFill, Easing, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { BRAND, EASE_OUT, SANS } from "./brand";

// A small editorial label under the wall logo during the establishing shot. Neutral wording only.
export const Label: React.FC<{ text: string; fromFrame: number; toFrame: number }> = ({ text, fromFrame, toFrame }) => {
  const frame = useCurrentFrame();
  const { width, height } = useVideoConfig();
  const k = width / 1080;
  if (frame < fromFrame || frame >= toFrame) return null;
  const ease = Easing.bezier(...EASE_OUT);
  const inP = interpolate(frame, [fromFrame, fromFrame + 12], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease });
  const out = interpolate(frame, [toFrame - 8, toFrame], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const rule = { height: 1.5 * k, width: 46 * k * inP, backgroundColor: BRAND.champagne } as const;
  return (
    <AbsoluteFill>
      <div style={{ position: "absolute", left: 0, right: 0, top: height * 0.283, display: "flex", justifyContent: "center", alignItems: "center", gap: 16 * k, opacity: Math.min(inP, out) }}>
        <div style={rule} />
        <div style={{ fontFamily: SANS, fontWeight: 600, fontSize: 21 * k, letterSpacing: "0.34em", color: BRAND.petrol, textTransform: "uppercase", paddingLeft: "0.34em" }}>{text}</div>
        <div style={rule} />
      </div>
    </AbsoluteFill>
  );
};
