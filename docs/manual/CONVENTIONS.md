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
7. Colour cells use exactly `Black` or `Orange` (add `(opaque)` where the STL is `[o]_`); the filament identity lives once, in print plan §1.2.

## Steps
- `### Step NN.M — short imperative title`
- Image line first: `![Voron manual p.XX](assets/manual-pages/manual-pXXX.png)` or an LDO image URL, or `(no image — see text)`.
- **Parts:** exact fasteners/parts for THIS step, qty.
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
`scripts/lint_manual.py` runs in CI, after `mkdocs build --strict`. Five checks (the fifth, step word budgets, is in § Action-first steps; `--budgets-only` runs it alone, `--no-budgets` skips it): raw `⚠` / `**Check:**` / `Tip:` text outside an admonition or `<code>`/`<pre>` block; `Step NN.M` references with no matching heading; STL filenames in an assembly-chapter table with no matching print-batch table row (exempt: a row containing `not printed`, `kit-supplied`, or `SKIP`, case-insensitive); Markdown tables wider than 7 columns (exempt: tables under a heading whose text contains "Machine-readable").

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
**Parts:** → **Check:** → a collapsed `What you're looking at` block → `⚠`/`Tip:` → `Pause:` →
`Source:`. Images stay hoisted to the figure column. Write a step in house order as before; the
generator moves it.

**Budgets** (words, excluding images, code, inline `code` spans and link URLs):

| Field | Budget |
|---|---|
| **Do:** (plus its list/continuation lines) | 40 |
| **Check:** | 25 |
| **What you're looking at:** | 45 |
| `Tip:` | 30 |
| `⚠` callout, each | 60 |

Also, in Do / Check / description: **no em-dash** (`—`), and **no parenthetical** except the two
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
action-first — **Do:** → **Parts:** → **Check:** → the collapsed `What you're looking at` block →
`⚠`/`Tip:` → `Pause:` → `Source:` — regardless of where those lines sit in the chapter (see
"Action-first steps and word budgets"). A list or code block directly under a Do line rides with
it; a table, code block or blockquote and the paragraph beside it stay visible; every other loose
paragraph joins the collapsed block. `**Parts:**` becomes a compact list (split on `;`, then `·`),
each item carrying the part render from `assets/parts/MANIFEST.csv` when it names an STL in
backticks. `(no image — …)` renders as a neutral placeholder. Every relative link is re-resolved
for the new depth; `chapter.md#step-…` retargets that step's page and a bare `chapter.md`
retargets that chapter's overview.

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
generated markup, never from nav order. Each overview
links to the long chapter page ("Read the whole chapter on one page") and every long chapter page
gets a banner back to its overview.

**Progress** is keyed `chapter-slug` + `step id`, so one tick is the same tick on the step page,
the overview grid and the long chapter page.
