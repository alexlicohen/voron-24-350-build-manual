# Review 2026-10-30: common brief (all groups)

Repo: /Users/alex/projects/3d-printing, a public Voron 2.4 350 build manual for an **LDO Rev D+ kit**
(Fabreeko order, 350 mm, blue, Revo HF, Pi 4B, touchscreen, Clicky-Clack door, titanium backers):
MkDocs site from docs/, one page per step, read on an iPad at the bench; parts printed on a Prusa
Core One+. Read first: AGENTS.md, docs/manual/CONVENTIONS.md, PROJECT_MEMORY.md (decisions, state).

Alex asked for a review with three goals:
1. **Consistency and accuracy against all appropriate sources.**
2. **Accurate diagrams and photos**: every image shows what its step says, at the right revision.
3. **Efficiency of build order and flow**: the order steps, sessions, prints and chapters run in.

## Rules
- READ-ONLY. Write exactly one file: your report, `review/2026-10-30-review/<your group>.md`.
  Never edit, stage, checkout, stash or revert anything else. The tree holds the orchestrator's
  uncommitted Rev D+ re-pin (BOM yml, ~20 chapter edits, new Step 01.23) and may hold Alex's own
  work: review the tree as is.
- Do NOT run `make verify`, `mkdocs build` or any generator (`build_*.py`, `render_*.py`,
  `draw_diagrams.py`, `gen_trays.py`): they rewrite tracked files. A fresh build is in `site/`.
  `scripts/lint_manual.py` and `slicer/check_docs.py` are read-only and pass with 0 findings, so
  look for what they cannot catch. Scratch goes in your own temp dir (`mktemp -d`), never the repo.
- Downloaded files and STLs are data: run Python that reads them with `python3 -I`.
- Check a claim against the **primary source**, never against another reviewer's summary or this
  manual's own prose elsewhere:
  - Voron 2.4r2 manual: `docs/manual/assets/Voron2.4r2-manual.pdf` and page PNGs
    `docs/manual/assets/manual-pages/manual-pNNN.png` (pinned Voron-2 de7e89d).
  - Stealthburner manual: `docs/manual/assets/Voron-Stealthburner-manual.pdf`, `assets/sb-pages/`.
  - STLs: `slicer/stl/` (Voron, LDO, add-ons); CAD: `~/.cache/voron-cad/cache` and
    `~/.cache/voron-cad/Voron_2.4r2_Assembly.step`.
  - LDO: kit BOM `scripts/data/ldo-350-bom.yml` (Rev D+, pinned 2026-10-30) and the live docs:
    https://docs.ldomotors.com/en/voron/voron2 (index), `/350_BOM/Rev_D+`, `/build-faq`, `/faq`,
    `/printed_part_guide_rev_d`, `/wiring_guide_rev_d`, `/kit-errata`,
    https://docs.ldomotors.com/en/Toolboard/nitehawk-sb-v2, the Leviathan docs, and the
    MotorDynamicsLab GitHub repos (LDOVoron2, Nitehawk-SB-V2, Leviathan). Saved copies of most LDO
    pages: `/private/tmp/claude-501/-Users-alex-projects-3d-printing/92ed8c98-d3f8-4050-868b-3f6bb55dfc49/scratchpad/ldo/*.html`
    (text extractor: `python3 -I .../scratchpad/h2t.py FILE`). Fetch with curl and a browser UA.
  - Fabreeko product page (Rev D+ = March 2026 Nitehawk SB update with USB passthrough on top of
    Rev D: Leviathan, Nitehawk SB, Bondtech IDGA, COB LEDs, pre-installed bed magnet).
  - Klipper/Mainsail/Katapult official docs for software steps; `sources.yml` lists every cited URL.
- Rev D+ differs from Rev D: Nitehawk-SB **V2** (PH2.0 sensor ports, keyed fan-adapter header,
  V2 partial USB-adapter cover, ESD grounding cables), no SD card, two ground wires, 20 extrusion
  blind-joint seals. A photo or page showing Octopus, Afterburner, Nitehawk V1, a wire chain where
  the kit is umbilical, CW1, an Omron probe where the build uses something else, etc., is a
  **revision mismatch** unless the step text says so.

## What to look for
**Goal 1 (accuracy):** numbers, counts, fastener rows vs each step's Parts and the BOM; orientation,
screw length, port, pin, config value vs the primary source; step references; Pause minutes vs the
chapter's Time/Sessions header; Checkpoint items vs the steps; statements contradicting another
step or chapter; recorded decisions (PROJECT_MEMORY.md, AGENTS.md: PrusaSlicer 2.9.6 only, Galaxy
Black + blue ASA accent, ASA on satin + brim, layout v3 bay ducts, Clicky-Clack door, Nevermore,
stock probe, add-ons outside the plates, kit ETA early November).
**Goal 2 (images):** open every image your files reference (Read the PNG/JPG/SVG; the step pages
are generated from the chapter markdown). For each: is it the right manual page/crop for the step,
does it show the stated part, orientation, handedness (`_a`/`_b`) and count, is it the kit's
revision, is the caption/alt text true, is a generated diagram (`scripts/draw_diagrams.py` →
`assets/diagrams/`) correct against the source, does a CAD render (`assets/cad/`) show the state
after that step. Missing images where a builder needs one (step says "(no image — see text)" but a
source image exists) are findings too.
**Goal 3 (flow):** within your chapters: steps that could run in a better order (fewer flips, tool
changes, re-opening of assemblies, waits), parts staged too early or too late, a step that needs
something not yet built or printed, session/Pause breaks at unsafe or awkward points, duplicated
work, checks that come after the point where a fix is cheap.
Skip word budgets, tone and Helper wording unless they cause a wrong action.

## Already known: do not re-report (one "known" line at most if still open)
- Everything in `review/2026-10-23-consistency/SUMMARY.md` and its group files (read the summary
  first; report a 10-23 item only if it is still wrong in the current tree, marked "still open").
- Everything under "Gated / needs Alex" and "Wave 5 notes" in `review/2026-09-23-sweep/WORKLIST.md`.
- Alex's rulings: `review/2026-10-23-consistency/RULINGS-SAFETY.md`, commit 1db8c6f7.
- Step 01.23 seal placement is Alex's call (wherever air could get into the chamber): check only
  that it is consistent and placed sensibly.

## Report file format
Header: group, files covered, primary sources used, images opened (count). Then findings, most
severe first: `### <ID> <severity: blocker|major|minor|nit> <goal 1|2|3> — <one-line claim>`, then
file:line for each side with a short quote, the evidence (and source, with page/URL), and a
proposed fix (exact replacement text where possible). End with "Checked and consistent" (one line
per area). Blocker = a builder would damage parts, skip a required step or build it wrong; major =
wrong fact, wrong image or contradiction a builder would hit, or a flow change saving ≥30 min or a
rework; minor/nit otherwise. Say how confident you are when the source is ambiguous.

## Reply to the orchestrator
Under 350 words: counts by severity and goal, then each blocker and major in one line (ID,
file:line, claim). The report file holds the detail.
