#!/usr/bin/env python3
"""Vendor LDO's pinned V2.4 350 BOM (Rev. D) into `scripts/data/ldo-350-bom.yml`.

The BOM is the source of truth for which kit box (bag) a Parts item comes from.
`scripts/parts.py` reads the yml; nothing reads the web page at build time.

    python3 scripts/kit_bom.py                  # curl the pinned page, rewrite the yml
    python3 scripts/kit_bom.py --html page.html # parse a saved copy instead
    python3 scripts/kit_bom.py --check          # re-fetch; exit 1 if the rows changed

Kit day: re-pin to the batch sheet that ships with the kit. Either point
`--url` at LDO's batch page, or edit the yml rows by hand; `aliases` below are
keyed by the BOM's own item text and survive a re-fetch.

Row schema: {carton, box, item, qty, aliases?, note?}. `box` is LDO's box name
with its punctuation tidied ("Fasteners,Tools&Misc" -> "Fasteners, Tools & Misc").
`aliases` are case-insensitive regexes searched in the plain, casefolded Parts
item text (× written as x). Fasteners, nuts, washers, spacers, T-nuts and
inserts need none: parts.canon_key() derives the same key from both spellings.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "scripts" / "data" / "ldo-350-bom.yml"
URL = "https://docs.ldomotors.com/en/voron/voron2/350_BOM/Rev_D"   # sources.yml pin

# BOM item text -> regexes (see module docstring). Keep each one specific
# enough that it cannot match another row's item.
ALIASES: dict[str, list[str]] = {
    "Power Cables": [r"\bpower cables? (?:bag|set)\b"],
    "Toolhead PCB Cables (Z Probe is included in this bag)": [
        r"\btoolhead (?:pcb )?cable", r"\bumbilical\b", r"\binductive probe\b|\btl-q5mc\b"],
    "Misc. Cables": [r"\bmisc\.? cables?\b"],
    "Bearing, F695-2RS": [r"\bf695\b"],
    "Bearing, 625-2RS": [r"\b625(?:-2rs)?\b.*\bbearing|\b625-2rs\b"],
    "Pulley, 2GT, 16T, (5mm ID 6mm W)": [r"\b16 ?t(?:ooth)?\b.*\bpulley|\bpulley\b.*\b16 ?t\b|^16t\b"],
    "Pulley, 2GT, 20T, (5mm ID 6mm W)": [
        r"\b20 ?t(?:ooth)?\b.*\bpulley\b.*\b6 ?mm\b|\bpulley\b.*\b20 ?t\b.*\b6 ?mm w",
        r"\b20 ?t(?:ooth)?\b.*\b6 ?mm\b.*\bpulley\b"],
    "Pulley, 2GT, 20T, (5mm ID 9mm W)": [
        r"\b20 ?t(?:ooth)?\b.*\b9 ?mm\b.*\bpulley\b|\bpulley\b.*\b20 ?t\b.*\b9 ?mm\b",
        r"\b20 ?t(?:ooth)? (?:9 ?mm )?pulley\b"],
    "Pulley, 2GT, 80T, (5mm ID 6mm W)": [r"\b80 ?t\b"],
    "Idler, 2GT, 20T, (5mm ID 6mm W)": [
        r"\b20 ?t(?:ooth)?\b.*\bidler\b.*\b6 ?mm|\b20 ?t(?:ooth)? 6 ?mm idler",
        r"\bgt2 20-?tooth idler\b|\b20-tooth idler\b"],
    "Idler, 2GT, 20T, (5mm ID 9mm W)": [
        r"\b20 ?t(?:ooth)?\b.*\b9 ?mm\b.*\bidler\b|\b20 ?t idler\b.*\b9 ?mm|\bgt2 20t 9 ?mm idler"],
    "Shaft, 5x60mm": [r"\b5 ?x ?60 ?mm\b.*\bshaft|\bshaft\b.*\b5 ?x ?60\b"],
    "Shaft, for Nozzle Probe": [r"\bnozzle[- ]probe shaft\b|\bprobe shaft\b"],
    "Thumb Screw Kit": [r"\bthumb ?screw\b"],
    "MR85 Bearing": [r"\bmr85\b"],
    "Bondtech IDGA Gear Set": [r"\bidga\b|\bbondtech\b.*\bgear"],
    "4mm Bowden Coupler": [r"\bbowden coupler\b"],
    "Teflon Tube (4mm OD 2mm ID) - 10cm": [
        r"\b(?:ptfe|teflon)\b.*\b2 ?mm id\b|\b(?:ptfe|teflon)\b.*/ ?2 ?mm\b|\b(?:ptfe|teflon)\b.*\b10 ?cm\b"],
    "Foam Tape, 1mm": [r"\bfoam tape,? 1 ?mm\b|\b1 ?mm foam tape\b"],
    "Foam Tape, 3mm": [r"\bfoam tape,? 3 ?mm\b|\b3 ?mm foam tape\b"],
    "Sandpaper": [r"\bsandpaper\b"],
    "4.3 Capacitive Display, for RPi DSI": [r"\bdsi\b|\btouch ?screen\b|\b4\.3\b.*\bdisplay\b"],
    "AC Inlet, Integrated Switch & Fuse": [r"\bac inlet\b|\biec inlet\b"],
    "Keystone CAT6 Insert": [r"\bkeystone\b"],
    "Raspberry Pi 4B (OPTIONAL item, check with your reseller whether the RPi is included)": [
        r"\braspberry pi\b(?!.*\bheatsink\b)|\bpi 4b?\b(?!.*\bheatsink\b)"],
    "Heatsink, for Raspberry Pi": [r"\b(?:raspberry )?pi heatsink\b|\bheatsink,? for (?:the )?(?:raspberry )?pi\b"],
    "Solid State Relay, Omron": [r"\bssr\b(?!.*\bbracket\b)|\bsolid state relay\b|\bg3nb\b"],
    "DIN Rail Mount Bracket for SSR": [r"\bssr\b.*\b(?:din )?bracket\b|\bdin bracket\b|\bdin rail mount bracket\b"],
    "Fiberglass Tape, 2x12cm": [r"\bfib(?:er|re)glass tape\b"],
    "Genuine Wago 221-412 Splicing Connector": [r"\b221-412\b|\bwago\b.*\b2-way\b"],
    "Genuine Wago 221-415 Splicing Connector": [r"\b221-415\b|\bwago\b.*\b5-way\b"],
    "SD Card, 32GB": [r"\b(?:micro ?)?sd card\b"],
    "XY Endstop PCB": [r"\bxy endstop (?:pcb|board)\b"],
    "3x2 XH Splicer PCB": [r"\b3 ?x ?2 xh splicer\b"],
    "2x2 XH Splicer PCB": [r"\b2 ?x ?2 xh splicer\b"],
    "Z Endstop PCB": [r"\bz endstop pcb\b"],
    "Nitehawk SB Toolhead PCB": [r"\bnitehawk\b"],
    "USB Adapter PCB": [r"\busb adapter pcb\b"],
    "Stealthburner Fan Adapter": [r"\bfan adapter\b"],
    "Klicky Probe Kit": [r"\bklicky\b.*\bkit\b"],
    "Print a Steppy Kit (LDO Mascot)": [r"\bsteppy\b"],
    "Tape, 3M VHB": [r"\bvhb\b"],
    "DIN Rail Plastic Endcap": [r"\bdin rail\b.*\bend ?caps?\b"],
    "Ferrule, VE0508": [r"\bv?e0508\b"],
    "Brass Brush": [r"\bbrass brush\b"],
    "6x3mm Neodymium Magnet": [r"\b6 ?x ?3 ?mm\b.*\bmagnets?\b|\bmagnets?\b.*\b6 ?x ?3\b"],
    "Teflon Tube (4mm OD 3mm ID) - 1.2m": [
        r"\b(?:ptfe|teflon)\b.*\b3 ?mm id\b|\b(?:ptfe|teflon)\b.*/ ?3 ?mm\b|\b(?:ptfe|teflon)\b.*\b1\.2 ?m\b"],
    "Zip Ties, 3x150mm": [r"\bzip[- ]?ties?\b"],
    "Brass Heatset Insert tool (for M3 Brass Inserts)": [r"\binsert tool\b|\bbrass tip\b|\b900m-t\b"],
    "Drill bit, 2mm": [r"\b2 ?mm drill\b|\bdrill bit\b"],
    "Hex Wrench, 1.5mm": [r"\b1\.5 ?mm hex (?:key|wrench)\b"],
    "Hex Wrench, 2mm": [r"(?<![.\d])2 ?mm hex (?:key|wrench)\b"],
    "Hex Wrench, 2.5mm": [r"\b2\.5 ?mm hex (?:key|wrench)\b"],
    "Hex Wrench, 3mm": [r"\b3 ?mm hex (?:key|wrench)\b"],
    "Hex Wrench, 4mm": [r"\b4 ?mm hex (?:key|wrench)\b"],
    "Slot head screwdriver, 2.5mm": [r"\bslot(?:ted)?(?: head)? screwdriver\b"],
    "Aluminium Handle": [r"\balumin(?:i)?um handles?\b|\bhandle ?bars?\b"],
    "50x50x15 Centrifugal Fan (24V)": [r"\b50 ?x ?50 ?x ?15\b|\b5015\b(?!.*nevermore)|\bcentrifugal\b|\bblower\b"],
    "40x40x10 Axial Fan (24V)": [r"\b40 ?x ?40 ?x ?10\b|\b4010\b|\bhotend fan\b"],
    "Nevermore Micro V5 Parts": [r"\bnevermore\b"],
    "60x60x20 Fan (24V)": [r"\b60 ?x ?60 ?x ?20\b|\b6020\b|\bbay fan\b"],
    "Gates Open Belt, 2GT, 9mm (by metre)": [r"\b(?:open )?belt\b.*\b9 ?mm\b|\b9 ?mm\b.*\bbelt\b"],
    "Gates Open Belt, 2GT, 6mm (by metre)": [r"\bopen belt\b.*\b6 ?mm\b|\b6 ?mm (?:wide )?(?:open )?belt\b|\b2gt open belt, 6 ?mm\b"],
    "Gates Belt Loop, 2GT, 6x188mm": [r"\b188 ?mm\b|\bclosed loop\b|\bbelt loop\b"],
    "Rubber Feet, 38x19mm (Amplifier Cabinet Feet)": [r"\brubber (?:feet|foot)\b"],
    "Drag Chain, 10x10mm, R18": [r"\b(?:drag|cable) chain\b.*\b10 ?x ?10\b|\br18\b"],
    "Drag Chain, 10x15mm, R28": [r"\b(?:drag|cable) chain\b.*\b10 ?x ?15\b|\br28\b"],
    "Linear Rail Stainless Steel, LDO-SLR12H-400Z1": [r"\bmgn12h?\b.*\brail\b|\bslr12h\b"],
    "Linear Rail Stainless Steel, LDO-SLR9H-400Z0": [r"\bmgn9h?\b.*\brails?\b|\bslr9h\b"],
    "LDO-V2.4F350-2020T-340E": [r"\be extrusions?\b|\b340 ?e\b"],
    "LDO-V2.4F350-2020T-430D": [r"\bd extrusions?\b|\b430 ?d\b"],
    "LDO-V2.4F350-2020-450C": [r"\bc extrusions?\b|\b450 ?c\b"],
    "LDO-V2.4F350-2020T-470A": [r"\ba extrusions?\b|\b470 ?a\b"],
    "LDO-V2.4F350-2020T-530B": [r"\bb extrusions?\b|\b530 ?b\b"],
    "LDO-36STH20-1004AHG(VRN) E Motor": [r"\b36sth20\b|\bpancake (?:stepper|motor)\b(?! lead)|\bnema ?14\b|^(?:the )?(?:e|extruder) motor\b"],
    "LDO-42STH48-2004MAH(VRN) AB Motor": [r"\b2004mah\b|\ba/?b motors?\b|\b0\.9 ?°"],
    "LDO-42STH48-2004AC(VRN) Z Motor": [r"\b2004ac\b|\bz motors?\b(?!\s+cables?)"],
    "C13 Power Cord 1.5 meter": [r"\bc13\b|\bpower cord\b"],
    "PVC Wire Duct 20Wx25H": [r"\bwire duct\b|\bpvc duct\b"],
    "E3D Revo Hotend (HF)": [r"\brevo\b"],
    "DIN Rails (35mm W)": [r"\bdin rails?\b(?!.*\b(?:end ?caps?|clips?|bracket|mount)\b)"],
    "LDO Leviathan Mainboard": [r"\bleviathan\b(?!.*\bbracket\b)"],
    "Meanwell LRS-200-24 PSU*": [r"\blrs-200\b|\bpsu\b(?!.*\b(?:bracket|cables?)\b)|\bpower supply\b"],
    "Extrusion Slot Cover, 6mm width": [r"\bslot covers?\b"],
    "Deck Panel, Acrylic, Black, 469x469x3mm": [r"\bdeck panel\b"],
    "Back Panel, Acrylic, Black, 483x503x3mm": [r"\bback panel\b"],
    "Bottom Panel, Acrylic, Black, 469x469x4mm": [r"\bbottom panel\b"],
    "Door Panel, PC, Clear, 241x503x3mm": [r"\bdoor panels?\b"],
    "Side Panel, PC, Clear, 483x503x3mm": [r"\bside panels?\b"],
    "Top Panel, PC, Clear, 483x483x3mm": [r"\btop panel\b"],
    "Magnetic Pad 2.4-350": [r"\bmagnetic (?:pad|sheet)\b"],
    "Spring Steel Flex Plate 2.4-350": [r"\bflex ?plate\b|\bspring steel\b|\bpei sheet\b"],
    "Build Plate, Cast 5083 Aluminium, Blanchard Ground, w/ LDO AC Heatpad & Thermal Fuse (125C), 355x355x10mm": [
        r"\bbuild plate\b|\bbed plate\b|\bheated bed\b"],
    "Leviathan Bracket Left": [r"\bleviathan bracket left\b"],
    "Leviathan Bracket Right": [r"\bleviathan bracket right\b"],
    "NH Adapter Mount": [r"\bnh adapter mount\b"],
    "DIN Clip": [r"\bdin clips?\b"],
    "CW2 Chain Anchor Tilted": [r"\bchain anchor tilted\b"],
    "2x3 Splitter Spacer": [r"\bsplitter spacer\b"],
    "LDO Nozzle Probe": [r"\bnozzle probe\b(?!.*\bshaft\b)"],
    "Bed WAGO Mount": [r"\bbed wago mount\b"],
    "Stealthburner LED Diffuser": [r"\bled diffuser\b"],
    "CW2 PCB Spacer": [r"\bcw2 pcb spacer\b"],
}


def _tidy_box(name: str) -> str:
    name = re.sub(r"\s*,\s*", ", ", name.strip())
    name = re.sub(r"\s*&\s*", " & ", name)
    return name.replace(", & ", " & ")


class _Table(HTMLParser):
    """Rows of the page's one BOM table, as lists of (text, rowspan, colspan)."""

    def __init__(self) -> None:
        super().__init__()
        self.rows: list[list[tuple[str, int, int]]] = []
        self._cell: tuple[int, int] | None = None
        self._buf: list[str] = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "tr":
            self.rows.append([])
        elif tag in ("td", "th"):
            self._cell = (int(a.get("rowspan") or 1), int(a.get("colspan") or 1))
            self._buf = []
        elif tag in ("p", "br") and self._cell is not None:
            self._buf.append(" ")

    def handle_endtag(self, tag):
        if tag in ("td", "th") and self._cell is not None and self.rows:
            text = re.sub(r"\s+", " ", "".join(self._buf).replace("\xa0", " ")).strip()
            self.rows[-1].append((text, *self._cell))
            self._cell = None

    def handle_data(self, data):
        if self._cell is not None:
            self._buf.append(data)


def _grid(rows: list[list[tuple[str, int, int]]]) -> list[list[str]]:
    """Expand rowspan/colspan into a plain grid."""
    grid, pending = [], {}   # col -> (text, rows left)
    for row in rows:
        out, col, ci = [], 0, 0
        while ci < len(row) or col in pending:
            if col in pending:
                text, left = pending[col]
                out.append(text)
                if left > 1:
                    pending[col] = (text, left - 1)
                else:
                    del pending[col]
                col += 1
                continue
            text, rs, cs = row[ci]
            ci += 1
            for _ in range(cs):
                out.append(text)
                if rs > 1:
                    pending[col] = (text, rs - 1)
                col += 1
        grid.append(out)
    return grid


def _qty(text: str):
    try:
        v = float(text)
    except ValueError:
        return None
    return int(v) if v == int(v) else v


def parse(html_text: str) -> tuple[list[dict], list[str]]:
    """(rows, notes) from the BOM page."""
    t = _Table()
    t.feed(html_text)
    grid = _grid(t.rows)
    if not grid or [c.lower() for c in grid[0][:4]] != ["carton", "box", "item", "qty."]:
        raise SystemExit("kit_bom: unexpected BOM table header: %r" % (grid[0] if grid else None))
    rows, notes = [], []
    for cells in grid[1:]:
        if len(cells) < 4:
            continue
        carton, box, item, qty = cells[:4]
        if not carton.strip().isdigit():
            if item and item not in notes:
                notes.append(item)          # the EU PSU footnote spans the whole row
            continue
        box = _tidy_box(box)
        q = _qty(qty)
        if q is None and not qty.strip():
            # "LDO Printed Parts" contents: "Leviathan Bracket Left x1 … DIN Clip x4 …"
            for name, n in re.findall(r"(.+?)\s+x(\d+)(?=\s|$)", item):
                rows.append({"carton": int(carton), "box": box, "item": name.strip(),
                             "qty": int(n), "note": "LDO Printed Parts bag"})
            continue
        rows.append({"carton": int(carton), "box": box, "item": item, "qty": q})
    for r in rows:
        if r["item"] in ALIASES:
            r["aliases"] = ALIASES[r["item"]]
    return rows, notes


def fetch(url: str) -> str:
    return subprocess.run(["curl", "-sSL", "--fail", url], check=True,
                          capture_output=True, text=True).stdout


def render(rows: list[dict], notes: list[str], url: str, fetched: str) -> str:
    import yaml

    head = [
        "# LDO Voron 2.4 350 kit BOM, vendored by scripts/kit_bom.py (scripts/parts.py reads it).",
        "# Hand edits are fine (kit-day re-pin) but a re-fetch overwrites them; aliases live in",
        "# kit_bom.ALIASES, keyed by item text.",
        "# source: %s" % url,
        "# fetched: %s (curl)" % fetched,
        "# Kit day: re-pin to the batch sheet shipped with the kit (Step 00.2).",
    ]
    body = yaml.safe_dump({"source": url, "fetched": fetched, "notes": notes, "rows": rows},
                          sort_keys=False, allow_unicode=True, width=120)
    return "\n".join(head) + "\n" + body


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--url", default=URL)
    ap.add_argument("--html", help="parse a saved copy of the page instead of fetching")
    ap.add_argument("--out", default=str(OUT))
    ap.add_argument("--check", action="store_true",
                    help="re-fetch and compare the rows with the vendored file; exit 1 on drift")
    args = ap.parse_args(argv)

    html_text = Path(args.html).read_text(encoding="utf-8") if args.html else fetch(args.url)
    rows, notes = parse(html_text)
    missing = sorted(set(ALIASES) - {r["item"] for r in rows})
    if args.check:
        import yaml

        have = yaml.safe_load(Path(args.out).read_text(encoding="utf-8"))["rows"]
        strip = lambda rs: [{k: r[k] for k in ("carton", "box", "item", "qty")} for r in rs]  # noqa: E731
        if strip(have) != strip(rows):
            print("kit_bom: the live BOM differs from %s" % args.out)
            return 1
        print("kit_bom: %d rows, unchanged" % len(rows))
        return 0
    fetched = _dt.date.today().isoformat()
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(rows, notes, args.url, fetched), encoding="utf-8")
    print("kit_bom: wrote %d rows (%d boxes) to %s" % (
        len(rows), len({r["box"] for r in rows}), out.relative_to(REPO) if out.is_relative_to(REPO) else out))
    if missing:
        print("kit_bom: WARN aliases for items no longer in the BOM: %s" % "; ".join(missing))
    return 0


if __name__ == "__main__":
    sys.exit(main())
