import { loadFont } from "@remotion/fonts";
import { staticFile } from "remotion";

// Caption system matched to the agency team's edit (measured from "LEEVORA NEW 1RC.mp4"):
// Inter Tight (SIL OFL) for captions; a high-contrast serif for the opening title (Gloock, the closest open match to the team's title and the logo).
export const TEAM_SANS = "Inter Tight";
export const TEAM_SERIF = "Gloock";
export const TEAM = { white: "#F0ECE2", gold: "#C7AF83", petrol: "#173B39", petrolDark: "#0E2422" } as const;

export const teamFontsReady = Promise.all([
  loadFont({ family: TEAM_SANS, url: staticFile("fonts/InterTight-Variable.ttf"), weight: "400 800" }),
  loadFont({ family: TEAM_SERIF, url: staticFile("fonts/Gloock-Regular.ttf"), weight: "400" }),
]);
