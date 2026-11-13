import React from "react";
import { AbsoluteFill, Easing, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { BRAND, CAPTION_FONT } from "./brand";
import type { CaptionPage } from "./types";

// Layout is authored for 1080x1920 and scaled, so the same component renders the 4K master.
const BASE_W = 1080;
const FADE_IN = 4; // frames
const FADE_OUT = 3;

const Page: React.FC<{ page: CaptionPage }> = ({ page }) => {
  const frame = useCurrentFrame();
  const { fps, width } = useVideoConfig();
  const k = width / BASE_W;
  const start = Math.round((page.startMs / 1000) * fps);
  const end = Math.round((page.endMs / 1000) * fps);
  if (frame < start || frame >= end) return null;

  const fadeIn = interpolate(frame, [start, start + FADE_IN], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
  const fadeOut = interpolate(frame, [end - FADE_OUT, end], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const rise = interpolate(frame, [start, start + FADE_IN + 2], [6 * k, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });

  return (
    <div
      style={{
        opacity: Math.min(fadeIn, fadeOut),
        transform: `translateY(${rise}px)`,
        backgroundColor: "rgba(23, 59, 57, 0.88)", // BRAND.petrol
        borderRadius: 18 * k,
        padding: `${17 * k}px ${32 * k}px ${19 * k}px`,
        maxWidth: 820 * k,
        fontFamily: CAPTION_FONT,
        fontWeight: 600,
        fontSize: 50 * k,
        lineHeight: 1.24,
        letterSpacing: "-0.005em",
        color: BRAND.ivory,
        textAlign: "center",
      }}
    >
      {page.lines.map((line, i) => (
        <div key={i} style={{ whiteSpace: "nowrap" }}>
          {line.map((tok, j) => (
            <span key={j} style={{ color: tok.hl ? BRAND.champagne : BRAND.ivory }}>
              {tok.t}
              {j < line.length - 1 ? " " : ""}
            </span>
          ))}
        </div>
      ))}
    </div>
  );
};

export const Captions: React.FC<{ pages: CaptionPage[] }> = ({ pages }) => {
  const { height } = useVideoConfig();
  // Vertical centre at 69% of the frame: below her hands, above Instagram's caption / button area, clear of her face.
  return (
    <AbsoluteFill style={{ alignItems: "center" }}>
      <div style={{ position: "absolute", top: height * 0.69, transform: "translateY(-50%)", display: "flex", justifyContent: "center", width: "100%" }}>
        {pages.map((p) => (
          <div key={p.startMs} style={{ position: "absolute", transform: "translateY(-50%)" }}>
            <Page page={p} />
          </div>
        ))}
      </div>
    </AbsoluteFill>
  );
};
