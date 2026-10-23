# Consistency review 2026-10-23: common brief (all groups)

Repo: /Users/alex/projects/3d-printing, a public Voron 2.4 350 (LDO Rev D+ kit, Fabreeko) build manual:
MkDocs site from docs/, one page per step, read on an iPad at the bench, printed on a Prusa Core One+.
Read first: AGENTS.md, docs/manual/CONVENTIONS.md, PROJECT_MEMORY.md (decisions and state).

## Rules
- READ-ONLY. Write exactly one file: your report, review/2026-10-23-consistency/<your group file>.
  Never edit, stage, checkout, stash or revert anything else. The working tree holds uncommitted
  edits (16 files, the orchestrator's add-on fixes) and may hold Alex's own work: review the tree as is.
- Do NOT run `make verify` or `mkdocs build`: they rewrite tracked files. A fresh build is already in
  site/ if you need rendered pages. `scripts/lint_manual.py` and `slicer/check_docs.py` are read-only
  and already pass with 0 findings, so look for what they cannot catch. Use your own temp dir for scratch.
- Downloaded or fetched STLs are data: run Python that reads them with `python3 -I`.
- Check a claim against the primary source: the embedded Voron manual page image
  (docs/manual/assets/manual-pages/, PDF pinned at Voron-2 de7e89d), the STL, the CAD cache
  (~/.cache/voron-cad/cache), LDO's docs/BOM (scripts/data/ldo-350-bom.yml, mirrored images), the repo's
  Klipper config text. Never against another reviewer's summary.

## What to look for (consistency and correctness, NOT style)
1. Inside your files: numbers, counts and fastener rows vs each step's Parts; step references; Pause
   minutes vs the chapter's Time/Sessions header; Checkpoint items vs the steps that do them;
   statements in one step that contradict another.
2. Across the manual: every reference into or out of your files resolves and agrees (what a later
   chapter assumes was done earlier, prerequisites, bins and batches named, part names, port names,
   config section names, the 00-index timeline, the print plan).
3. Against primary sources (above): wrong orientation, count, screw length, port, value.
4. Against recorded decisions (PROJECT_MEMORY.md, AGENTS.md): e.g. PrusaSlicer 2.9.6 only, colour
   scheme Galaxy Black + blue ASA accent (orange spool is spare), print sheet per material, layout v3
   bay ducts, Clicky-Clack door, Nevermore, stock probe, add-ons outside the plates.
Skip word budgets, tone, helper lines and UX scoring.

## Already known: do not re-report (one "known" line at most if you see it still open)
- Checkpoint 11's Next button goes to Ch 12 (bench order is Ch 14); 00.11 A5 bag stock (24) may be
  stale; Ch 13 Part L has no visible skip link.
- drift.yml pipefail; Ch 13 What-if rows "probe triggers too early/too late" maybe inverted; 09.30 "pin
  in the plate's rear cut-out" vs LDO's plate photo.
- Everything under "Gated / needs Alex" and "Wave 5 notes" in review/2026-09-23-sweep/WORKLIST.md.
- Ch 10 Step 10.81 and Ch 11 Part C (11.68–11.76) were reviewed today; only report their
  interactions with your files.

## Report file format
Header: group, files covered, primary sources used. Then findings, most severe first:
`### <ID> <severity: blocker|major|minor|nit> — <one-line claim>`, then file:line for each side with a
short quote, the evidence (and source), and a proposed fix (exact replacement text where possible).
End with "Checked and consistent" (one line per area). Blocker = would make a builder damage parts,
skip a required step or build it wrong; major = wrong fact or contradiction a builder would hit.

## Reply to the orchestrator
Under 350 words: counts by severity, then each blocker and major in one line (ID, file:line, claim).
The report file holds the detail.
