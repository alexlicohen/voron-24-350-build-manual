# Verify-then-fix brief, 2026-10-23 (all fix agents)

Alex: "confirm that these errors are actually errors against the source material where possible", then fix.
Findings are in review/2026-10-23-consistency/G1..G8 reports (detail, quotes, proposed text) and SUMMARY.md.

## Order of work, per finding
1. Re-read both sides in the CURRENT tree (line numbers may have moved).
2. Check against the PRIMARY source, never the reviewer's summary or its replacement text: the Voron
   manual page image (docs/manual/assets/manual-pages/, sb-pages/; PDFs pinned at Voron-2 de7e89d,
   Stealthburner 1bccf05), the STL (slicer/stl/..., read with `python3 -I` numpy; `venv-cq/bin/python`
   has numpy), the CAD cache (~/.cache/voron-cad/cache), LDO docs/BOM (scripts/data/ldo-350-bom.yml,
   mirrored images under docs/manual/assets/remote/), Klipper source/docs, PrusaSlicer 2.9.6 behaviour,
   the repo's own rule text (00a for mains rules, AGENTS.md, CONVENTIONS.md). Web pages may be fetched
   for vendor docs (docs.ldomotors.com, docs.vorondesign.com, klipper3d.org).
3. Verdict: CONFIRMED / REFUTED / PARTLY (say which part) / UNVERIFIABLE (no source settles it).
4. Fix only CONFIRMED (or the confirmed part). REFUTED and UNVERIFIABLE: no edit; say why.
   A fact no source settles but the build needs gets `(verify on bench)`, per CONVENTIONS.md.

## Rules
- Edit ONLY your assigned files. Other agents edit other files at the same time. If a fix needs a
  file outside your list, do not edit it: put the exact proposed change in your log.
- Never renumber or split steps. Follow docs/manual/CONVENTIONS.md: field order, word budgets (Do ≤40,
  Check ≤25, What-you're-looking-at ≤45, ⚠ ≤60, Tip ≤30, Helper ≤20), no em-dash or parenthetical
  inside those fields, Parts grammar. New or changed mains/iron/blade/hot steps carry no Helper line.
- Never checkout, stash, revert or stage anything; never commit; the tree may hold Alex's work.
- Do NOT run `make verify` or `mkdocs build` (they rewrite tracked files and would collide with the
  other agents). Gate your own chapters with the read-only
  `.venv/bin/python scripts/lint_manual.py --strict-parts --chapters NN,...` and, for print/slicer
  numbers, `.venv/bin/python slicer/check_docs.py`. The orchestrator runs `make verify` at the end.
- Do NOT touch the five items held for Alex: kit ETA (G1-01/G8-03); Ch 13 checks that look into the
  closed bay while live (G6-01/G5-5: 13.1–13.3 bay/LED checks, 13.8 SSR LED, What-if rows, Checkpoint
  13 line); Leviathan SW1/SW2 flashing (G5-2); B02-P3 3MF (G8-06); preset "(modified)" (G8-04).
- Scope: the findings assigned to you. No drive-by edits.

## Log (required)
Write review/2026-10-23-consistency/VERIFY-<your letter>.md: one block per finding with verdict, the
source evidence (file/page/STL measurement/URL), and the change made (file:line) or why none.
Reply to the orchestrator in under 300 words: verdict counts, files changed, lint result, anything you
need another agent or Alex to do.
