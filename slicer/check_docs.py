#!/usr/bin/env python3
"""Verify the manual's printed numbers still match slicer/estimates.csv.

The plate hours and grams appear in five places (the batch chapters, the plan's
§3 headers, §4, §9 and print/README.md). This checks all of them against the
one file the slicer wrote, so a re-slice cannot silently leave a stale number at
the bench. It also checks the bin scheme (slicer/bins.py) against the batch
chapters' Printed-parts `Bin` column and *Sort into bins* steps, print/README.md
§ Bins, and the `bin` column of docs/manual/assets/parts/MANIFEST.csv.

    python3 slicer/check_docs.py        # exits non-zero on any mismatch

Rounding is **additive**: plate values are rounded half-up for display, a batch
is the sum of its displayed plates, and the total is the sum of the displayed
batches. Every number in the manual is therefore the sum of the numbers under
it - which matters more at a bench than the last 0.2 h of precision. The exact
values stay in estimates.csv.
"""
from __future__ import annotations

import collections
import csv
import re
import sys
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import bins  # noqa: E402
from plates import PLATES  # noqa: E402
REPO = ROOT.parent
DOCS = REPO / "docs"
PRINT = DOCS / "manual" / "print"


def r1(x) -> float:
    return float(Decimal(str(x)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))


def r0(x) -> int:
    return int(Decimal(str(x)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def load():
    rows = [r for r in csv.DictReader((ROOT / "estimates.csv").open())
            if r["plate"] != "TOTAL"]
    plate = {r["plate"]: (r1(r["hours"]), r0(r["grams"]), r["batch"], r["colour"])
             for r in rows}
    batch = collections.OrderedDict()
    for pid, (h, g, b, c) in plate.items():
        d = batch.setdefault(b, {"plates": 0, "h": 0.0, "black": 0, "orange": 0})
        d["plates"] += 1
        d["h"] = round(d["h"] + h, 1)
        d[c] += g
    return plate, batch


CHAPTER = {
    "B00": "B00-calibration-and-jigs", "B01": "B01-z-drive-assemblies",
    "B02": "B02-accent-parts-orange", "B03": "B03-ab-drive-units-and-front-idlers",
    "B04": "B04-xy-joints-and-x-carriage", "B05": "B05-z-joints-and-z-chain",
    "B06": "B06-toolhead-sb-cw2-klicky", "B07": "B07-electronics-bay-and-lighting",
    "B08": "B08-skirts-and-front-modules", "B09": "B09-panels-filtration-spool",
    "B10": "B10-clicky-clack-door",
}


def _batch_bins() -> dict[str, dict[str, set[str]]]:
    """batch -> stl -> bins its copies go to, per slicer/bins.py."""
    out: dict[str, dict[str, set[str]]] = {}
    for pid, spec in PLATES.items():
        for _r, path, qty in spec["parts"]:
            stl = path.rsplit("/", 1)[-1]
            out.setdefault(spec["batch"], {}).setdefault(stl, set()).update(
                bins.copies_bins(pid, stl, qty))
    return out


def check_bins(readme: str) -> list[str]:
    bad: list[str] = []
    sources = [p.rsplit("/", 1)[-1] for pl in PLATES.values() for _r, p, _q in pl["parts"]]
    bad += [f"bins.py: {b}" for b in bins.check(sources)]
    expected = _batch_bins()
    for bid, stem in CHAPTER.items():
        text = (PRINT / f"{stem}.md").read_text()
        # Printed-parts table: Bin column present and each row's bins match
        tbl = re.search(r"^\| STL \| Repo path \| Qty \| Colour \| g ea \| Bin \|\n\|[-:| ]+\n((?:\|.*\n)+)",
                        text, re.M)
        if not tbl:
            bad.append(f"{stem}.md: Printed-parts table has no Bin column")
        else:
            for row in tbl.group(1).splitlines():
                m = re.search(r"`([^`]+\.(?:stl|3mf|STL))`", row)
                if not m or m.group(1) not in expected[bid]:
                    continue
                cell = row.strip().strip("|").split("|")[-1]
                want = expected[bid][m.group(1)]
                got = set(re.findall(r"\b(\d\d-[A-Za-z0-9-]+|spare-alt)\b", cell.replace("02-Z0–Z3", "02-Z0 02-Z1 02-Z2 02-Z3")))
                if got != want:
                    bad.append(f"{stem}.md: Bin cell for {m.group(1)} says {sorted(got)}, bins.py says {sorted(want)}")
        # Sort step: every bin the batch feeds is named, nothing else
        sm = re.search(r"^## Step B\d\d\.\d+ — Sort into bins\n(.*?)(?=^---$|^## )", text, re.M | re.S)
        if not sm:
            bad.append(f"{stem}.md: no 'Sort into bins' step")
        else:
            named = set(re.findall(r"\| \*\*([^*]+)\*\* — ", sm.group(1)))
            want = {b for s_ in expected[bid].values() for b in s_}
            if named != want:
                bad.append(f"{stem}.md: Sort step tables name {sorted(named)}, bins.py says {sorted(want)}")
    # README § Bins: one row per bin
    for b in bins.BINS:
        if not re.search(rf"^\| \*\*{re.escape(b)}\*\* \|", readme, re.M):
            bad.append(f"print/README § Bins: no row for {b}")
    # manifest column
    manifest = DOCS / "manual" / "assets" / "parts" / "MANIFEST.csv"
    rows = list(csv.DictReader(manifest.open()))
    if rows and "bin" not in rows[0]:
        bad.append("MANIFEST.csv: no `bin` column (run scripts/render_plate_bins.py --write-manifest)")
    else:
        for r in rows:
            want = bins.manifest_value(r["stl"]) if r["stl"] in bins.ASSIGN else ""
            if r.get("bin", "") != want:
                bad.append(f"MANIFEST.csv: {r['stl']} bin {r.get('bin')!r}, bins.py says {want!r}")
    return bad


DIAGRAMS = DOCS / "manual" / "assets" / "diagrams"


def check_index_and_timeline(batch, th) -> list[str]:
    """The numbers that live outside the plan/README pair: 00-index.md's timeline
    rows and batch table, 00-slicer-setup's two round figures, and diagram 11 —
    which is generated from the index, so a stale SVG means nobody re-ran
    scripts/draw_diagrams.py."""
    bad: list[str] = []
    index = (DOCS / "manual" / "00-index.md").read_text()
    setup = (PRINT / "00-slicer-setup.md").read_text()
    svg = (DIAGRAMS / "11-build-timeline.svg").read_text()
    manifest = (DIAGRAMS / "MANIFEST.md").read_text()

    for bid, d in batch.items():
        if not re.search(rf"^- \*\*\d+ · Print\*\* — \[{bid} —[^\]]*\]\([^)]*\) · "
                         rf"{d['h']} h print\b", index, re.M):
            bad.append(f"00-index.md: timeline row for {bid} does not read {d['h']} h print")
        if not re.search(rf"^\| \[{bid} —[^\]]*\]\([^)]*\) \|[^|]*\| "
                         rf"{d['plates']} · {d['h']} \|", index, re.M):
            bad.append(f"00-index.md: batch table row for {bid} is not "
                       f"{d['plates']} · {d['h']}")
        if f">{d['h']} h print<" not in svg:
            bad.append(f"11-build-timeline.svg: no '{d['h']} h print' text for {bid} — "
                       f"re-run `python3 scripts/draw_diagrams.py --only 11`")

    b08 = batch["B08"]["black"] + batch["B08"]["orange"]
    for name, pat in (("~157 h of ASA", rf"~{round(th)} h of ASA"),
                      ("B08 skirt grams", rf"\b{b08} g of skirts \(B08\)")):
        if not re.search(pat, setup):
            bad.append(f"00-slicer-setup.md: expected /{pat}/ ({name})")

    n_rows = len(re.findall(r"^- \*\*\d+ · (?:Print|Build|Both)\*\* — ", index, re.M))
    strip = f"print, {n_rows} rows / {len(batch)} batches (sliced)"
    if strip not in svg:
        bad.append(f"11-build-timeline.svg: facts strip does not say {strip!r} — "
                   f"the index has {n_rows} timeline rows; re-run scripts/draw_diagrams.py")
    if f">{th} h<" not in svg:
        bad.append(f"11-build-timeline.svg: facts strip does not carry the {th} h print total")
    hm = re.search(r"^\| Hands-on time \| \*\*([\d.]+) h\*\*", index, re.M)
    if not hm:
        bad.append("00-index.md § Critical path: no parseable 'Hands-on time' row")
    elif f">{hm.group(1)} h<" not in svg:
        bad.append(f"11-build-timeline.svg: facts strip does not carry the index's "
                   f"{hm.group(1)} h hands-on figure")

    entry = re.search(r"^## 11\..*?(?=^## |\Z)", manifest, re.M | re.S)
    if not entry:
        bad.append("diagrams/MANIFEST.md: no entry 11")
    else:
        stale = re.findall(r"\b\d+ timeline rows\b|\b[\d.]+ h hands-on\b", entry.group(0))
        if stale:
            bad.append(f"diagrams/MANIFEST.md entry 11 restates a figure the diagram now "
                       f"reads from 00-index.md: {stale} — drop it, don't update it")
    return bad


_PLATE_ID_RE = re.compile(r"\bB\d\d-P\d\b")


def check_plate_ids(known: set[str]) -> list[str]:
    bad: list[str] = []
    for path in sorted(DOCS.rglob("*.md")):
        if "manual/steps" in path.as_posix():
            continue
        text = path.read_text()
        if path.name == "00-index.md":
            text = text.split("\n## Corrections log")[0]
        for n, line in enumerate(text.splitlines(), 1):
            for pid in _PLATE_ID_RE.findall(line):
                if pid not in known:
                    bad.append(f"{path.relative_to(REPO)}:{n}: plate {pid} does not exist")
    return bad


def main() -> int:
    plate, batch = load()
    plan = (DOCS / "voron-print-plan.md").read_text()
    readme = (PRINT / "README.md").read_text()
    bad: list[str] = []

    # 1. every plate's Load step: preview image + labelled Parts line
    seen = set()
    for bid, stem in CHAPTER.items():
        text = (PRINT / f"{stem}.md").read_text()
        for m in re.finditer(
                r"## Step B\d\d\.\d+ — Load(?: and print)? plate (B\d\d-P\d)(.*?)(?=\n## |\Z)",
                text, re.S):
            pid, body = m.group(1), m.group(2)
            seen.add(pid)
            if not re.search(rf"!\[Plate {pid}[^\]]*\]\(\.\./assets/plates/{pid}\.png\)", body):
                bad.append(f"{stem}.md: {pid} has no plate diagram image")
            pm = re.search(r"\*\*Parts:\*\*.*?— ([\d.]+) h, (\d+) g "
                           r"\(PrusaSlicer 2\.9\.6 estimate\)", body)
            if not pm:
                bad.append(f"{stem}.md: {pid} has no labelled Parts line")
            elif (float(pm.group(1)), int(pm.group(2))) != plate[pid][:2]:
                bad.append(f"{stem}.md: {pid} says "
                           f"{pm.group(1)} h / {pm.group(2)} g, csv says "
                           f"{plate[pid][0]} h / {plate[pid][1]} g")
        # chapter Time: line
        tm = re.search(r"\*\*Time:\*\* ([\d.]+) h \((\d+) plates?\)", text)
        if not tm:
            bad.append(f"{stem}.md: no parseable **Time:** line")
        elif (float(tm.group(1)), int(tm.group(2))) != (batch[bid]["h"], batch[bid]["plates"]):
            bad.append(f"{stem}.md: Time says {tm.group(1)} h / {tm.group(2)} plates, "
                       f"csv says {batch[bid]['h']} h / {batch[bid]['plates']}")
    missing = set(plate) - seen
    if missing:
        bad.append(f"no Load step found for: {', '.join(sorted(missing))}")

    # 2. plan §9 per-plate CSV
    blk = re.search(r"```csv\nplate_id,batch_id,hours,grams,colour\n(.*?)```", plan, re.S)
    if not blk:
        bad.append("plan §9: per-plate CSV block not found")
    else:
        for line in blk.group(1).strip().splitlines():
            pid, _b, h, g, _c = line.split(",")
            if (float(h), int(g)) != plate[pid][:2]:
                bad.append(f"plan §9 CSV: {pid} says {h} h / {g} g, csv says "
                           f"{plate[pid][0]} h / {plate[pid][1]} g")

    # 3. totals, everywhere they are stated
    th = round(sum(d["h"] for d in batch.values()), 1)
    tb = sum(d["black"] for d in batch.values())
    to = sum(d["orange"] for d in batch.values())
    n = sum(d["plates"] for d in batch.values())
    wanted = [
        ("plan header", plan, rf"{n} plates · \*\*{th} h\*\* print time · "
                              rf"\*\*{tb} g Galaxy Black \+ {to} g Prusa Orange\*\*"),
        ("plan §4.2 black", plan, rf"\| \*\*Galaxy Black\*\* \| \*\*{tb} g\*\*"),
        ("plan §4.2 orange", plan, rf"\| \*\*Prusa Orange\*\* \| \*\*{to} g\*\*"),
        ("plan §9 table total", plan,
         rf"\| \*\*TOTAL\*\* \| \| \*\*{n}\*\* \| \*\*{th}\*\* \| \*\*{tb}\*\* \| \*\*{to}\*\* \|"),
        ("plan §9 csv total", plan, rf"TOTAL,,{n},{th},{tb},{to},,"),
        ("print README total", readme,
         rf"\| \*\*TOTAL\*\* \| \*\*{n}\*\* \| \*\*{th}\*\* \| \*\*{tb}\*\* \| \*\*{to}\*\* \|"),
        ("print README intro", readme,
         rf"{n} plates, \*\*{th} h\*\*, \*\*{tb} g Galaxy Black \+ {to} g Prusa Orange\*\*"),
        ("root README", (REPO / "README.md").read_text(), rf"\*\*{th} h / {tb + to} g\*\*"),
    ]
    for name, text, pat in wanted:
        if not re.search(pat, text):
            bad.append(f"{name}: expected /{pat}/ — not found")

    # 4. per-batch rows in the plan §9 table and print/README
    for bid, d in batch.items():
        if not re.search(rf"\| {bid} \|[^|]*\| {d['plates']} \| {d['h']} \| "
                         rf"{d['black']} \| {d['orange']} \|", plan):
            bad.append(f"plan §9 table: {bid} row does not match "
                       f"{d['plates']}/{d['h']}/{d['black']}/{d['orange']}")
        if not re.search(rf"\| \[{bid}\][^|]*\| {d['plates']} \| {d['h']} \| "
                         rf"{d['black']} \| {d['orange']} \|", readme):
            bad.append(f"print/README: {bid} row does not match "
                       f"{d['plates']}/{d['h']}/{d['black']}/{d['orange']}")

    # 5. bins: scheme vs chapters, README and manifest
    bad += check_bins(readme)

    # 6. 00-index.md, 00-slicer-setup.md and diagram 11
    bad += check_index_and_timeline(batch, th)

    # 7. every plate id named anywhere in docs/ exists (a merged/renumbered plate
    #    leaves stale ids in prose that nothing else catches). The corrections log
    #    in 00-index.md is history and exempt; generated step pages are skipped.
    bad += check_plate_ids(set(plate))

    if bad:
        print(f"{len(bad)} mismatch(es):")
        for b in bad:
            print(f"  {b}")
        return 1
    print(f"OK — {len(plate)} plates, {len(batch)} batches, {th} h, "
          f"{tb} g black + {to} g orange, consistent across the chapters, "
          f"the plan (§3/§4/§9), print/README.md and README.md; "
          f"{len(bins.BINS)} bins consistent across bins.py, the chapters, README § Bins and "
          f"MANIFEST.csv; 00-index.md's timeline rows and batch table, 00-slicer-setup's "
          f"totals and diagram 11's hours all agree")
    return 0


if __name__ == "__main__":
    sys.exit(main())
