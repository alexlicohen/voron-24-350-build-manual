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

Both files are regenerated on every build — never hand-edit them. QR SVGs
are written to docs/print/assets/qr/.
"""

import os
import sys
import re
from pathlib import Path

try:
    import segno
except ImportError:  # pragma: no cover - degrade gracefully if not installed
    segno = None

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "slicer"))
import bins  # noqa: E402  (slicer/bins.py — the bin scheme)
from plates import PLATES  # noqa: E402  (slicer/plates.py — what is on each plate)
DOCS = REPO / "docs"
MANUAL = DOCS / "manual"
PRINT_DIR = DOCS / "print"
QR_DIR = PRINT_DIR / "assets" / "qr"

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


if __name__ == "__main__":
    chapters = _load_chapters()
    print(build_checklists_markdown(chapters)[:2000])
    print("---")
    print(build_bin_labels_markdown(chapters)[:2000])
