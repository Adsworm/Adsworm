import React from "react";
import { AbsoluteFill, Easing, Img, interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { TEAM, TEAM_SANS } from "./fonts";
import type { TeamPage } from "./types";

const ease = Easing.bezier(0.16, 1, 0.3, 1);

// Two-tier captions: a white Inter Tight line (~54 px at 1080 wide) and a larger SemiBold gold line (~76 px) for the words that matter.
// Words arrive one by one with a short blur-in, as in the team's edit. No box; a soft shadow keeps them legible.
const Page: React.FC<{ page: TeamPage }> = ({ page }) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();
  const k = width / 1080;
  const start = Math.round((page.startMs / 1000) * fps);
  const end = Math.round((page.endMs / 1000) * fps);
  if (frame < start || frame >= end) return null;
  const nWords = page.lines.reduce((n, l) => n + l.text.split(" ").length, 0);
  const stagger = Math.min(3.5, Math.max(1.2, ((end - start) * 0.4) / Math.max(1, nWords)));
  const out = interpolate(frame, [end - 4, end], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  let idx = 0;
  const wordStyle = (at: number): React.CSSProperties => {
    const p = interpolate(frame, [at, at + 6], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease });
    return { display: "inline-block", opacity: p, filter: `blur(${(1 - p) * 9 * k}px)`, translate: `0px ${(1 - p) * 10 * k}px` };
  };
  return (
    <div style={{ position: "absolute", left: 0, right: 0, top: height * 0.69, translate: "0px -50%", isolation: "isolate", display: "flex", flexDirection: "column", alignItems: "center", gap: 2 * k, opacity: out, filter: `blur(${(1 - out) * 6 * k}px)` }}>
      {/* Soft dark glow behind the words, no hard edge: keeps the gold line readable over the white marble table. */}
      <div
        style={{
          position: "absolute",
          inset: `${-56 * k}px ${-120 * k}px`,
          background: "radial-gradient(ellipse at center, rgba(8,20,19,0.62) 0%, rgba(8,20,19,0.45) 36%, rgba(8,20,19,0.18) 60%, rgba(8,20,19,0) 76%)",
          opacity: interpolate(frame, [start, start + 6], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
          zIndex: -1,
        }}
      />
      {page.lines.map((line, i) => (
        <div
          key={i}
          style={{
            display: "flex",
            gap: (line.gold ? 15 : 12) * k,
            whiteSpace: "nowrap",
            fontFamily: TEAM_SANS,
            fontWeight: line.gold ? 600 : 500,
            fontSize: (line.gold ? 76 : 54) * k,
            lineHeight: line.gold ? 1.06 : 1.16,
            letterSpacing: line.gold ? "-0.018em" : "-0.01em",
            color: line.gold ? TEAM.gold : TEAM.white,
            textShadow: `0 ${2 * k}px ${16 * k}px rgba(0,0,0,0.5), 0 0 ${3 * k}px rgba(0,0,0,0.3)`,
          }}
        >
          {line.text.split(" ").map((w, j) => {
            const at = start + idx * stagger;
            idx += 1;
            return (
              <span key={j} style={wordStyle(at)}>
                {w}
              </span>
            );
          })}
        </div>
      ))}
      {page.logo ? (
        <Img
          src={staticFile("leevora-logo-ivory.svg")}
          style={{
            width: 560 * k,
            marginTop: 6 * k,
            filter: `drop-shadow(0 ${3 * k}px ${18 * k}px rgba(0,0,0,0.38)) blur(${interpolate(frame, [start + 6, start + 14], [8 * k, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })}px)`,
            opacity: interpolate(frame, [start + 6, start + 14], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease }),
            scale: interpolate(frame, [start + 6, end], [0.96, 1.0], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease }),
          }}
        />
      ) : null}
    </div>
  );
};

export const TeamCaptions: React.FC<{ pages: TeamPage[] }> = ({ pages }) => (
  <AbsoluteFill>
    {pages.map((p) => (
      <Page key={p.startMs} page={p} />
    ))}
  </AbsoluteFill>
);
