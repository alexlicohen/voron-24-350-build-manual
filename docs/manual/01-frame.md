# Chapter 01 — Frame

Builds the 2020 frame — bottom square, four verticals, top square — plus the two bed extrusions, squared on a verified-flat surface. Unlocks Ch 02 (Z drives) and Ch 03 (build plate), and fixes the squareness every later axis inherits.

**What you're building in this chapter:** the box the whole printer hangs off, out of 2020 aluminium extrusion — 20 × 20 mm bars with a T-slot down each face, so anything can be bolted anywhere along them. Three sub-assemblies. The **bottom square** is four horizontal extrusions joined by the four **verticals** that stand in its corners; the **top square** is four more horizontals closing the cube at the top. Every one of those sixteen corners is a *blind joint* — a screw threaded into the end of the horizontal, its head hidden inside the vertical's slot, tightened through a small access hole in the vertical's side. The **bed extrusions** are two more horizontals running front to back across the base, left and right of centre, carried on corner brackets from the front and rear bottom rails; the heated build plate sits on them in Ch 03, and their spacing has to match the plate's own mounting holes. Everything is assembled loose, squared with a tape measure and a mallet, and only then tightened — because a bolt taken to full torque locks in whatever error was there when you tightened it.

**Time:** 2.5–4.0 h hands-on, first build, two people ([survey §5.1 P01 / §7.2](../voron-build-instructions-survey.md)).

**Sessions:** 4 × ~30 min — the `Pause:` lines below break the chapter into 4 segments; every minute figure is a first-build estimate.

**Prerequisites:**

- **Ch 00** — inventory, extrusions counted, tools to hand.
- **Print batches: none gate this chapter.** No printed part is required for the frame; you can square it the day the kit lands ([print plan §2](../voron-print-plan.md)). Batch **B01-P1** went on the Prusa the morning the kit landed, after Gate B (Step B00.7) — it prints under Ch 00 and this chapter, and Ch 02 waits only on B01-P2.

**Tools**

- 3 mm hex key, straight, long-arm — the kit's 3 mm L-wrench (the Fabreeko precision set is ball-end) — for the 16 M5×16 BHCS blind joints; the access hole is in line with the bolt, so no ball end is needed and a straight key is better for the torque pass. A 3 mm ball-end is optional for the first snug
- Machinist square, 150 mm, DIN 875/2 or better
- Steel rule 300 mm, plus a steel tape ≥1 m (a 350 frame's plan diagonal is ≈721 mm)
- Straightedge + feeler gauges, 0.02–0.10 mm — to re-check the reference surface (Step 01.1)
- Flat reference surface: the kitchen stone counter, verified (decision recorded in `CLAUDE.md` → Tools & metrology)
- Rubber or nylon mallet, for nudging the frame square
- Torque screwdriver 0.5–3 N·m — optional; the manual specifies no torque value
- Masking tape + marker (FRONT label, extrusion labels, log)

**Printed parts**


| STL | Qty | Colour |
|---|---|---|
| *none — this chapter needs no printed parts* | — | — |

**Hardware** (chapter totals)

| Fastener / part | Qty | Where |
|---|---|---|
| A extrusion | 10 | 4 bottom + 4 top frame (p.15–17), 2 bed (p.18–20) |
| B extrusion | 4 | verticals (p.15–16) |
| M5×16 BHCS | 20 | 16 frame blind joints + 4 corner brackets |
| Corner bracket | 4 | one per bed-extrusion end (p.18) |
| M5×10 BHCS | 4 | bed extrusions down to the frame (p.19) |
| **M5 precision spacer, brass** | 4 | under each M5×10 head — replaces the manual's "M5 shim" |
| M5 T-nut, roll-in | 4 | bottom rails, under the bed extrusions (p.19) |
| M3 T-nut, roll-in | 1 | fit test only (Step 01.3) — goes back in its bag |

C, D and E extrusions are sorted here but **not used** in this chapter — they are the gantry (manual p.85, p.88, p.101 → Ch 05).

**Read first**

- **Frame squaring is the one irreversible quality decision in this build.** Re-check after every tightening pass. Gantry racking, quad-gantry-level and bed mesh all inherit what you set here (survey §4.4 #1).
- Extrusion and roll-in T-nut tolerances are tight in this kit. LDO: *"Due to the tight tolerances of the extrusions and roll-in t-nuts it is advisable to either test fit before assembly to identify the sides of the extrusions that fits the best or to pre-load the t-nuts into the extrusions."* [src](https://docs.ldomotors.com/en/voron/voron2/build-faq)
- Every **"M5 shim"** in the official manual is a **brass M5 precision spacer** in this kit — here and for the rest of the build.
- **Titanium extrusion backers are NOT installed in this chapter.** They go onto the gantry's X and Y extrusions during **Ch 05**, on the face opposite the rail. Leave them bagged; fitting them to frame extrusions now would be wrong and fitting them after the gantry is assembled costs a teardown (survey §4.4 #3, §5.2 W2). This is the only place this note appears.
- Nothing here is printed. Build it the day the kit lands, while batch **B01** prints.

**Sources for this chapter:**

- [Voron 2.4r2 assembly manual (pinned `de7e89d`)](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf) pages 12–21 — extrusion sort, blind joints, bottom and top squares, bed extrusions, squareness check
- [LDO Build Notes (Rev D)](https://docs.ldomotors.com/voron/voron2/build-faq) — roll-in T-nut tolerance, and the brass M5 precision spacer substituted for every "M5 shim"
- [blind-joint video](https://voron.link/onjwmcd) and [frame squaring video](https://voron.link/kdtpzam) — the two videos the manual links from p.10 and p.21
- [whopping_Voron_mods — `extrusion_backers`](https://github.com/tanaes/whopping_Voron_mods/tree/main/extrusion_backers) — why the titanium backers are Ch 05 parts, not frame parts
- [survey](../voron-build-instructions-survey.md) §4.2, §4.4, §5.2

**Video coverage (Steve Builds, pre-release LDO kit — differs from Rev D+):** [Part 1 @0:54:42](https://www.youtube.com/watch?v=feTxcc0LIWM&list=PL0fUJbigELQPqpeGOgHYisG4KaSXVtnNY&t=3282s) (+2m), [Part 1 @0:55:46](https://www.youtube.com/watch?v=feTxcc0LIWM&list=PL0fUJbigELQPqpeGOgHYisG4KaSXVtnNY&t=3346s) (+19m), [Part 1 @1:14:12](https://www.youtube.com/watch?v=feTxcc0LIWM&list=PL0fUJbigELQPqpeGOgHYisG4KaSXVtnNY&t=4452s) (+14m), [Part 1 @1:29:00](https://www.youtube.com/watch?v=feTxcc0LIWM&list=PL0fUJbigELQPqpeGOgHYisG4KaSXVtnNY&t=5340s) (+19m), [Part 5 @3:14:50](https://www.youtube.com/watch?v=hTKCBrk36R0&list=PL0fUJbigELQPqpeGOgHYisG4KaSXVtnNY&t=11690s) (+2m)

---

### Step 01.1 — Verify the flat reference surface

![Voron manual p.12](assets/manual-pages/manual-p012.png)

**What you're looking at:** Manual p.12 opens the frame section. On your bench it is the stone counter, a long straightedge and feeler gauges. This surface is the frame's only reference: any **twist** in it, one corner high, is copied permanently into the printer.

**Parts:** none.

**Do:**

1. Re-clean the patch you masked at Step 00.10.
2. Run the straightedge and feelers over the same five positions: left–right, front–back, both diagonals, centre.
3. Work where both of you can reach all four corners. Put nothing underneath.

**Check:** Worst feeler gap ≤ 0.1 mm, no larger than your Ch 00 figure, and no rock of the straightedge. Write the number in the log.

Tip: tape a strip marked **FRONT** on the face you want to face you. Any face will do until the bed extrusions go in; after that it is fixed.

Source: [Voron manual p.12](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=12) · [Voron manual p.15](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=15) · [Video: Part 1 @0:53:46](https://www.youtube.com/watch?v=feTxcc0LIWM&list=PL0fUJbigELQPqpeGOgHYisG4KaSXVtnNY&t=3226s)

---

### Step 01.2 — Sort the extrusions by length

![Voron manual p.13](assets/manual-pages/manual-p013.png)

**What you're looking at:** Manual p.13 lays the eighteen extrusions out by length. These 2020 extrusions are 20 × 20 mm aluminium bars with a T-slot down each face. **A** is the horizontal, **B** the vertical, **C / D / E** the gantry in Ch 05.

**Parts:** all extrusions — A ×10, B ×4, C ×2, D ×1, E ×1 (counted off p.13).

**Do:**

1. Lay every extrusion out and sort by length.
2. Label each group A/B/C/D/E with masking tape.
3. Bag C, D and E separately, labelled for Ch 05: manual p.85, p.88, p.101.

**Check:** 10 A, 4 B, 2 C, 1 D, 1 E. Only the four B extrusions have small round **access holes** near each end.

Source: [Voron manual p.13](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=13)

---

### Step 01.3 — Inspect the ends and test-fit a T-nut

![Voron manual p.13](assets/manual-pages/manual-p013.png)

**What you're looking at:** The same p.13 layout plus one **roll-in T-nut**, a nut that drops into an extrusion slot and rotates a quarter turn to lock, see [glossary](16-glossary.md#r). You are checking for a burred end face and a slot that will not accept a nut.

**Parts:** 1× M5 roll-in T-nut and 1× M3 roll-in T-nut (for the fit test — both go back in their bags).

**Do:**

1. Deburr all 10 A and 4 B end faces.
2. Roll an M5 nut into the front and rear bottom rails' top channel, and the M3 nut into each vertical's two channels without access holes; tape the better face.

**Check:** Every end face sits flat on the machinist square with no rock, and every T-nut rolls in and rotates with finger pressure.

⚠ Rev D+ / LDO: extrusion and roll-in T-nut tolerances are tight on this kit — LDO's advice is to test-fit *before* assembly and identify the best-fitting sides, or to pre-load T-nuts. If one refuses to rotate, use a different face or a different extrusion; do not force it. [src](https://docs.ldomotors.com/en/voron/voron2/build-faq)

Source: [Voron manual p.13](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=13) · [LDO Build Notes (Rev D)](https://docs.ldomotors.com/voron/voron2/build-faq)

---

### Step 01.4 — Start an M5×16 BHCS in each end of eight A extrusions

![Voron manual p.14](assets/manual-pages/manual-p014.png)

**What you're looking at:** Manual p.14 shows eight A extrusions with an **M5×16 BHCS** button head cap screw started in the tapped bore at each end. The screw goes into the horizontal first because in the finished joint its head hides inside the vertical.

**Parts:** 8× A extrusion, 16× M5×16 BHCS.

**Do:**

1. Take 8 of the 10 A extrusions, keeping 2 back for the bed.
2. Thread an M5×16 BHCS into each tapped end bore, 16 bolts, until the head plus about 2 mm of shank stands proud. Leave finger-loose.

**Check:** All 16 bolts start cleanly and stand proud by the same ~2 mm. A bolt that binds means a damaged thread; fix it now.

Source: [Voron manual p.14](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=14)

---

### Step 01.5 — Understand the blind joint before you make one

![Voron manual p.15](assets/manual-pages/manual-p015.png)

**What you're looking at:** Manual p.15 and p.10 show one horizontal and one vertical dry-assembled: the **blind joint**, see [glossary](16-glossary.md#b). The screw head slides into a slot of the vertical, and you tighten it through the access hole in the opposite face.

**Parts:** none — dry run.

**Do:**

1. Dry-assemble one A and one B extrusion on the bench. [src](https://voron.link/onjwmcd)
2. Slide the bolt head into a channel from the vertical's open end, then reach the 3 mm key through the access hole opposite.

**Check:** You can see the bolt socket through the access hole and get the 3 mm key straight onto it.

Source: [Voron manual p.15](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=15) · [Voron manual p.10](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=10) · [blind-joint video](https://voron.link/onjwmcd) · [Video: Part 1 @0:54:58](https://www.youtube.com/watch?v=feTxcc0LIWM&list=PL0fUJbigELQPqpeGOgHYisG4KaSXVtnNY&t=3298s)

Pause: ~40 min since the last pause — extrusions sorted and labelled A–E, all end faces deburred, 16 M5×16 BHCS started finger-loose in eight A extrusions, and one blind joint dry-run understood. Nothing is assembled. The next segment is the long one — the frame goes from loose extrusions to squared-and-torqued in ~65 min and cannot safely be broken in the middle, so start it with the time to finish it.

---

### Step 01.6 — Lay out the bottom square on the reference surface

![Voron manual p.15](assets/manual-pages/manual-p015.png)

**What you're looking at:** Manual p.15 shows four A extrusions lying flat on the reference surface in a square, with a gap at each corner. The extrusions do not touch: each corner void is where a vertical drops in and joins the two horizontals.

**Parts:** 4× A extrusion (prepared, from Step 01.4).

**Do:**

1. Lay four A extrusions flat on the stone in a square, each end face pointing into a corner void. They do not touch each other.
2. Keep every part flat on the stone. Build here and nowhere else.

**Check:** All four extrusions lie dead flat with no gap under any of them. The four corner voids are square and roughly 20 × 20 mm.

Source: [Voron manual p.15](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=15) · [Video: Part 1 @0:53:47](https://www.youtube.com/watch?v=feTxcc0LIWM&list=PL0fUJbigELQPqpeGOgHYisG4KaSXVtnNY&t=3227s)

---

### Step 01.7 — Join the first vertical to the first corner

![Voron manual p.15](assets/manual-pages/manual-p015.png)

**What you're looking at:** Manual p.15 shows the first corner going together: one B extrusion standing in the void with its two **access holes** on the outward faces. The two horizontals occupy the vertical's inner faces, so only the outer pair can take a driver.

**Parts:** 1× B extrusion; engages 2 of the M5×16 BHCS already in the two A extrusions.

**Do:**

1. Stand a B extrusion in the first corner, **access holes facing outward**.
2. Slide it over the two bolt heads and push both A extrusions home.
3. Snug through each access hole with the 3 mm key. **Not tight.**

**Check:** Both A end faces sit flush against the vertical, its bottom is flush with theirs, and the corner sits flat on the stone.

Source: [Voron manual p.15](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=15)

---

### Step 01.8 — Add the remaining three verticals and close the bottom square

![Voron manual p.16](assets/manual-pages/manual-p016.png)

**What you're looking at:** Manual p.16 shows the other three verticals and the last two bottom horizontals, closing the base into a rectangle. Everything stays snug rather than tight so the assembly can still be nudged square before anything locks.

**Parts:** 3× B extrusion, 2× A extrusion (prepared); engages 6 more M5×16 BHCS.

**Do:** Repeat Step 01.7 at the other three corners, working around the frame, adding the last two bottom A extrusions as you go. Access holes outward every time. Snug only.

**Check:** Bottom square closed, four verticals standing, 8 of the 16 blind joints engaged. The assembly still sits flat on the stone with no rock.

Source: [Voron manual p.16](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=16)

---

### Step 01.9 — Snug and check the bottom square

![Voron manual p.16](assets/manual-pages/manual-p016.png)

**What you're looking at:** Manual p.16 shows the closed bottom square with the machinist square standing in each inside corner. A machinist square is a precision-ground right angle; you are looking for light between its blade and the extrusion.

**Parts:** none.

**Do:**

1. Press each corner down onto the stone.
2. Snug all 8 bottom bolts in a diagonal pattern: corner 1, corner 3, corner 2, corner 4.
3. Put the machinist square in each of the four inside corners.

**Check:** All four inside corners read 90° against the square with no light. All four extrusions still touch the stone along their whole length.

Source: [Voron manual p.16](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=16)

---

### Step 01.10 — Fit the four top A extrusions

![Voron manual p.17](assets/manual-pages/manual-p017.png)

**What you're looking at:** Manual p.17 shows the four remaining A extrusions dropping onto the tops of the verticals. Their screw heads enter the verticals' slots from the open top ends, which is why this half needs a second pair of hands.

**Parts:** 4× A extrusion (prepared); engages the remaining 8 M5×16 BHCS.

**Do:**

1. Drop the four remaining A extrusions onto the verticals, bolt heads entering the channels from the **top** open ends. Two people.
2. If one will not drop in, run its bolts in further; never spread the verticals. Snug only.

**Check:** All 16 blind joints are now engaged and the top square is closed. No end face has a visible gap.

Source: [Voron manual p.17](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=17)

---

### Step 01.11 — Snug the top square

![Voron manual p.17](assets/manual-pages/manual-p017.png)

**What you're looking at:** Manual p.17 shows the completed 2020 cube, all sixteen blind joints engaged. The second pass over every joint matters because the frame settles as it is assembled and the joints you snugged first are no longer snug.

**Parts:** none.

**Do:** Snug the 8 top bolts through their access holes, again in a diagonal pattern. Then go back over all 16 joints once at snug.

**Check:** All 16 joints are snug. The cube stands on its own and does not rack under a light hand push.

Source: [Voron manual p.17](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=17)

---

### Step 01.12 — Square the bottom square and lock it

![Voron manual p.21](assets/manual-pages/manual-p021.png)

**What you're looking at:** Manual p.21 shows the squareness check, measuring both plan diagonals of the bottom square. A rectangle whose two diagonals are equal is square. The absolute number does not matter, only that the pair agree, so hook the tape the same way both times.

**Parts:** none.

**Do:**

1. Measure both plan diagonals of the bottom square, outside face to outside face.
2. Tap the longer diagonal's corner inward with the mallet until the pair agrees.
3. Tighten the 8 bottom joints fully, diagonal pattern, then re-measure.

**Check:** Both diagonals equal, near **721 mm** on a 350, and all four corners 90°. Record the pair in the log. [src](https://voron.link/kdtpzam)

Source: [Voron manual p.21](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=21) · [frame squaring video](https://voron.link/kdtpzam)

---

### Step 01.13 — Square the top square and lock it

![Voron manual p.21](assets/manual-pages/manual-p021.png)

**What you're looking at:** Manual p.21 again, applied to the top square. Both squares can be individually square and still be rotated relative to each other. That is a twisted frame, and it shows up later as a gantry that will not sit parallel to the bed.

**Parts:** none.

**Do:**

1. Repeat on the top square: both diagonals, mallet.
2. Before the torque pass, sight down the four verticals for lean and square the top inside corners.
3. Tighten the 8 top joints fully in a diagonal pattern and re-measure.

**Check:** Top diagonals equal to each other and within a millimetre or so of the bottom pair.

Source: [Voron manual p.21](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=21)

---

### Step 01.14 — Check the four vertical faces

![Voron manual p.21](assets/manual-pages/manual-p021.png)

**What you're looking at:** Manual p.21 shows the four upright faces of the cube, each measured across its own diagonals. This is the check the first two cannot make: it catches a frame leaning over like a square-based prism rather than a rectangular box.

**Parts:** none.

**Do:**

1. Measure both diagonals on each of the four vertical faces and square their inside corners, top and bottom.
2. A face that will not come square means a joint not fully home: back it off, reseat it, re-tighten.

**Check:** Each face's two diagonals equal and every corner reads 90°. A 350 pair lands near **735 mm**, from 510 × 530 outside.

Source: [Voron manual p.21](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=21) · [Video: Part 1 @1:13:15](https://www.youtube.com/watch?v=feTxcc0LIWM&list=PL0fUJbigELQPqpeGOgHYisG4KaSXVtnNY&t=4395s)

---

### Step 01.15 — Check the frame sits without rock

![CAD render — the frame on the reference surface](assets/cad/01-15-a.png)

**What you're looking at:** The finished, torqued frame standing on the reference surface. All four bottom corners should touch at once; a frame that rocks between two diagonal corners is twisted. The render already shows the bed extrusions, so ignore them here.

**Parts:** none.

**Do:** Set the frame back on the stone and press each top corner in turn.

**Check:** No rock, no rattle, all four bottom corners in contact. A frame that rocks is twisted: go back to Step 01.13.

Torque note: the manual specifies **no** torque value for these M5 blind joints. Tighten firmly with the straight 3 mm hex key — not the ball end, which cams out under load. If you use the torque screwdriver, pick one setting and apply it identically to all 16 joints — consistency matters more here than any particular number. `(not specified — snug, then even)`

Tip: The CAD is the 250 mm machine — its frame is 370 mm horizontals on 430 mm verticals. Yours is the 350 set; the contact geometry is the same.

Source: [Voron manual p.21](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=21) · [Voron manual p.15](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=15) · CAD: Voron 2.4r2 STEP @ de7e89d

Pause: ~65 min since the last pause — the frame is assembled, squared on both squares and all four vertical faces, all 16 blind joints fully torqued, and it sits on the stone with no rock. This is the first genuinely safe stop in the chapter: a frame left snug-but-untorqued keeps whatever error was in it, so never walk away between squaring and the torque pass. Leave the frame on the reference surface, covered.

---

### Step 01.16 — Fit corner brackets to the two bed extrusions

![Voron manual p.18](assets/manual-pages/manual-p018.png)

**What you're looking at:** Manual p.18: the last two A extrusions with a **corner bracket** on each end. These *bed extrusions* are 470 mm and carry the build plate. They hang on their brackets between the front and rear rails, underside about level with the rail tops `(verify on bench)`.

**Parts:** 2× A extrusion (the last two), 4× corner bracket, 4× M5×16 BHCS.

**Do:**

1. Fit a gusseted corner bracket to each end of the two remaining A extrusions, one leg flat on the end face with an M5×16 BHCS into the centre bore.
2. Point the other leg down and outward. Snug only.

**Check:** 4 brackets, 4 bolts, all four free legs pointing down and outward, all four brackets oriented identically.

Source: [Voron manual p.18](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=18) · [Voron manual p.20](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=20) · [Video: Part 1 @1:29:21](https://www.youtube.com/watch?v=feTxcc0LIWM&list=PL0fUJbigELQPqpeGOgHYisG4KaSXVtnNY&t=5361s)

---

### Step 01.17 — Load four M5 T-nuts into the bottom rails

![Voron manual p.19](assets/manual-pages/manual-p019.png)

**What you're looking at:** Manual p.19 shows four M5 roll-in T-nuts dropped into the top slots of the two bottom rails. Each is the thread a bracket bolt picks up, loaded now and slid into position later.

**Parts:** 4× M5 T-nut (roll-in).

**Do:** Roll two M5 T-nuts into the top channel of the front bottom rail and two into the rear, one per bed-extrusion end. Leave them loose, roughly where the brackets will land.

**Check:** All four T-nuts rotate freely and sit flat. If one is tight, swap it or use the other channel face.

Source: [Voron manual p.19](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=19) · [LDO Build Notes (Rev D)](https://docs.ldomotors.com/voron/voron2/build-faq) · [Video: Part 1 @1:28:12](https://www.youtube.com/watch?v=feTxcc0LIWM&list=PL0fUJbigELQPqpeGOgHYisG4KaSXVtnNY&t=5292s)

---

### Step 01.18 — Set the bed extrusions and start the fasteners

![Voron manual p.19](assets/manual-pages/manual-p019.png)

**What you're looking at:** Manual p.19 shows both bed extrusions in the frame, each bracket leg on a rail over a T-nut, with an **M5 precision spacer** under each bolt head. The brass spacer is a controlled thickness that sets stack height, not a washer, see [glossary](16-glossary.md#p).

**Parts:** 2× bed extrusion (from Step 01.16), 4× M5×10 BHCS, 4× **M5 precision spacer**.

**Do:**

1. Set the bed extrusions **front-to-back**, bracket legs on the rails over T-nuts. Move the FRONT tape if parallel to the bed extrusions.
2. Drop a precision spacer on each hole and start an M5×10 BHCS into the T-nut, finger-loose.

**Check:** Four bolts started, four spacers seated, ends flush with the rails' inner faces, undersides about at the rails' top faces `(verify on bench)`.

⚠ Rev D+ / LDO: the manual calls this part an **"M5 Shim"** (p.19). This kit supplies a **brass M5 precision spacer** instead, for *every* M5 shim in the manual from here on. LDO: *"The brass M5 Precision Spacer are used in place of the M5 Shim. This will be for all M5 Shims in the guide unless noted."* [src](https://docs.ldomotors.com/en/voron/voron2/build-faq)

Source: [Voron manual p.19](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=19) · [LDO Build Notes (Rev D)](https://docs.ldomotors.com/voron/voron2/build-faq)

---

### Step 01.19 — Position the bed extrusions on the centreline

![Voron manual p.20](assets/manual-pages/manual-p020.png)

**What you're looking at:** Manual p.20 shows the two bed extrusions set symmetrically about the printer's centreline. Their spacing puts the build plate's mounting points where the plate's own holes are, so measure it at both ends of both extrusions.

**Parts:** none — positioning only.

**Do:**

1. Mark the centreline **255 mm** in from the left rail's outer face, front and rear.
2. Slide each bed extrusion until its inner face is **65 mm** from that line.
3. Tighten the four M5×10 bolts.

**Check:** **65 mm** each side of the centreline at both ends of both extrusions, four equal measurements, and both extrusions read **90°** to the rails.

Tip: p.20's dimension lines land on the facing inner faces: 130 mm clear, 150 mm centre to centre. If the bed's holes disagree later, trust the bed.

Source: [Voron manual p.20](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=20) · [Voron manual p.58](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=58) · [Video: Part 1 @1:46:36](https://www.youtube.com/watch?v=feTxcc0LIWM&list=PL0fUJbigELQPqpeGOgHYisG4KaSXVtnNY&t=6396s)

Pause: ~35 min since the last pause — both bed extrusions are bracketed, spaced with brass M5 precision spacers, set 65 mm each side of the centreline and their four M5×10 tightened. Nothing is half-fastened. Do not fit the titanium backers, and do not move the frame off the stone yet — Step 01.20 re-checks squareness there.

---

### Step 01.20 — Final squareness verification

![Voron manual p.21](assets/manual-pages/manual-p021.png)

**What you're looking at:** Manual p.21 one last time, on the fully torqued frame with the bed extrusions in. Bolting the bed extrusions in can pull a square frame out of square, so this is the pass whose numbers go in the log.

**Parts:** none.

**Do:** With everything torqued, walk the whole check once more: both bottom diagonals, both top diagonals, both diagonals on each of the four vertical faces, machinist square in every inside corner, frame flat on the stone.

**Check:** Every diagonal pair equal, every corner 90°, no rock. Anything you cannot null out here is permanent. [src](https://voron.link/kdtpzam)

Source: [Voron manual p.21](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=21) · [frame squaring video](https://voron.link/kdtpzam) · [Video: Part 5 @3:15:10](https://www.youtube.com/watch?v=hTKCBrk36R0&list=PL0fUJbigELQPqpeGOgHYisG4KaSXVtnNY&t=11710s)

---

### Step 01.21 — Titanium backers: not now

(no image — see text)

**What you're looking at:** The titanium extrusion backers, still bagged. A **backer** is a titanium strip bolted to the face opposite a linear rail; it cancels the bimetallic bow of steel rail on aluminium extrusion, see [glossary](16-glossary.md#b).

**Parts:** none — confirm the backers stay bagged.

**Do:** Check the titanium backers are still sealed and labelled for **Ch 05**. They are **not** frame parts and fit the gantry's X and Y extrusions, on the face opposite the rail.

**Check:** Backers bagged, labelled "Ch 05", stored with the C/D/E extrusions. [src](https://github.com/tanaes/whopping_Voron_mods/tree/main/extrusion_backers)

Source: [whopping_Voron_mods — `extrusion_backers`](https://github.com/tanaes/whopping_Voron_mods/tree/main/extrusion_backers) · [survey](../voron-build-instructions-survey.md)

---

### Step 01.22 — Record the frame log

(no image — see text)

**What you're looking at:** The finished frame, a tape measure and the log table. These numbers are the only baseline you will have when Ch 06 asks why the gantry will not square. "It looked fine" is not a measurement you can compare against.

**Parts:** none.

**Do:** Fill this in before the frame leaves the counter. Two people, two jobs: one measures and calls the number, one writes it down.

| Measurement | Target | Measured (mm) | By / date |
|---|---|---|---|
| Reference surface — worst feeler gap under the straightedge (Steps 00.10 / 01.1) | ≤ 0.1, no larger than the 00.10 figure | | |
| Bottom square, diagonal 1 | ≈721 (350) | | |
| Bottom square, diagonal 2 | = diagonal 1 | | |
| Top square, diagonal 1 | = bottom pair | | |
| Top square, diagonal 2 | = diagonal 1 | | |
| Front face, diagonals 1 / 2 | equal (≈735) | | |
| Rear face, diagonals 1 / 2 | equal (≈735) | | |
| Left face, diagonals 1 / 2 | equal (≈735) | | |
| Right face, diagonals 1 / 2 | equal (≈735) | | |
| Centreline to bed extrusion inner face — 4 places | 65 each | | |
| Clear gap between bed extrusions | 130 | | |
| Torque setting used, if any | one value, all 16 | | |

**Check:** Table filled, both diagonal pairs written down as numbers rather than "looked fine".

Source: [Voron manual p.21](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=21) · [survey](../voron-build-instructions-survey.md)

Pause: ~25 min since the last pause — final squareness pass done, backers confirmed still bagged for Ch 05, and the frame log table complete. Work through Checkpoint 01, then the frame can come off the counter.

---

## Checkpoint 01

- [ ] Reference surface re-checked with straightedge + feelers in five positions; worst gap no larger than the Step 00.10 figure
- [ ] 10 A, 4 B extrusions used; C ×2, D ×1, E ×1 bagged for Ch 05
- [ ] All extrusion end faces deburred and flat against the square
- [ ] 16 frame blind joints engaged and fully tightened, evenly
- [ ] Bottom square diagonals equal; top square diagonals equal and matching the bottom
- [ ] All four vertical faces: diagonals equal, corners 90°
- [ ] Frame sits on all four corners with no rock
- [ ] Every vertical's access holes face outward and take the straight 3 mm key face-on
- [ ] Two bed extrusions running front-to-back on the front and rear rails, corner brackets, **M5 precision spacers** (not shims), 90° to the rails; FRONT tape on one of the two faces their ends land on
- [ ] Bed extrusions 65 mm each side of the centreline, 130 mm clear gap, checked at both ends
- [ ] Titanium backers still bagged and labelled for Ch 05
- [ ] Frame log table filled in

## Common mistakes

- **Tightening as you go.** The frame must be assembled snug, squared, then torqued. Bolts taken to full torque corner by corner lock in whatever error was there at the time; the mallet cannot fix it afterwards.
- **Verticals installed with the access holes facing inward.** The two horizontals occupy the vertical's two inner faces, so the holes must face out. Caught late, this is a full corner disassembly — check it at Step 01.7 on the first corner and the rest follow.
- **Building on a "flat enough" table.** A surface with one corner a few tenths high becomes a twisted frame that reads square on every diagonal and still racks the gantry. Verify the surface (Step 00.10, re-checked at Step 01.1) or do not use it.
- **Using an M5 washer where the kit supplies a precision spacer.** The brass precision spacer is a controlled thickness, not a washer; the M5 shims in the manual are all replaced by it. Substituting a washer changes the stack height.
- **Forcing a roll-in T-nut.** LDO flags the tolerance explicitly. A forced T-nut galls the channel and the next one will not go in at all. Try another face or another nut.
- **Fitting the titanium backers to frame extrusions.** They are gantry parts and go on in Ch 05, on the face opposite the rail — putting a backer on the same face as an MGN12 makes bimetallic bowing worse, not better.

## Next

Ch 02 — Z drives, Z idlers, Z rails and deck panel (manual p.22–51); gated on batches **B00 + B01 + B02-P1 + B02-P3**. B00 and B02 printed before the kit; B01 has been running since Gate B on kit-day morning, so Ch 02 waits only on B01-P2 (22.8 h in all, print plan §2).
