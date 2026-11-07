# FRENUGO / BridgeMoney visual reproduction

The home page follows the observed section order: animated hero, white five-wordmark panel, rounded card grid, earning ticker, oversized pink introduction, How It Works, three image/text steps, coin ribbon, sculpted gold lettering, coin tunnel/counter, white CTA, ruled footer.

## Original assets and licenses

- All 3D models were authored for this repository. `scripts/render/scenes.py` builds the coin, banknote, phone, card, banks and gold script lettering in Blender. No model, image, video, stylesheet or script was downloaded from BridgeMoney.
- `scripts/render/textures.py` generates FRENUGO's phone display textures and prepares the OFL fonts for rendering.
- Archivo and DM Sans are self-hosted through Fontsource and distributed under the SIL Open Font License. Allura's license is at `public/fonts/ALLURA-LICENSE.txt`.
- Live Three.js scene source is retained in `src/scripts/bridge-scenes.ts`. The production page uses Blender renders and animates the two coin poses with CSS transforms and opacity.
- Static scene outputs are `public/visuals/*.webp`. The two coin poses are `src/assets/coin-*.webp`. PNG intermediates and render frames are reproducible and intentionally excluded from Git.

## Content adaptation

The FRENUGO wordmark replaces Bridge. Brand-specific third-party press endorsements, reviews, customer names, app-store links and member earnings are not represented as FRENUGO facts. Those slots retain their visual structure with project links, neutral cards and the existing author-reported 4,619 USD historical PnL. Internal statistics, signals and legal routes remain available. Existing GitHub Pages workflow and base-path handling are preserved.

## Rebuild visual assets

Use Blender 4.3+, Python with Pillow/fontTools/brotli, and the installed npm font packages:

```
python scripts/render/textures.py
blender -b -t 6 -P scripts/render/scenes.py
python scripts/render/pack.py
```

## Validation

- Reference inspected at 1363 × 936. Each desktop section was compared with the implementation at that viewport; the hero, wordmark panel, cards, ticker, introduction, steps, coin ribbon, gold text, counter, CTA and footer were opened and inspected.
- Both pages were opened side by side in 390 × 844 iframes. This exposed the reference's single mobile coin, hamburger, full-width pink CTA, single card column, centered banknote and stacked steps. These differences were corrected. A later attempt to reload the comparison harness was rejected by the browser URL policy; the final mobile revision could not be fully rechecked in that harness. No attempt was made to bypass the policy.
- Desktop section positions after adjustment: white panel 983.83 px, cards 1415.34 px, ticker 2365.00 px, intro 2640.69 px, steps 4399.25 px, coin ribbon 6594.55 px, gold title 7027.42 px, counter 7609.42 px and CTA 8499.50 px. Main section offsets differ from the observed reference by less than 0.5 px at this width; content and font outlines remain approximations.
- Gold coins use two 640 px transparent WebP renders. Static scenes use up to 384 Cycles samples. Off-screen coin animations pause and reduced-motion uses still poses.
- `npm run check`: zero errors, warnings or hints. Production build with `BASE_PATH=/frenchug/` succeeds. All home-page internal links, anchors and linked assets resolve in the build; the temporary comparison harness is excluded.
- The first implementation commit `6bf2a6b` was deployed by GitHub Actions run `42280464328`, conclusion `success`. Final deployment is verified separately after the visual adjustment commit.

This is an independently implemented visual reconstruction. Licensed typefaces, third-party brand artwork, testimonials and source models from the reference are not copied. Archivo/DM Sans/Allura and the original models produce visible differences from the reference.
