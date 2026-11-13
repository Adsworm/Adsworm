import React, { useEffect, useState } from "react";
import { AbsoluteFill, Sequence, useDelayRender } from "remotion";
import { fontsReady } from "./brand";
import { Captions } from "./Captions";
import { EndCard } from "./EndCard";
import { Label } from "./Label";
import { Scrim } from "./Scrim";
import type { OverlayProps } from "./types";

export const END_DISSOLVE = 10; // frames the end card takes to cover the picture; it finishes on the last content frame

export const Overlay: React.FC<OverlayProps> = ({ pages, contentFrames, endCardFrames, label }) => {
  const { delayRender, continueRender, cancelRender } = useDelayRender();
  const [handle] = useState(() => delayRender("Loading fonts"));
  useEffect(() => {
    fontsReady.then(() => continueRender(handle)).catch((e) => cancelRender(e));
  }, [handle, continueRender, cancelRender]);

  return (
    <AbsoluteFill>
      <Scrim contentFrames={contentFrames} />
      {label ? <Label text={label.text} fromFrame={label.fromFrame} toFrame={label.toFrame} /> : null}
      <Captions pages={pages} />
      {endCardFrames > 0 ? (
        <Sequence from={contentFrames - END_DISSOLVE} durationInFrames={endCardFrames + END_DISSOLVE}>
          <EndCard dissolveFrames={END_DISSOLVE} />
        </Sequence>
      ) : null}
    </AbsoluteFill>
  );
};
