import React from "react";
import { AbsoluteFill, Easing, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { TEAM, TEAM_SERIF } from "./fonts";

// Opening label in the team's style: serif title inside a frosted pill with a thin ivory outline.
export const TitlePill: React.FC<{ text: string; fromMs: number; toMs: number }> = ({ text, fromMs, toMs }) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();
  const k = width / 1080;
  const a = Math.round((fromMs / 1000) * fps), b = Math.round((toMs / 1000) * fps);
  if (frame < a || frame >= b) return null;
  const ease = Easing.bezier(0.16, 1, 0.3, 1);
  const pin = interpolate(frame, [a, a + 9], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease });
  const pout = interpolate(frame, [b - 6, b], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const words = text.split(" ");
  return (
    <AbsoluteFill>
      <div style={{ position: "absolute", left: 0, right: 0, top: height * 0.575, display: "flex", justifyContent: "center", translate: "0px -50%", opacity: Math.min(pin, pout), filter: `blur(${(1 - pout) * 10 * k}px)` }}>
        <div
          style={{
            display: "flex",
            gap: 20 * k,
            padding: `${14 * k}px ${46 * k}px ${18 * k}px`,
            borderRadius: 999,
            border: `${2 * k}px solid rgba(240,236,226,0.72)`,
            background: "rgba(40,48,46,0.42)",
            backdropFilter: `blur(${14 * k}px)`,
            scale: interpolate(pin, [0, 1], [0.94, 1]),
            boxShadow: `0 ${6 * k}px ${30 * k}px rgba(0,0,0,0.18)`,
          }}
        >
          {words.map((w, i) => {
            const at = a + 3 + i * 4;
            const p = interpolate(frame, [at, at + 7], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease });
            return (
              <span key={i} style={{ fontFamily: TEAM_SERIF, fontSize: 84 * k, lineHeight: 1.05, letterSpacing: "-0.022em", color: TEAM.white, opacity: p, filter: `blur(${(1 - p) * 10 * k}px)` }}>
                {w}
              </span>
            );
          })}
        </div>
      </div>
    </AbsoluteFill>
  );
};
