# Chapter 03 — Build plate

Prepares the 355×355×10 mm heated plate and bolts it to the bed extrusions, so the frame has its datum surface and the bed harness is hanging below deck ready for Ch 10.

**What you're building in this chapter:** the heated bed, as a stack of four things. The **build plate** is a cast, ground aluminium slab with a mains-powered silicone **heater pad** and a 125 °C **thermal fuse** already bonded to its underside — both are factory-fitted on this kit, so two of the official manual's pages become inspections. On top of it you laminate the **magnetic pad**, an adhesive magnetised sheet, and onto that drops the **flex plate**: removable spring steel, the surface prints actually stick to and the reason you can pop a finished part off by flexing it. The whole stack sits on four **thumb-nut spacers** on the two bed extrusions from Ch 01, held by four bolts of which only one is ever tightened — the other three let a 355 mm aluminium plate expand as it heats instead of buckling. Nothing is wired here; the plate's three cables are left hanging below the deck for Ch 10.

**Time:** 1.5–2.5 h hands-on, first build (survey §7.2).

**Sessions:** 4 × ~30 min — the `Pause:` lines below break the chapter into 4 segments; every minute figure is a first-build estimate.

**Prerequisites:**

- **Ch 01 — Frame.** Squared, and the bed extrusions positioned with **65 mm from the centreline to each inner face** — a 130 mm clear gap, 150 mm centre-to-centre (manual p.20; Ch 01 Step 01.19).
- **Ch 02 — Z drives and idlers.** Deck panel and deck supports fitted (manual p.28–29); the wire opening in the deck must be clear and unobstructed.
- **Printed parts: none.** No print batch gates this chapter. The 2.4r2 mounts the plate straight onto the bed extrusions with metal hardware — there are no printed feet, bed mounts or spacers anywhere in p.52–61. The bed WAGO mount is supplied printed by LDO and is fitted in Ch 09, not here.

**Tools**

- Hex 2.5 mm and 3 mm
- Plastic scraper, squeegee or an old credit card (magnet application)
- Sharp craft knife with a fresh blade (trimming the magnet at the bolt holes; cutting the liner at Step 03.9)
- Masking tape (marking the back edge at Step 03.2; the hinge for the magnet at Step 03.9)
- Steel rule or straightedge ≥360 mm (flatness check and the 38 mm offset)
- Digital caliper

**Consumables:** IPA ≥90%, lint-free cloth, nitrile gloves. The plate's protective film goes in the bin.

**Printed parts**


| STL | Qty | Colour |
|---|---|---|
| — none — | 0 | — |

**Hardware** (chapter totals)

| Fastener / part | Qty | Note |
|---|---|---|
| Build plate, cast 5083 aluminium, Blanchard ground, 355×355×10 mm, LDO AC heatpad + 125 °C thermal fuse pre-applied | 1 | [LDO 350 Rev D BOM](https://docs.ldomotors.com/en/voron/voron2/350_BOM/Rev_D) |
| Magnetic Pad 2.4-350 | 1 | applied in this chapter |
| Spring Steel Flex Plate 2.4-350 | 1 | drops on, no fasteners |
| M3×20 SHCS | 4 | **not** the manual's M3×16 |
| M4 knurled thumb nut | 4 | used as the spacer, not as a nut |
| M3 roll-in T-nut, 2020 | 4 | bed extrusion top slots |
| M4×6 BHCS (bed PE) | 1 | already fitted to the plate — verify only, do not remove (washer: verify on bench) |
| M3×12 SHCS + M3 washer (thermal fuse) | 0 | manual p.56 hardware — **not used**, fuse is pre-installed |

**Read first**

- The heater pad (p.55) and the thermal fuse (p.56) are already on your plate. Both pages are **verify-only**. Do not peel, re-seat or re-bolt anything. [src](https://docs.ldomotors.com/voron/voron2/build-faq)
- Trim the magnet at the four bolt holes **immediately after** you roll it down and **before** you bolt anything. Discovering it at p.59 means peeling the magnet or drilling through it (survey §5.2 W6).
- Use **M3×20 SHCS**, not the manual's M3×16 — this plate and these spacers are thicker. [src](https://docs.ldomotors.com/voron/voron2/build-faq)
- The magnet goes on with the hinge method at Step 03.9 — one shot; read the whole step before you peel anything.
- Only one of the four bolts gets tightened (p.59). A bed clamped hard at all four corners while cold, then heated fast, tacos.
- No wiring happens here. The Omron SSR, the WAGO breakout, the bed PE run and the thermistor connection are all Ch 10. Leave the three bed cables loose below deck.

**Sources for this chapter:**

- [Voron 2.4r2 assembly manual (pinned `de7e89d`)](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf) pages 52–61 — plate orientation, magnet, bed-extrusion verification, spacers, the DON'T TIGHTEN rule
- [LDO Build Notes (Rev D)](https://docs.ldomotors.com/voron/voron2/build-faq) — p.55 and p.56 skipped (heater and fuse pre-applied), M4×6 PE screw, M3×20 instead of M3×16, trim the magnet now
- [LDO 350 Rev D BOM](https://docs.ldomotors.com/en/voron/voron2/350_BOM/Rev_D) — plate, magnetic pad, flex plate and thermal-fuse line items
- [LDO wiring guide § Wiring the Bed Heater](https://docs.ldomotors.com/en/voron/voron2/wiring_guide_rev_d#wiring-the-bed-heater) — where the three bed cables actually terminate (Ch 10)
- [magnet lamination demo](https://voron.link/rm6tpld) — the lamination demo the manual links from p.54
- [survey](../voron-build-instructions-survey.md) §5.2 W6
- The one mirrored image in this chapter (Step 03.4) is LDO Motors', used with attribution; see `assets/remote/03-build-plate/SOURCES.txt`. Its original URL stays on that step's `Source:` line.

**Video coverage (Steve Builds, pre-release LDO kit — differs from Rev D+):** [Part 1 @0:45:02](https://www.youtube.com/watch?v=feTxcc0LIWM&list=PL0fUJbigELQPqpeGOgHYisG4KaSXVtnNY&t=2702s) (+5m)

---

### Step 03.1 — Unpack the plate and read the end state

![Voron manual p.52](assets/manual-pages/manual-p052.png)

**What you're looking at:** Manual p.52 — the finished bed, and on the bench the three parts that make it. The **build plate** is a 355 × 355 × 10 mm cast aluminium slab with an AC heater pad already bonded underneath; the **magnetic pad** is an adhesive sheet you laminate to its top face; and the **flex plate** is the removable spring-steel sheet that snaps onto that magnet and is the surface prints actually stick to.

**Parts:** build plate ×1, magnetic pad ×1, spring steel flex plate ×1.

**Do:** Take the plate out flat, never on edge — a 355×355×10 mm cast slab will dent a corner if you drop it. Lay it on a clean towel on the bench. Note the target in the render: the plate sits on the two bed extrusions above the deck panel, with the cables dropping through the deck.

**Check:** Three cables leave the plate at the back-centre edge, and a small screw (the M4×6 PE screw; washer: verify on bench) sits near them. All present before you go further.

Source: [Voron manual p.52](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=52) · [LDO 350 Rev D BOM](https://docs.ldomotors.com/en/voron/voron2/350_BOM/Rev_D) · [Video: Part 1 @0:44:56](https://www.youtube.com/watch?v=feTxcc0LIWM&list=PL0fUJbigELQPqpeGOgHYisG4KaSXVtnNY&t=2696s)

---

### Step 03.2 — Work out which side is which

![Voron manual p.53](assets/manual-pages/manual-p053.png)

**What you're looking at:** Manual p.53 — the plate's two faces. The top is the one whose four corner holes are **counterbored**, a widened pocket that lets a bolt head sit below the surface so nothing stands proud under the flex plate; the bottom carries the heater, the thermal fuse and the earth screw.

**Parts:** build plate.

**Do:** Find the four corner mounting holes. The face where those holes are **counterbored** — so a bolt head sits flush or below the surface — is the **top**. The opposite face carries the heater, the thermal fuse and the tapped holes for the PE screw, and is the **bottom**. Mark the back edge (the edge the cables leave from) with a strip of masking tape.

**Check:** Drop an M3×20 SHCS into a corner hole from the top; the head sinks into the bore. From the other side it stands proud.

Source: [Voron manual p.53](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=53)

---

### Step 03.3 — Strip the protective film

![Voron manual p.54](assets/manual-pages/manual-p054.png)

**What you're looking at:** Manual p.54 — the ground top face under its protective film. The face is Blanchard-ground, which is the swirl pattern you will see; the film has been protecting it since the factory and has to come off before the magnet, because adhesive will not bond through it.

**Parts:** build plate.

**Do:** Peel the blue/clear protective film off the top face and bin it. Work from one corner; do not use a metal tool on the ground surface.

**Check:** No film left in the counterbores or under the edges. The ground surface is bare metal, matte, with visible Blanchard swirl.

⚠ **Rev D+ / LDO:** the manual never mentions the film — LDO adds this. Remove it now; the magnet will not bond through it. [src](https://docs.ldomotors.com/voron/voron2/build-faq)

Source: [Voron manual p.54](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=54) · [LDO Build Notes (Rev D)](https://docs.ldomotors.com/voron/voron2/build-faq)

---

### Step 03.4 — Verify the heater pad (do not apply one)

![Voron manual p.55](assets/manual-pages/manual-p055.png)
![LDO — build-plate underside, heater pad and thermal fuse pre-applied (Rev C guide photo: 300 mm / 220 VAC pad; your 350 pad differs)](assets/remote/03-build-plate/build_plate_bottom_view.jpg)

**What you're looking at:** Manual p.55 shows the official manual *applying* a heater pad — a page you skip. The LDO photo beside it is what your plate actually looks like from below: the silicone AC pad already bonded and screwed down, the thermal-fuse patch, and the cable exit. (LDO's photo is the Rev C guide's 300 mm / 220 VAC pad; your 350 kit's pad is a different part number and its label reads differently — the layout is what to compare, not the ratings.)

**Parts:** none.

**Do:** Turn the plate bottom-up. Confirm the AC heatpad is bonded flat and centred, with no lifted corner, no wrinkle and no trapped air. No bubble size is specified anywhere — judge it against "flat and fully bonded", and raise anything you are unsure about in `#ldo_motors`. Confirm every pad screw is present. Do not tighten them — LDO's label on the pad says not to (verify screw head type on bench; the 350 pad may differ from the photo). Do not add adhesive and do not re-press a lifted edge with heat.

**Check:** Pad flat and centred; every pad screw present and untouched; nothing peeling at the cable exit.

⚠ **Rev D+ / LDO:** **SKIP manual p.55 entirely** — the heater pad is pre-applied on Rev C and later kits. This step is inspection only. If the pad is genuinely lifting, stop and raise it in `#ldo_motors` before you bolt the plate in. [src](https://docs.ldomotors.com/voron/voron2/build-faq) · [wiring guide § Wiring the Bed Heater](https://docs.ldomotors.com/en/voron/voron2/wiring_guide_rev_d#wiring-the-bed-heater)

Source: [Voron manual p.55](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=55) · [LDO Build Notes (Rev D)](https://docs.ldomotors.com/voron/voron2/build-faq) · [LDO wiring guide § Wiring the Bed Heater](https://docs.ldomotors.com/en/voron/voron2/wiring_guide_rev_d#wiring-the-bed-heater) · [image: LDO `build_plate_bottom_view.jpg`](https://raw.githubusercontent.com/MotorDynamicsLab/LDOVoron2/main/Images/WiringGuide/RevC/build_plate_bottom_view.jpg)

---

### Step 03.5 — Verify the thermal fuse (do not fit one)

![Voron manual p.56](assets/manual-pages/manual-p056.png)

**What you're looking at:** Manual p.56 shows the official fuse installation, also a page you skip. The **thermal fuse** is a one-shot cut-out that opens permanently at 125 °C and is wired in series with one heater lead, so a runaway heater loses its supply whatever the firmware is doing ([glossary](16-glossary.md#t)). It only works if its body is pressed flat against the aluminium — which is what you are checking.

**Parts:** none. The manual's M3×12 SHCS and M3 washer stay in the bag.

**Do:** Find the 125 °C thermal fuse on the bottom face, near the cable exit, clamped to the plate by a single screw and washer. Confirm the fuse body is pressed flat against the aluminium — it only protects you if it is thermally coupled to the plate. Confirm it is wired in-line with one heater lead, and that its screw is tight.

**Check:** Fuse flat to the plate, screw tight, no strain on either leg of the fuse where it joins the heater wire.

⚠ **Rev D+ / LDO:** **SKIP manual p.56 entirely** — the fuse is pre-installed. Inspect only. [src](https://docs.ldomotors.com/voron/voron2/build-faq)

Source: [Voron manual p.56](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=56) · [LDO Build Notes (Rev D)](https://docs.ldomotors.com/voron/voron2/build-faq)

---

### Step 03.6 — Verify the PE screw and identify the three cables

![Voron manual p.57](assets/manual-pages/manual-p057.png)

**What you're looking at:** Manual p.57 — the plate's cable exit. Three cables leave here: two thick braided AC leads (**N** and **Bed L**) that carry mains to the heater, and one thin two-pin **BED TH** cable, the thermistor the firmware reads the bed temperature from. Beside them is the **protective-earth** screw — an M4×6 BHCS that bonds the plate to earth ([glossary](16-glossary.md#p)); whether it carries a serrated washer is not in LDO's note (verify on bench).

**Parts:** none — the PE screw is already fitted.

**Do:** Identify the three cables leaving the back edge: two thick braided AC leads labelled **N** and **Bed L**, and one thin two-pin cable labelled **BED TH** (the ATC Semitec 104NT bed thermistor). Find the **M4×6 BHCS** threaded into the plate beside them — that is the bed PE point (washer: verify on bench). Leave it in place; back it off later only when you land the PE ring terminal in Ch 10.

**Check:** Three labelled cables, no chafe or cut in the braid, no exposed conductor. PE screw present, snug.

⚠ **Rev D+ / LDO:** the manual calls for an M3×6 BHCS you supply. Your plate ships with an **M4×6 BHCS** already attached — use that one. [src](https://docs.ldomotors.com/voron/voron2/build-faq)

⚠ **Rev D+ / LDO:** do **not** wire the PE, the heater leads or the thermistor here. The bed harness is a breakout design: the AC leads land on the bed WAGO mount and the SSR, and the thermistor on the 2×2 XH splicer PCB, all in Ch 10. [src](https://docs.ldomotors.com/en/voron/voron2/wiring_guide_rev_d#wiring-the-bed-heater)

Source: [Voron manual p.57](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=57) · [LDO Build Notes (Rev D)](https://docs.ldomotors.com/voron/voron2/build-faq) · [LDO wiring guide § Wiring the Bed Heater](https://docs.ldomotors.com/en/voron/voron2/wiring_guide_rev_d#wiring-the-bed-heater)

Pause: ~30 min since the last pause — the plate is unpacked and identified top from bottom, the film is off, and the pre-applied heater, thermal fuse and PE screw are all inspected and left alone. The magnet is still in its backing. Do not start Step 03.9 until you can run 03.8–03.10 straight through: the magnet is a one-shot lamination.

---

### Step 03.7 — Check the plate for flatness before the magnet goes on

![Voron manual p.53](assets/manual-pages/manual-p053.png)

**What you're looking at:** The bare ground face and a straightedge. This is the last moment the aluminium is visible; once the magnet is on, a dish or crown in the plate can only be inferred from a bed mesh, and neither mesh nor quad gantry level can correct a plate that is not flat in itself.

**Parts:** build plate, steel rule or straightedge.

**Do:** Stand the straightedge on edge on the ground face and sight against a light: one diagonal and one centreline, two minutes. Do this now — once the magnet is on you cannot inspect the ground surface again.

**Check:** No daylight under the straightedge. Voron and LDO publish **no flatness tolerance (not specified)** for this plate; only a gap you can slide a sheet of paper under is worth raising in `#ldo_motors` before you build on it — a Blanchard-ground 10 mm cast plate is not going to be dished.

Tip: a cast, Blanchard-ground 5083 plate is deliberately thick and stress-relieved; a visible dish here does not get corrected by mesh or QGL later. [src](https://docs.ldomotors.com/en/voron/voron2/350_BOM/Rev_D)

Source: [Voron manual p.53](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=53) · [LDO 350 Rev D BOM](https://docs.ldomotors.com/en/voron/voron2/350_BOM/Rev_D)

---

### Step 03.8 — Clean the top face

![Voron manual p.54](assets/manual-pages/manual-p054.png)

**What you're looking at:** The top face, IPA and a lint-free cloth. Anything left on the surface — oil, dust, a fingerprint — becomes a permanent bump under an adhesive sheet you cannot lift again.

**Parts:** build plate; IPA, lint-free cloth, gloves.

**Do:** Wipe the whole top face with IPA and let it flash off completely, so no solvent is trapped under the adhesive. Wear gloves from here on — a fingerprint under the magnet is a permanent bump.

**Check:** Surface dry, no lint, no residue in the counterbores.

Source: [Voron manual p.54](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=54)

---

### Step 03.9 — Apply the magnet sheet

![Voron manual p.54](assets/manual-pages/manual-p054.png)

**What you're looking at:** Manual p.54 and the magnetic pad. It is a flexible sheet of magnetised rubber with a pressure-sensitive adhesive back under a liner; laminated to the plate it becomes the thing that holds the spring-steel flex plate down. On this kit it is a separate BOM line, not factory-applied, so this lamination is yours to get right first time (one shot — read the whole step first).

**Parts:** Magnetic Pad 2.4-350 ×1; masking tape; plastic squeegee or card; knife or scissors for the liner.

**Do:** Measure the pad against the plate before peeling anything (verify on bench — LDO publishes no drawing): same 355 mm as the plate → it goes edge-flush to the **back** edge and one side; smaller → centre it and write the border down. The liner side is the adhesive; the plain rubber face is the magnet. The four bolt holes are not pre-cut (that is Step 03.10). Hinge it: with the liner on, lay the pad exactly where it goes and tape it along the back edge with two strips of masking tape running from the pad's top face over the plate's side — that tape is the hinge. Fold the pad back over the hinge, peel 40–50 mm of liner at the hinged edge and cut it off, lay that strip down and squeegee it. Then pull the liner out underneath while squeegeeing from the hinge toward you, ~50 mm per stroke, keeping the unlaid pad lifted so adhesive never touches ahead of the squeegee. Remove the hinge tape and press the whole sheet with a card edge or roller (p.54) — the bond is pressure-activated. If the first strip lands crooked, lift it **immediately** — once more than a few cm are down it will not reposition. Watch the manual's linked demo first if you have never laminated an adhesive sheet: [https://voron.link/rm6tpld](https://voron.link/rm6tpld) (manual p.54).

**Check:** No bubbles, no wrinkles, the border you wrote down (or flush edges) all round, pad square to the plate edges. Bubbles pushed to an edge can still be worked out; ones in the middle cannot.

⚠ **Rev D+ / LDO:** the magnetic pad is a **separate line item** in the 350 Rev D BOM — it is not laminated at the factory, unlike the heater and fuse. If your plate did arrive with the magnet already on, skip to 03.10 and check whether the four bolt holes are already cut. [src](https://docs.ldomotors.com/en/voron/voron2/350_BOM/Rev_D)

Source: [Voron manual p.54](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=54) · [LDO 350 Rev D BOM](https://docs.ldomotors.com/en/voron/voron2/350_BOM/Rev_D) · [magnet lamination demo](https://voron.link/rm6tpld)

---

### Step 03.10 — Trim the magnet at the four bolt holes

![Voron manual p.54](assets/manual-pages/manual-p054.png)

**What you're looking at:** The laminated magnet with four dimples where the plate's counterbored corner holes are underneath. The mounting bolts have to pass through those holes and a hex key has to reach their heads, so the magnet is cut away over each one — now, while the bolts are still in their bag.

**Parts:** Magnetic pad (applied), sharp craft knife.

**Do:** Locate the four counterbored corner holes under the magnet — press down and they show as dimples. Cut the magnet away over each one, following the bore, so the M3×20 head and a 2.5 mm hex key both drop in cleanly. Cut with light repeated passes; do not gouge the aluminium, because a burr in a counterbore stops the bolt head sitting flush.

**Check:** All four bores fully open. Test each with an M3×20 SHCS and the hex key before you go anywhere near the frame.

⚠ **Rev D+ / LDO:** LDO's note at p.54 exists because the magnet gets applied here and the bolts do not go in until p.59. Trimming now costs two minutes; discovering it at p.59 costs the magnet (survey §5.2 W6). [src](https://docs.ldomotors.com/voron/voron2/build-faq)

Source: [Voron manual p.54](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=54) · [LDO Build Notes (Rev D)](https://docs.ldomotors.com/voron/voron2/build-faq)

Pause: ~30 min since the last pause — the top face is cleaned, the magnet is rolled down bubble-free and all four bolt holes are cut clear through it and test-fitted with an M3×20 and a hex key. The lamination is finished, so nothing is mid-adhesive. Lay the plate flat, magnet up, and cover it.

---

### Step 03.11 — Verify the bed extrusion position

![Voron manual p.58](assets/manual-pages/manual-p058.png)

**What you're looking at:** Manual p.58 — the front elevation of the frame with the bed extrusions in it. You are re-checking Ch 01's placement because those two extrusions carry the plate's four mounting points; if they are not where the plate's holes are, the plate cannot sit down evenly on its spacers. (p.58 also carries a bare "25" on the verticals; what it dimensions is not identified, and nothing in this chapter depends on it.)

**Parts:** none — measurement only.

**Do:** With the printer upright, measure the two bed extrusions: **130 mm of clear space between their facing inner faces**, centred on the printer centreline, i.e. 65 mm from the centreline to each inner face (manual p.20 — the dimension lines land on the inner faces, so the centres are 150 mm apart). Measure at both ends of the extrusions — a difference between the ends shows up later as a plate that will not sit down on all four spacers.

**Check:** 130 mm clear gap between the facing inner faces (= 150 mm centre-to-centre), 65 mm from the centreline to each inner face, the same at both ends.

Source: [Voron manual p.58](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=58) · [Voron manual p.20](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=20)

---

### Step 03.12 — Load the four M3 T-nuts

![Voron manual p.58](assets/manual-pages/manual-p058.png)

**What you're looking at:** Manual p.58 — four M3 roll-in T-nuts in the top slots of the bed extrusions, two per extrusion. Each is the thread one corner bolt picks up.

**Parts:** M3 roll-in T-nut, 2020 ×4 (two per bed extrusion).

**Do:** Roll two T-nuts into the **top** slot of each bed extrusion, one toward each end, and position them roughly under where the plate's corner holes will land. Leave them loose enough to slide.

**Check:** Four T-nuts, all in the top slot, all rotated so their threads face up and they cannot fall out.

⚠ **Rev D+ / LDO:** extrusion and roll-in T-nut tolerances on this kit are tight. Test-fit each nut and, if a slot is stiff, pick the extrusion face that accepts it best — do not force one and gall the slot. [src](https://docs.ldomotors.com/voron/voron2/build-faq)

Source: [Voron manual p.58](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=58) · [LDO Build Notes (Rev D)](https://docs.ldomotors.com/voron/voron2/build-faq)

---

### Step 03.13 — Fit the four thumb nuts as spacers

![Voron manual p.58](assets/manual-pages/manual-p058.png)

**What you're looking at:** Manual p.58 — four knurled **thumb nuts**, used here as spacers rather than as nuts. They hold the plate a fixed height above the extrusion so the bolt is the only contact; the bolt passes straight through the thumb nut's bore and threads into the T-nut below ([glossary](16-glossary.md#t)).

**Parts:** M4 knurled thumb nut ×4.

**Do:** Stand one M4 thumb nut over each T-nut, knurl up, so it sits on the extrusion face with its bore concentric with the T-nut thread. These are used purely as heat-resistant spacers — the M3 bolt passes straight through the M4 bore and threads into the T-nut below. Do not thread anything into the thumb nut.

**Check:** Four thumb nuts standing on the extrusions, none tipped over, each aligned with the T-nut under it. All four the same height — if you substitute other spacers they must be the same length and heat-resistant (p.58).

Source: [Voron manual p.58](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=58)

---

### Step 03.14 — Lower the plate on and feed the cables through the deck

![Voron manual p.60](assets/manual-pages/manual-p060.png)

**What you're looking at:** Manual p.60 — the plate coming down onto its four spacers, cables first. The three cables have to go through the deck opening before the plate lands, because once the plate is on them there is no way to feed them through without lifting it again.

**Parts:** build plate assembly.

**Do:** Two hands, plate flat, magnet up, cables at the **back**. Feed the two AC leads and the thermistor cable down through the opening in the deck panel first, then lower the plate onto the four thumb nuts. Keep the cables clear of the plate edge as it comes down so nothing gets pinched.

**Check:** Plate rests on all four thumb nuts with none knocked over. All three cables hang free below the deck with slack. No cable trapped between the plate and an extrusion.

Source: [Voron manual p.60](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=60) · [Video: Part 2 @1:36:04](https://www.youtube.com/watch?v=2U0YahE8w_0&list=PL0fUJbigELQPqpeGOgHYisG4KaSXVtnNY&t=5764s)

---

### Step 03.15 — Start the four bolts

![Voron manual p.59](assets/manual-pages/manual-p059.png)

**What you're looking at:** Manual p.59 — the four M3×20 bolts. They are longer than the official manual's M3×16 because this plate is 10 mm thick and sits on a spacer; started by hand first so the T-nuts can still be nudged along the slot to meet each hole.

**Parts:** M3×20 SHCS ×4.

**Do:** Drop an M3×20 SHCS through each trimmed corner hole, through the thumb nut, and start it into the T-nut below. Get all four started by hand before driving any of them — the T-nuts still need to slide to meet the holes. Nudge a T-nut along the slot with a hex key if a bolt will not pick up the thread. Run all four down until they just take up, no more.

**Check:** All four bolts engaged and turning freely, plate still sitting flat on the spacers, no bolt cross-threaded.

⚠ **Rev D+ / LDO:** **M3×20 SHCS, not the manual's M3×16.** This plate is 10 mm and the spacer stack is taller, so an M3×16 will not reach enough thread. [src](https://docs.ldomotors.com/voron/voron2/build-faq)

Source: [Voron manual p.59](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=59) · [LDO Build Notes (Rev D)](https://docs.ldomotors.com/voron/voron2/build-faq)

---

### Step 03.16 — Set the 38 mm front offset and centre the plate

![Voron manual p.60](assets/manual-pages/manual-p060.png)

**What you're looking at:** Manual p.60 — the plate's position in plan. The 38 mm setback puts the plate where the toolhead can reach all of it, and equal side gaps keep it clear of the vertical extrusions and Z rails, which is tight because a 355 mm plate is in a 350 mm machine.

**Parts:** steel rule / caliper.

**Do:** With the bolts still loose, slide the plate front-to-back until its front edge sits **38 mm behind the front edge of the frame** (p.60). Then check the left and right gaps between the plate edge and the vertical extrusions and split any difference evenly. Re-check the 38 mm after the sideways move. No tolerance is specified for either dimension — make the two sides read the same on the caliper. The plate is 355 mm in a 350 machine, so run a finger right round the perimeter afterwards; the clearances are small.

**Check:** 38 mm at both the front-left and front-right corners, left and right gaps equal, and nothing on the plate touching a vertical extrusion or a Z rail.

Source: [Voron manual p.60](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=60)

---

### Step 03.17 — Tighten one bolt only

![Voron manual p.59](assets/manual-pages/manual-p059.png)

**What you're looking at:** Manual p.59 and its **DON'T TIGHTEN** rule. One bolt locates the plate; the other three are deliberately left loose so the aluminium can grow as it heats — clamped hard at all four corners and taken to 110 °C, a plate this size buckles and never comes flat again.

**Parts:** the four M3×20 SHCS already fitted.

**Do:** Pick one corner (the manual names none — any works; a front corner keeps the tightened bolt away from the cable exit at the back) and tighten that bolt fully. **Leave the other three slightly loose.** They locate the plate; they must not clamp it. Torque is **not specified** by the manual: snug the one bolt by hand feel with a short hex key, no torque driver.

**Check:** One bolt tight. The other three can be turned with a fingertip on the hex key. Push the plate laterally at a free corner — it should give slightly and return, neither slide freely nor feel locked solid.

⚠ **Rev D+ / LDO:** none — the manual's DON'T TIGHTEN rule stands unchanged (p.59). Aluminium at 110 °C grows against a steel-bolted frame; three loose bolts are what lets it grow.

Source: [Voron manual p.59](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=59)

Pause: ~35 min since the last pause — the plate is on its four thumb-nut spacers, set 38 mm behind the frame's front edge and centred, one bolt tight and three deliberately loose, cables fed through the deck. This is the natural stop: the plate is bolted and the assembly is stable. Do not tighten the other three bolts.

---

### Step 03.18 — Verify the plate floats level

![CAD render — the four gaps that have to match](assets/cad/03-18-a.png)
![CAD render — the four gaps that have to match, in place](assets/cad/03-18-b.png)

**What you're looking at:** The four corners and a caliper. You are proving the plate is sitting on all four spacers and not on a tipped thumb nut or a half-rolled T-nut — a short corner here is a permanent tilt every bed mesh afterwards has to fight. The build plate riding on four bolts above the two bed extrusions that span the frame — the gap under each bolt is what you measure, and all four should be the same.

**Parts:** caliper.

**Do:** Measure the gap between the top face of the bed extrusion and the underside of the plate at each of the four bolts. Then sight along the plate from the front of the frame at eye level, and again from the side. A short corner means a T-nut is not fully rolled in, a thumb nut is tipped, or that bolt got tightened.

**Check:** All four gaps equal to the thumb-nut height and to each other; press each corner in turn — no rock, no click.

Tip: do not try to level the plate to the gantry mechanically. Quad gantry level does that in software in Ch 13; this step only proves the plate floats evenly on its four spacers.

Tip: The CAD bed is the 10 in (254 mm) MIC6 plate on 370 mm bed extrusions (250). Yours is the 350 plate on the 350 frame — still four bolts, four gaps.

Source: [Voron manual p.59](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=59) · [Voron manual p.58](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=58) · CAD: Voron 2.4r2 STEP @ de7e89d

---

### Step 03.19 — Dress the bed harness below deck

![Voron manual p.60](assets/manual-pages/manual-p060.png)

**What you're looking at:** Manual p.60 — the three bed cables below the deck, loose. Nothing is terminated in this chapter: the AC pair goes to the relay and the WAGO bus, and the thermistor to a splicer PCB, all in Ch 10 after those parts are actually mounted.

**Parts:** none — no zip ties yet.

**Do:** Below the deck, separate the two AC leads from the thin thermistor cable and lay them along the route they will take toward the electronics bay, leaving generous slack at the plate end. Make sure nothing bears on the sharp edge of the deck opening, nothing is pulled taut against the plate's cable exit, and nothing rests on a bed extrusion where the plate can pinch it. Leave the ends free and unterminated.

**Check:** Slack loop at the plate; no cable under tension; no cable touching a cut edge; the thermal fuse's legs undisturbed. Nothing tied down.

⚠ **Rev D+ / LDO:** do not zip-tie or terminate anything yet. The bed harness is a breakout design specifically so the plate can be removed from the top of the deck panel later; final routing, the WAGO terminals, the 2×2 XH splicer and the Omron SSR are all Ch 10. [src](https://docs.ldomotors.com/en/voron/voron2/wiring_guide_rev_d#wiring-the-bed-heater)

Source: [Voron manual p.60](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=60) · [LDO wiring guide § Wiring the Bed Heater](https://docs.ldomotors.com/en/voron/voron2/wiring_guide_rev_d#wiring-the-bed-heater)

---

### Step 03.20 — Fit the flex plate, then cover the bed

![Voron manual p.61](assets/manual-pages/manual-p061.png)

**What you're looking at:** Manual p.61 — the **flex plate**, the removable spring-steel print surface that clicks onto the magnet ([glossary](16-glossary.md#f)). It goes on once to prove it sits flat, then straight back in its sleeve: the six chapters above this surface drop hex keys, swarf and threadlocker, and the magnet is not something you can resurface.

**Parts:** Spring Steel Flex Plate 2.4-350 ×1.

**Do:** Drop the spring steel flex plate onto the magnet, coated side up, square to the plate edges — no fasteners. Then take it straight back off, put it back in its sleeve, and lay a sheet of cardboard over the magnet. The gantry, A/B drives and all the belt work happen directly above this surface for the next six chapters, and dropped hex keys, swarf and threadlocker all land here.

**Check:** Flex plate sits flat with no rocking and does not overhang the magnet on any side. Bed covered.

⚠ **Rev D+ / LDO:** the flex plate is an LDO kit item; the official manual's PRINT BED section ends at p.60 and p.61 carries no build content. [src](https://docs.ldomotors.com/en/voron/voron2/350_BOM/Rev_D)

Source: [Voron manual p.61](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=61) · [LDO 350 Rev D BOM](https://docs.ldomotors.com/en/voron/voron2/350_BOM/Rev_D)

Pause: ~20 min since the last pause — the four-corner gap check is done, the bed harness is dressed loose below deck with nothing tied or terminated, and the flex plate has been test-fitted, removed and the bed covered with cardboard. Work through Checkpoint 03; the cover stays on for the next six chapters.

---

## Checkpoint 03

- [ ] Protective film removed; top face clean, magnet applied with no bubbles or wrinkles.
- [ ] All four bolt holes trimmed clear through the magnet; a 2.5 mm hex key reaches each bolt head.
- [ ] Heater pad flat and centred, pad screws present and untouched — inspected, not re-applied.
- [ ] Thermal fuse flat against the plate, screw tight, in-line with a heater lead — inspected, not re-fitted.
- [ ] M4×6 BHCS present on the plate as the PE point (washer: verify on bench); nothing wired to it.
- [ ] Four M3 roll-in T-nuts in the bed extrusion top slots; four M4 thumb nuts standing as spacers.
- [ ] Four **M3×20** SHCS fitted (not M3×16); **one** tightened, three deliberately loose.
- [ ] Front edge of the plate 38 mm behind the front edge of the frame, both corners.
- [ ] Equal gap under all four corners; no rock; plate clear of every vertical extrusion and Z rail.
- [ ] Straightedge check done before the magnet went on — no gap you could slide paper under.
- [ ] Three bed cables hanging free below the deck with slack, unterminated, nothing pinched or tied.
- [ ] Flex plate test-fitted, removed, and the bed covered for the rest of the build.

## Common mistakes

- **Applying the magnet over untrimmed bolt holes and only noticing at p.59.** The fix is a peel-and-replace magnet or drilling through it — both bad. Trim at 03.10.
- **Using the M3×16 the manual calls for.** It engages barely any thread through a 10 mm plate plus spacer, and strips the T-nut on first tighten. M3×20.
- **Tightening all four bolts because three loose bolts feel wrong.** The plate tacos on the first fast heat-up to 110 °C and never comes flat again.
- **Trying to "fix" the pre-applied heater or fuse.** Peeling a bonded AC heatpad to re-seat it wrecks it. Inspect and ask in `#ldo_motors` if something looks wrong.
- **Wiring the bed here.** The PE, heater leads and thermistor all terminate in Ch 10 after the SSR and WAGOs are mounted. Landing them now means undoing them.
- **Building on the bare magnet, or leaving the surface exposed.** The magnet sheet is not a print surface, and everything you drop for the next six chapters lands on it.

## Next

Ch 04 — A/B drives and idlers (manual p.62–81): the two gantry drive units and the front idlers, built on the bench with the bed covered.
