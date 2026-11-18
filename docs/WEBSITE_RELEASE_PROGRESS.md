# Website + inference release: progress and review packet

Owner steering of 19 Nov 2026 (via Codex). This file is updated as work lands, so it can be read instead of asking for status.
Every statement below describes what is on disk or on the remote at the time of the last update, not what is planned.

Last update: 2026-11-19 (in progress)

## 1. Hero simplification

| item | status |
|---|---|
| Title + one abstract paragraph only (expandable full abstract removed) | done locally, not yet pushed |
| Teaser as a plain image (no click, no lightbox) | done locally |
| Exactly three buttons: Explore 3D (anchor `#explore`), Paper (coming soon), Code (coming soon); the last two are not links | done locally |
| Laptop check 1366×768: teaser bottom at 748 px of 768, no horizontal overflow | checked on the local preview |
| 1440×900 and mobile check | pending |

## 2. Inference-only code release

In progress in a separate clean clone; see `docs/CODE_RELEASE_STATUS.md` once written. The website Code button stays "coming soon" as requested.

## 3. Ground truth hosted on our Sketchfab account

Rule applied: our local/RDS GT file (student `gt.glb` where we had none) is uploaded to our account under its source licence with attribution and replaces original-author embeds and still-only fallbacks.

| object | licence used | status |
|---|---|---|
| 6 Smithsonian objects | CC0 (Open Access record) | upload in progress |
| ant_392 | CC BY 4.0 | uploaded |
| ant_124, ant_4008 | CC BY 4.0 | retry in progress (first attempt dropped by the network) |
| Armillary sphere | CC BY 4.0 | upload in progress |
| Badge of the Black Prince, Lymphatic system | CC BY-NC-SA 4.0 | upload in progress |
| Occipital AVM, Tetralogy of Fallot | CC BY 4.0 | queued (student `gt.glb`, sha256 verified against `source.json`) |
| Statue of Liberty | CC BY 4.0 | **blocked**: the GT file is 111.3 MB, above the 100 MB upload limit of the account plan; the original author's model stays |

## 4. Student uploads

First pass finished for Mammuthus, Subhyracodon and ant_392. Network resets interrupted Triceratops, Brachyceratops, Corallium, Geochelone, ant_124 and ant_4008; these are being retried. Retries cannot duplicate: an uploaded model is adopted by its exact title.

## Still to do

Verification of every model through the API, gallery rebuild, desktop and mobile screenshots, push, live check, final coverage table.
