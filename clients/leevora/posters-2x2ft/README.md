# leevorá: 2 × 2 ft treatment posters

Two in-clinic posters in the standee's visual system: deep bottle-green, cream Gloock headline with one aqua
accent, gold line icons, the client's own vector logo, and a real-looking photo in a rounded gold-line frame.
The copy is the client's, word for word. There is no QR code and no phone number.

| Poster | Print file |
|---|---|
| Benefits of CoolSculpting Treatment | `print/Leevora_Benefits_of_CoolSculpting_Treatment_2x2ft_PRINT_CMYK.pdf` |
| What laser hair reduction can do for you | `print/Leevora_Laser_Hair_Reduction_Poster_2x2ft_PRINT_CMYK.pdf` |

Every file is trim 610 × 610 mm, with 10 mm bleed, 40 mm safe area, CMYK FOGRA39 and outlined type. The folder
also has a flattened CMYK TIFF and an sRGB master. Previews and a wall mockup are in `previews/`.
Rebuild with `source/engine/poster.py cool|laser`. It uses the same fonts, logo JSON and ICC profile as the standee.

## CoolSculpting: "Walk in / Walk out" version (licensed stock)
`source/engine/poster_door.py` builds the door diptych. On the left she walks in (back view, oversized sweater).
On the right she walks out (fitted dress, light). The rest is the client's copy, plus WALK IN / WALK OUT tags and
the licence disclaimer "Images are illustrative and posed by models. Individual results vary."
Photos: iStock 1182388957 (Erstudiostok) and 1687013196 (Luca Ladi Bucciolini). Both are model-released;
license the XL size. Put the files at `licensed/iStock-<id>.jpg` and run `MODE=final poster_door.py` for the
CMYK print PDF and TIFFs. The watermarked comps are not stored in this repo.
