# Code release status (inference only)

Written 19 November 2026. Scope: part (2) of the owner's 19 November steering.

## Where it is

| Item | Value |
|---|---|
| Repository | `YNhuHuynh/OPERA-Flow` (still **private**; visibility not changed) |
| Branch | `release/inference-v1` (orphan: one commit, no research history) |
| Commit | `550a23f7df0238870849187002bb967084a7f34f` |
| Size | 153 tracked entries (150 files, 2 symbolic links, 1 submodule pointer) |
| Local build folder | a separate fresh clone on the owner machine; the research workspaces were not modified |
| Publication status | **Prepared, not public.** No GitHub Release was created, no checkpoint was published anew, `main` and the tags were not touched |

The website "Code" button stays "coming soon", as requested.

## What the branch contains

- `geometry/`: inference import closure from tag `combined-ds-v1-geometry` (base `a70b1ae`).
- `material/`: inference import closure from tag `combined-ds-v1` (base `f2a6781`), plus the checkpoint manifest, fetch and verify helpers, the DINOv3 converter and the example manifest.
- `run_opera.sh`: one entrypoint derived from the proven `handoff/combined/run_combined.sh` (same stage commands and frozen settings: structure λ 0.6, η 0.0025; DINOv3 head `6b76fa76` + RGB-4V head `515e3440`, 1:1, η 0.0025, input view only).
- `third_party/TRELLIS.2`: submodule pointer at `75fbf0183001ed9876c8dbb35de6b68552ee08bd`.
- `SOURCE_MANIFEST.sha256` + `tools/verify_source.py`: 133 of 135 code files are byte-identical to the research tags; 2 (`config.py` in each tree) had a cluster path string replaced.
- `MODIFICATIONS.md`, `THIRD_PARTY.md`, `env.example.sh`, `assets/` (4 preview strips, 2 paper figures).

## README order

1. Title and short purpose, with a release-status note.
2. Qualitative highlights: 4 preview strips (input, TRELLIS.2, OPERA Combined), each linked to `https://opera-3d.github.io/#flow/<object id>`.
3. News with actual dates: 2026-09-24 page first published; 2026-11-04 recipe, tags and checkpoints shared with collaborators only; 2026-11-17 flow gallery released; 2026-11-19 this branch prepared, not public. Public code, public checkpoints, paper and diffusion code are listed as pending without dates.
4. Method: paper Figures 5 and 8; supported backbones; the frozen recipe.
5. Installation, base models, checkpoints (real manifest with sha256; hosting stated as private release assets, public download pending).
6. Inference quickstart with the real stage commands.
7. Test data and examples.
8. Status and validation table.
9. Licences, credits, citation (pending).

## Validation actually done

| Check | Result |
|---|---|
| `python -m py_compile` on every Python file | pass |
| `bash -n` on `run_opera.sh` and `fetch_checkpoints.sh` | pass |
| `tools/verify_source.py` | 135 / 135 match the manifest |
| `run_opera.sh prep-images` and `status` on CPU, two synthetic RGBA images | 2 / 2 objects prepared |
| `--help` of `generate_gpam`, `merge_generation_dirs.py`, `verify_checkpoints.py` | pass |
| Private-string scan of the pushed tree (cluster paths, user names, credentials, private links) | no hit |
| Remote check (`gh api`): branch at the commit, 0 parents, 153 entries, no job scripts, docs, results or weights | pass |

## Not tested (stated in the README)

- No GPU run from this single-repository layout; `run_opera.sh check` was not run (needs the full environment).
- `--help` of `opera_flow.generate` and `pfs/run.py` could not run on this Mac (missing `yaml`, `trellis2`).
- Checkpoint download fallback without `gh`; the DINOv3 conversion reproduction; GPUs other than H100 / H200; photographs with unknown camera.

## Pending owner decisions

- Making the repository (or a new public repository) public.
- A public location for the four checkpoints (17 MB).
- The licence of our code (README says "to be announced").
- Citation: title and authors are not final, so no BibTeX entry is given.
- The diffusion (Era3D) branch: the code in `Projects/RQ2` is a research tree with no clean inference entrypoint; it is marked pending.

## Left out on purpose

- Training entrypoints, job scripts, training configurations and data; evaluation and Blender code; benchmark object lists; logs, results, internal documents; `CLAUDE.md`.
- The checkpoints themselves (two of them are in git at the research tag; they were not copied).
- Caveat: `gpam/train.py` and a few data-preparation modules are in the tree because the inference code imports functions from them. Nothing in the branch launches training. Removing them would mean editing the proven code.
- The preview strips use the website's current stills; if the site's baseline stills are replaced by the student versions, the strips should be rebuilt.
