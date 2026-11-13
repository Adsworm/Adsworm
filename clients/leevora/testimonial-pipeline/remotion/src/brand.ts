import { loadFont } from "@remotion/fonts";
import { staticFile } from "remotion";

// Colours supplied for consideration by the agency; the ivory matches the logo colour in the client's own artwork.
// Confirm against the current brand book before treating as final.
export const BRAND = {
  petrol: "#173B39",
  sage: "#A9B1A2",
  ivory: "#F2EDE3",
  champagne: "#C7B183",
} as const;

export const CAPTION_FONT = "Instrument Sans";

// SIL Open Font Licence. Variable font: one file covers weights 400-700.
export const fontsReady = loadFont({
  family: CAPTION_FONT,
  url: staticFile("fonts/InstrumentSans-Variable.ttf"),
  weight: "400 700",
});
