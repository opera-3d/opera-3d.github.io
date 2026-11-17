# OPERA paper figure map

Source PDF: `OPERA.pdf` (70 pages, PDF created 2026-11-17; read-only).
All exports live in `static/images/paper/`.

**Source of every export: PDF page render, cropped.** Each page was rasterised with PyMuPDF at 7.5x (540 dpi),
clipped between the body text above and the caption below, then auto-trimmed to the figure's ink with a 12 px margin.
No caption text, no body text, nothing redrawn or retouched.

Original assets were searched for under `~/Research/Papers` and `~/Research/Projects` and **not found**: the
manuscript source for this PDF is not on disk there. `Papers/RQ2/IJCV/` is an empty journal template, and the figure
folders in `Papers/RQ2/{arxiv,iclr2027,NeurIPS26}/` (`teaser.pdf`, `framework.pdf`, ...) belong to older drafts dated
9 Oct with different figures, so they were not used. (`~/Documents` was not searched, as instructed.)

Encoding: diagrams and text-heavy figures are lossless WebP; the four photo-heavy figures (1, 12, 13, 14) are lossy
WebP at quality 93, checked at 100% zoom for label and thin-line legibility. No PNG fallbacks were needed.

## Owner's mapping: verdict

| Fig. | PDF page | Owner's mapping | Verdict | Caption (verbatim) | Exported file | Pixel size | Encoding |
|---|---|---|---|---|---|---|---|
| 1 | 2 | teaser | MATCH | "Figure 1: OPERA guides multiview diffusion and native 3D flow matching through perceptual alignment. The upper panels illustrate the complementary roles of the guidance components; the lower panel illustrates application domains for cross-domain transfer." | `fig01_teaser.webp` | 2939 x 2963 | lossy q93 |
| 2 | 3 | motivation (plausibility vs instance fidelity, one example per paradigm) | MATCH | "Figure 2: Instance fidelity errors in existing generative backbones." | `fig02_motivation.webp` | 2909 x 725 | lossless |
| 5 | 9 | unified perceptual-alignment / guidance diagram | MATCH | "Figure 5: Perceptual alignment and guidance in OPERA." | `fig05_unified.webp` | 2915 x 1205 | lossless |
| 6 | 13 | Multiview Diffusion (Era3D) pipeline | MATCH | "Figure 6: OPERA for multiview diffusion." | `fig06_diffusion.webp` | 2835 x 1537 | lossless |
| 7 | 14 | optional detail | MATCH (GPAM + DDIM detail for Era3D) | "Figure 7: Perceptual guidance for multiview diffusion." | `fig07_diffusion_detail.webp` | 2911 x 1833 | lossless |
| 8 | 17 | Native 3D Flow Matching (TRELLIS.2) pipeline | MATCH | "Figure 8: OPERA for native 3D flow matching." | `fig08_flow.webp` | 2823 x 1546 | lossless |
| 9 | 18 | optional detail | MATCH (structure + material guidance detail) | "Figure 9: Structure and material guidance." | `fig09_flow_detail.webp` | 2922 x 1540 | lossless |

No mismatch with the owner's mapping: all seven figure numbers, pages and subjects agree with the PDF.

## Additional figures exported

| Fig. | PDF page | Use | Caption (verbatim) | Exported file | Pixel size | Encoding |
|---|---|---|---|---|---|---|
| 3 | 7 | Background: unguided multiview-diffusion pipeline | "Figure 3: Multiview diffusion for 3D reconstruction." | `fig03_bg_diffusion.webp` | 2797 x 665 | lossless |
| 4 | 8 | Background: unguided TRELLIS.2 three-stage pipeline | "Figure 4: Native 3D flow matching." | `fig04_bg_flow.webp` | 2803 x 744 | lossless |
| 10 | 23 | Components, diffusion: Era3D / + depth / + semantic / + combined error maps (one hat object, six views) | "Figure 10: Effects of perceptual guidance on multi-view generation. Error maps are produced by calculating the pixel-wise discrepancy between generated pixels and their ground truth. MAEs are reported per view and their mean are averaged across the six views." | `fig10_diffusion_components_multiview.webp` | 2830 x 1336 | lossless |
| 11 | 24 | Diffusion qualitative: Era3D vs OPERA vs ground truth, six objects | "Figure 11: Effects of perceptual guidance on 3D reconstruction with Era3D. Each example compares Era3D, OPERA, and ground truth, with the input image shown as an inset." | `fig11_diffusion_components_recon.webp` | 2909 x 1464 | lossless |
| 12 | 32 | Components, flow: TRELLIS.2 / + guided structure / + guided material / combined / ground truth, plus ReconViaGen and Hi3DGen | "Figure 12: Qualitative results with TRELLIS.2. Structure and Material guidance improve complementary aspects of instance fidelity. Insets highlight local details; ReconViaGen and Hi3DGen provide external comparisons." | `fig12_flow_components.webp` | 2861 x 2400 | lossy q93 |
| 13 | 35 | Cross-domain qualitative (archaeology, ant scan, medical, biology) | "Figure 13: Qualitative cross-domain results. Each row shows TRELLIS.2, OPERA, and the ground truth." | `fig13_cross_domain.webp` | 2705 x 2706 | lossy q93 |
| 14 | 57 | Failure cases (useful for a limitations note) | "Figure 14: Failure cases and object-specific fidelity. From left to right: input image, ground truth, OPERA, TRELLIS.2, and SAM 3D Objects. Red shading and red-bordered close-ups highlight selected errors, including surface discontinuities, degraded details, and altered object-specific features." | `fig14_failure_cases.webp` | 2700 x 3231 | lossy q93 |

The paper has 14 figures in total; all 14 are exported.

## Notes, gaps and defects (all present in the PDF itself, not introduced by export)

- **No Toys4K qualitative figure.** No figure is labelled as Toys4K. Figure 12 is the TRELLIS.2 qualitative figure, but
  its caption does not name a dataset (objects: Badge of the Black Prince, Statue of Liberty, Armillary sphere), so
  the file is named `fig12_flow_components` and should not be captioned "Toys4K" on the site.
- **Component coverage.** Diffusion: Figure 10 shows baseline / depth / semantic / combined as per-view error maps
  for one object; Figure 1 (upper left) shows Baseline / + Depth / + Semantic / Combined renders. Figure 11 shows only
  Era3D vs OPERA. Flow: Figure 12 shows baseline / structure / material / combined; in the "+ Guided Structure Flow"
  column only the normal render is shown and in "+ Guided Material Flow" only the textured render.
- **Figure 13 label defect.** In the ANT SCAN panel the column header "OPERA" wraps onto two lines ("OPER" / "A").
- **Figures 5 and 7 (possibly 9) icon defect.** The flame ("Trainable") icons next to GPAM sit on a small white square that shows
  against the tinted box background.
- **Figure 9 overlap.** The "Input RGB" lion thumbnail slightly overlaps its label in panel B.
- **Figure 10 numbers.** The figure prints "3.1% / 12.8% / 30.8% lower vs. baseline" for mean view MAE of a single
  example object; these are per-example values, not dataset results.
- **Figure 1** is partly a composed illustration (lower "OPERA" museum scene); embedded raster resolution is about
  1672 px wide, so the 2939 px export is upsampled in that region. Labels are vector and crisp.
- Small embedded thumbnails (e.g. lion icons in Figures 3-9, 205-308 px sources) are soft at full export size; text
  and line work are vector and sharp.
