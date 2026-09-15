# Voron 2.4 350 — Build Manual

**Where things stand (14 Sept 2026):** the Core One+ is running, all the ASA is on the shelf, and two kits are in transit: the Gen 2 belt kit for the Prusa (due first) and the Voron kit itself (late November to late December). Every plate prints before the Voron kit lands.

## How to begin

1. **Now, before the Gen 2 kit arrives.** Read [slicer setup](manual/print/00-slicer-setup.md). Do the pre-kit steps of [Ch 00](manual/steps/00-before-you-start/index.md): what the kit supplies, tools, consumables, the flat reference and the bins (Steps 00.7–00.12); the Voron manual's front matter, the measurement log and the Discord questions (Steps 00.23–00.32). Do [Ch 00a — Mains safety](manual/steps/00a-mains-safety/index.md). Print the [bin labels](print/bin-labels.md).
2. **The day the Gen 2 kit lands.** [Gen 2 first](manual/steps/b00-calibration-and-jigs/note-gen-2-first.md): the belt upgrade, one day. Then [B00](manual/steps/b00-calibration-and-jigs/index.md) and Gate A, then the insert practice (Steps 00.13–00.16).
3. **Then every plate, B01 → B10,** in the [manual index](manual/00-index.md) timeline order. Sort each plate into its bins as it comes off the bed.
4. **The day the Voron cartons land.** [Ch 00 — Before you start](manual/steps/00-before-you-start/index.md) from Step 00.1, then the **Build** tab in chapter order. Nothing waits on a plate.

## How to proceed, every session

Open [Tonight](manual/00-tonight.md), pick the 30, 60 or 90-minute plan, tap its first step, work to the `Pause:` line, tick each step done. **Resume** on any chapter overview jumps to your first unticked step.

<div class="build-progress" data-build-progress="assets/build-progress.json">
  <img class="build-progress__img" alt="" hidden>
  <p class="build-progress__caption">Tick a chapter's steps and this shows the machine as it stands at the end of it.</p>
  <p class="build-progress__counts"></p>
</div>

This site consolidates the Voron 2.4 R2 Rev D+ 350 build into one Prusa-style manual. Five tabs across the top (behind ☰ on a phone), and the sidebar only ever shows the tab you are in: **Build** — the 16 assembly chapters, in build order; **Print** — [slicer setup](manual/print/00-slicer-setup.md), the 11 print batches, and the [plate plans](print/plate-plans.md), [checklists](print/checklists.md) and [bin labels](print/bin-labels.md); **Plan** — the [manual index](manual/00-index.md), the [Tonight](manual/00-tonight.md) planner, the [print plan](voron-print-plan.md) (batch order and dependencies) and the [instruction survey](voron-build-instructions-survey.md) (source docs and known deviations); **Reference** — [troubleshooting](manual/15-troubleshooting.md) and [glossary](manual/16-glossary.md).

!!! tip "Bench mode"
    Open <https://alexlicohen.github.io/voron-24-350-build-manual/> on the iPad (or the LAN URL printed by `scripts/serve.sh` when editing offline). Share → Add to Home Screen for a full-screen, app-like view. Tap the ☼ button in the header to keep the screen awake while you work — it re-arms automatically if the tab is backgrounded, though on iPadOS 16.4–18.3 it only holds inside Safari itself, not once added to the Home Screen (18.4+ fixes this); turn up Auto-Lock as a fallback on older iPadOS.

    **One page per step.** Every chapter has an overview page — time, sessions, and a thumbnail grid of its steps — and each step is its own page: the picture large, then Do, Parts, Check, and what you're looking at. Move with the big **prev / next** bar at the bottom, the **← →** keys, or a swipe. Each step page has a *done* toggle; ticks are shared with the chapter overview grid and with the whole-chapter page (linked from every overview as "Read the whole chapter on one page"), and **Resume** on an overview jumps to your first unticked step. Progress is per-device, in the browser, offline.

    Searching a bare step number (`10.58`) is faster than "Step 10.58"; step pages are indexed individually. [Tonight](manual/00-tonight.md) turns every chapter's `Time:` and `Pause:` lines — and every print plate's start — into a 30/60/90-minute session planner in the index's timeline order, generated fresh on every build, with a "Before the kit" plan first; each segment links straight to its first step page. Those same `Pause:` lines mark the stopping points — where a sub-assembly is safe to leave and what not to do before walking away. Every step ends with a `Source:` line pinning it to the exact manual page, LDO doc or print-plan section it came from. The print section (see [print-ready checklists and bin labels](print/checklists.md)) has print-ready Checkpoint checklists and a bin-labels sheet — one label per bin (a chapter, or a sub-assembly such as a Z-drive corner), each listing the parts it should hold, its chapter and steps, and a QR code to that chapter's step overview — plus a bin map; every plate diagram in the print chapters shows which bin each part goes to as it comes off the bed. Print them for the garage bench where a tablet doesn't survive.
