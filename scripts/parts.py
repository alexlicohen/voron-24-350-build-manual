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

_ROLE_RE = re.compile(r"^(reused|tool|consumable)\s*:\s*", re.IGNORECASE)
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
    `reused:` items are listed once and never summed."""
    group = item.group
    ident = ("bom", item.bom["_n"]) if (item.bom and not item.printed and not item.source) else ("name", merge_key(item.name))
    key = "%r|%r" % (group[0], ident)
    counted = item.role != "reused"
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
            if it.role == "reused":
                if _STEP_REF_RE.search(it.text):
                    add(step, line, "reused-xref", label, "reused: items never cite step numbers")
                continue
            if it.role in ("tool", "consumable"):
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


def check_reconcile(text: str, rel: str, bom: list[dict] | None = None) -> tuple[list[dict], dict[int, int]]:
    """Check 7 (warn until wave-4 phase 5): per chapter, the step totals of
    each kit item (not `reused:`/`tool:`/`consumable:`/`— from`) equal the
    chapter Hardware table's total. Returns (findings, {BOM row: table total})."""
    bom = load_bom() if bom is None else bom
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
        n = table_qty(qty)
        if row is None:
            add(line, "table-unresolved", pname, "Hardware row is not a kit BOM item")
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
            if k is None:
                continue
            first_line.setdefault(k, (line, step))
            if it.count is None:
                continue
            steps[k] = steps.get(k, 0) + it.count

    by_n = {r["_n"]: r for r in bom}
    for k in sorted(set(table) | set(steps) | set(first_line)):
        if k in unsure:
            continue
        s, t = steps.get(k, 0), table.get(k)
        item = by_n[k]["item"]
        if t is None:
            if not s:
                continue            # uncounted mentions are check 6's no-count
            line, step = first_line[k]
            add(line, "not-in-table", item, "steps use %d, the Hardware table has no row" % s, step)
        elif s != t:
            add(table_line.get(k, 0), "mismatch", item, "steps total %d, Hardware table %d" % (s, t))
    return found, table


def kit_totals(tables: dict[int, int], bom: list[dict] | None = None) -> list[str]:
    """Informative: Σ chapter Hardware tables against the BOM quantity."""
    bom = load_bom() if bom is None else bom
    lines = []
    for r in bom:
        used = tables.get(r["_n"])
        if used is None or not isinstance(r.get("qty"), (int, float)):
            continue
        spare = r["qty"] - used
        if spare < 0:
            lines.append("OVER  %-45s tables %d > BOM %s" % (r["item"][:45], used, r["qty"]))
    n = sum(1 for r in bom if r["_n"] in tables)
    lines.append("%d BOM rows appear in chapter Hardware tables; %d over the BOM quantity"
                 % (n, sum(1 for l in lines if l.startswith("OVER"))))
    return lines


def report(files: list[Path] | None = None) -> tuple[list[dict], list[str]]:
    """Checks 6 and 7 over the assembly chapters (or `files`)."""
    files = assembly_chapters() if files is None else files
    findings: list[dict] = []
    totals: dict[int, int] = {}
    for f in files:
        text = f.read_text(encoding="utf-8")
        rel = str(f.relative_to(REPO)) if f.is_relative_to(REPO) else str(f)
        findings += check_grammar(text, rel)
        found, table = check_reconcile(text, rel)
        findings += found
        for k, v in table.items():
            totals[k] = totals.get(k, 0) + v
    info = kit_totals(totals) if files == assembly_chapters() else []
    return findings, info


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
    print(__doc__)
