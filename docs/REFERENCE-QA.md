# FRENUGO / BridgeMoney visual reproduction

The home page follows the observed section order: animated hero, white five-wordmark panel, rounded card grid, earning ticker, oversized pink introduction, How It Works, three image/text steps, coin ribbon, sculpted gold lettering, coin tunnel/counter, white CTA, ruled footer.

## Original assets and licenses

- All 3D models were authored for this repository. `scripts/render/scenes.py` builds the coin, banknote, phone, card, banks and gold script lettering in Blender. No model, image, video, stylesheet or script was downloaded from BridgeMoney.
- `scripts/render/textures.py` generates FRENUGO's phone display textures and prepares the OFL fonts for rendering.
- Archivo and DM Sans are self-hosted through Fontsource and distributed under the SIL Open Font License. Allura's license is at `public/fonts/ALLURA-LICENSE.txt`.
- Live Three.js scene source is retained in `src/scripts/bridge-scenes.ts`. The production page uses the same types of authored objects rendered with Blender, then composites the 32-frame coin atlas with Canvas 2D. This works when WebGL is unavailable, including the QA browser.
- Raster outputs are `public/visuals/*.webp`. PNG intermediates and render frames are reproducible and intentionally excluded from Git.

## Content adaptation

The FRENUGO wordmark replaces Bridge. Brand-specific third-party press endorsements, reviews, customer names, app-store links and member earnings are not represented as FRENUGO facts. Those slots retain their visual structure with project links, neutral cards and the existing author-reported 4,619 USD historical PnL. Internal statistics, signals and legal routes remain available. Existing GitHub Pages workflow and base-path handling are preserved.

## Rebuild visual assets

Use Blender 4.3+, Python with Pillow/fontTools/brotli, and the installed npm font packages:

```
python scripts/render/textures.py
blender -b -t 6 -P scripts/render/scenes.py
python scripts/render/pack.py
```

Reference was inspected in the browser at 1363 × 936 and within a 390 × 844 iframe. Further validation notes are appended after publication.
