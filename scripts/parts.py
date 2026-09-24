#!/usr/bin/env python3
"""`**Parts:**` fields: the one owner of parsing, counting, merging, the
printed-part/bin lookup and the kit-BOM (bag source) resolve.

`scripts/build_steps.py` renders step lists and Gather blocks from what this
module returns; `scripts/lint_manual.py` runs checks 6 and 7 through it.
CONVENTIONS.md § Parts grammar is the contract; in short:

    **Parts:** none.                         (single line, unchanged)

    **Parts:**                               (assembly chapters 00–14)

    - M3×40 SHCS ×24                         count = total for the whole step
    - `[a]_z_drive_baseplate_a` ×2           printed: bin from assets/parts/MANIFEST.csv
    - reused: the four belted shaft assemblies   listed, never summed
    - tool: 2.5 mm hex key                   gathered apart, never reconciled
    - consumable: masking tape
    - M3 heat-set insert ×7 — from KADRICK kit   source set by hand (not in the kit BOM)

Print chapters (B00–B11) keep the single-line form, `;`/`·`-separated: their
Load-step lines are also read by build_tonight.py and slicer/check_docs.py.
Both forms parse here. The kit source comes from scripts/data/ldo-350-bom.yml
(vendored by scripts/kit_bom.py), never typed on the line.

    python3 scripts/parts.py --selftest
    python3 scripts/parts.py --ledger [BOM-item regex]   # per-step consumption ledger

Hardware ownership (check 7): scripts/data/hardware-ownership.yml says where
each cross-chapter kit unit is consumed; `staged:` items are set out for a later
step. Rule: review/2026-09-23-sweep/HARDWARE-OWNERSHIP.md.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
MANUAL = REPO / "docs" / "manual"
BOM_YML = REPO / "scripts" / "data" / "ldo-350-bom.yml"

PARTS_RE = re.compile(r"^\*\*Parts:\*\*\s*(.*)$")
CODE_SPAN_RE = re.compile(r"`([^`]+)`")
_BQ_PREFIX_RE = re.compile(r"^>\s?")
_LIST_ITEM_RE = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+(.*)$")
_NONE_WORDS = {"none", "—", "-", "n/a"}


# --------------------------------------------------------------------------
# text helpers (build_steps imports these)
# --------------------------------------------------------------------------


def plain(text: str) -> str:
    """Markdown inline -> plain text, for card titles and nav labels."""
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = text.replace("`", "").replace("**", "").replace("*", "")
    return re.sub(r"\s+", " ", text).strip()


def split_top_level(text: str, sep: str) -> list[str]:
    out, depth, tick, buf = [], 0, False, []
    for ch in text:
        if ch == "`":
            tick = not tick
        elif not tick:
            if ch in "([":
                depth += 1
            elif ch in ")]":
                depth = max(0, depth - 1)
            elif ch == sep and depth == 0:
                out.append("".join(buf).strip())
                buf = []
                continue
        buf.append(ch)
    out.append("".join(buf).strip())
    return [p for p in out if p]


def _logical(line: str) -> str:
    return _BQ_PREFIX_RE.sub("", line, count=1)


# --------------------------------------------------------------------------
# printed parts: renders and bins from assets/parts/MANIFEST.csv
# --------------------------------------------------------------------------

# stl stem -> part render, longest stem first so `Handle-Hinge_Top` wins over `Handle`.
PART_THUMBS: list[tuple[re.Pattern, Path]] = []
# Same keys, mapped to the manifest's `bin` column, so the gather block can say
# which bin a printed part is waiting in.
PART_BINS: list[tuple[re.Pattern, str]] = []


def load_part_thumbs() -> None:
    import csv

    PART_THUMBS.clear()
    PART_BINS.clear()
    manifest = MANUAL / "assets" / "parts" / "MANIFEST.csv"
    if not manifest.exists():
        return
    rows: list[tuple[str, Path]] = []
    bins: list[tuple[str, str]] = []
    seen: set[str] = set()
    seen_bin: set[str] = set()
    with manifest.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            stl = (row.get("stl") or "").strip()
            png = (row.get("png") or "").strip()
            if not stl:
                continue
            path = REPO / png if png else None
            # Chapters name a part as the Voron repo does (`z_drive_main_a`);
            # the manifest keeps the LDO filename's `[a]_` colour prefix, its
            # `_x2` / `-2X` multiplicity suffix and any `(contributed_by_…)`
            # tail. Register every spelling in between.
            keys = {Path(stl).stem}
            keys |= {re.sub(r"\([^()]*\)$", "", k) for k in keys}
            keys |= {re.sub(r"(?:[-_][xX]\d+|-\d+[xX])$", "", k) for k in keys}
            keys |= {re.sub(r"^\[[a-z]\]_", "", k) for k in keys}
            ordered = sorted((k for k in keys if k), key=len, reverse=True)
            for key in ordered:
                if path is not None and path.exists() and key not in seen:
                    seen.add(key)
                    rows.append((key, path))
                if key not in seen_bin:
                    seen_bin.add(key)
                    bins.append((key, (row.get("bin") or "").strip()))
    rows.sort(key=lambda r: -len(r[0]))
    bins.sort(key=lambda r: -len(r[0]))
    PART_THUMBS.extend(
        (re.compile(r"(?<![0-9A-Za-z_])%s(?![0-9A-Za-z_])" % re.escape(stem)), png)
        for stem, png in rows
    )
    PART_BINS.extend(
        (re.compile(r"(?<![0-9A-Za-z_])%s(?![0-9A-Za-z_])" % re.escape(stem)), bin_id)
        for stem, bin_id in bins
    )


def thumb_for(item: str, dest_dir: Path) -> str | None:
    """Part render for a Parts item that names an STL in backticks."""
    spans = CODE_SPAN_RE.findall(item)
    if not spans:
        return None
    import os

    # Spans in item order: the thumb depicts the part the bullet leads with,
    # not whichever named part happens to have the longest filename.
    for s in spans:
        for pattern, png in PART_THUMBS:
            if pattern.search(s):
                return os.path.relpath(str(png), str(dest_dir)).replace("\\", "/")
    return None


_BIN_IN_TEXT_RE = re.compile(r"\bbins?\s+`?([0-9]{2}-[A-Za-z0-9-]+)`?")


def printed_info(item: str) -> tuple[bool, list[str]]:
    """(is a printed part, bins it lives in) for one Parts item."""
    spans = CODE_SPAN_RE.findall(item)
    printed, bins = False, []
    for span in spans:
        if span.lower().endswith(".stl"):
            printed = True
        for pattern, bin_id in PART_BINS:
            if pattern.search(span):
                printed = True
                for one in bin_id.split(";"):
                    one = one.strip()
                    if one and one not in bins:
                        bins.append(one)
                break
    for one in _BIN_IN_TEXT_RE.findall(item):
        if one not in bins:
            bins.append(one)
    return printed, bins


# --------------------------------------------------------------------------
# counts
# --------------------------------------------------------------------------

# Count forms, searched on the item with its `code spans` masked out so that
# `z_rail_stop_x4` and `M3×8` are never read as quantities.
_CNT_PREFIX_RE = re.compile(r"^\s*(\d+)\s*[×xX](?=\s)")
# A suffix count is `… ×4`, never the `×` of a dimension: reject one whose left
# neighbour is a digit (`Ø4.7 × 5 mm`) or whose number carries a unit.
_CNT_SUFFIX_RE = re.compile(
    r"(?<=\s)[×xX]\s*(\d+)(?![0-9A-Za-z])"
    r"(?!\s*(?:mm|cm|µm|m\b|kg|g\b|h\b|min\b|°))"
)
_CNT_PAREN_RE = re.compile(r"(?<=\s)\((\d+)\)")
_CODE_MASK_RE = re.compile("\x00(\\d+)\x00")


def _mask_code(text: str) -> tuple[str, list[str]]:
    spans: list[str] = []

    def repl(m: re.Match) -> str:
        spans.append(m.group(0))
        return "\x00%d\x00" % (len(spans) - 1)

    return CODE_SPAN_RE.sub(repl, text), spans


def _unmask_code(text: str, spans: list[str]) -> str:
    return _CODE_MASK_RE.sub(lambda m: spans[int(m.group(1))], text)


def count_of(item: str) -> tuple[int | None, str]:
    """(count, item without its count token). No count token -> (None, item)."""
    masked, spans = _mask_code(item)
    for rx in (_CNT_PREFIX_RE, _CNT_SUFFIX_RE, _CNT_PAREN_RE):
        m = rx.search(masked)
        if m and rx is _CNT_SUFFIX_RE and masked[:m.start()].rstrip()[-1:].isdigit():
            # `Ø4.7 × 5` (spaced) is a dimension; `M3×5×4 ×3` and
            # `T-nut, 2020 ×4` are a size then a count.
            if re.match(r"[×xX]\s", m.group(0)):
                m = None
        if m:
            rest = (masked[:m.start()] + " " + masked[m.end():])
            rest = re.sub(r"\s+", " ", rest)
            rest = re.sub(r"\s+([,;.)\]])", r"\1", rest)   # ` ,` left where the count was
            rest = re.sub(r"([(\[])\s+", r"\1", rest)
            rest = rest.strip(" ,;·").strip()
            return int(m.group(1)), _unmask_code(rest, spans).strip()
    return None, item.strip()


def merge_key(name: str) -> str:
    return re.sub(r"\s+", " ", plain(name)).strip().strip(".,;").casefold()


# --------------------------------------------------------------------------
# the single-line form (print chapters; assembly chapters until converted)
# --------------------------------------------------------------------------


def parts_items(line: str) -> list[str]:
    """The items of a single-line `**Parts:**` field, or [] when it lists nothing.

    House separators are `;` then `·`; a comma list counts only when *every*
    chunk carries its own count, so `door panels (PC clear, 241×503) ×2` stays
    one item while `build plate ×1, magnetic pad ×1` becomes two.
    """
    body = PARTS_RE.match(line).group(1).strip()
    low = plain(body).strip().rstrip(".").lower()
    if not body or low in _NONE_WORDS:
        return []
    items = split_top_level(body, ";")
    if len(items) == 1:
        items = split_top_level(body, "·")
    if len(items) == 1:
        commas = split_top_level(body, ",")
        if len(commas) > 1 and all(count_of(c)[0] is not None for c in commas):
            items = commas
    return [i.strip().rstrip(".").strip() for i in items if i.strip()]


# The legacy gather tally: build_steps' Gather blocks for segments with no
# list-form field use exactly this, so their rendered output never moves.
_NONE_ITEM_RE = re.compile(r"^\s*none\b", re.IGNORECASE)
# An item with no count that runs this long is prose, not a part; it is still
# listed verbatim, but the build log names it so a chapter can be tightened.
UNPARSED_WORDS = 8
PARSE_WARNINGS: list[str] = []


@dataclass
class Tally:
    display: str
    count: int
    explicit: bool = False      # a count was written in the chapter
    bins: list[str] = field(default_factory=list)
    key: str = ""               # grouped path: merge identity
    group: tuple = ()           # grouped path: (order, heading)
    note: str = ""              # grouped path: muted suffix (bin, box)
    counted: bool = True        # False for `reused:` — listed, never summed


def collect(items: list[Tally], item: str, where: str) -> None:
    """Legacy tally: merge by plain name, uncounted items count as one."""
    if _NONE_ITEM_RE.match(plain(item)):
        return
    count, name = count_of(item)
    if count is None and len(plain(name).split()) > UNPARSED_WORDS:
        PARSE_WARNINGS.append("%s: unparsed Parts item, listed verbatim: %s" % (where, name))
    key = merge_key(name)
    if not key:
        return
    printed, bins = printed_info(name)
    for existing in items:
        if merge_key(existing.display) == key:
            existing.count += count if count is not None else 1
            existing.explicit = existing.explicit or count is not None
            for b in bins:
                if b not in existing.bins:
                    existing.bins.append(b)
            return
    items.append(Tally(display=name, count=count if count is not None else 1,
                       explicit=count is not None, bins=list(bins)))


# --------------------------------------------------------------------------
# kit BOM: which box/bag an item comes from
# --------------------------------------------------------------------------

_BOM: list[dict] | None = None


def load_bom(path: Path = BOM_YML) -> list[dict]:
    """Rows of the vendored BOM, each with `_n` (row order), `_key` (canon
    key or None) and `_rx` (compiled aliases)."""
    global _BOM
    if _BOM is not None and path == BOM_YML:
        return _BOM
    import yaml

    rows = []
    if path.exists():
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        for n, r in enumerate(data.get("rows") or []):
            r = dict(r)
            r["_n"] = n
            r["_key"] = canon_key(r["item"])
            r["_rx"] = [re.compile(a, re.IGNORECASE) for a in r.get("aliases") or []]
            rows.append(r)
    if path == BOM_YML:
        _BOM = rows
    return rows


def _norm(text: str) -> str:
    t = plain(text).casefold().replace("×", "x").replace("–", "-").replace("\xa0", " ")
    return re.sub(r"\s+", " ", t).strip()


_FASTENER_RE = re.compile(r"\bm(\d(?:\.\d)?)\s*x\s*(\d+(?:\.\d+)?)\b")
_HEADS = (
    ("shcs", r"\bshcs\b|\bsocket head\b"),
    ("bhcs", r"\bbhcs\b|\bbutton head\b"),
    ("fhcs", r"\bfhcs\b|\bflat head\b|\bcountersunk\b"),
    ("wafer", r"\bwafer\b"),
    ("captive", r"\bcaptive\b"),
    ("selftap", r"\bself[- ]?tapping\b"),
    ("set", r"\bset ?screws?\b|\bgrub\b"),
)


def canon_key(text: str) -> str | None:
    """A spelling-independent key for fasteners and small hardware, so
    `M3×40 SHCS` and `Machine Screw, SHCS, M3x40` meet. None for the rest,
    which resolve through the BOM rows' aliases."""
    t = _norm(text)
    if re.search(r"\binsert tool\b|\bbrass tip\b", t):
        return None
    if re.search(r"heat-?set|\bbrass inserts?\b|\binserts?,? brass\b", t) and re.search(r"\bm3\b|\bm3x", t):
        return "insert m3"
    f = _FASTENER_RE.search(t)
    if f:
        for head, rx in _HEADS:
            if re.search(rx, t):
                return "%s m%sx%s" % (head, f.group(1), f.group(2))
    size = re.search(r"\bm(\d(?:\.\d)?)\b", t)
    if re.search(r"\bt-?nuts?\b", t):
        if size:
            return "tnut-%s m%s" % ("hammer" if "hammer" in t else "rollin", size.group(1))
        return None
    if not size:
        return None
    m = size.group(1)
    if re.search(r"\bknurled\b", t):
        return "knurled m%s" % m
    if re.search(r"\bhex ?nuts?\b|\bnuts?\b", t):
        return "hexnut m%s" % m
    if re.search(r"\block(?:ing)? washers?\b", t):
        return "lockwasher m%s" % m
    if re.search(r"\bwashers?\b", t):
        return "washer m%s" % m
    if re.search(r"\bspacers?\b|\bshims?\b", t):
        return "spacer m%s" % m
    return None


def resolve(name: str, bom: list[dict] | None = None) -> dict | None:
    """The BOM row a Parts item name (count already removed) comes from."""
    bom = load_bom() if bom is None else bom
    key = canon_key(name)
    if key:
        for row in bom:
            if row["_key"] == key:
                return row
    t = _norm(name)
    best, best_len = None, 0
    for row in bom:
        for rx in row["_rx"]:
            m = rx.search(t)
            if m and len(m.group(0)) > best_len:
                best, best_len = row, len(m.group(0))
    return best


def box_label(row: dict) -> str:
    return "%s box%s" % (row["box"], "" if row.get("carton", 1) == 1 else " (carton %d)" % row["carton"])


# --------------------------------------------------------------------------
# one item, one field
# --------------------------------------------------------------------------

# Roles. `staged:` = taken out and set aside (unpacked, inspected, trimmed,
# bagged) but fitted at a later step; `reused:` = fitted earlier, touched again.
# Neither is summed; check 7 checks that a later / an earlier step consumes it.
_ROLE_RE = re.compile(r"^(reused|staged|tool|consumable)\s*:\s*", re.IGNORECASE)
_FROM_RE = re.compile(r"\s+[—–]\s+from\s+(.+?)\s*\.?$", re.IGNORECASE)
_PER_RE = re.compile(r"\b(?:per|each)\b", re.IGNORECASE)
_STEP_REF_RE = re.compile(r"\bSteps?\s+[A-Za-z]?\d+[A-Za-z]?\.\d+\b")


@dataclass
class PartItem:
    text: str                 # as written
    name: str                 # prefix, `— from`, count removed
    count: int | None
    role: str                 # part | reused | tool | consumable
    source: str | None        # `— from <source>`, by hand
    printed: bool
    bins: list[str]
    bom: dict | None
    form: str                 # line | list

    @property
    def body(self) -> str:
        """The text without its role prefix and `— from` tail (count kept)."""
        t = _ROLE_RE.sub("", self.text, count=1)
        return _FROM_RE.sub("", t).strip()

    @property
    def note(self) -> str | None:
        """Where it comes from, for the muted suffix on the step list."""
        if self.role == "reused":
            return "already on the bench"
        if self.role == "staged":
            return "set out now, fitted later"
        if self.role in ("tool", "consumable"):
            return self.role
        if self.source:
            return self.source
        if self.printed:
            return ("bin " + ", ".join(self.bins)) if self.bins else "printed"
        if self.bom:
            return box_label(self.bom)
        return None

    @property
    def group(self) -> tuple:
        """(sort key, heading) of the Gather group this item lands in."""
        if self.role == "reused":
            return ((6,), "Already on the bench")
        if self.role == "staged":
            return ((5, 1), "Set out for later steps")
        if self.role in ("tool", "consumable"):
            return ((5,), "Tools and consumables")
        if self.printed:
            return ((4,), "Printed parts")
        if self.source:
            return ((2, self.source.casefold()), self.source[:1].upper() + self.source[1:])
        if self.bom:
            return ((1, self.bom.get("carton", 1), _box_order(self.bom["box"])), box_label(self.bom))
        return ((3,), "Other hardware")

    @property
    def kit_key(self) -> int | None:
        """BOM row number when this item consumes kit stock (reconciled by check 7)."""
        if self.role == "part" and not self.source and not self.printed and self.bom:
            return self.bom["_n"]
        return None


def _box_order(box: str) -> int:
    for row in load_bom():
        if row["box"] == box:
            return row["_n"]
    return 10 ** 6


def parse_item(text: str, form: str = "list") -> PartItem:
    text = text.strip()
    role_m = _ROLE_RE.match(text)
    role = role_m.group(1).lower() if role_m else "part"
    rest = text[role_m.end():] if role_m else text
    src_m = _FROM_RE.search(rest)
    source = src_m.group(1).strip() if src_m else None
    if src_m:
        rest = rest[:src_m.start()]
    count, name = count_of(rest)
    printed, bins = printed_info(name)
    bom = None if printed else resolve(name)
    return PartItem(text=text, name=name, count=count, role=role, source=source,
                    printed=printed, bins=bins, bom=bom, form=form)


@dataclass
class Field:
    form: str                         # none | line | list
    items: list[PartItem]
    raw: list[str]                    # the field's lines
    blank_after_label: bool = True    # list form: blank line after `**Parts:**`
    stray: list[str] = field(default_factory=list)   # list form: non-bullet text


def is_label(line: str) -> bool:
    return bool(PARTS_RE.match(_logical(line)))


def parse_field(lines: list[str]) -> Field:
    """A `**Parts:**` field (its label line plus, for the list form, the list)."""
    head = PARTS_RE.match(_logical(lines[0]))
    body = head.group(1).strip() if head else ""
    if body:
        # Single-line form: continuation lines of the paragraph join the label.
        joined = " ".join(l.strip() for l in lines)
        joined = _logical(joined)
        low = plain(PARTS_RE.match(joined).group(1)).strip().rstrip(".").lower()
        if low in _NONE_WORDS:
            return Field("none", [], list(lines))
        return Field("line", [parse_item(i, "line") for i in parts_items(joined)], list(lines))
    items: list[str] = []
    stray: list[str] = []
    blank = False
    seen_item = False
    for line in lines[1:]:
        s = _logical(line)
        if not s.strip():
            if not seen_item:
                blank = True
            continue
        m = _LIST_ITEM_RE.match(s)
        if m and not s.startswith("    "):
            items.append(m.group(1).strip())
            seen_item = True
        elif seen_item and (s.startswith("  ") or not _LIST_ITEM_RE.match(s)) and items:
            items[-1] += " " + s.strip()
        else:
            stray.append(s.strip())
    parsed = [parse_item(i, "list") for i in items
              if plain(i).strip().rstrip(".").lower() not in _NONE_WORDS]
    if not items and not stray:
        return Field("none", [], list(lines))
    return Field("list", parsed, list(lines), blank_after_label=blank or not items, stray=stray)


def absorb_list(lines: list[str], end: int, is_boundary) -> int:
    """End index of a list-form Parts field whose label line ends at `end`:
    at most one blank line, then the bullets (loose or tight, with indented
    continuation lines), up to a blank line not followed by another bullet or
    up to any `is_boundary` line."""
    k = end
    while k < len(lines) and not lines[k].strip():
        k += 1
    if k >= len(lines) or k - end > 1 or not _LIST_ITEM_RE.match(_logical(lines[k])):
        return end
    last = k
    while k < len(lines):
        if not lines[k].strip():
            nxt = k + 1
            while nxt < len(lines) and not lines[nxt].strip():
                nxt += 1
            if (nxt < len(lines) and not is_boundary(lines[nxt])
                    and _LIST_ITEM_RE.match(_logical(lines[nxt]))):
                k = nxt
                continue
            break
        if is_boundary(lines[k]):
            break
        k += 1
        last = k
    return last


def grouped_tally(items: list[Tally], item: PartItem) -> None:
    """Grouped Gather tally: merge by BOM row (so spellings meet), else by name;
    `reused:` and `staged:` items are listed once and never summed."""
    group = item.group
    ident = ("bom", item.bom["_n"]) if (item.bom and not item.printed and not item.source) else ("name", merge_key(item.name))
    key = "%r|%r" % (group[0], ident)
    counted = item.role not in ("reused", "staged")
    display = item.name if counted else item.body
    if not merge_key(display):
        return
    note = ("bin " + ", ".join(item.bins)) if (item.printed and item.bins) else ""
    for existing in items:
        if existing.key == key:
            if counted:
                existing.count += item.count if item.count is not None else 1
                existing.explicit = existing.explicit or item.count is not None
            for b in item.bins:
                if b not in existing.bins:
                    existing.bins.append(b)
            if existing.bins:
                existing.note = "bin " + ", ".join(existing.bins)
            return
    items.append(Tally(display=display, count=(item.count or 1) if counted else 0,
                       explicit=counted and item.count is not None, bins=list(item.bins),
                       key=key, group=group, note=note, counted=counted))


def groups(items: list[Tally]) -> list[tuple[str, list[Tally]]]:
    """Tallies grouped for the Gather block: kit boxes in BOM order, sources
    set by hand, other hardware, printed parts (by bin), tools and
    consumables, then what is already on the bench."""
    out: dict[tuple, tuple[str, list[Tally]]] = {}
    for t in items:
        out.setdefault(t.group[0], (t.group[1], []))[1].append(t)
    result = []
    for order in sorted(out):
        heading, members = out[order]
        if order == (4,):
            members = sorted(members, key=lambda t: (t.bins[:1] or ["~"])[0])
        result.append((heading, members))
    return result


def tally_line(t: Tally) -> str:
    if not t.counted:
        return t.display
    count = " ×%d" % t.count if (t.explicit or t.count > 1) else ""
    return "%s%s" % (t.display, count)


# --------------------------------------------------------------------------
# chapter scan for the lint checks (6 grammar, 7 hardware reconciliation)
# --------------------------------------------------------------------------

_FENCE_RE = re.compile(r"^\s{0,3}(`{3,}|~{3,})")
_STEP_HEAD_RE = re.compile(r"^#{2,3}\s*Step\s+([A-Za-z]?\d+[A-Za-z]?\.\d+)\b")
_ANY_HEAD_RE = re.compile(r"^#{1,6}\s")
_HR_RE = re.compile(r"^(?:-{3,}|\*{3,}|_{3,})\s*$")
_OTHER_MARKER_RE = re.compile(
    r"^(?:\*{0,2}(?:Do|Check|Tip|Helper|What you're looking at):|⚠|Pause:\s|Source:\s|!\[)")
ASSEMBLY_RE = re.compile(r"^\d\d[a-z]?-.+\.md$")
_META = {"00-index.md", "00-tonight.md", "CONVENTIONS.md"}


def _boundary(line: str) -> bool:
    s = _logical(line)
    return bool(_ANY_HEAD_RE.match(s) or _HR_RE.match(s) or _FENCE_RE.match(s)
                or _OTHER_MARKER_RE.match(s.strip()) or is_label(s))


def step_fields(text: str) -> list[tuple[str, int, Field]]:
    """(step id, 1-based line of the label, Field) for every Parts field in a
    step of a chapter's markdown."""
    lines = text.split("\n")
    out, fence, step = [], None, None
    i = 0
    while i < len(lines):
        line = lines[i]
        m = _FENCE_RE.match(line)
        if m:
            token = m.group(1)[0] * 3
            fence = None if fence and line.strip().startswith(fence) else (fence or token)
            i += 1
            continue
        if fence is not None:
            i += 1
            continue
        if _ANY_HEAD_RE.match(line):
            sm = _STEP_HEAD_RE.match(line)
            step = sm.group(1) if sm else None
            i += 1
            continue
        if step and is_label(line):
            j = i + 1
            while j < len(lines) and lines[j].strip() and not _boundary(lines[j]):
                j += 1
            if not PARTS_RE.match(_logical(line)).group(1).strip():
                j = absorb_list(lines, j, _boundary)
            out.append((step, i + 1, parse_field(lines[i:j])))
            i = j
            continue
        i += 1
    return out


def assembly_chapters() -> list[Path]:
    return [f for f in sorted(MANUAL.glob("*.md"))
            if ASSEMBLY_RE.match(f.name) and f.name not in _META]


def check_grammar(text: str, rel: str) -> list[dict]:
    """Check 6 (warn until wave-4 phase 5): each Parts field is `none` or the
    list form, and each bullet is one counted, sourced, per-step-total item."""
    found: list[dict] = []
    own = load_ownership()

    def add(step, line, kind, item="", detail=""):
        found.append({"check": 6, "file": rel, "line": line, "step": step,
                      "kind": kind, "item": item, "detail": detail})

    for step, line, fld in step_fields(text):
        if fld.form == "none":
            continue
        if fld.form == "line":
            add(step, line, "single-line", detail="%d item(s) on one line; use one bullet per item" % len(fld.items))
        else:
            if not fld.blank_after_label:
                add(step, line, "no-blank-line", detail="put a blank line after **Parts:**")
            for s in fld.stray:
                add(step, line, "stray-text", s)
        for it in fld.items:
            label = plain(it.text)
            if it.role in ("reused", "staged"):
                if _STEP_REF_RE.search(it.text):
                    add(step, line, "%s-xref" % it.role, label,
                        "%s: items never cite step numbers" % it.role)
                continue
            if it.role in ("tool", "consumable"):
                continue
            if it.bom and not it.printed and not it.source and it.bom["_n"] in own.unreconciled:
                add(step, line, "unreconciled-row", label,
                    "%s: prefix `%s:`" % (own.unreconciled[it.bom["_n"]],
                                          "tool" if own.unreconciled[it.bom["_n"]].startswith("tool") else "consumable"))
                continue
            body = it.body
            if (";" in body or "·" in body or re.search(r"\s\+\s", plain(_mask_code(body)[0]))
                    or (len(split_top_level(body, ",")) > 1
                        and sum(count_of(c)[0] is not None for c in split_top_level(body, ",")) > 1)):
                add(step, line, "multi-item", label, "one item per bullet")
            if it.count is None:
                add(step, line, "no-count", label, "give the total count for the whole step (×N)")
            if _PER_RE.search(plain(_mask_code(it.name)[0])):
                add(step, line, "per-unit", label, "per/each goes in Do; Parts counts the step total")
            if not (it.printed or it.source or it.bom):
                add(step, line, "unresolved", label,
                    "not a kit BOM item, a printed STL or `— from <source>`")
    return found


def hardware_rows(text: str) -> list[tuple[int, str, str]]:
    """(line no, name cell, qty cell) of the rows of every table that follows a
    `**Hardware**` label in a chapter."""
    lines = text.split("\n")
    out = []
    i = 0
    while i < len(lines):
        if not lines[i].startswith("**Hardware"):
            i += 1
            continue
        j = i + 1
        while j < len(lines) and not lines[j].strip():
            j += 1
        while j < len(lines) and lines[j].lstrip().startswith("|"):
            cells = [c.strip() for c in lines[j].strip().strip("|").split("|")]
            name = cells[0] if cells else ""
            qty = cells[1] if len(cells) > 1 else ""
            if not re.fullmatch(r":?-{3,}:?", name) and plain(name).lower() not in ("fastener / part", "part", "item"):
                out.append((j + 1, name, qty))
            j += 1
        i = j
    return out


_NON_KIT_ROW_RE = re.compile(r"\bnot the (?:voron|ldo) kit\b|\s[—–]\s+from\s", re.IGNORECASE)


def table_qty(cell: str) -> int | None:
    """The total a Hardware Qty cell leads with: `24`, `60: 24 drives + 36 Z
    rails`, `28 (16 drives + 8 idlers + 4 deck)`. None when it does not lead
    with one (`24 (drives) + 36 (Z rails)`, `2 + 2`, `1 each`, `~35`)."""
    c = plain(cell).strip()
    m = re.match(r"^(\d+)\s*:", c)
    if m:
        return int(m.group(1))
    m = re.match(r"^(\d+)(?=\s|\(|$)", c)
    if not m:
        return None
    rest = c[m.end():].strip()
    if rest.startswith("("):
        depth = 0
        for k, ch in enumerate(rest):
            depth += ch == "("
            depth -= ch == ")"
            if depth == 0:
                rest = rest[k + 1:].strip()
                break
        else:
            return None
    if re.search(r"[+×]|\beach\b|\bx\b", rest):
        return None
    return int(m.group(1))


# --------------------------------------------------------------------------
# ownership: where each kit unit is consumed (scripts/data/hardware-ownership.yml)
# --------------------------------------------------------------------------
#
# The rule (review/2026-09-23-sweep/HARDWARE-OWNERSHIP.md): a kit unit is
# consumed once, at the step that first mounts, fastens, presses, glues,
# solders or plugs it into the machine or a sub-assembly. Earlier steps list it
# `staged:`, later ones `reused:`; neither is summed. Inventory chapters are
# never consumption. A Hardware table counts its chapter's consumption, plus
# the carries the map declares (staged here, fitted in a later chapter).

OWNERSHIP_YML = REPO / "scripts" / "data" / "hardware-ownership.yml"


@dataclass
class Ownership:
    inventory: set[str] = field(default_factory=set)          # chapter ids
    unreconciled: dict[int, str] = field(default_factory=dict)  # BOM row -> reason
    bags: set[int] = field(default_factory=set)
    owners: dict[int, dict[str, int]] = field(default_factory=dict)  # row -> {step: qty}
    notes: dict[int, dict] = field(default_factory=dict)       # row -> {staged, reused, evidence}
    carries: list[dict] = field(default_factory=list)          # {row, qty, staged, consumed, evidence}
    errors: list[str] = field(default_factory=list)


_OWN: Ownership | None = None


def load_ownership(path: Path = OWNERSHIP_YML, bom: list[dict] | None = None,
                   data: dict | None = None) -> Ownership:
    """The ownership map, with items resolved to BOM row numbers. `data`
    (a dict shaped like the YAML) is for tests."""
    global _OWN
    if data is None and bom is None and path == OWNERSHIP_YML and _OWN is not None:
        return _OWN
    from_file = data is None and bom is None and path == OWNERSHIP_YML
    bom = load_bom() if bom is None else bom
    if data is None:
        import yaml

        data = (yaml.safe_load(path.read_text(encoding="utf-8")) or {}) if path.exists() else {}
    by_item = {r["item"]: r["_n"] for r in bom}
    own = Ownership(inventory={str(c) for c in data.get("inventory_chapters") or []})

    def row(item: str, where: str) -> int | None:
        n = by_item.get(item)
        if n is None:
            own.errors.append("%s: %r is not an item of scripts/data/ldo-350-bom.yml" % (where, item))
        return n

    for item, reason in (data.get("unreconciled") or {}).items():
        n = row(item, "unreconciled")
        if n is not None:
            own.unreconciled[n] = str(reason)
    for item in data.get("bags") or []:
        n = row(item, "bags")
        if n is not None:
            own.bags.add(n)
    for o in data.get("owners") or []:
        n = row(o.get("item", ""), "owners")
        if n is None:
            continue
        own.owners[n] = {str(k): int(v) for k, v in (o.get("at") or {}).items()}
        own.notes[n] = {"staged": [str(s) for s in o.get("staged") or []],
                        "reused": [str(s) for s in o.get("reused") or []],
                        "evidence": o.get("evidence", "")}
    for c in data.get("carries") or []:
        n = row(c.get("item", ""), "carries")
        if n is not None:
            own.carries.append({"row": n, "qty": int(c["qty"]), "staged": str(c["staged"]),
                                "consumed": str(c["consumed"]), "evidence": c.get("evidence", "")})
    if from_file:
        _OWN = own
    return own


def chapter_id(rel: str) -> str:
    """`docs/manual/05-gantry.md` -> `05`, `00a-mains-safety.md` -> `00a`."""
    return Path(rel).name.split("-", 1)[0]


@dataclass
class Use:
    """One kit-item mention in a step, in manual order."""
    idx: int          # position in the manual (file order, then line)
    rel: str
    chapter: str
    step: str
    line: int
    row: int
    role: str         # part | staged | reused | inventory
    count: int | None
    text: str


def ledger(docs: list[tuple[str, str]], own: Ownership) -> tuple[list[Use], dict[str, str]]:
    """Every kit-row mention (not printed, not `— from`, not tool/consumable,
    not an unreconciled row) across `docs` in order, and {step id: rel}."""
    uses: list[Use] = []
    where: dict[str, str] = {}
    idx = 0
    for rel, text in docs:
        ch = chapter_id(rel)
        for step, line, fld in step_fields(text):
            where.setdefault(step, rel)
            for it in fld.items:
                if not it.bom or it.printed or it.source or it.role in ("tool", "consumable"):
                    continue
                n = it.bom["_n"]
                if n in own.unreconciled:
                    continue
                role = "inventory" if (ch in own.inventory and it.role == "part") else it.role
                uses.append(Use(idx, rel, ch, step, line, n, role, it.count, plain(it.text)))
                idx += 1
    return uses, where


def _steps_in_order(text: str) -> list[str]:
    return [m.group(1) for m in map(_STEP_HEAD_RE.match, text.split("\n")) if m]


def _steps_in(text: str) -> set[str]:
    return set(_steps_in_order(text))


def check_ownership(docs: list[tuple[str, str]], own: Ownership | None = None,
                    bom: list[dict] | None = None) -> list[dict]:
    """Check 7, cross-chapter part: double counts, fake `reused:`, `staged:`
    with nothing fitting it later, the map's owner steps and carries, and kit-wide
    consumption over the BOM quantity. `docs` = [(rel, text)] in manual order."""
    bom = load_bom() if bom is None else bom
    own = load_ownership() if own is None else own
    by_n = {r["_n"]: r for r in bom}
    uses, where = ledger(docs, own)
    found: list[dict] = []

    def add(u_or_rel, line, kind, item, detail, step=None):
        found.append({"check": 7, "file": u_or_rel, "line": line, "step": step,
                      "kind": kind, "item": item, "detail": detail})

    for e in own.errors:
        add(str(OWNERSHIP_YML.relative_to(REPO)), 0, "map-error", "", e)
    for n, at in own.owners.items():
        for s in list(at) + own.notes.get(n, {}).get("staged", []) + own.notes.get(n, {}).get("reused", []):
            if s not in where and chapter_id_of_step(s) in {chapter_id(r) for r, _ in docs}:
                add(str(OWNERSHIP_YML.relative_to(REPO)), 0, "map-error", by_n[n]["item"],
                    "ownership map names Step %s, which no chapter has" % s)
    for c in own.carries:
        for s in (c["staged"], c["consumed"]):
            if s not in where and chapter_id_of_step(s) in {chapter_id(r) for r, _ in docs}:
                add(str(OWNERSHIP_YML.relative_to(REPO)), 0, "map-error", by_n[c["row"]]["item"],
                    "carry names Step %s, which no chapter has" % s)

    def qty(u: Use) -> int:
        return u.count if u.count is not None else 1

    # Consumption = a counted part. An uncounted mention is check 6's
    # no-count finding and is not summed here either (as in check_reconcile).
    def fits(u: Use) -> bool:
        return u.role == "part" and u.count is not None

    order = {}
    for rel, text in docs:
        for s in _steps_in_order(text):
            order.setdefault(s, len(order))
    consumed_by_step: dict[tuple[int, str], int] = {}
    for u in uses:
        if fits(u):
            consumed_by_step[(u.row, u.step)] = consumed_by_step.get((u.row, u.step), 0) + qty(u)

    # Owned rows: every counted consumption sits at an owner step, and each
    # owner step carries at least its quantity.
    for n, at in own.owners.items():
        item = by_n[n]["item"]
        first_owner = min((order.get(s, 10 ** 9) for s in at), default=None)
        seen: set[str] = set()
        for u in uses:
            if u.row != n or not fits(u) or u.step in at or u.step in seen:
                continue
            seen.add(u.step)
            before = first_owner is None or order.get(u.step, 0) < first_owner
            fix = "staged:" if before else "reused:"
            add(u.rel, u.line, "double-count", item,
                "Step %s lists it as fitted (×%d), but the ownership map fits it at %s — list it as `%s`"
                % (u.step, qty(u), ", ".join("%s ×%d" % kv for kv in at.items()) or "no step (unused)", fix),
                u.step)
        for s, q in at.items():
            got = consumed_by_step.get((n, s), 0)
            if got < q and s in where:
                rel = where[s]
                line = next((l for st, l, _ in step_fields(dict(docs)[rel]) if st == s), 0)
                add(rel, line, "owner-missing", item,
                    "the ownership map fits ×%d here; the step lists ×%d as fitted" % (q, got), s)

    # Carries: staged at the staging step, fitted at the consuming step.
    for c in own.carries:
        item = by_n[c["row"]]["item"]
        st = sum(qty(u) for u in uses if u.row == c["row"] and u.step == c["staged"] and u.role == "staged")
        if st < c["qty"] and c["staged"] in where:
            u0 = next((u for u in uses if u.row == c["row"] and u.step == c["staged"]), None)
            add(where[c["staged"]], u0.line if u0 else 0, "carry-unstaged", item,
                "the ownership map carries ×%d from here to Step %s; list them `staged: … ×%d`"
                % (c["qty"], c["consumed"], c["qty"]), c["staged"])
        got = consumed_by_step.get((c["row"], c["consumed"]), 0)
        if got < c["qty"] and c["consumed"] in where:
            u0 = next((u for u in uses if u.row == c["row"] and u.step == c["consumed"]), None)
            add(where[c["consumed"]], u0.line if u0 else 0, "carry-unfitted", item,
                "the ownership map fits ×%d here (bagged at Step %s); the step lists ×%d as fitted"
                % (c["qty"], c["staged"], got), c["consumed"])

    # `reused:` needs an earlier consumption; `staged:` needs a later one.
    running: dict[int, int] = {}
    total = {}
    for u in uses:
        if fits(u):
            total[u.row] = total.get(u.row, 0) + qty(u)
    for u in uses:
        item = by_n[u.row]["item"]
        if u.role == "reused":
            have = running.get(u.row, 0)
            if have < qty(u):
                add(u.rel, u.line, "fake-reuse", item,
                    "reused: ×%d, but only %d fitted before Step %s — new hardware is a counted part (or `staged:`)"
                    % (qty(u), have, u.step), u.step)
        elif u.role == "staged":
            later = total.get(u.row, 0) - running.get(u.row, 0)
            if later < qty(u):
                add(u.rel, u.line, "staged-unfitted", item,
                    "staged: ×%d, but only %d fitted at or after Step %s" % (qty(u), later, u.step), u.step)
        if fits(u):
            running[u.row] = running.get(u.row, 0) + qty(u)

    # Kit-wide: consumption over the BOM quantity is a double count somewhere.
    running = {}
    flagged: set[int] = set()
    for u in uses:
        if not fits(u) or u.row in own.bags or u.row in own.owners:
            continue
        running[u.row] = running.get(u.row, 0) + qty(u)
        cap = by_n[u.row].get("qty")
        if isinstance(cap, (int, float)) and running[u.row] > cap and u.row not in flagged:
            flagged.add(u.row)
            add(u.rel, u.line, "over-bom", by_n[u.row]["item"],
                "fitted %d by Step %s, the kit BOM has %s — a double count (mark the repeat `reused:`/`staged:`) or a non-kit source (`— from …`)"
                % (running[u.row], u.step, cap), u.step)
    return found


def chapter_id_of_step(step: str) -> str:
    """`06b.13` -> `06`, `05.46` -> `05`: the chapter file a step id lives in."""
    return re.sub(r"(?<=\d\d)[b-z]$", "", step.split(".", 1)[0])


def carry_adjust(text: str, own: Ownership) -> dict[int, int]:
    """{BOM row: table delta} for one chapter: + a carry staged here, − a carry
    consumed here (it came out of the bag in the staging chapter)."""
    steps = _steps_in(text)
    adj: dict[int, int] = {}
    for c in own.carries:
        if c["staged"] in steps:
            adj[c["row"]] = adj.get(c["row"], 0) + c["qty"]
        if c["consumed"] in steps:
            adj[c["row"]] = adj.get(c["row"], 0) - c["qty"]
    return adj


def check_reconcile(text: str, rel: str, bom: list[dict] | None = None,
                    own: Ownership | None = None) -> tuple[list[dict], dict[int, int]]:
    """Check 7, per chapter (warn until wave-4 phase 5): the chapter's
    consumption of each kit item (counted parts; not `reused:`/`staged:`/
    `tool:`/`consumable:`/`— from`, not an inventory chapter, not an
    unreconciled row), plus its carries, equals the Hardware table's total.
    Returns (findings, {BOM row: table total})."""
    bom = load_bom() if bom is None else bom
    own = load_ownership() if own is None else own
    inventory = chapter_id(rel) in own.inventory
    found: list[dict] = []

    def add(line, kind, item="", detail="", step=None):
        found.append({"check": 7, "file": rel, "line": line, "step": step,
                      "kind": kind, "item": item, "detail": detail})

    rows = hardware_rows(text)
    table: dict[int, int] = {}
    table_line: dict[int, int] = {}
    unsure: set[int] = set()
    for line, name, qty in rows:
        pname = plain(name)
        if not pname or pname.startswith(("—", "-")) or _NON_KIT_ROW_RE.search(name):
            continue
        if re.search(r"\s[+/]\s", pname):
            add(line, "table-multi", pname, "one kit item per Hardware row")
            continue
        row = resolve(pname, bom)
        if row is not None and row["_n"] in own.unreconciled:
            continue
        n = table_qty(qty)
        if row is None:
            add(line, "table-unresolved", pname, "Hardware row is not a kit BOM item (add `— from <source>` if it is not kit)")
            continue
        table_line.setdefault(row["_n"], line)
        if n is None:
            unsure.add(row["_n"])
            add(line, "table-qty", pname, "Qty %r does not lead with the total (write `N` or `N: breakdown`)" % plain(qty))
            continue
        table[row["_n"]] = table.get(row["_n"], 0) + n

    steps: dict[int, int] = {}
    first_line: dict[int, tuple[int, str]] = {}
    for step, line, fld in step_fields(text):
        for it in fld.items:
            k = it.kit_key
            if k is None or k in own.unreconciled or inventory:
                continue
            first_line.setdefault(k, (line, step))
            if it.count is None:
                continue
            steps[k] = steps.get(k, 0) + it.count
    adj = carry_adjust(text, own)

    by_n = {r["_n"]: r for r in bom}
    for k in sorted(set(table) | set(steps) | set(first_line) | set(adj)):
        if k in unsure:
            continue
        s, t = steps.get(k, 0) + adj.get(k, 0), table.get(k)
        item = by_n[k]["item"]
        carry = (" (%+d carried, see scripts/data/hardware-ownership.yml)" % adj[k]) if adj.get(k) else ""
        if t is None:
            if not s:
                continue            # uncounted mentions are check 6's no-count
            line, step = first_line.get(k, (0, None))
            add(line, "not-in-table", item, "steps use %d%s, the Hardware table has no row" % (s, carry), step)
        elif s != t:
            add(table_line.get(k, 0), "mismatch", item, "steps total %d%s, Hardware table %d" % (s, carry, t))
    return found, table


def kit_totals(tables: dict[int, int], bom: list[dict] | None = None,
               own: Ownership | None = None) -> list[str]:
    """Informative: Σ chapter Hardware tables against the BOM quantity (bag
    rows, whose quantity counts bags, are skipped)."""
    bom = load_bom() if bom is None else bom
    own = load_ownership() if own is None else own
    lines = []
    for r in bom:
        used = tables.get(r["_n"])
        if used is None or not isinstance(r.get("qty"), (int, float)) or r["_n"] in own.bags:
            continue
        spare = r["qty"] - used
        if spare < 0:
            lines.append("OVER  %-45s tables %d > BOM %s" % (r["item"][:45], used, r["qty"]))
    n = sum(1 for r in bom if r["_n"] in tables)
    lines.append("%d BOM rows appear in chapter Hardware tables; %d over the BOM quantity"
                 % (n, sum(1 for l in lines if l.startswith("OVER"))))
    return lines


def _rel(f: Path) -> str:
    return str(f.relative_to(REPO)) if f.is_relative_to(REPO) else str(f)


def report(files: list[Path] | None = None) -> tuple[list[dict], list[str]]:
    """Checks 6 and 7 over the assembly chapters (or `files`). The
    cross-chapter part of check 7 always reads the whole manual; its findings
    are then kept for `files` only."""
    every = assembly_chapters()
    files = every if files is None else files
    docs = [(_rel(f), f.read_text(encoding="utf-8")) for f in every]
    texts = dict(docs)
    picked = {_rel(f) for f in files}
    findings: list[dict] = []
    totals: dict[int, int] = {}
    for f in files:
        rel = _rel(f)
        text = texts.get(rel) or f.read_text(encoding="utf-8")
        findings += check_grammar(text, rel)
        found, table = check_reconcile(text, rel)
        findings += found
        for k, v in table.items():
            totals[k] = totals.get(k, 0) + v
    for x in check_ownership(docs):
        if x["file"] in picked or (x["kind"] == "map-error" and files == every):
            findings.append(x)
    info = kit_totals(totals) if files == every else []
    return findings, info


def print_ledger(pattern: str = "") -> None:
    """`--ledger [pattern]`: every mention of each matching kit row, in manual
    order, with its role, count and the step's Source line (per-step evidence)."""
    own = load_ownership()
    docs = [(_rel(f), f.read_text(encoding="utf-8")) for f in assembly_chapters()]
    sources: dict[str, str] = {}
    for rel, text in docs:
        step = None
        for line in text.split("\n"):
            m = _STEP_HEAD_RE.match(line)
            if m:
                step = m.group(1)
            elif _ANY_HEAD_RE.match(line):
                step = None
            elif step and line.startswith("Source:") and step not in sources:
                sources[step] = re.sub(r"\]\([^)]*\)", "]", line[7:].strip())[:110]
    uses, _ = ledger(docs, own)
    bom = {r["_n"]: r for r in load_bom()}
    rx = re.compile(pattern, re.IGNORECASE) if pattern else None
    for n in sorted({u.row for u in uses}):
        item = bom[n]["item"]
        if rx and not rx.search(item):
            continue
        fitted = sum(u.count for u in uses if u.row == n and u.role == "part" and u.count is not None)
        tag = " [owned]" if n in own.owners else (" [bag]" if n in own.bags else "")
        print("%s — BOM %s, fitted %d%s" % (item, bom[n].get("qty"), fitted, tag))
        for u in uses:
            if u.row == n:
                print("   %-7s %-9s %-4s %s  ⟨%s⟩" % (u.step, u.role, u.count if u.count is not None else "-",
                                                  u.text[:60], sources.get(u.step, "no Source line")))


# --------------------------------------------------------------------------
# selftest
# --------------------------------------------------------------------------


def _selftest() -> int:
    load_part_thumbs()
    fails: list[str] = []

    def eq(label, got, want):
        if got != want:
            fails.append("%s: got %r, want %r" % (label, got, want))

    # Canonical keys meet across spellings.
    for a, b in [("M3×40 SHCS", "Machine Screw, SHCS, M3x40"),
                 ("M5 roll-in T-nut, 2020", "T-nut, Roll-in, 2020, M5"),
                 ("M3 hammerhead T-nut, 2020", "T-nut, Hammer Head, 2020, M3"),
                 ("M3×5×4 brass heat-set insert", "Heatset Insert, Brass, M3x5x4"),
                 ("M5 precision spacer, 1 mm", "Precision Spacer, M5, 1mm"),
                 ("M5 hexnut", "Hexnut, M5"), ("M5 nut", "Hexnut, M5"),
                 ("M4×4 set screw, pre-applied threadlocker", "Set Screw, M4x4, Pre-applied Threadlocker"),
                 ("M2×10 self-tapping", "Self-tapping Screw, M2x10")]:
        eq("canon %s" % a, canon_key(a), canon_key(b))
        if canon_key(a) is None:
            fails.append("canon %s: None" % a)
    # Aliases resolve to the right box.
    for name, item in [("C13 power cord", "C13 Power Cord 1.5 meter"),
                       ("E extrusion (XY bridge)", "LDO-V2.4F350-2020T-340E"),
                       ("MGN9H 400 mm rail", "Linear Rail Stainless Steel, LDO-SLR9H-400Z0"),
                       ("MGN12H rail + carriage", "Linear Rail Stainless Steel, LDO-SLR12H-400Z1"),
                       ("GT2 20T 9 mm idler, 5 mm ID", "Idler, 2GT, 20T, (5mm ID 9mm W)"),
                       ("GT2 16T pulley, 5 mm ID 6 mm W", "Pulley, 2GT, 16T, (5mm ID 6mm W)"),
                       ("NEMA17 Z motor", "LDO-42STH48-2004AC(VRN) Z Motor"),
                       ("Deck panel, acrylic black 469×469", "Deck Panel, Acrylic, Black, 469x469x3mm"),
                       ("Magnetic Pad 2.4-350", "Magnetic Pad 2.4-350")]:
        row = resolve(name)
        eq("resolve %s" % name, row and row["item"], item)
    eq("box label", box_label(resolve("M3×40 SHCS")), "Fasteners, Tools & Misc box")
    eq("carton 2 label", box_label(resolve("deck panel")), "Panel Kit box (carton 2)")

    # Both grammars parse.
    f = parse_field(["**Parts:** none."])
    eq("none", (f.form, f.items), ("none", []))
    f = parse_field(["**Parts:** `z_drive_main_a` or `_b` ×1 (side inserts fitted, Step 02.04); M3×40 SHCS ×6."])
    eq("line form", [(i.name, i.count) for i in f.items],
       [("`z_drive_main_a` or `_b` (side inserts fitted, Step 02.04)", 1), ("M3×40 SHCS", 6)])
    eq("line form printed", f.items[0].printed, True)

    # G2-03: 02.22–02.26 builds four drives; the list form carries step totals,
    # and a per-unit count is a finding.
    g203 = """### Step 02.24 — Close the drives

**Parts:**

- M3×40 SHCS ×24
- M5 hexnut ×4
- `[a]_z_drive_baseplate_a` ×2
- `[a]_z_drive_baseplate_b` ×2
- reused: the four belted shaft assemblies
- tool: 2.5 mm hex key
- M3 heat-set insert ×7 — from KADRICK kit

**Check:** all four close.

### Step 02.25 — Per-unit counting (the G2-03 bug)

**Parts:**
- M3×8 SHCS ×3 per drive
"""
    fields = step_fields(g203)
    eq("G2-03 fields", [(s, fl.form) for s, _, fl in fields], [("02.24", "list"), ("02.25", "list")])
    its = fields[0][2].items
    eq("G2-03 counts", [(i.role, i.count) for i in its],
       [("part", 24), ("part", 4), ("part", 2), ("part", 2), ("reused", None), ("tool", None), ("part", 7)])
    eq("G2-03 notes", [i.note for i in its],
       ["Fasteners, Tools & Misc box", "Fasteners, Tools & Misc box",
        "bin " + ", ".join(its[2].bins) if its[2].bins else "printed",
        "bin " + ", ".join(its[3].bins) if its[3].bins else "printed",
        "already on the bench", "tool", "KADRICK kit"])
    eq("G2-03 printed", [its[2].printed, its[3].printed], [True, True])
    eq("G2-03 blank line", [fl.blank_after_label for _, _, fl in fields], [True, False])
    kinds = sorted({(x["step"], x["kind"]) for x in check_grammar(g203, "t.md")})
    eq("G2-03 grammar", kinds, [("02.25", "no-blank-line"), ("02.25", "per-unit")])
    tallies: list[Tally] = []
    for _, _, fl in fields:
        for it in fl.items:
            grouped_tally(tallies, it)
    eq("G2-03 groups", [h for h, _ in groups(tallies)],
       ["Fasteners, Tools & Misc box", "KADRICK kit", "Printed parts",
        "Tools and consumables", "Already on the bench"])
    eq("G2-03 fastener totals", [tally_line(t) for t in groups(tallies)[0][1]],
       ["M3×40 SHCS ×24", "M5 hexnut ×4", "M3×8 SHCS per drive ×3"])
    # A legacy line in the same chapter is still reconciled against the table:
    # the old 02.22–02.26 said M3×40 ×6 for a step that needs 24.
    legacy = """**Hardware** — chapter totals.

| Fastener / part | Qty |
|---|---:|
| M3×40 SHCS | 24 |
| M3×8 SHCS | 24 (drives) + 36 (Z rails) |

### Step 02.23 — Retainer

**Parts:** `z_drive_main_a` or `_b` ×1; M3×40 SHCS ×6.
"""
    found, _ = check_reconcile(legacy, "t.md")
    eq("G2-03 reconcile", sorted((x["kind"], x["detail"]) for x in found),
       [("mismatch", "steps total 6, Hardware table 24"),
        ("table-qty", "Qty '24 (drives) + 36 (Z rails)' does not lead with the total (write `N` or `N: breakdown`)")])
    eq("table qty forms", [table_qty(c) for c in ["24", "60: 24 drives + 36 Z rails", "8 (drives)",
                                                   "24 (drives) + 36 (Z rails)", "~35", "**0**",
                                                   "12 (idlers: 2 mounting + 1 axle each)", "2 + 2",
                                                   "1 each", "4 × ~1400 mm"]],
       [24, 60, 8, None, None, 0, 12, None, None, None])

    # G3-06: comma lists. The single-line parser splits only when every chunk
    # has a count; in list form a comma bullet is a multi-item finding, and the
    # same extrusion under two spellings merges by BOM row.
    eq("G3-06 line split", parts_items("**Parts:** C extrusion ×1, M3 T-nut ×10."),
       ["C extrusion ×1", "M3 T-nut ×10"])
    eq("G3-06 line no split", parts_items("**Parts:** C extrusion, D extrusion ×1, E extrusion ×1."),
       ["C extrusion, D extrusion ×1, E extrusion ×1"])
    g306 = """### Step 05.5 — E

**Parts:**

- C extrusion ×2, D extrusion ×1
- E extrusion ×1

### Step 05.6 — E again

**Parts:**

- E extrusion (XY bridge) ×1
"""
    eq("G3-06 grammar", [(x["step"], x["kind"]) for x in check_grammar(g306, "t.md")],
       [("05.5", "multi-item")])
    tallies = []
    for _, _, fl in step_fields(g306):
        for it in fl.items:
            grouped_tally(tallies, it)
    eq("G3-06 merge", [tally_line(t) for _, ts in groups(tallies) for t in ts],
       ["C extrusion, D extrusion ×1 ×2", "E extrusion ×2"])

    # G3-16: a reused part is listed, never summed, and never merged with the
    # fresh one; it may not cite a step.
    g316 = """### Step 04.7 — Idler

**Parts:**

- M5×40 SHCS ×1
- reused: the same M5×40 SHCS
- reused: the A motor with its pulley, from Step 04.3
"""
    tallies = []
    for _, _, fl in step_fields(g316):
        for it in fl.items:
            grouped_tally(tallies, it)
    eq("G3-16 gather", [(h, [tally_line(t) for t in ts]) for h, ts in groups(tallies)],
       [("Fasteners, Tools & Misc box", ["M5×40 SHCS ×1"]),
        ("Already on the bench", ["the same M5×40 SHCS", "the A motor with its pulley, from Step 04.3"])])
    eq("G3-16 grammar", [x["kind"] for x in check_grammar(g316, "t.md")], ["reused-xref"])
    found, _ = check_reconcile("**Hardware**\n\n| Fastener / part | Qty |\n|---|---:|\n| M5×40 SHCS | 1 |\n\n" + g316, "t.md")
    eq("G3-16 reconcile", found, [])

    # G6-24: prose rows. The old line turns prose into items; in list form a
    # tool is gathered apart and prose is a finding.
    eq("G6-24 legacy", [i.name for i in parse_field(["**Parts:** C13 power cord. No meter ×1."]).items],
       ["C13 power cord. No meter"])
    g624 = """### Step 10.17 — Mains check

**Parts:**

- C13 power cord ×1
- tool: multimeter
- this step only confirms it
"""
    kinds = [(x["kind"], x["item"]) for x in check_grammar(g624, "t.md")]
    eq("G6-24 grammar", kinds, [("no-count", "this step only confirms it"),
                                ("unresolved", "this step only confirms it")])
    its = step_fields(g624)[0][2].items
    eq("G6-24 sources", [i.note for i in its], ["Other box", "tool", None])

    # Hardware ownership (check 7 reconciles consumption, not listing).
    own = load_ownership(data={
        "inventory_chapters": ["00"],
        "unreconciled": {"Zip Ties, 3x150mm": "consumable"},
        "owners": [{"item": "Genuine Wago 221-415 Splicing Connector", "at": {"09.13": 3}}],
        "carries": [{"item": "Machine Screw, SHCS, M3x30", "qty": 2,
                     "staged": "05.46", "consumed": "09.33"}]})
    eq("own map resolves", own.errors, [])
    ch00 = """### Step 00.17 — Unbag the rails

**Parts:**

- MGN9H 400 mm rail ×6
- Genuine WAGO 221-415 (5-way) ×3
"""
    ch05 = """**Hardware**

| Fastener / part | Qty |
|---|---:|
| M3×30 SHCS | 2: bagged with the pod for Ch 09 |

### Step 05.46 — Bag what belongs to later chapters

**Parts:**

- staged: M3×30 SHCS ×2
"""
    ch09 = """**Hardware**

| Fastener / part | Qty |
|---|---:|
| WAGO 221-415 (5-way) | 3 |
| M3×30 SHCS | 0: bagged at Step 05.46 |

### Step 09.13 — WAGO mount

**Parts:**

- WAGO 221-415 (5-way) ×3
- zip ties ×4

### Step 09.33 — Pod

**Parts:**

- M3×30 SHCS ×2
"""
    ch10 = """**Hardware**

| Fastener / part | Qty |
|---|---:|
| WAGO 221-415 (5-way) | 3 |

### Step 10.7 — Wire the WAGOs

**Parts:**

- WAGO 221-415 (5-way) ×3
"""
    ch10_ok = """### Step 10.7 — Wire the WAGOs

**Parts:**

- reused: the three WAGO 221-415 (5-way) blocks
"""
    ch08_fake = """### Step 08.9 — Pre-wire

**Parts:**

- reused: WAGO 221-415 (5-way) ×3
"""
    ch09_fake = ch09.replace("- M3×30 SHCS ×2", "- reused: M3×30 SHCS ×2")

    def kinds(docs):
        out = []
        for rel, text in docs:
            out += [(x["step"], x["kind"]) for x in check_reconcile(text, rel, own=own)[0]]
        out += [(x["step"], x["kind"]) for x in check_ownership(docs, own=own)]
        return sorted(out, key=str)

    good = [("t/00-a.md", ch00), ("t/05-a.md", ch05), ("t/09-a.md", ch09), ("t/10-a.md", ch10_ok)]
    # Cross-chapter item accepted: staged + carried in Ch 05, fitted at 09.33,
    # Ch 09's table leaves it out (`0:`); Ch 00 inventory never counts; the
    # WAGOs are fitted once and reused in Ch 10; zip ties are never reconciled.
    eq("own accepted", kinds(good), [])
    # Double count rejected: Ch 10 lists the same three WAGOs as fitted again.
    eq("own double count", kinds(good[:3] + [("t/10-a.md", ch10)]),
       [("10.7", "double-count")])
    no_owner = load_ownership(data={"inventory_chapters": ["00"]})
    eq("own over-bom", [x["kind"] for x in check_ownership(good[:3] + [("t/10-a.md", ch10)], own=no_owner)],
       ["over-bom"])
    # Fake reuse rejected: `reused:` before anything fitted it, and a carried
    # (only staged) screw passed off as reused.
    eq("own fake reuse", kinds([("t/08-a.md", ch08_fake)] + good),
       [("08.9", "fake-reuse")])
    eq("own fake reuse of a staged screw", kinds(good[:2] + [("t/09-a.md", ch09_fake)] + good[3:]),
       [("05.46", "staged-unfitted"), ("09.33", "carry-unfitted"), ("09.33", "fake-reuse"), (None, "mismatch")])
    # Inventory excluded: without the inventory rule Ch 00's six rails are a
    # consumption with no table row.
    eq("own inventory excluded", [x["kind"] for x in check_reconcile(ch00, "t/00-a.md", own=own)[0]], [])
    eq("own inventory counted without the rule",
       sorted(x["kind"] for x in check_reconcile(ch00, "t/00-a.md", own=no_owner.__class__())[0]),
       ["not-in-table", "not-in-table"])
    # A staged item nothing fits later.
    eq("own staged unfitted", kinds([("t/05-a.md", ch05)]),
       [("05.46", "staged-unfitted")])
    # Count parse: a size then a count.
    eq("count after a size", count_of("heat-set inserts M3×5×4 ×3"), (3, "heat-set inserts M3×5×4"))
    eq("dimension stays", count_of("Ø4.7 × 5 mm"), (None, "Ø4.7 × 5 mm"))
    eq("profile then count", count_of("M3 roll-in T-nut, 2020 ×4"), (4, "M3 roll-in T-nut, 2020"))
    eq("staged role", (parse_item("staged: M3×30 SHCS ×2").role, parse_item("staged: M3×30 SHCS ×2").kit_key), ("staged", None))

    if fails:
        for f_ in fails:
            print("FAIL", f_)
        print("parts selftest: %d failure(s)" % len(fails))
        return 1
    print("parts selftest: ok")
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        sys.exit(_selftest())
    if "--ledger" in sys.argv[1:]:
        load_part_thumbs()
        rest = [a for a in sys.argv[1:] if a != "--ledger"]
        print_ledger(rest[0] if rest else "")
        sys.exit(0)
    print(__doc__)
