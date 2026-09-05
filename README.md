# Voron 2.4 R2 (LDO Rev D+, 350 mm) — build manual

A Prusa-style, single-track build manual for an LDO Voron 2.4 R2 Rev D+ 350 kit, with every printed part produced on a Prusa Core One+. Numbered steps, fasteners per step, "what you should see" checks, and print batches interleaved with assembly so the printer never idles and no chapter waits on a part.

- `docs/manual/00-index.md` — start here: the interleaved print/build timeline, critical path, corrections log.
- `docs/manual/00-…14-*.md` — assembly chapters (frame → calibration), transcribed from the official Voron 2.4r2 manual with LDO Rev D/D+ deviations inline.
- `docs/manual/print/` — PrusaSlicer setup (quality-first overrides) and eleven print-batch chapters with per-plate packing lists.
- `docs/voron-print-plan.md`, `docs/voron-build-instructions-survey.md` — the research the chapters are built from.

## Read it

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
./scripts/serve.sh        # prints the LAN URL; open it on a tablet at the bench
```

The rendered manual pages under `docs/manual/assets/manual-pages/` come from the official manual PDF, which is not committed (size). To regenerate:

```bash
curl -L -o docs/manual/assets/Voron2.4r2-manual.pdf \
  https://raw.githubusercontent.com/VoronDesign/Voron-2/de7e89d/Manual/Assembly_Manual_2.4r2.pdf
pdftoppm -png -r 110 docs/manual/assets/Voron2.4r2-manual.pdf docs/manual/assets/manual-pages/manual-p
```

The rendered Stealthburner manual pages under `docs/manual/assets/sb-pages/` come from the official Stealthburner manual PDF, also not committed (size). To regenerate:

```bash
curl -L -o docs/manual/assets/Voron-Stealthburner-manual.pdf \
  https://raw.githubusercontent.com/VoronDesign/Voron-Stealthburner/1bccf0543f40741243d81505c4ad5406eb822715/Manual/Assembly_Manual_SB.pdf
pdftoppm -png -r 110 docs/manual/assets/Voron-Stealthburner-manual.pdf docs/manual/assets/sb-pages/sb-p
# the SB manual has <100 pages, so pdftoppm 2-digit-pads by default — rename to the 3-digit sb-pNNN.png the chapters reference
cd docs/manual/assets/sb-pages && for f in sb-p-*.png; do n=$(echo "$f" | sed -E 's/sb-p-0*([0-9]+)\.png/\1/'); mv "$f" "$(printf sb-p%03d.png "$n")"; done && cd -
```

## Sources and drift

Every external URL cited in `docs/**/*.md` is inventoried in [`sources.yml`](sources.yml) — one row per source, with a title, a `kind`, and (for GitHub sources) the commit SHA of the default branch at the time it was last checked. Rebuild the inventory with `python3 scripts/sources_build.py`; re-check it with `python3 scripts/sources_verify.py --dry-run` (add no flag to also refresh `last_verified`/`sha` in place).

[`.github/workflows/drift.yml`](.github/workflows/drift.yml) runs weekly against the git repos this manual is most exposed to (`Voron-2`, `Voron-Documentation`, LDO's `Nitehawk-SB-V2` and `LDOVoron2`, `Voron-Stealthburner`, PrusaSlicer's settings repo) and opens or updates a single "Upstream drift" issue when any of them moves or a pinned URL stops resolving. It does not diff `docs.ldomotors.com` — that site is JS-rendered and would be all noise; LDO drift still surfaces through the corrections log and manual URL checks.

## Contributing

Found a step that doesn't match your kit? See [`CONTRIBUTING.md`](CONTRIBUTING.md) — corrections and questions both have issue templates, and PRs run through the same `mkdocs build --strict` + `scripts/lint_manual.py` checks as `main`.

## CI and deploy

`.github/workflows/check.yml` runs on every PR: `mkdocs build --strict` (with `validation.links.anchors: warn`, so a broken cross-reference anchor now fails the build, not just a missing file), the `hooks/callouts.py` self-test, and `scripts/lint_manual.py` (truncated callouts, dangling `Step NN.M` references, STLs printed in no batch, tables over 7 columns). `.github/workflows/deploy.yml` runs on push to `main`: same strict build, then `mkdocs gh-deploy --force` — chosen over `actions/deploy-pages` because `gh-pages` already exists as a classic branch-based Pages source and this keeps that config unchanged.

## Attribution and licences

- Voron 2.4r2 assembly manual pages (rendered PNGs) and Stealthburner/gantry-squaring images: © VoronDesign, [GPL-3.0](https://github.com/VoronDesign/Voron-2/blob/Voron2.4/LICENSE). Page images are reproduced under that licence; the pinned source commit is `de7e89d`.
- Voron Stealthburner assembly manual pages (rendered PNGs, `docs/manual/assets/sb-pages/`): © VoronDesign, [GPL-3.0](https://github.com/VoronDesign/Voron-Stealthburner/blob/main/LICENSE). Reproduced under that licence; the pinned source commit is `1bccf054`.
- LDO Motors guides and images are linked, not copied. Klipper documentation excerpts are GPL-3.0.
- Everything else in this repository (chapter text, print plan, survey) is provided as-is for personal builds; no warranty. Steps marked `(verify on bench)` are counts or details no source states — confirm on your own kit.
- No licence has been chosen for this repository's own content (chapter text, print plan, survey) yet — treat it as "all rights reserved" until one is added.
- `docs/manual/assets/` intentionally keeps the full rendered page range from each source PDF, including pages no chapter currently cites — that's deliberate (chapters are still being filled in against page references), not an oversight.

This manual is for one specific kit revision. If your kit differs (Rev C/D, different toolboard, different probe), the corrections log in the index tells you which steps to re-check.
