# G8 — Build order and flow (goal 3), print-side files (goal 1)

**Group:** G8 (flow). Reviewer: claude deep tier, 2026-10-30, read-only; tree reviewed as is (orchestrator's
uncommitted Rev D+ edits included).

**Files covered:** docs/voron-print-plan.md, docs/manual/00-index.md (timeline, critical path, batch table),
docs/manual/00-tonight.md, docs/manual/print/README.md, docs/manual/print/00-slicer-setup.md,
docs/manual/print/B00-calibration-and-jigs.md, docs/print/plate-board.md (+ docs/assets/plate-board.json),
docs/print/plate-plans.md, docs/print/checklists.md, docs/print/bin-labels.md,
slicer/bench/hardware-trays/README.md; header, prerequisites and every `Pause:` line of Ch 00–14; B01/B05/B11
where they set the schedule.

**Primary sources used:** `slicer/estimates.csv` (per-plate times), `slicer/plates.py` + `slicer/bins.py`
(which plate feeds which bin and chapter, computed, not read from prose), the 26 committed
`slicer/plates/*.3mf` (count, start G-code), `docs/assets/plate-board.json`, every chapter's `Pause:` minutes
(summed by script), PROJECT_MEMORY.md and context/build-facts.md for state and rulings, and a discrete-event
schedule simulation (below). **Images opened:** 1 (`assets/diagrams/11-build-timeline.svg`, rendered).

Counts: 0 blocker · 5 major · 14 minor · 3 nit.

---

## Answers to the five questions

**Method.** A 15-minute-step simulation of one printer and one builder, from today (Fri 2026-10-30 17:30),
using the 26 plates' sliced times (+0.4 h chamber heat-up/cool per ASA plate, which B00.4's Tip says is not in
the estimates), the trays first (15.2 h), B00.8 review and Gates A/B as builder tasks, and the build rows 14–31
at their Time midpoints with each chapter's print needs computed from `bins.py` (Ch 08 needs B07-P1 only at
08.64, Ch 10 needs B08-P4 at 10.50, Ch 11A needs B10 by 11.44). Printer swaps: 2/day (06:45 + 21:30, weekends
08:00 + 21:30) or 3/day. Builder: the index's 22 h/week (2 h weekday evenings, 6 h each weekend day), plus 12
and 35 h/week for sensitivity. Kit lands at 18:00 on Nov 2, 4, 6 or 10. Scenarios: **S1** = the manual as
written (numeric B00→B10, B11 after B10 per index row 32, B01-P1 morning start); **S2** = S1 but B11-P1…P3
right after B07-P2 and B11-P4/P5 as soon as B11.10–11.11 are done; **S2b** = S2 with B02→B03→B04 printed
before B01 (front-loading Ch 04/05) and a builder free to take any unblocked chapter.

| Ch 14 done (2 swaps/day) | kit Nov 2 | kit Nov 4 | kit Nov 6 | kit Nov 10 |
|---|---|---|---|---|
| 22 h/wk, S1 (as written) | Nov 23 20:15 (5.8 h builder idle at Ch 09) | Nov 23 20:15 (1.8 h idle) | Nov 24 20:30 | Nov 29 |
| 22 h/wk, S2 | **Nov 22 10:00** (0 idle) | **Nov 22 16:00** | Nov 24 20:30 | Nov 29 |
| 35 h/wk, S1 → S2 | Nov 21 → **Nov 16** (24.8 h idle removed) | — | Nov 21 → **Nov 19** | Nov 23 = Nov 23 |
| 12 h/wk, S1 = S2 | Dec 08 | — | Dec 11 | Dec 15 |

S2b and "B00 before the trays" change nothing beyond ±1 day of weekend quantisation in any case. With 3
swaps/day every S1/S2 pair at 22 h/wk ties.

**(a) Print order.** Numeric order is already consumption order for B00–B10: Ch 01–05's batches (B00–B04,
64.2 h) are the first 64 h of the run, and the printer (~11 print-h/day at two swaps) out-runs the builder
(~3.1 h/day) about 2:1 in print-hours needed per build-hour, so front-loading anything further shortens
nothing (S2b = S2). The critical path is the builder from kit day to Ch 14 (≈ 18 days at 22 h/week). The one
print-side risk is **B11**: index row 32 prints it after B10, which lands it (Nov 15 in every S1 run) just as
Ch 09 needs it (Ch 08 done Nov 14–16). Moving B11-P1…P3 behind B07 removes that wait: **1.2–1.4 days saved
if the kit lands by ~Nov 4 at 22 h/week, 2–5 days at 35 h/week, nothing if the kit lands Nov 6 or later**, at
the cost of one extra satin↔textured / ASA↔PETG swap (~10 min). B08–B10 still finish (Nov 14) ≥ 3 days before
Ch 11A needs them. G8-01.

**(b) Chapter order.** Sound as written. Ch 12 Part 1 on kit day and Part 2 after Checkpoint #1 are right
(12.11 is the first sanctioned power-on); Ch 04 before Ch 02 only helps if the kit beats B02 off the bed,
which no realistic date does (B02 done Nov 4–5). Ch 13 → 06b → 11B → 14 is right; the Checkpoint 11 *Next*
button pointing at Ch 12 instead of Ch 14 is known and still open. What the order lacks is a **location
decision and a move point** (G8-02) and, for the 30-minute/child-helper reality, a list of **bench fillers**
(Ch 04 sub-assemblies, Ch 08 SB/CW2 bench builds, Ch 11 Nevermore 11.26–11.40 and door hinges 11.44–11.50)
for nights when a 2P row (Ch 01, 05, 06 lift, 06b) has no second person (minor, G8-13).

**(c) Pre-kit and parallel work.** Since the builder is the bottleneck, only work moved to *before* kit day
shortens the end date (1 builder-hour ≈ ⅓ day at 22 h/week). Movable without a kit part: 12.2–12.3 (write
MainsailOS to the separately-bought microSD; Rev D+ ships no SD card), a local draft of the printer.cfg edits
12.21–12.22 and 12.24–12.36 (all but the serial paths 12.23 and the board-dependent checks), 13.41 (the
PrusaSlicer profile for the Voron), and 11.68's three camera-board rows once the OV5640 is bought: ≈ 1.5 h,
≈ ½ day. Kit-day sequencing: start the IPA soak (00.18, "an hour at least, overnight is better") early and run
B11.10–11.11, Ch 12 Part 1 and Ch 01 while the rails dry; nothing in Ch 01 needs a greased rail. Everything
after kit day already runs in parallel with the printer. G8-12.

**(d) Session structure.** Forced idles found: the printer pauses for an operator at the planned B09-P1
runout, which the index says resumes by itself (G8-05); Gate B "the same week" plus B01-P1's morning-only
start idles the printer one night (16 h in the sim) when Gate B is signed off after the morning swap
(G8-07); Gate B's insert row is technique, yet failing it holds B01 (G8-08); B00.8 reviews all 26 plates
before B00 can start, although only B00-P1 has to be reviewed first (G8-09). Long unbroken segments (Ch 07
80 min, Ch 01 65 min, Ch 06b 60 min, Ch 02 55 min) need weekend slots; the index lists 06b as 1 × ~30 min
(G8-11). After ~Nov 14 the printer is free until the add-on jobs (11.69 ≈ 14 h, 13.48 2.5 h, 14.26 7 h):
that is the window for INBXX (~69 h), provided the add-on jobs keep priority (G8-10).

**(e) Totals.** Run totals (150.2 h, 1802 + 277 g, 21 plates, B11 24.9 h / 348 g) agree across README,
plate-plans, checklists, plate-board.json, Tonight, the index and the diagram. Stale figures remain in prose
around them: G8-11 and G8-14.

### Proposed timeline (kit ≈ Fri Nov 6, 22 h/week, two plate swaps a day; simulated dates)

| When | Core One+ | Bench |
|---|---|---|
| Oct 30 – Nov 1 | Trays A, B, C (PLA, 15.2 h) | B00.8 review of **B00-P1 only** (the rest before each batch); decide the Voron's spot (G8-02); 00a; Ch 00 pre-kit steps; 12.2–12.3 microSD; printer.cfg draft |
| Nov 1 | B00 (3.8 h) | Gate A + Gate B bore row the same day |
| Nov 1 eve – Nov 7 | B01-P2 that night if Gate B passed after the morning swap, B01-P1 next morning; then B02 ×3 → B03 → B04 → B05 → B06 → B07 ×2 | sort each plate; read ahead |
| Nov 7 – 10 | **B11-P1 (coupon) → P2 → P3**, then **P4/P5** as soon as B11.10–11.11 are done | kit day: inventory, Gate B kit rows, trays, rail soak → B11.10–11.11 → Ch 12 Part 1 → Ch 01 while rails dry; grease before Ch 02 |
| Nov 10 – 14 | B08 ×4 → B09 ×4 (**B09-P1 on fresh spool #3**) → B10 | Ch 02 (~Nov 8) → 03 → 04 → 05 (~Nov 14) |
| Nov 14 → | Add-on jobs when their gates pass (11.69, 13.48, 14.26); INBXX overnight plates in between | 06A → 07 → 08 (~Nov 16) → 09 (~Nov 17) → 10 (~Nov 20) → 12 Pt 2 → 11A → **move to the final spot** → 13 (~Nov 22) → 06b → 11B → 14 (~Nov 24) |

The end date is set by builder hours, not print order: at 12 h/week the same plan ends ~Dec 11.

---

## Findings

### G8-01 major goal 3 — B11 is scheduled after B10, so with an early-November kit it lands just as Ch 09 needs it; print P1–P3 after B07 and P4/P5 right after the kit-day measurements

- docs/manual/00-index.md:132 (row 32) — "needs: B10 off the bed (row 13); the PETG V0 spool and the textured sheet."
- docs/manual/00-index.md:136 (row 33) — "needs: row 32 and the kit-day bay measurements … must finish before Ch 09 (row 24)"; :137 "*While it prints:* Ch 00–08 build rows"
- docs/manual/print/README.md:273 — "Print whenever the Core One+ is free" (no B10 condition); B11-bay-ducting.md:12 "P4 and P5 print right after kit day".

Evidence: B11 feeds bins 09-ducts-DC/AC (Ch 09), 10-lids-AC (Ch 10.80), 11-lids-DC (Ch 11.52) (`bins.py`).
Under row 32 the run reaches B11 only after 150.2 h of ASA; simulated, B11-P5 is off the bed Nov 15 while Ch 08
ends Nov 14 (kit Nov 2) to Nov 16 (kit Nov 6). Row 33 cannot print "while Ch 00–08" run because it needs row 32,
which needs B10. Quantified in the table above: 1.2–1.4 days lost at 22 h/week if the kit lands by Nov 4; up to
4.8 days at 35 h/week; none for a kit on Nov 6 or later. B08–B10 are not needed until Ch 10.50 / Ch 11A, ≥ 3 days
after they finish in S2. Row 32's title "before kit" is also unreachable now (the kit lands around B02).

Fix (index row 32 needs): "needs: B07 off the bed (row 10); the PETG V0 spool and the textured sheet. Print it
between B07 and B08." Row 33: "needs: row 32 and Steps B11.10–B11.11 (kit day); print it at the next free slot
after them, ahead of any B08–B10 plate still waiting". Retitle row 32 "B11 — Bay ducting, part 1" (ids
unchanged). Mirror in README § B11 run schedule (# column: insert after #12) and print plan §2's order
sentence. Cost: one more sheet/filament/filtration swap back to ASA (B11.8's Pause already covers it).

### G8-02 major goal 3 — The Voron's final location is undecided and no step says when the machine moves; three gates depend on it

- docs/manual/00a-mains-safety.md:155 (00a.5, a pre-kit step) — "The wall outlet the printer will live on, and the breaker that feeds it."
- docs/manual/01-frame.md:603 — "Work through Checkpoint 01, then the frame can come off the counter." (to nowhere named)
- docs/manual/14-calibration.md:1092 (14.25) — "The housing stands about 62 mm proud … Move the machine forward, or stop here."
- PROJECT_MEMORY.md § To print (Side projects) — "move Voron before power-on. Gate: nightstand ≥ ~55×55 cm, rigid: FAILS … Voron spot open."

Evidence: no chapter, index row or Tonight segment names a location decision or a move (grep for
nightstand/location/move/carry across docs/: none). Ch 13 sets QGL, Z=0 and the mesh; Ch 06b squares the
gantry; Ch 14 Part E measures input shaping, which is a property of the machine on its surface (engineering
inference, not a quoted source); a move after Ch 14 repeats at least Part E and the mesh. 00a.5 cannot be
closed honestly before the spot is chosen, and the 14.25 depth check and Part C's right-side spool frame
depend on it.

Fix: append a pre-kit step to Ch 00 (next free id; no renumbering): "**Choose where the Voron will live.**
Rigid surface ≥ 55 × 55 cm (more on the right for the side spool), a GFCI outlet within reach (00a.5 tests
that outlet), ≥ 70 mm free behind if the exhaust add-on is wanted (14.25), and a route you can carry a 20 kg
machine along with two people." Add to Checkpoint 00a: "the printer's spot chosen and its outlet is the
one tested". Add to index row 28 (Ch 13) needs: "the machine on its final spot — move it before 13.1, never
after Ch 14 Part E". Confidence: high that the gap exists; the 55 cm and 20 kg figures are approximate.

### G8-03 major goal 1 — Index row 1, Tonight and the timeline diagram still say "Gen 2 joints and wiper" first, against the 2026-10-28 ruling

- docs/manual/00-index.md:25 — "**1 · Both** — **Gen 2 joints and wiper, then pre-B00 checks, Gen 1 belts** · ~3 h · needs: the Gen 2 kit on the shelf"
- docs/manual/00-tonight.md:15, :21, :28 — "**First, before B00 (not tonight):** Gen 2 joints and wiper, then pre-B00 checks, Gen 1 belts."
- docs/manual/assets/diagrams/11-build-timeline.svg row 1 — "Gen 2 joints and wiper, then pre-B00 checks, Gen 1 belts ~3 h"
- vs docs/manual/print/B00-calibration-and-jigs.md:87–91 — "**0. Gen 2 expansion joints and nozzle wiper: skipped** Not fitted (Alex 2026-10-28)"; index:27 and :141 say the same.

Evidence: the Tonight planner's first line on every "Before the kit" plan tells the builder to fit the Gen 2
parts. Fix (index:25, which regenerates Tonight and diagram 11): "**1 · Print** — **Pre-B00 checks on Gen 1
belts: belt pluck, hot first layer, brim-gap ladder** · ~1.5 h · needs: nothing". Then rebuild Tonight and
`draw_diagrams.py --only 11` (orchestrator).

### G8-04 major goal 1 — ASA is printed on the satin sheet now, but six places still say "smooth sheet back on" for ASA or list add-ons on "smooth"

- docs/manual/print/README.md:304–307 — sheet column "smooth" for all four ASA add-ons; same page :321 "satin sheet".
- docs/manual/00-tonight.md:122, :406, :414 — "Swap the smooth sheet back on and set Adv. Filtration if an ASA plate is next."
- docs/print/checklists.md:465 — "Smooth sheet back on the printer and Chamber Filtration on Adv. Filtration for any ASA plate"
- docs/manual/print/B00-calibration-and-jigs.md:180 — "the **textured** sheet, not the smooth one."
- (source of the generated lines, not my file) B11-bay-ducting.md:73, :86, :201, :203, :407, :409, :422.
- vs AGENTS.md "ASA satin + brim, no glue (Alex 2026-10-28)"; 00-slicer-setup.md:196 "ASA (every Voron plate, the add-on prints) | **satin**, no glue … Smooth PEI without glue risks ASA tearing the film".

Evidence: a builder following B11's Pause after the PETG plates fits smooth PEI for B08 (or, under G8-01, for
every plate after B11): the very sheet 00-slicer-setup says ASA can tear without glue. Fix: "smooth" → "satin"
in all of them (B11: "Swap the satin sheet back on"; README add-on column "satin"; B00.8 "not the satin
one"); rebuild Tonight and checklists.

### G8-05 major goal 1/3 — The index says the printer resumes by itself after B09-P1's planned runout; it waits for a person, mid-day, on visible parts

- docs/manual/00-index.md:70 — "The one predicted runout lands mid-plate on B09-P1 … and the printer resumes on its own"
- vs docs/manual/print/README.md:239 — "Follow the screen … Load the next spool, check it extrudes clean, press **Continue**."
- docs/manual/print/README.md:190, :223 — #2 has ~31 g at B09-P1's start; the plate needs 71 g; B09-P1 is a 4.4 h *day* plate (run schedule #17).

Evidence: started at a morning swap, the runout comes ~2 h in, while the house is empty; the plate sits paused
until someone returns (≈ 8–10 h in the sim's weekday pattern), and B09-P1 carries the exhaust cover and two
Z belt covers, both visible, the same reason README:201–203 already gives for not running out on B08-P4.
Fix: start B09-P1 on fresh spool #3 and keep #2's ~31 g stub with #1's 137 g for clip reprints. Margin is
unchanged (598 g); #3 ends at ~430 g. Ledger: B09-P1 "#3 (fresh; #2's 31 g kept)", remaining 729 → 638 → 557
→ 505 → 430; README:186–190 and :201–203, index:66/:70 and plan §4.3 (:737–739) follow. If Alex prefers the
runout, at least replace index:70's "resumes on its own" with "pauses for you: load spool #3 and press
Continue (README § When the printer stops)" and make B09-P1 an evening start.

### G8-06 minor goal 3 — Ch 01, 02 and 05 prerequisites name the B02 plates as they were before the 10-24 re-split

- 02-z-drives.md:21 — "Print batch **B02** … plates P1 and P3 — the five `[a]_` parts below." 01-frame.md:19 — "Ch 02 needs only B00, B01 and B02-P1/P3".
- 05-gantry.md:20 — "**B02-P3** (the blue accent plate — cable bridge, endstop pod and the four upper Z-belt clips)".
- vs `bins.py` + `plates.py` (computed): 02-Z1 takes baseplate_b, z_tensioner_9mm and belt_tensioner_b off **B02-P2**, 02-Z2 baseplate_a off B02-P2; 05-XY = endstop pod (P1), 2-hole bridge (P2), Igus backer (P3), upper clips on P1, P2 and P3 ×2. Index :87/:96/:143 are right ("all three plates gate Ch 02").

Evidence: harmless under back-to-back B02, but wrong for anyone gating by plate. Fix: 02:21 "plates P1, P2
and P3 (the baseplates, belt tensioners and Z tensioners are spread across all three)"; 01:19 "B00, B01 and all
of B02"; 05:20 "**B02** (all three plates: endstop pod P1, cable bridge P2, Igus backer P3, upper Z-belt
clips on P1–P3)". Same lines: 05:20 "8.6 h" → 8.7 h; 05:1187 "6.4 h" → 6.2 h.

### G8-07 minor goal 3 — Gate B "the same week" and B01-P1's morning-only start leave the printer idle a night after B00

- B00-calibration-and-jigs.md:5 "runs in the same week"; :313 "run Gate B in the same week before B01 and B03 to B06"; 00-slicer-setup.md:270 "run Gate B first, the same week".
- README.md:56 / B01:57 "B01-P1 … start it in the morning"; run schedule #2 B01-P1 then #3 B01-P2.

Evidence: B00 is a 3.8 h day plate; Gates A and B need a cooled cube, a caliper and the iron (~40 min). The sim
signs them off Sunday 14:45 and B01-P1 waits for Monday 06:45 (16 h idle). Fix: "Gate B the same day as Gate
A, before the next swap", and in README § Run schedule add: "If Gate B is signed off after the morning swap,
start B01-P2 (7.5 h) that evening and B01-P1 the next morning" (B01-P1 then starts with 649 g, ≥ 200 g rule
still met).

### G8-08 minor goal 3 — Gate B's insert row is technique, yet the gate calculator will not release B01 until it passes

- B00-calibration-and-jigs.md:378–382 — inserts row: "A bulging boss is technique, not the slicer … practise … Do not re-slice anything."; :395 pass text "B01 and B03 to B06 are released" only when all non-optional rows pass; Checkpoint B00 :428.

Evidence: B01 (22.3 h, the head of the critical print chain) waits on soldering practice that says nothing
about the print. Fix: mark the `inserts` row `optional: true` with "no: … B01 can still print; pass this row
before Ch 02 Step 02.03", and pass text "B01 and B03 to B06 are released on the bore row."

### G8-09 minor goal 1/3 — B00.8 reviews "25" plates (there are 26) and demands all of them before B00 can print

- B00-calibration-and-jigs.md:21 "reviewing all 25 committed plates"; :160 "each of the 25 committed 3MFs"; :169 "All 25 plates ticked"; vs :164 "the 21 ASA plates … then B11's 5", checklists.md:470–534 (26 boxes), `ls slicer/plates/*.3mf` = 26.
- :69 "baked into all 20 projects" (26 carry the cold start); :190 "re-slices all 27"; 00-slicer-setup.md:83 "all 25 plates", :85 "all 27".
- :156 "Do it before B00-P1 starts" with four helper sessions (~100 min).

Fix: 25/20/27 → 26. Flow: "Review B00-P1 before it starts; review each later batch's plates before its Load
step, B11 with its own" — the four-session block then stops being a precondition of the run (today the trays
cover the wait, so the saving is small).

### G8-10 minor goal 3 — The timeline has no place for the trays, the add-on jobs or the free-printer window after the run

- 00-index.md rows 1–33 and 00-tonight.md: no tray row (README.md:341 "15.2 h … any time the Core One+ is free before kit day"; PROJECT_MEMORY: trays print before B00).
- 00-index.md:74 (row 13) — "Every bin is now full and the printer is free" (B11's four bins are not, under row 32).
- Add-on jobs sit mid-chapter: 11.69 (~14 h), 13.48 (2.5 h), 14.26 (~7 h), README.md:298–332.

Evidence: simulated, the ASA run + B11 end ~Nov 14 and the add-on jobs come ~Nov 20–24; INBXX (~69 h,
PROJECT_MEMORY "print INBXX after the Voron plates (during assembly)") would fill that gap and collide with
11.69/13.48. Fix: row 2 needs "the hardware trays printed or printing (bench print, README § Bench prints)";
row 13 text "Every ASA bin is now full; B11 and the add-on jobs are what the Core One+ still owes the Voron";
one sentence under the timeline: "After the last plate, other jobs (INBXX) may run overnight, but keep a day
slot free when 11.69, 13.48 or 14.26 comes up; those three sit on the build's path." Also rows 4–13's
*While it prints* ("Read Ch 02" …) describe the pre-overlap plan: from the kit day on, the build rows are what
runs while those batches print.

### G8-11 minor goal 1 — Critical-path figures disagree with their own inputs

- 00-index.md:153 / README.md:83 / plan :248 — "~16 printer-days ≈ 3–4 weeks". 16 printer-days of continuous printing is ~2.3 calendar weeks; the sim (2 swaps/day) runs B00 → B10 in 13 days, B11 included 14.
- 00-index.md:152 — "Hands-on time **59.9 h**"; the chapters' `Pause:` minutes sum to 64.8 h without add-ons (Ch 00 4.2, 01 2.9, 02 5.9, 03 1.9, 04 3.6, 05 6.0, 06+06b 5.3, 07 3.3, 08 4.1, 09 4.1, 10 6.5, 11 A+B 5.3, 12 2.8, 13 3.9, 14 4.2, 00a 0.9), plus ~4.5 h of plate sorting and starts that now fall inside the build weeks. Ch 14's core Pauses (4.2 h) exceed its own 2.5–4.0 h header.
- 00-index.md:158 — "plus 20 plate starts" (21 ASA + 5 B11 = 26). :155 "Starting late October" (B00 starts ~Nov 1 after the trays).
- 00-index.md:129 and :178 — Ch 06b "1 × ~30 min" vs 06-z-axis…md:1063 "Pause: ~60 min … Part B is one session by design".

Fix: "~16 printer-days ≈ 2–2½ weeks"; "Hands-on ≈ 65 h by the Pause lines (59.9 h by the Time midpoints)" and
"Building ≈ 3 weeks at 22 h/week"; "26 plate starts"; "starting ~1 November"; 06b "1 × ~60 min, unbroken".

### G8-12 minor goal 3 — Pre-kit work that would shorten the kit-to-Ch 14 path is not marked `(pre-kit)`

- 12-software.md:94–146 (12.2–12.3 write MainsailOS) needs only the microSD + reader, on the before-kit buy list (PROJECT_MEMORY § Purchases decided 10-05); Rev D+ ships no SD card (BRIEF).
- 12-software.md:712–1515 (12.21–12.22, 12.24–12.36): text edits to LDO's sample config; only 12.23 (serial paths), 12.28 (verify) and 12.37 (compile on the Pi) need the boards.
- 13-initial-startup.md 13.41 (PrusaSlicer printer profile, ~15 min at the laptop); 11-skirts-panels-door.md:1948 (11.68) rows `holes`, `pegs`, `length` need only the bought camera board.

Evidence: builder hours are the critical path (table above); ≈ 1.5 h moved before kit day ≈ ½ day earlier
finish at 22 h/week. Fix: tag 12.2–12.3 and 13.41 `(pre-kit)`; add a Tip to 12.21: "Before the kit: copy
LDO's `-sbv2` file to a laptop and make 12.22 and 12.24–12.36 there; paste it in at 12.21 and do 12.23 on
the Pi." Confidence medium on the printer.cfg draft (the steps are written for the Mainsail editor).

### G8-13 minor goal 3 — 2P rows have no fallback; bench sub-assemblies could fill nights without a second person

- 00-index.md:19 markers; rows 16, 20, 21, 29 are **2P**; the brief's builder is one adult plus a child helper in 30-minute sessions.

Fix (one paragraph under the timeline): "No second person tonight? Bench work that needs no frame: Ch 04
sub-assemblies (04.1–04.33), Ch 08's Stealthburner and Clockwork 2 bench builds, Ch 11's Nevermore
(11.26–11.40) and door hinges (11.44–11.50), each once its bins are full." (Confirm the Ch 08/11 step ranges
against those chapters before writing.)

### G8-14 minor goal 1 — Stale hours, grams and plate counts in prose around the (correct) totals

- docs/print/plate-board.md:3 — "The 20 plates of the ASA run … outside the run's 157.0 h" → 21 plates, 150.2 h (plate-board.json is right: 26 plates, run 150.2 h).
- voron-print-plan.md:241 — "B00 + B01 + B02-P1 + B02-P2 + B02-P3 ≈ 49 h" → 3.8 + 22.3 + 20.9 = **47.0 h**.
- 00-slicer-setup.md:269–270 — "that is 58.4 h and 763 g" → B01 + B03–B06 = **57.3 h, 759 g**.
- B00-calibration-and-jigs.md:438 — "protects 22.8 h of Z-drive bodies" → 22.3 h.
- 11-skirts-panels-door.md:21–22 — "B08 … (6 plates, 29.2 h)", "B09 … (5 plates, 21.8 h)" → 4 plates, 26.7 h; 4 plates, 20.5 h (the B08 plate count is 10-23 G1-23, still open).
- B11-bay-ducting.md:8 — "Not part of the 156.9 h ASA run" → 150.2 h. B01-z-drive-assemblies.md:83 — "Estimated plate time is **15 h 13 m**" vs estimates.csv 14 h 50 m (B00.2's 3 h 50 m matches).

### G8-15 minor goal 1 — Pre-B00 hot-check pass band is the old one in three places; "Two checks" lists three

- 00-index.md:27 "0.17–0.23 mm each, spread ≤0.05 mm"; voron-print-plan.md:892 and 00-slicer-setup.md:413 the same.
- vs B00-calibration-and-jigs.md:113 "a good square reads about 0.24–0.26 mm across the middle (the plates print the first layer at Z 0.28)" (z_offset +0.08, PROJECT_MEMORY 10-29).
- voron-print-plan.md:881 and 00-slicer-setup.md:400 "Two checks replace the upgrade" then items 1–3 with 2 dropped, and no brim-gap ladder; index:141 "Row 1's two checks (belt pluck, hot first layer)".

Fix: "every square smooth and closed, about 0.24–0.26 mm on calipers, all five alike (B00 item 3)"; "Three
checks … belt pluck, hot first layer, brim-gap ladder".

### G8-16 minor goal 1/3 — Ch 02's bins are not "full" until B05, which prints after Ch 02 has passed 02.10

- 00-index.md:87 (row 17) — "bins for Ch 02 full (B00, B01, **B02**)"; README.md:129–132 bins 02-Z0…Z3 "from batches B00, B01, B02, B05" (`z_rail_stop`).
- 02-z-drives.md (02.10) "Optional … Skip them and the tape from Step 02.08 covers you until Ch 06."; B05-z-joints-and-z-chain.md:103 "the rail stops stay bagged".

Evidence: B05 ends ~70 h into the run (sim: Nov 6), about when Ch 02 reaches 02.10 with a Nov 2–4 kit; a
literal "bins full" reader waits ~a day for an optional part. Fix: row 17 "(B00, B01, B02; B05's rail stops
are optional, tape until they arrive)"; B05.5 "drop the rail stops in 02-Z0…Z3; if Ch 02 is past 02.10, fit
them before the gantry lift at Ch 06".

### G8-17 minor goal 1 — Index "Dependencies inside B02" sends the upper Z-belt clips and chain retainers to Ch 06 and omits the cable cover

- 00-index.md:143 — "the Z belt clips and chain retainers gate Ch 06 Part A".
- vs `bins.py`: upper clips → 05-XY (Ch 05, 05.19–05.23), lower clips → 06-Z-joints, chain retainer brackets → 10-chains (Ch 10, staged at 06.26), `[a]_cable_cover` (P3) → 07-X (Ch 07), not mentioned.

Fix: "the upper Z belt clips go to Ch 05 and the lower ones to Ch 06 Part A; the cable cover (P3) to Ch 07;
the chain retainers to Ch 10 (bagged with the chain at 06.26)".

### G8-18 minor goal 2 — Timeline diagram draws no rail from B11 to Ch 09, 10 or 11, though Ch 09's needs list names all five B11 plates

- assets/diagrams/11-build-timeline.svg (rendered): rows 32–33 have no outgoing rails; Ch 09 shows only B07's rail. Footer: "Each orange rail leaves a print batch and forks to every chapter whose needs list names it".
- vs 00-index.md:108 (row 24) "bins for Ch 09 full (B07, all five B11 plates)", :111 (row 25) "B11 strip fin and AC lids", :126 (row 30) "B11 DC lids".

Evidence: the one batch that can starve the build (G8-01) is the one the diagram shows as unconnected.
Fix: draw B11 rails to rows 24, 25 and 30 in `draw_diagrams.py` (and move rows 32–33 under row 10 if G8-01 is
taken).

### G8-19 minor goal 1 — The 00-jigs bin says the pulley jig is used at 02.18; 02.18 uses a caliper, and README's copy of the row differs

- slicer/bins.py:59 and docs/print/bin-labels.md (00-jigs label) — "pulley jig at 02.18, 04.24, 04.33".
- 02-z-drives.md 02.18 — "**Parts:** … tool: caliper … Caliper the first pulley at 33 mm"; no `pulley_jig` anywhere in Ch 02.
- README.md:128 — "pulley jig at 04.24, 04.33" (the README row claims to be generated from bins.py but no longer matches it).

Fix: bins.py:59 drop "02.18, "; regenerate labels; the README row then matches.

### G8-20 nit goal 3 — Kit-day order lets the rail IPA dry become a stop instead of a window

- 00-before-you-start.md:731 "an hour at least, overnight is better … stopping here costs nothing"; index rows 14–16 run Ch 00 (rails included) before Ch 12 Part 1 and Ch 01.

Fix (row 14 *While it prints*): "Start the IPA soak (00.17–00.18) early on kit day; while the rails dry do
B11.10–B11.11, Ch 12 Part 1 and Ch 01 (no rail needed); grease (00.19–00.21) before Ch 02."

### G8-21 nit goal 1 — "Halfway: plate 11 of 21" sits on B07-P1, 60 % of the run's hours

- plate-board.json milestone on B07-P1. By count it is right; by hours (89.7 of 150.2 h) it is not. Optional: "Plate 11 of 21; 60 % of the hours done."

### G8-22 nit goal 1 — context/build-facts.md:17 still has "ETA late November to late December 2026"; line 26 "prints before kit day"

Untracked file, not shipped; PROJECT_MEMORY and the docs carry early November. Update when convenient.

**Known, still open (not re-reported):** Checkpoint 11's *Next* goes to Ch 12, not Ch 14; README.md:269/:286
"V1 … not yet bought" (PETG V0 bought 10-13).

---

## Checked and consistent

- Run totals: 21 plates, 150.2 h, 1802 g + 277 g, margins 598 g / 523 g; B11 5 plates, 24.9 h, 348 g. Same in README, plate-plans, checklists (26 boxes, per-plate h/g = estimates.csv), plate-board.json, Tonight header, index :5/:151, diagram footer, plan header.
- README run schedule: 10 overnight + 11 day plates; spool ledger arithmetic (#1 749→137, #2 653→31, #3 760→461) and B01-P1 ≥ 200 g rule.
- Batch → chapter needs in index rows 17–30 against `bins.py` (except G8-16, G8-17): Ch 04 B02-P2/P3 + B03 + pulley jig; Ch 05 B02 + B04 + rail guides; Ch 06A B02 + B05; Ch 08 B02/B04/B06/B07-P1; Ch 09 B07 + B11; Ch 10 B05/B07/B08-P4/B02/B11; Ch 11A/B.
- Numeric print order = consumption order for B00–B10; front-loading Ch 01–05's batches gains nothing (simulated).
- Chapter order rows 14–31 against chapter prerequisites: Ch 12 Part 1 needs only the Pi; Part 2 after Checkpoint #1; Ch 13 → 06b → 11B → 14.
- Pause minutes vs chapter Time ranges: within range for every chapter except Ch 00 (4.2 h incl. pre-kit, over 4.0) and Ch 14 (4.2 h core, over 4.0).
- Gate structure: Gate A releases B02/B07–B10, Gate B releases B01/B03–B06, the same in README, B00, 00-slicer-setup, index, plate-board notes.
- B00-P1 sliced figure (3 h 50 m / 51.3 g) = estimates.csv; hardware-tray figures (A 5 h 58, B 4 h 40, C 4 h 36 = 15.2 h, 531 g) agree between README and the trays README.
- Gen 2 deferral and cold-start retention: consistent in B00, 00-slicer-setup and plan §8 bodies (only the headings and row 1 lag, G8-03/G8-15).
