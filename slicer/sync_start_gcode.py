#!/usr/bin/env python3
"""Force one config key in the committed plate 3MFs to match the ini bundles.

Why this exists: a PrusaSlicer project carries a full `Metadata/Slic3r_PE.config`,
and opening one *overrides the reader's selected presets*. The 22 plates were
written before the cold-probe start G-code existed, so every one of them shipped
the stock CORE One start (`M109 R{...170}` waits and `G29 P9`) and would push it
back over Alex's `coldstart` printer preset on open, re-heating the nozzle during
probing. `build_plates.py --from-3mf` does not help: it re-slices the committed
3MF as it is and never re-injects the config.

So this patches the key in place. It rewrites *only* the one `; key = value` line
inside `Metadata/Slic3r_PE.config`; every other zip member - `3D/3dmodel.model`
(the GUI-arranged object transforms, the QC authority), `Metadata/Slic3r_PE_model.config`
(names, per-object brim), thumbnails - is copied through byte for byte. Five of the
plates were re-saved from the GUI and hold PrusaSlicer's own 377-line config rather
than the 263-line one build_plates.py injects; a blanket regeneration from the ini
would strip the keys the GUI added, which is why this is a single-line edit.

    python3 slicer/sync_start_gcode.py            # all plates, key `start_gcode`
    python3 slicer/sync_start_gcode.py --check    # report only, change nothing
    python3 slicer/sync_start_gcode.py --key end_gcode B03-P1
    python3 slicer/sync_start_gcode.py --key filament_settings_id --key filament_colour \
        B02-P1 B02-P2 B02-P3            # --key repeats; each value comes from the ini
    python3 slicer/sync_start_gcode.py --key filament_colour --value "#1F4E9C" B02-P1

The value comes from the matching ini (`voron-coreone-asa.ini` for black plates,
`voron-accent-blue.ini` for the blue accent plates), so the inis stay the single source of truth.
Re-run `python3 slicer/build_plates.py --from-3mf` afterwards to refresh the G-code
and estimates.csv.
"""
from __future__ import annotations

import shutil
import sys
import zipfile
from pathlib import Path

from plates import PLATES

ROOT = Path(__file__).resolve().parent
PLATE_DIR = ROOT / "plates"
CONFIG_MEMBER = "Metadata/Slic3r_PE.config"
INI = {"black": ROOT / "voron-coreone-asa.ini",
       "blue": ROOT / "voron-accent-blue.ini"}


def ini_value(ini: Path, key: str) -> str:
    """The raw (single-line, `\\n`-escaped) value of `key` in an ini bundle."""
    hits = [ln.split(" = ", 1)[1] for ln in ini.read_text().splitlines()
            if ln.startswith(key + " = ")]
    if len(hits) != 1:
        raise SystemExit(f"{ini.name}: expected exactly one `{key} = `, found {len(hits)}")
    return hits[0]


def patch(path: Path, key: str, value: str, check: bool) -> bool:
    """Return True if the member needed the change. Writes unless `check`."""
    with zipfile.ZipFile(path) as z:
        infos = z.infolist()
        members = [(i, z.read(i.filename)) for i in infos]

    out = []
    changed = False
    for info, data in members:
        if info.filename == CONFIG_MEMBER:
            lines = data.decode("utf-8").split("\n")
            hits = [n for n, ln in enumerate(lines) if ln.startswith(f"; {key} = ")]
            if len(hits) != 1:
                raise SystemExit(f"{path.name}: expected one `; {key} = ` line, found {len(hits)}")
            want = f"; {key} = {value}"
            if lines[hits[0]] != want:
                lines[hits[0]] = want
                changed = True
            data = "\n".join(lines).encode("utf-8")
        out.append((info, data))

    if changed and not check:
        tmp = path.with_suffix(".3mf.tmp")
        with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
            for info, data in out:
                # keep the member's own name, order and mtime; only the bytes may differ
                new = zipfile.ZipInfo(info.filename, date_time=info.date_time)
                new.compress_type = zipfile.ZIP_DEFLATED
                new.external_attr = info.external_attr
                # ZipInfo carries its own level and would otherwise ignore the
                # ZipFile's compresslevel=9, inflating every plate by ~6 %
                new._compresslevel = 9
                z.writestr(new, data)
        shutil.move(tmp, path)
    return changed


def main() -> int:
    args = sys.argv[1:]
    check = "--check" in args
    keys: list[str] = []
    override: str | None = None
    while "--key" in args:
        i = args.index("--key")
        keys.append(args[i + 1])
        args = args[:i] + args[i + 2:]
    if "--value" in args:
        i = args.index("--value")
        override = args[i + 1]
        args = args[:i] + args[i + 2:]
    keys = keys or ["start_gcode"]
    if override is not None and len(keys) != 1:
        raise SystemExit("--value takes exactly one --key")
    wanted = [a for a in args if not a.startswith("--")] or list(PLATES)

    n = 0
    for pid in wanted:
        path = PLATE_DIR / f"{pid}.3mf"
        if not path.exists():
            raise SystemExit(f"{pid}: {path} does not exist")
        for key in keys:
            value = override if override is not None else \
                ini_value(INI[PLATES[pid]["colour"]], key)
            if patch(path, key, value, check):
                n += 1
                print(f"{pid:8s} {key} {'differs' if check else 'updated'}")
            else:
                print(f"{pid:8s} {key} already current")
    verb = "would change" if check else "changed"
    print(f"\n{verb} {n} of {len(wanted) * len(keys)} plate-key(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
