#!/usr/bin/env python3
"""Verify the manual's printed numbers still match slicer/estimates.csv.

The plate hours and grams appear in five places (the batch chapters, the plan's
§3 headers, §4, §9 and print/README.md). This checks all of them against the
one file the slicer wrote, so a re-slice cannot silently leave a stale number at
the bench.

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
            if f"![Plate {pid}](../assets/plates/{pid}.png)" not in body:
                bad.append(f"{stem}.md: {pid} has no plate preview image")
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

    if bad:
        print(f"{len(bad)} mismatch(es):")
        for b in bad:
            print(f"  {b}")
        return 1
    print(f"OK — {len(plate)} plates, {len(batch)} batches, {th} h, "
          f"{tb} g black + {to} g orange, consistent across the chapters, "
          f"the plan (§3/§4/§9), print/README.md and README.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
