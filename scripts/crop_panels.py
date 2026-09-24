#!/usr/bin/env python3
"""Panel crops for shared manual/Stealthburner page images.

Wave 4 subtask 2A (`review/2026-09-23-sweep/WAVE4-PLAN.md` § 2). A step whose
Do text acts on one panel of a multi-panel PDF page gets a cropped, larger
image instead of the whole page at ~39% scale on the iPad column. The crop is
declared on the chapter's existing image line as a page-fraction box:

    ![Voron manual p.88](assets/manual-pages/manual-p088.png){ crop="0.12 0.14 0.62 0.72" }

This script does not read or write chapter markdown (that is subtask 2B/2F).
It only renders crop PNGs and checks them against crops markdown already
declares, via three modes:

    --sheet PAGE                     10%-gridded full-page overlay, for
                                      picking a box by eye. Written to
                                      --out-dir (default: the scratchpad).
    --render PAGE --box X0 Y0 X1 Y1  render + crop + quantise, written to
                                      docs/manual/assets/manual-crops/ (or
                                      --out-dir).
    --check                          scan docs/manual/*.md for declared
                                      `{ crop="..." }` boxes, report any
                                      whose crop PNG is missing (exit 1) and
                                      any crop PNG in manual-crops/ that no
                                      chapter declares (reported, exit 0).
                                      Needs no PDF — CI has neither source
                                      PDF (both gitignored).

PAGE is `pNNN` for a Voron manual page (1-indexed, matches
assets/manual-pages/manual-pNNN.png and page N of Voron2.4r2-manual.pdf) or
`sbNNN` for a Stealthburner manual page (assets/sb-pages/sb-pNNN.png,
Voron-Stealthburner-manual.pdf).

Determinism: the crop's output filename is `<PAGE>-<hash8>.png`, an 8-hex
digest of the page id and box alone (not of rendered pixels), so two workers
choosing the same box for the same page always agree on the filename without
coordinating — "content-addressed" in the plan's sense. Rendering is also
byte-deterministic for a fixed (page, box): pdftoppm and `magick -colors 64`
take no randomised input, so re-running `--render` with the same page and box
reproduces the same file bytes (verified by `--self-test`).

Requires on PATH: pdftoppm, magick (both Poppler/ImageMagick, already used
elsewhere in this repo's asset pipeline). `--check` needs neither.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ASSETS = REPO_ROOT / "docs" / "manual" / "assets"
MANUAL_PDF = ASSETS / "Voron2.4r2-manual.pdf"
SB_PDF = ASSETS / "Voron-Stealthburner-manual.pdf"
MANUAL_PAGES_DIR = ASSETS / "manual-pages"
SB_PAGES_DIR = ASSETS / "sb-pages"
CROPS_DIR = ASSETS / "manual-crops"
CHAPTERS_DIR = REPO_ROOT / "docs" / "manual"

RENDER_DPI = 300
MAX_LONG_EDGE = 1200
QUANTISE_COLORS = 64

PAGE_RE = re.compile(r"^(sb|p)(\d{3})$")

# Declared crop on an existing image line, e.g.:
#   ![Voron manual p.88](assets/manual-pages/manual-p088.png){ crop="0.12 0.14 0.62 0.72" }
#   ![SB manual p.5](assets/sb-pages/sb-p005.png){ crop="0.0 0.0 0.5 0.5" }
CROP_ATTR_RE = re.compile(
    r"!\[[^\]]*\]\(assets/(?:manual-pages/manual-p(\d{3})\.png|sb-pages/sb-p(\d{3})\.png)\)"
    r"\{[^}]*\bcrop="
    r"[\"']([0-9.]+)\s+([0-9.]+)\s+([0-9.]+)\s+([0-9.]+)[\"'][^}]*\}"
)


class CropError(Exception):
    pass


def _page_info(page_id: str) -> tuple[str, Path, Path]:
    """(kind, source_pdf, source_png) for a page id like 'p088' or 'sb005'."""
    m = PAGE_RE.match(page_id)
    if not m:
        raise CropError(f"page id {page_id!r} must look like p088 or sb005")
    kind, num = m.group(1), m.group(2)
    if kind == "p":
        return "manual", MANUAL_PDF, MANUAL_PAGES_DIR / f"manual-p{num}.png"
    return "sb", SB_PDF, SB_PAGES_DIR / f"sb-p{num}.png"


def _page_number(page_id: str) -> int:
    return int(PAGE_RE.match(page_id).group(2))


def _require_tool(name: str) -> None:
    if shutil.which(name) is None:
        raise CropError(f"{name!r} not found on PATH (required for --sheet/--render)")


def crop_hash(page_id: str, box: tuple[float, float, float, float]) -> str:
    x0, y0, x1, y1 = box
    key = f"{page_id}:{x0:.4f},{y0:.4f},{x1:.4f},{y1:.4f}"
    return hashlib.sha256(key.encode("utf-8")).hexdigest()[:8]


def crop_filename(page_id: str, box: tuple[float, float, float, float]) -> str:
    return f"{page_id}-{crop_hash(page_id, box)}.png"


def _validate_box(box: tuple[float, float, float, float]) -> None:
    x0, y0, x1, y1 = box
    for v in box:
        if not (0.0 <= v <= 1.0):
            raise CropError(f"box values must be in [0, 1], got {box}")
    if x1 <= x0 or y1 <= y0:
        raise CropError(f"box must have x1>x0 and y1>y0, got {box}")


def _render_full_page(page_id: str, dpi: int, work_dir: Path) -> Path:
    """pdftoppm the single page at `dpi` into work_dir, return the PNG path."""
    kind, pdf, _png = _page_info(page_id)
    if not pdf.exists():
        raise CropError(
            f"source PDF missing: {pdf} (gitignored, local-only; --render/--sheet "
            "need it, --check does not)"
        )
    _require_tool("pdftoppm")
    n = _page_number(page_id)
    prefix = work_dir / f"raw-{page_id}"
    subprocess.run(
        ["pdftoppm", "-f", str(n), "-l", str(n), "-r", str(dpi), "-png", str(pdf), str(prefix)],
        check=True, capture_output=True,
    )
    matches = sorted(work_dir.glob(f"raw-{page_id}-*.png"))
    if not matches:
        raise CropError(f"pdftoppm produced no page for {page_id} (page {n} out of range?)")
    return matches[-1]


def cmd_sheet(page_id: str, out_dir: Path, dpi: int = 150) -> Path:
    """Render the full page with a 10% grid overlay, for picking a crop box."""
    from PIL import Image, ImageDraw

    with tempfile.TemporaryDirectory() as tmp:
        raw = _render_full_page(page_id, dpi, Path(tmp))
        im = Image.open(raw).convert("RGB")
        draw = ImageDraw.Draw(im)
        w, h = im.size
        for i in range(1, 10):
            x = round(w * i / 10)
            y = round(h * i / 10)
            draw.line([(x, 0), (x, h)], fill=(255, 0, 0), width=1)
            draw.line([(0, y), (w, y)], fill=(255, 0, 0), width=1)
        for i in range(10):
            for j in range(10):
                label = f"{i/10:.1f},{j/10:.1f}"
                draw.text((round(w * i / 10) + 3, round(h * j / 10) + 2), label, fill=(255, 0, 0))
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"sheet-{page_id}.png"
        im.save(out_path)
        return out_path


def cmd_render(page_id: str, box: tuple[float, float, float, float], out_dir: Path) -> Path:
    """Render `page_id` at 300 dpi, crop to `box` (page fractions), quantise,
    write the content-addressed PNG. Returns the written path."""
    from PIL import Image

    _page_info(page_id)  # validates page_id, source files
    _validate_box(box)
    _require_tool("magick")

    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / crop_filename(page_id, box)

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        raw = _render_full_page(page_id, RENDER_DPI, tmp_path)
        im = Image.open(raw).convert("RGB")
        w, h = im.size
        x0, y0, x1, y1 = box
        left, top, right, bottom = round(w * x0), round(h * y0), round(w * x1), round(h * y1)
        cropped = im.crop((left, top, right, bottom))

        long_edge = max(cropped.size)
        if long_edge > MAX_LONG_EDGE:
            scale = MAX_LONG_EDGE / long_edge
            new_size = (round(cropped.width * scale), round(cropped.height * scale))
            cropped = cropped.resize(new_size, Image.LANCZOS)

        pre_quant = tmp_path / "pre-quant.png"
        cropped.save(pre_quant)

        # -strip + exclude-chunks=date,time: magick otherwise stamps a tIME
        # chunk (current wall-clock) into every PNG, which would make the
        # "same box -> same bytes" determinism promise false.
        subprocess.run(
            ["magick", str(pre_quant), "-colors", str(QUANTISE_COLORS),
             "-strip", "-define", "png:exclude-chunks=date,time", str(dest)],
            check=True, capture_output=True,
        )
    return dest


def _declared_crops() -> dict[str, tuple[str, tuple[float, float, float, float]]]:
    """{expected_filename: (chapter_path, page_id_and_box)} for every `{ crop=… }`
    attr found on a manual-pages/sb-pages image line in docs/manual/*.md."""
    declared: dict[str, tuple[str, tuple[float, float, float, float]]] = {}
    if not CHAPTERS_DIR.exists():
        return declared
    for md in sorted(CHAPTERS_DIR.glob("*.md")):
        text = md.read_text(encoding="utf-8")
        for m in CROP_ATTR_RE.finditer(text):
            manual_num, sb_num, x0, y0, x1, y1 = m.groups()
            page_id = f"p{manual_num}" if manual_num else f"sb{sb_num}"
            box = (float(x0), float(y0), float(x1), float(y1))
            fname = crop_filename(page_id, box)
            try:
                chapter = str(md.relative_to(REPO_ROOT))
            except ValueError:
                chapter = str(md)
            declared[fname] = (chapter, page_id)
    return declared


def cmd_check() -> int:
    """No PDF required. Returns the process exit code."""
    declared = _declared_crops()
    existing = {p.name for p in CROPS_DIR.glob("*.png")} if CROPS_DIR.exists() else set()

    missing = sorted(fname for fname in declared if fname not in existing)
    orphaned = sorted(existing - set(declared))

    print(f"declared crops: {len(declared)}  present: {len(existing)}")
    if missing:
        print(f"MISSING ({len(missing)}) — declared in a chapter but no PNG in manual-crops/:")
        for fname in missing:
            chapter, page_id = declared[fname]
            print(f"  {fname}  <- {chapter} ({page_id})")
    else:
        print("missing: none")
    if orphaned:
        print(f"orphaned ({len(orphaned)}) — in manual-crops/ but no chapter declares them:")
        for fname in orphaned:
            print(f"  {fname}")
    else:
        print("orphaned: none")

    return 1 if missing else 0


def _parse_box(values: list[str]) -> tuple[float, float, float, float]:
    if len(values) != 4:
        raise CropError("--box needs exactly 4 numbers: x0 y0 x1 y1")
    return tuple(float(v) for v in values)  # type: ignore[return-value]


def cmd_self_test(out_dir: Path) -> int:
    """Render the same (page, box) twice and confirm byte-identical output,
    for both a manual page and a Stealthburner page — the smoke test the
    plan's acceptance criteria ask for."""
    cases = [
        ("p088", (0.10, 0.10, 0.55, 0.55)),
        ("sb005", (0.05, 0.05, 0.50, 0.50)),
    ]
    ok = True
    for page_id, box in cases:
        try:
            first = cmd_render(page_id, box, out_dir)
            first_bytes = first.read_bytes()
            first.unlink()
            second = cmd_render(page_id, box, out_dir)
            second_bytes = second.read_bytes()
        except CropError as exc:
            print(f"FAIL {page_id} {box}: {exc}")
            ok = False
            continue
        same = first_bytes == second_bytes
        print(f"{'PASS' if same else 'FAIL'} {page_id} {box} -> {second.name} "
              f"({len(second_bytes)} bytes, {'identical' if same else 'DIFFERED'} on re-render)")
        ok = ok and same
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sheet", metavar="PAGE", help="e.g. p088 or sb005")
    ap.add_argument("--render", metavar="PAGE", help="e.g. p088 or sb005")
    ap.add_argument("--box", nargs=4, metavar=("X0", "Y0", "X1", "Y1"), help="page-fraction crop box, required with --render")
    ap.add_argument("--check", action="store_true", help="validate declared crops vs manual-crops/, no PDF needed")
    ap.add_argument("--self-test", action="store_true", help="two-crop determinism smoke test (p088 + one SB page)")
    ap.add_argument("--out-dir", type=Path, default=None,
                     help="override output dir (default: manual-crops/ for --render, scratchpad for --sheet)")
    ap.add_argument("--dpi", type=int, default=None, help="override sheet dpi (default 150) or render dpi (default 300)")
    args = ap.parse_args(argv)

    modes = [bool(args.sheet), bool(args.render), args.check, args.self_test]
    if sum(modes) != 1:
        ap.error("pass exactly one of --sheet, --render, --check, --self-test")

    try:
        if args.check:
            return cmd_check()

        if args.self_test:
            out_dir = args.out_dir or CROPS_DIR
            return cmd_self_test(out_dir)

        if args.sheet:
            out_dir = args.out_dir or Path(tempfile.gettempdir())
            dpi = args.dpi or 150
            path = cmd_sheet(args.sheet, out_dir, dpi)
            print(path)
            return 0

        if args.render:
            if not args.box:
                ap.error("--render needs --box X0 Y0 X1 Y1")
            box = _parse_box(args.box)
            out_dir = args.out_dir or CROPS_DIR
            path = cmd_render(args.render, box, out_dir)
            print(path)
            return 0

    except CropError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    return 2  # unreachable


if __name__ == "__main__":
    raise SystemExit(main())
