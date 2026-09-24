# Wave 4 plan: parts preparation, panel crops, helpers, rewards, Tonight overlay

Status: **PLAN, awaiting Alex's approval** (claude, 2026-09-24). Scope as approved 2026-09-23 (WORKLIST § Decisions).
Nothing is implemented. The decisions Alex needs to make are in § 8.

Gate for every subtask: `python3 scripts/lint_manual.py && python3 slicer/check_docs.py && .venv/bin/mkdocs build --strict`.
Parallel workers run it only through the serialising wrapper `…/scratchpad/gate.sh`.
Binding rules:
- Step ids are never split or renumbered. Appending is allowed.
- Counts, crops and placements are checked against the manual page image, the STL or the CAD. Never against a G-file's suggested text.
- Every changed page type is checked at 1024×768 before it is called done.
- Alex's uncommitted files (`IMG_3298/3299.jpeg`, GUI-saved 3MFs) are never checked out, stashed, reverted or committed.

## 0. Baseline (verified 2026-09-24)

Every step in chapters 00–14 has a `**Parts:**` line. Every assembly chapter has a **Hardware** table.

| Ch | Steps | Parts, not none | Parts items | Items with no count | Manual/SB page image lines | Steps with no image | Helper lines |
|---|---:|---:|---:|---:|---:|---:|---:|
| 00 | 32 | 21 | 46 | 23 | 11 | 17 | 4 |
| 00a | 12 | 2 | 2 | 2 | 0 | 8 | 0 |
| 01 | 22 | 13 | 25 | 6 | 19 | 2 | 5 |
| 02 | 44 | 38 | 76 | 23 | 43 | 0 | 5 |
| 03 | 20 | 19 | 25 | 20 | 18 | 0 | 3 |
| 04 | 38 | 36 | 60 | 29 | 38 | 0 | 4 |
| 05 | 48 | 41 | 75 | 8 | 38 | 1 | 5 |
| 06 | 42 | 22 | 28 | 13 | 25 | 8 | **0** |
| 07 | 39 | 24 | 29 | 19 | 33 | 3 | **0** |
| 08 | 65 | 62 | 78 | 35 | 5 + 50 SB | 1 | **0** |
| 09 | 36 | 31 | 72 | 17 | 27 | 1 | **0** |
| 10 | 80 | 74 | 99 | 41 | 12 | 17 | **0** |
| 11 | 67 | 66 | 130 | 39 | 63 | **30** | 7 |
| 12 | 37 | 4 | 6 | 3 | 0 | **30** | **0** |
| 13 | 43 | 9 | 15 | 15 | 0 | **26** | 5 |
| 14 | 24 | 12 | 14 | 13 | 0 | **20** | 1 |

- Item counts come from the current parser (`build_steps._parts_items` / `_count_of`).
- About 170 items are prose longer than 8 words.
- There are 382 manual/SB page image lines on 275 distinct pages. 188 of those lines sit on the 81 pages shared by two or more steps.
- Ch 12–14 have 76 of 104 steps with no image. Ch 11 has 30 of 67 (the sweep's 29/66 predates an appended step).

---

## 1. Parts: one item per line, with a count and a source, feeding a Prusa-style Gather

### Current state
- There is one parser, and it lives in `scripts/build_steps.py`:
  - `_PARTS_RE` (:75).
  - `_parts_items` (:480) splits on `;`, then `·`, then on commas only when every chunk has its own count.
  - `_parts_block` (:501) renders the step list and its thumbnails.
  - `_count_of` (:851) reads `×N`, `N×` and `(N)`.
  - `_printed_info` (:868) finds bins through `assets/parts/MANIFEST.csv`.
  - `_merge_key` (:889), `build_segments` (:949), `gather_admonition` (:986) and `gather_overview` (:1001) do the rest.
- `_segments` (:616) collects a Parts marker with `_run` (:561) up to the first blank line. Only Do gets `_absorb_lead` (:569). A list under **Parts:** would therefore fall out as a visible "block" and never reach the gather.
- Other consumers:
  - `scripts/lint_manual.py:227` uses Parts only as a field boundary. It sets no budget. Step refs in Parts count toward the ≤1 cross-ref limit (:367).
  - `scripts/build_tonight.py:99–100,186` and `slicer/check_docs.py:299–313` read the single-line `**Parts:** … — H h, G g (PrusaSlicer 2.9.6 estimate)` of print-chapter **Load** steps.
  - Nothing else parses Parts. I grepped hooks, JS, cad_render, slicer and workflows.
- Failure modes, all confirmed:
  - Per-unit counts in "build all four" steps. G2-03: 02.22–02.26 lists M3×40 ×6, but the step needs 24.
  - Comma lists merge (G3-06).
  - Reused parts are counted twice (G3-16).
  - Prose turns into rows (G2-08, G6-24).
  - No step says where hardware comes from (G2-20, and U2 in G2–G7).
- **Bag source.** The repo has no BOM copy. The only in-repo trace is the carton-1 box list in 00.3 (`00-before-you-start.md:153`) and its partial count table.
  - The source of truth is LDO's **V2.4 350 BOM (Rev. D)**, <https://docs.ldomotors.com/en/voron/voron2/350_BOM/Rev_D>. It is pinned in `sources.yml:120`.
  - `curl -sL` returns it in full: a Carton → Box → Item → Qty table with about 85 rows. The 11 boxes are Cable Kit, Motion, Electronics 1, Electronics 2, Fasteners Tools & Misc, Belts Chains & Fans, Linear Rail Kit, Frame Kit, Motor Kit, Other and Panel Kit. Build Plate is a carton-2 box.
  - Each fastener size is its own bag inside *Fasteners, Tools & Misc*.
  - Caveat, already in 00.2: Alex's batch is not yet listed, so the file must be re-pinned to his batch sheet on kit day.

### Design
**Markdown grammar (assembly chapters 00–14):**

```
**Parts:**

- M3×40 SHCS ×24
- M5 hexnut ×4
- `[a]_z_drive_baseplate_a` ×2
- `[a]_z_drive_baseplate_b` ×2
- reused: the four belted shaft assemblies
- tool: 2.5 mm hex key
- M3 heat-set insert ×7 — from KADRICK kit
```

- Put a blank line after `**Parts:**`. Without it the list renders as a run-on paragraph on the long page, the same as the Do-list rule.
- One item per bullet. The count is the **total for everything the step does**. "per drive" / "each" phrasing goes into Do, never into Parts.
- `**Parts:** none.` stays a single line.
- Prefixes:
  - `reused:` (already on the bench): listed and never summed.
  - `tool:` / `consumable:`: gathered under their own heading and never reconciled.
  - A trailing `— from <source>` sets the source by hand, for things that are not in the kit BOM: KADRICK inserts, the door kit, Ti backers.
- `reused:` items never cite step numbers, because they would count against the cross-ref limit.
- **Print chapters (B00–B11) keep the single-line form.** Their Load-step lines are parsed by `build_tonight`/`check_docs`, and G8 rated them 2. The parser accepts both forms, and lint applies the new rule to `NN-*.md` only.

**The source is derived, not typed.** A new `scripts/data/ldo-350-bom.yml` holds `{carton, box, item, qty, aliases}` rows, fetched by `scripts/kit_bom.py` from the pinned page.
- A canonical-key normaliser maps `M3×40 SHCS` ⇄ `Machine Screw, SHCS, M3x40`. Aliases cover T-nuts, bearings, pulleys, motors, extrusions and rails.
- Printed items keep their bin from `MANIFEST.csv`, which is unchanged.
- Kit-day re-pin means editing one file, and every step updates.

**Rendering:**
- Step list: `M3×40 SHCS ×24 · Fasteners box` (muted). Printed items keep their thumb and add `· bin 02-Z0`.
- Gather block and overview line are **grouped by source**, Prusa-style:
  - one heading per kit box, then printed parts by bin, then tools and consumables;
  - then "already on the bench" (the `reused:` items), for reference.
- Counts are summed per segment, as today.

**One owner of the decision:** a new `scripts/parts.py` (moved out of `build_steps.py`, not reimplemented). It holds the parse, count, merge key, printed/bin lookup and BOM resolve. `build_steps.py` and `lint_manual.py` both import it.

**Lint** (`lint_manual.py`, two new checks, in warn mode until § 6 phase 5 flips them to fail):
- **6 · Parts grammar** (assembly chapters). Each Parts field is `none` or the list form. Each unprefixed item has a count, has no `per`/`each`, holds one item per bullet, and resolves to a BOM row, a printed STL or a `— from`.
- **7 · Hardware reconciliation.** Per chapter, the step totals of each kit item (excluding `reused:`/`tool:`) must equal the chapter **Hardware** table total.
  - Table Qty cells must *lead* with the total, for example `60: 24 drives + 36 Z rails`.
  - This is the objective check that makes the count migration verifiable. It will surface real count errors like G2-03.
  - An informative kit-wide line reports Σ chapter tables vs BOM qty (spares).

### Subtasks
| id | level | files (owner) | acceptance | check |
|---|---|---|---|---|
| 1A | deep | `scripts/parts.py` (new), `scripts/kit_bom.py` (new), `scripts/data/ldo-350-bom.yml` (new), `scripts/build_steps.py` (Parts/gather functions only), `scripts/lint_manual.py`, `docs/stylesheets/extra.css` | Both grammars parse. `_segments` absorbs the list. Gather is grouped by source. Checks 6 and 7 are in warn mode with `--json`. Unit examples cover G2-03 / G3-06 / G3-16 / G6-24 fixtures (`python3 scripts/parts.py --selftest`). Rendered output is unchanged for print chapters. | gate; `--selftest`; `python3 scripts/lint_manual.py --parts-report` |
| 1B | builder | all chapter files `docs/manual/0*.md 1[0-4]-*.md` (**exclusive, one run**) | One-off converter, kept in the scratchpad and not committed, that reuses `parts.py` to rewrite every Parts line to the list form. Anything it cannot classify is left verbatim, with the check 6 finding naming it. No other text changes. | gate; `git diff --stat` touches only Parts lines |
| 1C | deep | content packets P1–P9 (§ 6) | Check 6 and check 7 at zero for the packet's chapters. Counts are checked against page images and Hardware tables. | gate + `lint_manual.py --parts-report <chapters>` |

Effort: 1A ~5 h, 1B ~1 h, 1C folded into the packets (~1–2 h each).

---

## 2. Step images: panel crops; screenshots for Ch 11–14

### Current state
- Images are plain markdown image lines inside the step, for example `![Voron manual p.88](assets/manual-pages/manual-p088.png)`.
- `layout_step` (:712) hoists them into `.step-figure`, sorting `_PRIMARY_IMG_DIRS` (:96: `manual-pages/`, `sb-pages/`) first.
- An optional `{ attr }` is already carried through (:752–762). One exists today: `{ width=240 }`.
- Pages are 1287×910 PNGs, 40 MB for `manual-pages/` and 8.9 MB for `sb-pages/`.
- At 1024×768 the figure column is about 500 CSS px (`extra.css:210–222`), so a whole page shows at ~39 % and its labels are unreadable. U4 scored 1–2 in G2–G5.
- The source PDFs are local only and gitignored: `docs/manual/assets/Voron2.4r2-manual.pdf` (pinned de7e89d) and `Voron-Stealthburner-manual.pdf`. Poppler (`pdftoppm`) and `magick` are installed.
- No crop tooling exists. `crop` in scripts only touches mascot/bin internals.
- Chapters 12–14 have 8/17/3 images, all LDO/Voron `assets/remote`. Nothing shows Mainsail, the Imager, KlipperScreen or a console response.
- Ch 11's 30 image-less steps are the Nevermore plenum (11.26–11.41), the Clicky-Clack door (11.44–11.51, 11.62–11.66), 11.5, 11.19 and 11.67.

### Design: crops
- **Declare the crop on the chapter image line.** The source keeps pointing at the full page, which the standing rule relies on:
  - `![Voron manual p.88](assets/manual-pages/manual-p088.png){ crop="0.12 0.14 0.62 0.72" }`.
  - The crop is page fractions x0 y0 x1 y1.
  - No attr means the full page, as today.
- **A new `scripts/crop_panels.py`** has three modes:
  - `--sheet pNNN` writes a 10 %-gridded overlay into the scratchpad, for choosing boxes.
  - `--render` rasterises the pinned PDF page at 300 dpi and crops to ≤1200 px on the long edge (2× the 500 px column). It quantises with `magick -colors 64` and writes `docs/manual/assets/manual-crops/pNNN-<hash8>.png`. The name is content-addressed, so it is idempotent across parallel workers.
  - `--check` reports declared crops that are missing and crops that are orphaned. It needs no PDF, so CI works.
  - Crops are committed. The PDF is not, so CI cannot re-render them.
  - Estimate: about 250 crops, ~100 KB each, **+25 MB repo**.
- **`build_steps` (2B)** uses the crop as `step-figure__main` and adds a "Full page" link to the page PNG.
  - A declared crop with a missing PNG fails the build (on_pre_build raises, so `--strict` stops).
  - The long chapter page keeps whole pages. It is the reference view.
- **Where to crop.** Any page image whose step acts on one panel of a multi-panel page. At minimum that is the 188 lines on shared pages; the target is the ~250 lines where a panel exists. Single-illustration pages stay whole.

### Design: screenshots before the kit (what is realistic)
| Need (steps) | Source | Licence status |
|---|---|---|
| Raspberry Pi Imager (12.2, 12.3) | Real screenshots on this Mac. The Imager is not installed yet (D2). | Own work |
| PrusaSlicer printer profile / slicing (13.41) | Real screenshots, 2.9.6 installed | Own work |
| Mainsail dashboard, console responses (`STATUS`, `QUERY_ENDSTOPS`, `PROBE_ACCURACY`), config editor (12.5–12.37, 13.x, 14.x) | A **local Klipper + Moonraker + Mainsail stack in Docker** (Docker.app is installed but not on PATH), captioned "simulated printer: your numbers differ" (D2) | Own work |
| KlipperScreen (12.9, 12.10) | The same stack if it runs headless, else kit day | Own work |
| Mechanical/physical startup steps (13.9–13.19, 14.5) | Voron-Documentation startup images | GPL-3.0 (survey § 7.4), already mirrored for 13.x |
| Input shaper, PA and rotation-distance figures (14.7–14.18) | Klipper `docs/img` | GPL-3.0, a new source (D3) |
| Mainsail / KlipperScreen docs screenshots | mainsail-crew docs, KlipperScreen docs | Unverified; verify first (D3) |
| Nevermore plenum, Clicky-Clack door (Ch 11) | Nevermore repo / the door's source repo; fallback: our own STL renders (`scripts/render_parts.py`, bigger frame) | Unverified (the survey has KB3D and ldomotion as link-only) |
| Ellis PA pattern (14.17) | Link only | No licence (survey) |

- Terminal-only steps get **no fake screenshot**. Where a Check names an expected output, the step shows it as a code block. The generated "terminal card" idea is rejected as duplication.

### Subtasks
| id | level | files (owner) | acceptance | check |
|---|---|---|---|---|
| 2A | builder | `scripts/crop_panels.py` (new), `docs/manual/assets/manual-crops/` (new dir) | `--sheet/--render/--check` work on p088 and one SB page. Output is deterministic (same box → same bytes). | `python3 scripts/crop_panels.py --check` + a two-crop smoke test |
| 2B | builder, after 1A | `scripts/build_steps.py` (figure only), `docs/stylesheets/extra.css` | Crop swap plus a "Full page" link. A missing crop fails the build. Pages without a crop are unchanged. | gate; 1024×768 screenshot of a cropped step |
| 2C | quick | none (report) | A licence table from each repo's LICENSE file: Klipper, mainsail-crew/docs, KlipperScreen, Nevermore Micro, the Clicky-Clack source, raspberrypi/documentation | report to the orchestrator, relayed to Alex |
| 2D | deep, gated by D2 | `docs/manual/assets/screens/` (new), scratch docker compose outside the repo | A 2-h time-box spike. Mainsail shows our `printer.cfg` in the editor. A sim config answers `STATUS`/`QUERY_ENDSTOPS`. Screenshots are at 2× DPR with a SOURCES line. If it fails, report and stop. | files exist and render in the gate build |
| 2E | builder, after 2C/D3 | `docs/manual/assets/remote/1[1-4]-*/` + `SOURCES.txt` | Mirror only licence-cleared images, each with file → URL → owner → date | gate |
| 2F | deep | content packets (§ 6): crop boxes in each packet; screenshot placement in P8/P9 | Every crop chosen on the gridded sheet and checked against the Do text | `crop_panels.py --check`, gate, 1024×768 spot checks |

Effort: 2A ~2 h, 2B ~2 h, 2C ~0.5 h, 2D ~2 h time-box, 2E ~1–2 h, crops ~15–20 min per 10 lines inside the packets.

---

## 3. Helper lines in Ch 06–10 and 12

### Current state
- There are zero `**Helper:**` lines in 06, 07, 08, 09, 10 and 12 (table above).
- The rules are in CONVENTIONS § Helper steps (`CONVENTIONS.md:97–128`): ≤20 words, after Check, and never on mains, iron/insert, blade or hot steps.
- `NO_MASCOT_STEPS` (`hooks/mascot.py:107–114`) is the only step classifier.
- **Nothing enforces the helper exclusion.** Lint check 5 checks budget and position only (`lint_manual.py:377`). mascot.py only strips badges.
- Conflict found: Checkpoint 00a (`00a-mains-safety.md:372`) says "she reads the meter only on the unplugged sweeps 10.74–10.78". CONVENTIONS forbids helpers on Ch 10 power-on checks, and NO_MASCOT lists 10.73, 10.77 and 10.78 → D4.
- Sweep seeds:
  - G4 m8: 06.12, 06.16, 06.23, 06b.3, 07.5, 07.27, 07.29, 07.31.
  - G5-21: 08.1, 08.13, 08.18, 08.40, 08.48, 08.52, 09.2, 09.3, 09.7, 09.19, 09.20, 09.27–09.33.
  - G6-17: 10.40, 10.65, 10.70, 10.74–10.77.
  - G7-23: 12.7, 12.13, 12.27. 12.11 is **rejected** because it is a mains power-on in NO_MASCOT.

### Candidate-step method
1. **Universe.** Take the steps of 06/06b, 07, 08, 09, 10 and 12, minus every NO_MASCOT id, minus any step whose Do names the iron, a blade, mains or heat.
2. **Score** each step's Do/Check on:
   - two-person cues: lift, hold, steady, both hands, second pair, tilt;
   - reading cues: phone, app, Hz, pluck, read, meter, caliper, screen, LED, version;
   - counting and labelling cues: count, turns, label, tag, tick, compare, photo.
   Union the result with the sweep seeds.
3. **Judge.** The packet worker reads each candidate against its page image and keeps it only if the helper's job is a whitelisted kind: sorting, labelling, counting, reading back, holding steady, cleaning, pressing a button. It writes one ≤20-word, third-person line after Check.
   - If the safe part is only a fraction of the step, leave the step untagged.
   - Expected yield: roughly 35–50 lines.
4. **Enforce.** `hooks/mascot.py` fails the build when a `**Helper:**` line sits inside a NO_MASCOT step, with an explicit exception set only if D4 says yes. `build_tonight`'s "With a helper" section picks the new lines up with no code change.

### Subtasks
| id | level | files | acceptance | check |
|---|---|---|---|---|
| 3A | builder, in the 2B slot | `hooks/mascot.py` | Build fails on a Helper line in a NO_MASCOT step. Its self-test covers the case and any D4 exception. | `python3 hooks/mascot.py`; gate |
| 3B | deep | packets P5–P7, P9 (§ 6) | Every seed is decided: added, or rejected with a one-line reason in the packet report. Lint check 5 is clean. | gate |

Effort: 3A ~1 h, 3B ~30–45 min per chapter inside the packets.

---

## 4. A reward at every Checkpoint (Revali `pass` + "you built X" + gummy worms)

### Current state
- There are 17 assembly Checkpoints (00, 00a, 01–05, 06, 06b, 07–14) and 12 batch Checkpoints (B00–B11).
- `## Checkpoint` pages are built at `build_steps.py:289–297` and rendered at :1104. The CAD figure is added at :1139–1146.
- The `pass` pose appears once today, in Ch 14's intro fence (`14-calibration.md:7–10`), and not on any Checkpoint.
- `mascot.scene_html` (`hooks/mascot.py:222`) emits the scene with the `@mascot/` sentinel, which `on_page_content` resolves after markdown, so hook order does not matter.
- The humour rule is enforced only per step id, which is fine: Checkpoints are not steps.
  - Checkpoint 00a is mains content. Its whole chapter is mains safety → D5.
  - Checkpoint 10 is an unplugged checklist whose "cord out of the room" Pause comes first. The G6-20 sweep suggests a bird there, off the mains steps.
  - Checkpoints 13 and 14 are verification lists, not hot actions.

### Design: generated, from one authored line
- **Assembly Checkpoints.** Each chapter gets one authored line under its heading: `**Built:** a square frame that everything else hangs off` (≤12 words, no em-dash, no parenthetical).
  - `build_steps` renders it after the checklist on the Checkpoint page, and on the long page via its `on_page_markdown`, as `scene_html("pass", "You built <X>. <N> gummy worms.")`.
  - N is the chapter's `**Sessions:**` count (D6). The caption stays ≤18 words, the mascot rule.
  - A Checkpoint without `**Built:**` fails the build once phase 5 flips it on.
- **Batch Checkpoints: fully generated, no authoring.** "Batch B03 printed: plates 7–9 of 22, 81.3 of 157.0 h. N gummy worms." The numbers come from `slicer/plates.py` (`PLATES`, `run_of`). B11 reads "outside the run".
- **Humour rule.** A set `REWARD_TEXT_ONLY = {"00a"}` in `hooks/mascot.py`, the one classifier, gives a plain reward line with no bird (D5).
- **No `⚠` gag, and the bird never makes the mistake.** Captions follow STYLE.md.

### Subtasks
| id | level | files | acceptance | check |
|---|---|---|---|---|
| 4A | builder, in the 2B slot | `scripts/build_steps.py` (checkpoint render + long-page expansion), `hooks/mascot.py` (`REWARD_TEXT_ONLY`), `docs/stylesheets/extra.css` | All 29 Checkpoints render a reward. 00a has no bird. Batch numbers match `plates.py`. The caption word cap is enforced. | gate; 1024×768 of Checkpoint 02, 10, B05 |
| 4B | deep (in packets) | one `**Built:**` line per assembly chapter | 17 lines. Each names the end state its Checkpoint verifies. | gate |

Effort: 4A ~2 h, 4B minutes per packet.

---

## 5. Tonight progress overlay, and the wave-2 leftovers

### Current state
- `scripts/build_tonight.py` (on_pre_build) builds `00-tonight.md` from the index timeline rows. `_parse_chapter` (:164) makes Pause-delimited build segments and one print segment per Load step.
- `_plan_for_budget` (:296) packs greedily and is static: one plate start per plan, a misfit takes the rest of its row, `stop_at_kit`, and `bench_first` while the row-1 gate is open.
- Segments are emitted as `<span data-first-step>` (:384). `build_steps.on_page_markdown` rewrites them to `<a class="tonight-seg" data-first-step href>` (:1435, :1494–1502).
- **No JS reads them.** `progress.js:310` excludes `.tonight-seg` from badges.
- The tick store (`progress.js:17–36`) is `localStorage['voron-progress:ch:<chapter-slug>']`, a `{stepId: true}` object with Checkpoint items under `cp:…`. The slug is the file stem, lower-cased (`b03-…` for batches).
- `docs/javascripts/boards.js` already does "Python writes JSON to `docs/assets/`, JS reads ticks, static fallback" for Home (`build-progress.json`, `build_printables.py:530`). It also keeps per-plate "printed" state. **Reuse that pattern.**
- The wave-2 claim was removed. Today's header text (`00-tonight.md:3`) says plans "do not know which steps you have already ticked". Home (`docs/index.md:23`) says "Open Tonight, pick the 30, 60 or 90-minute plan, tap its first step".
- Known planner bug (PROJECT_MEMORY, lab backlog): the kit-arrived branch can offer a later batch's plate start when the earlier batch's segment did not fit (a cross-row break). A JS port must not inherit it.
- Leftover a: the `**Next:**` override is read on Checkpoint pages only (`build_steps.py:293–297`, :1383), so 13.34's Next goes to 13.35 instead of Ch 06b.
- Leftover b: the Pause at `00-before-you-start.md:432` (pre-kit, after 00.12) is followed by kit-day 00.13. The next Pause (:536) is `(pre-kit)`, so the pre-kit segment "00.13 → 00.16" starts on a kit-day step.

### Design
1. `build_tonight.py` also writes `docs/assets/tonight.json` with:
   - the rows in timeline order (`label`, `kind`, `kit`);
   - per segment: `chapter` (progress slug), `steps` (every step id in it), `first_step`, `href`, `minutes`, `kind`, `pre_kit`, `plate`, `print_hours`, `leave_state`, `helpers`;
   - the planner constants;
   - and `cases`: the Python planner's own output for about 12 seeded done-states.
   - `href` is computed with `build_steps._slug_for_step` and the chapter overview map (import them; never re-derive).
2. A new `docs/javascripts/tonight.js` (Tonight page only) reads each chapter's tick store.
   - A build segment is done when every id in `steps` is ticked. For a multi-Pause single step (B00.8 ×4), all of its segments stay until the step is ticked.
   - A print segment is done when its Load step is ticked **or** the plate board marks the plate printed.
   - It removes done segments and re-runs a port of `_plan_for_budget`, including `stop_at_kit`, `bench_first` and the gate line.
   - It then replaces the three bucket lists and the "With a helper" list, and adds "N segments done on this device; plans start at Step X".
   - With JS off, or on a fresh device, the static plan stays.
3. **Parity.** A new `scripts/check_tonight.mjs` (node is at `/opt/homebrew/bin/node`) loads the planner from `tonight.js` (UMD guard) and asserts it equals `cases`. It is added to `.github/workflows/check.yml` and run alongside the gate for this wave.
4. Fix the cross-row bug in the Python planner first, so both implementations carry the fix.
5. Restore the claims:
   - Tonight header: "Plans are packed from the index timeline. On this device, segments you have ticked are skipped and each plan starts at your first unfinished step."
   - Home (`docs/index.md:23`): "Open Tonight: it starts where your ticks stop."
6. Leftover a: accept a `**Next:** [..](..)` line in a **step** body too. It renders visible, after Source, and overrides that page's Next button. Content: add `**Next:**` → Ch 06b to 13.34.
7. Leftover b: add a kit-day `Pause:` line to 00.13 (no renumbering), so the pre-kit segment is 00.14–00.16 and 00.13 becomes its own kit-day segment. Verify in the generated Tonight page.

### Subtasks
| id | level | files (owner) | acceptance | check |
|---|---|---|---|---|
| 5A | deep | `scripts/build_tonight.py`, `docs/javascripts/tonight.js` (new), `docs/stylesheets/tonight.css` (new), `mkdocs.yml` (extra_js/css), `docs/index.md`, `scripts/check_tonight.mjs` (new), `.github/workflows/check.yml` | JSON emitted. Cross-row bug fixed with a test case. The JS planner matches all `cases`. Overlay verified in WebKit at 1024×768 with seeded localStorage for three states: none ticked, Ch 00a done, B00 plates 1–2 done. The first-open render needs no refresh. | gate; `node scripts/check_tonight.mjs`; private Playwright WebKit script |
| 5B | builder, in the 2B slot | `scripts/build_steps.py` (Next override on step pages) | 13.34's Next targets the 06b start page. Checkpoint overrides are unchanged. | gate; inspect generated `13-34.md` |
| 5C | deep (packets P1, P9) | `00-before-you-start.md` (00.13 Pause), `13-initial-startup.md` (13.34 `**Next:**`) | Tonight lists 00.14–00.16 as pre-kit and 00.13 as kit-day | gate; grep generated `00-tonight.md` |

Effort: 5A ~5 h, 5B ~1 h, 5C minutes.

---

## 6. Execution order and file ownership

| Phase | Subtasks (parallel within a phase) | Exclusive files |
|---|---|---|
| 0 | 2C licence table; Alex answers § 8 | none |
| 1 | **1A** parts generator · **2A** crop tool · **5A** Tonight · **2D** sim spike (if D2) · **2E** mirrors (after 2C) | 1A: `parts.py`, `kit_bom.py`, `data/`, `build_steps.py`, `lint_manual.py`, `extra.css`. 2A: `crop_panels.py`, `manual-crops/`. 5A: `build_tonight.py`, `tonight.*`, `mkdocs.yml`, `index.md`, `check.yml`. 2D: `assets/screens/`. 2E: `assets/remote/1[1-4]-*` |
| 2 | **2B + 3A + 4A + 5B**, one builder, sequential **after 1A** (shares `build_steps.py`, `extra.css`, `mascot.py`) | `build_steps.py`, `mascot.py`, `extra.css` |
| 3 | **1B** mechanical Parts conversion, one run, **after phase 2** | every chapter file 00–14 |
| 4 | Content packets, deep, ≤8 at once. Each owns its chapter files and does 1C + 2F + 3B + 4B + its leftovers: **P1** 00, 00a, 01 (+00.13 Pause) · **P2** 02 · **P3** 03, 04 · **P4** 05 · **P5** 06, 07 · **P6** 08 · **P7** 09, 10 · **P8** 11 (+ Ch 11 images). Then **P9** 12, 13, 14 (screenshots from 2D/2E, +13.34 Next) | the packet's chapters; crop PNGs are content-addressed, so the shared dir is safe |
| 5 | Integration (orchestrator + builder): flip checks 6/7 and the `**Built:**` requirement to fail; `crop_panels.py --check` for orphans; CONVENTIONS.md sections (Parts grammar, crops, reward, helper exception) from the workers' proposed text; WORKLIST ticks; full gate; 1024×768 pass on one step page, one overview Gather and one Checkpoint per chapter, plus Tonight; PROJECT_MEMORY entry | `CONVENTIONS.md`, `WORKLIST.md` |

- Wall clock: phase 1 about half a day, phase 2 about 3 h, phase 4 about 2–4 h per packet in two waves. Roughly 2 days of agent time in total.
- Before the phase-4 fan-out, run one cheap `critique` pass on the packet decomposition. The likely coupling: Hardware tables whose items span chapters, such as Ch 06/06b and 07.

## 7. Risks
- **Check 7 will fail widely at first.** That is its purpose: it exposes real count errors. Packets fix them against page images, which can turn into accuracy fixes in the text. Those edits are in scope, and are noted in each packet report.
- **The BOM is Rev D generic.** A different batch changes box names or quantities. It is one file to re-pin on kit day, and 00.2 already says so.
- **A wrong crop hides the part the step is about.** Mitigations: the grid sheet, a crop-plus-Do-text contact sheet per packet, and the "Full page" link on every cropped figure.
- **Repo growth.** About +25 MB of crops, plus any mirrored or screenshot PNGs.
- **Two planners.** Drift is caught by `cases` parity in CI. The JS must never plan without the JSON; the static page is the fallback.
- **The Docker sim may not boot Klipper without an MCU.** The spike is time-boxed, and the fallback is GPL docs images plus kit-day screenshots.
- **Parallel packets.** They share only content-addressed crop files and the serialised gate.

## 8. Decisions for Alex
1. **Bag source.** Derive it from a vendored LDO 350 Rev D BOM file, re-pinned to your batch sheet on kit day, rather than typing it on each line. **Recommend: derive.**
2. **Mainsail/KlipperScreen screenshots now.** Time-box a 2-h local Docker sim (Klipper + Moonraker + Mainsail; pulls images) with "simulated printer" captions, and install Raspberry Pi Imager on the Mac for 12.2/12.3. The alternative is to wait for kit day. **Recommend: yes to both.**
3. **Licences.** Embed Klipper-docs images (GPL-3.0, the same class as the Voron/LDO repos you already allowed). Embed Mainsail docs, KlipperScreen, Nevermore and Clicky-Clack images only if 2C finds a GPL or permissive licence, else link-only. **Recommend: yes.**
4. **Helper on the unplugged meter sweep 10.74–10.78.** Your Checkpoint 00a allows it. CONVENTIONS forbids it, and NO_MASCOT lists 10.73/10.77/10.78. **Recommend: follow Checkpoint 00a.** Allow "reads the meter aloud, cord out of the room" on 10.74–10.78 via an explicit exception in `mascot.py` and CONVENTIONS. The badge stays stripped on 10.77/10.78.
5. **Reward placement under the humour rule.** Checkpoint 00a gets a text-only reward. Checkpoint 10, an unplugged checklist, gets the bird. **Recommend: as stated.**
6. **Gummy-worm count.** One per bench session in the chapter (from **Sessions:**), and one per plate for a batch. **Recommend: yes.** The alternative is a flat "gummy worms" line.

## Alex's decisions (2026-09-24)
1. Bag source: derived from the vendored LDO Rev D BOM, re-pinned to the batch sheet on kit day. Yes.
2. Docker Klipper/Moonraker/Mainsail simulator (2 h spike, "simulated printer" captions) and Raspberry Pi Imager on the Mac: yes.
3. Licences: embed Klipper-docs images; others embedded only if the licence check clears, else linked. Yes.
4. Meter sweep 10.74–10.78: helper allowed as **recorder only; the adult holds the probes**. Exception goes in mascot.py and CONVENTIONS.
5. Checkpoint 00a text-only reward; Checkpoint 10 gets the bird. Yes.
6. Gummy worms: 1 per 30 min of bench time in the chapter, 1 per plate for a batch.
