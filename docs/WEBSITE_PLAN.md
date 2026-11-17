# OPERA paper website: implementation plan

Owner-approved on 17 Nov 2026 (via Codex). This file is the working plan for the site at https://opera-3d.github.io. Keep the domain and the GitHub organisation; nothing is renamed.

## Sources of truth

- **Paper:** the current OPERA PDF. It is read only; the manuscript is never edited from here.
- **Bibliographic data:** the PDF title and authors are placeholders, so no placeholder bibliographic data is published. The site keeps its current verified identity ("Anonymous supplement") until final metadata is supplied.
- **Design base:** the existing diffusion site. Its style stays: warm white, dark type, generous spacing, one OPERA accent, no dashboard clutter.
- **Diffusion 3D models:** the existing Sketchfab collection `idea0907 / P4G-Era3D` (7 models). It is not re-uploaded, duplicated or renamed.
- **Flow 3D models:** one new Sketchfab collection, "OPERA — Native 3D Flow Matching", on the owner's account.

## Page order

1. **Hero.**
   - OPERA, plus one paper-grounded sentence: perceptual alignment for instance-faithful single-image 3D generation, across multiview diffusion and native 3D flow matching.
   - Verified Paper / Code links only, and a prominent "Explore 3D" anchor.
   - Figure 1 teaser.
2. **Motivation.**
   - Plausibility versus instance fidelity, one example per paradigm (Figure 2 and current resources).
   - Short; not the abstract again.
3. **Our approach** (central).
   - Figure 5: the unified perceptual-alignment and guidance diagram, large and click-to-enlarge.
   - Tabs below it: Multiview Diffusion (Era3D), Figure 6; Native 3D Flow Matching (TRELLIS.2), Figure 8.
   - Figures 7 and 9 are optional expandable details.
   - Text covers: frozen backbone and frozen perception, lightweight GPAM, sampling-time guidance, and stage dependencies as in the paper.
   - Figures are the paper's own: original assets, or tight crops of the PDF. No redrawn equations and no generated diagrams.
4. **Interactive gallery** (main attraction).
   - Two branches: Diffusion and Flow Matching.
   - Diffusion reuses the current images and the P4G collection.
   - Flow Matching layout:
     - Five collection filters with three objects each (list below), a thumbnail selector, and one active object.
     - The default is Mammuthus, with input + TRELLIS.2 stock + OPERA Combined as the primary comparison.
     - "More comparisons" exposes the available GT, +Structure, +Material only, ReconViaGen, Hi3DGen (and Era3D for Mammuthus).
     - Desktop: at most two active 3D viewers plus the input. Mobile: one viewer with a method toggle.
   - Viewer behaviour:
     - Fullscreen, a link to Sketchfab, descriptive names and attribution.
     - Lazy loading: inactive iframes are unloaded, with a poster fallback.
     - Same-view camera sync only if the Sketchfab Viewer API supports it in testing.
     - Appearance / Geometry control only if reliable; otherwise labelled matched-camera normal stills.
   - Links to the native research galleries stay.
5. **Components.**
   - Diffusion: baseline, semantic, depth, combined. Flow: baseline, structure, material, combined.
   - Geometry and appearance are kept distinct.
   - Only available outputs are shown, and the gated fallback is explained.
   - No claim that every selected object improves on every metric.
6. **Evidence.**
   - Compact tables and figures from the current paper for GSO, OmniObject3D, Toys4K and cross-domain results.
   - Each is sourced with cohort, metric direction, seed and coverage.
   - Old-site headline percentages are not carried over unless the current paper supports them.
   - External methods are within-backbone contextual comparisons; Hi3DGen is geometry only.
   - The qualitative gallery is labelled selected, not representative.
7. **Resources.**
   - Citation with verified metadata only; dataset and model attribution and licences.

## Flow showcase: 15 objects (IDs immutable)

Each object uses the campaign and version of the gallery it is linked from.

| group | object id | linked gallery |
|---|---|---|
| A Fossils & Natural History | `si01_triceratops_view2` | ood-results |
| A | `si02_mammuthus` | ood-results |
| A | `si25v2_a01_brachyceratops_montanensis_gilmo` | ood-results |
| B Insects / AntScan | `ant_124` | ood-results |
| B | `ant_4008` | ood-results |
| B | `ant_392` | ood-results |
| C Medical Anatomy | `ov13_10_lymphatic_system` | smithsonian-supervisor-gallery /3d/ |
| C | `f7aa60639c60483f8e82fc182d2b0514` | ood-results |
| C | `e903b83694d5455da1d71c2943dd7bab` | ood-results |
| D Biological Specimens | `si05_corallium` | ood-results |
| D | `si25_17_subhyracodon_gidleyi_wood_1927` | ood-results |
| D | `si25v2_c38_geochelone_carbonaria` | ood-results |
| E Cultural Heritage | `ov13_03_badge_of_the_black_prince` | smithsonian-supervisor-gallery /3d/ |
| E | `ov13_06_statue_of_liberty` | smithsonian-supervisor-gallery /3d/ |
| E | `ov13_02_armillary_sphere_1771` | smithsonian-supervisor-gallery /3d/ |

## Sketchfab upload rules

- **Order:** the Mammuthus pilot (8 entries) first; then the 15 objects, stock + Combined first, then the available ablation and external arms. Missing methods are not generated.
- **Files:** self-contained GLBs from the original high-quality sources, never the ~12k-face previews. Textures or vertex colours are preserved. Hi3DGen is geometry only.
- **No duplicates:** a model already uploaded is reused by UID. UIDs are recorded immediately.
- **Licences:** no new open redistribution licence is granted without the owner's choice. Models are published for viewing without a download licence.
- **GT:** uploaded only where redistribution is clearly permitted; otherwise the original public source is linked and the entry is marked pending.
- **Era3D Mammuthus:** belongs with the diffusion branch logically and is linked across, not uploaded twice.
- **Display:** every display transform and frame difference is recorded. No per-method alignment.
- **Credentials:** the API token lives only in `~/.config/opera-sketchfab/token` on the owner's machine. It is never in Git, the frontend, logs or chat.
- **Repo contents:** manifests and scripts live in Git (OPERA-Flow `tools/sketchfab_export/`, and `static/data/` here). Heavy assets stay on RDS.

## Acceptance before publishing

- Responsive on desktop and mobile; figures readable.
- Models load, with correct labels and the exact selected IDs.
- No broken links and no secrets.
- Old resources and URLs are preserved where feasible.
- Other galleries (Vercel) are not replaced.
- Anything missing (account access, rights, metadata) is stated on the page or in the report, never papered over.
