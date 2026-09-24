"""mkdocs on_pre_build hook (R6 B7): generate print-ready pages.

Produces:
  docs/print/checklists.md  — every chapter's `## Checkpoint` list, one per
                               printed page (page-break before each), for
                               docs/stylesheets/print.css to render cleanly,
                               then one more page, `## Plate review (B00.8)`:
                               one checkbox per plate (batch, material, sheet,
                               time, grams from slicer/plates.py + estimates.csv)
                               for Step B00.8 in the B00 batch chapter, so that
                               step never hand-types the 27 plate ids.
  docs/print/bin-labels.md  — one label per sorting bin from slicer/bins.py
                               (bin id, label, chapter · steps, the parts it
                               should contain with qty and the plates they come
                               off, a QR code linking to the chapter's step-page
                               overview), then a one-page bin map listing every
                               bin, then a 1:1 fastener gauge (inline SVG in mm,
                               from the kit BOM). QR codes are generated with segno
                               (SVG, no external service).
  docs/print/plate-plans.md — every plate sorting diagram on one page,
                               grouped by batch in print order, each with its
                               colour/parts/hours/grams (from slicer/estimates.csv)
                               and bins (from slicer/bins.py), linking to that
                               plate's Load step in the batch chapter.

  docs/assets/build-progress.json — every assembly chapter with its step ids and
                               its cumulative CAD render, for the "what you have
                               built so far" block on Home (docs/javascripts/boards.js).

  docs/assets/plate-board.json — the 22 plates of the ASA run in run order, then
                               B11's PETG V0 plates, with hours, grams,
                               colour, slot, spool and predicted remaining, for
                               the plate board (docs/print/plate-board.md). Hours
                               and grams come from slicer/estimates.csv; slot,
                               spool and remaining are parsed out of
                               docs/manual/print/README.md's hand-written
                               "Run schedule" and "Spool ledger" tables (B11:
                               "B11 run schedule", "B11 spool ledger") and
                               cross-checked against the CSV — a table that stops
                               parsing, or disagrees, fails the build. Also: each
                               batch's gate on its first plate's note, four
                               `milestone` plates, and `runs` (one header line
                               each for the ASA run and B11, never summed).

All five files are regenerated on every build — never hand-edit them. QR SVGs
are written to docs/print/assets/qr/.
"""

import csv
import json
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
sys.path.insert(0, str(REPO / "hooks"))
import mascot  # noqa: E402  (hooks/mascot.py — the raven's markup and asset paths)

sys.path.insert(0, str(REPO / "slicer"))
import bins  # noqa: E402  (slicer/bins.py — the bin scheme)
from plates import PLATES, run_of  # noqa: E402  (slicer/plates.py — what is on each plate)
from check_docs import r0, r1  # noqa: E402  (same additive-rounding convention as the chapters)
DOCS = REPO / "docs"
MANUAL = DOCS / "manual"
PRINT_DIR = DOCS / "print"
QR_DIR = PRINT_DIR / "assets" / "qr"
DATA_DIR = DOCS / "assets"
CAD_DIR = MANUAL / "assets" / "cad"
PLATE_DIAGRAMS = MANUAL / "assets" / "plates"
ESTIMATES = REPO / "slicer" / "estimates.csv"
README = MANUAL / "print" / "README.md"

# A plate of this many hours or more starts in the evening and runs overnight
# (docs/manual/print/README.md "Run schedule"). Parsed rows are checked against it.
OVERNIGHT_H = 7.0

# Print order (docs/manual/print/README.md "Print order" — Gate A batches, then Gate B batches).
_BATCH_PRINT_ORDER = ["B00", "B01", "B02", "B03", "B04", "B05", "B06", "B07", "B08", "B09", "B10",
                      "B11"]   # B11: PETG V0 bay ducting, outside the ASA run

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
                    # A group heading after a tick box needs its own paragraph, or
                    # python-markdown folds it into the last item's text (sweep G8-13).
                    if lines[-1] != "":
                        lines.append("")
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


# ---------------------------------------------------------------------------
# Fastener gauge (sweep G1-28): 1:1 silhouettes of every M3/M5 SHCS/BHCS/FHCS the
# kit BOM ships, the heat-set insert and both roll-in T-nuts, plus a 50 mm bar to
# check the print scale. Inline SVG in mm, so it prints true at 100 %.
# ---------------------------------------------------------------------------

_SCREW_RE = re.compile(r"^Machine Screw, (SHCS|BHCS|FHCS), M([35])x(\d+)$")
_INSERT_RE = re.compile(r"^Heatset Insert, Brass, (M3x(\d+)x(\d+))$")
_TNUT_RE = re.compile(r"^T-nut, Roll-in, 2020, M([35])$")
# Head sizes (mm): SHCS ISO 4762 (dk, k); BHCS ISO 7380 (dk, k); FHCS dk as drawn in
# the Voron CAD (~/.cache/voron-cad index: M3 FHCS head 6.0 mm), 90° countersink.
_HEAD = {("SHCS", 3): (5.5, 3.0), ("SHCS", 5): (8.5, 5.0),
         ("BHCS", 3): (5.7, 1.65), ("BHCS", 5): (9.5, 2.75),
         ("FHCS", 3): (6.0, 1.5), ("FHCS", 5): (10.0, 2.5)}
# Roll-in (drop-in) 2020 T-nut footprint from the same CAD: M3 12.5 × 7.7, M5 13.0 × 7.7.
_TNUT = {3: (12.5, 7.7), 5: (13.0, 7.7)}
_TYPE_ORDER = {"SHCS": 0, "BHCS": 1, "FHCS": 2}


def _gauge_items():
    """(screws, insert, tnuts) from the vendored kit BOM, via scripts/parts.py's loader."""
    import parts   # scripts/parts.py owns the BOM load
    screws, insert, tnuts = [], None, []
    for row in parts.load_bom():
        item = str(row.get("item", "")).strip()
        m = _SCREW_RE.match(item)
        if m:
            screws.append((m.group(1), int(m.group(2)), int(m.group(3)), row.get("qty")))
            continue
        m = _INSERT_RE.match(item)
        if m:
            insert = (m.group(1), float(m.group(2)), float(m.group(3)), row.get("qty"))
            continue
        m = _TNUT_RE.match(item)
        if m:
            tnuts.append((int(m.group(1)), row.get("qty")))
    screws.sort(key=lambda s: (s[1], _TYPE_ORDER[s[0]], s[2]))
    tnuts.sort()
    return screws, insert, tnuts


def _f(x):
    return f"{x:.2f}".rstrip("0").rstrip(".")


def _screw_svg(kind, d, length, xo, y):
    """One screw lying along +x, its length measured from x = xo (under the head for
    SHCS/BHCS, the flat top for FHCS), plus a length bar under the shank."""
    dk, k = _HEAD[(kind, d)]
    out = []
    shank = 'fill="currentColor" fill-opacity="0.35" stroke="currentColor" stroke-width="0.2"'
    head = 'fill="currentColor" fill-opacity="0.75" stroke="currentColor" stroke-width="0.2"'
    if kind == "SHCS":
        out.append(f'<rect x="{_f(xo - k)}" y="{_f(y - dk / 2)}" width="{_f(k)}" height="{_f(dk)}" {head}/>')
        out.append(f'<rect x="{_f(xo)}" y="{_f(y - d / 2)}" width="{_f(length)}" height="{_f(d)}" {shank}/>')
    elif kind == "BHCS":
        out.append(f'<path d="M{_f(xo)} {_f(y - dk / 2)} A{_f(k)} {_f(dk / 2)} 0 0 0 {_f(xo)} {_f(y + dk / 2)} Z" {head}/>')
        out.append(f'<rect x="{_f(xo)}" y="{_f(y - d / 2)}" width="{_f(length)}" height="{_f(d)}" {shank}/>')
    else:   # FHCS: the countersunk head is inside the stated length
        out.append(f'<path d="M{_f(xo)} {_f(y - dk / 2)} L{_f(xo + k)} {_f(y - d / 2)} '
                   f'L{_f(xo + k)} {_f(y + d / 2)} L{_f(xo)} {_f(y + dk / 2)} Z" {head}/>')
        out.append(f'<rect x="{_f(xo + k)}" y="{_f(y - d / 2)}" width="{_f(length - k)}" height="{_f(d)}" {shank}/>')
    by = y + max(d / 2, 1.5) + 1.2
    out.append(f'<path d="M{_f(xo)} {_f(by)} H{_f(xo + length)} M{_f(xo)} {_f(by - 0.7)} V{_f(by + 0.7)} '
               f'M{_f(xo + length)} {_f(by - 0.7)} V{_f(by + 0.7)}" stroke="currentColor" stroke-width="0.25" fill="none"/>')
    return out


def _fastener_gauge_svg():
    screws, insert, tnuts = _gauge_items()
    if not screws:
        raise SystemExit("build_printables.py: no M3/M5 screws parsed from scripts/data/ldo-350-bom.yml "
                         "— the fastener gauge would be empty")
    txt = 'fill="currentColor" font-family="Arial, Helvetica, sans-serif"'
    parts_ = []
    cols = {3: (16.0, 8.5), 5: (104.0, 12.5)}   # size -> (origin x, row pitch)
    bottom = 0.0
    for size, (xo, pitch) in cols.items():
        rows = [s for s in screws if s[1] == size]
        if not rows:
            continue
        top = 8.0
        parts_.append(f'<text x="{_f(xo - 12)}" y="4" font-size="3.6" font-weight="700" {txt}>M{size} screws</text>')
        y_first, y_last = top + pitch / 2, top + pitch / 2 + pitch * (len(rows) - 1)
        parts_.append(f'<path d="M{_f(xo)} {_f(y_first - pitch / 2 + 1)} V{_f(y_last + pitch / 2 - 1)}" '
                      f'stroke="currentColor" stroke-width="0.2" stroke-dasharray="1 1" fill="none"/>')
        max_len = max(s[2] for s in rows)
        for i, (kind, d, length, qty) in enumerate(rows):
            y = top + pitch / 2 + pitch * i
            parts_ += _screw_svg(kind, d, length, xo, y)
            parts_.append(f'<text x="{_f(xo + max_len + 3)}" y="{_f(y + 1)}" font-size="2.8" {txt}>'
                          f'M{d}×{length} {kind}</text>')
        bottom = max(bottom, y_last + pitch / 2)

    # insert and T-nuts under the M5 column
    xo = cols[5][0]
    y = 8.0 + cols[5][1] * sum(1 for s in screws if s[1] == 5) + 6
    if insert:
        name, od, ln, _q = insert
        parts_.append(f'<rect x="{_f(xo)}" y="{_f(y - od / 2)}" width="{_f(ln)}" height="{_f(od)}" '
                      f'fill="currentColor" fill-opacity="0.5" stroke="currentColor" stroke-width="0.2"/>')
        for kx in range(1, int(ln)):
            parts_.append(f'<path d="M{_f(xo + kx)} {_f(y - od / 2)} V{_f(y + od / 2)}" stroke="currentColor" '
                          f'stroke-width="0.15" fill="none"/>')
        cx = xo + ln + 6
        parts_.append(f'<circle cx="{_f(cx)}" cy="{_f(y)}" r="{_f(od / 2)}" fill="currentColor" fill-opacity="0.5" '
                      f'stroke="currentColor" stroke-width="0.2"/>')
        parts_.append(f'<circle cx="{_f(cx)}" cy="{_f(y)}" r="1.5" style="fill: var(--md-default-bg-color, #fff)" stroke="currentColor" stroke-width="0.2"/>')
        parts_.append(f'<text x="{_f(cx + od / 2 + 3)}" y="{_f(y + 1)}" font-size="2.8" {txt}>'
                      f'{name.replace("x", "×")} heat-set insert, Ø{_f(od)} × {_f(ln)} mm</text>')
        y += 12
    for size, _q in tnuts:
        w, h = _TNUT[size]
        parts_.append(f'<rect x="{_f(xo)}" y="{_f(y - h / 2)}" width="{_f(w)}" height="{_f(h)}" rx="1.2" '
                      f'fill="currentColor" fill-opacity="0.35" stroke="currentColor" stroke-width="0.2"/>')
        parts_.append(f'<circle cx="{_f(xo + w / 2)}" cy="{_f(y)}" r="{_f(size / 2)}" style="fill: var(--md-default-bg-color, #fff)" '
                      f'stroke="currentColor" stroke-width="0.2"/>')
        parts_.append(f'<text x="{_f(xo + w + 3)}" y="{_f(y + 1)}" font-size="2.8" {txt}>'
                      f'M{size} roll-in T-nut, top view: M{size} hole</text>')
        y += h + 4
    bottom = max(bottom, y - 2)

    # 50 mm scale bar
    y0 = bottom + 6
    ticks = []
    for mm in range(0, 51):
        t = 3.0 if mm % 10 == 0 else (2.0 if mm % 5 == 0 else 1.2)
        ticks.append(f"M{_f(4 + mm)} {_f(y0)} V{_f(y0 + t)}")
    parts_.append(f'<path d="M4 {_f(y0)} H54 {" ".join(ticks)}" stroke="currentColor" stroke-width="0.2" fill="none"/>')
    for mm in range(0, 51, 10):
        parts_.append(f'<text x="{_f(4 + mm)}" y="{_f(y0 + 6.2)}" font-size="2.6" text-anchor="middle" {txt}>{mm}</text>')
    parts_.append(f'<text x="58" y="{_f(y0 + 3)}" font-size="2.8" {txt}>50 mm: caliper this bar. 50.0 mm means '
                  f'the sheet printed at 100 %.</text>')
    height = y0 + 9
    width = 172
    return (f'<svg class="fastener-gauge__svg" xmlns="http://www.w3.org/2000/svg" width="{width}mm" '
            f'height="{_f(height)}mm" viewBox="0 0 {width} {_f(height)}" role="img" '
            'style="max-width: 100%; height: auto" '
            f'aria-label="Fastener gauge: kit screws, insert and T-nuts drawn at 1:1, with a 50 mm scale bar">'
            + "".join(parts_) + "</svg>")


def build_fastener_gauge_markdown():
    return [
        '<div class="print-page-break"></div>',
        "",
        "## Fastener gauge, print at 100 %",
        "",
        "_Every M3 and M5 cap, button and flat head screw in the kit BOM "
        "(`scripts/data/ldo-350-bom.yml`), the heat-set insert and both roll-in T-nuts, drawn 1:1. "
        "Print with scaling at 100 % (not *fit to page*), then check the 50 mm bar with the caliper. "
        "Lay a screw on its drawing: length runs from the dashed line, under the head for cap and button "
        "heads, from the flat top for a flat head. The bar under each shank is that length._",
        "",
        '<div class="fastener-gauge">',
        _fastener_gauge_svg(),
        "</div>",
        "",
    ]


def build_bin_labels_markdown(chapters):
    lines = [
        "# Bin labels",
        "",
        # extra.css hides every mascot inside @media print (even under the
        # `.print-images` opt-in these sheets need for their QR codes and plate
        # diagrams), so the bird is on the screen copy and never on the paper.
        mascot.panel_html("carry"),
        "",
        "_Generated by `scripts/build_printables.py` from `slicer/bins.py` — do not hand-edit. One label per "
        "bin: cut along the page breaks, tape to the box. The bin id is also what the plate diagrams and the "
        "batch chapters' *Sort into bins* steps use, and each QR links to the chapter's step overview. Then "
        "the bin map, and last a 1:1 fastener gauge._",
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
    lines += build_fastener_gauge_markdown()
    return "\n".join(lines).rstrip() + "\n"


def _load_estimates():
    """plate id -> (colour, parts, display-hours, display-grams), rounded the same additive
    way as the batch chapters and print/README.md (slicer/check_docs.py r1/r0) so every caption
    on this page matches the number already printed elsewhere."""
    out = {}
    with ESTIMATES.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            if row["plate"].startswith("TOTAL"):
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

    asa = {pid: e for pid, e in estimates.items() if run_of(pid) == "asa"}
    bay = {pid: e for pid, e in estimates.items() if run_of(pid) != "asa"}
    total_hours = sum(h for _c, _n, h, _g in asa.values())
    grams_black = sum(g for c, _n, _h, g in asa.values() if c == "black")
    grams_accent = sum(g for c, _n, _h, g in asa.values() if c == "blue")

    lines = [
        "# Plate plans",
        "",
        mascot.panel_html("gather"),   # screen only; extra.css hides it in @media print
        "",
        "_Generated by `scripts/build_printables.py` — do not hand-edit._",
        "",
        f"All **{len(asa)} plates** of the ASA run, **{total_hours:.1f} h**, **{grams_black:.0f} g Galaxy "
        f"Black + {grams_accent:.0f} g ASA Blue**, in print order (batches: "
        f"{' → '.join(b for b in _BATCH_PRINT_ORDER if b != 'B11')}), then B11, the bay ducting: "
        f"**{len(bay)} plates**, **{sum(h for _c, _n, h, _g in bay.values()):.1f} h**, "
        f"**{sum(g for _c, _n, _h, g in bay.values()):.0f} g Jet Black PETG V0**, outside the run's totals. "
        "Every diagram is drawn from the committed PrusaSlicer "
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


def build_plate_review_markdown():
    """`## Plate review (B00.8)` — one checkbox per plate, appended to
    docs/print/checklists.md for Step B00.8 (docs/manual/print/B00-calibration-and-jigs.md):
    "Review every plate in PrusaSlicer, together". Never hand-write the 27 plate ids in the
    chapter — this is the generated list they tick against, batch/colour/material/sheet from
    `slicer/plates.py` (`run_of`), hours/grams from `slicer/estimates.csv` via `_load_estimates`,
    same sources `build_plate_plans_markdown` above reads."""
    estimates = _load_estimates()
    plates_by_batch: dict[str, list[str]] = {}
    for pid, spec in PLATES.items():
        plates_by_batch.setdefault(spec["batch"], []).append(pid)

    lines = [
        "## Plate review (B00.8)",
        "",
        "_Generated by `scripts/build_printables.py` from `slicer/plates.py` and "
        "`slicer/estimates.csv` — do not hand-edit. One box per plate for "
        "[Step B00.8](../manual/print/B00-calibration-and-jigs.md#step-b008-review-every-plate-in-prusaslicer-together): "
        "open it in PrusaSlicer 2.9.6, slice it, and check the slicer's time and grams "
        "against the figure here._",
        "",
    ]
    for batch in _BATCH_PRINT_ORDER:
        pids = plates_by_batch.get(batch, [])
        if not pids:
            continue
        lines.append(f"**Batch {batch}**")
        lines.append("")
        for pid in pids:
            colour, _parts, hours, grams = estimates[pid]
            asa = run_of(pid) == "asa"
            material = "ASA" if asa else "PETG V0"
            sheet = "smooth/satin" if asa else "textured"
            # `colour` is "petg" for every B11 plate (slicer/plates.py's colour key doubles
            # as its ini/profile selector there) — the actual filament is Jet Black PETG V0.
            shown_colour = "black" if colour == "petg" else colour
            lines.append(
                f"- [ ] {pid} — {material}, {sheet} sheet, {shown_colour} · "
                f"{hours:.1f} h · {grams:.0f} g"
            )
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


# ---------------------------------------------------------------------------
# JSON for the two client-side boards (R7). Both are read at runtime by
# docs/javascripts/boards.js; neither carries a hand-maintained list.
# ---------------------------------------------------------------------------

_STEP_HEAD_RE = re.compile(r"^#{2,3}\s*Step\s+([A-Za-z]?\d+[A-Za-z]?\.\d+)\b")
_FENCE_RE = re.compile(r"^\s{0,3}(`{3,}|~{3,})")


def _step_ids(text):
    """Every step id in a chapter, in source order, ignoring fenced code
    (Ch 12's printer.cfg carries `## Step`-looking lines)."""
    ids, fence = [], None
    for line in text.splitlines():
        m = _FENCE_RE.match(line)
        if m:
            token = m.group(1)[0] * 3
            fence = None if fence and line.strip().startswith(fence) else (fence or token)
            continue
        if fence is not None:
            continue
        sm = _STEP_HEAD_RE.match(line)
        if sm:
            ids.append(sm.group(1))
    return ids


def build_progress_json():
    """Assembly chapters in build order: the progress key (`slug`, the same one
    progress.js uses), the step ids that have to be ticked for the chapter to
    count as finished, and the cumulative render to show once they are.

    Paths are relative to the site root, which is where docs/index.md sits."""
    chapters = []
    for path in _chapter_files():
        text = path.read_text(encoding="utf-8")
        number, title = _parse_header(text)
        if number is None:
            continue
        steps = _step_ids(text)
        if not steps:                      # Ch 15 / Ch 16 are reference pages
            continue
        render = CAD_DIR / f"ch-{number}-after.png"
        chapters.append({
            "number": number,
            "slug": path.stem.lower(),     # scripts/build_steps.py's chapter slug
            "title": title,
            "steps": steps,
            "image": (f"manual/assets/cad/{render.name}" if render.exists() else None),
        })
    if not chapters:
        raise SystemExit("build_printables.py: no assembly chapter carried a step heading")
    data = {"chapters": chapters}
    start = CAD_DIR / "ch-00-after.png"
    if start.exists():
        data["start"] = {"image": f"manual/assets/cad/{start.name}",
                         "title": "Before the first chapter"}
    return data


_SECTION_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
# | 1 | B00-P1 | 4.0 | black | day | #1 |
_RUN_ROW_RE = re.compile(
    r"^\|\s*(\d+)\s*\|\s*(B\d\d-P\d)\s*\|\s*([\d.]+)\s*\|\s*([A-Za-z]+)\s*\|"
    r"\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*$",
    re.MULTILINE,
)
# | B00-P1 | 52 | | #1 | 748 |
_LEDGER_ROW_RE = re.compile(
    r"^\|\s*(B\d\d-P\d)\s*\|\s*(\d+)\s*\|[^|]*\|\s*([^|]+?)\s*\|\s*(\d+)\s*\|\s*$",
    re.MULTILINE,
)
_SPOOL_HEAD_RE = re.compile(r"[#AV]\d+")   # #1-#3 black, A1 accent, V1 B11's PETG V0
# A batch chapter's gate is the bold one its **Prerequisites:** line names ("**Gate B passed**",
# "**Gate A**"); B11 names neither. The plate board shows it on the batch's first plate.
_PREREQ_RE = re.compile(r"^\*\*Prerequisites:\*\*(.*)$", re.MULTILINE)
_GATE_RE = re.compile(r"\*\*Gate ([AB])\b[^*]*\*\*")


def _readme_section(text, heading):
    """The body under a `## <heading>` up to the next `##`."""
    spans = [(m.start(), m.end(), m.group(1)) for m in _SECTION_RE.finditer(text)]
    for i, (start, end, title) in enumerate(spans):
        if title.strip().lower() == heading.lower():
            stop = spans[i + 1][0] if i + 1 < len(spans) else len(text)
            return text[end:stop]
    raise SystemExit(
        f"build_printables.py: {README.name} has no '## {heading}' section — "
        "the plate board reads its slot/spool/remaining columns from it"
    )


def _fail(problems):
    raise SystemExit(
        "build_printables.py: docs/manual/print/README.md no longer agrees with "
        "slicer/estimates.csv — " + "; ".join(problems)
    )


def _batch_gate(text):
    """'A', 'B' or None: the gate a batch chapter's Prerequisites line names in bold."""
    m = _PREREQ_RE.search(text)
    g = _GATE_RE.search(m.group(1)) if m else None
    return g.group(1) if g else None


def _milestones(plates):
    """plate id -> milestone text for the four moments the plate board celebrates (sweep
    G8-29), all derived from the run order: B00 off the bed (Gate A is next), the last
    accent-colour plate, the middle plate of the ASA run, and its last plate."""
    asa = [p for p in plates if p["run"] == "asa"]
    if not asa:
        return {}
    out = {}
    b00 = [p for p in asa if p["batch"] == "B00"]
    if b00:
        out[b00[-1]["id"]] = "B00 done: the first plate is off the bed. Gate A's cube is next."
    blue = [p for p in asa if p["colour"] == "blue"]
    if blue:
        out[blue[-1]["id"]] = "Blue day done: every accent part is printed."
    half = asa[(len(asa) + 1) // 2 - 1]
    out[half["id"]] = f"Halfway: plate {(len(asa) + 1) // 2} of {len(asa)}."
    out[asa[-1]["id"]] = f"Last ASA plate off the bed: all {len(asa)} plates of the run are done."
    return out


def build_plate_board_json():
    """The 22 plates of the ASA run in run order, then B11's, for docs/print/plate-board.md.

    Hours, grams and colour are the CSV's (rounded the same additive way as every
    other page); slot, spool and predicted remaining come from README.md's two
    hand-written tables. Everything that can be cross-checked is, because those
    tables are edited by hand after a re-slice and a silent drift is exactly what
    the board would hide."""
    estimates = _load_estimates()
    batches = _batch_files()
    text = README.read_text(encoding="utf-8")

    run = {}
    schedules = ["Run schedule"] + (["B11 run schedule"] if any(
        run_of(p) != "asa" for p in estimates) else [])
    ledgers = ["Spool ledger"] + (["B11 spool ledger"] if len(schedules) > 1 else [])
    for m in (m for sec in schedules for m in _RUN_ROW_RE.finditer(_readme_section(text, sec))):
        order, pid, hours, colour, slot, spool = m.groups()
        run[pid] = {"order": int(order), "hours": float(hours), "colour": colour,
                    "slot": slot, "spool": spool}
    ledger = {}
    for m in (m for sec in ledgers for m in _LEDGER_ROW_RE.finditer(_readme_section(text, sec))):
        pid, grams, spool, remaining = m.groups()
        ledger[pid] = {"grams": int(grams), "spool": spool.replace("*", "").strip(),
                       "remaining": int(remaining)}

    problems = []
    if set(run) != set(estimates):
        problems.append(f"run schedule parsed {sorted(set(run) ^ set(estimates))} "
                        "differently from the CSV")
    if set(ledger) != set(estimates):
        problems.append(f"spool ledger parsed {sorted(set(ledger) ^ set(estimates))} "
                        "differently from the CSV")
    if problems:
        _fail(problems)
    if sorted(r["order"] for r in run.values()) != list(range(1, len(run) + 1)):
        problems.append("the run schedule's # column is not 1..N")

    plates = []
    for pid in sorted(run, key=lambda p: run[p]["order"]):
        colour, _parts, hours, grams = estimates[pid]
        row, led = run[pid], ledger[pid]
        if row["hours"] != hours:
            problems.append(f"{pid}: run schedule says {row['hours']} h, CSV says {hours}")
        if row["colour"] != colour:
            problems.append(f"{pid}: run schedule says {row['colour']}, CSV says {colour}")
        if led["grams"] != grams:
            problems.append(f"{pid}: ledger says {led['grams']} g, CSV says {grams}")
        slot = "overnight" if hours >= OVERNIGHT_H else "day"
        run_key = run_of(pid)
        if not row["slot"].lower().startswith(slot):
            problems.append(f"{pid}: {hours} h is a {slot} plate, the run schedule "
                            f"calls it {row['slot']!r}")
        heads = [_SPOOL_HEAD_RE.search(s) for s in (row["spool"], led["spool"])]
        if not all(heads) or heads[0].group(0) != heads[1].group(0):
            problems.append(f"{pid}: run schedule spool {row['spool']!r} and ledger "
                            f"spool {led['spool']!r} are not the same spool")
        note = row["slot"][len(slot):].strip(" ()") if len(row["slot"]) > len(slot) else ""
        batch = pid[:3]
        if batch not in batches:
            problems.append(f"{pid}: no batch chapter for {batch}")
            continue
        path, title, batch_text = batches[batch]
        gate = _batch_gate(batch_text)
        if gate and not any(p["batch"] == batch for p in plates):
            note = " · ".join(n for n in (note, f"after Gate {gate}") if n)
        diagram = PLATE_DIAGRAMS / f"{pid}.png"
        if not diagram.exists():
            problems.append(f"{pid}: no sorting diagram at {diagram.relative_to(DOCS)}")
        plates.append({
            "id": pid,
            "batch": batch,
            "batch_title": title,
            "run": run_key,
            "hours": hours,
            "grams": grams,
            "colour": colour,
            "slot": slot,
            "note": note,
            "spool": row["spool"],
            "remaining": led["remaining"],
            # Relative to docs/print/plate-board.md's page URL (…/print/plate-board/).
            "diagram": f"../../manual/assets/plates/{pid}.png",
            "chapter": f"../../manual/steps/{path.stem.lower()}/",
        })
    if problems:
        _fail(problems)

    for pid, text in _milestones(plates).items():
        next(p for p in plates if p["id"] == pid)["milestone"] = text

    # One header line per run (sweep G8-24): the 22-plate ASA run and B11 are never summed.
    runs = []
    for p in plates:
        if not runs or runs[-1]["run"] != p["run"]:
            runs.append({"run": p["run"], "plates": 0, "hours": 0.0, "batches": []})
        r = runs[-1]
        r["plates"] += 1
        r["hours"] = round(r["hours"] + p["hours"], 1)
        if p["batch"] not in r["batches"]:
            r["batches"].append(p["batch"])
    for r in runs:
        r["label"] = (f"{r['plates']}-plate run" if r["run"] == "asa"
                      else " + ".join(r["batches"]))
        del r["batches"]

    return {
        "plates": plates,
        "runs": runs,
        "totals": {
            "plates": len(plates),
            "hours": round(sum(p["hours"] for p in plates), 1),
            "overnight": sum(1 for p in plates if p["slot"] == "overnight"),
            # the ASA run alone (22 plates, 157.0 h); B11 is the remainder
            "run_plates": sum(1 for p in plates if p["run"] == "asa"),
            "run_hours": round(sum(p["hours"] for p in plates if p["run"] == "asa"), 1),
        },
    }


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
    checklists = (build_checklists_markdown(chapters).rstrip("\n") + "\n\n"
                  '<div class="print-page-break"></div>\n\n'
                  + build_plate_review_markdown())
    (PRINT_DIR / "checklists.md").write_text(checklists, encoding="utf-8")
    (PRINT_DIR / "bin-labels.md").write_text(
        build_bin_labels_markdown(chapters), encoding="utf-8"
    )
    (PRINT_DIR / "plate-plans.md").write_text(
        build_plate_plans_markdown(), encoding="utf-8"
    )
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    for name, payload in (("build-progress.json", build_progress_json()),
                          ("plate-board.json", build_plate_board_json())):
        (DATA_DIR / name).write_text(
            json.dumps(payload, ensure_ascii=False, indent=1) + "\n", encoding="utf-8"
        )


if __name__ == "__main__":
    chapters = _load_chapters()
    print(build_checklists_markdown(chapters)[:2000])
    print("---")
    print(build_bin_labels_markdown(chapters)[:2000])
    print("---")
    print(build_plate_plans_markdown()[:2000])
    print("---")
    print(build_plate_review_markdown()[:2000])
    print("---")
    progress = build_progress_json()
    print(f"build-progress.json: {len(progress['chapters'])} chapters, "
          f"{sum(len(c['steps']) for c in progress['chapters'])} steps, "
          f"{sum(1 for c in progress['chapters'] if c['image'])} renders")
    board = build_plate_board_json()
    print(f"plate-board.json: {board['totals']}")
    print(json.dumps(board["plates"][:2], indent=1))
