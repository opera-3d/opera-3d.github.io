# OPERA paper evidence (for the website Evidence section)

Source: `OPERA.pdf (70 pages, PDF created 2026-11-17)`. Machine-readable twin: `docs/paper_evidence.json`.

All values copied as printed in the PDF text layer. No statistics were computed, re-rounded or inferred. Percentages/deltas appear only where the paper prints them. Bold/best-value markup of the tables is not transcribed.

## Paper identity

- Title as printed: **OPERA: Title of the manuscript** — PLACEHOLDER.
- Authors as printed: **First Author — Institution, Country** — PLACEHOLDER.
- Page 1 and the PDF metadata both carry the template title 'OPERA: Title of the manuscript' and author 'First Author / Institution, Country'. Do not use either on the website; the real title and author list must come from the owner.
- Keywords: Single-image 3D generation, Perceptual alignment, Multiview diffusion, Native 3D flow matching.

## Abstract gist (paraphrase)

OPERA is a unified perceptual-alignment framework for instance-faithful single-image 3D generation: lightweight alignment modules map a frozen generator's intermediate representations to pretrained perceptual representations, and the discrepancy with input-derived targets guides sampling. It is instantiated as gradient-based denoising guidance for multiview diffusion (Era3D) and velocity guidance for native 3D flow matching (TRELLIS.2), with backbones and perception models frozen (abstract, p.1).

## Headline numbers

- Abstract / introduction: None. The abstract (p.1) and introduction (pp.2-5) contain no numeric results; they make qualitative claims only (improvements on GSO, OmniObject3D, Toys4K; cross-dataset generalisation without target-domain training; 'strongest instance fidelity among the evaluated systems').
- Numbers printed in the results text:
  - p.22, Table 1: Mean CD decreases by 30.4% on GSO and 24.8% on OmniObject3D, while PSNR increases by 0.88 dB and 0.81 dB, respectively (Era3D, combined guidance vs baseline). Caveat: Same paragraph: 'Paired tests do not establish a CD improvement on GSO (p = 0.280); on OmniObject3D, the strongest adjusted evidence is for PSNR and LPIPS rather than CD.'
  - p.28, Table 6: Toys4K structure guidance: 'CD-L2 decreases by 11.0%'; F1@0.01 and F1@0.02 improve with p = 10^-4 and p = 3 x 10^-4. Caveat: Table 6 prints p = 0.1075 for the CD-L2 comparison.
  - p.29, Table 8: Versus ReconViaGen on Toys4K: CD-L2 reduced by 34.7%, from 0.014378 to 0.009387; F1@0.01 increased by 49.4%, from 0.2861 to 0.4273; on the common appearance subset PSNR +1.789 dB and LPIPS -0.0228; all six paired comparisons favour OPERA with unadjusted p < 10^-5.
  - p.33, Table 10: Cross-domain CD-L2 decreases by 13.2% (MedShapeNet), 18.6% (Medical Sketchfab), 24.4% (Smithsonian), 19.0% (AntScan), 'an average of 18.8%, compared with 11.0% on Toys4K'.
  - p.33, Table 10: Smithsonian: PSNR increases by 0.89 dB (24.72 to 25.61) and LPIPS decreases by 9.1% (0.0649 to 0.0590); PSNR +0.77 dB MedShapeNet, +0.23 dB Medical Sketchfab, +0.12 dB AntScan.
  - p.29, Table 8: Alignment-module training cost: approximately 3.7 H100 GPU-hours (structure) and 7.1 H100 GPU-hours (material); combined reuses both. Caveat: Costs exclude backbone pretraining, preprocessing and hyperparameter search; the paper states Table 8 'does not establish a numerical training-cost advantage' over external methods.
  - p.36, Table 11: Guided inference time ratio: Era3D 1.37x, TRELLIS.2 5.47x.

## Old website headline check

| Old claim | Still supported exactly? |
|---|---|
| 30.4% mean Chamfer reduction, GSO, 30 objects, Era3D combined guidance | YES |
| 24.8% mean Chamfer reduction, OmniObject3D, 100 objects, Era3D combined guidance | YES |

Sec. 5.1.2 text, p.22: 'Mean CD decreases by 30.4% on GSO and 24.8% on OmniObject3D'; values in Table 1 (p.22): GSO CD 16.46 -> 11.45, OmniObject3D CD 35.78 -> 26.89. Cohort sizes: 'means over 30 GSO objects or 100 OmniObject3D objects' (p.22).

Caveats the paper attaches (should accompany the numbers):
- Paired tests do not establish a CD improvement on GSO (p = 0.280) (p.22).
- On OmniObject3D the strongest adjusted evidence is for PSNR and LPIPS, not CD (p.22; Appendix E.1, p.51).
- Appendix E.1 (p.51): analyses are exploratory; settings were selected on the evaluation sets; all arms use one sampling seed (42).
- The semantic target differs by dataset: Caption-T5 on GSO, DINOv3 on OmniObject3D (Table 1 footnote).

## Method notes (paraphrased, with page refs)

### Frozen backbone + frozen perception

- Both generative backbones and the perception models are kept frozen; only alignment modules are trained. (p.1)
- Perceptual knowledge informs sampling 'without retraining, fine-tuning, or modifying the generative backbone'; restricting training to alignment modules avoids costly backbone adaptation. (p.8)
- Only the alignment-module parameters are learned; the generator and perception models remain frozen. (p.11)
- Although network parameters are frozen, their operations stay differentiable with respect to the input state, so gradients flow through GPAM and the generator to the sampling state. (p.12)
- For flow matching, OPERA changes the state from which the flow continues while keeping the pretrained velocity model fixed; setting the guidance scale to 0 recovers the original update. (p.18)

### Lightweight GPAM

- A generation-perception alignment module (GPAM) is trained to predict each perceptual target from the corresponding intermediate generative representation. (p.8)
- A separate GPAM is learned per selected perceptual target, pairing a frozen perception extractor with a trainable alignment module. (p.10)
- Era3D GPAM = Feature Aggregation (selected frozen U-Net decoder stages, softmax-weighted) + Perception Mapping (MLP for the global Caption-T5 target; lightweight convolutional decoder for spatial DINO/depth targets). (p.13-14)
- TRELLIS.2 structure GPAM aggregates selected DiT block features into 3D volumes and projects them along camera rays to predict VGGT features; material GPAM interpolates DiT features at visible surface points to predict DINOv3 features. (p.18-19)
- Training data: Era3D GPAMs on 1,000 Objaverse objects (900 train / 100 val); TRELLIS.2 GPAMs on Objaverse with 1000 training and 100 validation objects. (p.21, 26)
- Training cost approx. 3.7 H100 GPU-hours (structure modules, 20k steps) and 7.1 H100 GPU-hours (material heads, 5k steps each), single H100, backbone frozen. (p.29-30)

### Sampling-time guidance

- The target s_k = P_k(y) is computed once from the input image and held fixed; the GPAM prediction evolves with the sampling state, defining a perceptual energy. (p.11)
- The guidance gradient is the derivative of that energy with respect to the sampling state; the state is corrected by a scaled, normalised/preconditioned gradient and the sampler advances from the corrected state. (p.11-12)
- The correction acts on the multiview latent state before a DDIM transition (diffusion) and on the current flow state before an Euler step (flow matching). (p.12)
- Stated limit: a local energy decrease does not guarantee lower energy after the next generative transition, nor improved fidelity on unobserved surfaces. (p.12)
- Auxiliary losses that need ground-truth information are excluded at inference. (p.11)
- Guidance adds sampling cost (Table 11: 1.37x Era3D, 5.47x TRELLIS.2): the framework trades extra inference computation for instance fidelity. (p.36-37)

### Stage dependencies — multiview diffusion (Era3D)

- Era3D jointly generates colour images and normal maps for N views; OPERA intervenes during view synthesis using decoder activations that carry cross-view information. (p.6-7)
- The backbone's image conditioning, cross-view interactions, schedule, classifier-free guidance and the original surface reconstruction pipeline are retained; reconstruction itself is not guided (Fig. 6: '(not guided)'). (p.12, 16)
- The input-aligned view is compared pointwise with the target; neighbouring views are compared structurally (CKA). Cross-view interactions propagate gradients to all view latents. (p.14-15)
- Each guided timestep: one latent correction over all views and both domains, U-Net re-evaluated, then the DDIM transition. Combined guidance RMS-normalises each target's gradient per colour/normal domain before mixing with weights (lambda_d, lambda_s). (p.15-16)
- Settings: eta_d = 2.5e-3 (depth), eta_s = 1e-3 (semantic), (lambda_d, lambda_s) = (0.75, 0.25); 40 DDIM steps, CFG 3.0, unchanged from baseline. (p.21)
- Because a separate downstream reconstruction stage produces the 3D object, better views need not yield proportional geometry improvements. (p.36)

### Stage dependencies — native 3D flow matching (TRELLIS.2)

- TRELLIS.2 has three sequential flows: sparse structure (active voxel layout) -> shape (geometry latents on that layout) -> material (appearance conditioned on image and geometry). (p.7, 16)
- OPERA guides the first and third stages. The shape sampler is unchanged, and geometry stays fixed during material sampling. (p.17)
- Structure flow is guided with VGGT features; structure guidance influences shape only through the generated layout. (p.16, 18)
- Material flow is guided with DINOv3 features, optionally plus an input-view RGB energy (DINOv3 + RGB); RGB guidance stops gradients through the velocity prediction. (p.19-20)
- Ground-truth layout supervision (auxiliary head) is training-only and discarded at inference; the RGB module is trained on ground-truth renders but uses only the input view at inference. No ground truth is needed at inference. (p.19)
- Structure and material alignment modules are trained independently, no gradient passes back through a completed stage, and they are combined without joint retraining. (p.21)
- Material camera fitting gate: fitted silhouette IoU below 0.8 disables material guidance for that object; non-finite/zero gradients leave that step unguided; such cases count in coverage, not as successful guidance. (p.49)

## Tables

Direction: (↓) lower is better, (↑) higher is better. Role column: OPERA / backbone baseline / external.

### Table 1 (p.22)

Caption (verbatim): "Table 1: Quantitative evaluation on Era3D."

Footnote (verbatim): "CD is reported in units of 10^-3. Caption-T5 and DINOv3 are used as semantic models on GSO and OmniObject3D, respectively."
- Backbone: Era3D (multiview diffusion)
- Seeds: one sampling seed (42) for all arms (Appendix E.1, p.51)

**GSO** (n = 30 objects)

| Method | Role | CD ↓ | IoU ↑ | F1@.1 ↑ | PSNR ↑ | SSIM ↑ | LPIPS ↓ |
|---|---|---|---|---|---|---|---|
| Baseline | backbone baseline | 16.46 | 0.531 | 0.801 | 21.54 | 0.9222 | 0.0705 |
| + Depth | OPERA | 11.64 | 0.558 | 0.833 | 22.21 | 0.9272 | 0.0624 |
| + Semantic | OPERA | 15.51 | 0.529 | 0.803 | 21.70 | 0.9235 | 0.0690 |
| + Combined | OPERA | 11.45 | 0.574 | 0.842 | 22.42 | 0.9283 | 0.0613 |

**OmniObject3D** (n = 100 objects)

| Method | Role | CD ↓ | IoU ↑ | F1@.1 ↑ | PSNR ↑ | SSIM ↑ | LPIPS ↓ |
|---|---|---|---|---|---|---|---|
| Baseline | backbone baseline | 35.78 | 0.499 | 0.683 | 20.44 | 0.9162 | 0.0842 |
| + Depth | OPERA | 33.49 | 0.526 | 0.698 | 20.71 | 0.9179 | 0.0804 |
| + Semantic | OPERA | 28.89 | 0.503 | 0.693 | 21.02 | 0.9183 | 0.0773 |
| + Combined | OPERA | 26.89 | 0.512 | 0.705 | 21.25 | 0.9205 | 0.0746 |

Printed summary: Mean CD decreases by 30.4% on GSO and 24.8% on OmniObject3D, while PSNR increases by 0.88 dB and 0.81 dB, respectively (p.22).

Caveats / coverage:
- Paired tests do not establish a CD improvement on GSO (p = 0.280) (p.22).
- On OmniObject3D the strongest adjusted evidence is for PSNR and LPIPS rather than CD (p.22); geometry metrics do not reach pHolm < 0.05 (p.51).
- On Era3D-GSO none of the six baseline comparisons meets the adjusted threshold (p.51).
- On OmniObject3D depth alone retains higher IoU than combined (p.22).
- Exploratory: settings were selected on the evaluation sets; single sampling seed (p.51).
- Performance tables report means; CD between meshes normalised to a unit sphere; IoU on a 256^3 grid (p.22).

### Table 6 (p.28)

Caption (verbatim): "Table 6: Geometric quality on Toys4K."
- Backbone: TRELLIS.2 (native 3D flow matching)
- Cohort: Toys4K
- N: fixed cohort of 1,250 objects (p.26); geometry includes 1,083 objects passing ground-truth self-control, 167 excluded by that protocol (Appendix D, p.51)
- Seeds: seed 0, one generation seed (pp.50-51)

| Method | Role | CD-L2 ↓ | p | F1@.01 ↑ | p | F1@.02 ↑ | p |
|---|---|---|---|---|---|---|---|
| Baseline | backbone baseline (TRELLIS.2) | 0.010546 | – | 0.416083 | – | 0.650337 | – |
| Structure | OPERA | 0.009387 | 0.1075 | 0.427310 | 0.0001 | 0.661241 | 0.0003 |

Printed summary: CD-L2 decreases by 11.0%. Both F1@0.01 and F1@0.02 improve significantly, with p = 10^-4 and p = 3 x 10^-4 (p.28).

Caveats / coverage:
- The CD-L2 comparison has p = 0.1075 as printed in Table 6.
- Two-sided sign-flip p-values, unadjusted unless stated; object is the statistical unit (p.50).
- CD-L2 is reported without rescaling (diffusion tables use units of 10^-3); meshes normalised to unit sphere and ICP-aligned (p.26).
- Settings were selected on DEV32 (32 Objaverse objects) and transferred to Toys4K without further tuning (p.28).

### Table 7 (p.28)

Caption (verbatim): "Table 7: Appearance quality on Toys4K."
- Backbone: TRELLIS.2 (native 3D flow matching)
- Cohort: Toys4K
- N: Material appearance covers 1,250 objects, structure 1,249, Structure + Material 1,248; the baseline row reports all 1,250 objects; each test restricts both methods to their common objects (Appendix D, p.51)
- Seeds: seed 0, one generation seed (pp.50-51)

| Method | Role | PSNR ↑ | p | SSIM ↑ | p | LPIPS ↓ | p |
|---|---|---|---|---|---|---|---|
| Baseline | backbone baseline (TRELLIS.2) | 23.8986 | – | 0.9436 | – | 0.0728 | – |
| Structure | OPERA | 24.0595 | < 0.0001 | 0.9441 | 0.0132 | 0.0702 | < 0.0001 |
| Material | OPERA | 24.1887 | < 0.0001 | 0.9438 | 0.0039 | 0.0723 | < 0.0001 |
| Structure + Material | OPERA | 24.3769 | < 0.0001 | 0.9444 | 0.0001 | 0.0697 | < 0.0001 |

Caveats / coverage:
- The material primary result includes 99 camera-gated objects and three unguided memory fallbacks; guided-subset results are sensitivity analyses, not replacements for the primary cohort (p.51).
- Gate definition: fitted silhouette IoU below 0.8 disables material guidance for that object (p.49).
- Missing exports are not imputed (p.51).
- Appearance on 25 views (input view + 24 novel views) against rendered ground truth, PSNR in dB (p.26).
- All Toys4K comparisons use one generation seed; intervals describe variation across objects, not seeds (pp.50-51).

### Table 8 (p.30)

Caption (verbatim): "Table 8: External comparisons on Toys4K."
- Backbone: TRELLIS.2 (OPERA rows); external systems as listed
- Cohort: Toys4K
- N: same input images and evaluation protocol (p.29); coverage as Tables 6-7; appearance comparison with ReconViaGen is on 'the common appearance subset' (size not printed); Hi3DGen vs TRELLIS paired CD test n = 1,078 (p.29)
- Seeds: seed 0, one generation seed (pp.50-51)

| Method | Role | Training cost (GPU h) | CD-L2 ↓ | F1@.01 ↑ | F1@.02 ↑ | PSNR ↑ | SSIM ↑ | LPIPS ↓ |
|---|---|---|---|---|---|---|---|---|
| TRELLIS | external (unmodified backbone of Hi3DGen) | ≈9,984 (A100) | 0.014117 | 0.3355 | 0.5714 | 21.376 | 0.9377 | 0.0850 |
| Hi3DGen | external, geometry-only (no appearance values printed) | Not available | 0.014728 | 0.2986 | 0.5401 | – | – | – |
| TRELLIS.2 | backbone baseline | Not available | 0.010546 | 0.4161 | 0.6503 | 23.899 | 0.9436 | 0.0728 |
| ReconViaGen | external (released v0.5 single-image configuration, with TRELLIS.2) | Not available | 0.014378 | 0.2861 | 0.5088 | 22.587 | 0.9391 | 0.0924 |
| Ours (Structure) | OPERA | ≈3.7 (H100) | 0.009387 | 0.4273 | 0.6612 | 24.0595 | 0.9441 | 0.0702 |
| Ours (Material) | OPERA | ≈7.1 (H100) | 0.010546 | 0.4161 | 0.6503 | 24.1887 | 0.9438 | 0.0723 |
| Ours (Structure + Material) | OPERA | ≈10.8 (H100) | 0.009387 | 0.4273 | 0.6612 | 24.3769 | 0.9444 | 0.0697 |

Printed summary: Compared with ReconViaGen, the combined configuration reduces CD-L2 by 34.7%, from 0.014378 to 0.009387, and increases F1@0.01 by 49.4%, from 0.2861 to 0.4273. On the common appearance subset, it improves PSNR by 1.789 dB and reduces LPIPS by 0.0228. All six paired metric comparisons favour OPERA, with unadjusted p < 10^-5 (p.29).

Caveats / coverage:
- Comparisons assess complete systems under a shared protocol; gains from OPERA are established against the unmodified backbone (p.29).
- Hi3DGen is built on the earlier TRELLIS backbone and reports geometry only; it 'does not demonstrate an improvement over image-conditioned TRELLIS on this benchmark': F1 lower, paired mean CD difference not significant (p = 0.603, n = 1,078) (p.29).
- Material-only rows repeat the baseline geometry values because material guidance reuses baseline geometry (p.50).
- Training costs exclude backbone pretraining, preprocessing and hyperparameter search; comparable training times are unavailable for external methods, so Table 8 'does not establish a numerical training-cost advantage' (p.29).

### Table 9 (p.30)

Caption (verbatim): "Table 9: Ground-truth supervision ablation on Toys4K."
- Backbone: TRELLIS.2
- Cohort: Toys4K
- N: as Tables 6-7; structure without ground-truth layout supervision covers 1,248 objects (p.51)
- Seeds: seed 0

| Method | Role | Ground-truth supervision | CD-L2 ↓ | F1@.01 ↑ | F1@.02 ↑ | PSNR ↑ | SSIM ↑ | LPIPS ↓ |
|---|---|---|---|---|---|---|---|---|
| Structure | OPERA ablation | – | 0.009726 | 0.4294 | 0.6649 | 24.0279 | 0.9438 | 0.0708 |
| Structure | OPERA | ✓ | 0.009387 | 0.4273 | 0.6612 | 24.0595 | 0.9441 | 0.0702 |
| Material | OPERA ablation | – | 0.010546 | 0.4161 | 0.6503 | 23.9245 | 0.9433 | 0.0733 |
| Material | OPERA | ✓ | 0.010546 | 0.4161 | 0.6503 | 24.1887 | 0.9438 | 0.0723 |
| Structure + Material | OPERA ablation | – | 0.009726 | 0.4294 | 0.6649 | 24.0605 | 0.9437 | 0.0712 |
| Structure + Material | OPERA | ✓ | 0.009387 | 0.4273 | 0.6612 | 24.3769 | 0.9444 | 0.0697 |

Caveats / coverage:
- Layout supervision improves LPIPS (p = 0.0437); differences in the remaining metrics are not statistically significant; benefit 'modest' (p.30).
- RGB supervision improves all three appearance metrics over DINOv3 alone (p < 0.0001); PSNR +0.264 dB (p.31).
- Both forms together vs neither: all three appearance metrics improve (p < 0.00005); PSNR +0.312 dB (p.31).
- Note as printed: the rows without layout supervision have higher F1@.01/F1@.02 than the supervised rows.

### Table 10 (p.33)

Caption (verbatim): "Table 10: Cross-domain transfer."
- Backbone: TRELLIS.2; OPERA = Structure + Material configuration, GPAMs trained on Objaverse only, no retraining or re-tuning (pp.31, 33)
- N: 30 objects per dataset, 120 in total; Medical (pooled) = 60 objects (pp.31-32)
- Seeds: not stated for this table; evaluation 'follows Sec. 5.2.1 and Appendix D' (p.33)

**MedShapeNet** (n = 30)

| Method | Role | CD-L2 ↓ | CD-L2 change (as printed) | F1@.01 ↑ | F1@.02 ↑ | PSNR ↑ | SSIM ↑ | LPIPS ↓ |
|---|---|---|---|---|---|---|---|---|
| TRELLIS.2 | backbone baseline | 0.0448 | – | 0.117 | 0.247 | 26.47 | 0.9669 | 0.1032 |
| OPERA | OPERA | 0.0389 | ↓13.2% | 0.129 | 0.274 | 27.24 | 0.9675 | 0.1001 |

**Medical Sketchfab** (n = 30)

| Method | Role | CD-L2 ↓ | CD-L2 change (as printed) | F1@.01 ↑ | F1@.02 ↑ | PSNR ↑ | SSIM ↑ | LPIPS ↓ |
|---|---|---|---|---|---|---|---|---|
| TRELLIS.2 | backbone baseline | 0.0304 | – | 0.152 | 0.311 | 19.23 | 0.9257 | 0.1554 |
| OPERA | OPERA | 0.0248 | ↓18.6% | 0.165 | 0.335 | 19.46 | 0.9269 | 0.1518 |

**Medical (pooled)** (n = 60)

| Method | Role | CD-L2 ↓ | CD-L2 change (as printed) | F1@.01 ↑ | F1@.02 ↑ | PSNR ↑ | SSIM ↑ | LPIPS ↓ |
|---|---|---|---|---|---|---|---|---|
| TRELLIS.2 | backbone baseline | 0.0376 | – | 0.134 | 0.279 | 22.85 | 0.9463 | 0.1293 |
| OPERA | OPERA | 0.0318 | ↓15.4% | 0.147 | 0.305 | 23.35 | 0.9472 | 0.1260 |

**Smithsonian** (n = 30)

| Method | Role | CD-L2 ↓ | CD-L2 change (as printed) | F1@.01 ↑ | F1@.02 ↑ | PSNR ↑ | SSIM ↑ | LPIPS ↓ |
|---|---|---|---|---|---|---|---|---|
| TRELLIS.2 | backbone baseline | 0.0198 | – | 0.207 | 0.387 | 24.72 | 0.9505 | 0.0649 |
| OPERA | OPERA | 0.0150 | ↓24.4% | 0.221 | 0.415 | 25.61 | 0.9506 | 0.0590 |

**AntScan (Katzke et al., 2026)** (n = 30)

| Method | Role | CD-L2 ↓ | CD-L2 change (as printed) | F1@.01 ↑ | F1@.02 ↑ | PSNR ↑ | SSIM ↑ | LPIPS ↓ |
|---|---|---|---|---|---|---|---|---|
| TRELLIS.2 | backbone baseline | 0.0196 | – | 0.187 | 0.359 | 26.19 | 0.9461 | 0.1167 |
| OPERA | OPERA | 0.0159 | ↓19.0% | 0.205 | 0.379 | 26.31 | 0.9443 | 0.1122 |

Printed summary: CD-L2 decreases by 13.2% (MedShapeNet), 18.6% (Medical Sketchfab), 24.4% (Smithsonian), and 19.0% (AntScan), an average of 18.8%, compared with 11.0% on Toys4K (p.33).

Caveats / coverage:
- No p-values are printed for Table 10.
- Datasets provide meshes but no input images: each ground-truth mesh is rendered from a single frontal view; untextured meshes (MedShapeNet, AntScan) are rendered with a uniform grey material, which limits what PSNR/LPIPS can show (pp.33-34).
- SSIM decreases slightly on AntScan (0.9461 to 0.9443) (p.33).
- The paper's explanations for the pattern 'are not tested by a separate ablation in this setting' (p.34).
- Stated limitations: both methods smooth fine surface detail; OPERA's meshes contain small holes; on the Subhyracodon gidleyi jaw the two methods are similar (p.35).

### Table 16 (p.55)

Caption (verbatim): "Table 16: Comparison with external generators on GSO (30 objects). Values are means. OPERA uses combined depth and semantic guidance. F1@0.1 uses a distance threshold of 0.1 unit-sphere radii. Appearance scores depend on the pose handling described below."
- Backbone: Era3D + OPERA vs complete external pipelines
- Cohort: GSO
- N: 30 objects
- Seeds: Era3D arms use sampling seed 42 (p.51); not stated for external generators

| Method | Role | F1@0.1 ↑ | PSNR ↑ | SSIM ↑ | LPIPS ↓ |
|---|---|---|---|---|---|
| Era3D + OPERA | OPERA | 0.842 | 22.42 | 0.9283 | 0.0613 |
| SAM 3D Objects | external | 0.903 | 18.95 | 0.9180 | 0.0758 |
| TRELLIS.2 | external | 0.936 | 19.99 | 0.9213 | 0.0694 |

Caveats / coverage:
- External generators obtain higher F1@0.1; OPERA configurations have higher mean PSNR/SSIM and lower mean LPIPS (p.55).
- Appearance scores reflect pose alignment as well as geometry and texture and 'should not be interpreted as an isolated comparison of texture quality' (p.55).
- Complete-pipeline comparison; the contribution of guidance is measured against each corresponding backbone (p.55).
- Discussion (p.36): guided Era3D still achieves lower geometric accuracy than unmodified TRELLIS.2 in the GSO comparison.

### Table 11 (p.36)

Caption (verbatim): "Table 11: Computational cost of baseline and guided inference."

| Method | Role | Hardware | Baseline (s) ↓ | Guided (s) ↓ | Ratio |
|---|---|---|---|---|---|
| Era3D | backbone / guided | H100 80 GB | 112.7 ± 1.3 | 154.0 ± 3.9 | 1.37× |
| TRELLIS.2 | backbone / guided | H100 80 GB | 13.3 ± 3.2 | 72.7 ± 18.9 | 5.47× |

Caveats / coverage:
- Era3D additionally needs approximately 2 minutes of NeuS reconstruction per object; multi-view generation approximately 2.5 minutes (p.21).

## General caveats

- External methods are contextual, complete-system comparisons; the effect of OPERA is measured against its own frozen backbone (pp.29, 55).
- Hi3DGen is geometry-only in Table 8 (appearance cells are '–').
- Toys4K coverage: geometry 1,083 objects (167 excluded by ground-truth self-control); appearance 1,250 / 1,249 / 1,248 depending on arm; 99 camera-gated objects and three unguided memory fallbacks are included in the material primary result (p.51).
- The paper does not claim every object improves: it reports means with paired tests, a failure-case figure (Fig. 14, p.57: surface discontinuities, degraded details, fragmented surfaces), view-dependent gains in Fig. 10 (p.23), and notes the DEV32 PSNR gain is sensitive to one predefined outlier object (p.50).
- Diffusion results (GSO, OmniObject3D) are single-seed (42) and exploratory; Toys4K results are single-seed (0); DEV32 parameter studies use seeds 0, 1, 2 (pp.50-51).
- Scoring parity between Mac and HPC hosts was checked on four objects only (p.51).

## Not found in the paper

- No qualitative figure is explicitly labelled as Toys4K (Fig. 12 caption says only 'Qualitative results with TRELLIS.2').
- No per-object win/loss counts or improved-fraction statistics are printed in the main-text tables used here.
- Seed for Table 10 is not stated explicitly.
