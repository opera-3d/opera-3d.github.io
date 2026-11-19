# Website + inference release: progress and review packet

Owner steering of 19 Nov 2026 (via Codex). Every statement describes what is on disk, on Sketchfab or on the remote at the time of the last update.

Last update: 2026-11-19, after the gallery rebuild. Live site: https://opera-3d.github.io

## Summary

| part | status |
|---|---|
| 1. Hero simplification | live (commit `d838f37`) |
| 2. Inference-only code release | pushed to a private branch; **prepared, not publicly released**. Details: `docs/CODE_RELEASE_STATUS.md` |
| 3. Ground truth on our Sketchfab account | 14 of 15 objects; 1 concrete blocker (file size) |
| 4. Student uploads | complete: 6 baseline replacements in place, 28 filled arms, no duplicates |
| 5. New cross-domain qualitative figure | live on the site (`d838f37`) and in the release README (`860af51`) |

## 1. Hero

- Title, subtitle and one abstract paragraph. The expandable full abstract is removed.
- The teaser is a plain image: no click target, no lightbox.
- Exactly three buttons: Explore 3D (anchor `#explore`), Paper (coming soon), Code (coming soon). The last two are not links.
- Checked on the local preview: at 1366×768 the teaser ends at 748 px, at 1440×900 at 880 px; no horizontal overflow at either size or on a 375 px phone.

## 2. Inference-only code release

- Repository `YNhuHuynh/OPERA-Flow` (still **private**), orphan branch `release/inference-v1`, head `860af51` (first commit `550a23f`). No research history, no training entrypoints, no job scripts, no private paths, no credentials, no checkpoints.
- `main`, the existing tags and the repository visibility were not touched; no GitHub Release was created.
- Validated on CPU only: byte-compilation of all files, `bash -n` of both scripts, the source-hash check (135/135), `prep-images` and `status` on two synthetic images, `--help` of three entrypoints.
- **Not validated:** no GPU run from the single-repository layout; `run_opera.sh check`; the two entrypoints that need the GPU environment; the token download fallback; the DINOv3 conversion; GPUs other than H100/H200.
- Pending owner decisions: making the code public, public checkpoint hosting, the code licence, the citation. The multiview-diffusion (Era3D) branch has no clean inference entrypoint and is marked pending in the README.
- The website Code button stays "coming soon".

## 3 and 4. Flow gallery coverage (15 objects)

Legend: **kept** = existing result unchanged; **student baseline (same UID)** = the student release's TRELLIS.2 stock mesh replaced our baseline file under the same Sketchfab UID; **filled (student)** = arm that was missing or held, now from the student release; **ours (licence)** = ground truth hosted on our account under that licence.

| object | TRELLIS.2 stock | + Structure | + Material | Combined | ReconViaGen | Hi3DGen | GT |
|---|---|---|---|---|---|---|---|
| `si02_mammuthus` | student baseline (same UID) | kept | kept | kept | kept | kept | ours (cc0) |
| `si01_triceratops_view2` | student baseline (same UID) | kept | filled (student) | filled (student) | kept | kept | ours (cc0) |
| `si25v2_a01_brachyceratops_montanensis_gilmo` | student baseline (same UID) | kept | filled (student) | filled (student) | kept | kept | ours (cc0) |
| `ant_124` | filled (student) | filled (student) | filled (student) | filled (student) | n/a | n/a | ours (by) |
| `ant_4008` | filled (student) | filled (student) | filled (student) | filled (student) | n/a | n/a | ours (by) |
| `ant_392` | filled (student) · regenerated | filled (student) · regenerated | filled (student) · regenerated | filled (student) · regenerated | n/a | n/a | ours (by) |
| `ov13_10_lymphatic_system` | kept | kept | kept | kept | kept | kept | ours (by-nc-sa) |
| `f7aa60639c60483f8e82fc182d2b0514` | filled (student) | filled (student) | filled (student) | filled (student) | n/a | n/a | ours (by) |
| `e903b83694d5455da1d71c2943dd7bab` | filled (student) | filled (student) | filled (student) | filled (student) | n/a | n/a | ours (by) |
| `si05_corallium` | student baseline (same UID) | kept | filled (student) | filled (student) | kept | kept | ours (cc0) |
| `si25_17_subhyracodon_gidleyi_wood_1927` | student baseline (same UID) | kept | kept | kept | kept | kept | ours (cc0) |
| `si25v2_c38_geochelone_carbonaria` | student baseline (same UID) | filled (student) | kept | filled (student) | kept | kept | ours (cc0) |
| `ov13_03_badge_of_the_black_prince` | kept | kept | kept | kept | kept | kept | ours (by-nc-sa) |
| `ov13_06_statue_of_liberty` | kept | kept | kept | kept | kept | kept | author embed (blocked: >100 MB) |
| `ov13_02_armillary_sphere_1771` | kept | kept | kept | kept | kept | kept | ours (by) |

Source of the student files: `Dyrekk/opera-cross-domain-120` at revision `743c809ab8ab753ae699baa7f6d06801c6964cfd`; every downloaded file is recorded with its sha256.

Provenance shown on the page:

- Student meshes labelled "paper-run mesh, decimated for the web" are reduced-detail copies (about 11–12 thousand faces for the Smithsonian objects, about 100 thousand for two ants, about 1 million for the medical objects).
- `ant_392` is labelled "regenerated at full resolution with the same recipe; not the paper-run mesh itself".
- The release does not record per-object gate or guided status, so filled arms carry the arm name only, not a guided / not-guided label.
- The student input images differ from our conditioning images by at most 1/255 per channel with an identical alpha mask: the same render, not byte-identical files.
- No paper metric or table was changed, and no GPU job was run.

Ground truth:

- 6 Smithsonian objects: CC0, as stated by the Open Access record of each object. The Voyager document of each scan carries a generic "(c) Smithsonian Institution" line; this is recorded in the manifests as a note.
- 3 AntScan objects, Armillary sphere, Occipital AVM, Tetralogy of Fallot: CC BY 4.0 with attribution.
- Badge of the Black Prince, Lymphatic system: CC BY-NC-SA 4.0 with attribution (the source licence; generated outputs for these objects carry the same licence).
- **Blocker, Statue of Liberty:** the ground-truth file is 111.3 MB and the account plan accepts 100 MB per upload. The original author's public model remains the ground truth for this object.

API verification of all 95 recorded models (94 ours, 1 author model): processing succeeded, published, downloadable, licence as intended. Collection `3f8664bfe9414ad69461e8f6b0f23a47` holds 94 models. View-only quota still 10 of 10. No duplicate titles among these uploads.

## Open items

- Statue of Liberty ground truth (size limit): needs a smaller export of the GT or a higher plan; neither was done without a decision.
- Public release of code and checkpoints, code licence, final title and authors, Paper link.
- The Smithsonian copyright line noted above, if the owner wants a second confirmation.

## Sketchfab UIDs

| object | entry | Sketchfab UID | licence | faces | downloadable | file sha256 (first 12) |
|---|---|---|---|---|---|---|
| `si02_mammuthus` | stock | `6eef11d56e13497f844687fa0f894532` | by | 11,895 | yes | d8b1a197717f |
| `si02_mammuthus` | structure | `a633c10f373846a49a591338c59b4be5` | by | 985,102 | yes | 02f5abf3ff7c |
| `si02_mammuthus` | material_only | `5ad4a8407b1349ef88e9dbc54d18203a` | by | 983,993 | yes | 86a9448eae91 |
| `si02_mammuthus` | opera_combined | `8c1eef5e371540dd84467eb706699de2` | by | 985,510 | yes | 9a90b7781128 |
| `si02_mammuthus` | reconviagen_v0.5 | `26c9e3ed0c0744ce84bfaf0da8d0ae14` | by | 464,543 | yes | 3df7200b8182 |
| `si02_mammuthus` | hi3dgen | `989a098ad126429f8f43ecd3cde28615` | by | 261,108 | yes | 6b210348e701 |
| `si02_mammuthus` | gt | `7892af1468b3412392483fafd87f6ad2` | cc0 | 150,000 | yes | ca8e1f97f402 |
| `si01_triceratops_view2` | stock | `d3fb26b300334f41a2a9b87ae43658bf` | by | 11,095 | yes | 4465952b5f1d |
| `si01_triceratops_view2` | structure | `8bd3a9b582c141849844f0ea6cbf41cf` | by | 967,602 | yes | 84ab49ee8c9b |
| `si01_triceratops_view2` | material_only | `340f0936c8eb4e66aabff78dfbbb4ad0` | by | 11,264 | yes | 32a9890deefe |
| `si01_triceratops_view2` | opera_combined | `49e903fabed24e5abbfb0210c5de0d19` | by | 11,683 | yes | 86ef824222f2 |
| `si01_triceratops_view2` | reconviagen_v0.5 | `376b9a0a7ee14db38a16fced120c3517` | by | 498,768 | yes | 04ed8a6cbfd0 |
| `si01_triceratops_view2` | hi3dgen | `2d61900f56ae4fff94d50c449e42de4a` | by | 209,804 | yes | 3291ca477a7c |
| `si01_triceratops_view2` | gt | `0f902df82b8d4f67959f4dee24dbe868` | cc0 | 150,000 | yes | 192dddbd09db |
| `si25v2_a01_brachyceratops_montanensis_gilmo` | stock | `c19f844cbaf641bf9357211eadcda877` | by | 11,581 | yes | 69b5e80c69af |
| `si25v2_a01_brachyceratops_montanensis_gilmo` | structure | `8228a6ce177d402b93e38cc9c4d3481c` | by | 974,738 | yes | 87c66d54f325 |
| `si25v2_a01_brachyceratops_montanensis_gilmo` | material_only | `bf11e99bc02a478aaa7a78cb03856d91` | by | 11,775 | yes | 8df4032e5fa7 |
| `si25v2_a01_brachyceratops_montanensis_gilmo` | opera_combined | `c17facb1b72b4247a8bcbd898b669d8a` | by | 11,699 | yes | 2bf273616630 |
| `si25v2_a01_brachyceratops_montanensis_gilmo` | reconviagen_v0.5 | `56529693e1d44958b75b5fe98e56b2f4` | by | 475,081 | yes | 5c1571ea827a |
| `si25v2_a01_brachyceratops_montanensis_gilmo` | hi3dgen | `2f5b1e17984341c0a90765bc1706230b` | by | 230,266 | yes | aa04512475f3 |
| `si25v2_a01_brachyceratops_montanensis_gilmo` | gt | `991e709c87cb4f73af18ac87459885c1` | cc0 | 150,000 | yes | f2ec24698095 |
| `ant_124` | stock | `3cad3ad2d1674ec587e429d0fc4be187` | by | 99,986 | yes | d9261ff520b4 |
| `ant_124` | structure | `e54d650adde648529298e5ae6eb7ab3c` | by | 99,973 | yes | 777c9a6f1517 |
| `ant_124` | material_only | `0bc74bae99044efe8cbfe1b2ccfd16c4` | by | 99,986 | yes | 55f5309cc368 |
| `ant_124` | opera_combined | `f85f381ec02b4c419b42c488e7333f97` | by | 99,975 | yes | 3a890b1aea86 |
| `ant_124` | gt | `5eba57c93642449f81448a0529c9e6f8` | by | 4,784,614 | yes | bab02d5a0d87 |
| `ant_4008` | stock | `203dfe6b05f547d1b603129185189b49` | by | 99,997 | yes | 9fe2973a979d |
| `ant_4008` | structure | `2918b68d45e04ce0897a0c9266d06c65` | by | 99,961 | yes | f239705df797 |
| `ant_4008` | material_only | `a8edd89246f045029186088dae897abf` | by | 99,996 | yes | 5d724ac477dd |
| `ant_4008` | opera_combined | `bb59032644ac4cd3a1477cdd45f796b4` | by | 99,960 | yes | 12e0e9787cbe |
| `ant_4008` | gt | `ad4372f0bdc940d4878cf6d9ae60e7ba` | by | 4,779,626 | yes | 66002a5a8f4b |
| `ant_392` | stock | `b832c297a84148029a4ab6a68ee29f59` | by | 937,994 | yes | 569ba2d6b8d2 |
| `ant_392` | structure | `9bd7c3ca01a8463fa82bce8751d80a7f` | by | 991,284 | yes | 02d20f0f1fe0 |
| `ant_392` | material_only | `b7fa020ad0f14f4bb5a81904301d650b` | by | 930,966 | yes | 0fd8ca5c9f59 |
| `ant_392` | opera_combined | `9fea523a664442a7a8f7ba1f617c11b6` | by | 990,878 | yes | 9382854af641 |
| `ant_392` | gt | `0630dfb32965494da89ffccd00e84a04` | by | 2,597,144 | yes | 9f72705bca17 |
| `ov13_10_lymphatic_system` | stock | `edfaa7b1adad4bd299c26a34ee8e62d2` | by-nc-sa | 959,039 | yes | 51a22ac4ef00 |
| `ov13_10_lymphatic_system` | structure | `26ca6624205b403ea9c885a476fcae7b` | by-nc-sa | 943,732 | yes | 6451a782f3d5 |
| `ov13_10_lymphatic_system` | material_only | `84a07e1232a1452bb826c5da38604b52` | by-nc-sa | 958,209 | yes | c9aa5e316b9d |
| `ov13_10_lymphatic_system` | opera_combined | `6268d8065a474a08a4f059923ec4c4da` | by-nc-sa | 944,100 | yes | 7a28a979da58 |
| `ov13_10_lymphatic_system` | reconviagen_v0.5 | `639ff92d26c64693abceb9cb53ae2b3f` | by-nc-sa | 495,438 | yes | 6d89c63a0453 |
| `ov13_10_lymphatic_system` | hi3dgen | `33330cafbf4c4b58ad37670db7f0c0ef` | by-nc-sa | 112,098 | yes | cc1dc1d92521 |
| `ov13_10_lymphatic_system` | gt | `a91d8df068cf4be2a8f34be64150a48e` | by-nc-sa | 994,272 | yes | ed3bce5df6c5 |
| `f7aa60639c60483f8e82fc182d2b0514` | stock | `9fa5f4d7261c48abb86d6601f8ec95f9` | by | 963,139 | yes | 60dc3f99b08b |
| `f7aa60639c60483f8e82fc182d2b0514` | structure | `7a41a8781b6d4e39ab4d5367a3100aac` | by | 997,973 | yes | ad8f54097e43 |
| `f7aa60639c60483f8e82fc182d2b0514` | material_only | `a9853c6e651a4d6d8831d87d71d4316b` | by | 961,575 | yes | 8af918de8bd5 |
| `f7aa60639c60483f8e82fc182d2b0514` | opera_combined | `edd9139dd7d1410e87f2603e2b7fd818` | by | 999,525 | yes | 3153be5a61cc |
| `f7aa60639c60483f8e82fc182d2b0514` | gt | `6b334ee5f248464cb2e42f1a81efd2ef` | by | 297,719 | yes | 5bbabdba63ea |
| `e903b83694d5455da1d71c2943dd7bab` | stock | `da18fc42121a443e95ee94a23522e3c9` | by | 957,436 | yes | a2d4c6e02b6c |
| `e903b83694d5455da1d71c2943dd7bab` | structure | `d3139e6068044809a4cae3b73b877499` | by | 929,430 | yes | e2e4bbd66972 |
| `e903b83694d5455da1d71c2943dd7bab` | material_only | `12fc9ddc7046430686eb3a4f16136cbf` | by | 957,541 | yes | 617bf5288067 |
| `e903b83694d5455da1d71c2943dd7bab` | opera_combined | `4d7c8a46b78c481e9db7bb887afcf557` | by | 928,536 | yes | 10ae6ca31f44 |
| `e903b83694d5455da1d71c2943dd7bab` | gt | `ad82ed6010ab46cea963f71a9ff4c644` | by | 1,109,942 | yes | 3afa8a7c5f4f |
| `si05_corallium` | stock | `fb7a3cdb44b34e7d8e4a2b836018efe4` | by | 11,940 | yes | 4a3ee9738d50 |
| `si05_corallium` | structure | `d1e491d67ac44187bc04d90b0cc12d16` | by | 981,614 | yes | 196feef8c934 |
| `si05_corallium` | material_only | `2ab96aa9c58f4bd1ab110a427a06d78c` | by | 11,939 | yes | 7af0067b94c9 |
| `si05_corallium` | opera_combined | `0ca2cdcde538400f8ffe8b32e52ed21a` | by | 11,955 | yes | da0622ba17cd |
| `si05_corallium` | reconviagen_v0.5 | `df48c20ceff24b1e8d722b409bb4b85d` | by | 496,396 | yes | ae6df9c58f9f |
| `si05_corallium` | hi3dgen | `79376c524fd8472db69c2601ebafbe74` | by | 408,734 | yes | 110f0ae920b4 |
| `si05_corallium` | gt | `5b4e6ccd75bc46618b18843324f8fae5` | cc0 | 150,000 | yes | adf886d086b7 |
| `si25_17_subhyracodon_gidleyi_wood_1927` | stock | `9f902b8e1c59401ba3b83a4d0030d363` | by | 12,000 | yes | 6b69883b6207 |
| `si25_17_subhyracodon_gidleyi_wood_1927` | structure | `7f7e52deb16444ce8ebcd3e5958c6173` | by | 984,021 | yes | 375d5d70b806 |
| `si25_17_subhyracodon_gidleyi_wood_1927` | material_only | `5b81d544d8fa4d53b626e5d22ec2e280` | by | 981,924 | yes | a3776ee9a43c |
| `si25_17_subhyracodon_gidleyi_wood_1927` | opera_combined | `b5c56ddcdb3446ae9045c499b9d1429c` | by | 984,201 | yes | 56a6b9d75990 |
| `si25_17_subhyracodon_gidleyi_wood_1927` | reconviagen_v0.5 | `63ab7ba539294816b2f15e7aafc730f7` | by | 467,586 | yes | 531282a93ef0 |
| `si25_17_subhyracodon_gidleyi_wood_1927` | hi3dgen | `e4e1fab9d0a94fb2ae02547ee758aee5` | by | 358,952 | yes | 418ba409377c |
| `si25_17_subhyracodon_gidleyi_wood_1927` | gt | `161f004e6db2444ba34c023efd9116a0` | cc0 | 150,000 | yes | 81de2dcb6b34 |
| `si25v2_c38_geochelone_carbonaria` | stock | `876ccd9aaa674a6cb7289380a8ad976f` | by | 11,589 | yes | 7ac0154df6ab |
| `si25v2_c38_geochelone_carbonaria` | structure | `31a620f6ca61448ebfeb4612f6a4ae6e` | by | 11,997 | yes | d28a2d58e492 |
| `si25v2_c38_geochelone_carbonaria` | material_only | `5c5d87ea18a04e1fa243efbc56cfd4a6` | by | 966,145 | yes | 2d7da5ee0547 |
| `si25v2_c38_geochelone_carbonaria` | opera_combined | `e149af048356408f943849760bfbcb9a` | by | 11,995 | yes | 91211b65e00c |
| `si25v2_c38_geochelone_carbonaria` | reconviagen_v0.5 | `f5017c52f5d141b6a606704c50fcea84` | by | 471,588 | yes | e512b62ab930 |
| `si25v2_c38_geochelone_carbonaria` | hi3dgen | `dc31957865df49f78f9d42568f89b569` | by | 540,986 | yes | ec8cdb4b1ff5 |
| `si25v2_c38_geochelone_carbonaria` | gt | `cdca62327db74d43b41279c287b03c66` | cc0 | 149,992 | yes | 45a5fa3c079f |
| `ov13_03_badge_of_the_black_prince` | stock | `a090d9816cf041b0aac4676571f8c18a` | by-nc-sa | 992,878 | yes | f9266f24554c |
| `ov13_03_badge_of_the_black_prince` | structure | `8d59efc86e7e4f2783b4c60119503d6a` | by-nc-sa | 989,450 | yes | 70517a7c9f5e |
| `ov13_03_badge_of_the_black_prince` | material_only | `16f4bad5d3ac4cd5b9129b4caf17a3db` | by-nc-sa | 994,582 | yes | 6aad137bfe22 |
| `ov13_03_badge_of_the_black_prince` | opera_combined | `9eff70d9235748fc87685dfda11770eb` | by-nc-sa | 990,516 | yes | f2df30eb9bea |
| `ov13_03_badge_of_the_black_prince` | reconviagen_v0.5 | `8294f62c76af44fdaed891a6fb0d8ab5` | by-nc-sa | 478,404 | yes | 234d11d7cabe |
| `ov13_03_badge_of_the_black_prince` | hi3dgen | `eb70a715a14c4e119fdd7e1711dc27be` | by-nc-sa | 389,216 | yes | 4f9d0113f841 |
| `ov13_03_badge_of_the_black_prince` | gt | `b1a01a1698c845fab50285f0341bcb09` | by-nc-sa | 224,488 | yes | 93ed5c60b755 |
| `ov13_06_statue_of_liberty` | stock | `6d7a87f871324763bef6d9ba6162ca23` | by | 940,570 | yes | 05415e9564c3 |
| `ov13_06_statue_of_liberty` | structure | `482f6c760e5e4fdb82fc5b6c56767f07` | by | 922,385 | yes | b8afbc51fb8c |
| `ov13_06_statue_of_liberty` | material_only | `4d2e467734f24d7db2179fd7fd1ed28f` | by | 931,233 | yes | 1b10d02f3351 |
| `ov13_06_statue_of_liberty` | opera_combined | `4b3c95b2752846dea87ff6557535470e` | by | 922,780 | yes | e24c97ef9c9c |
| `ov13_06_statue_of_liberty` | reconviagen_v0.5 | `84df86c607ac4b44aaa5b9bc9fb21df4` | by | 485,247 | yes | 674c6ad869ba |
| `ov13_06_statue_of_liberty` | hi3dgen | `6b0a8027049142608e906304fdc7282b` | by | 192,410 | yes | 019852e9cb4c |
| `ov13_06_statue_of_liberty` | gt | `6626abe1f3e8469a9d8f4b74d8aa2a71` | by | 3,999,999 | yes | 98655ab41e84 |
| `ov13_02_armillary_sphere_1771` | stock | `bae99d494cbe4997bee00cbdca288679` | by | 978,629 | yes | cd268db093b8 |
| `ov13_02_armillary_sphere_1771` | structure | `349d53904ce14693bf26536e05cb8527` | by | 996,190 | yes | 75bcbb3c2959 |
| `ov13_02_armillary_sphere_1771` | material_only | `f4dc3529af694002aeac5bae2257544d` | by | 977,703 | yes | d564a3d880a7 |
| `ov13_02_armillary_sphere_1771` | opera_combined | `e37609794e74419988243597bf4b809c` | by | 996,178 | yes | 267634e6fc83 |
| `ov13_02_armillary_sphere_1771` | reconviagen_v0.5 | `f8dfd3ae1c674a3fb9b590c611f93a3c` | by | 497,779 | yes | 1c58c0628ce5 |
| `ov13_02_armillary_sphere_1771` | hi3dgen | `ea401eb5ab0249be94fc9bb9e292a888` | by | 537,674 | yes | 9186451f2d28 |
| `ov13_02_armillary_sphere_1771` | gt | `4d9f55c35f2744a38284694c65f06be2` | by | 308,898 | yes | 4ff1030cedf8 |
