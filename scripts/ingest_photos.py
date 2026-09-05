#!/usr/bin/env python3
"""Ingest bench photos from the iPad-to-Mac drop folder into the manual.

Workflow (docs/manual/CONVENTIONS.md, "Bench photos"): Alex photographs a
step at the bench; the photo lands via iCloud Photos/AirDrop in a drop
folder on the Mac; this script resizes it, strips EXIF (no GPS), files it
under docs/manual/assets/photos/<chapter>/, and inserts an image line into
the chapter markdown right after the step's existing image line(s) — so the
CAD render/manual page and the real photo sit together.

Step id resolution, per file:
  1. Filename encodes it: `NN.M[-n].jpg` (e.g. `10.58-2.jpg`, `00a.5.heic`).
  2. `--step NN.M` on the command line, applied to every file in this run.
  3. A sidecar note file with the same stem (`IMG_1234.jpg` + `IMG_1234.txt`):
     first line is the step id (`10.58` or `10.58-2`); an optional following
     line `caption: <text>` is written to that chapter's captions.yml.

Idempotent: a successfully ingested source is moved into `<drop>/.ingested/`
so re-running the command is a no-op for it, and a destination image that
already exists on disk is never overwritten by an auto-numbered file. Pass
--dry-run to see the plan without touching anything.

Usage:
  python3 scripts/ingest_photos.py [--drop DIR] [--step NN.M] [--dry-run]
                                    [--chapter-root DIR] [--keep]

--chapter-root overrides docs/manual (default) — used by tests to point at a
throwaway copy of a chapter tree instead of the real manual.
"""

import argparse
import os
import re
import shutil
import sys
from pathlib import Path

try:
    from PIL import Image, ImageOps
except ImportError:
    sys.exit(
        "Pillow is required: pip install -r requirements-photos.txt "
        "(from the repo root)"
    )

try:
    import pillow_heif

    pillow_heif.register_heif_opener()
except ImportError:
    pillow_heif = None  # HEIC support is optional; .jpg/.png always work.

REPO = Path(__file__).resolve().parent.parent
DEFAULT_CHAPTER_ROOT = REPO / "docs" / "manual"
DEFAULT_DROP = Path.home() / "Pictures" / "voron-drop"
MAX_DIM = 1600
JPEG_QUALITY = 85
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".heic", ".heif"}
_EXCLUDED_CHAPTER_FILES = {"00-index.md", "00-tonight.md", "CONVENTIONS.md"}

STEP_TOKEN_RE = re.compile(r"^([A-Za-z]?\d+\.\d+)(?:-(\d+))?$")
STEP_HEADING_RE = re.compile(r"^###\s*Step\s+([A-Za-z]?\d+\.\d+)\b")
IMAGE_LINE_RE = re.compile(r"^\s*!\[.*\]\(.*\)\s*$")
NO_IMAGE_RE = re.compile(r"^\s*\*?\(no image[^)]*\)\*?\s*$", re.IGNORECASE)
DEST_NAME_RE = re.compile(r"^([A-Za-z]?\d+\.\d+)-(\d+)\.jpg$")


def chapter_files(chapter_root):
    files = list(chapter_root.glob("*.md")) + list((chapter_root / "print").glob("*.md"))
    return [f for f in files if f.name not in _EXCLUDED_CHAPTER_FILES]


def build_step_index(chapter_root):
    """step_id -> chapter markdown file that defines '### Step <step_id>'."""
    index = {}
    for f in chapter_files(chapter_root):
        text = f.read_text(encoding="utf-8")
        for line in text.splitlines():
            m = STEP_HEADING_RE.match(line)
            if not m:
                continue
            index.setdefault(m.group(1), f)
    return index


def resolve_step_token(image_path, cli_step):
    """Return (step_id, forced_seq_or_None) for one source image."""
    if cli_step:
        return cli_step, None
    m = STEP_TOKEN_RE.match(image_path.stem)
    if m:
        return m.group(1), (int(m.group(2)) if m.group(2) else None)
    sidecar = image_path.with_suffix(".txt")
    if sidecar.exists():
        lines = sidecar.read_text(encoding="utf-8").splitlines()
        if lines:
            m = STEP_TOKEN_RE.match(lines[0].strip())
            if m:
                return m.group(1), (int(m.group(2)) if m.group(2) else None)
    return None, None


def read_sidecar_caption(image_path):
    sidecar = image_path.with_suffix(".txt")
    if not sidecar.exists():
        return None
    for line in sidecar.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.lower().startswith("caption:"):
            return line.split(":", 1)[1].strip()
    return None


def next_sequence(dest_dir, step_id):
    if not dest_dir.exists():
        return 1
    best = 0
    for f in dest_dir.iterdir():
        m = DEST_NAME_RE.match(f.name)
        if m and m.group(1) == step_id:
            best = max(best, int(m.group(2)))
    return best + 1


def process_image(src_path, dest_path):
    img = Image.open(src_path)
    img = ImageOps.exif_transpose(img)  # bake in rotation before EXIF is dropped
    if img.mode not in ("RGB", "L"):
        img = img.convert("RGB")
    w, h = img.size
    scale = min(1.0, MAX_DIM / max(w, h))
    if scale < 1.0:
        img = img.resize((max(1, round(w * scale)), max(1, round(h * scale))), Image.LANCZOS)
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(dest_path, "JPEG", quality=JPEG_QUALITY)  # no exif= kwarg -> EXIF/GPS stripped


def image_markdown_line(step_id, rel_path):
    return f"![Bench photo — Step {step_id}]({rel_path})"


def insert_image_line(chapter_file, step_id, new_line, dry_run):
    """Insert new_line right after the step's existing image line(s).
    Returns 'inserted', 'already-present', or 'no-step-block-found'."""
    text = chapter_file.read_text(encoding="utf-8")
    lines = text.split("\n")
    heading_idx = None
    for i, line in enumerate(lines):
        m = STEP_HEADING_RE.match(line)
        if m and m.group(1) == step_id:
            heading_idx = i
            break
    if heading_idx is None:
        return "no-step-block-found"

    i = heading_idx + 1
    while i < len(lines) and lines[i].strip() == "":
        i += 1
    if i < len(lines) and (IMAGE_LINE_RE.match(lines[i]) or NO_IMAGE_RE.match(lines[i])):
        if NO_IMAGE_RE.match(lines[i]):
            i += 1
        else:
            while i < len(lines) and IMAGE_LINE_RE.match(lines[i]):
                i += 1
    block_end = i  # insert here, before the blank line that follows

    if any(lines[j].strip() == new_line.strip() for j in range(heading_idx, block_end)):
        return "already-present"

    if dry_run:
        return "inserted"

    lines.insert(block_end, new_line)
    chapter_file.write_text("\n".join(lines), encoding="utf-8")
    return "inserted"


def write_caption(chapter_root, chapter_slug, filename, caption):
    try:
        import yaml
    except ImportError:
        print(f"  (skipping caption — pyyaml not installed: {caption!r})")
        return
    captions_path = chapter_root / "assets" / "photos" / chapter_slug / "captions.yml"
    data = {}
    if captions_path.exists():
        data = yaml.safe_load(captions_path.read_text(encoding="utf-8")) or {}
    data[filename] = caption
    captions_path.parent.mkdir(parents=True, exist_ok=True)
    captions_path.write_text(yaml.dump(data, sort_keys=True, allow_unicode=True), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--drop", type=Path, default=DEFAULT_DROP, help="drop folder (default: ~/Pictures/voron-drop)")
    ap.add_argument("--step", help="apply this step id (e.g. 10.58) to every image in this run")
    ap.add_argument("--chapter-root", type=Path, default=DEFAULT_CHAPTER_ROOT, help="manual root (default: docs/manual)")
    ap.add_argument("--dry-run", action="store_true", help="print the plan; touch nothing")
    ap.add_argument("--keep", action="store_true", help="don't move ingested sources into <drop>/.ingested/")
    args = ap.parse_args()

    drop = args.drop.expanduser()
    drop.mkdir(parents=True, exist_ok=True)
    chapter_root = args.chapter_root
    photos_root = chapter_root / "assets" / "photos"

    sources = sorted(
        p for p in drop.iterdir()
        if p.is_file() and p.suffix.lower() in IMAGE_EXTS
    )
    if not sources:
        print(f"No images in {drop}")
        return 0

    step_index = build_step_index(chapter_root)
    ingested_dir = drop / ".ingested"
    rc = 0

    for src in sources:
        step_id, forced_seq = resolve_step_token(src, args.step)
        if not step_id:
            print(f"SKIP {src.name}: no step id in filename, --step, or sidecar note")
            rc = 1
            continue
        chapter_file = step_index.get(step_id)
        if not chapter_file:
            print(f"SKIP {src.name}: no 'Step {step_id}' heading found under {chapter_root}")
            rc = 1
            continue
        chapter_slug = chapter_file.stem
        dest_dir = photos_root / chapter_slug
        seq = forced_seq or next_sequence(dest_dir, step_id)
        dest_name = f"{step_id}-{seq}.jpg"
        dest_path = dest_dir / dest_name

        if dest_path.exists():
            print(f"SKIP {src.name}: {dest_path.relative_to(chapter_root.parent)} already exists (idempotent)")
            continue

        rel_path = Path(os.path.relpath(dest_path, chapter_file.parent))
        new_line = image_markdown_line(step_id, rel_path.as_posix())

        caption = read_sidecar_caption(src)

        print(f"{src.name} -> {dest_path.relative_to(chapter_root.parent)}  ({chapter_file.relative_to(chapter_root.parent)}: {new_line})")

        if args.dry_run:
            continue

        process_image(src, dest_path)
        result = insert_image_line(chapter_file, step_id, new_line, dry_run=False)
        if result == "no-step-block-found":
            print(f"  WARNING: could not find 'Step {step_id}' image block to insert into")
            rc = 1
        elif result == "already-present":
            print("  (markdown already had this line)")
        if caption:
            write_caption(chapter_root, chapter_slug, dest_name, caption)

        if not args.keep:
            ingested_dir.mkdir(exist_ok=True)
            shutil.move(str(src), str(ingested_dir / src.name))
            sidecar = src.with_suffix(".txt")
            if sidecar.exists():
                shutil.move(str(sidecar), str(ingested_dir / sidecar.name))

    return rc


if __name__ == "__main__":
    sys.exit(main())
