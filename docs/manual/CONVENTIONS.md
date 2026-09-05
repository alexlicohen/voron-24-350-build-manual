# Manual conventions (all chapter writers follow this exactly)

Purpose: a Prusa-style, single-track build manual for Alex's LDO Voron 2.4 R2 Rev D+ 350 (blue), all parts self-printed on a Prusa Core One+. Spine and per-phase sources: `docs/voron-build-instructions-survey.md` (§3 spine, §4 deviations, §7.2 per-chapter writing spec). Print batches: `docs/voron-print-plan.md`.

## Files
- One chapter per file: `docs/manual/NN-slug.md` (e.g. `01-frame.md`, `02-z-drives.md`). `00-index.md` is written last by the orchestrator.
- Rendered official-manual pages live at `docs/manual/assets/manual-pages/manual-p{NNN}.png` (NNN = PDF page index, zero-padded 3). Reference them by that path; don't re-render.
- LDO/other images: link by URL (don't download) unless the survey §7.4 says the license allows embedding.

## Chapter header (in this order)
1. `# Chapter NN — Title`
2. One-line scope: what this chapter builds and what it unlocks.
3. **Time:** hands-on estimate (first build), with source.
4. **Prerequisites:** chapters and print batches that must be done (name batches by their `batch_id` from the print plan; if the print plan isn't available yet, list the STL filenames and write `batch: TBD`). Canonical form: batches are `B00`–`B10` (always two digits); plates are `B00-P1` (two-digit batch, plate number as printed — no padding on the plate digit).
5. **Tools** (bullets), **Printed parts** (table: STL, qty, color), **Hardware** (table: fastener/part, qty) — chapter totals, pulled from the official manual pages and the LDO batch BOM notes.
6. **Read first:** 2–5 bullets of the pitfalls for this chapter (from survey §4).
7. Colour cells use exactly `Black` or `Orange` (add `(opaque)` where the STL is `[o]_`); the filament identity lives once, in print plan §1.2.

## Steps
- `### Step NN.M — short imperative title`
- Image line first: `![Voron manual p.XX](assets/manual-pages/manual-pXXX.png)` or an LDO image URL, or `(no image — see text)`.
- **Parts:** exact fasteners/parts for THIS step, qty.
- **Do:** 1–5 imperative sentences. Say which way round, which hole, how tight ("snug, not torqued", "torque after squaring").
- **Check:** what you should see/measure before moving on.
- `⚠ Rev D+ / LDO:` callout whenever the kit deviates from the official manual (from survey §4.1–4.2 and LDO Build Notes) — always inline at the step, never only in a preamble.
- `Tip:` optional, one line, community-sourced, cite URL.
- Steps are atomic: one sub-assembly action each. Prusa's manual averages ~1 photo and ~3 fasteners per step; match that granularity.
- Mode A chapters (frame, Z, plate, A/B, gantry, belts): transcribe the manual's page sequence step by step; one manual page may become 1–4 steps.
- Mode B chapters (prep, toolhead, electronics, wiring, panels, software, startup, calibration): write from LDO guides + survey; cite the source URL per step.

## Chapter end
- `## Checkpoint NN` — a checklist (5–12 items) the builder ticks before continuing (squareness, free motion, no binding, torque done, photos taken).
- `## Common mistakes` — 3–6 bullets with the fix.
- `## Next` — one line.

## Style
- Second person, present tense, terse. No preamble, no history. Units: mm, N·m. Fastener names as the manual writes them (M3×8 BHCS, M5×16 SHCS, roll-in T-nut).
- Never invent a count or a torque. If the source doesn't give it, write `(verify on bench)` or `(not specified — snug)`.
- Cite: `[src](url)` at the end of a step or a callout; manual pages by `p.XX`.
- No emoji except the `⚠` callout marker.

## Lint
`scripts/lint_manual.py` runs in CI, after `mkdocs build --strict`. Four checks: raw `⚠` / `**Check:**` / `Tip:` text outside an admonition or `<code>`/`<pre>` block; `Step NN.M` references with no matching heading; STL filenames in an assembly-chapter table with no matching print-batch table row (exempt: a row containing `not printed`, `kit-supplied`, or `SKIP`, case-insensitive); Markdown tables wider than 7 columns (exempt: tables under a heading whose text contains "Machine-readable").

## Print-batch chapters (added 2026-09-05)
- Live in `docs/manual/print/`: `00-slicer-setup.md` then `B00-calibration-and-jigs.md` … `B10-clicky-clack-door.md` (batch ids from `docs/voron-print-plan.md`). Assembly chapters stay in `docs/manual/NN-*.md`; `00-index.md` holds the interleaved timeline that says which batch to start before which assembly chapter.
- A batch chapter's steps are: prepare filament (dry state, spool) → load the plate file/list in PrusaSlicer with the named profile and overrides → pre-print checks (sheet, chamber preheat) → print → inspect (calipers on the named critical dimensions, bearing-seat test) → label and bin the parts by the assembly chapter that consumes them. Same Step/Parts/Do/Check format.
- Never restate the whole override table per batch; link `00-slicer-setup.md` and list only batch-specific deviations (brim, orientation, accent color).
