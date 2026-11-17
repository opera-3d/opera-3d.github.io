#!/usr/bin/env python3
"""One-off composer of index.html for the OPERA paper site (plan: docs/WEBSITE_PLAN.md). Keeps three blocks of the previous page
verbatim (Era3D Sketchfab picker, Era3D object comparison, multi-view dataset figure: their ids are used by static/app.js) and
writes the new page order around them. Numbers are copied from docs/paper_evidence.md (transcribed from the paper), not computed.
usage: build_index.py <file with the three old blocks separated by a line '====='>"""
import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
picker, showcase, multiview = open(sys.argv[1], encoding='utf-8').read().split('\n=====\n')
P = 'static/images/paper/'


def fig(src, w, h, alt, cap, zoom_title, cls=''):
    return (f'<figure class="paper-figure {cls}"><button class="zoom" data-zoom="{P}{src}" data-description="{zoom_title}" aria-label="Enlarge: {zoom_title}">'
            f'<img src="{P}{src}" alt="{alt}" loading="lazy" width="{w}" height="{h}"></button><figcaption>{cap}</figcaption></figure>')


def table(head, rows, ours=()):
    h = ''.join(f'<th scope="col">{c}</th>' for c in head)
    b = ''.join('<tr' + (' class="ours"' if i in ours else '') + '>' + ''.join((f'<th scope="row">{c}</th>' if j == 0 else f'<td>{c}</td>') for j, c in enumerate(r)) + '</tr>' for i, r in enumerate(rows))
    return f'<div class="table-scroll"><table class="evidence"><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>'


viewer = lambda s, lab: f'''<div class="fg-viewer viewer-output" data-slot="{s}"><div class="viewer-heading"><label class="fg-select"><span class="sr">{lab}</span><select aria-label="{lab}"></select></label><span class="fg-actions"><button class="text-button fg-full">Fullscreen</button><button class="text-button fg-unload" hidden>Unload</button></span></div>
        <div class="viewer-stage"><div class="viewer-cover"><img alt="" loading="lazy"><button class="button">Load interactive 3D ↗</button><p></p></div><iframe allow="autoplay; fullscreen; xr-spatial-tracking" allowfullscreen referrerpolicy="no-referrer" hidden></iframe></div>
        <div class="fg-foot"><span class="fg-method-note"></span><a class="text-button fg-link" target="_blank" rel="noopener noreferrer" hidden>Open on Sketchfab ↗</a></div></div>'''

html = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="robots" content="noindex,nofollow">
  <meta name="referrer" content="no-referrer">
  <meta name="description" content="OPERA aligns frozen 3D generators with pretrained perception models to guide sampling towards the object in the input image, for multiview diffusion and native 3D flow matching.">
  <meta name="color-scheme" content="light">
  <title>OPERA · Perceptual alignment for instance-faithful single-image 3D generation</title>
  <link rel="icon" href="static/icon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="static/style.css?v=20261117">
  <script src="static/app.js?v=20261117" defer></script>
  <script src="static/gallery.js?v=20261117" defer></script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="nav"><a class="wordmark" href="#">OPERA<span class="mark">✳</span></a><nav aria-label="Main navigation"><a href="#motivation">Motivation</a><a href="#method">Approach</a><a href="#explore">Explore 3D</a><a href="#components">Components</a><a href="#evidence">Evidence</a><a href="#resources">Resources</a></nav><span class="edition">Anonymous supplement</span></header>
<main id="main">
  <section class="hero hero-v2 wrap">
    <div class="hero-text">
      <p class="eyebrow">PERCEPTION → GENERATION</p>
      <h1>OPERA</h1>
      <h2>Object Perception Enhances Single-view 3D Reconstruction</h2>
      <p class="hero-copy">Perceptual alignment for <em>instance-faithful</em> single-image 3D generation, across multiview diffusion and native 3D flow matching.</p>
      <p class="intro">Lightweight alignment modules connect a frozen 3D generator to frozen perception models. At sampling time, the mismatch with what perception sees in the input image steers generation towards <em>that</em> object. No backbone is retrained.</p>
      <div class="hero-actions"><a class="button" href="#explore">Explore 3D <span aria-hidden="true">↓</span></a><span class="pending-link" title="Links will be added when the paper and code are public">Paper · forthcoming</span><span class="pending-link">Code · forthcoming</span></div>
    </div>
    <figure class="hero-teaser"><button class="zoom" data-zoom="{P}fig01_teaser.webp" data-description="Figure 1 · OPERA overview" aria-label="Enlarge Figure 1"><img src="{P}fig01_teaser.webp" alt="Figure 1 of the paper: perception models guide single-image 3D generation towards the object in the input image." width="2939" height="2963" fetchpriority="high"></button><figcaption>Figure 1 of the paper.</figcaption></figure>
  </section>

  <section class="section wrap" id="motivation" aria-labelledby="motivation-title">
    <p class="eyebrow">01 / MOTIVATION</p>
    <h2 id="motivation-title">Plausible is not the same as faithful.</h2>
    <div class="approach-copy"><p>A single photograph leaves most of an object unseen. Generative models fill the gap with convincing detail, but convincing detail can belong to <em>some</em> object of the category rather than to the one in the image. <strong>Instance fidelity</strong> asks for the particular object: its proportions, surface patterns and distinctive parts. The figure shows one example per paradigm, a multiview diffusion model and a native 3D flow-matching model.</p></div>
    {fig('fig02_motivation.webp', 2909, 725, 'Figure 2 of the paper: one Era3D example and one TRELLIS.2 example where a plausible result departs from the input object.', '<strong>Plausibility versus instance fidelity.</strong> One example for multiview diffusion (Era3D) and one for native 3D flow matching (TRELLIS.2). Figure 2 of the paper.', 'Figure 2 · Plausibility versus instance fidelity')}
  </section>

  <section class="section wrap" id="method" aria-labelledby="method-title">
    <div class="section-head"><div><p class="eyebrow">02 / OUR APPROACH</p><h2 id="method-title">Let perception guide generation.</h2></div><p>One alignment principle, instantiated for two generative paradigms.</p></div>
    {fig('fig05_unified.webp', 2915, 1205, 'Figure 5 of the paper: unified perceptual alignment and guidance. Intermediate generator features are mapped to perceptual representations; the discrepancy with the input-derived target guides the sampling state.', '<strong>Unified perceptual alignment and guidance.</strong> A generation–perception alignment module (GPAM) predicts a perceptual target from the generator’s intermediate features. The discrepancy with the target computed from the input image defines an energy whose gradient corrects the sampling state. Figure 5 of the paper; click to enlarge.', 'Figure 5 · Unified perceptual alignment and guidance', 'framework-figure')}
    <div class="method-cards"><article><span class="step">01</span><h3>Frozen backbone, frozen perception</h3><p>The generator and the perception models keep their weights. Their operations stay differentiable, so gradients can reach the sampling state.</p></article><article><span class="step">02</span><h3>Lightweight GPAM</h3><p>A small alignment module per perceptual target is the only thing trained, on about a thousand Objaverse objects, independently of the other modules.</p></article><article><span class="step">03</span><h3>Sampling-time guidance</h3><p>The target is computed once from the input image. At guided steps the state is corrected along the alignment gradient, and the sampler continues from the corrected state.</p></article></div>
    <div class="choice-row tabs" role="group" aria-label="Choose a paradigm" data-tabs="approach"><button class="choice active" data-tab="flow" aria-pressed="true">Native 3D flow matching <span>TRELLIS.2</span></button><button class="choice" data-tab="diffusion" aria-pressed="false">Multiview diffusion <span>Era3D</span></button></div>
    <div data-panel-of="approach" data-panel="flow">
      {fig('fig08_flow.webp', 2823, 1546, 'Figure 8 of the paper: OPERA on TRELLIS.2. Structure guidance acts on the sparse-structure flow and material guidance on the material flow; the shape flow is unchanged.', '<strong>OPERA on TRELLIS.2.</strong> TRELLIS.2 runs three flows in sequence: sparse structure, shape, material. OPERA guides the first with VGGT features and the third with DINOv3 features (optionally with an input-view colour term). The shape sampler is unchanged, so structure guidance reaches geometry only through the generated layout, and geometry is fixed while material is sampled. Figure 8 of the paper.', 'Figure 8 · OPERA on native 3D flow matching (TRELLIS.2)')}
      <details class="more"><summary>Guidance details (Figure 9)</summary>{fig('fig09_flow_detail.webp', 2922, 1540, 'Figure 9 of the paper: structure and material guidance in detail.', 'Structure and material alignment modules and how their gradients enter each flow. Figure 9 of the paper.', 'Figure 9 · Structure and material guidance')}</details>
    </div>
    <div data-panel-of="approach" data-panel="diffusion" hidden>
      {fig('fig06_diffusion.webp', 2835, 1537, 'Figure 6 of the paper: OPERA on Era3D. Guidance corrects the multiview latents before each DDIM step; surface reconstruction is not guided.', '<strong>OPERA on Era3D.</strong> Era3D generates colour and normal images for several views. At each guided step OPERA corrects the latents of all views once, the frozen U-Net is evaluated again, and the DDIM step follows. Depth and semantic gradients are normalised before mixing. The downstream surface reconstruction is unchanged and not guided. Figure 6 of the paper.', 'Figure 6 · OPERA on multiview diffusion (Era3D)')}
      <details class="more"><summary>Alignment module and guided step (Figure 7)</summary>{fig('fig07_diffusion_detail.webp', 2911, 1833, 'Figure 7 of the paper: the Era3D alignment module and the guided DDIM step.', 'Feature aggregation, perception mapping and the guided DDIM step. Figure 7 of the paper.', 'Figure 7 · Era3D alignment module and guided step')}</details>
    </div>
  </section>

  <section class="section gallery-section explore" id="explore" aria-labelledby="explore-title">
    <div class="wrap">
      <div class="section-head"><div><p class="eyebrow">03 / EXPLORE 3D</p><h2 id="explore-title">Turn the results around.</h2></div><p>Selected examples, chosen to show what guidance changes. They are not a representative sample; the evidence section reports the full cohorts.</p></div>
      <div class="choice-row tabs" role="group" aria-label="Choose a gallery" data-tabs="gallery"><button class="choice active" data-tab="flow" aria-pressed="true">Flow matching <span>TRELLIS.2</span></button><button class="choice" data-tab="diffusion" aria-pressed="false">Diffusion <span>Era3D</span></button></div>

      <div id="flow-gallery" data-panel-of="gallery" data-panel="flow">
        <div class="choice-row fg-filters" role="group" aria-label="Choose a collection"></div>
        <div class="model-picker fg-picker" role="group" aria-label="Choose an object"></div>
        <div class="fg-head"><h3 class="fg-name"></h3><p class="fg-credit"></p><span class="fg-links"><a class="text-button fg-source" target="_blank" rel="noopener noreferrer" hidden>Source ↗</a><a class="text-button fg-native" target="_blank" rel="noopener noreferrer" hidden>Full research gallery ↗</a></span></div>
        <div class="fg-compare">
          <figure class="viewer-input fg-input"><figcaption>Input image <span>the only image every method sees</span></figcaption><img alt="" loading="lazy"></figure>
          {viewer('a', 'Method shown in the first viewer')}
          {viewer('b', 'Method shown in the second viewer')}
          <div class="fg-linkonly viewer-output"><div class="viewer-cover"><span class="viewer-orbit" aria-hidden="true">↻</span><h3>Shown in the cross-domain gallery</h3><p>The original outputs for this object are not hosted on this page yet.</p><a class="button" target="_blank" rel="noopener noreferrer">Open in the cross-domain gallery ↗</a></div></div>
        </div>
        <div class="fg-more"><p class="fg-more-label">More comparisons</p><div class="choice-row fg-methods" role="group" aria-label="Show another method"></div></div>
        <p class="reference-note fg-status" aria-live="polite"></p>
        <p class="reference-note">Each viewer is an independent Sketchfab embed: cameras are not synchronised, and models keep the frame they were generated in. For matched-camera views and the surface-normal row, use the research gallery linked above. ReconViaGen and Hi3DGen are external methods run at their release settings; Hi3DGen outputs geometry only.</p>
        <noscript><p>The interactive gallery requires JavaScript. The models are listed in the <a href="https://sketchfab.com/idea0907/collections/3f8664bfe9414ad69461e8f6b0f23a47">Sketchfab collection</a>.</p></noscript>
      </div>

      <div data-panel-of="gallery" data-panel="diffusion" hidden>
        <div class="gallery-intro" id="gallery-3d"><h3>Era3D with OPERA guidance</h3><p>Choose an object to explore its reconstruction.</p></div>
        {picker}<noscript><p>The interactive selector requires JavaScript. The Thinker model is available through the Sketchfab link above.</p></noscript>
      </div>
    </div>
  </section>

  <section class="section wrap" id="components" aria-labelledby="components-title">
    <div class="section-head"><div><p class="eyebrow">04 / COMPONENTS</p><h2 id="components-title">What each signal contributes.</h2></div><p>Geometry and appearance are guided by different signals, alone or together.</p></div>
    <div class="choice-row tabs" role="group" aria-label="Choose a paradigm" data-tabs="components"><button class="choice active" data-tab="flow" aria-pressed="true">Flow matching <span>structure · material</span></button><button class="choice" data-tab="diffusion" aria-pressed="false">Diffusion <span>semantic · depth</span></button></div>
    <div data-panel-of="components" data-panel="flow">
      <div class="approach-copy"><p><strong>Structure</strong> guidance changes geometry: it acts on the sparse layout from which the shape is then generated. <strong>Material</strong> guidance changes appearance only, on fixed geometry. <strong>Combined</strong> uses the structure-guided geometry and then guides its material.</p><p>Material guidance needs a camera fitted to the generated shape. When the fitted silhouette overlaps the input by less than 0.8 IoU, guidance is switched off for that object and the output is the unguided fallback. Such objects stay in the reported cohorts and are labelled in the gallery; they are not counted as guided results.</p></div>
      {fig('fig12_flow_components.webp', 2861, 2400, 'Figure 12 of the paper: TRELLIS.2, structure, material and combined results with ground truth, and ReconViaGen and Hi3DGen for context.', '<strong>Components on TRELLIS.2.</strong> Baseline, structure, material and combined, with ground truth; ReconViaGen and Hi3DGen are shown for context. Selected objects. Figure 12 of the paper.', 'Figure 12 · Flow-matching components')}
    </div>
    <div data-panel-of="components" data-panel="diffusion" hidden>
      <div class="approach-copy"><p><strong>Depth</strong> guidance carries geometric structure; <strong>semantic</strong> guidance carries what the object is and how its surface looks. Each is trained separately and they are mixed at sampling time. On the two benchmarks they help differently: depth alone gives most of the geometric gain on GSO, while the semantic signal matters more on OmniObject3D.</p></div>
      {fig('fig10_diffusion_components_multiview.webp', 2830, 1336, 'Figure 10 of the paper: foreground error maps over six generated views for baseline, depth, semantic and combined guidance on one object.', '<strong>One object, six views.</strong> Error maps for the baseline, depth, semantic and combined guidance. The percentage printed in the figure is the view error of this single example, not a dataset result. Figure 10 of the paper.', 'Figure 10 · Diffusion components on one object')}
      <h3 class="sub">Same backbone, with and without guidance</h3>
      {showcase}<noscript><p>Enable JavaScript to switch examples; the book comparison is shown above.</p></noscript>
    </div>
  </section>

  <section class="results-region" id="evidence" aria-labelledby="evidence-title">
    <div class="wrap results-intro"><p class="eyebrow">05 / EVIDENCE</p><h2 id="evidence-title">What the benchmarks show.</h2><p>Means over fixed cohorts, copied from the paper. The comparison that matters is each backbone with and without OPERA. Arrows give the better direction. Not every object improves, and not every difference is statistically established; the notes under each table say which are.</p></div>
    <div class="wrap evidence-grid">
      <article><h3>Multiview diffusion · Era3D</h3><p class="ev-meta">GSO, 30 objects · OmniObject3D, 100 objects · one sampling seed · Chamfer distance in units of 10⁻³</p>
        {table(['GSO', 'CD ↓', 'F1@0.1 ↑', 'PSNR ↑', 'LPIPS ↓'], [['Era3D', '16.46', '0.801', '21.54', '0.0705'], ['+ Depth', '11.64', '0.833', '22.21', '0.0624'], ['+ Semantic', '15.51', '0.803', '21.70', '0.0690'], ['+ Combined', '11.45', '0.842', '22.42', '0.0613']], ours=(3,))}
        {table(['OmniObject3D', 'CD ↓', 'F1@0.1 ↑', 'PSNR ↑', 'LPIPS ↓'], [['Era3D', '35.78', '0.683', '20.44', '0.0842'], ['+ Depth', '33.49', '0.698', '20.71', '0.0804'], ['+ Semantic', '28.89', '0.693', '21.02', '0.0773'], ['+ Combined', '26.89', '0.705', '21.25', '0.0746']], ours=(3,))}
        <p class="ev-note">Mean Chamfer distance falls by 30.4% on GSO and 24.8% on OmniObject3D with combined guidance. Paired tests do not establish the GSO Chamfer improvement (p = 0.280); on OmniObject3D the adjusted evidence is for PSNR and LPIPS. Settings were selected on these sets, so the analysis is exploratory. The semantic target is Caption-T5 on GSO and DINOv3 on OmniObject3D. Table 1 of the paper.</p></article>
      <article><h3>Native 3D flow matching · TRELLIS.2</h3><p class="ev-meta">Toys4K, fixed cohort of 1,250 objects · one generation seed · geometry on the 1,083 objects that pass the ground-truth check</p>
        {table(['Toys4K geometry', 'CD-L2 ↓', 'F1@0.01 ↑', 'F1@0.02 ↑'], [['TRELLIS.2', '0.010546', '0.4161', '0.6503'], ['+ Structure', '0.009387', '0.4273', '0.6612']], ours=(1,))}
        {table(['Toys4K appearance', 'PSNR ↑', 'SSIM ↑', 'LPIPS ↓'], [['TRELLIS.2', '23.8986', '0.9436', '0.0728'], ['+ Structure', '24.0595', '0.9441', '0.0702'], ['+ Material', '24.1887', '0.9438', '0.0723'], ['+ Structure + Material', '24.3769', '0.9444', '0.0697']], ours=(3,))}
        <p class="ev-note">Structure guidance lowers CD-L2 by 11.0% (p = 0.1075, not established) and raises both F1 scores (p = 0.0001 and 0.0003). All appearance differences against the baseline have p ≤ 0.0132. The material result includes 99 camera-gated objects and 3 memory fallbacks that ran unguided. Tables 6 and 7 of the paper.</p></article>
      <article><h3>Across domains, without retraining</h3><p class="ev-meta">30 objects per dataset · TRELLIS.2 against OPERA (structure + material) · alignment modules trained on Objaverse only</p>
        {table(['Dataset', 'CD-L2 ↓ TRELLIS.2', 'CD-L2 ↓ OPERA', 'PSNR ↑ TRELLIS.2', 'PSNR ↑ OPERA'], [['MedShapeNet', '0.0448', '0.0389', '26.47', '27.24'], ['Medical Sketchfab', '0.0304', '0.0248', '19.23', '19.46'], ['Smithsonian', '0.0198', '0.0150', '24.72', '25.61'], ['AntScan', '0.0196', '0.0159', '26.19', '26.31']])}
        <p class="ev-note">CD-L2 falls by 13.2%, 18.6%, 24.4% and 19.0%. The paper prints no significance tests for this table, and SSIM drops slightly on AntScan. Untextured sources are rendered grey, which limits what appearance metrics can show. Table 10 of the paper.</p></article>
      <article><h3>External methods, for context</h3><p class="ev-meta">Toys4K, same input images and protocol · complete systems, not controlled ablations</p>
        {table(['Method', 'CD-L2 ↓', 'F1@0.01 ↑', 'PSNR ↑', 'LPIPS ↓'], [['TRELLIS', '0.014117', '0.3355', '21.376', '0.0850'], ['Hi3DGen (geometry only)', '0.014728', '0.2986', '–', '–'], ['ReconViaGen v0.5', '0.014378', '0.2861', '22.587', '0.0924'], ['TRELLIS.2', '0.010546', '0.4161', '23.899', '0.0728'], ['OPERA (Structure + Material)', '0.009387', '0.4273', '24.3769', '0.0697']], ours=(4,))}
        <p class="ev-note">Hi3DGen builds on the earlier TRELLIS backbone and outputs geometry only. OPERA’s gain is measured against its own backbone, TRELLIS.2; the other rows place it among complete systems. Table 8 of the paper.</p></article>
    </div>
    <div class="wrap"><h3 class="sub">Cross-domain examples</h3>
      {fig('fig13_cross_domain.webp', 2705, 2706, 'Figure 13 of the paper: TRELLIS.2 and OPERA results on medical, Smithsonian and AntScan objects.', '<strong>Selected cross-domain examples.</strong> Both methods smooth fine surface detail, and some OPERA meshes contain small holes. Figure 13 of the paper.', 'Figure 13 · Cross-domain examples')}
    </div>
  </section>

  <section class="section gallery-section" id="multiview" aria-labelledby="multiview-title">
    <div class="wrap"><div class="section-head"><div><p class="eyebrow">MORE QUALITATIVE RESULTS · DIFFUSION</p><h2 id="multiview-title">Across objects, datasets<br>and viewpoints.</h2></div><p>Selected colour and normal outputs with combined guidance, across two backbones and three datasets.</p></div>
    {multiview}</div>
  </section>

  <section class="section wrap" id="resources" aria-labelledby="resources-title">
    <p class="eyebrow">06 / RESOURCES</p><h2 id="resources-title">Resources and credits.</h2>
    <div class="resource-grid">
      <article><h3>Paper and code</h3><p>The paper and code are not public yet. Links and a citation entry will be added here once the final bibliographic details are available.</p></article>
      <article><h3>Interactive 3D</h3><ul><li><a href="https://sketchfab.com/idea0907/collections/3f8664bfe9414ad69461e8f6b0f23a47" target="_blank" rel="noopener noreferrer">OPERA · Native 3D Flow Matching</a> (Sketchfab collection)</li><li><a href="https://sketchfab.com/idea0907/collections/p4g-era3d-4f3f6464097c4e16a16811222eb00636" target="_blank" rel="noopener noreferrer">OPERA · Era3D</a> (Sketchfab collection)</li><li><a href="https://ood-results.vercel.app/" target="_blank" rel="noopener noreferrer">Cross-domain results gallery</a></li><li><a href="https://smithsonian-supervisor-gallery.vercel.app/3d/" target="_blank" rel="noopener noreferrer">Method comparison gallery</a>, with matched cameras and surface normals</li></ul></article>
      <article><h3>Data and models</h3><p>Benchmarks: Google Scanned Objects, OmniObject3D, Toys4K, MedShapeNet, AntScan, Smithsonian Open Access 3D and Sketchfab models under their own licences; each gallery object names its source. Backbones: Era3D and TRELLIS.2. Perception models: DINOv3 and VGGT for flow matching; a caption (T5) or DINO semantic target and a monocular depth model for diffusion. External methods: ReconViaGen and Hi3DGen, run from their official releases.</p></article>
    </div>
  </section>
</main>
<footer class="wrap"><a class="wordmark" href="#">OPERA<span class="mark">✳</span></a><p>Object Perception Enhances Single-view 3D Reconstruction</p><span>Anonymous supplementary website · Selected results</span></footer>
<dialog id="lightbox" aria-label="Enlarged research figure"><div class="lightbox-bar"><p id="lightbox-title"></p><button id="close-lightbox" autofocus aria-label="Close enlarged figure">Close ×</button></div><img id="lightbox-image" alt=""></dialog>
</body>
</html>
'''
open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8').write(html)
print('index.html', len(html))
