# G9: Rev D+ re-pin diff (uncommitted, against HEAD cb088cf5)

- **Group:** G9. Scope: everything in `git diff HEAD` (22 files): `scripts/kit_bom.py`, `scripts/data/ldo-350-bom.yml`, `scripts/data/hardware-ownership.yml`, `sources.yml`, `docs/manual/CONVENTIONS.md`, Ch 00, 00-tonight, 01, 02, 03, 04, 06, 07, 08, 09, 10, 11, 12, `print/B01`, `docs/print/checklists.md`, and the generated `tonight.json` / `build-progress.json`. I also grepped all of `docs/` for SD-card, grounding, question-count and Rev D label leftovers.
- **Primary sources:**
  - LDO pages fetched live 2026-10-30 into my own temp dir: `350_BOM/Rev_D+` (page created 2026-06-08), `350_BOM/Rev_D`, `350_BOM/HOME` (updated 2026-09-21), `/en/voron/voron2`, `/faq`, `/kit-errata`, `Toolboard/nitehawk-sb-v2` (updated 2026-07-10). The `*_rev_d_plus` guide URLs return 404.
  - Both D and D+ BOMs parsed with the repo's own `kit_bom.parse` and diffed row by row against the yml.
  - West3D and DREMC seal listings (`.json` plus all 6 images).
  - Fabreeko product JSON (saved 2026-10-30).
  - Voron CAD index `~/.cache/voron-cad/cache/index.json`: bbox queries at all 16 joints.
  - Voron manual p.15 (via Ch 01's crops and text).
  - `scripts/parts.py --ledger` (read-only; `git status` hash unchanged before and after).
- **Images opened:** 13. LDO seal drawings `p.png`, West3D w1/w2/w3, DREMC d1/d3, plus two enlarged crops of the junction; Nitehawk-SB-V2 `grounding_scheme.jpg` (08 and 10 mirrors), `toolboard_ground_routing.jpg`, `usb_adapter_gnd.jpg`, and Ch 09's `usb-adapter-grounding.jpg`.

---

### G9-01 major goal 1/2: Step 01.23 puts the seals in the wrong extrusion; LDO's own drawing puts them in the *vertical's* slot, and the step's slot seals nothing

**Where:**
- `docs/manual/01-frame.md:591–592`: "press a seal into the **horizontal's inward-facing slot** … Slide it until it stops against the vertical."
- The same placement is repeated at `:50` (Hardware "16 joints' inward slot ends"), `:583` ("Where a horizontal's slot ends against a vertical it leaves an open channel to the outside"), `:595` (Check), `:599` ("LDO's guides do not place them"), `:623` (Checkpoint), and `docs/print/checklists.md:56`.

**Evidence:**
- **LDO's drawing.** The illustration is on both cited listings (West3D image 2/3; DREMC `p.png` and the `…ebjs-9181133.png` top view). It shows the rubber T-plug with its body **inside the vertical's slot**, the slot that the horizontal butts into. The seal rests against the horizontal on the open, chamber side (in the drawing, a bottom joint, so the seal sits above it). Its small square boss pokes into the end of the horizontal's slot.
  - In the top view, the seal's T cross-section sits in the vertical's profile.
  - The horizontal's own top-slot channel is empty right up to the joint.
  - The listing text says: "insert one side first, then press the other side in. Finally, slide it along the extrusion slot until it reaches the end." Here "the slot" is the vertical's and "the end" is where it meets the horizontal.
  - Confidence: high on the location, because the two views agree. Medium on "chamber side" at the **top** joints (below the horizontal), because LDO draws only one joint.
- **Geometry.** A horizontal's end is centred on the vertical's face, and the vertical's 6 mm slot opening is a vertical strip down the middle of that face.
  - The horizontal's *side* slots (inward or outward) end against the vertical's solid flanges. An inward slot is therefore a dead end inside the chamber, and a plug there seals nothing.
  - Only the horizontal's top and bottom slot ends line up with the vertical's slot channel. That channel runs past the joint to the vertical's open end, behind the bolt head, and it is the leak path LDO plugs.
- **"Inward-facing" is ambiguous at all 16 joints.** On a bottom horizontal it can mean the top slot (facing into the chamber) or the inner side slot (facing the machine centre).
- **Nothing later needs the vertical-slot location free** (CAD 250, same corner parts on the 350):
  - Every T-nut in this kit is roll-in or hammerhead, so none has to enter from a slot end.
  - The Z rail sits on the very face where the four bottom side-horizontal joints are. Its lowest M3 T-nut starts 8.6 mm above the bottom horizontal; the rail itself starts 3 mm above (Step 02.06).
  - The Z belt cover's hammerhead in the bottom front/rear rail's top slot starts 5.4 mm from the vertical. LDO's boss enters that slot end by roughly 2–3 mm, judged from the drawing.
  - Both should clear, but LDO publishes no seal dimensions: `(verify on bench)`.
- **Ordering.** At those four bottom side-horizontal joints the Z rail covers the slot from 3 mm up once Step 02.06 is done. After that a seal cannot be rolled in, so **01.23's position (end of Ch 01, before Ch 02) is right and in fact required**. The step should say why.
- **Missing image.** The step says "(no image — see text)", yet LDO's drawing exists and is the only thing that shows the placement.

**Proposed fix** (step ID, count and Pause unchanged):
- **Image:** mirror DREMC `p.png` (iso view) and the top view into `assets/remote/01-frame/` with attribution. First check that Alex's LDO image ruling covers LDO renders hosted on reseller stores.
- **What you're looking at:** "The frame's 16 blind joints. The vertical's slot that each horizontal butts into runs on past the joint to the vertical's open end, and the horizontal's own top and bottom slots open into it: that channel is the leak. LDO's seal is a short rubber T-plug that sits in that vertical slot hard against the horizontal, its square boss in the end of the horizontal's slot (drawing)."
- **Do:**
  1. Work on the chamber side of each joint: above a bottom horizontal, below a top horizontal.
  2. Tip one edge of a seal into the vertical's slot that faces the horizontal, boss toward the horizontal, then press the other edge in, like a roll-in T-nut.
  3. Slide it along the vertical until the boss drops into the horizontal's slot end and it stops. Do all 16. *(Then Alex's call on the last four: spares in bin `01-…`, or named leak points.)*
- **Check:** "16 seals, each hard against its horizontal on the chamber side, boss in the horizontal's slot end, none proud of the vertical's face."
- **Tip/why now:** "At the four bottom joints where the side rails meet the verticals, the Z rail covers the slot from 3 mm up at Step 02.06; after that a seal cannot go in."
- **Callout:** "LDO's guides do not mention the seals; LDO's product drawing (DREMC/West3D listings) shows the placement."
- **Apply the same wording to** Hardware `:50`, Read-first `:59`, Checkpoint `:623`, `checklists.md:56`.

### G9-02 major goal 1: Step 00.2's Do and Check (and Checkpoint 00) still send the builder to the batch tile, which opens the Rev D page; the new callout says the kit is Rev D+

**Where:**
- `00-before-you-start.md:140–143`: "open the batch tile… this is your inventory checklist", and Check "headed `V2.4 350 BOM (Rev. D)`… as expected".
- `:133`: "the generic page is no stand-in".
- `:1110` Checkpoint: "inventoried against **your batch's** BOM page".
- Compare `:147`: "every tile linking the Rev D page. This kit's BOM is the separate Rev D+ page".

**Evidence:**
- Live `350_BOM/HOME`: 27 tile links, all `/Rev_D` (batches 2406…2609, including every 2603–2609 batch after Fabreeko's "Rev D+ Changes for March 2026").
- Neither index page links `Rev_D+`.
- The D vs D+ row diff is exactly: −SD Card 32GB; +DC Ground Wire, +Extruder Motor Ground Wire, +Extrusion Blind Joint Seal ×20.
- A builder who follows Do and Check ticks against Rev D. They would report a "short" SD card to Fabreeko, and the seals and ground wires would have no line to tick.

**Proposed fix:**
- Do 3 → "Print the Rev D+ page (or your tile, if it is headed Rev. D+): this is your inventory checklist."
- Check → "The tile opens `V2.4 350 BOM (Rev. D)`; LDO's tiles still point there (2026-10-30). Inventory against the Rev D+ page instead."
- `:133`: drop "the generic page is no stand-in", or qualify it.
- Checkpoint `:1110` → "against the Rev D+ BOM page (or a Rev D+ batch sheet)".

### G9-03 minor goal 1: "both gating questions" survives in two checklists

**Where:**
- `00-before-you-start.md:1123` (Checkpoint 00): "both gating questions posted".
- `docs/print/checklists.md:22`: same text.
- Nit: `00-index.md:21` still says "the Discord questions" (an index edit needs `draw_diagrams.py --only 11`).

**Fix:** "the gating question posted (Step 00.32)".

### G9-04 minor goal 1/3: the ground-cable rename stops short of Ch 08.43, Ch 10.58 and the fallback callouts

**Mapping verified.**
- LDO's ESD Hardening section (Nitehawk-SB V2 doc) says: "connecting the extruder motor body to the toolboard ground, and the USB adapter ground to the printer frame… kits now also provide grounding cables". The scheme image shows a black motor↔toolboard wire and a green/yellow USB-adapter↔extrusion wire.
- So Extruder Motor Ground Wire = toolboard→motor, and DC Ground Wire = USB adapter→frame. The second is **by elimination**: LDO's prose names neither BOM row.
- `parts --ledger`: Extruder Motor Ground Wire is consumed only at 08.53, DC Ground Wire only at 09.25.

**Gaps:**
1. `08-toolhead.md:1034` (Step 08.43) traps "the supplied ground cable's ring lug", but 08.43's Parts has no ground wire; it first appears at 08.53. Gather for 08.43 therefore omits a part the step fits.
   - **Fix:** move `Extruder Motor Ground Wire ×1` to 08.43's Parts and make 08.53 `reused: the Extruder Motor Ground Wire, board end under the toolboard M3×8`.
2. `10-wiring.md:1527`, `:1534` still say "the long supplied grounding cable", "both short-cable lugs" and "the long cable".
   - **Fix:** "reused: the DC Ground Wire, ring already on the USB adapter"; Do 1: "both lugs of the Extruder Motor Ground Wire under screws, the DC Ground Wire's ring on the USB adapter."
3. The fallback callouts still treat the cables as undocumented extras, "**If your kit did not include the grounding cables** … ask in `#ldo_motors`… The scheme was undocumented": `08-toolhead.md:1270–1273`, `10-wiring.md:1541`, `08-toolhead.md:1564`, `checklists.md:195`.
   - They are BOM rows now. A missing one is a Step 00.3 shortage for Fabreeko (which is how Ch 03:59 routes missing parts), not a support question.
   - **Fix:** "Missing from *Electronics 2*? It is a BOM row: report it to Fabreeko at inventory (Step 00.3); do not improvise a ground."
4. Nit: `00-before-you-start.md:1096` asserts the cable mapping as fact. Add "(by elimination; LDO's prose names neither row)".

### G9-05 minor goal 3: Step 09.22 inserts "the SD card", but the bought card is only useful once imaged at 12.2–12.6

**Where:** `09-electronics-bay.md:634` Parts "32 GB microSD card, bought (Step 00.8: Rev D+ ships none)"; `:640` "Slide the SD card in now."

**Evidence:** Tonight runs Ch 12 Part 1 (12.1–12.6, "image the Pi") at row 15, before Ch 01, and Ch 12's prerequisites call that half "bench-done on day one". A blank card slid in at 09.22 would have to come back out, from under the Pi on the Leviathan, for 12.2.

**Fix:** Parts → "consumable: the 32 GB microSD card imaged at Steps 12.2–12.6"; Do 3 → "Slide the imaged card in now (if Ch 12 Part 1 is not done yet, leave the slot empty)."

### G9-06 minor goal 1: the sweep left two deliverables and seven in-manual labels on Rev D

**Survey:**
- `docs/voron-build-instructions-survey.md:54` "32 GB SD" in the kit host row.
- `:491` "32 GB SD (supplied)". Wrong for D+.
- `:75`, `:587` link the Rev D BOM.

**Print plan:** `docs/voron-print-plan.md:36, 37, 311, 466, 1018` link "Rev D 350 BOM". Every fact cited (panels, rails, deck 3 mm) holds on Rev D+, so this is a re-label only.

**Mixed labels inside the manual:**
- `02-z-drives.md:92`: the label "Rev D 350 BOM" sits over a `Rev_D+` link.
- `02-z-drives.md:55`, `:418`.
- `00-before-you-start.md:661` (insert table, "LDO Rev D 350 BOM | 153").
- `08-toolhead.md:1075`.
- `00-index.md:39`.
- `print/B01-z-drive-assemblies.md:38`.

All of these facts hold on D+ (inserts 153, deck 3 mm, fans 24 V), so the change is wording only.

**Changed correctly:** scripts, slicer and `docs/print/*` hold no other `Rev_D` URLs; `kit_bom.URL` is the only one in code.

### G9-07 minor goal 1: Step 01.23's daylight check cannot discriminate on an open frame, and "4 wherever daylight shows" is not checkable

**Where:** `01-frame.md:593`, `:595` and the Helper line.

**Evidence:** No panels are on at Ch 01; light passes around every member. LDO's illustration places one seal per joint (16), so the other 4 of the 20-pack read as spares.

**Fix:** replace with G9-01's Check, and say where the four go (Alex's ruling), or bag them as spares.

### G9-08 minor goal 1 (re-asserted by the relabel): Ch 03's "not laminated at the factory" contradicts Fabreeko

**Where:** `03-build-plate.md:287`: "the magnetic pad is a **separate line item** in the 350 Rev D+ BOM — it is not laminated at the factory".

**Evidence:**
- The relabelled fact holds: `Magnetic Pad 2.4-350` is its own row, in the *Build Plate* box.
- The inference does not. Fabreeko's Rev D+ page says "Pre-installed magnet sheet on the metal bed" and "(Rev D) now includes … pre-installed bed magnet". The fallback branch ("If your plate did arrive with the magnet already on, skip to 03.10") limits the damage.

**Fix:** "LDO lists the pad as its own row; Fabreeko says it ships pre-installed. If it is already on, skip to 03.10 …; if it is loose, laminate it here."

### G9-09 nit goal 1: Ch 01 Sessions header says segments of 25–65 min; after the move they run 35–65

**Where:** `01-frame.md:14`. Pause minutes are 40 / 65 / 35 / 35; Time 2.5–4.0 h still holds (~2.9 h).

**Fix:** "4 segments of 35–65 min".

### G9-10 nit goal 1: sources.yml adds two LDO pages that nothing cites, and both are Rev A–era

`docs-ldomotors-com-en-voron-voron2-faq` and `…-kit-errata` are cited by no doc. Their live content is Afterburner/Octopus/Klicky-Rev-A material, the "wrong revision" kind. Either drop them, or note that they are Rev A reference only. The DREMC listing that carries LDO's `p.png` is a better addition if G9-01's image is adopted.

### Known, still open (one line)

- 10-23 **G5-11** (Ch 11 `:310`, `:531` "one 3×2 XH splicer PCB" vs BOM qty 2): the diff re-sourced both sentences to `Rev_D+`, where qty is still 2.

---

## Checked and consistent

- **BOM yml vs live Rev D+:** all 143 rows identical in carton, box, item and qty, in the same order. The note line matches. The D→D+ delta is exactly the four rows claimed. Fasteners are identical. The literal `Rev_D+` URL serves the D+ page (HTTP 200).
- **kit_bom.py:** URL and docstring are Rev D+. The three new aliases match their own rows only. The SD alias and its `hardware-ownership.yml` role are removed. The ledger shows seals 20/20, both ground wires 1/1, no SD Parts line resolving to the BOM. Running the parser was read-only.
- **SD card:**
  - 00.8 Buy row, 09.22, the Ch 12 header and 12.2 are all updated.
  - Ch 00 inventory, glossary, 00-index, checklists (`SD card in`) and print pages have no kit-SD assumption left. The exceptions are the survey (G9-06) and the 09.22 wording (G9-05).
  - PROJECT_MEMORY's purchase list already has "32 GB A1 microSD + reader".
- **Ground-cable mapping:**
  - Matches LDO's ESD Hardening prose and the three repo images.
  - Ch 08 Hardware row and 08.53 Parts updated.
  - Ch 09 Hardware row and 09.25 Parts/Do updated. Its image is the V2 `usb_adapter_gnd` photo (identical md5 to Ch 10's mirror).
- **00.32 reduction:**
  - Updated consistently: title, What you're looking at, Do, table (one row), Check, both callouts, Pause, Read-first `:67`, Before-the-kit-ships `:92`, 00.30 Do 2, and the regenerated 00-tonight / tonight.json.
  - The `printed_part_guide_rev_d_plus` and `wiring_guide_rev_d_plus` 404s are re-verified.
  - Leftovers in G9-03.
- **00.2 callout facts:** index tops out at 2609; every tile links Rev_D; D+ unlinked on both index pages; delta text correct. The step logic is in G9-02.
- **Relabelled facts on the Rev D+ page:**
  - Deck 469×469×3 and bottom 4 mm: yes.
  - Magnetic pad separate row: yes.
  - No heatpad wattage: yes.
  - COB strip has no row: yes.
  - Two handles and four M5×14 BHCS: yes.
  - Two 6020 fans; 9 mm belt 6 m and 6 mm belt 6.21 m: yes.
  - Motor part numbers, LRS-200-24, three 221-415: yes.
  - Inserts 153: yes.
- **sources.yml:** the working tree parses (195 entries, no duplicate ids). **HEAD's copy does not parse** ("mapping values are not allowed here", line 840), so the HappyCam colon fix is a real repair and should ship with this diff. The four new entries use the six-key neighbour schema with existing `kind` values. Titles match the live `<title>`s.
- **CONVENTIONS.md:158:** pin sentence says Rev D+.
- **Step 01.23 bookkeeping:**
  - ID appended, no renumbering; Hardware 20 equals Parts 20.
  - Read-first bullet present; box is *Electronics 2* (BOM).
  - Pause moved from 01.22 to 01.23 at 35 min.
  - Checkpoint, checklists, tonight.json and build-progress.json are consistent with each other.
  - The placement itself is G9-01.
- **Rev D+ coverage beyond the BOM:** nothing else is missing that the Fabreeko page or the Nitehawk-SB V2 doc implies. USB passthrough / secondary port is covered at 00.5 (ID table), 08 (`:1225`, `:1242`, Checkpoint), Ch 10 slack callout (`10-wiring.md:1762`), 12 (`:348` extra USB device) and the glossary; tacho fans are optional diagnostics. No Rev D+ BOM row goes unconsumed (`--ledger`); fastener surpluses are spares and unchanged by D+.
