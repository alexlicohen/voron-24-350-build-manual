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
7. Colour cells use exactly `Black` or `Blue` (add `(opaque)` where the STL is `[o]_`); the filament identity lives once, in print plan §1.2.

## Steps
- `### Step NN.M — short imperative title`
- Image line first: `![Voron manual p.XX](assets/manual-pages/manual-pXXX.png)` or an LDO image URL, or `(no image — see text)`.
- **Parts:** exact fasteners/parts for THIS step, one per line with the step total (§ Parts grammar).
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
`scripts/lint_manual.py` runs in CI, after `mkdocs build --strict`. Five checks (the fifth, step word budgets, is in § Action-first steps; `--budgets-only` runs it alone, `--no-budgets` skips it): raw `⚠` / `**Check:**` / `Tip:` text outside an admonition or `<code>`/`<pre>` block; `Step NN.M` references with no matching heading; STL filenames in an assembly-chapter table with no matching print-batch table row (exempt: a row containing `not printed`, `kit-supplied`, or `SKIP`, case-insensitive); Markdown tables wider than 7 columns (exempt: tables under a heading whose text contains "Machine-readable"). Checks 6 and 7 (Parts grammar, Hardware reconciliation) are in § Parts grammar; check 8 (every assembly Checkpoint has a `**Built:**` line) is in § Checkpoint reward.

## Print-batch chapters (added 2026-09-05)
- Live in `docs/manual/print/`: `00-slicer-setup.md` then `B00-calibration-and-jigs.md` … `B10-clicky-clack-door.md` (batch ids from `docs/voron-print-plan.md`). Assembly chapters stay in `docs/manual/NN-*.md`; `00-index.md` holds the interleaved timeline that says which batch to start before which assembly chapter.
- A batch chapter's steps are: prepare filament (dry state, spool) → load the plate file/list in PrusaSlicer with the named profile and overrides → pre-print checks (sheet, chamber preheat) → print → inspect (calipers on the named critical dimensions, bearing-seat test) → label and bin the parts by the assembly chapter that consumes them. Same Step/Parts/Do/Check format.
- Never restate the whole override table per batch; link `00-slicer-setup.md` and list only batch-specific deviations (brim, orientation, accent color).

## Source lines and stopping points (added 2026-09-05, evening)
- **Every step ends with a `Source:` line** after Check (and after any `⚠`/`Tip:` line): `Source: [Voron manual p.NN](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=NN) · [LDO Build Notes p.NN](<url>) · [LDO wiring guide § name](<url>)`. Link the exact page/section the step was transcribed from, using the pinned commit for GitHub files. Print-batch steps link the print plan section (`../../voron-print-plan.md#…`) and the PrusaSlicer/Voron page they rely on. The build hook renders it as a muted caption; the reader taps it to compare notes with the original.
- **Stopping points**: Alex builds in ~30-minute sessions. At every safe place to stop, add a line `Pause: ~NN min since the last pause — <state you leave things in; what NOT to do before walking away>`. Place one wherever a sub-assembly is self-supporting and nothing is half-torqued or half-wired; never inside a bearing press, belt threading, a glued/greased step, or mains work. NN is the estimated hands-on minutes since the previous Pause (or chapter start), a first-build estimate; keep segments ≤ 45 min where the work allows. The hook renders it as an info box; `scripts/` builds the "Tonight" view (`docs/manual/00-tonight.md`) from these lines and the chapter `Time:` fields.
- Chapter header gains one line after Time: `**Sessions:** N × ~30 min` (count of Pause segments).

## Describe the pieces (added 2026-09-05, evening — Alex: "explain and describe the pieces for each step")
- The reader is a first-time builder. Every step carries, directly after its image line(s) and before **Parts:**, a line `**What you're looking at:** <1–3 sentences>` that names each part in the picture/step in plain words, says what it does in the finished machine, and how it relates to what was just built (e.g. "The Z drive is the gearbox in each corner that turns a motor's spin into the belt that lifts the gantry. The housing you printed holds two bearings that carry the 80T pulley; the retainer clamps them."). Define jargon on first use in the chapter (link the glossary entry: `[QGL](16-glossary.md#qgl)`), then use the short form.
- Where the purpose of the action isn't obvious, add one clause of **why** inside Do ("…so the belt runs centred on the pulley and doesn't rub the flange").
- Keep Prusa's tone: concrete, calm, no history, no marketing. Never guess a part's function — the manual/LDO/Voron docs state it; cite in Source.
- Chapter intro (after the scope line): a 3–6 sentence plain-language paragraph "What you're building in this chapter" with the sub-assembly names the steps will use.

## Action-first steps and word budgets (added 2026-09-06)

Prusa's help-site steps run 30–60 words. Ours averaged 237. The fix is the action first and
hard budgets, not more structure.

**Rendered order** (`scripts/build_steps.py`, chapter source order unchanged): **Do:** →
**Check:** → **Helper:** → the segment's Gather block → **Parts:** → a collapsed `What you're looking at` block → `⚠`/`Tip:` →
`Pause:` → `Source:` → **Next:** (§ Step pages › Next overrides). Check sits right under Do so the
pass criterion is on the first screen at 1024×768 (Alex, 2026-09-24). Images stay hoisted to the figure column. Write a step in house order as before; the
generator moves it.

**Budgets** (words, excluding images, code, inline `code` spans and link URLs):

| Field | Budget |
|---|---|
| **Do:** (plus its list/continuation lines) | 40 |
| **Check:** | 25 |
| **What you're looking at:** | 45 |
| `Tip:` | 30 |
| `⚠` callout, each | 60 |
| **Helper:** | 20 |

Also, in Do / Check / description / Helper: **no em-dash** (`—`), and **no parenthetical** except the two
canonical markers `(verify on bench)` and `(not specified — snug)`. At most **one** `Step NN.M`
cross-reference per step outside the `Source:` and `Pause:` lines — the rest belong in `Source:`.

**Multi-action steps**: a numbered list of ≤ 3 imperatives under the Do line (it renders as part
of the lead). **Never split or renumber a step to fit a budget** — step ids are keys in progress
storage, the Tonight view, `assets/parts/MANIFEST.csv`, `cad/steps.yml` and every cross-reference.

**Cut why-clauses, don't move them.** The manual-page image shows what the Source link explains;
the collapsed block is orientation only, not a place to park the words the Do line lost. A
why-clause survives only where the action is wrong without it.

Lint: `python3 scripts/lint_manual.py --budgets` (adds it to the default run) or
`--budgets-only` (this check alone, no `mkdocs build` needed; `--json` for one finding per line).

## Helper steps (added 2026-09-14)

Alex builds this machine with his daughter. A step she can genuinely own carries one extra
field so the manual says so at the bench instead of leaving it to be worked out mid-step.

**Field.** `**Helper:** <what the helper does>` — one line, placed **after `**Check:**` and
before any `⚠` / `Tip:` / `Pause:` / `Source:` line**, with a blank line either side (without
it the line is swallowed into the Check admonition on the long chapter page).

**Budget.** ≤ 20 words, third person present ("Reads each bin label aloud and checks the count
against the diagram."), naming the job rather than the virtue. No em-dash, no parenthetical —
the same two rules Do / Check / the description follow. One Helper line per step.

**Safety rule — where it must never appear.** Only on steps whose helper job is sorting,
labelling, counting, reading a number or a screen back, holding a part steady, cleaning a panel
or pressing a button. **Never** on a step that involves mains (Ch 00a, Ch 09's inlet / WAGO /
PSU / SSR steps, Ch 10's mains-side wiring and power-on checks), the soldering iron or heat-set
inserts (00.13–00.16, 02.03–02.04, 08.3–08.7 and every other insert step), a blade or cutter, or
a hot chamber, bed, nozzle or freshly-pulled plate. The build enforces this: a `**Helper:**` line in
a step listed in `NO_MASCOT_STEPS` (`hooks/mascot.py`) fails it. **One exception** (Alex,
2026-09-24): the unplugged meter sweep 10.74–10.78 (`HELPER_RECORD_ONLY`), where the helper
records the readings the adult calls out and the adult holds the probes. Its job text must contain
"record"; the badge stays stripped on the listed steps. If the safe part of a step is only a fraction
of it, leave the step untagged rather than splitting it: **steps are never split or renumbered.**

**What the build does with it.** `scripts/build_steps.py` renders the job as a
`<p class="step-helper">` line directly under Check, adds a `with a helper` badge
(`.step-helper-badge`) beside the step counter, marks the step's tile on the chapter overview
(`.step-card--helper` / `.step-card__helper`), and puts a `Helper steps: N` line
(`.step-helper-list`) on the chapter's start page. `scripts/build_tonight.py` adds a
`## With a helper` section listing every segment that carries one, and suffixes each planner
bucket line with `· helper: <job>`.

**Lint.** `scripts/lint_manual.py` check 5 enforces the budget, the position (it must follow
Check) and the em-dash / parenthetical rules; `--json` reports them as `words`, `em-dash`,
`parenthetical` and `helper-position` findings.

## Parts grammar (added 2026-09-24, wave 4)

`scripts/parts.py` owns the parse, the counts, the kit-BOM resolve and checks 6–7; `build_steps.py`
and `lint_manual.py` only call it. Assembly chapters (00–14) write every `**Parts:**` field as
`**Parts:** none.` or the list form: the label alone, a blank line, one bullet per item.

    **Parts:**

    - M3×40 SHCS ×24
    - `[a]_z_drive_baseplate_a` ×2
    - staged: roll-in M5 T-nut ×4
    - reused: the four belted shaft assemblies
    - tool: 2.5 mm hex key
    - consumable: masking tape
    - M3 heat-set insert ×7 — from KADRICK kit

- **One item per bullet, counted with the step total** (`×N`): a step that closes four drives says
  ×24, not ×6. `per` / `each` belongs in Do. A `×` inside a dimension (`M3×8`) or a code span is
  never a count.
- **Sourced.** Each counted item is a kit BOM row, a printed STL in backticks (bin from
  `assets/parts/MANIFEST.csv`), or ends `— from <source>` (anything the kit does not ship). **The
  kit box is never typed**: it resolves from `scripts/data/ldo-350-bom.yml`, LDO's pinned 350
  Rev D BOM vendored by `scripts/kit_bom.py`; re-pin it to the batch sheet on kit day (Step 00.2).
  Spelling aliases live in `kit_bom.ALIASES`; fasteners, nuts, T-nuts and inserts need none.
- **Roles** (prefix): `staged:` taken out and set aside for a later step (unpack, inspect, set,
  trim, bag); `reused:` fitted earlier and touched again. Neither is summed, and neither cites a
  step number. `tool:` and `consumable:` are gathered apart and never reconciled; the map's
  `unreconciled:` rows (zip ties, VHB, foam tape, belt stock, ferrules…) must carry one of them.
- **Print chapters** (B00–B11) keep the single-line form, `;` then `·` separated:
  `build_tonight.py` and `slicer/check_docs.py` read their Load-step lines.

**Consumption and ownership.** A kit unit is consumed once, at the step that first mounts,
fastens, presses, glues, solders or plugs it in; that step counts it. Earlier mentions are
`staged:`, later ones `reused:`. Ch 00 is inventory and never counts. A chapter's **Hardware**
table counts its own consumption, one kit item per row, the Qty cell leading with the total
(`24`, or `60: 24 drives + 36 Z rails`). Units bagged in one chapter for another are a `carries:`
entry in `scripts/data/hardware-ownership.yml` (the consuming table writes `0: bagged at Step …`);
the same map fixes the step that fits each cross-chapter unit. Rule and per-row evidence:
`review/2026-09-23-sweep/HARDWARE-OWNERSHIP.md`. New hardware on a later step is a counted part,
never `reused:`.

**Checks.** `lint_manual.py` check 6 is the grammar (`single-line`, `no-count`, `per-unit`,
`multi-item`, `unresolved`, `unreconciled-row`, `staged-xref`/`reused-xref`); check 7 reconciles
step totals against each chapter's Hardware table and, across the manual, flags `double-count`,
`owner-missing`, `fake-reuse`, `staged-unfitted`, `carry-unstaged`/`carry-unfitted`, `over-bom`
and `map-error`. Both fail the default run for the assembly chapters (`PARTS_CHECKS_FAIL`, on since
wave 4 phase 5); print chapters are never scanned. **Strict mode**, the per-chapter gate: `python3 scripts/lint_manual.py --strict-parts
--chapters 09,10` exits 1 on any check 6/7 finding in those chapters (a cross-chapter finding is
filed under the chapter that holds the step). `--parts-report [chapter …]` lists every finding;
`python3 scripts/parts.py --ledger '<BOM regex>'` prints every mention of a kit row in manual
order with its role, count and Source line, so equal totals cannot hide a wrong step.

## Panel crops (added 2026-09-24, wave 4)

A step that acts on one panel of a multi-panel page shows that panel, larger. Add
`{ crop="x0 y0 x1 y1" }` (page fractions) directly after the image:
`![Voron manual p.NN](assets/manual-pages/manual-pNNN.png){ crop="0.12 0.14 0.62 0.72" }`
(`sb-pages/sb-pNNN.png` too). Pick the box on `python3 scripts/crop_panels.py --sheet pNNN` (a
10 % grid), render it with `--render pNNN --box 0.12 0.14 0.62 0.72` into
`assets/manual-crops/pNNN-<hash8>.png` (named from page + box, so two writers agree), and commit
the PNG; `--sheet`/`--render` need the gitignored source PDFs. The step page shows the crop with
a **Full page** link; the long chapter page keeps the whole page. The build fails on a declared
crop whose PNG is missing and on a crop written where `crop_panels.py --check` cannot see it (a
print chapter, another image path). `--check` needs no PDF: it exits 1 on a missing PNG and lists
orphan PNGs no chapter declares.

## Checkpoint reward (added 2026-09-24, wave 4)

Each assembly `## Checkpoint` carries one `**Built:** <what now exists>` line: at most 12 words,
no em-dash, no parenthetical, no leading "You built". The build renders it at the end of the
Checkpoint (step page and long page) as Revali's `pass` scene captioned "You built X. N gummy
worms."; the line itself is not shown. N is one worm per 30 min of the chapter's
`**Sessions:**` time (else the `Time:` midpoint), split across a chapter's Checkpoints by their
Pause segments, at least one each. Two `**Built:**` lines in one Checkpoint fail the build.
Without one the caption is "Checkpoint NN passed. N gummy worms.", and lint check 8 fails
(`BUILT_REQUIRED`, on since wave 4 phase 5). Print-batch Checkpoints take no `**Built:**` line (it fails
the build): their caption is generated from `slicer/plates.py` ("Batch Bnn printed: plates … of
22, … of 157.0 h."), one worm per plate. Checkpoint 00a's reward is the caption
alone, no bird (`REWARD_TEXT_ONLY` in `hooks/mascot.py`); Checkpoint 10 gets the bird.

## Bench photos (added 2026-09-05, evening)
Alex's own photos, taken at the bench and filed by `scripts/ingest_photos.py` — not mirrored
third-party material (that's `assets/remote/`, above). Workflow: photograph a step on the iPad,
let it land via iCloud Photos/AirDrop in the drop folder (`~/Pictures/voron-drop` by default),
then run one command to file it.
- **Step id in the filename:** `NN.M[-n].jpg` (e.g. `10.58-2.jpg`, `00a.5.heic`) — `NN.M` is the
  step id, `-n` an optional shot number within that step. No filename match? Use `--step NN.M` on
  the command to apply one step id to every file in that run, or drop a sidecar note file next to
  the photo (`IMG_1234.jpg` + `IMG_1234.txt`, first line the step id, optional `caption: <text>`
  line).
- **Destination:** `docs/manual/assets/photos/<chapter-slug>/<step>-<n>.jpg` (chapter-slug matches
  the chapter's own filename stem, e.g. `10-wiring`) — resized to max 1600 px on the long edge,
  EXIF stripped (no GPS), JPEG q85. `<chapter-slug>/captions.yml` optionally maps filename to a
  one-line caption; no `SOURCES.txt` needed (this is Alex's own work, not mirrored material).
- **Chapter markdown:** the tool inserts `![Bench photo — Step NN.M](assets/photos/<chapter-slug>/<step>-<n>.jpg)`
  immediately after the step's existing image line(s), so the CAD render/manual page and the real
  photo sit together. Never hand-place this line — re-running the tool is idempotent (a source
  already ingested is moved to `<drop>/.ingested/`; an existing destination file is never
  overwritten) and will just skip it.
- **Command:** `python3 scripts/ingest_photos.py [--drop DIR] [--step NN.M] [--dry-run]` from the
  repo root (`pip install -r requirements-photos.txt` first; HEIC needs `pillow-heif`, an optional
  dependency — plain JPEG/PNG work without it).
- **What's still missing:** `python3 scripts/photo_wanted.py` prints every step still showing
  `(no image — see text)`, as a checklist. Optional tooling only — Alex's 2026-09-06 ruling is
  that this is a manual to build from, not a record, so no step asks for a photo.

## Image licensing (updated 2026-09-05, evening)
Alex's ruling: LDO documentation images and the Nitehawk-SB V2 / Leviathan / LDOVoron2 repo images MAY be mirrored into `docs/manual/assets/` for this non-commercial, attributed manual. Every mirrored image is listed in the folder's `SOURCES.txt` (file → URL → owner → date) and the README attribution names LDO Motors. Voron/Klipper (GPL-3.0) as before. Ellis' guide: still link-only (no licence). Keep the original URL in the step's Source line.

## Step pages (added 2026-09-06 — Alex: "one page per step like Prusa's help site")

`scripts/build_steps.py` runs as an mkdocs `on_pre_build` hook and regenerates
`docs/manual/steps/` from the chapters on every build. **The chapters stay the single
source; never hand-edit anything under `steps/`** (the directory is gitignored, rebuilt by
CI's `mkdocs build`, and any file whose source step disappears is deleted on the next run).

**What the parser needs from a chapter.** Everything below is already the house style; the
generator only formalises it.

- `# Chapter NN — Title` (or `# Batch BNN — Title`) as the one h1. Everything between it and
  the first step becomes the chapter's **"Before you start"** page and the overview's Time /
  Sessions line.
- `### Step NN.M — title` opens a step and runs to the next `###`/`##`. A `##` step heading is
  accepted too — that is how the print-batch chapters are written — so no chapter needed
  editing for this. Step ids stay globally unique: they are the progress key and the page name
  (`04.2` → `steps/04-ab-drives/04-2/`, `06b.14` → `06b-14`, `B03.1` → `b03-1`).
- `## Checkpoint NN` becomes a page of its own that ends the chapter (or the part — Ch 06 has
  two). `## Common mistakes` and `## Next` ride on the last page.
- Any other `##` is a **section**: its title becomes the breadcrumb on the steps beneath it. If
  it carries body text and no steps follow before the next section or the Checkpoint (Ch 11's
  ⛔ stop gate, Ch 13's "What if"), it becomes its own page rather than being dropped.
- Headings inside fenced code (Ch 12's `printer.cfg`) are ignored.

**What the generator does to a step block.** Images are hoisted to the top with the manual-page
render first and the part renders and diagrams after. The text column is then re-ordered
action-first — **Do:** → **Check:** → **Helper:** → Gather → **Parts:** → the collapsed
`What you're looking at` block → `⚠`/`Tip:` → `Pause:` → `Source:` → **Next:** — regardless of where those lines sit in the chapter (see
"Action-first steps and word budgets"). A manual-page or panel-crop figure gets a muted "Tap to
enlarge" line under it (glightbox opens every figure image zoomable). A step whose code block
runs to 12+ lines (or 5+ lines with one over 72 characters; `gate-calc`, `tap-tree` and `mascot`
fences are widgets, not code) renders stacked in landscape too (`.step-body--wide`): the picture on
top at 40vh, then the text and code full width, so a config block never scrolls sideways in the
half-width column. A list or code block directly under a Do line rides with
it; a table, code block or blockquote and the paragraph beside it stay visible; every other loose
paragraph joins the collapsed block. `**Parts:**` becomes a compact list (the list form's bullets;
a single-line field splits on `;`, then `·`), each item carrying the part render from
`assets/parts/MANIFEST.csv` when it names an STL in backticks, and a muted note saying where it
comes from: bin, kit box, `— from` source, `tool`/`consumable`, "set out now, fitted later"
(`staged:`) or "already on the bench" (`reused:`). An image line with a `crop=` box shows its
panel crop (§ Panel crops). `(no image — …)` renders as a neutral placeholder. Every relative link is re-resolved
for the new depth; `chapter.md#step-…` retargets that step's page and a bare `chapter.md`
retargets that chapter's overview.

**Gather for this segment** (added 2026-09-14, after Prusa's kit guide, which spends ~39 % of
its steps on staging parts). **Generated — never hand-write a gather list in a chapter.** A
*segment* is the run of steps from the step after a `Pause:` line (or the chapter's first step)
through the next step that carries one; the trailing run after the last `Pause:` is a segment too.
For each segment the generator sums every `**Parts:**` item across its steps and renders it twice:

- on the segment's **first step page**, as a collapsed `??? note` titled
  `Gather for this segment — steps 02.05–02.08 (~25 min)`, placed after the **Do:**, **Check:**
  and **Helper:** lines and before that step's own **Parts:** list — hardware first, then printed parts, one item per line
  with the summed count;
- on the **chapter overview**, as one line per segment under the step grid ("Gather per session"),
  so a session can be laid out before it starts.

Minutes come from the closing `Pause:` line and are omitted where it carries none. Counts are read
from `×N` / `N×` / `xN` / `(N)`; an item with no count counts as 1 and prints without a quantity; a
`×` inside a dimension (`M3×8`, `Ø4.7 × 5 mm`) or inside a `code span` (`z_rail_stop_x4`) is never a
count. Items merge case- and whitespace-insensitively, so the same fastener named twice in a
segment shows one summed line. An item is a *printed part* when it names an STL in backticks that
`assets/parts/MANIFEST.csv` knows, and then carries `— from bin NN` from that manifest's `bin`
column (a bin id written into the Parts text is honoured too). A Parts item the count parser cannot
read is listed **verbatim** rather than dropped, and named in the build log
(`mkdocs build` INFO, or the `warn:` lines from `python3 scripts/build_steps.py`) so the chapter can
be tightened. A segment with nothing to gather gets no block on the step page and a
"nothing to lay out" line on the overview. A segment that holds any list-form Parts field is
**grouped by source** instead: kit boxes in BOM order, hand-named sources, other hardware, printed
parts by bin, tools and consumables, set out for later (`staged:`), already on the bench
(`reused:`). Kit items merge by BOM row, so two spellings of one fastener meet. Within one segment:
a `staged:` item that a later step fits is listed only under its box (a partial fit leaves the
remainder under "set out for later"); `reused:` lines are listed once and never summed; a `tool:` is
listed once, at the most any one step needs; a `consumable:` sums its counts, a quantity in its name
("about 25 g") counts one portion per step, and a bare name is listed once.

**Chapter progress figure.** Where `docs/manual/assets/cad/ch-NN-after.png` exists — one
cumulative "state at the end of this chapter" CAD render per assembly chapter, built by
`scripts/cad_render/render_steps.py --chapters` from the `chapters:` list in
`assets/cad/steps.yml` — the chapter overview opens with a **"What this chapter builds"**
figure (the previous rendered chapter's image on the left, this chapter's on the right, new
parts orange and earlier parts grey), and the chapter's own Checkpoint page repeats that
image under "What you should have now". Chapters the CAD cannot show — 10 (wiring) and
12–14 (software, startup, calibration) — have no PNG and get no figure, and Ch 06's second
Checkpoint (06b) does not repeat Ch 06's.

The words under both figures are the entry's own `caption` and `note_350`, so a render's
caveats are on the page rather than buried in the manifest, and each render has to show the
end state its chapter's Checkpoint describes — Ch 04 and Ch 05 end with a subassembly on the
bench and the machine untouched, so those two entries carry `frame: null` and `context:` and
show the assemblies alone.

**Navigation.** `docs/.nav.yml` owns the whole nav — five tabs (Home / Build / Print / Plan /
Reference), with the sidebar showing only the active tab's pages. Build and Print list chapter and
batch overviews only; add a row there when a chapter is added (`steps/.nav.yml` carries
`hide: true`). Step pages are built and searchable but out of nav, and prev/next comes from the
generated markup, never from nav order. Search finds a step on its step page only: the long
chapter page's step headings carry `data-search-exclude` (`build_steps.on_page_content`), so
`10.58` lands on the page with the done toggle; the long page's intro, section headings,
Checkpoint and Common mistakes stay searchable.

**Pre-kit badge.** A step inside a segment whose closing `Pause:` carries `(pre-kit)` (the tag
`scripts/build_tonight.py` plans "Before the kit" from) gets a `pre-kit` badge on its overview tile
(`.step-card__prekit`) and beside its step counter (`.step-prekit-badge`). Nothing is hand-marked:
tag the Pause line and the badges follow. Each overview
links to the long chapter page ("Read the whole chapter on one page") and every long chapter page
gets a banner back to its overview.

**Next overrides.** Prev/next follow file order unless one of three lines says otherwise
(`scripts/build_steps.py`; only the first link counts, and only when its anchor is a step heading):

- a chapter's `## Next` section that **leads** with a step link sends the chapter's last page there
  (Ch 12 → Step 11.67). A lead link to a chapter or a non-step anchor changes nothing;
- a `## Checkpoint` whose body carries `**Next:** [text](chapter.md#step-anchor)` sends that
  Checkpoint page's Next button there (Checkpoint 06 → Ch 07, Checkpoint 06b → 13.35,
  Checkpoint 13 → Ch 11 Part B). The line stays visible in the checklist;
- a **step** may end with the same `**Next:**` line (13.34 → 06b.1). It renders after `Source:`
  and overrides that step page's Next button. It is navigation, like `Source:`, so its link does
  not count against the step's one cross-reference.

Use one wherever the bench order in `00-index.md` leaves the file order.

**Progress** is keyed `chapter-slug` + `step id`, so one tick is the same tick on the step page,
the overview grid and the long chapter page.

## Interactive fences

**The mascot (added 2026-09-15).** `hooks/mascot.py` owns a ` ```mascot ` fence and runs on `on_page_markdown` for every page, so — like the two fences above — a scene written in a chapter renders identically in the step page `build_steps.py` copies it into; the hook works the asset path out from the page's own URL, so the same fence resolves to `../assets/mascot/…` on the chapter page and `../../../assets/mascot/…` on its step page. The fence is YAML with two keys and an optional third:

    ```mascot
    pose: hexkey
    caption: Square the frame once, properly.
    side: left
    ```

`pose:` is one of the twenty files in `assets/mascot/` without its `mascot-` prefix and `.svg` suffix (`base`, `base-3q`, `base-front`, `badge`, `cable`, `caliper`, `carry`, `check`, `fail`, `gather`, `helper`, `hexkey`, `kitday`, `pass`, `pause`, `point`, `print`, `screen`, `tip`, `warn`); `assets/mascot/STYLE.md` § *Where each pose belongs* says which moment each one is for. `caption:` is at most **18 words**, with no em-dash and no parenthetical — the same prose rule the Do and Check budgets follow. `side:` is `left` or `right` and defaults to right; the figure floats there on a wide screen and stacks on a phone. An unknown pose, an over-long caption or an unknown key fails the build with the page name.

**Where the bird may and may not go.** The five neutral badges are placed by the generators, never by hand: `hooks/callouts.py` puts one in the **title row** of every Check, Tip and `Pause:` box, and `scripts/build_steps.py` puts one on the *Gather for this segment* block and on the `**Helper:**` line. A badge is punctuation in a title, so it never costs a word budget and never appears inside a Do, Check, Tip or `⚠` text run. Three rules are enforced rather than trusted, and one is not:

- **`⚠` boxes carry no mascot.** `callouts.py` badges `success` / `tip` / `info` and deliberately not `warning`.
- **`pose: warn`** — the hard hat — is rejected on any page but `00a-mains-safety`.
- **No mascot at all** on mains, soldering-iron, blade or hot-chamber content. There is no pose for those and there will not be one; that is the humour rule, not an oversight. The steps are an explicit id list, `NO_MASCOT_STEPS` in `hooks/mascot.py` (the one place that classifies them): the hook strips every badge inside a listed step, on its step page and on the long chapter page, and fails the build on a ` ```mascot ` fence inside one. An appended step of one of those kinds goes into that list.
- **One scene per page** is a judgement call the fence does not police. Home is the deliberate exception.

Captions are dry and kind, and the bird never makes the mistake: it watches, checks, shrugs alongside you. No speech, no puns, no `⚠` gags. Everything else about the art — palette, views, the two-wing rule, regeneration — is in `assets/mascot/STYLE.md`, and `scripts/gen_mascot.py` is the only thing that writes an SVG.


**Gate calculators and tap-through trees (added 2026-09-14).** `hooks/gatecalc.py` runs on `on_page_markdown` for every page, so both fences work in a chapter *and* in the step page `build_steps.py` copies it into. A ` ```gate-calc ` fence is YAML: `id:` (the `gate-calc:<id>` storage key, shared by every page that carries the same fence), `title:`, `pass:`, and an `inputs:` list. Each input needs `key:` and `label:`, plus exactly one shape — `nominal:` + `tol:` for a band, `min:` / `max:` for a one-sided limit, or `kind: yesno` for a toggle. A number row carries `low:` and/or `high:` advice; a yes/no row carries `no:` (or `yes:`) — whichever is present is the *failing* side. `optional: true` lets a row stay blank without holding up the verdict, but it still fails the gate if answered and failing (that is how B00.7's two kit-day rows work). `hint:` overrides the generated "30 ±0.15" / "≤ 0.15" line. `why:` is one sentence on what that row protects ("Every bearing bore in the build inherits this number"), rendered as a collapsed `why?` toggle under the row and never part of the verdict. A fence-level `derive:` (`expr:` over the fence's own number keys, with `label:` and `digits:`) shows one computed number beside the badge — Step 14.18's pressure advance is `start + stepv * line` — and the hook whitelists the expression to those keys, digits and `+ - * / ( ) .` so the JS can evaluate it. The hook emits the normalised spec as JSON in a `data-gate-calc` attribute, so `gatecalc.js` knows nothing about any particular gate; bad YAML, a missing key or a shapeless row fails the build with the page name. Put the fence after the step's **Check:** field, blank-line separated; lint check 5 skips fenced content, so it costs no word budget. A ` ```tap-tree ` fence holds a plain nested markdown list, 4 spaces per level — level 1 the phase, level 2 the symptom, level 3 what you see, and a blank-line-separated indented paragraph under an item as its leaf (one sentence plus the same step links the index already gives). The hook only wraps it in `<div class="tap-tree" markdown="1">`, so Python-Markdown renders an ordinary list and mkdocs rewrites and validates every relative link; `taptree.js` then turns it into cards and hides the list, and with JS off the list is the fallback. Never put `⚠` / `Tip:` / `Check:` / `Source:` / `Pause:` text in a leaf — it renders outside an admonition and lint check 1 flags it.
