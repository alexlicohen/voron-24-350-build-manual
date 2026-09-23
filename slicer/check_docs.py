#!/usr/bin/env python3
"""Verify the manual's printed numbers still match slicer/estimates.csv.

The plate hours and grams appear in five places (the batch chapters, the plan's
§3 headers, §4, §9 and print/README.md). This checks all of them against the
one file the slicer wrote, so a re-slice cannot silently leave a stale number at
the bench. It also checks the bin scheme (slicer/bins.py) against the batch
chapters' Printed-parts `Bin` column and *Sort into bins* steps, print/README.md
§ Bins, and the `bin` column of docs/manual/assets/parts/MANIFEST.csv.

    python3 slicer/check_docs.py        # exits non-zero on any mismatch

B11 (the PETG V0 bay ducting, `run="bay"` in slicer/plates.py) is outside the 22-plate ASA
run: every run total above excludes it, and § 8 checks B11's own numbers the same way (batch
page, print/README's B11 tables, plan §3 header and §9 B11 CSV, 00-index.md's two B11 rows).

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
from plates import PLATES, run_of  # noqa: E402
REPO = ROOT.parent
DOCS = REPO / "docs"
PRINT = DOCS / "manual" / "print"


def r1(x) -> float:
    return float(Decimal(str(x)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))


def r0(x) -> int:
    return int(Decimal(str(x)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def load():
    rows = [r for r in csv.DictReader((ROOT / "estimates.csv").open())
            if not r["plate"].startswith("TOTAL")]
    plate = {r["plate"]: (r1(r["hours"]), r0(r["grams"]), r["batch"], r["colour"])
             for r in rows}
    batch = collections.OrderedDict()
    for pid, (h, g, b, c) in plate.items():
        d = batch.setdefault(b, {"plates": 0, "h": 0.0, "black": 0, "blue": 0, "petg": 0})
        d["plates"] += 1
        d["h"] = round(d["h"] + h, 1)
        d[c] += g
    return plate, batch


# Display name of the accent spool in the docs. The exact Prusament blue colour name
# is not known yet (spool unread); change this one line when it is, and re-run.
ACCENT = "ASA Blue"

CHAPTER = {
    "B00": "B00-calibration-and-jigs", "B01": "B01-z-drive-assemblies",
    "B02": "B02-accent-parts-orange", "B03": "B03-ab-drive-units-and-front-idlers",
    "B04": "B04-xy-joints-and-x-carriage", "B05": "B05-z-joints-and-z-chain",
    "B06": "B06-toolhead-sb-cw2-klicky", "B07": "B07-electronics-bay-and-lighting",
    "B08": "B08-skirts-and-front-modules", "B09": "B09-panels-filtration-spool",
    "B10": "B10-clicky-clack-door",
    "B11": "B11-bay-ducting",
}
# Batches outside the ASA run (slicer/plates.py run="bay"): no run total includes them.
SEPARATE = {spec["batch"] for pid, spec in PLATES.items() if run_of(pid) != "asa"}


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
        if bid in SEPARATE:
            continue
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

    b08 = batch["B08"]["black"] + batch["B08"]["blue"]
    for name, pat in (("~157 h of ASA", rf"~{round(th)} h of ASA"),
                      ("B08 skirt grams", rf"\b{b08} g of skirts \(B08\)")):
        if not re.search(pat, setup):
            bad.append(f"00-slicer-setup.md: expected /{pat}/ ({name})")

    n_rows = len(re.findall(r"^- \*\*\d+ · (?:Print|Build|Both)\*\* — ", index, re.M))
    n_asa = len([b for b in batch if b not in SEPARATE])
    strip = f"print, {n_rows} rows / {n_asa} batches (sliced)"
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


def b11_groups(plate) -> collections.OrderedDict:
    """group -> {"plates", "h", "g"} for B11, additive like every other figure."""
    out = collections.OrderedDict()
    for pid, spec in PLATES.items():
        if spec["batch"] != "B11":
            continue
        d = out.setdefault(spec["group"], {"plates": 0, "h": 0.0, "g": 0, "ids": []})
        d["plates"] += 1
        d["h"] = round(d["h"] + plate[pid][0], 1)
        d["g"] += plate[pid][1]
        d["ids"].append(pid)
    return out


def check_b11(plate, plan: str, readme: str) -> list[str]:
    """B11 is added up on its own; every place that states a B11 figure must agree."""
    bad: list[str] = []
    grp = b11_groups(plate)
    pre, post = grp["before-kit"], grp["after-kit"]
    n = pre["plates"] + post["plates"]
    h = round(pre["h"] + post["h"], 1)
    g = pre["g"] + post["g"]
    page = (PRINT / f"{CHAPTER['B11']}.md").read_text()
    index = (DOCS / "manual" / "00-index.md").read_text()
    wanted = [
        ("B11 page Time line (before kit)", page, rf"\*\*Time:\*\* {h} h \({n} plates\).*?"
         rf"{pre['h']} h before kit.*?{post['h']} h after the kit-day measurements"),
        ("B11 page ledger total", page, rf"\b{g} g\b"),
        ("print/README B11 before-kit row", readme,
         rf"^\| \[B11\]\([^)]*\) before kit \| {pre['plates']} \| {pre['h']} \| {pre['g']} \|"),
        ("print/README B11 after-kit row", readme,
         rf"^\| \[B11\]\([^)]*\) after the kit-day measurements \| {post['plates']} \| "
         rf"{post['h']} \| {post['g']} \|"),
        ("print/README B11 total row", readme,
         rf"^\| \*\*B11 total\*\* \| \*\*{n}\*\* \| \*\*{h}\*\* \| \*\*{g}\*\* \|"),
        ("print/README B11 ledger total", readme,
         rf"^\| \*\*TOTAL PETG V0\*\* \| \*\*{g}\*\* \|"),
        ("plan §3 B11 header", plan,
         rf"^### Batch B11 — [^\n]*· \*\*{n} plates · {h} h · {g} g Jet Black PETG V0\*\*"),
        ("plan §9 B11 csv total", plan, rf"^TOTAL B11,B11,all,{h},{g},petg$"),
        ("00-index B11 before-kit row", index,
         rf"^- \*\*\d+ · Print\*\* — \[B11 — [^\]]*\]\([^)]*#before-kit\) · {pre['h']} h print\b"),
        ("00-index B11 after-kit row", index,
         rf"^- \*\*\d+ · Print\*\* — \[B11 — [^\]]*\]\([^)]*#after-the-kit-day-measurements\) "
         rf"\*\*KIT\*\* · {post['h']} h print\b"),
        ("00-index B11 batch-table row", index,
         rf"^\| \[B11 —[^\]]*\]\([^)]*\) \|[^|]*\| {n} · {h} \|"),
    ]
    for name, text, pat in wanted:
        if not re.search(pat, text, re.M | re.S):
            bad.append(f"B11 — {name}: expected /{pat}/ — not found")
    svg = (DOCS / "manual" / "assets" / "diagrams" / "11-build-timeline.svg").read_text()
    for gname, d in (("before kit", pre), ("after kit", post)):
        if f">{d['h']} h print<" not in svg:
            bad.append(f"11-build-timeline.svg: no '{d['h']} h print' text for B11 {gname} — "
                       f"re-run `python3 scripts/draw_diagrams.py --only 11`")
    # plan §9 B11 per-plate block
    blk = re.search(r"```csv\nplate_id,batch_id,group,hours,grams,colour\n(.*?)```", plan, re.S)
    if not blk:
        bad.append("plan §9: B11 per-plate CSV block not found")
    else:
        seen = set()
        for line in blk.group(1).strip().splitlines():
            if line.startswith("TOTAL"):
                continue
            pid, _b, group, ph, pg, _c = line.split(",")
            seen.add(pid)
            if (float(ph), int(pg)) != plate[pid][:2] or group != PLATES[pid]["group"]:
                bad.append(f"plan §9 B11 CSV: {pid} says {group} {ph} h / {pg} g, csv says "
                           f"{PLATES[pid]['group']} {plate[pid][0]} h / {plate[pid][1]} g")
        want_ids = set(pre["ids"]) | set(post["ids"])
        if seen != want_ids:
            bad.append(f"plan §9 B11 CSV lists {sorted(seen)}, plates.py has {sorted(want_ids)}")
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

    # 2. plan §9 per-plate CSV (the ASA run; B11 has its own block, § 8)
    blk = re.search(r"```csv\nplate_id,batch_id,hours,grams,colour\n(.*?)```", plan, re.S)
    if not blk:
        bad.append("plan §9: per-plate CSV block not found")
    else:
        for line in blk.group(1).strip().splitlines():
            pid, _b, h, g, _c = line.split(",")
            if (float(h), int(g)) != plate[pid][:2]:
                bad.append(f"plan §9 CSV: {pid} says {h} h / {g} g, csv says "
                           f"{plate[pid][0]} h / {plate[pid][1]} g")

    # 3. totals, everywhere they are stated - the ASA run only (B11 is § 8)
    run = {b: d for b, d in batch.items() if b not in SEPARATE}
    th = round(sum(d["h"] for d in run.values()), 1)
    tb = sum(d["black"] for d in run.values())
    to = sum(d["blue"] for d in run.values())
    n = sum(d["plates"] for d in run.values())
    wanted = [
        ("plan header", plan, rf"{n} plates · \*\*{th} h\*\* print time · "
                              rf"\*\*{tb} g Galaxy Black \+ {to} g {ACCENT}\*\*"),
        ("plan §4.2 black", plan, rf"\| \*\*Galaxy Black\*\* \| \*\*{tb} g\*\*"),
        ("plan §4.2 accent", plan, rf"\| \*\*{ACCENT}\*\* \| \*\*{to} g\*\*"),
        ("plan §9 table total", plan,
         rf"\| \*\*TOTAL\*\* \| \| \*\*{n}\*\* \| \*\*{th}\*\* \| \*\*{tb}\*\* \| \*\*{to}\*\* \|"),
        ("plan §9 csv total", plan, rf"TOTAL,,{n},{th},{tb},{to},,"),
        ("print README total", readme,
         rf"\| \*\*TOTAL\*\* \| \*\*{n}\*\* \| \*\*{th}\*\* \| \*\*{tb}\*\* \| \*\*{to}\*\* \|"),
        ("print README intro", readme,
         rf"{n} plates, \*\*{th} h\*\*, \*\*{tb} g Galaxy Black \+ {to} g {ACCENT}\*\*"),
        ("root README", (REPO / "README.md").read_text(), rf"\*\*{th} h / {tb + to} g\*\*"),
    ]
    for name, text, pat in wanted:
        if not re.search(pat, text):
            bad.append(f"{name}: expected /{pat}/ — not found")

    # 4. per-batch rows in the plan §9 table and print/README
    for bid, d in run.items():
        if not re.search(rf"\| {bid} \|[^|]*\| {d['plates']} \| {d['h']} \| "
                         rf"{d['black']} \| {d['blue']} \|", plan):
            bad.append(f"plan §9 table: {bid} row does not match "
                       f"{d['plates']}/{d['h']}/{d['black']}/{d['blue']}")
        if not re.search(rf"\| \[{bid}\][^|]*\| {d['plates']} \| {d['h']} \| "
                         rf"{d['black']} \| {d['blue']} \|", readme):
            bad.append(f"print/README: {bid} row does not match "
                       f"{d['plates']}/{d['h']}/{d['black']}/{d['blue']}")

    # 5. bins: scheme vs chapters, README and manifest
    bad += check_bins(readme)

    # 6. 00-index.md, 00-slicer-setup.md and diagram 11
    bad += check_index_and_timeline(batch, th)

    # 8. B11, the bay ducting: its own totals, stated consistently everywhere
    if "B11" in batch:
        bad += check_b11(plate, plan, readme)

    # 7. every plate id named anywhere in docs/ exists (a merged/renumbered plate
    #    leaves stale ids in prose that nothing else catches). The corrections log
    #    in 00-index.md is history and exempt; generated step pages are skipped.
    bad += check_plate_ids(set(plate))

    if bad:
        print(f"{len(bad)} mismatch(es):")
        for b in bad:
            print(f"  {b}")
        return 1
    print(f"OK — {n} plates, {len(run)} batches, {th} h, "
          f"{tb} g black + {to} g {ACCENT.lower()}, consistent across the chapters, "
          f"the plan (§3/§4/§9), print/README.md and README.md; "
          f"{len(bins.BINS)} bins consistent across bins.py, the chapters, README § Bins and "
          f"MANIFEST.csv; 00-index.md's timeline rows and batch table, 00-slicer-setup's "
          f"totals and diagram 11's hours all agree; "
          + (f"B11 {batch['B11']['plates']} plates, {batch['B11']['h']} h, {batch['B11']['petg']} g "
             f"PETG V0 on its own, consistent across its page, print/README, the plan and the index"
             if "B11" in batch else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
