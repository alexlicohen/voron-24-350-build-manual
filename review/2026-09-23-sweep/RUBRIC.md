# Manual sweep rubric, 2026-09-23. Gold standard: Prusa CORE One+ kit assembly manual (1.02)

The reference PDF is `prusa-core-one-plus-kit-assembly-1.02.pdf` in the session scratch folder (Prusa's copyright; not committed). It is 228 pages; its text extract is `prusa.txt` next to it. Pages worth viewing as images:
- p.9–20: Introduction chapter;
- p.21–22: a chapter's "Tools necessary" step;
- p.115–116: typical action steps and a "parts preparation" step;
- p.128 and p.215: "Haribo time" / "Done".

Alex builds with their 13-year-old daughter, reading on an iPad (1024×768) at the bench. The Core One+ manual is the one they built from together, and it is the bar.

## What the Prusa manual does (score each chapter against these)

**U: Usability**
- U1 **Chapter opener:** "Tools necessary for this chapter" as step 1, before any action.
- U2 **Parts preparation before each assembly step:** every part named, with its count and where it comes from (bag or package), e.g. "M3x10 screw (5x)". Nothing appears in an action step that wasn't prepared.
- U3 **One idea per step:** a 2–6 word title naming the action ("Mounting the PSU"), 1–4 short imperative lines, one action per line.
- U4 **Picture first:** every action step has an image showing exactly that action, with colour highlights on the parts involved. Text and image agree.
- U5 **Explicit checks:** "Checking …" steps at the points where a mistake would be buried later (belt routing, orientation).
- U6 **Orientation language** a first-timer can follow: which side, which way up, "the longer end".
- U7 **Wayfinding:** step N of M, chapter list, next/previous, a clear "Done" at the end of each chapter.
- U8 **Recoverability:** where to get help, what to do if a part is missing (the spare bag), how to undo a step.

**A: Accuracy**
- A1 Instructions match the picture, the part and the source (Voron manual page image, LDO docs/photos, STL/CAD). Never judge against a reviewer's summary.
- A2 Fastener names and counts match the chapter's parts table and the kit BOM.
- A3 Numbers (lengths, torques, temperatures, gaps, times, grams) agree with their sources and across pages.
- A4 Cross-references resolve and point at the right step.
- A5 Unverified claims are marked `(verify on bench)`, and no bench-verify item is stated as fact elsewhere.
- A6 Safety content (mains, heat, blades) is correct, complete, and placed before the hazard.

**E: Engagement** (for a 13-year-old co-builder and an adult)
- E1 **Rewards and rhythm:** Prusa's Haribo per chapter ("Victory tastes like gummy bears!"). Is there a comparable earned moment, and are chapters split into satisfying sessions?
- E2 **Tone:** friendly second person, confident, a little playful; never condescending, never a wall of caveats.
- E3 **The helper has real jobs,** not token ones (`**Helper:**` lines).
- E4 **Mascot (Revali):** captions land; used where they add delight; absent where the rules say (mains, iron, blade, hot).
- E5 **Visible progress:** progress bars, checkpoints, "look what you built" moments (the end-of-chapter CAD renders).

## Where this manual deliberately differs (don't flag these as defects)
- Source layering: the Voron manual + LDO overlays. The `⚠ Rev D+ / LDO` callouts exist for this.
- The action-first step order: Do → Parts → Check → collapsed "What you're looking at" → ⚠/Tip → Pause → Source. Lint word budgets: Do ≤ 40 words, Check ≤ 25, description ≤ 45, Tip ≤ 30, ⚠ ≤ 60.
- No bench photos; renders and diagrams instead.
- Step ids are keys: **never recommend splitting or renumbering steps**. Recommend appending, or restructuring inside a step.
- Printing is interleaved (the Print tab); Tonight is a generated planner.

## Finding format (one line each, in your group's file)
`| id | where (file / step id / URL) | dim (U1…E5) | severity | finding | evidence | fix |`
- **Severity:**
  - blocker: builds wrong, or unsafe;
  - major: likely confusion, rework, or a wrong number;
  - minor: friction;
  - polish.
- **Evidence:** cite the source page, photo, STL or rendered screenshot you checked.
- **Fix:** concrete and short, and within the conventions above.
- Before reporting, skim `review/2026-09-05`, `2026-09-06` and `2026-09-14` for your chapters, and don't re-report something already fixed.
