"""mkdocs on_pre_build hook (R6 C4): generate docs/manual/00-tonight.md.

Order comes from the index timeline — the `- **N · Print|Build|Both** —
[title](file#anchor) …` rows in docs/manual/00-index.md — never from
filenames. Each row names one chapter, or one part of a chapter by anchor
(Ch 06 Part A / 06b, Ch 11 Part A / B). For every row the chapter is parsed
for its segments:

  - assembly chapters (docs/manual/NN-*.md): `**Time:**`, `**Sessions:**` and
    `Pause: ~NN min since the last pause — <state>` lines → hands-on segments
    "Step X.Y → Step X.Z · ~NN min · leave-state: <state>".
  - a row whose anchor is a `## Part …` or `### Step …` heading takes only the
    segments from that heading to the next row's heading (Ch 06 A/06b, Ch 11 A/B,
    Ch 12 Part 2 from Step 12.11).
  - print chapters (docs/manual/print/B*.md): every
    `## Step BNN.M — Load [and print] plate BNN-PN` step with its
    `**Parts:** … — H h, G g (PrusaSlicer 2.9.6 estimate)` line → a print
    segment: open the project, confirm the estimate, start it and watch the
    first layer (PLATE_START_MIN hands-on), then H h unattended. Their
    `Pause:` lines (after the inspect steps) become hands-on segments too.

Planner: 30/60/90-minute buckets packed greedily in timeline order. At most
one plate start per bucket (one printer), and once a plate is started the
rest of that batch waits for it. A hands-on segment that does not fit is
skipped together with the rest of its row (a chapter's segments are
sequential), so a 30-minute bucket never offers a 40-minute segment; a bucket
that fits nothing says so. "Before the kit" runs the same planner over the
rows that carry no **KIT** marker, plus any `Pause: ~NN min since the last pause
(pre-kit) — …` segment inside a row that does carry one (Ch 00's reading, log
and Discord steps are real bench work weeks before the kit ships).

A `## With a helper` section after the planner lists every segment that holds a
`**Helper:**` step (CONVENTIONS.md § "Helper steps") with its jobs, under the
same before-the-kit filter the buckets ran with; each bucket line carrying one
gets a `· helper: <job>` suffix.

Each segment carries `data-first-step` so scripts/build_steps.py can link it
to its first step page. This file is regenerated on every build — never
hand-edit docs/manual/00-tonight.md.
"""

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "hooks"))
import mascot  # noqa: E402  (hooks/mascot.py — the raven's markup and asset paths)

try:  # mkdocs' own slug rule, so anchors in the index match chapter headings
    from markdown.extensions.toc import slugify as _md_slugify

    def _slug(text):
        return _md_slugify(text, "-")
except ImportError:  # pragma: no cover - standalone fallback
    import unicodedata

    def _slug(text):
        text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
        text = re.sub(r"[^\w\s-]", "", text).strip().lower()
        return re.sub(r"[-\s]+", "-", text)

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "slicer"))
from plates import PLATES, run_of  # noqa: E402  (slicer/plates.py — which run a plate belongs to)
MANUAL = REPO / "docs" / "manual"
PRINT = MANUAL / "print"
INDEX = MANUAL / "00-index.md"
OUT = MANUAL / "00-tonight.md"

PLATE_START_MIN = 5  # open the project, confirm the estimate, start, watch the first layer

# The Voron kit is not here yet (expected late Nov - late Dec 2026), so "Before
# the kit" is the section that gets read and it renders first. Flip this to True
# on kit day and the two planner sections swap back.
KIT_ARRIVED = False

_CHAPTER_TITLE_RE = re.compile(
    r"^#\s*(?:Chapter|Batch)\s+([A-Za-z]?\d+[a-z]?)\s*—\s*(.+?)\s*$", re.MULTILINE
)
_TIME_RE = re.compile(r"^\*\*Time:\*\*\s*(.+)$", re.MULTILINE)
_TIME_RANGE_RE = re.compile(r"(\d+(?:\.\d+)?)\s*(?:[–-]\s*(\d+(?:\.\d+)?))?\s*h")
_STEP_HEADING_RE = re.compile(
    r"^#{2,3}\s*Step\s+([A-Za-z]?\d+[A-Za-z]?\.\d+)\s*—\s*(.*?)\s*$", re.MULTILINE
)
_SECTION_RE = re.compile(r"^#{2,3}\s+(.+?)\s*$", re.MULTILINE)  # any h2/h3: a row's anchor may be a Part or a Step
# `(pre-kit)` after "since the last pause" marks a segment that needs no Voron
# part, so the "Before the kit" planner can offer it even though its timeline
# row is **KIT** (Ch 00's reading, log and Discord steps).
_PAUSE_RE = re.compile(
    r"^>?\s*Pause:\s*~?(\d+)\s*min\s*since the last pause\s*(\(pre-kit\))?\s*—\s*(.+?)\s*$",
    re.MULTILINE,
)
# `**Helper:** <job>` — the helper (child) task in a step, per
# docs/manual/CONVENTIONS.md § "Helper steps".
_HELPER_RE = re.compile(r"^\*{0,2}Helper:\*{0,2}\s*(.+?)\s*$", re.MULTILINE)
_LOAD_TITLE_RE = re.compile(r"^Load(?: and print)? plate (B\d\d-P\d)")
_PRINT_TITLE_RE = re.compile(r"^Print\b")
_PARTS_TIME_RE = re.compile(
    r"^\*\*Parts:\*\*.*?— ([\d.]+) h, (\d+) g \(PrusaSlicer", re.MULTILINE
)
_ROW_RE = re.compile(r"^- \*\*(\d+) · (Print|Build|Both)\*\* — (.*)$", re.MULTILINE)
_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)#\s]+)(?:#([^)\s]+))?\)")
_GATE_LINE_RE = re.compile(r"^\s*- \*Gate:\*(.*)$", re.MULTILINE)
_EXCLUDE = {"00-index.md", "00-tonight.md", "CONVENTIONS.md", "README.md"}


# --------------------------------------------------------------------------
# index timeline
# --------------------------------------------------------------------------

def _timeline_rows():
    """The index's numbered rows, in order: n, kind, title, file, anchor, kit, rest.

    `rest` is the row's raw text after the kind — scripts/draw_diagrams.py reads
    the duration, the marker and the `needs:` list out of it so diagram 11 draws
    the same timeline this planner walks.
    """
    rows = []
    text = INDEX.read_text(encoding="utf-8")
    matches = list(_ROW_RE.finditer(text))
    for i, m in enumerate(matches):
        n, kind, rest = int(m.group(1)), m.group(2), m.group(3)
        lm = _LINK_RE.search(rest)
        if lm:
            title, file, anchor = lm.group(1), lm.group(2), lm.group(3)
        else:
            title = re.sub(r"\*\*", "", rest.split(" · ")[0]).strip()
            file = anchor = None
        # The row's `*Gate:*` sub-bullet names the page section its gate lives
        # on (row 1: B00's "Before B00" checks). Ticking any step after that
        # section, or printing any plate after it, means the gate was passed.
        block = text[m.end(): matches[i + 1].start() if i + 1 < len(matches) else len(text)]
        gm = _GATE_LINE_RE.search(block)
        glm = _LINK_RE.search(gm.group(1)) if gm else None
        rows.append({
            "n": n, "kind": kind, "title": title, "file": file, "anchor": anchor,
            "kit": "**KIT" in rest, "rest": rest, "segments": [],
            "gate_file": glm.group(2) if glm and glm.group(3) else None,
            "gate_anchor": glm.group(3) if glm else None,
        })
    return rows


# --------------------------------------------------------------------------
# chapters
# --------------------------------------------------------------------------

def _chapter_files():
    files = [f for f in MANUAL.glob("*.md") if f.name not in _EXCLUDE]
    files += [f for f in PRINT.glob("B*.md")]
    return sorted(files, key=lambda f: (f.parent.name != "print", f.name))


def _midpoint_hours(time_line):
    m = _TIME_RANGE_RE.search(time_line or "")
    if not m:
        return None
    lo = float(m.group(1))
    hi = float(m.group(2)) if m.group(2) else lo
    return (lo + hi) / 2.0


def _helper_jobs(text, steps):
    """step id -> its `**Helper:**` jobs, in source order."""
    jobs = {}
    bounds = [pos for pos, _sid, _t, _e in steps] + [len(text)]
    for i, (pos, sid, _t, _e) in enumerate(steps):
        found = [m.group(1) for m in _HELPER_RE.finditer(text, pos, bounds[i + 1])]
        if found:
            jobs.setdefault(sid, []).extend(found)
    return jobs


def _parse_chapter(path):
    text = path.read_text(encoding="utf-8")
    is_print = path.parent == PRINT
    title_m = _CHAPTER_TITLE_RE.search(text)
    number = title_m.group(1) if title_m else path.stem
    title = title_m.group(2) if title_m else path.stem
    time_m = _TIME_RE.search(text)
    hours = None if is_print else (_midpoint_hours(time_m.group(1)) if time_m else None)

    steps = [(m.start(), m.group(1), m.group(2), m.end()) for m in _STEP_HEADING_RE.finditer(text)]
    sections = [(m.start(), _slug(m.group(1))) for m in _SECTION_RE.finditer(text)]
    helpers = _helper_jobs(text, steps)
    segments = []
    print_hours = 0.0

    # print segments: one per plate (Load step), timed from its Parts line
    if is_print:
        for i, (pos, sid, stitle, end) in enumerate(steps):
            lm = _LOAD_TITLE_RE.match(stitle)
            if not lm:
                continue
            body_end = steps[i + 1][0] if i + 1 < len(steps) else len(text)
            pm = _PARTS_TIME_RE.search(text, end, body_end)
            plate_h = float(pm.group(1)) if pm else None
            grams = int(pm.group(2)) if pm else None
            if plate_h is not None:
                print_hours += plate_h
            hours_txt = f"{plate_h:.1f} h" if plate_h is not None else "(time not stated)"
            segments.append({
                "kind": "print", "pos": pos, "first_step": sid, "last_step": sid, "steps": [sid],
                "plate": lm.group(1), "minutes": PLATE_START_MIN, "print_hours": plate_h,
                "grams": grams,
                "leave_state": (f"plate {lm.group(1)} running, {hours_txt} unattended — "
                                f"door shut; come back for the next step when it ends"),
                "helpers": [(sid, job) for job in helpers.get(sid, [])],
            })

    # hands-on segments: pause-delimited, starting after the previous
    # boundary (the last pause, or in a print chapter the last plate step)
    boundary = 0
    for pm in _PAUSE_RE.finditer(text):
        ppos = pm.start()
        if is_print:
            for pos, sid, stitle, end in steps:
                if pos < ppos and (_LOAD_TITLE_RE.match(stitle) or _PRINT_TITLE_RE.match(stitle)):
                    boundary = max(boundary, pos + 1)
        first = next(((pos, sid) for pos, sid, _t, _e in steps if pos >= boundary and pos <= ppos), None)
        if first is None:
            # No step heading opens strictly after `boundary`: it sits inside a step that is
            # already open (a step with more than one `Pause:` line, e.g. B00.8's four review
            # sessions). Reuse that step instead of dropping the segment - but not a plate
            # load/start step: its trailing pause is already covered by the print segment.
            containing = None
            for pos, sid, stitle, _e in steps:
                if pos <= boundary:
                    containing = (pos, sid, stitle)
                else:
                    break
            if (containing is not None and containing[0] <= ppos
                    and not _LOAD_TITLE_RE.match(containing[2])
                    and not _PRINT_TITLE_RE.match(containing[2])):
                first = containing[:2]
        last = None
        for pos, sid, _t, _e in steps:
            if pos <= ppos:
                last = sid
            else:
                break
        if first is None or last is None:
            boundary = ppos
            continue
        segments.append({
            "kind": "build", "pos": first[0], "first_step": first[1], "last_step": last,
            # every step heading the segment spans, in page order (Ch 11's appended
            # 11.67 sits first in Part A); the segment is done when all are ticked
            "steps": [sid for pos, sid, _t, _e in steps if first[0] <= pos <= ppos],
            "minutes": int(pm.group(1)), "leave_state": pm.group(3),
            "pre_kit": bool(pm.group(2)),
            "helpers": [(sid, job)
                        for pos, sid, _t, _e in steps if first[0] <= pos <= ppos
                        for job in helpers.get(sid, [])],
        })
        boundary = ppos

    segments.sort(key=lambda s: s["pos"])
    slug = path.stem.lower()  # progress.js's store key: voron-progress:ch:<slug>
    for i, seg in enumerate(segments):
        seg["chapter"] = slug
        seg["id"] = f"{slug}#{i}"
    return {
        "number": number, "title": title, "path": path, "hours": hours,
        "print_hours": print_hours if is_print else None, "is_print": is_print,
        "segments": segments, "sections": sections, "slug": slug,
        "step_positions": [(pos, sid) for pos, sid, _t, _e in steps],
    }


def _assign(rows, chapters):
    """Give every timeline row the segments of the chapter (or chapter part) it names."""
    by_file = defaultdict(list)
    for r in rows:
        if r["file"]:
            by_file[Path(r["file"]).name].append(r)
    used = set()
    for fname, rs in by_file.items():
        ch = chapters.get(fname)
        if not ch:
            continue
        used.add(fname)
        for r in rs:
            r["chapter"] = ch
        anchored = [r for r in rs if r["anchor"]]
        if len(rs) == 1 or not anchored:
            rs[0]["segments"] = list(ch["segments"])
            continue
        starts = []
        for r in rs:
            pos = next((p for p, slug in ch["sections"] if slug == r["anchor"]), 0)
            starts.append((pos, r))
        starts.sort(key=lambda t: t[0])
        for i, (pos, r) in enumerate(starts):
            nxt = starts[i + 1][0] if i + 1 < len(starts) else float("inf")
            r["segments"] = [s for s in ch["segments"] if pos <= s["pos"] < nxt]
    # chapters the index does not name yet: append, filename order, so nothing is lost
    extra = []
    for fname, ch in chapters.items():
        if fname in used or not ch["segments"]:
            continue
        extra.append({
            "n": None, "kind": "Print" if ch["is_print"] else "Build",
            "title": f"{'Batch' if ch['is_print'] else 'Ch'} {ch['number']} — {ch['title']} (not yet on the timeline)",
            "file": None, "anchor": None, "kit": True, "chapter": ch, "segments": list(ch["segments"]),
        })
    return rows + extra



# --------------------------------------------------------------------------
# planner
#
# docs/javascripts/tonight.js carries a line-for-line port of everything from
# here to the rendering section (_plan_for_budget, _next_segment, _live_rows,
# _pre_kit_rows, plan_sections, done_segments, gate_is_closed, plan_state).
# Change one, change both: scripts/check_tonight.mjs replays the `cases` this
# file writes into docs/assets/tonight.json through the JS and fails on drift.
# --------------------------------------------------------------------------

BUDGETS = (30, 60, 90)


def _plan_for_budget(rows, budget, stop_at_kit=False, bench_first=False):
    """Greedy pack in timeline order. One plate start per plan; a segment
    that does not fit takes the rest of its row with it (sequential work).

    Print rows are sequential too: a batch waits on the one before it (B01 on
    B00's Gate B, B11 on B10 off the bed). Once a Print row is left unfinished,
    because a segment did not fit or a plate was started, no later Print row
    is entered, so a bucket never offers B01's plate start while B00's Gate B
    is still ahead of it. **KIT** Build rows are sequential the same way (Ch 10
    waits on Ch 01 even when Ch 10's first segment would fit the time left);
    the pre-kit Build rows keep the per-row rule.

    With `stop_at_kit`, packing stops at the first row marked **KIT**: the
    rows are in timeline order, so nothing past that row can be started
    before the cartons land, and a bucket that ran on past it would offer
    (say) mains wiring tonight.

    With `bench_first` (the Before-the-kit planner while row 1's pre-B00
    checks are still open), bench segments are packed before any print
    segment, so a short bucket offers the pre-kit reading and bench work
    instead of a plate start that waits on the checks.
    """
    picked, total, plate_started = [], 0, False
    if bench_first:
        # Pass 1: bench rows (Build rows and the (pre-kit) segments of KIT
        # rows) in timeline order. Print rows and the whole-day Both row wait.
        for row in rows:
            if stop_at_kit and row["kit"]:
                break
            if row["kind"] in ("Print", "Both"):
                continue
            for seg in row["segments"]:
                if total + seg["minutes"] > budget:
                    break
                picked.append((row, seg))
                total += seg["minutes"]
        # Pass 2: the print rows, exactly as the plain packer treats them,
        # with whatever budget is left.
        # Print rows are sequential (B01 waits on B00's gate), so only the
        # first print row with work left is eligible for the remaining budget.
        first_print = next((r for r in rows if r["kind"] == "Print" and r["segments"]), None)
        if first_print is not None and budget - total >= PLATE_START_MIN:
            rest, extra = _plan_for_budget([first_print], budget - total, stop_at_kit)
            picked.extend(rest)
            total += extra
        return picked, total
    prints_blocked = builds_blocked = False
    for row in rows:
        if stop_at_kit and row["kit"]:
            break
        if not row["segments"]:
            continue
        if row["kind"] == "Print" and prints_blocked:
            continue
        kit_build = row["kind"] == "Build" and row["kit"]
        if kit_build and builds_blocked:
            continue
        finished = True
        for seg in row["segments"]:
            if seg["kind"] == "print":
                finished = False  # the plate runs; the rest of this batch waits for it
                if not plate_started and total + seg["minutes"] <= budget:
                    picked.append((row, seg))
                    total += seg["minutes"]
                    plate_started = True
                break
            if total + seg["minutes"] > budget:
                finished = False
                break
            picked.append((row, seg))
            total += seg["minutes"]
        if row["kind"] == "Print" and not finished:
            prints_blocked = True
        if kit_build and not finished:
            builds_blocked = True
        if budget - total < PLATE_START_MIN:
            break
    return picked, total


def _next_segment(rows):
    for row in rows:
        for seg in row["segments"]:
            return row, seg
    return None, None


def _live_rows(rows, done):
    """The rows with their done segments removed (`done`: segment ids)."""
    if not done:
        return rows
    return [dict(r, segments=[s for s in r["segments"] if s["id"] not in done]) for r in rows]


def _pre_kit_rows(rows):
    """A row without **KIT**, or the (pre-kit) segments of a row that has it;
    rows left with nothing are dropped."""
    out = []
    for r in rows:
        segs = (r["segments"] if not r["kit"]
                else [s for s in r["segments"] if s.get("pre_kit")])
        if segs:
            out.append(dict(r, segments=segs))
    return out


def plan_sections(rows, gate, kit_arrived, done=frozenset(), gate_closed=False):
    """Every planner section the page shows, in page order, plus the helper list.

    `gate` is row 1 (or None). While it is open the Before-the-kit section packs
    bench work first and names the gate on every bucket; once a step after the
    gate's section is ticked (or its plate printed) the gate is closed and the
    same rows pack in plain timeline order.
    """
    live = _live_rows(rows, done)
    pre = _pre_kit_rows(live)
    gate_open = gate is not None and not gate_closed
    specs = []
    if kit_arrived:
        specs.append(("tonight", live, not kit_arrived, False))
    specs.append(("before-kit", pre, False, gate_open))
    sections = []
    for sid, srows, stop_at_kit, bench_first in specs:
        buckets = []
        for budget in BUDGETS:
            picked, total = _plan_for_budget(srows, budget, stop_at_kit, bench_first=bench_first)
            buckets.append({"budget": budget, "picked": picked, "total": total,
                            "next": None if picked else _next_segment(srows)})
        sections.append({"id": sid, "rows": srows, "gate": gate_open,
                         "bench_first": bench_first, "buckets": buckets})
    source = live if kit_arrived else pre
    helpers = [(row, seg) for row in source for seg in row["segments"] if seg.get("helpers")]
    return sections, helpers


def done_segments(rows, ticks, printed):
    """Segment ids done on a device. `ticks`: progress slug -> set of ticked step
    ids (progress.js's stores); `printed`: plate ids the plate board marks printed.
    A build segment is done when every step it spans is ticked; a print segment
    when its Load step is ticked or its plate is marked printed."""
    done = set()
    for row in rows:
        for seg in row["segments"]:
            have = ticks.get(seg["chapter"], ())
            if seg["kind"] == "print":
                ok = seg["first_step"] in have or seg.get("plate") in printed
            else:
                ok = bool(seg["steps"]) and all(s in have for s in seg["steps"])
            if ok:
                done.add(seg["id"])
    return done


def gate_is_closed(gate, ticks, printed):
    if not gate:
        return False
    have = ticks.get(gate.get("chapter") or "", ())
    return (any(s in have for s in gate.get("closed_by", []))
            or any(p in printed for p in gate.get("plates", [])))


def _summary(sections, helpers, done, gate_closed):
    """The comparable shape of a plan: segment ids only (check_tonight.mjs)."""
    head = sections[0]["buckets"][-1]
    if head["picked"]:
        start = head["picked"][0][1]["first_step"]
    elif head["next"] and head["next"][1]:
        start = head["next"][1]["first_step"]
    else:
        start = None
    return {
        "done": len(done), "gate_closed": gate_closed, "start": start,
        "sections": [{
            "id": sec["id"], "gate": sec["gate"], "bench_first": sec["bench_first"],
            "buckets": [{
                "budget": b["budget"], "total": b["total"],
                "items": [seg["id"] for _row, seg in b["picked"]],
                "next": b["next"][1]["id"] if b["next"] and b["next"][1] else None,
            } for b in sec["buckets"]],
        } for sec in sections],
        "helpers": [seg["id"] for _row, seg in helpers],
    }


def plan_state(data, ticks, printed, kit_arrived):
    """The whole overlay for one device state, over tonight.json's own rows."""
    ticks = {ch: set(ids) for ch, ids in ticks.items()}
    printed = set(printed)
    done = done_segments(data["rows"], ticks, printed)
    closed = gate_is_closed(data["gate"], ticks, printed)
    sections, helpers = plan_sections(data["rows"], data["gate"], kit_arrived, done, closed)
    return _summary(sections, helpers, done, closed)


# --------------------------------------------------------------------------
# rendering
# --------------------------------------------------------------------------

def _row_label(row):
    if row["n"] is None:
        return row["title"]
    return row["title"]


def _segment_text(seg):
    if seg["kind"] == "print":
        hrs = f"{seg['print_hours']:.1f} h" if seg["print_hours"] is not None else "?"
        return (f"Start plate {seg['plate']} (Step {seg['first_step']}) · "
                f"~{seg['minutes']} min hands-on, then {hrs} unattended · "
                f"leave-state: {seg['leave_state']}")
    if seg["first_step"] == seg["last_step"]:
        label = f"Step {seg['first_step']}"
    else:
        label = f"Step {seg['first_step']} → Step {seg['last_step']}"
    return f"{label} · ~{seg['minutes']} min · leave-state: {seg['leave_state']}"


def _segment_span(seg):
    return f'<span data-first-step="{seg["first_step"]}">{_segment_text(seg)}</span>'


def _helper_suffix(seg):
    """`· helper: <job>` for a bucket line, or "" when nobody can help here."""
    jobs = seg.get("helpers") or []
    if not jobs:
        return ""
    more = f" (+{len(jobs) - 1} more)" if len(jobs) > 1 else ""
    return f" · helper: {jobs[0][1]}{more}"


def _gate_row(rows):
    """A wall-clock row (`Both`) with no stopping points that sits ahead of
    every row carrying segments - row 1's pre-B00 checks. Nothing below it
    should be planned before it is done, but it has no segments to plan, so
    the planner names it instead of silently stepping over it."""
    for row in rows:
        if row["segments"]:
            return None
        if row["kind"] == "Both":
            return row
    return None


def _gate_info(gate, chapters):
    """Row 1 for tonight.json: its label, and what closes it on a device — any
    step after the section its `*Gate:*` link names, or any plate printed after
    it (B00.8 onward; B00-P1)."""
    if gate is None:
        return None
    info = {"label": _row_label(gate), "chapter": None, "closed_by": [], "plates": []}
    ch = chapters.get(Path(gate["gate_file"]).name) if gate.get("gate_file") else None
    if ch:
        apos = next((p for p, slug in ch["sections"] if slug == gate["gate_anchor"]), None)
        if apos is not None:
            info["chapter"] = ch["slug"]
            info["closed_by"] = [sid for pos, sid in ch["step_positions"] if pos > apos]
            info["plates"] = [s["plate"] for s in ch["segments"]
                              if s["kind"] == "print" and s["pos"] > apos]
    return info


def _emit_section(lines, section, gate):
    """One planner section's three buckets. `bench_first`: bench items (kind
    != Print) come first and print items are labelled as waiting on the gate.
    Wrapped in a `.tonight-plan` block so tonight.js can re-plan it in place."""
    lines.append(f'<div class="tonight-plan" data-tonight-section="{section["id"]}" markdown>')
    lines.append("")
    for b in section["buckets"]:
        label = f"{b['budget']} min"
        lines.append(f"**If you have {label}:**")
        lines.append("")  # without it Python-Markdown runs the list into the paragraph
        if section["gate"]:
            if section["bench_first"]:
                lines.append(f"- **First, before B00 (not tonight):** "
                             f"{_row_label(gate)}. The print rows below wait on it; "
                             f"the bench items do not.")
            else:
                lines.append(f"- **first, and not tonight:** {_row_label(gate)} — "
                             f"every row below waits on it")
        if not b["picked"]:
            row, seg = b["next"]
            if seg is None:
                lines.append("- nothing to plan — no segments on this timeline yet")
            else:
                lines.append(f"- nothing fits in {label} — the next segment is "
                             f"{_row_label(row)} — {_segment_text(seg)}")
        else:
            for row, seg in b["picked"]:
                after = "after the checks: " if section["bench_first"] and row["kind"] == "Print" else ""
                lines.append(f"- {_row_label(row)} — {after}{_segment_span(seg)}{_helper_suffix(seg)}")
        lines.append(f"  <small>~{b['total']} min hands-on planned</small>")
        lines.append("")
    lines.append("</div>")
    lines.append("")


def _model():
    chapters = {f.name: _parse_chapter(f) for f in _chapter_files()}
    rows = _assign(_timeline_rows(), chapters)
    return chapters, rows


# The Tonight page is served from manual/00-tonight/, the JSON from assets/.
TONIGHT_JSON = REPO / "docs" / "assets" / "tonight.json"
_JSON_FROM_PAGE = "../../assets/tonight.json"


def build_tonight_markdown(model=None):
    chapters, rows = model or _model()

    build_chapters = [c for c in chapters.values() if not c["is_print"] and c["hours"] is not None]
    total_hours = sum(c["hours"] for c in build_chapters)
    print_chapters = [c for c in chapters.values() if c["is_print"]]
    # The ASA run's plates, and separately those of a batch outside it (B11, slicer/plates.py
    # run != "asa"), so the run's 157.0 h / 22 plates reads the same here as everywhere else.
    plate_segs = [s for c in print_chapters for s in c["segments"] if s["kind"] == "print"]
    outside = [s for s in plate_segs if s["plate"] in PLATES and run_of(s["plate"]) != "asa"]
    run_segs = [s for s in plate_segs if s not in outside]
    total_print = sum(s["print_hours"] or 0 for s in run_segs)
    n_plates = len(run_segs)
    extra_print = ""
    if outside:
        batches = sorted({s["plate"][:3] for s in outside})
        extra_print = (f", plus {sum(s['print_hours'] or 0 for s in outside):.1f} h across "
                       f"{len(outside)} plates of {', '.join(batches)}, outside the run")

    lines = [
        "# Tonight",
        "",
        # tonight.js fills this in and un-hides it; without JS (or without the JSON)
        # the page below is the full static plan, as if nothing were ticked.
        f'<p class="tonight-live" data-tonight="{_JSON_FROM_PAGE}" hidden></p>',
        "",
        f"**Total remaining (estimate):** ~{total_hours:.1f} h hands-on across "
        f"{len(build_chapters)} build chapters; {total_print:.1f} h of printing across "
        f"{n_plates} plates{extra_print} (~{PLATE_START_MIN} min hands-on per plate start, the rest unattended).",
        "",
    ]

    gate = _gate_row(rows)
    sections, helpers = plan_sections(rows, gate, KIT_ARRIVED)
    by_id = {s["id"]: s for s in sections}

    def emit_before_the_kit():
        lines.append("## %s Before the kit" % mascot.badge_html("pause", "pause"))
        lines.append("")
        if by_id["before-kit"]["rows"]:
            lines.extend([
                "The same planner over the timeline rows without the **KIT** marker, plus the "
                "individual `(pre-kit)` stopping points inside rows that do need the kit — the "
                "Core One+ batches and every piece of bench work that needs no Voron part.",
                "",
            ])
            _emit_section(lines, by_id["before-kit"], gate)
        else:
            lines.extend(["_Every timeline row needs the kit._", ""])

    def emit_tonight():
        lines.append("## Tonight's planner")
        lines.append("")
        lines.extend([
            "Timeline order, stopping at the first **KIT** row. One plate start per plan "
            f"(one printer): a plate start is ~{PLATE_START_MIN} min hands-on — open the project, "
            "confirm the estimate, start it, watch the first layer — and then the printer runs "
            "unattended for the hours shown, so the rest of a 30-minute bucket can go on bench work.",
            "",
        ])
        if not any(r["segments"] for r in rows):
            lines.append(
                "_No stopping points marked yet anywhere in the manual — chapters are still "
                "being written. Check back once `Pause:` lines land._"
            )
            lines.append("")
        else:
            _emit_section(lines, by_id["tonight"], gate)

    def emit_with_a_helper():
        """Every segment with a `**Helper:**` step, in timeline order, under the
        same before-the-kit filter the buckets above ran with."""
        lines.append("## %s With a helper" % mascot.badge_html("helper", "helper"))
        lines.append("")
        lines.extend([
            "Segments that carry a job a helper can own, in timeline order. The adult keeps "
            "the iron, the blade, mains work and anything hot; the helper's job is named in "
            "the step itself.",
            "",
        ])
        lines.append('<div class="tonight-helpers" markdown>')
        lines.append("")
        for row, seg in helpers:
            lines.append(f"- **{_row_label(row)}** — {_segment_span(seg)}")
            for sid, job in seg["helpers"]:
                lines.append(f"    - Step {sid} — {job}")
        if not helpers:
            lines.append("- no helper jobs marked on this timeline yet")
        lines.append("")
        lines.append("</div>")
        lines.append("")

    # Until kit day the pre-kit plan is the one that gets read, so it goes first.
    # Before kit day the two plans are identical (every pre-kit row is also the
    # stop-at-kit plan), so only one is emitted until KIT_ARRIVED flips.
    for emit in ((emit_tonight, emit_before_the_kit) if KIT_ARRIVED
                 else (emit_before_the_kit,)):
        emit()

    emit_with_a_helper()

    lines += ["---", "", "## By timeline row", ""]

    for row in rows:
        head = f"{row['n']} · {row['kind']} — {row['title']}" if row["n"] else row["title"]
        lines.append(f"### {head}")
        if not row["segments"]:
            if row["kind"] == "Both":
                lines.append("- wall-clock pause — see the timeline row for its gate")
            elif row.get("chapter") is None:
                lines.append("- no chapter file behind this row")
            else:
                lines.append("- no stopping points marked yet")
        else:
            for seg in row["segments"]:
                lines.append(f"- {_segment_span(seg)}")
        lines.append("")

    # The generator note sits at the foot: the first screen at the bench is the
    # plan, not boilerplate (G1-30).
    lines += [
        "---",
        "",
        "_Generated by `scripts/build_tonight.py` on every build — do not hand-edit. "
        "Plans are packed from the index timeline. On this device, segments you have ticked "
        "are skipped and each plan starts at your first unfinished step._",
        "",
    ]
    return "\n".join(lines).rstrip() + "\n"


# --------------------------------------------------------------------------
# docs/assets/tonight.json — what tonight.js re-plans from
# --------------------------------------------------------------------------

def _step_urls():
    """build_steps.STEP_URLS ("04.2" -> "manual/steps/04-ab-drives/04-2.md"), from
    the build_steps hook mkdocs has already run (it is listed before this hook, and
    mkdocs loads hooks under their config path, not as `build_steps`). Empty when
    this file runs on its own: the JSON is then written without hrefs."""
    for mod in list(sys.modules.values()):
        f = getattr(mod, "__file__", None) or ""
        if f.endswith("build_steps.py") and getattr(mod, "STEP_URLS", None):
            return mod.STEP_URLS
    return {}


def _href(step_urls, step_id):
    """The step page's URL relative to docs/assets/ (use_directory_urls)."""
    dest = step_urls.get(step_id)
    if not dest:
        return None
    return "../" + dest[:-len(".md")] + "/"


def _seg_json(seg, step_urls):
    return {
        "id": seg["id"], "chapter": seg["chapter"], "kind": seg["kind"],
        "steps": seg["steps"], "first_step": seg["first_step"], "last_step": seg["last_step"],
        "href": _href(step_urls, seg["first_step"]),
        "minutes": seg["minutes"], "pre_kit": bool(seg.get("pre_kit")),
        "plate": seg.get("plate"), "print_hours": seg.get("print_hours"),
        # Home's progress counts the run's plates ("N of 22"), not B11's
        "run": run_of(seg["plate"]) if seg.get("plate") in PLATES else None,
        "leave_state": seg["leave_state"],
        "helpers": [[sid, job] for sid, job in seg.get("helpers") or []],
        "text": _segment_text(seg),
    }


def _case_ticks(chapters, *specs):
    """{slug: [step ids]} from (file name, first id or None, last id or None)
    triples — a range of steps in page order, or the whole chapter."""
    ticks = {}
    for fname, first, last in specs:
        ch = chapters[fname]
        ids = [sid for _p, sid in ch["step_positions"]]
        a = ids.index(first) if first else 0
        b = ids.index(last) + 1 if last else len(ids)
        ticks.setdefault(ch["slug"], []).extend(ids[a:b])
    return ticks


def _pre_kit_steps(chapters, fname):
    """Every step of a chapter's (pre-kit) segments (Ch 00's reading and log steps)."""
    ch = chapters[fname]
    return {ch["slug"]: [sid for s in ch["segments"] if s.get("pre_kit") for sid in s["steps"]]}


def _merge(*tick_maps):
    out = {}
    for m in tick_maps:
        for k, v in m.items():
            out.setdefault(k, []).extend(x for x in v if x not in out.get(k, []))
    return out


def _cases_spec(chapters):
    """Seeded device states: (name, kit_arrived, ticks, printed)."""
    by = {n.split("-")[0]: n for n in chapters}  # "00a" -> "00a-mains-safety.md", "B00" -> ...
    assert len(by) == len(chapters), "two chapter files share a number"
    whole = lambda *keys: _case_ticks(chapters, *[(by[k], None, None) for k in keys])
    ch00_pre = _pre_kit_steps(chapters, by["00"])
    run = ["B%02d" % i for i in range(11)]
    return [
        ("none ticked", False, {}, []),
        ("Ch 00a done", False, whole("00a"), []),
        ("B00 done, plates 1-2 printed on the plate board (B00-P1, B01-P1)", False,
         whole("B00"), ["B00-P1", "B01-P1"]),
        ("B00.0 only: the gate is still open", False,
         _case_ticks(chapters, (by["B00"], "B00.0", "B00.0")), []),
        ("B00.0 and B00.8 ticked: the gate is passed", False,
         _merge(_case_ticks(chapters, (by["B00"], "B00.0", "B00.0")),
                _case_ticks(chapters, (by["B00"], "B00.8", "B00.8"))), []),
        ("half a segment: 00a.1-00a.3 ticked", False,
         _case_ticks(chapters, (by["00a"], "00a.1", "00a.3")), []),
        ("every bench segment done, gate open", False,
         _merge(whole("00a"), ch00_pre, _case_ticks(chapters, (by["B00"], "B00.0", "B00.0"))), []),
        ("plate board only: B00-P1 printed, nothing ticked", False, {}, ["B00-P1"]),
        ("printed through B05, Ch 00a done", False, whole("00a", *run[:6]), []),
        ("everything before the kit done", False,
         _merge(whole("00a", *run), ch00_pre, whole("B11")), []),
        ("kit arrived, none ticked", True, {}, []),
        ("kit arrived, cross-row: B00 ticked to B00.4 (Gate A, sort, Gate B left)", True,
         _merge(_case_ticks(chapters, (by["B00"], "B00.0", "B00.4"))), []),
        ("kit arrived, run printed and Ch 00 done", True,
         whole("00a", "00", *run), []),
        ("kit arrived, everything done", True,
         whole(*sorted(by)), []),
    ]


def tonight_json(model=None, step_urls=None):
    chapters, rows = model or _model()
    step_urls = _step_urls() if step_urls is None else step_urls
    gate = _gate_row(rows)
    data = {
        "_comment": "Generated by scripts/build_tonight.py on every build; read by "
                    "docs/javascripts/tonight.js and scripts/check_tonight.mjs. Do not hand-edit.",
        "kit_arrived": KIT_ARRIVED,
        "plate_start_min": PLATE_START_MIN,
        "budgets": list(BUDGETS),
        "gate": _gate_info(gate, chapters),
        "rows": [{
            "n": r["n"], "label": _row_label(r), "kind": r["kind"], "kit": r["kit"],
            "segments": [_seg_json(s, step_urls) for s in r["segments"]],
        } for r in rows],
    }
    # the cases run over the JSON's own rows, exactly what the JS will see
    plain = json.loads(json.dumps(data))
    data["cases"] = [{
        "name": name, "kit_arrived": kit, "ticks": ticks, "printed": printed,
        "expect": plan_state(plain, ticks, printed, kit),
    } for name, kit, ticks, printed in _cases_spec(chapters)]
    return data


def on_pre_build(config, **kwargs):
    model = _model()
    OUT.write_text(build_tonight_markdown(model), encoding="utf-8")
    TONIGHT_JSON.parent.mkdir(parents=True, exist_ok=True)
    TONIGHT_JSON.write_text(json.dumps(tonight_json(model), ensure_ascii=False, indent=1) + "\n",
                            encoding="utf-8")


# --------------------------------------------------------------------------
# self-test: python3 scripts/build_tonight.py --self-test
# --------------------------------------------------------------------------

def _self_test():
    fails = 0

    def check(name, ok, detail=""):
        nonlocal fails
        print(("PASS " if ok else "FAIL ") + name + ("" if ok else f"  {detail}"))
        fails += 0 if ok else 1

    def seg(i, kind, minutes):
        return {"id": i, "kind": kind, "minutes": minutes, "first_step": i, "pre_kit": False}

    # The lab-backlog bug: the kit-arrived (plain) branch stepped over an unfinished
    # print row and offered the next batch's plate start.
    rows = [
        {"kind": "Print", "kit": False, "segments": [seg("A.gate", "build", 20), seg("A.sort", "build", 10)]},
        {"kind": "Build", "kit": False, "segments": [seg("C.1", "build", 40)]},
        {"kind": "Print", "kit": False, "segments": [seg("B.plate", "print", 5)]},
    ]
    ids = lambda picked: [s["id"] for _r, s in picked]
    got = ids(_plan_for_budget(rows, 15)[0])
    check("misfit in batch A: batch B's plate is not offered", "B.plate" not in got, got)
    got = ids(_plan_for_budget(rows, 25)[0])
    check("batch A half done: batch B still waits", got == ["A.gate"], got)
    got = ids(_plan_for_budget(rows, 35)[0])
    check("batch A finished: batch B's plate follows", got == ["A.gate", "A.sort", "B.plate"], got)
    rows2 = [{"kind": "Print", "kit": False, "segments": [seg("A.p1", "print", 5), seg("A.p2", "print", 5)]},
             {"kind": "Print", "kit": False, "segments": [seg("B.x", "build", 10)]}]
    got = ids(_plan_for_budget(rows2, 90)[0])
    check("a started plate holds the next batch", got == ["A.p1"], got)
    rows3 = [{"kind": "Build", "kit": False, "segments": [seg("C.1", "build", 40)]},
             {"kind": "Build", "kit": False, "segments": [seg("D.1", "build", 20)]}]
    got = ids(_plan_for_budget(rows3, 30)[0])
    check("pre-kit build rows keep the per-row rule", got == ["D.1"], got)
    rows4 = [{"kind": "Build", "kit": True, "segments": [seg("E.1", "build", 40)]},
             {"kind": "Build", "kit": True, "segments": [seg("F.1", "build", 20)]},
             {"kind": "Print", "kit": False, "segments": [seg("G.plate", "print", 5)]}]
    got = ids(_plan_for_budget(rows4, 30)[0])
    check("KIT build rows are sequential; the printer track still runs",
          got == ["G.plate"], got)

    # The same bug on the real timeline, as the kit-arrived case in tonight.json.
    model = _model()
    data = tonight_json(model, step_urls={})
    case = next(c for c in data["cases"] if c["name"].startswith("kit arrived, cross-row"))
    b01 = model[0]["B01-z-drive-assemblies.md"]["slug"]
    b00 = model[0]["B00-calibration-and-jigs.md"]["slug"]
    gate_b = b00 + "#9"  # B00.7, the last B00 segment
    bad = []
    for sec in case["expect"]["sections"]:
        for b in sec["buckets"]:
            its = b["items"]
            first_b01 = next((k for k, i in enumerate(its) if i.startswith(b01 + "#")), None)
            if first_b01 is not None and gate_b not in its[:first_b01]:
                bad.append((sec["id"], b["budget"], its))
    check("real timeline: B01 is offered only after B00's Gate B in the same bucket",
          not bad, bad)
    late = next(c for c in data["cases"] if c["name"].startswith("kit arrived, run printed"))
    frame = model[0]["01-frame.md"]["slug"]
    # Ch 00 done, run printed: only row 15 (Ch 12 flashing), the frame and the B11 prints may appear.
    skipped = [(b["budget"], b["items"]) for b in late["expect"]["sections"][0]["buckets"]
               if any(i.split("#")[0] not in ("12-software", frame) and not i.startswith("b11-")
                      for i in b["items"])]
    check("real timeline: no build chapter is offered ahead of the frame", not skipped, skipped)
    b30 = case["expect"]["sections"][0]["buckets"][0]["items"]
    check("real timeline: the 30-min bucket is Gate A + sort", len(b30) == 2, b30)

    none = data["cases"][0]["expect"]
    check("static page = the none-ticked case", none["done"] == 0 and not none["gate_closed"])
    check("gate closes on B00.8", data["cases"][4]["expect"]["gate_closed"])
    check("gate stays open on B00.0", not data["cases"][3]["expect"]["gate_closed"])
    print("self-test:", "OK" if not fails else f"{fails} FAILED")
    return 1 if fails else 0


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(_self_test())
    print(build_tonight_markdown())
