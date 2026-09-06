"""mkdocs on_pre_build hook (R6 B7): generate print-ready pages.

Produces:
  docs/print/checklists.md  — every chapter's `## Checkpoint` list, one per
                               printed page (page-break before each), for
                               docs/stylesheets/print.css to render cleanly.
  docs/print/bin-labels.md  — one label per sorting bin from slicer/bins.py
                               (bin id, label, chapter · steps, the parts it
                               should contain with qty and the plates they come
                               off, a QR code linking to the chapter's step-page
                               overview), then a one-page bin map listing every
                               bin. QR codes are generated with segno (SVG, no
                               external service).
  docs/print/plate-plans.md — all 27 plate sorting diagrams on one page,
                               grouped by batch in print order, each with its
                               colour/parts/hours/grams (from slicer/estimates.csv)
                               and bins (from slicer/bins.py), linking to that
                               plate's Load step in the batch chapter.

All three files are regenerated on every build — never hand-edit them. QR SVGs
are written to docs/print/assets/qr/.
"""

import csv
import os
import sys
import re
from pathlib import Path

try:
    import segno
except ImportError:  # pragma: no cover - degrade gracefully if not installed
    segno = None

from markdown.extensions.toc import slugify as _toc_slugify

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "slicer"))
import bins  # noqa: E402  (slicer/bins.py — the bin scheme)
from plates import PLATES  # noqa: E402  (slicer/plates.py — what is on each plate)
from check_docs import r0, r1  # noqa: E402  (same additive-rounding convention as the chapters)
DOCS = REPO / "docs"
MANUAL = DOCS / "manual"
PRINT_DIR = DOCS / "print"
QR_DIR = PRINT_DIR / "assets" / "qr"
ESTIMATES = REPO / "slicer" / "estimates.csv"

# Print order (docs/manual/print/README.md "Print order" — Gate A batches, then Gate B batches).
_BATCH_PRINT_ORDER = ["B00", "B02", "B07", "B08", "B09", "B10", "B01", "B03", "B04", "B05", "B06"]

_SITE_URL = "https://alexlicohen.github.io/voron-24-350-build-manual/"

_EXCLUDE = {"00-index.md", "00-tonight.md", "CONVENTIONS.md", "README.md"}
# One owner for "what a chapter heading looks like": build_tonight.py's parser,
# so a lettered chapter (00a, 06b) or a print batch can never be visible to the
# planner and invisible to the printable sheets.
sys.path.insert(0, str(REPO / "scripts"))
from build_tonight import _CHAPTER_TITLE_RE  # noqa: E402  (# Chapter NN / # Batch BNN)

# A checkpoint heading may carry its own tail ("## Checkpoint 08 — bench test
# before anything is powered"), and a file may hold more than one (Ch 06/06b).
_CHECKPOINT_RE = re.compile(
    r"^##\s*Checkpoint\s+(\S+)\s*(?:—\s*(.+?))?\s*$\n(.*?)(?=^##\s|\Z)",
    re.MULTILINE | re.DOTALL,
)
_GROUP_RE = re.compile(r"^\*\*(.+?)\*\*$")
_PART_RE = re.compile(r"^##\s*Part\s+\S+\s*—\s*(.+?)\s*$", re.MULTILINE)
_PRINTED_PARTS_RE = re.compile(
    r"^\*\*Printed parts\*\*\s*\n\n(.*?)(?=\n\n)", re.MULTILINE | re.DOTALL
)
_STL_CELL_RE = re.compile(r"`([\w\[\]-]+\.stl)`")
_TABLE_ROW_RE = re.compile(r"^\s*\|(.+)\|\s*$", re.MULTILINE)
_LOAD_STEP_RE = re.compile(
    r"^##\s*(Step\s+\S+\s*—\s*Load(?:\s+and\s+print)?\s+plate\s+(B\d\d-P\d+)[^\n]*)$",
    re.MULTILINE,
)


def _chapter_files():
    """Assembly chapters only — this is also what the bin-label QR codes resolve
    a `Ch NN` against, so print batches must not leak into it."""
    return sorted(f for f in MANUAL.glob("*.md") if f.name not in _EXCLUDE)


def _print_files():
    return sorted(f for f in (MANUAL / "print").glob("*.md") if f.name not in _EXCLUDE)


def _slug_for(path):
    return path.stem


def _chapter_url(path):
    # mkdocs `use_directory_urls` default (true): NN-slug.md -> manual/NN-slug/
    return f"{_SITE_URL}manual/{_slug_for(path)}/"


def _parse_header(text):
    m = _CHAPTER_TITLE_RE.search(text)
    if not m:
        return None, None
    return m.group(1), m.group(2)


_LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)\s]+)\)")


def _relink(text, src_dir):
    """Re-resolve a checklist item's relative links for docs/print/checklists.md,
    which sits a directory away from the chapter the item was written in."""
    def sub(m):
        label, target = m.group(1), m.group(2)
        if target.startswith(("http://", "https://", "#", "/", "mailto:")):
            return m.group(0)
        path, _, frag = target.partition("#")
        if not path:
            return m.group(0)
        new = os.path.relpath((src_dir / path).resolve(), PRINT_DIR)
        return f"[{label}]({new}{'#' + frag if frag else ''})"
    return _LINK_RE.sub(sub, text)


def _checkpoint_items(body):
    """The checkpoint body as blocks: ("group", label) for a bold sub-heading
    (Gate A / Gate B on B00, Part A / Part B on Ch 11), ("item", text) per tick
    box. An indented continuation line joins the item above it."""
    out = []
    for raw in body.splitlines():
        line = raw.strip()
        gm = _GROUP_RE.match(line)
        if gm:
            out.append(("group", gm.group(1)))
        elif line.startswith(("- [ ]", "- [x]")):
            out.append(("item", line[5:].strip()))
        elif line and raw[:1] in " \t" and out and out[-1][0] == "item":
            out[-1] = ("item", f"{out[-1][1]} {line}")
    return out


def _checkpoints(text, title, src_dir):
    """Every checkpoint in a file, in source order: (id, label, blocks).

    The label is the checkpoint heading's own tail where it has one ("Checkpoint
    08 — bench test before anything is powered"); in a file with two checkpoints
    (Ch 06 / Ch 06b) it is the enclosing `## Part …` heading, so the two sheets
    are told apart; otherwise the chapter title."""
    out = []
    parts = [(m.start(), m.group(1)) for m in _PART_RE.finditer(text)]
    found = list(_CHECKPOINT_RE.finditer(text))
    for m in found:
        blocks = [(kind, _relink(s, src_dir)) for kind, s in _checkpoint_items(m.group(3))]
        if not blocks:
            continue
        label = (m.group(2) or "").strip()
        if not label and len(found) > 1:
            label = next((p for pos, p in reversed(parts) if pos < m.start()), "")
            label = re.sub(r"^Chapter\s+\S+\s*[:—-]\s*", "", label)
        out.append((m.group(1), label or title, blocks))
    return out


def _printed_part_names(text):
    m = _PRINTED_PARTS_RE.search(text)
    if not m:
        return []
    names = []
    for row in _TABLE_ROW_RE.finditer(m.group(1)):
        for stl in _STL_CELL_RE.findall(row.group(1)):
            names.append(stl)
    return names


def _write_qr(slug, url):
    if segno is None:
        return None
    QR_DIR.mkdir(parents=True, exist_ok=True)
    out = QR_DIR / f"{slug}.svg"
    segno.make(url, error="m").save(out, kind="svg", scale=4, border=2)
    return out.relative_to(PRINT_DIR)


def build_checklists_markdown(chapters):
    lines = [
        "# Printable checklists",
        "",
        "_Generated by `scripts/build_printables.py` — do not hand-edit. Print with "
        "`.print-images` off (default) for a text-only sheet._",
        "",
        "One page per checkpoint, assembly chapters first (Ch 00 → Ch 14, including "
        "Ch 00a and Ch 06b), then the print batches in print order (B00 → B10). "
        "**Gate A** and **Gate B** are the two halves of the B00 sheet — the day-1 and "
        "kit-day gates for the whole build.",
        "",
    ]
    first = True
    for path, _number, title, text in chapters:
        for cp_id, label, blocks in _checkpoints(text, title, path.parent):
            if not first:
                lines.append('<div class="print-page-break"></div>')
                lines.append("")
            first = False
            lines.append(f"## Checkpoint {cp_id} — {label}")
            lines.append("")
            for btype, text_ in blocks:
                if btype == "group":
                    lines.append(f"**{text_}**")
                    lines.append("")
                else:
                    lines.append(f"- [ ] {text_}")
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _chapter_overview_url(chapter_number):
    """The chapter's step-page overview (scripts/build_steps.py writes
    docs/manual/steps/<chapter-slug>/index.md), e.g. manual/steps/02-z-drives/."""
    for path in _chapter_files():
        if path.stem.startswith(f"{chapter_number}-"):
            return f"{_SITE_URL}manual/steps/{path.stem}/", path.stem
    return None, None


def _bin_contents():
    """bin id -> {stl: {"n": copies, "plates": [plate ids]}} from slicer/plates.py + bins.py."""
    out = {}
    for pid, spec in PLATES.items():
        for _repo, path, qty in spec["parts"]:
            stl = path.rsplit("/", 1)[-1]
            for b in bins.copies_bins(pid, stl, qty):
                entry = out.setdefault(b, {}).setdefault(stl, {"n": 0, "plates": []})
                entry["n"] += 1
                if pid not in entry["plates"]:
                    entry["plates"].append(pid)
    return out


def _label_block(bin_id, meta, contents, qr_rel):
    lines = [f"### {bin_id}", "", f"**{meta['label']}**", "",
             f"_{meta['chapter']} · {meta['steps']}_", ""]
    if contents:
        lines.append("**Should contain:**")
        lines.append("")
        for stl, entry in contents.items():
            qty = f" ×{entry['n']}" if entry["n"] > 1 else ""
            note = bins.NOTES.get(stl)
            plates = ", ".join(entry["plates"])
            lines.append(f"- `{bins.short_name(stl)}`{qty} — {plates}" + (f" — {note}" if note else ""))
        lines.append("")
        n = sum(e["n"] for e in contents.values())
        lines.append(f"_{n} piece{'s' if n != 1 else ''}_")
    else:
        lines.append("_(empty — nothing in the plan feeds this bin)_")
    lines.append("")
    if qr_rel:
        lines.append(f"![QR link to the chapter overview]({qr_rel})")
    lines.append("")
    return lines


def build_bin_labels_markdown(chapters):
    lines = [
        "# Bin labels",
        "",
        "_Generated by `scripts/build_printables.py` from `slicer/bins.py` — do not hand-edit. One label per "
        "bin: cut along the page breaks, tape to the box. The bin id is also what the plate diagrams and the "
        "batch chapters' *Sort into bins* steps use, and each QR links to the chapter's step overview. The last "
        "page is the bin map._",
        "",
    ]
    contents = _bin_contents()
    for bin_id, meta in bins.BINS.items():
        number = meta["chapter"].replace("Ch ", "") if meta["chapter"].startswith("Ch ") else None
        url, slug = _chapter_overview_url(number) if number else (None, None)
        if url is None:
            url, slug = f"{_SITE_URL}manual/print/#bins", "print-README-bins"
        qr_rel = _write_qr(f"bin-{bin_id}", url)
        lines += _label_block(bin_id, meta, contents.get(bin_id, {}), qr_rel)
        lines.append('<div class="print-page-break"></div>')
        lines.append("")

    lines += ["## Bin map", "",
              "_All bins on one page — which chapter opens each one, and what should be inside._", "",
              "| bin | label | chapter · steps | pieces | from batches |", "|---|---|---|---:|---|"]
    for bin_id, meta in bins.BINS.items():
        c = contents.get(bin_id, {})
        n = sum(e["n"] for e in c.values())
        batches = sorted({p[:3] for e in c.values() for p in e["plates"]})
        lines.append(f"| **{bin_id}** | {meta['label']} | {meta['chapter']} · {meta['steps']} | {n} | "
                     f"{', '.join(batches)} |")
    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _load_estimates():
    """plate id -> (colour, parts, display-hours, display-grams), rounded the same additive
    way as the batch chapters and print/README.md (slicer/check_docs.py r1/r0) so every caption
    on this page matches the number already printed elsewhere."""
    out = {}
    with ESTIMATES.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            if row["plate"] == "TOTAL":
                continue
            out[row["plate"]] = (row["colour"], int(row["parts"]), r1(row["hours"]), r0(row["grams"]))
    return out


def _plate_bins():
    """plate id -> bin ids on it, in slicer/bins.py order — same owner function
    (bins.copies_bins) that _bin_contents() uses, just grouped the other way round."""
    out = {}
    for pid, spec in PLATES.items():
        seen = set()
        for _repo, path, qty in spec["parts"]:
            stl = path.rsplit("/", 1)[-1]
            seen.update(bins.copies_bins(pid, stl, qty))
        out[pid] = [b for b in bins.BINS if b in seen] + sorted(seen - set(bins.BINS))
    return out


def _batch_files():
    """batch id -> (path, title) for docs/manual/print/BNN-*.md."""
    out = {}
    for path in _print_files():
        text = path.read_text(encoding="utf-8")
        number, title = _parse_header(text)
        if number:
            out[number] = (path, title, text)
    return out


def _check_batch_print_order(plates_by_batch, batches):
    """`_BATCH_PRINT_ORDER` is hand-maintained from docs/manual/print/README.md's
    "Print order" section — fail loudly instead of silently dropping/duplicating
    a batch if a new one is added there without updating this list."""
    known = set(plates_by_batch) | set(batches)
    listed = set(_BATCH_PRINT_ORDER)
    missing = known - listed
    extra = listed - known
    dupes = {b for b in _BATCH_PRINT_ORDER if _BATCH_PRINT_ORDER.count(b) > 1}
    if missing or extra or dupes:
        problems = []
        if missing:
            problems.append(f"missing from _BATCH_PRINT_ORDER: {sorted(missing)}")
        if extra:
            problems.append(f"in _BATCH_PRINT_ORDER but no such batch: {sorted(extra)}")
        if dupes:
            problems.append(f"listed more than once: {sorted(dupes)}")
        raise SystemExit(
            "build_printables.py: _BATCH_PRINT_ORDER is out of sync with "
            "slicer/plates.py / docs/manual/print/ — " + "; ".join(problems)
        )


def build_plate_plans_markdown():
    estimates = _load_estimates()
    plate_bins = _plate_bins()
    batches = _batch_files()

    plates_by_batch = {}
    for pid, spec in PLATES.items():
        plates_by_batch.setdefault(spec["batch"], []).append(pid)

    _check_batch_print_order(plates_by_batch, batches)

    total_hours = sum(h for _c, _n, h, _g in estimates.values())
    grams_black = sum(g for c, _n, _h, g in estimates.values() if c == "black")
    grams_orange = sum(g for c, _n, _h, g in estimates.values() if c == "orange")

    lines = [
        "# Plate plans",
        "",
        "_Generated by `scripts/build_printables.py` — do not hand-edit._",
        "",
        f"All **{len(estimates)} plates**, **{total_hours:.1f} h**, **{grams_black:.0f} g Galaxy Black + "
        f"{grams_orange:.0f} g Prusa Orange**, in print order (batches: "
        f"{' → '.join(_BATCH_PRINT_ORDER)}). Every diagram is drawn from the committed PrusaSlicer "
        "project `slicer/plates/<id>.3mf` (`python3 slicer/build_plates.py --from-3mf`).",
        "",
    ]

    for batch in _BATCH_PRINT_ORDER:
        path, title, text = batches[batch]
        rel = os.path.relpath(path, PRINT_DIR)
        lines.append(f"## Batch {batch} — [{title}]({rel})")
        lines.append("")
        load_steps = {m.group(2): m.group(1) for m in _LOAD_STEP_RE.finditer(text)}
        lines.append(f'<div class="plate-grid" markdown="1">')
        lines.append("")
        for pid in plates_by_batch.get(batch, []):
            colour, parts, hours, grams = estimates[pid]
            bin_list = ", ".join(plate_bins.get(pid, []))
            heading = load_steps.get(pid)
            if heading is None:
                raise SystemExit(f"build_printables.py: no Load step for plate {pid} in {path.name}")
            anchor = _toc_slugify(heading, "-")
            lines.append(f'<div class="plate-card" markdown="1">')
            lines.append("")
            lines.append(f"![Plate {pid} — sorting diagram](../manual/assets/plates/{pid}.png)")
            lines.append("")
            lines.append(
                f"**{pid}** · {colour} · {parts} parts · {hours:.1f} h · {grams:.0f} g · "
                f"bins: {bin_list} · [Load step]({rel}#{anchor})"
            )
            lines.append("")
            lines.append("</div>")
            lines.append("")
        lines.append("</div>")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def _load_chapters():
    """Assembly chapters then print batches, each in file order — which is
    chapter order (00, 00a, 01 … 14) and print order (B00 … B10)."""
    chapters = []
    for paths in (_chapter_files(), _print_files()):
        for path in paths:
            text = path.read_text(encoding="utf-8")
            number, title = _parse_header(text)
            if number is None:          # print/README.md, 00-slicer-setup.md
                continue
            chapters.append((path, number, title, text))
    return chapters


def on_pre_build(config, **kwargs):
    PRINT_DIR.mkdir(parents=True, exist_ok=True)
    chapters = _load_chapters()
    (PRINT_DIR / "checklists.md").write_text(
        build_checklists_markdown(chapters), encoding="utf-8"
    )
    (PRINT_DIR / "bin-labels.md").write_text(
        build_bin_labels_markdown(chapters), encoding="utf-8"
    )
    (PRINT_DIR / "plate-plans.md").write_text(
        build_plate_plans_markdown(), encoding="utf-8"
    )


if __name__ == "__main__":
    chapters = _load_chapters()
    print(build_checklists_markdown(chapters)[:2000])
    print("---")
    print(build_bin_labels_markdown(chapters)[:2000])
    print("---")
    print(build_plate_plans_markdown()[:2000])
