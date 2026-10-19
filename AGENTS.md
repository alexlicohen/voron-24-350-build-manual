# 3D Printing — Prusa Core One+ / Voron 2.4 350

## Goal (stated 2026-09-05)
Most efficient AND most effective print/build order for the Voron 2.4 350 once the Core One+ is running: one interleaved timeline of Prusa print batches and Voron assembly phases, dependency-ordered, so the printer is never idle and no assembly step waits on a part. Deliverables: docs/voron-print-plan.md (what to print, batch order), docs/voron-build-instructions-survey.md (which instructions to follow, Prusa-manual-style consolidation), and docs/manual/ — the actual consolidated build manual: Prusa-style numbered steps with fasteners, checks, and print batches interleaved as chapters (Alex: "not just an order, a detailed set of instructions"). Printing guidance is Prusa/PrusaSlicer-specific and quality-first: "speed is not the priority, quality is." Slicer: PrusaSlicer 2.9.6 for every batch (Alex, 2026-09-26). The 3.0 preview (yaml profiles, multi-bed projects, per-tool profiles; not feature-complete) is not used for this build; the slicer chapter keeps its 3.0 section as reference only. Delivery: MkDocs Material site from docs/ (`scripts/serve.sh` → LAN URL), read on an iPad at the bench; markdown is the single source, PDFs only as exported snapshots. Presentation (Alex 2026-09-06): one page per step like Prusa's help site (generated at build from the chapter markdown; chapter overview pages list steps with thumbnails), NOT long scrolling chapters. No bench photos: the manual is to build from, not a record — the photo ingest script is optional tooling only.


## Voron build manual
- Authoring (step field order, word budgets, Helper, fences, mascot, Parts grammar): read
  `docs/manual/CONVENTIONS.md` before writing or editing any chapter or step.
- Never split or renumber steps (ids are keys everywhere); appending a step is allowed.
- Check a transcribed step against the manual page image, the STL or the CAD — never against a
  reviewer's summary or a reviewer's replacement text.
- Check a chapter at the iPad viewport (1024×768) before calling it done; the bench reader is an iPad.
- Check: `make verify` (must exit 0). It runs the CI steps of `.github/workflows/check.yml` with the
  repo `.venv` (`mkdocs build --strict`, the tonight self-test and JS parity, callouts, `lint_manual.py`)
  plus `slicer/check_docs.py`. The build regenerates the tracked `docs/assets/tonight.json`.
- Guard rails: `scripts/lint_manual.py` (per-chapter gate `--strict-parts --chapters NN,…`),
  `slicer/check_docs.py` (fails on any stale bin count or plate id in prose), the plate board
  (build fails on drift), CI build + deploy, weekly drift job.

## Printing and slicing
- Print sheet follows the material: ASA smooth PEI + glue, PLA satin, PETG textured.
- Test one variable at a time (Alex): change one print setting per test print.
- The 2.9.6 CLI cannot arrange plates: `slicer/nest.py` proposes, the GUI Arrange is the QC authority.
  After any GUI re-save: `python3 slicer/build_plates.py --from-3mf <re-saved plate ids>`
  (no ids = all, slow but safe; never drop `--from-3mf`: bare, it re-packs every plate and loses
  the GUI arrangements), then `python3 slicer/check_docs.py` gates the numbers; the spool ledger
  in print/README shifts by hand.
- Delegated workers: the tree may hold Alex's GUI-saved 3MFs; every brief forbids reverting them.

## Memory
Durable context: `PROJECT_MEMORY.md` at the repo root (publication: local-only — untracked and
git-ignored, so it never ships with the manual). Operational facts, states, decisions and design
rationale only: printer configuration (`## Printer:`), what to print (`## To print:`) and manual
state (`## Manual:`), including status, plate counts and kit timing.

## Build facts (untracked)
Hardware, the Voron 2.4 plan decisions, materials, tools, open items, key numbers and order
history live in `context/build-facts.md` and `context/orders.md`. Both are git-ignored (`context/`)
because this repo is public; read them when a task needs those facts, and keep personal, order
and household details out of every tracked file.


## Source

Raw record: `context/chat-transcript.md` (51-turn claude.ai chat, exported 2026-09-05, covering 2026-09-03 through 2026-09-05).
