# Font build

1. `node exp.js` exports glyph outlines from the Kɔradin Structure engine (`eng.js`, extracted from the Structure artifact) with overrides from `ovr.js` → `display.json`, `text.json` (also `#s` short variants for the reduplication dash).
2. `python3 build2.py` builds `SakyiraText-Regular.otf` and `SakyiraDisplay-BoldSlanted.otf` (fontTools, skia-pathops, feaLib). Takes ~10 min (two-sign reduplication rules).
3. Check with `python3 -m ots <font>` and `spec.py` (uharfbuzz specimen).

Hand-drawn glyphs from Ntirikwaamaa live in `ovr/*.svg` (Illustrator export, viewBox 0 -1000 W 1260) and are mapped in `OVR_D` in build2.py.
`CLIP` in build2.py trims diagonal end caps sticking out of box sides (pa, ba).
