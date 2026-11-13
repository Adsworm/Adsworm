import { loadFont } from "@remotion/fonts";
import { staticFile } from "remotion";

// Colours supplied for consideration by the agency; the ivory matches the logo colour in the client's own artwork.
// Confirm against the current brand book before treating as final.
export const BRAND = {
  petrol: "#173B39",
  petrolDeep: "#0C2220",
  sage: "#A9B1A2",
  ivory: "#F2EDE3",
  champagne: "#C7B183",
} as const;

// Pairing used across leevorá work: a high-contrast serif for the words that matter, a clean sans for everything else.
export const SANS = "Instrument Sans";
export const SERIF = "Gloock";

// SIL Open Font Licence for both.
export const fontsReady = Promise.all([
  loadFont({ family: SANS, url: staticFile("fonts/InstrumentSans-Variable.ttf"), weight: "400 700" }),
  loadFont({ family: SERIF, url: staticFile("fonts/Gloock-Regular.ttf"), weight: "400" }),
]);

export const EASE_OUT = [0.16, 1, 0.3, 1] as const; // soft landing, no bounce
