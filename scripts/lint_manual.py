#!/usr/bin/env python3
"""Repo lints for the Voron build manual (R6 V4 / V1).

Run after `mkdocs build` (uses the built `site/` output for the raw-callout
check) from the repo root:

    mkdocs build --strict && python3 scripts/lint_manual.py

Checks, each a separate class of defect invisible to `mkdocs build --strict`:
  1. Raw `⚠` / `**Check:**` / `Tip:` text in built HTML outside an
     `.admonition` block (hooks/callouts.py missed it).
  2. `Step NN.M` / `Step BNN.M` references with no matching heading anywhere
     in the manual (a renamed or deleted step, dangling cross-reference).
  3. STL filenames that appear in an assembly-chapter parts table but in no
     print-batch table (docs/manual/print/B*.md) — the part would never get
     printed.
  4. Any Markdown table wider than 7 columns (per R5 F1/F2/F6, iPad-portrait
     readability).

Exits non-zero (and prints every finding) if any check fails. This only
reports — it does not edit chapter content.
"""

import re
import sys
from html.parser import HTMLParser
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DOCS = REPO / "docs"
SITE = REPO / "site"
MANUAL = DOCS / "manual"
PRINT = MANUAL / "print"

_VOID_TAGS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
}

_RAW_MARKER_RE = re.compile(
    r"⚠|\*\*Check:\*\*|(?<![A-Za-z])Tip:|(?<![A-Za-z])Source:|(?<![A-Za-z])Pause:"
)
_STEP_REF_RE = re.compile(r"\bStep\s+([A-Za-z]?\d+[A-Za-z]?\.\d+)\b")
_STEP_HEADING_RE = re.compile(r"^#{2,3}\s*Step\s+([A-Za-z]?\d+[A-Za-z]?\.\d+)\b", re.MULTILINE)
_STEP_HEADING_ANY_RE = re.compile(r"^###\s*Step\s+([A-Za-z]?\d+[A-Za-z]?\.\d+)\b.*$", re.MULTILINE)
_SOURCE_LINE_RE = re.compile(r"^>?\s*Source:")
_GENERATED_OR_META = {"00-index.md", "00-tonight.md", "CONVENTIONS.md"}
_STL_CELL_RE = re.compile(r"`([\w\[\]-]+\.stl)`")
_TABLE_ROW_RE = re.compile(r"^\s*\|(.+)\|\s*$")
_NOT_PRINTED_RE = re.compile(r"not printed|kit-supplied|\bSKIP\b", re.IGNORECASE)


class _OutsideAdmonitionText(HTMLParser):
    """Collects text nodes that are not inside any element carrying the
    `admonition` class (nesting-aware, void-element-aware)."""

    def __init__(self):
        super().__init__()
        self.stack = []  # bool per open element: True if it or an ancestor is an admonition
        self.outside_text = []

    def handle_starttag(self, tag, attrs):
        if tag in _VOID_TAGS:
            return
        classes = dict(attrs).get("class", "").split()
        # "admonition" covers ⚠/Check/Tip/Pause; "src" covers the Source: caption
        # (hooks/callouts.py renders both, so neither is a raw-marker leak).
        is_admonition = "admonition" in classes or "src" in classes
        is_code = tag in ("code", "pre")
        inside = (self.stack[-1] if self.stack else False) or is_admonition or is_code
        self.stack.append(inside)

    def handle_startendtag(self, tag, attrs):
        pass  # self-closed, no text content

    def handle_endtag(self, tag):
        if tag in _VOID_TAGS:
            return
        if self.stack:
            self.stack.pop()

    def handle_data(self, data):
        inside = self.stack[-1] if self.stack else False
        if not inside:
            self.outside_text.append(data)


def check_raw_callouts():
    findings = []
    if not SITE.exists():
        findings.append(f"SKIPPED (raw-callout check): {SITE} not found — run `mkdocs build` first")
        return findings
    for html_file in sorted(SITE.rglob("*.html")):
        parser = _OutsideAdmonitionText()
        parser.feed(html_file.read_text(encoding="utf-8", errors="replace"))
        text = "".join(parser.outside_text)
        for m in _RAW_MARKER_RE.finditer(text):
            snippet = text[max(0, m.start() - 40): m.end() + 40].replace("\n", " ")
            rel = html_file.relative_to(SITE)
            findings.append(f"{rel}: raw {m.group(0)!r} outside an admonition — ...{snippet}...")
    return findings


def _all_manual_files():
    return sorted(MANUAL.rglob("*.md"))


def check_step_refs():
    findings = []
    files = _all_manual_files()
    defined = set()
    for f in files:
        text = f.read_text(encoding="utf-8")
        defined.update(_STEP_HEADING_RE.findall(text))

    for f in files:
        text = f.read_text(encoding="utf-8")
        for m in _STEP_REF_RE.finditer(text):
            step_id = m.group(1)
            if step_id not in defined:
                line_no = text.count("\n", 0, m.start()) + 1
                findings.append(
                    f"{f.relative_to(REPO)}:{line_no}: reference to 'Step {step_id}' "
                    "has no matching heading anywhere in the manual"
                )
    return findings


def check_stl_coverage():
    findings = []
    if not PRINT.exists():
        return [f"SKIPPED (STL coverage check): {PRINT} not found"]

    printed = set()
    for f in sorted(PRINT.glob("B*.md")):
        for line in f.read_text(encoding="utf-8").splitlines():
            if _TABLE_ROW_RE.match(line):
                printed.update(_STL_CELL_RE.findall(line))

    assembly_files = [f for f in MANUAL.glob("*.md") if f.name not in {"00-index.md", "CONVENTIONS.md"}]
    for f in assembly_files:
        for line_no, line in enumerate(f.read_text(encoding="utf-8").splitlines(), start=1):
            if not _TABLE_ROW_RE.match(line):
                continue
            if _NOT_PRINTED_RE.search(line):
                continue
            for stl in _STL_CELL_RE.findall(line):
                if stl not in printed:
                    findings.append(
                        f"{f.relative_to(REPO)}:{line_no}: `{stl}` appears in an assembly "
                        f"table but in no print-batch table ({PRINT.relative_to(REPO)}/B*.md)"
                    )
    return findings


_HEADING_RE = re.compile(r"^#{1,6}\s+(.*)$")


def check_table_width():
    findings = []
    for f in sorted(DOCS.rglob("*.md")):
        under_exempt_heading = False
        for line_no, line in enumerate(f.read_text(encoding="utf-8").splitlines(), start=1):
            heading_m = _HEADING_RE.match(line)
            if heading_m:
                under_exempt_heading = "machine-readable" in heading_m.group(1).lower()
                continue
            m = _TABLE_ROW_RE.match(line)
            if not m:
                continue
            if under_exempt_heading:
                continue
            cells = m.group(1).split("|")
            if len(cells) > 7:
                findings.append(
                    f"{f.relative_to(REPO)}:{line_no}: table row has {len(cells)} columns (> 7)"
                )
    return findings


def check_missing_source():
    """WARN-only (R6 B improvements): every `### Step` in an assembly chapter
    should end with a `Source:` line (docs/manual/CONVENTIONS.md, "Source
    lines and stopping points"). Chapters are being written concurrently, so
    this does not fail CI yet — it only reports a count."""
    findings = []
    assembly_files = [
        f for f in MANUAL.glob("*.md") if f.name != "CONVENTIONS.md" and re.match(r"^\d", f.name)
        if f.name not in _GENERATED_OR_META
    ]
    for f in assembly_files:
        lines = f.read_text(encoding="utf-8").splitlines()
        steps = list(_STEP_HEADING_ANY_RE.finditer("\n".join(lines)))
        text = "\n".join(lines)
        bounds = [m.start() for m in steps] + [len(text)]
        for idx, m in enumerate(steps):
            step_id = m.group(1)
            block = text[m.start(): bounds[idx + 1]]
            if not any(_SOURCE_LINE_RE.match(ln) for ln in block.splitlines()):
                line_no = text.count("\n", 0, m.start()) + 1
                findings.append(
                    f"{f.relative_to(REPO)}:{line_no}: Step {step_id} has no `Source:` line"
                )
    return findings


def main():
    checks = [
        ("Raw callout markers outside admonitions", check_raw_callouts),
        ("Unresolved Step NN.M references", check_step_refs),
        ("STL printed in no batch", check_stl_coverage),
        ("Tables wider than 7 columns", check_table_width),
    ]

    total = 0
    for name, fn in checks:
        findings = fn()
        print(f"\n== {name}: {len(findings)} finding(s) ==")
        for line in findings:
            print(f"  {line}")
        if findings and not findings[0].startswith("SKIPPED"):
            total += len(findings)

    print(f"\n{total} lint finding(s) total.")

    missing_source = check_missing_source()
    print(f"\n== WARN: Steps missing a `Source:` line: {len(missing_source)} ==")
    for line in missing_source:
        print(f"  WARN: {line}")

    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
