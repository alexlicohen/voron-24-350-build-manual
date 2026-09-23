# Revali — design notes (mascot-revali-fable)

**Cues chosen (two, plus one implied).**
1. Champion's scarf — a band round the neck, a knot at the back, two tails streaming behind. Reads at 30 px as one blue stroke under the chin; it is the cue that ties him to the build (frame blue).
2. Braided nape feathers — two plaits with a blue tie and a loose tuft, hanging from under the skull. Read at 48 px and above; one plain braid in the badge.
3. Revali's Gale, implied only: the tails stream in a self-made updraft. Asleep (`pause`) they droop, so the cap's tassel stays clear. No swirl lines.

**Rejected.** Green eyes (green is the PASS tick's, and the one big dark eye is the raven's identity); yellow brow / red cheek patches (amber is warn/fail only, and the friendly expression would go); a lighter, slate-blue plumage (no longer the same raven; the black-with-blue-sheen is already the nod); the bow, the Vah Medoh emblem, any Rito armour (public repo, homage not copy); an animated scarf (`.m-*` classes untouched); a scarf on the fledgling (not the champion).

**Palette.** `SCARF #1F4E9C` base (the manual's accent, 8.0:1 on white, 2.2:1 on the body and on slate), `SCARF_LIT #3A6DC4` lit fold (3.5:1 on the body — what carries it on the dark theme, with the halo rim), `SCARF_DK #163B7A` crease, knot and edge. Flat, no gradient. Rows added to STYLE.md § Palette.

**Files changed.** `scripts/gen_mascot.py` (Revali cue section; `bird()`, `bird_3q()`, `bird_front()`, `head_*()`, `halo_shapes()`, `pose_badge()` inherit it; titles/labels now "Revali …"; no API, pose id, class or file-name change), all 20 SVGs + 41 preview PNGs regenerated, `STYLE.md` (new § The Champion's cues, palette row, badge row, 20-file count), `docs/mascot.md` (intro, badge, pause, helper, front paragraphs; names section untouched), `hooks/mascot.py` (fallback title, docstring, self-test alts + a "every title names Revali" check), eight captions.

**Captions (old → new).**
- index.md: "Cartons open, bins already labelled, every plate printed." → "Cartons open, bins labelled, every plate printed. I planned it this way. Naturally."
- voron-print-plan.md: "…and it took surprisingly long to arrange." → "One plate is one job. That is the entire plan. Making it look this simple took a champion."
- 14-calibration: "…I brought a caliper, because feelings are not evidence." → "…I brought a caliper. Feelings are not evidence. My opinions nearly are."
- B01 pause: "I will supervise from the spool." → "A champion can supervise from a spool."
- B06 pause: "…inspect it at breakfast. I will be asleep." → "…inspect at breakfast. Even champions need their sleep."
- B02 print: "The blue spool goes on once, which is once enough." → "One blue spool, and yes, it matches my scarf."
- 07-ab-belts: "Ears are cheerful liars." → "Belts that sound alike are not alike. Measure both. My ears are excellent. I still measure."
- B08 pause: "…one long, quiet, entirely uneventful weekend." → "Four plates, one quiet weekend, and my updraft stays switched off." (also true: ASA hates a draught)
Mains-safety caption unchanged; FAIL caption unchanged (sympathetic).

**Uncertainty.** Character details are from fan wikis (Zelda Wiki blocked the fetch): canon is a *sky-blue* scarf with a white emblem, *four* braids with ribbons and rings, slate grey-blue plumage, green eyes. The frame blue and two braids are deliberate departures; nothing else was invented.

**For the orchestrator.** `mkdocs build` (the gate) regenerates `docs/print/bin-labels.md` and `docs/print/plate-plans.md` via `build_printables.py`; both now carry the "Revali …" alts (one-line diffs each, not hand edits). Still stale and out of my scope: `docs/index.md` line 2 (`alt='The raven, facing the reader'`) and line 27 plus `docs/print/plate-board.md` line 9 (`data-mascot-*-alt="The raven watching a first layer"`). Glossary/AGENTS/CLAUDE names still say "The raven".
