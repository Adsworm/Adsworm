# leevorá: 2 × 4 ft double-sided LED standee

Outdoor illuminated standee for leevorá Aesthetic Clinic, Subhash Nagar, New Delhi.
There are two different faces. **Side A** (woman, skin) leads with "Your mirror only shows half."
**Side B** (man, hair) leads with "Hair fall has a reason." Both carry the launch offer: free skin and hair analysis.

## Send to the vendor
| File | Use |
|---|---|
| `print/LEEVORA_Standee_2x4ft_Side{A,B}_PRINT_CMYK.pdf` | **Master.** 1:1, CMYK FOGRA39, outlined type, 10 mm bleed, crop marks, Trim/BleedBox |
| `print/..._PRINT_CMYK_10mm-bleed.tif` | Same artwork, flattened. 630 × 1239 mm @ 150 ppi |
| `print/..._FLEX-WRAP_CMYK_75mm-extension.tif` | Only for flex that wraps the frame (760 × 1369 mm) |
| `print/..._RIP-MASTER_sRGB_10mm-bleed.tif` | Only for a RIP that has an ICC profile for the actual backlit media |
| `docs/leevora_standee_VENDOR-SPEC.pdf` | Build, material, LED, colour, checklist (English + Hindi notes) |

`docs/leevora_standee_DESIGN-AUDIT.pdf` lists the 24 mistakes in the original, the reasoning behind the
redesign, day and lit-at-night simulations, and the decisions to confirm before printing.
`previews/` has day and night mockups of both faces.

## Re-rendering
`source/engine/build.py A|B` rebuilds every file for a side from `source/photos/` (the engine expects them at `hero/woman3.png|npz` and `hero/man3.png|npz` under its `ROOT`; adjust `ROOT` and `CFG` paths). The logo is the client's own vector artwork, lifted from their original PDF by `extract_logo.py` into `leevora_logo.json`; it is never retyped. To change copy, a price
anchor or a phone number, edit `CFG` / `draw_vectors()` and re-run. Requirements: Python 3.13, numpy, opencv,
skia-python, uharfbuzz, fonttools, mediapipe (landmarks are cached in the `.npz` files), qrcode, Pillow,
Ghostscript, pikepdf. The FOGRA39 ICC profile was built with ArgyllCMS from the FOGRA39L characterisation data.
Fonts (OFL): Gloock, Instrument Sans.
