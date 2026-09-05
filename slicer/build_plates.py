#!/usr/bin/env python3
"""Build one PrusaSlicer project per plate, slice it, and record the numbers.

For each of the 27 plates in `plates.py`:
  1. arrange the parts on the 250 x 220 bed (see geom.py - the CLI cannot),
  2. write the arranged meshes and merge them into `slicer/plates/<id>.3mf`,
  3. inject the print/filament/printer config and the per-object brim widths
     into that 3MF, so the committed file is self-sufficient,
  4. slice it with **no** `--load`, proving the 3MF carries its own config,
  5. read the time and grams out of the G-code footer,
  6. draw the plate preview into docs/manual/assets/plates/<id>.png,
  7. write slicer/estimates.csv.

    python3 slicer/build_plates.py                # all 27
    python3 slicer/build_plates.py B07-P2 B10-P1  # named plates only

Needs Pillow for the previews (`pip install -r slicer/requirements.txt`).
"""
from __future__ import annotations

import csv
import math
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

from geom import BED_X, BED_Y, Piece, bbox, convex_hull, pack, read_stl
from plates import MODEL_ESTIMATE, PLATES, brim_for, local_path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
STL = ROOT / "stl"
OUT_3MF = ROOT / "plates"
OUT_PNG = REPO / "docs" / "manual" / "assets" / "plates"
PRUSA = "/Applications/PrusaSlicer.app/Contents/MacOS/PrusaSlicer"
INI = {"black": ROOT / "voron-coreone-asa.ini",
       "orange": ROOT / "voron-accent-orange.ini"}

_hull_cache: dict[str, tuple[list[tuple[float, float]], tuple]] = {}


def hull_and_bbox(rel: str):
    if rel not in _hull_cache:
        tris = read_stl(STL / rel)
        _hull_cache[rel] = (convex_hull([(v[0], v[1]) for t in tris for v in t]),
                            bbox(tris))
    return _hull_cache[rel]


def source_stl(repo: str, path: str) -> str:
    """Local path for one source. The two Nevermore cartridges ship as 3MF;
    fetch_stls.py leaves them as-is and we slice from a converted STL."""
    rel = local_path(repo, path)
    if rel.endswith(".3mf"):
        stl = rel[:-4] + ".stl"
        if not (STL / stl).exists():
            run([PRUSA, "--export-stl", "-o", str(STL / stl), str(STL / rel)])
        return stl
    return rel


def run(cmd: list[str]) -> subprocess.CompletedProcess:
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(f"command failed ({p.returncode}): {' '.join(cmd)}\n"
                           f"{p.stdout[-2000:]}\n{p.stderr[-2000:]}")
    return p


# ------------------------------------------------------------- mesh writing

def write_transformed_stl(src: Path, dst: Path, rot_deg: float,
                          tx: float, ty: float, tz: float) -> None:
    """Rotate about Z, translate, write a binary STL."""
    tris = read_stl(src)
    r = math.radians(rot_deg)
    c, s = math.cos(r), math.sin(r)
    out = bytearray(b"\0" * 80)
    out += struct.pack("<I", len(tris))
    pack_tri = struct.Struct("<12fH").pack
    for t in tris:
        v = []
        for x, y, z in t:
            v += [x * c - y * s + tx, x * s + y * c + ty, z + tz]
        out += pack_tri(0.0, 0.0, 0.0, *v, 0)
    dst.write_bytes(bytes(out))


# ------------------------------------------------------------ 3MF surgery

def config_lines(ini: Path) -> list[str]:
    """The `--load` ini as the `; key = value` lines a 3MF config member holds."""
    lines = []
    for raw in ini.read_text().splitlines():
        raw = raw.strip()
        if not raw or raw.startswith("#") or "=" not in raw:
            continue
        lines.append("; " + raw)
    return lines


def inject_3mf(path: Path, ini: Path, per_object: dict[str, dict[str, str]],
               names: dict[str, str]) -> None:
    """Add Metadata/Slic3r_PE.config, per-object settings and clean object
    names to a 3MF exported by the CLI.

    The CLI's `--export-3mf` writes model geometry only - no
    `Metadata/Slic3r_PE.config` - so a project file straight from the CLI opens
    with whatever presets the reader happens to have selected. Injecting the
    config is what makes the committed 3MF the artefact R6 P1 asks for.

    `per_object` / `names` are keyed by the temp STL basename, which PrusaSlicer
    records as each object's `source_file`.
    """
    with zipfile.ZipFile(path) as z:
        members = {n: z.read(n) for n in z.namelist()}

    cfg = members.get("Metadata/Slic3r_PE_model.config", b"").decode("utf-8")
    blocks = cfg.split("<object ")
    rebuilt = [blocks[0]]
    for blk in blocks[1:]:
        m = re.search(r'key="source_file" value="([^"]+)"', blk)
        src = Path(m.group(1)).name if m else ""
        extra = ""
        if src in names:
            blk = re.sub(r'(<metadata type="object" key="name" value=")[^"]*(")',
                         lambda mo: mo.group(1) + names[src] + mo.group(2), blk, count=1)
        for k, v in per_object.get(src, {}).items():
            extra += f'  <metadata type="object" key="{k}" value="{v}"/>\n'
        if extra:
            blk = blk.replace("\n", "\n" + extra, 1)
        rebuilt.append(blk)
    members["Metadata/Slic3r_PE_model.config"] = "<object ".join(rebuilt).encode("utf-8")

    header = ("; generated by slicer/build_plates.py from "
              f"{ini.name} (PrusaSlicer 2.9.6 system presets + Voron overrides)")
    members["Metadata/Slic3r_PE.config"] = (
        "\n".join([header] + config_lines(ini)) + "\n").encode("utf-8")

    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name, data in members.items():
            z.writestr(name, data)


# ---------------------------------------------------------------- G-code

FOOTER = {
    "time": re.compile(r"^; estimated printing time \(normal mode\) = (.+)$", re.M),
    "used_g": re.compile(r"^; filament used \[g\] = ([\d.]+)$", re.M),
    "total_g": re.compile(r"^; total filament used \[g\] = ([\d.]+)$", re.M),
}


def parse_time(text: str) -> float:
    h = re.search(r"(\d+)h", text)
    m = re.search(r"(\d+)m", text)
    s = re.search(r"(\d+)s", text)
    d = re.search(r"(\d+)d", text)
    total = 0.0
    if d:
        total += int(d.group(1)) * 24
    if h:
        total += int(h.group(1))
    if m:
        total += int(m.group(1)) / 60
    if s:
        total += int(s.group(1)) / 3600
    return total


def read_footer(gcode: Path) -> tuple[float, float, str, dict[str, str]]:
    text = gcode.read_text(errors="replace")
    t = FOOTER["time"].search(text)
    g = FOOTER["total_g"].search(text) or FOOTER["used_g"].search(text)
    if not t or not g:
        raise RuntimeError(f"no time/filament footer in {gcode}")
    cfg = dict(re.findall(r"^; ([a-z_0-9]+) = (.*)$", text, re.M))
    return parse_time(t.group(1)), float(g.group(1)), t.group(1), cfg


# ----------------------------------------------------------------- driver

def build(plate_id: str) -> dict:
    spec = PLATES[plate_id]
    colour = spec["colour"]
    ini = INI[colour]

    pieces: list[Piece] = []
    for repo, path, qty in spec["parts"]:
        rel = source_stl(repo, path)
        hull, bb = hull_and_bbox(rel)
        base = Path(path).name
        for i in range(qty):
            nm = base if qty == 1 else f"{base}#{i + 1}"
            pieces.append(Piece(rel, nm, hull, brim_for(path), bb[2]))

    fits, overflow = pack(pieces)
    if not fits:
        raise SystemExit(
            f"PLATE {plate_id} DOES NOT FIT on {BED_X:.0f} x {BED_Y:.0f} mm.\n"
            "  overflowing parts:\n    " + "\n    ".join(overflow) +
            "\n  Nothing was written for this plate. Re-pack the plate in the plan "
            "(docs/voron-print-plan.md §3) rather than scaling anything down.")

    # belt-and-braces: the packer works on bounding boxes, so overlap is a bug
    for i, a in enumerate(pieces):
        ax0, ay0 = a.x, a.y
        aw, ah = a.size()
        for b in pieces[i + 1:]:
            bw, bh = b.size()
            if (ax0 < b.x + bw and b.x < ax0 + aw
                    and ay0 < b.y + bh and b.y < ay0 + ah):
                raise SystemExit(f"{plate_id}: {a.name} overlaps {b.name}")

    tmp = Path(tempfile.mkdtemp(prefix=f"plate-{plate_id}-"))
    try:
        inputs: list[str] = []
        per_object: dict[str, dict[str, str]] = {}
        names: dict[str, str] = {}
        for n, p in enumerate(pieces, 1):
            stem = f"{n:02d}_{Path(p.name.split('#')[0]).stem}"
            fn = f"{stem}.stl"
            x0, y0, _, _ = p.extent()
            _, _, zmin, _, _, _ = hull_and_bbox(p.key)[1]
            write_transformed_stl(STL / p.key, tmp / fn, p.rot,
                                  p.x - x0, p.y - y0, -zmin)
            inputs.append(str(tmp / fn))
            names[fn] = p.name
            if p.brim:
                per_object[fn] = {"brim_width": f"{p.brim:g}",
                                  "brim_type": "outer_only"}

        OUT_3MF.mkdir(parents=True, exist_ok=True)
        dst = OUT_3MF / f"{plate_id}.3mf"
        run([PRUSA, "--load", str(ini), "--merge", "--dont-arrange",
             "--export-3mf", "-o", str(dst), *inputs])
        inject_3mf(dst, ini, per_object, names)

        gcode = tmp / f"{plate_id}.gcode"
        # deliberately no --load: this proves the committed 3MF is self-sufficient
        run([PRUSA, "--dont-arrange", "--binary-gcode=0",
             "--export-gcode", "-o", str(gcode), str(dst)])
        hours, grams, raw_time, cfg = read_footer(gcode)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    for key, want in (("perimeters", "4"), ("bottom_solid_layers", "5"),
                      ("fill_density", "40%"), ("xy_size_compensation", "0"),
                      ("filament_shrinkage_compensation_xy", "0%"),
                      ("filament_shrinkage_compensation_z", "0%"),
                      ("seam_position", "rear"), ("support_material", "0")):
        if cfg.get(key) != want:
            raise SystemExit(f"{plate_id}: sliced with {key} = {cfg.get(key)!r}, "
                             f"expected {want!r} - the 3MF config did not take")

    brims = sorted({p.brim for p in pieces if p.brim})
    brim_note = ("brim: " + ", ".join(f"{b:g} mm on "
                 f"{len([p for p in pieces if p.brim == b])} part(s)" for b in brims)
                 ) if brims else "no brim on this plate"

    from render_plate import render
    render(plate_id, colour, pieces, hours, grams, brim_note,
           OUT_PNG / f"{plate_id}.png")

    prev_h, prev_g = MODEL_ESTIMATE[plate_id]
    return dict(plate=plate_id, batch=spec["batch"], colour=colour,
                parts=len(pieces), hours=hours, grams=grams,
                raw_time=raw_time, prev_hours=prev_h, prev_grams=prev_g,
                d_hours=hours - prev_h, d_grams=grams - prev_g,
                brim=(max(brims) if brims else 0.0),
                size_kb=round(dst.stat().st_size / 1024))


def main() -> int:
    wanted = sys.argv[1:] or list(PLATES)
    rows = []
    for pid in wanted:
        r = build(pid)
        rows.append(r)
        print(f"{r['plate']:8s} {r['parts']:2d} parts  {r['raw_time']:>12s}  "
              f"{r['grams']:6.1f} g   (was {r['prev_hours']:.1f} h / {r['prev_grams']} g, "
              f"{r['d_hours']:+.1f} h {r['d_grams']:+.1f} g)   {r['size_kb']} KB")

    if len(rows) == len(PLATES):
        csv_path = ROOT / "estimates.csv"
        with csv_path.open("w", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(["plate", "batch", "colour", "parts", "raw_time", "hours", "grams",
                        "prev_model_hours", "prev_model_grams",
                        "delta_hours", "delta_grams", "brim_mm", "size_kb"])
            for r in rows:
                w.writerow([r["plate"], r["batch"], r["colour"], r["parts"], r["raw_time"],
                            f"{r['hours']:.4f}", f"{r['grams']:.2f}",
                            f"{r['prev_hours']:.1f}", r["prev_grams"],
                            f"{r['d_hours']:+.2f}", f"{r['d_grams']:+.1f}",
                            f"{r['brim']:g}", r["size_kb"]])
            th = sum(r["hours"] for r in rows)
            tg = sum(r["grams"] for r in rows)
            ph = sum(r["prev_hours"] for r in rows)
            pg = sum(r["prev_grams"] for r in rows)
            w.writerow(["TOTAL", "", "", sum(r["parts"] for r in rows), "",
                        f"{th:.4f}", f"{tg:.2f}", f"{ph:.1f}", pg,
                        f"{th - ph:+.2f}", f"{tg - pg:+.1f}", "", ""])
        print(f"\nTOTAL {th:.1f} h / {tg:.0f} g   (model said {ph:.1f} h / {pg} g)")
        print(f"wrote {csv_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
