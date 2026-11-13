import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";

// A soft petrol fall-off across the lower part of the frame. It seats the captions without a box and deepens the grade.
export const Scrim: React.FC<{ contentFrames: number }> = ({ contentFrames }) => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill
      style={{
        opacity: interpolate(frame, [0, 10, contentFrames - 8, contentFrames], [0, 1, 1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
        background: "linear-gradient(to top, rgba(12,34,32,0.80) 0%, rgba(12,34,32,0.62) 14%, rgba(12,34,32,0.40) 27%, rgba(12,34,32,0.14) 38%, rgba(12,34,32,0) 47%)",
      }}
    />
  );
};
