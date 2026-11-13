import React from "react";
import { AbsoluteFill, Easing, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { BRAND, EASE_OUT, SANS, SERIF } from "./brand";
import type { CaptionPage } from "./types";

// Layout is authored for 1080x1920 and scaled, so the same component renders the 4K master.
const BASE_W = 1080;
const ease = Easing.bezier(...EASE_OUT);

const Page: React.FC<{ page: CaptionPage }> = ({ page }) => {
  const frame = useCurrentFrame();
  const { fps, width } = useVideoConfig();
  const k = width / BASE_W;
  const start = Math.round((page.startMs / 1000) * fps);
  const end = Math.round((page.endMs / 1000) * fps);
  if (frame < start || frame >= end) return null;

  const words = page.lines.flat();
  // Words arrive one after another over the first part of the phrase, so the line builds as she speaks.
  const stagger = Math.min(4, Math.max(1.5, ((end - start) * 0.42) / Math.max(1, words.length)));
  let index = 0;

  return (
    <div
      style={{
        position: "relative",
        opacity: interpolate(frame, [end - 4, end], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        gap: (page.hero ? 6 : 4) * k,
        textShadow: `0 ${2 * k}px ${22 * k}px rgba(8, 24, 23, 0.7), 0 0 ${4 * k}px rgba(8, 24, 23, 0.45)`,
      }}
    >
      {/* Soft dark glow behind the words: keeps the champagne serif readable over the white table without a hard box. */}
      <div
        style={{
          position: "absolute",
          inset: `${-70 * k}px ${-150 * k}px`,
          background: "radial-gradient(ellipse at center, rgba(10,30,28,0.80) 0%, rgba(10,30,28,0.62) 38%, rgba(10,30,28,0.28) 62%, rgba(10,30,28,0) 78%)",
          opacity: interpolate(frame, [start, start + 6], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
          zIndex: -1,
        }}
      />
      {page.lines.map((line, i) => (
        <div key={i} style={{ display: "flex", alignItems: "baseline", gap: 13 * k, whiteSpace: "nowrap" }}>
          {line.map((tok, j) => {
            const at = start + index * stagger;
            index += 1;
            const serifSize = (page.hero ? 104 : 60) * k;
            return (
              <span
                key={j}
                style={{
                  display: "inline-block",
                  fontFamily: tok.hl ? SERIF : SANS,
                  fontWeight: tok.hl ? 400 : 600,
                  fontSize: tok.hl ? serifSize : (page.hero ? 46 : 52) * k,
                  lineHeight: tok.hl ? 1.04 : 1.22,
                  letterSpacing: tok.hl ? "-0.012em" : page.hero ? "0.02em" : "-0.008em",
                  color: tok.hl ? BRAND.champagne : BRAND.ivory,
                  opacity: interpolate(frame, [at, at + 5], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease }),
                  translate: `0px ${interpolate(frame, [at, at + 8], [12 * k, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease })}px`,
                }}
              >
                {tok.t}
              </span>
            );
          })}
        </div>
      ))}
    </div>
  );
};

export const Captions: React.FC<{ pages: CaptionPage[] }> = ({ pages }) => {
  const { height } = useVideoConfig();
  // Centre at 72% of the frame height: below her hands, above Instagram's caption and button area, clear of her face.
  return (
    <AbsoluteFill>
      {pages.map((p) => (
        <div key={p.startMs} style={{ position: "absolute", left: 0, right: 0, top: height * 0.72, display: "flex", justifyContent: "center", translate: "0px -50%" }}>
          <Page page={p} />
        </div>
      ))}
    </AbsoluteFill>
  );
};
