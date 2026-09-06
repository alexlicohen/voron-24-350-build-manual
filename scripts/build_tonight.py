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
that fits nothing says so. "Kit not here yet" runs the same planner over the
rows that carry no **KIT** marker.

Each segment carries `data-first-step` so scripts/build_steps.py can link it
to its first step page. This file is regenerated on every build — never
hand-edit docs/manual/00-tonight.md.
"""

import re
from collections import defaultdict
from pathlib import Path

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
MANUAL = REPO / "docs" / "manual"
PRINT = MANUAL / "print"
INDEX = MANUAL / "00-index.md"
OUT = MANUAL / "00-tonight.md"

PLATE_START_MIN = 5  # open the project, confirm the estimate, start, watch the first layer

_CHAPTER_TITLE_RE = re.compile(
    r"^#\s*(?:Chapter|Batch)\s+([A-Za-z]?\d+[a-z]?)\s*—\s*(.+?)\s*$", re.MULTILINE
)
_TIME_RE = re.compile(r"^\*\*Time:\*\*\s*(.+)$", re.MULTILINE)
_TIME_RANGE_RE = re.compile(r"(\d+(?:\.\d+)?)\s*(?:[–-]\s*(\d+(?:\.\d+)?))?\s*h")
_STEP_HEADING_RE = re.compile(
    r"^#{2,3}\s*Step\s+([A-Za-z]?\d+[A-Za-z]?\.\d+)\s*—\s*(.*?)\s*$", re.MULTILINE
)
_SECTION_RE = re.compile(r"^#{2,3}\s+(.+?)\s*$", re.MULTILINE)  # any h2/h3: a row's anchor may be a Part or a Step
_PAUSE_RE = re.compile(
    r"^>?\s*Pause:\s*~?(\d+)\s*min\s*since the last pause\s*—\s*(.+?)\s*$",
    re.MULTILINE,
)
_LOAD_TITLE_RE = re.compile(r"^Load(?: and print)? plate (B\d\d-P\d)")
_PRINT_TITLE_RE = re.compile(r"^Print\b")
_PARTS_TIME_RE = re.compile(
    r"^\*\*Parts:\*\*.*?— ([\d.]+) h, (\d+) g \(PrusaSlicer", re.MULTILINE
)
_ROW_RE = re.compile(r"^- \*\*(\d+) · (Print|Build|Both)\*\* — (.*)$", re.MULTILINE)
_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)#\s]+)(?:#([^)\s]+))?\)")
_EXCLUDE = {"00-index.md", "00-tonight.md", "CONVENTIONS.md", "README.md"}


# --------------------------------------------------------------------------
# index timeline
# --------------------------------------------------------------------------

def _timeline_rows():
    """The index's numbered rows, in order: n, kind, title, file, anchor, kit."""
    rows = []
    for m in _ROW_RE.finditer(INDEX.read_text(encoding="utf-8")):
        n, kind, rest = int(m.group(1)), m.group(2), m.group(3)
        lm = _LINK_RE.search(rest)
        if lm:
            title, file, anchor = lm.group(1), lm.group(2), lm.group(3)
        else:
            title = re.sub(r"\*\*", "", rest.split(" · ")[0]).strip()
            file = anchor = None
        rows.append({
            "n": n, "kind": kind, "title": title, "file": file, "anchor": anchor,
            "kit": "**KIT" in rest, "segments": [],
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
                "kind": "print", "pos": pos, "first_step": sid, "last_step": sid,
                "plate": lm.group(1), "minutes": PLATE_START_MIN, "print_hours": plate_h,
                "grams": grams,
                "leave_state": (f"plate {lm.group(1)} running, {hours_txt} unattended — "
                                f"door shut; come back for the next step when it ends"),
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
            "minutes": int(pm.group(1)), "leave_state": pm.group(2),
        })
        boundary = ppos

    segments.sort(key=lambda s: s["pos"])
    return {
        "number": number, "title": title, "path": path, "hours": hours,
        "print_hours": print_hours if is_print else None, "is_print": is_print,
        "segments": segments, "sections": sections,
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
# --------------------------------------------------------------------------

def _plan_for_budget(rows, budget):
    """Greedy pack in timeline order. One plate start per plan; a segment
    that does not fit takes the rest of its row with it (sequential work)."""
    picked, total, plate_started = [], 0, False
    for row in rows:
        for seg in row["segments"]:
            if seg["kind"] == "print":
                if plate_started or total + seg["minutes"] > budget:
                    break
                picked.append((row, seg))
                total += seg["minutes"]
                plate_started = True
                break  # the rest of this batch waits for the plate
            if total + seg["minutes"] > budget:
                break
            picked.append((row, seg))
            total += seg["minutes"]
        if budget - total < PLATE_START_MIN:
            break
    return picked, total


def _next_segment(rows):
    for row in rows:
        for seg in row["segments"]:
            return row, seg
    return None, None


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


def _planner(lines, rows):
    for label, budget in (("30 min", 30), ("60 min", 60), ("90 min", 90)):
        picked, total = _plan_for_budget(rows, budget)
        lines.append(f"**If you have {label}:**")
        if not picked:
            row, seg = _next_segment(rows)
            if seg is None:
                lines.append("- nothing to plan — no segments on this timeline yet")
            else:
                lines.append(f"- nothing fits in {label} — the next segment is "
                             f"{_row_label(row)} — {_segment_text(seg)}")
        for row, seg in picked:
            lines.append(f"- {_row_label(row)} — {_segment_span(seg)}")
        lines.append(f"  <small>~{total} min hands-on planned</small>")
        lines.append("")


def build_tonight_markdown():
    chapters = {f.name: _parse_chapter(f) for f in _chapter_files()}
    rows = _assign(_timeline_rows(), chapters)

    build_chapters = [c for c in chapters.values() if not c["is_print"] and c["hours"] is not None]
    total_hours = sum(c["hours"] for c in build_chapters)
    print_chapters = [c for c in chapters.values() if c["is_print"]]
    total_print = sum(c["print_hours"] or 0 for c in print_chapters)
    n_plates = sum(1 for c in print_chapters for s in c["segments"] if s["kind"] == "print")

    lines = [
        "# Tonight",
        "",
        "_Generated by `scripts/build_tonight.py` on every build — do not hand-edit. "
        "Order is the index timeline; checked-off state is overlaid client-side from your browser's saved progress._",
        "",
        f"**Total remaining (estimate):** ~{total_hours:.1f} h hands-on across "
        f"{len(build_chapters)} build chapters; {total_print:.1f} h of printing across "
        f"{n_plates} plates (~{PLATE_START_MIN} min hands-on per plate start, the rest unattended).",
        "",
        "## Tonight's planner",
        "",
        "Timeline order. One plate start per plan (one printer): a plate start is "
        f"~{PLATE_START_MIN} min hands-on — open the project, confirm the estimate, start it, watch the "
        "first layer — and then the printer runs unattended for the hours shown, so the rest of a "
        "30-minute bucket can go on bench work.",
        "",
    ]

    if not any(r["segments"] for r in rows):
        lines.append(
            "_No stopping points marked yet anywhere in the manual — chapters are still "
            "being written. Check back once `Pause:` lines land._"
        )
    else:
        _planner(lines, rows)

    pre_kit = [r for r in rows if not r["kit"] and r["segments"]]
    lines += ["## Kit not here yet", ""]
    if pre_kit:
        lines += [
            "The same planner over the timeline rows without the **KIT** marker — the Core One+ "
            "batches and the bench work that needs no Voron part.",
            "",
        ]
        _planner(lines, pre_kit)
    else:
        lines += ["_Every timeline row needs the kit._", ""]

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

    return "\n".join(lines).rstrip() + "\n"


def on_pre_build(config, **kwargs):
    OUT.write_text(build_tonight_markdown(), encoding="utf-8")


if __name__ == "__main__":
    print(build_tonight_markdown())
