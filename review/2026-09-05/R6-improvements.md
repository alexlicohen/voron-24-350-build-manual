# R6 — Improvements to the manual and the system around it

Read-only review, 2026-09-05. Baseline measured, not assumed: 641 numbered steps across 15 assembly
chapters + 12 print chapters; `mkdocs build --strict` passes; live site walked with Playwright at
1024×768 (Ch 00 / 05 / 06 / 08 / 10, print/B01).

Effort scale: **S** ≤ 2 h · **M** 2–8 h · **L** > 8 h.

Recommendations already implemented in the repo are **not** listed. Verified-as-done and therefore
dropped: a single-plate calibration coupon set (`print/B00`, seven-item gate), runout-aware plate
ordering (`print/README.md` — "Spool #1 runs out inside B07 … let it happen mid-plate except B01-P1"),
`_x#`/`[a]_`/`[o]_`/`[c]_` colour key, per-chapter Checkpoint + Common-mistakes sections, the
corrections log, the interleaved print/build timeline, and per-step `[src]` citation.

---

## Top 10 by value ÷ effort

| # | Improvement | Cat | Effort | Value |
|---:|---|---|---|---|
| 1 | Enable `pymdownx.tasklist` — **every Checkpoint checkbox in the manual currently renders as literal `[ ]` text** | 2 | S · 0.25 h | H |
| 2 | Fix the press-fit gate contradiction: `print/00-slicer-setup.md` names **F695 / 13 mm** where the Z drive takes **625-2RS / 16 mm** | 4 | S · 0.5 h | H |
| 3 | Pin PrusaSlicer **2.9.6** for the whole Voron run; declare a slicer change as invalidating the B00 gate | 4 | S · 0.5 h | H |
| 4 | GitHub Actions: `build --strict` + `validation.links.anchors: warn` + auto `gh-deploy` (site is **already stale vs `main`**) | 3 | S · 2 h | H |
| 5 | Render + commit the **Stealthburner manual pages** — 44 of Ch 08's 67 steps say "not embedded" | 1 | S · 2 h | H |
| 6 | Harden `hooks/callouts.py` for hard-wrapped bodies + add a lint — **22 callouts are silently truncated today** | 3 | M · 2 h | H |
| 7 | Mirror the **79 hot-linked step images** into `docs/manual/assets/` | 2 | M · 3 h | H |
| 8 | Mains-safety chapter (Ch 00a) with the "who is in the room" rule | 1 | M · 3 h | H |
| 9 | Per-step progress in `localStorage` + "resume where you left off" | 2 | M · 5 h | H |
| 10 | Commit a PrusaSlicer project per plate + the config bundle | 4 | M · 6 h | H |

**Flag for the content tracks:** item 2 is a BLOCKER-class factual error, not a process improvement —
see §4 P6. It should be routed to whichever track owns corrections regardless of what happens to this list.

---

## 1 · Content gaps

### C1 — Render and commit the Stealthburner manual pages · S (2 h) · **H**
**Why.** `docs/manual/08-toolhead.md` contains **44 occurrences** of `(SB manual p.NN, not embedded)` —
Steps 08.2 through 08.52 (p.11–p.67). The chapter has **67 steps and 5 images**; every other transcribed
chapter is 79–100 % illustrated (Ch 02: 44/47, Ch 04: 38/38). The Stealthburner PDF is neither committed,
nor rendered, nor even given a URL at the point of use — so 08.3 ("SB p.11–12 highlight **three** locations
… p.13 adds a **fourth**") asks the builder to compare against a page they cannot see. Ch 08 is also where
five of the six Rev D+ deltas land (its own "Read first" says so).
**Deciding criterion.** The toolhead is the highest fastener-density, lowest-illustration chapter in the
build; it is where a wrong insert costs a full extruder teardown (survey W3, cited at 08 "Read first").
**Sketch.** Same pipeline the Voron manual already uses (`README.md`): `curl` the Stealthburner assembly
manual at a pinned commit → `pdftoppm -png -r 110 … assets/sb-pages/sb-p`, gitignore the PDF, then replace
each `(SB manual p.NN, not embedded)` with `![Stealthburner manual p.NN](assets/sb-pages/sb-pNNN.png)`.
Add the GPL-3.0 attribution row to `README.md` beside the existing VoronDesign one.

### C2 — Mains-safety chapter (Ch 00a) · M (3 h) · **H**
**Why.** Mains safety exists only as a bullet inside Ch 10's "Read first" ("Mains is the one step in this
build that can kill you") and as ⚠ callouts distributed across Steps 10.2–10.23. There is no page that says,
*before* the builder reaches Ch 10: what a multimeter must be able to do, that a certified electrician may be
required, that the C13 cord leaves the room, and — for this build specifically — **who is allowed in the room
during §1 and §2**. Ch 00.30 explicitly assigns the daughter the camera and the measurement log; nothing
carves out the mains sections. `00-before-you-start.md` Step 00.8 lists a multimeter as "Buy if not owned"
in a 13-row tool table, three chapters and ~500 steps before it becomes mandatory.
**Deciding criterion.** Every other safety-critical fact in this manual is stated *before* the step that needs
it (rails greased in Ch 00, backers fitted in Ch 05, T-nuts pre-loaded at 05.14). Mains is the only one that
is not — and it is the only one that is irreversible.
**Sketch.** New `docs/manual/00a-safety.md`, 8–12 steps: supply type and RCD/GFCI, meter minimum spec and its
own self-test, the "cord in another room" rule, what to do if the breaker trips, when to stop and call
someone certified, and a `⚠` naming the two Ch 10 sections a 13-year-old is not present for. Link it from the
timeline row 22 and from Ch 10's "Read first". No new tooling.

### C3 — Troubleshooting index · M (4 h) · **H**
**Why.** The raw material is already written and is unreachable at the bench. There are 15 `## Common
mistakes` sections, ~198 `⚠` callouts, and 27 Checkpoint lists — all filed by *chapter*, none by *symptom*.
A builder at 23:00 has "QGL won't converge" or "the X carriage binds near one end", not "Chapter 06b". Today
that means full-text search across an 85,000-px page.
**Deciding criterion.** The manual's own structure proves the need: Ch 05 Step 05.44 already diagnoses by
symptom ("A tight spot near one end usually means a rail is not centred; a general stiffness that grows
towards one end usually means the gantry is racked"). That reasoning is invisible unless you are already on
that step.
**Sketch.** `docs/manual/99-troubleshooting.md`, a two-column symptom → step table generated by a script that
harvests `## Common mistakes` bullets and `⚠` first sentences and emits deep links (`05-gantry.md#step-0544`).
Regenerate in CI so it cannot drift.

### C4 — Session-planning view ("what can I do in 2 hours tonight") · M (4 h) · **H**
**Why.** Every chapter carries a machine-readable `**Time:**` line (15/15) and `00-index.md` holds a
30-row dependency-ordered timeline with per-row hours. The index's own assumption is *"2 h on each of five
weekdays, 6 h on each of two weekend days"* — but no chapter is 2 h. They are 2.5–7.0 h, and Ch 02, 05 and
10 are 5.0–7.0 h. Nothing marks a safe stopping point. Some steps make stopping *unsafe*: Ch 10 Step 10.71
("Leave the duct covers off") and Ch 05 Step 05.47 ("no belts, no squaring") are deliberate suspended states
that must be understood before you walk away.
**Deciding criterion.** The single largest scheduling risk in this build is starting a 5-hour chapter on a
weeknight and stopping mid-gantry. The data to prevent it already exists; only the view is missing.
**Sketch.** Add `pause_ok: true` markers (an HTML comment or an `attr_list` class) at natural boundaries —
Ch 05's section ends, Ch 10's section ends — and generate `docs/manual/00-tonight.md`: "you have 2 h and
you're at Step 05.17 → finish through 05.24, stop there; do not start 05.25". A mkdocs hook can emit it at
build time from the existing `Time:` fields plus the markers.

### C5 — First-month / maintenance chapter · M (3 h) · **M**
**Why.** The manual ends at Ch 14 (tuning). Facts that imply a maintenance schedule are already scattered
through it and never collected: rails greased in Ch 00.19 with no re-grease interval; every fastener taken to
"snug, not torqued" (05.7, 05.9, 05.23) with no re-torque pass; belts set "provisional" in Ch 07 and again at
Ch 14.4; the Advanced Filtration cartridge rated ~600 print-hours in `CLAUDE.md` with no reorder trigger in
any chapter. Ch 10's own warning — cables in chains "will survive assembly and fail in three months" — has
no follow-up inspection step anywhere.
**Deciding criterion.** The stated goal is a manual that *stays* valid. A build manual that stops at first
calibration cannot; the 10-hour and 100-hour re-checks are where a Voron either settles or drifts.
**Sketch.** `docs/manual/15-first-month.md` with three checklists (10 h, 100 h, 500 h) built from the
existing Checkpoint items that are time-sensitive, plus a consumables reorder table.

### C6 — "First prints with your daughter" chapter · S (2 h) · **M**
**Why.** The daughter is a named participant with assigned jobs — Ch 00.14 ("let your daughter do them; this
is the part of the build where practice is free"), Ch 00.30 ("Your daughter owns the camera and the
measurement log — the diagonals in Ch 01 are hers to read out") — and the print plan's preamble says it is
*"Written to be followed with a 13-year-old: one plate = one job."* But after Ch 14's tuning cube the manual
stops, and nothing says what to print on the finished machine. `CLAUDE.md` even ranks PVB first for exactly
this reason ("best 'wow' for daughter").
**Deciding criterion.** This is the payoff the whole 60-hour build is for, and it is the one chapter that
costs nothing to get wrong. Cheap to write, disproportionate value to the actual goal.
**Sketch.** `docs/manual/16-first-prints.md`: 6–10 steps — first ASA benchmark, first PVB print and vapour
smoothing, a chamber-temperature experiment she runs, and a "measure it and log it" step that reuses the
Ch 00.30 measurement log. Same Step/Do/Check format.

### C7 — Mods roadmap · S (2 h) · **M**
**Why.** Four mods are deferred in `CLAUDE.md` (StealthChanger, Beacon, Nevermore StealthMax, chamber
heater) and the manual is *already paying for them* without saying so. Ch 10 Step 10.67: "leave enough slack
at the toolhead that the V2's **secondary USB port stays reachable** … That port is the whole point of the
'+' … designing it out now costs you a re-route later." Ch 08 Step 08.54 has the builder print and bag an
entire Klicky set that is never used. Ch 08.7 leaves two insert holes empty for an ADXL that will never be
fitted. Those are correct decisions with no written destination.
**Deciding criterion.** A deferred-mod decision only pays off if the future step is recorded; otherwise the
bagged Klicky set and the reserved USB slack are just unexplained leftovers in twelve months.
**Sketch.** `docs/manual/98-mods.md`: one row per mod — what the build already reserved for it, which
chapter/step to reopen, what it invalidates (re-QGL, re-tension, re-flash), and the print batch it needs.

### C8 — Glossary · S (1.5 h) · **M**
**Why.** Ch 00 Steps 00.25–00.27 teach the fastener vocabulary once (BHCS/SHCS/FHCS, roll-in T-nut vs
hammerhead, F695 vs 625, shim vs precision spacer) — and then it is used across the next ~600 steps with no
second definition. Terms introduced elsewhere and never defined centrally: QGL, VFA, `nhk:`, PH2.0 vs XH2.5,
E-RV, flip-and-pack, Klicky, blind joint, "second hole in".
**Deciding criterion.** Ch 00.26's own Check is "You can tell an F695 (flanged) from a 625 (plain, larger
bore) on sight" — a claim about memory that the manual then relies on 400 steps later. A glossary makes that
claim recoverable instead of assumed.
**Sketch.** `docs/manual/97-glossary.md`, alphabetical, one line each, each entry deep-linking the step where
it is taught. Add an `abbr`-style pass later if worth it.

### C9 — Step granularity at named steps · M (3 h) · **M**
Not a general weakness — the median step is 3 sentences / 50 words, which matches Prusa. The exceptions are
concentrated and nameable. Details and the full grading in §5.

---

## 2 · Bench usability

### B1 — `pymdownx.tasklist` is missing · S (0.25 h) · **H** — *top pick*
**Why.** Verified in the live DOM at
`https://alexlicohen.github.io/voron-24-350-build-manual/manual/05-gantry/`:
```html
<li>[ ] E extrusion joined to both drive units with 8× M5×10 BHCS; drives parallel, no twist</li>
```
`mkdocs.yml` `markdown_extensions` lists `admonition, pymdownx.details, pymdownx.superfences, attr_list,
md_in_html, tables, toc` — **not** `pymdownx.tasklist`. So every `- [ ]` in the repo renders as the literal
characters `[ ]`. That is **27 checklists**: 15 assembly Checkpoints (Ch 05 alone has 13 items, Ch 00 has 13,
Ch 10 has 12) plus 12 batch Checkpoints. Confirmed on `print/B01` too (`checkboxes: 0`).
**Deciding criterion.** The Checkpoint list is the manual's only hard gate between chapters — Ch 10's says
"Do not start Ch 11 until every line is ticked" — and it is currently un-tickable. One line of config.
**Sketch.** Add to `mkdocs.yml`:
```yaml
  - pymdownx.tasklist:
      custom_checkbox: true
      clickable_checkbox: true
```
This is also the prerequisite for B2.

### B2 — Per-step progress in `localStorage` + resume · M (5 h) · **H**
**Why.** Ch 10 renders **84,930 px tall** (79 steps, ≈110 iPad-landscape screens); Ch 05 is 52,365 px,
Ch 06 51,422, Ch 08 51,645. There is no persisted position, no per-step tick, and no "you are here". At
1024×768 the Material secondary sidebar collapses to a 242 × **48** px box, so the 90-entry step TOC is not
available as a jump list at bench width. Resuming a chapter after a two-day gap means scrolling to find the
last step you remember doing.
**Deciding criterion.** This is a two-people-two-evenings-a-week build over ~5 calendar weeks (index
"Critical path"). Losing your place is the default state, not the exception.
**Sketch.** After B1, a ~60-line `docs/javascripts/progress.js` (`extra_javascript`): give every
`### Step NN.M` heading a checkbox from its `id`, persist `{page: {stepId: true}}` in `localStorage` keyed by
`document.location.pathname`, render "37 / 79 done" in the chapter header, and add a "Resume" link that
scrolls to the first unticked step. Per-device by construction, no backend, no new service. Wire the
Checkpoint checkboxes into the same store so a Checkpoint is a real gate.

### B3 — Mirror the 79 hot-linked images · M (3 h) · **H**
**Why.** Of 413 image references, **79 are external** — 73 from `raw.githubusercontent.com` (LDO's `main`
branch, an unpinned moving target) and 6 from `docs.ldomotors.com`. Ch 10 alone loads **29 external images
of 41**. Every one is a step illustration: `VS9_Final.jpg` is Step 10.1's *target state*; `S4_mapping.jpg` is
the SSR wiring; `psu_switch.jpg` is the 115/230 V selector. The bench read is served from the Mac over LAN
(`scripts/serve.sh`); if the garage has no route to the internet, or LDO reorganises its repo, those steps
lose their picture with no warning. LDO has already changed material twice on record (Leviathan H743
2025-10-30, ESD scheme 2026-07-10 — corrections log rows 5 and 6).
**Deciding criterion.** The repo already made this choice correctly for the Voron manual (263 PNGs committed,
PDF gitignored, source commit pinned in `README.md`). The LDO images are the same problem with a worse
failure mode, because they can change *without* changing.
**Sketch.** A `scripts/fetch-external-images.sh` that walks the markdown, downloads each external image to
`assets/ldo/<sha1-prefix>-<basename>`, rewrites the reference, and records URL + fetch date + sha256 in
`sources.yml` (see V2). `CONVENTIONS.md` line 8 says "link by URL (don't download) unless the survey §7.4
says the license allows embedding" — so this needs the licence call made first; if embedding is not
permissible for some, keep the URL *and* add a locally-cached fallback plus a link-checker (V3).

### B4 — Lazy-load and size the images · S (1 h) · **M**
**Why.** Measured: Ch 05 pulls **3.7 MB across 26 image requests**, all eager (`loading` attribute absent on
every `img`), largest single asset 276 KB. Natural size is 1287×910; displayed size is 735×520. Ch 10 pulls
2.3 MB. On an iPad on garage Wi-Fi that is the whole chapter's payload before the first step is readable.
**Deciding criterion.** Cheap, no content risk, and it compounds with B3 (mirroring adds ~5 MB of LDO images
to every chapter's eager load if not fixed first).
**Sketch.** `attr_list` is already enabled — either add `{ loading=lazy }` via a small `on_page_markdown`
addition to the existing `hooks/callouts.py`, or a one-line DOM pass in `extra_javascript`. Optionally
re-render `manual-pages` at ~900 px wide (currently 1287 px; 40 MB total) and add a 2× only where detail
matters.

### B5 — Screen keep-awake · S (0.5 h) · **M**
**Why.** `docs/index.md` currently tells the builder to *"enable Guided Access or turn up Auto-Lock so the
screen doesn't sleep mid-step"* — a manual iPadOS setting the user must remember to set and unset. The Screen
Wake Lock API does it automatically and is supported in iOS Safari 16.4+.
**Deciding criterion.** Greasy hands, a 5-hour chapter, and a screen that sleeps every 2 minutes. The manual
already recognises the problem and solves it with a human instruction where a 12-line script will do.
**Sketch.** `docs/javascripts/wakelock.js` in `extra_javascript`: a small toggle in the header that calls
`navigator.wakeLock.request('screen')`, re-acquires on `visibilitychange`, and remembers its state in
`localStorage`. Replace the Guided Access sentence with a pointer to the toggle.

### B6 — Bench-photo workflow · M (5 h) · **H**
**Why.** The manual asks for the photos and has nowhere to put them. Ch 00.30 names **ten specific shots**
"because no published source has them for a Rev D+" — the V2 board both faces, the keyed fan-adapter header
mated, the USB-adapter grounding wire as installed, the titanium backers before torque, the good/bad heat-set
inserts. Step 10.72 says "Rev D+ is undocumented in this configuration — your own photos are the reference
nobody else has." Yet there is no `assets/bench/` directory, no naming convention, no ingest path, and **not
one step references a bench photo**. Ch 08's 43 blind steps are exactly where Alex's own photos would beat any
CAD render.
**Deciding criterion.** The gap this manual uniquely fills is Rev D+, which is undocumented everywhere. Bench
photos are the only asset that can close it, and the manual already commissions them — it just cannot receive
them.
**Sketch.** Convention `assets/bench/ch08/08.07-inserts-rear-printhead.jpg` (chapter dir, step id, slug);
`scripts/ingest-bench-photos.sh` that reads EXIF date, resizes to ≤1200 px, strips GPS, and writes the file;
and a `hooks/` addition that, when `assets/bench/<ch>/<step>.*` exists, renders it **above** the CAD render
with the caption "Ours". Steps then need no edit — the photo appears when it exists. Add a build-time report
of which of Ch 00.30's ten shots are still missing.

### B7 — Printable per-chapter checklist + parts-bin labels · M (4 h) · **M**
**Why.** `printSheets: 0` — the site ships no print stylesheet, so printing a Checkpoint gives you the full
nav, sidebar and every image. Step 00.11 has the builder label **15 chapter bins plus two extras** by hand,
and Step 00.2 says to print the LDO batch BOM page — both jobs the site could produce.
**Deciding criterion.** Paper survives a garage; a tablet propped behind an open electronics bay does not.
Low risk, and the bin-label sheet is a one-time job that pays off across all 26 plates.
**Sketch.** A `print.css` in `extra_css` (`@media print`: hide `.md-sidebar`, `.md-header`, `.md-footer`;
force `.admonition` to page-break-inside: avoid). Add `docs/manual/96-labels.md`: a grid of bin labels
generated from the existing batch→bin table in Step 00.11, each with a QR (client-side, e.g. a pinned
`qrcode.js`) pointing at the chapter anchor. No new service.

### B8 — Tap targets · S (0.5 h) · **L**
**Why.** 11 links per chapter page measure < 24 px tall — the inline `[src](url)` citations, which are the
densest link class in the manual (~600 of them). At the bench with gloves these are effectively unhittable
and easy to hit by accident while scrolling.
**Sketch.** In `extra.css`, give `.md-typeset a[href^="http"]` `display:inline-block; min-height:32px;
padding:4px 2px`, or restyle `[src]` as a small pill. Do not enlarge them enough to break line rhythm.

### B9 — Split or fast-jump the long chapters · M (4 h) · **M**
**Why.** Ch 10 = 84,930 px / 79 steps / 8 sections in one document; Ch 11 = 66 steps; Ch 08 = 67 steps. The
chapters already have internal `## Section N` structure and the index already deep-links to Part A / Part B
anchors in Ch 06 (verified resolving). Nothing exploits that at bench width, where the TOC sidebar collapses.
**Deciding criterion.** Prefer a sticky step-jumper over splitting files — splitting breaks the ~600 existing
cross-references and the corrections-log links, which is the more expensive mistake.
**Sketch.** A small sticky bar (same JS bundle as B2) showing "Step 10.47 · Section 5" with a
type-a-number-to-jump box. Cheaper and safer than re-cutting the files.

---

## 3 · Keeping it valid

### V1 — CI: strict build, anchor validation, auto-deploy · S (2 h) · **H**
**Why.** There is **no `.github/` directory at all**. gh-pages was deployed by hand and is already stale:
`origin/gh-pages` head is `Deployed 23f154e`, while `main` is at `08c680e` — the live site is one commit
behind. Worse, `--strict` does not catch what you'd assume. Verified empirically on a scratch copy:

```
WARNING - Doc file 'manual/00-index.md' contains a link '99-nope.md', but the target ... is not found.
INFO    - Doc file 'manual/00-index.md' contains a link '01-frame.md#this-anchor-does-not-exist',
          but the doc 'manual/01-frame.md' does not contain an anchor '#this-anchor-does-not-exist'.
Aborted with 1 warnings in strict mode!
```
The **missing file** aborts; the **broken anchor is only INFO and passes**. `mkdocs.yml` has no `validation:`
block. The index links to `06-…#part-a-chapter-06-z-axis-mechanical` and `#part-b-…`, and chapters cross-link
by step anchor throughout — a renamed heading would break silently.
**Deciding criterion.** Every other recommendation here assumes the site builds and deploys itself. This is
the foundation, it is two hours, and it is currently absent.
**Sketch.** `.github/workflows/docs.yml` — on push to `main`: `pip install -r requirements.txt`,
`mkdocs build --strict`, then deploy via `actions/deploy-pages` (drop the `gh-pages` branch, or keep
`gh-deploy --force`). Add to `mkdocs.yml`:
```yaml
validation:
  links:
    anchors: warn
    not_found: warn
    unrecognized_links: warn
```
Add `lychee` or `linkchecker` on a schedule (not on every push — ~600 external URLs will rate-limit).

### V2 — `sources.yml`: pin every fetched source · M (4 h) · **H**
**Why.** External-link inventory: **250 links to `docs.ldomotors.com`**, 90 `github.com`, 85
`raw.githubusercontent.com`, 46 `docs.vorondesign.com`, 34 `ldomotion.com`, 25 `ellis3dp.com`. Exactly one
source in the whole repo is pinned: the Voron manual at commit `de7e89d` (`README.md`). Everything else is a
bare URL to a living page. The corrections log documents two sources that already moved under this manual
(row 5: Leviathan STM32H743 change 2025-10-30; row 6: ESD scheme documented 2026-07-10) — proof the risk is
real, not theoretical. Meanwhile `print/00-slicer-setup.md` tells the *builder* to "record the commit SHA in
a text file next to your STLs" — the right discipline, applied to the builder's files and not to the repo's
own sources.
**Deciding criterion.** The stated goal is a manual that stays updated. You cannot detect that a source
changed if you never recorded what it said.
**Sketch.** `sources.yml` at repo root: one entry per distinct source — `url`, `kind` (page | raw | repo),
`fetched` (ISO date), `sha256` of the fetched body (or commit SHA for repos), `used_by` (list of
file:step), and `why` (one line). Seed it with a script that harvests the URLs already in the markdown.

### V3 — Scheduled upstream-drift job · M (4 h) · **H**
**Why.** The three sources this manual is most exposed to are the three that have already moved:
LDO's Rev D build-FAQ / wiring guide (250 links), the `Nitehawk-SB-V2` repo (source of the V2 connector
pinouts, the partial cover STL and the grounding images), and
`LDOVoron2/Firmware/leviathan-printer-rev-d-sbv2.cfg` (the config Ch 12 is written against, cited by pin name
in Steps 10.39, 10.46, 08.7). A change to any of them invalidates specific numbered steps.
**Deciding criterion.** LDO's docs are the deviation layer this entire manual is built on. Everything else in
the build is pinned or physical; only this layer moves.
**Sketch.** `.github/workflows/upstream-drift.yml`, weekly: for each `sources.yml` entry, re-fetch, compare
`sha256` (or `git ls-remote` for repos), and on a diff open **one** issue titled
`Upstream drift: <source>` whose body lists the `used_by` steps and a unified diff of the text. Requires V2.
Depends on nothing but `curl` + `git` — no new service, no API keys beyond `GITHUB_TOKEN`.

### V4 — Repo lints (four checks, one script) · M (3 h) · **H**
**Why.** Four classes of defect exist in the repo right now that no build step looks for:

1. **Truncated callouts — 22 instances.** `hooks/callouts.py` emits a single indented body line
   (`return f'!!! {kind} "{title}"\n    {body}'`), so any callout whose body hard-wraps loses everything after
   the first line. Verified in the live DOM at `manual/08-toolhead/`:
   ```html
   <div class="admonition warning">
     <p class="admonition-title">Rev D+ / LDO</p>
     <p><strong>use the supplied grounding cable</strong> — LDO warns that larger ring-lug connectors can short</p>
   </div>
   <p>the PCB. <strong>If your kit did not include the grounding cables</strong>, stop and ask in <code>#ldo_motors</code> …</p>
   ```
   The warning box on the **undocumented ESD grounding step** ends mid-clause and the "stop and ask" escapes it.
   Same failure at `10-wiring.md:148` (Step 10.5's mains continuity list), `13-initial-startup.md:409` and
   `:438` (Z-offset correction lists), `07-ab-belts.md:307`, and 8 print-batch chapters — including
   `B01-z-drive-assemblies.md:23` (the deck-thickness conflict) and `:42` (the spool-runout check, which
   renders as "…a resume seam on a Z-drive" and stops).
2. **Batch-id drift.** Chapters use `B0/B1/B2/B3/B4/B5/B7/B8` (Ch 01, 02, 05, 06, 07, 08, 09, 10, 11 — 45
   occurrences in Ch 11 alone) while `00-index.md`, `print/README.md` and every filename use `B00`–`B10`.
   Ch 05 line 9 says "batch **B0**"; the index calls the same thing B00.
3. **Conventions conformance.** `CONVENTIONS.md` mandates `### Step NN.M` and an image line first; print
   chapters use `## Step B01.1` (H2) and have **zero images across all 12**. Ch 08's
   `(SB manual p.NN, not embedded)` is a marker the conventions do not define (44 uses).
4. **Cross-document fact drift.** See §4 P6 — a correction landed in `voron-print-plan.md` and never reached
   the three print chapters derived from it, despite `00-index.md` §"How to update" mandating exactly that
   propagation.

**Deciding criterion.** Each of these is invisible in the source and invisible in the build. They are only
visible in rendered HTML or by cross-file comparison — which is precisely what a lint is for.
**Sketch.** `scripts/lint-manual.py`, run in CI: (1) flag any `⚠` / `Tip:` / `**Check:**` line followed by a
non-blank line — and fix `_admonition()` to indent *all* continuation lines until a blank line, with the
existing `__main__` fixture extended into a real `pytest` case; (2) regex `\bB[0-9]\b` outside code spans;
(3) assert every step heading matches `### Step \d+\.\d+ — ` and has an image line or a `(no image` marker;
(4) a small `facts.yml` of cross-document invariants (bearing type per assembly, deck thickness, batch↔chapter
map) asserted against every file that mentions them.

### V5 — Corrections-log discipline · S (1.5 h) · **M**
**Why.** The log in `00-index.md` is 11 rows of `# | Correction | Detail lives in`. It has no **date**, no
**last-verified** column, and no **status**. Row 5 ("Which Leviathan you have is contested") is an open
question with no resolution field; row 6 records a source that changed on 2026-07-10 with no note of when it
was last checked. The page says "This is the list to re-check whenever LDO updates its docs" — but nothing
records when you last did.
**Sketch.** Add `Opened`, `Source checked`, `Status` (open | resolved-on-bench | superseded) columns; require
a `sources.yml` key per row so V3's drift job can reference the row it invalidates. Extend the "How to update"
list from two places to three: log row, inline `⚠`, and `sources.yml`.

### V6 — Community corrections: issue and PR templates · S (1 h) · **M**
**Why.** Public repo, zero templates, no `CONTRIBUTING.md`. `README.md` already anticipates other builders
("If your kit differs (Rev C/D, different toolboard, different probe), the corrections log tells you which
steps to re-check") — and a Rev C builder who spots an error has no structured way to report it. The single
most valuable inbound report is "my kit's Step NN.M differs", and it needs a serial, a batch, and a photo to
be usable.
**Sketch.** `.github/ISSUE_TEMPLATE/correction.yml` with required fields: kit revision, LDO serial/batch,
chapter + step id, what the manual says, what your kit is, photo. `.github/ISSUE_TEMPLATE/config.yml` pointing
question-shaped traffic at the Voron Discord. A `pull_request_template.md` that requires the CONVENTIONS
format and a corrections-log row for any factual change.

### V7 — Repo hygiene · S (0.5 h) · **L**
`hooks/__pycache__/callouts.cpython-*.pyc` is tracked in git (`git ls-files` → 1 `.pyc`); add
`__pycache__/` to `.gitignore` and `git rm --cached` it. 33 of the 263 committed manual-page PNGs
(6.0 MB of 40 MB) are referenced by no chapter — either delete them or note in `README.md` that the full
range is kept deliberately.

---

## 4 · Print-side

### P1 — Commit a PrusaSlicer project per plate + the config bundle · M (6 h) · **H**
**Why.** Plates exist only as prose. `print/B01-z-drive-assemblies.md` Step B01.2 says *"Slice
`z_drive_main_a` ×2, `z_drive_main_b` ×2, `z_drive_retainer_a` ×1, `z_drive_retainer_b` ×2 together on one
plate … 12.7 h, 216 g"* — and the Check is *"Estimated plate time is close to 12.7 h; if far off, re-verify
profile/overrides."* But the arrangement that produced 12.7 h is nowhere, so the builder must hand-place
seven parts on a 250×220 bed and then judge whether their guess matched. Repo-wide: **26 plates, zero
project files, zero plate images, zero `.ini`** (`git ls-files` by extension: 35 md, 263 png, 1 css, 1 py,
1 pyc, 1 sh, 1 txt, 2 yml). The 30-line override table in `print/00-slicer-setup.md` — including the
"single most important override in this document" (shrinkage compensation 0 %) — must be re-entered by hand
and cannot be diffed.
**Deciding criterion.** 134 h of ASA is gated on a ±0.15 mm cube and a press-fit bore. If the profile that
passed the gate is not a committed artefact, the gate proves nothing about the 25 plates that follow it.
**Sketch.** `printing/projects/B01-P1.3mf` … one project per plate (2.9.6 format), plus
`printing/VoronASA.ini` exported via *File → Export → Export Config Bundle*. Add to each batch chapter's
Step `.2`: "open `printing/projects/<plate>.3mf`" instead of "slice these files". Add a
`printing/README.md` recording PrusaSlicer version, the STL repo commit SHAs (the discipline
`00-slicer-setup.md` §"STL source of truth" already demands), and the bundle's checksum. ~200 MB if 3MFs
carry mesh — use *Export plate as 3MF* per plate and keep the STLs out of git via the existing pinned-source
pattern if size becomes a problem.

### P2 — Version posture: pin 2.9.6 for the whole Voron run · S (0.5 h) · **H**
**Why.** `print/00-slicer-setup.md` line 6 currently reads: *"PrusaSlicer **2.9.6** (current stable, released
2026-06-25). 3.0.0 is alpha — do not use it."* That is now stale in its facts and right in its conclusion.
Verified against Prusa's own announcement: the **3.0 preview shipped 2026-09-01** and Prusa state *"This is an
early preview, and not the kind of polished, nearly-ready alpha that we have shipped in the past"* and *"The
preview build is not feature complete (when compared to 2.9.6)"*, with some features waiting for 3.1.0. The
profile format also moved from `.ini` to `.yaml`, so the config bundle in P1 is not portable across the
boundary.
**Deciding criterion.** Dimensional reproducibility across the run, not features. The B00 gate (cube ±0.15 mm,
625-2RS press fit, `MGN12_rail_guide` finger fit) qualifies a *toolchain*, not a file — changing slicer major
version mid-run silently invalidates it for every plate after the change, and the manual already has one
precedent for handling exactly this: the Gen 2 belt-upgrade pause rule, which mandates re-printing and
re-measuring the cube before B08.
**Sketch.** Rewrite the version line to: pinned **2.9.6** for all 26 plates; a 3.0-preview install is fine
side-by-side for evaluation but must not slice a Voron plate; and add one row to the existing "Gen 2 pause"
rule generalising it — *any* change to slicer version, profile bundle, belts, or nozzle re-triggers the B00
seven-item gate before the next plate. Record slicer version + bundle checksum per plate in `printing/README.md`
(P1) so a mid-build reprint is provably identical.

### P3 — Plan the 3.0 migration as a post-build step (multi-bed projects, then per-tool for INDX) · M (4 h, deferred) · **M**
**Why.** 3.0's headline features map unusually well onto this repo's actual shape once the Voron run is done.
Prusa: *"each bed can have its own configuration"* and *"when you slice, beds are processed in parallel"*, with
the previous 9-bed cap removed — this project is **26 plates in 11 batches**, and batches B08 (6 plates) and
B09 (5 plates) are exactly the multi-bed case. Separately, *"You can even assign whole different print or
printer profiles to individual tools and mix them as needed"* is the feature the **INDX 8-tool conversion**
(ordered, pre-order per `CLAUDE.md`) will need, and there is no per-tool story anywhere in the current setup.
**Deciding criterion.** Adopt 3.0 when the cost of *not* adopting exceeds the risk of a non-feature-complete
slicer — i.e. when the dimension-critical run is over and the multi-tool machine arrives. That is after B10,
not before B00.
**Sketch.** One 3.0 project per **batch**, one bed per **plate** (`printing/projects/B08.3mf` with 6 beds),
replacing the 26 single-plate 2.9.6 files from P1 — commit alongside, do not delete, until the 3.0 projects
have themselves passed a re-run B00 gate. Keep the yaml profile in `printing/voron-asa.yaml`. When INDX lands,
add per-tool profiles there and a `print/00-slicer-setup-indx.md` sibling rather than editing the ASA
document that the Voron build is pinned to.

### P4 — Plate images in the batch chapters · S (1.5 h) · **M**
**Why.** All 12 print chapters have **zero images** (verified on the live `print/B01` page: `imgs: 0`).
Step B01.5's Check is *"All 12 deck-support clips accounted for on the plate"* — a visual count with nothing
to count against (and the parts table above it says **8**, an unlinted contradiction that V4 would catch).
**Sketch.** Export a plate screenshot per plate from the P1 projects into `assets/plates/B01-P1.png` and add
it as the image line of each `Step B01.N — Load plate` step. Falls out of P1 for near-zero extra effort.

### P5 — Per-batch spool-weight ledger · S (1 h) · **M**
**Why.** `print/README.md` already computes the margin correctly (1940 g needed / 2400 g on hand, 24 %) and
already predicts the runouts ("Spool #1 runs out inside B07, #2 inside B08/B09"). B01.1's Check is "Spool has
≥216 g remaining" — but nothing records what was *actually* consumed, so by B05 the prediction and reality
have silently diverged and the 24 % margin is unverifiable.
**Sketch.** A small table in `print/README.md` with an "actual g" column per plate, filled at each batch's
"Label and bin" step — the same discipline Ch 05's Step 05.48 measurement table already uses.

### P6 — **Fix the press-fit gate: F695 / 13 mm should be 625-2RS / 16 mm** · S (0.5 h) · **H** — *content error, not a process change*
**Why.** The single dimensional gate that authorises all 26 plates names the wrong bearing in the document
the builder actually reads at the bench:

- `print/00-slicer-setup.md:124` — <code>| \`z_drive_retainer_a\` **F695** bore (same plate) | **13.00 mm** bearing | … | **The real press-fit gate.** |</code>
- `print/B00-calibration-and-jigs.md:64, :87` and `print/B01-z-drive-assemblies.md:31, :78, :94, :95` — same, "F695 (13 mm OD)".

Against the sources of truth in the same repo:

- `voron-print-plan.md:182` — <code>| \`z_drive_retainer_a\` **625-2RS** bore | **16.00 mm** bearing (625-2RS; **F695 is the A/B-drive bearing, not the Z drive**) | … |</code>, and `:671` repeats it for the B1 checkpoint.
- `00-before-you-start.md:442` (transcribed from official manual p.8) — "**F695** flanged bearing (gantry, 20 in the kit), **625** bearing (**Z drives**, 12 in the kit)".
- `02-z-drives.md:67` — Hardware table: `625-2RS bearing | 12`; `:332` and `:368` fit 625 bearings into the Z drive housings.

So the print plan already **carries the correction** ("F695 is the A/B-drive bearing, not the Z drive") and
the three derived print chapters never received it — the exact propagation failure `00-index.md`
§"How to update" step 5 exists to prevent.
**Consequence.** A 13 mm F695 dropped into a 16 mm 625 seat is loose by 3 mm. The gate's own remediation text
then sends the builder the wrong way: *"Loose → check shrinkage compensation is 0 %. Tight → reduce EM 1 %"* —
they will chase a nonexistent under-extrusion problem, or worse, "fix" it and mis-tune the profile that all
134 h of printing depends on.
**Sketch.** Replace F695/13.00 mm with 625-2RS/16.00 mm in those six places; add a corrections-log row; add
the bearing-per-assembly invariant to V4's `facts.yml`.

---

## 5 · Quality of the writing

Graded all 641 steps mechanically, then read 20 in detail against Prusa's contract — **one action, one check,
one image**. Headline: the *action* half is genuinely Prusa-grade; the *image* and *check* halves are not.

**Measured across all 641 steps**

| Metric | Value |
|---|---|
| `**Do:**` present | 641 / 641 |
| `**Check:**` present | 641 / 641 |
| Do length | median **3 sentences / 50 words**; p90 4 sentences / 93 words |
| Steps over the CONVENTIONS 5-sentence cap | **16** |
| Steps with **no image** | **280 / 641 (44 %)** |
| Check length | median 25 words; **125 steps (20 %) exceed 40 words**; max **229** |

### The 20-step sample

| Step | One action | One check | One image | Grade |
|---|---|---|---|---|
| 05.5 Load the E extrusion | ✓ 1 action, exact count (8 T-nuts, 10–15 mm in) | ✓ 16 words | ✓ p.85 | **A** |
| 05.7 Bolt the A drive to the bridge | ✓ + failure mode inline ("if a bolt spins…") | ✓ 14 words | ✓ p.86 | **A** |
| 05.20 Check flush and notch orientation | ✓ verification-only step, correctly split out | ✓ 8 words | ✓ p.92 | **A** |
| 05.29 Fit the right joint's 20T idler | ✓ | ✓ 13 words | ✓ p.98 | **A** |
| 02.43 (Z tensioner idlers) | ✓ | ✓ | ✓ | **A** |
| 04.2 A = rear right, B = rear left | ✓ | ✓ | ✓ p.64 | **A** |
| 10.2 Set the PSU voltage selector | ✓ | ✓ "read the number out loud" | ✓ p.181 | **A** |
| 10.14 Bed Live → SSR LOAD 1 | ✓ | ✓ 24 words | ✓ LDO S5 | **A** |
| 10.27 Leviathan HEATBED → SSR INPUT | ✓ verbatim LDO quote | ✓ "say 'three, red; four, black' out loud" | ✓ LDO S4 | **A** |
| 03.9 Magnet sheet + trim | ✓ | ✓ | ✓ | **A** |
| 05.17 Fit the first Y backer | ✓ | ✓ | **✗ no image** — the highest-consequence irreversible step in Ch 05 (teardown if missed, per its own Common-mistakes) | **B** |
| 05.34 Fit the X backer to the rear face | ✓ | ✓ | **✗** — and "not on top" is the whole point | **B** |
| 05.14 Reserved M5+M3 T-nut pair | ✓ | ✓ "count them before you go on" | ✓ p.90 | **A** |
| 08.3 Inserts: CW2 main body | ✓ | ✓ | **✗ `(SB manual p.11–12 … not embedded)`** — asks you to match a page you cannot see | **C** |
| 08.7 Inserts: rear printhead, and the two you skip | ✓ | ✓ | **✗ not embedded** — "the two inside the circled region" refers to a circle on an invisible page | **C** |
| 10.5 Verify the pre-wired inlet | ✓ | ✗ **4-item mains continuity list escapes the Check box** (V4.1) | ✗ diagram is a bare link | **C** |
| 10.13 Measure the bed heater | ✓ | ✗ **156 words**: a 3-row table + an `R = V²÷P` derivation + two worked examples | ✗ | **C** |
| 06b.14 De-rack the gantry, then tighten | ✗ **7 sentences / 192 words**, several distinct actions | ✓ | ✗ | **C** |
| 14.4 Set A/B belt tension to 110 Hz | ✗ 6 sentences | ✗ **225 words** — contains a 4-row source-disagreement table | ✓ | **D** |
| 14.14 Read the graphs | ✗ **11 sentences / 172 words** | ✗ 140 words with a Klipper block quote | ✓ | **D** |

### Systematic weaknesses (in priority order)

1. **Missing images — 280 steps (44 %).** Not evenly spread; concentrated where it hurts most:
   Ch 08 **5/67 illustrated**, Ch 14 **2/23**, Ch 12 **4/37**, Ch 13 **15/43**, Ch 11 **34/66**. Ch 02 and
   Ch 04 are 94–100 %. Root causes are two and both fixable: the Stealthburner PDF was never rendered (C1),
   and no bench-photo path exists (B6). Fix those two and coverage goes from 56 % to ~85 % without writing a
   word.
2. **`Check:` used as a reference container — 125 steps over 40 words.** The worst six contain markdown
   tables (10.13, 14.4), block-quoted alternatives (08.54's 229-word Klicky aside), and source-disagreement
   analyses (14.4's "The disagreement, resolved"). All of it is *good content in the wrong field*: a Prusa
   check is a glance ("The idler spins freely"), and this one is a page. Fix: keep one glanceable line in
   `Check:` and move the rest into a collapsible `??? note "Why"` — `pymdownx.details` is already enabled and
   unused for this.
3. **Ch 14 is written as a tutorial, not as steps.** Mean 4.3 Do-sentences (highest in the manual) and
   **7 of 23 steps over the 5-sentence cap** vs 0–2 everywhere else. It reads like Ellis' guide rather than
   the rest of this manual. Split 14.4, 14.7, 14.13, 14.14, 14.15, 14.18 into action + interpretation pairs.
4. **A convention exists for missing images and Ch 08 doesn't use it.** 138 steps correctly carry
   `(no image — see text)`; Ch 08 invents `(SB manual p.NN, not embedded)` 44 times and 43 of its steps carry
   neither marker nor image — the only chapter in the manual out of conformance with `CONVENTIONS.md` line 20.
5. **Print chapters are a different genre from assembly chapters.** `## Step B01.1` (H2, not the mandated
   `### Step NN.M`), `**Do:**`/`**Check:**` run together with no blank line (which is *why* the callout hook
   truncates them — V4.1), no images, and no `Parts:` line on most steps. They read as batch notes; the
   assembly chapters read as a manual.
6. **Duplicated instructions that will drift.** The Rev D+ toolhead deltas are written twice at full length —
   Ch 08 Steps 08.53/08.55–08.57 and Ch 10 Steps 10.55–10.58 — with the ESD grounding procedure stated
   independently in both. That is defensible (Ch 10 is a verification pass) but nothing marks one as the
   source, so a future correction will land in one and not the other. Same pattern as P6.

### What is genuinely Prusa-grade and should not be touched

Median 3-sentence steps with a stated failure mode inline; exact fastener counts per step; orientation stated
every time ("motor pointing **down**", "notch pointing outboard"); "count them before you go on" checks;
verification-only steps split out as their own step (05.20, 05.24, 05.40); the `⚠ Rev D+ / LDO:` callout used
inline at the step rather than in a preamble; and the refusal to invent numbers — 67 `(verify on bench)`
markers and Step 00.8's honest "No Voron or LDO source publishes a torque figure for any fastener in this
build; this manual never invents one." That last discipline is rarer than the rest of the manual and is the
reason it can be trusted.
