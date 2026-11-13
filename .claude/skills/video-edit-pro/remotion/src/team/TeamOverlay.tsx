import React, { useEffect, useState } from "react";
import { AbsoluteFill, Sequence, useDelayRender } from "remotion";
import { EndCard } from "../EndCard";
import { teamFontsReady } from "./fonts";
import { TeamCaptions } from "./TeamCaptions";
import { TitlePill } from "./TitlePill";
import type { TeamProps } from "./types";

const END_DISSOLVE = 10;

export const TeamOverlay: React.FC<TeamProps> = ({ pages, contentFrames, endCardFrames, pill }) => {
  const { delayRender, continueRender, cancelRender } = useDelayRender();
  const [handle] = useState(() => delayRender("Loading team fonts"));
  useEffect(() => {
    teamFontsReady.then(() => continueRender(handle)).catch((e) => cancelRender(e));
  }, [handle, continueRender, cancelRender]);
  return (
    <AbsoluteFill>
      {pill ? <TitlePill text={pill.text} fromMs={pill.fromMs} toMs={pill.toMs} /> : null}
      <TeamCaptions pages={pages} />
      {endCardFrames > 0 ? (
        <Sequence from={contentFrames - END_DISSOLVE} durationInFrames={endCardFrames + END_DISSOLVE}>
          <EndCard dissolveFrames={END_DISSOLVE} />
        </Sequence>
      ) : null}
    </AbsoluteFill>
  );
};
