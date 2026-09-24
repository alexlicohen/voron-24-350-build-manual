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

Everything under `docs/manual/steps/` is skipped: it is generated from the
chapters by `scripts/build_steps.py` and carries no independent content.
  3. STL filenames that appear in an assembly-chapter parts table but in no
     print-batch table (docs/manual/print/B*.md) — the part would never get
     printed.
  4. Any Markdown table wider than 7 columns (per R5 F1/F2/F6, iPad-portrait
     readability).
  5. Step word budgets (CONVENTIONS.md § "Action-first steps and word
     budgets", plus the `**Helper:**` rules of § "Helper steps") — opt-in: `--budgets` adds it to the run above, `--budgets-only`
     runs it alone and needs no `site/` (`--json` for one finding per line).

  6. Parts grammar (assembly chapters; scripts/parts.py): each `**Parts:**`
     field is `none` or the one-item-per-bullet list, each item counted with
     the step total, no per/each, and sourced (kit BOM row, printed STL or
     `— from <source>`).
  7. Hardware reconciliation: per chapter, the step totals of each kit item
     equal the chapter **Hardware** table's total (Qty cells lead with it).
     Check 7 reconciles against consumption, not listing: inventory chapters
     and `staged:` / `reused:` lines are not summed, and
     scripts/data/hardware-ownership.yml fixes where cross-chapter kit units
     are fitted (double counts, fake `reused:`, carries, over-BOM).
     6 and 7 FAIL the default run (wave-4 phase 5, `PARTS_CHECKS_FAIL`) for
     the assembly chapters only; print chapters (print/B*.md) keep their
     single-line Load form and are never scanned. `--parts-report [chapter …]`
     lists every finding (`--json` one per line, `--strict` exits 1 on any);
     `--strict-parts --chapters 05,06` gates just those chapters.
  8. Checkpoint reward: every assembly `## Checkpoint` carries a `**Built:**`
     line (FAIL since wave-4 phase 5, `BUILT_REQUIRED`).

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
        if (SITE / "manual" / "steps") in html_file.parents:
            continue  # generated from chapters; the chapter page is checked
        parser = _OutsideAdmonitionText()
        parser.feed(html_file.read_text(encoding="utf-8", errors="replace"))
        text = "".join(parser.outside_text)
        for m in _RAW_MARKER_RE.finditer(text):
            snippet = text[max(0, m.start() - 40): m.end() + 40].replace("\n", " ")
            rel = html_file.relative_to(SITE)
            findings.append(f"{rel}: raw {m.group(0)!r} outside an admonition — ...{snippet}...")
    return findings


# docs/manual/steps/ is generated from the chapters by scripts/build_steps.py
# on every build; the chapters are the source of truth, so every lint below
# runs on them and skips the generated tree.
GENERATED = MANUAL / "steps"


def _is_generated(path):
    return GENERATED in path.parents


def _all_manual_files():
    return sorted(f for f in MANUAL.rglob("*.md") if not _is_generated(f))


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
    for f in sorted(f for f in DOCS.rglob("*.md") if not _is_generated(f)):
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


# --------------------------------------------------------------------------
# 5. step word budgets (docs/manual/CONVENTIONS.md § "Action-first steps and
#    word budgets"). On by default since the 2026-09-06 rewrite pass;
#    `--no-budgets` drops it, `--budgets-only` runs just this check (no `site/`
#    needed) and prints one JSON finding per line with `--json`.
# --------------------------------------------------------------------------

_BUDGETS = {"Do": 40, "Check": 25, "description": 45, "Tip": 30, "⚠": 60, "Helper": 20}
_XREF_LIMIT = 1
_CANONICAL_PARENS = ("(verify on bench)", "(not specified — snug)")

_B_STEP_HEAD_RE = re.compile(r"^#{2,3}\s*Step\s+([A-Za-z]?\d+[A-Za-z]?\.\d+)\b")
_B_ANY_HEAD_RE = re.compile(r"^#{1,6}\s")
_B_FENCE_RE = re.compile(r"^\s{0,3}(`{3,}|~{3,})")
_B_BQ_RE = re.compile(r"^>\s?")
_B_IMAGE_RE = re.compile(r"^!\[[^\]]*\]\([^)]*\)(?:\s*\{[^}]*\})?\s*$")
_B_HR_RE = re.compile(r"^(?:-{3,}|\*{3,}|_{3,})\s*$")
_B_LIST_RE = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s")
_B_XREF_RE = re.compile(r"\bSteps?\s+[A-Za-z]?\d+[A-Za-z]?\.\d+\b")
_B_PAREN_RE = re.compile(r"\([^)]*\)")
# Field name -> the marker that opens it. Order matters: first match wins.
_B_MARKERS = (
    ("Do", re.compile(r"^\*{0,2}Do:\*{0,2}(?:\s|$)")),
    ("Check", re.compile(r"^\*{0,2}Check:\*{0,2}(?:\s|$)")),
    ("Tip", re.compile(r"^\*{0,2}Tip:\*{0,2}(?:\s|$)")),
    ("⚠", re.compile(r"^⚠")),
    ("description", re.compile(r"^\*{0,2}What you're looking at:\*{0,2}")),
    ("Helper", re.compile(r"^\*{0,2}Helper:\*{0,2}(?:\s|$)")),
    ("Parts", re.compile(r"^\*\*Parts:\*\*")),
    ("Pause", re.compile(r"^Pause:\s")),
    ("Source", re.compile(r"^Source:\s")),
    # A step's `**Next:** [..](..)` override (build_steps.py): navigation, like
    # Source, so its link is not one of the step's cross-references.
    ("Next", re.compile(r"^\*\*Next:\*\*\s")),
)
_B_LABEL_RE = re.compile(
    r"^\s*(?:>\s?)?(?:⚠\s*)?"
    r"(?:\*{0,2}(?:Do|Check|Tip|Helper|What you're looking at):\*{0,2})?\s*"
)


def _b_logical(line):
    return _B_BQ_RE.sub("", line, count=1)


def _b_marker(line):
    if _B_IMAGE_RE.match(line.strip()):
        return "image"
    s = _b_logical(line)
    for name, rx in _B_MARKERS:
        if rx.match(s):
            return name
    return None


def _b_boundary(line):
    s = _b_logical(line)
    if _B_ANY_HEAD_RE.match(s) or _B_HR_RE.match(s) or _B_FENCE_RE.match(s):
        return True
    return _b_marker(line) is not None


def _b_run(lines, i):
    """End index (exclusive) of a marker line's logical body — the same
    run-to-a-blank-line rule hooks/callouts.py and build_steps.py use."""
    j = i + 1
    while j < len(lines) and lines[j].strip() and not _b_boundary(lines[j]):
        j += 1
    return j


def _b_absorb_list(lines, end):
    """A list directly under a Do line is part of the Do (the house form for a
    multi-action step is a numbered list of <= 3 imperatives)."""
    k = end
    while k < len(lines) and not lines[k].strip():
        k += 1
    if k >= len(lines) or k - end > 1 or not _B_LIST_RE.match(lines[k]):
        return end
    last = k
    while k < len(lines):
        if not lines[k].strip():
            nxt = k + 1
            while nxt < len(lines) and not lines[nxt].strip():
                nxt += 1
            if (nxt < len(lines) and not _b_boundary(lines[nxt])
                    and (_B_LIST_RE.match(lines[nxt]) or lines[nxt].startswith("  "))):
                k = nxt
                continue
            break
        if _b_boundary(lines[k]):
            break
        k += 1
        last = k
    return last


def _b_text(lines):
    """Countable text: no fenced code, no image lines, no inline code spans,
    no link URLs (the link text stays), no marker label."""
    kept, fence = [], None
    for line in lines:
        m = _B_FENCE_RE.match(line)
        if m:
            token = m.group(1)[0] * 3
            fence = None if fence and line.strip().startswith(fence) else (fence or token)
            continue
        if fence is not None or _B_IMAGE_RE.match(line.strip()):
            continue
        kept.append(_b_logical(line))
    text = "\n".join(kept)
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", text)      # inline images
    text = re.sub(r"`[^`]*`", " ", text)                    # inline code spans
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)    # link text, URL dropped
    return _B_LABEL_RE.sub("", text, count=1)


def _b_checkable(text):
    """Text for the em-dash / parenthetical rules: the two canonical markers
    are allowed, so they are removed before either rule looks at it."""
    for canon in _CANONICAL_PARENS:
        text = text.replace(canon, " ")
    return text


def _b_step_blocks(path):
    """(step_id, heading line no, body lines, body start line no) per step."""
    lines = path.read_text(encoding="utf-8").splitlines()
    fence, heads = None, []
    for n, line in enumerate(lines):
        m = _B_FENCE_RE.match(line)
        if m:
            token = m.group(1)[0] * 3
            fence = None if fence and line.strip().startswith(fence) else (fence or token)
            continue
        if fence is not None:
            continue
        if _B_ANY_HEAD_RE.match(line) and re.match(r"^#{2,3}\s", line):
            heads.append(n)
    out = []
    for idx, n in enumerate(heads):
        m = _B_STEP_HEAD_RE.match(lines[n])
        if not m:
            continue
        end = heads[idx + 1] if idx + 1 < len(heads) else len(lines)
        out.append((m.group(1), n + 1, lines[n + 1:end], n + 2))
    return out


def check_step_budgets():
    findings = []
    files = [f for f in sorted(MANUAL.glob("*.md")) if f.name not in _GENERATED_OR_META]
    if PRINT.exists():
        files += [f for f in sorted(PRINT.glob("*.md")) if f.name not in _GENERATED_OR_META]

    for path in files:
        rel = path.relative_to(REPO)
        for step_id, head_no, body, body_start in _b_step_blocks(path):
            def add(line_no, field, kind, words=None, limit=None):
                findings.append({"file": str(rel), "line": line_no, "step": step_id,
                                 "field": field, "words": words, "limit": limit,
                                 "kind": kind})

            xrefs, i, prev_field = 0, 0, None
            while i < len(body):
                line = body[i]
                if not line.strip():
                    i += 1
                    continue
                field = _b_marker(line)
                if field is None or field == "image":
                    xrefs += len(_B_XREF_RE.findall(line))
                    i += 1
                    continue
                end = _b_run(body, i)
                if field == "Do":
                    end = _b_absorb_list(body, end)
                run = body[i:end]
                line_no = body_start + i
                if field not in ("Pause", "Source", "Next"):
                    xrefs += sum(len(_B_XREF_RE.findall(l)) for l in run)
                if field == "Helper" and prev_field != "Check":
                    add(line_no, "Helper", "helper-position")
                prev_field = field
                if field in _BUDGETS:
                    text = _b_text(run)
                    words = len(text.split())
                    limit = _BUDGETS[field]
                    if words > limit:
                        add(line_no, field, "words", words, limit)
                    if field in ("Do", "Check", "description", "Helper"):
                        checkable = _b_checkable(text)
                        if "—" in checkable:
                            add(line_no, field, "em-dash")
                        if _B_PAREN_RE.search(checkable):
                            add(line_no, field, "parenthetical")
                i = end
            if xrefs > _XREF_LIMIT:
                add(head_no, "cross-reference", "cross-reference", xrefs, _XREF_LIMIT)
    return findings


def _budget_line(f):
    if f["kind"] == "words":
        detail = "%s %d/%d words" % (f["field"], f["words"], f["limit"])
    elif f["kind"] == "cross-reference":
        detail = "%d cross-references" % f["words"]
    elif f["kind"] == "helper-position":
        detail = "Helper: does not follow Check:"
    else:
        detail = "%s in %s" % (f["kind"], f["field"])
    return "%s:%d  Step %s  %s" % (f["file"], f["line"], f["step"], detail)


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


BUILT_REQUIRED = True    # wave-4 phase 5: every assembly Checkpoint has one (FAIL)
_CHECKPOINT_H2_RE = re.compile(r"^##\s+Checkpoint\b(.*)$")
_BUILT_LINE_RE = re.compile(r"^\*\*Built:\*\*\s*\S")


def check_checkpoint_built():
    """Every assembly `## Checkpoint` section carries one `**Built:** <X>` line,
    the caption of the reward scripts/build_steps.py renders (batch rewards are
    generated, so print/ is not scanned). FAIL when BUILT_REQUIRED, else WARN."""
    findings = []
    for f in sorted(MANUAL.glob("*.md")):
        if not re.match(r"^\d", f.name) or f.name in _GENERATED_OR_META:
            continue
        lines = f.read_text(encoding="utf-8").split("\n")
        open_at, found, fence = None, False, False
        for n, line in enumerate(lines + ["## (end)"], 1):
            if line.lstrip().startswith(("```", "~~~")):
                fence = not fence
            if fence:
                continue
            if re.match(r"^#{1,2}\s", line):
                if open_at and not found:
                    findings.append("%s:%d: %s has no `**Built:**` line"
                                    % (f.relative_to(REPO), open_at, lines[open_at - 1][3:]))
                open_at = n if _CHECKPOINT_H2_RE.match(line) else None
                found = False
            elif open_at and _BUILT_LINE_RE.match(line.strip()):
                found = True
    return findings


def _run_budgets_only(as_json):
    findings = check_step_budgets()
    steps = {(f["file"], f["step"]) for f in findings}
    summary = "%d steps over budget in %d files" % (
        len(steps), len({f for f, _ in steps}))
    try:
        if as_json:
            import json

            for f in findings:
                print(json.dumps(f, ensure_ascii=False))
        else:
            # Unindented, so `path:line` stays at column 0 for editors and grep.
            for f in findings:
                print(_budget_line(f))
        # With --json the summary goes to stderr so stdout stays JSON lines.
        print(summary, file=sys.stderr if as_json else sys.stdout)
    except BrokenPipeError:
        # `… | head` closed the pipe: say nothing, and keep the interpreter
        # from re-raising on its final flush.
        import os

        os.dup2(os.open(os.devnull, os.O_WRONLY), sys.stdout.fileno())
    return 1 if findings else 0


# --------------------------------------------------------------------------
# 6. Parts grammar and 7. Hardware reconciliation — scripts/parts.py owns the
#    parse and the kit-BOM resolve; this only selects files and prints.
# --------------------------------------------------------------------------

PARTS_CHECKS_FAIL = True    # wave-4 phase 5: assembly chapters at zero, now FAIL


def _parts_files(selectors):
    import parts

    files = parts.assembly_chapters()
    if not selectors:
        return files
    picked = []
    for f in files:
        for s in selectors:
            name = Path(s).name
            if f.name == name or f.name.startswith(name.rstrip("-") + "-") or f.stem == name:
                picked.append(f)
                break
    return picked


def _parts_line(f):
    step = ("  Step %s" % f["step"]) if f.get("step") else ""
    item = ("  %s" % f["item"]) if f.get("item") else ""
    detail = (" — %s" % f["detail"]) if f.get("detail") else ""
    return "%s:%d%s  [%d %s]%s%s" % (f["file"], f["line"], step, f["check"], f["kind"], item, detail)


def check_parts(selectors=None):
    """(check-6 findings, check-7 findings, kit-wide info lines)."""
    import parts

    parts.load_part_thumbs()
    files = _parts_files(selectors)
    findings, info = parts.report(files)
    return ([f for f in findings if f["check"] == 6],
            [f for f in findings if f["check"] == 7], info)


def _run_parts_report(argv):
    import json
    from collections import Counter

    selectors = [a for a in argv if not a.startswith("--")]
    six, seven, info = check_parts(selectors)
    findings = six + seven
    try:
        if "--json" in argv:
            for f in findings:
                print(json.dumps(f, ensure_ascii=False))
        else:
            for f in findings:
                print(_parts_line(f))
            for n, group in ((6, six), (7, seven)):
                kinds = Counter(f["kind"] for f in group)
                print("\ncheck %d: %d finding(s) in %d file(s)%s" % (
                    n, len(group), len({f["file"] for f in group}),
                    (" — " + ", ".join("%s %d" % kv for kv in kinds.most_common())) if kinds else ""))
            if info:
                print("\nkit-wide (informative): chapter Hardware tables vs the vendored LDO BOM")
                for line in info:
                    print("  " + line)
    except BrokenPipeError:
        import os

        os.dup2(os.open(os.devnull, os.O_WRONLY), sys.stdout.fileno())
    return 1 if (findings and "--strict" in argv) else 0


def _chapters_arg(argv):
    """`--chapters 05,06` / `--chapters=05,06` -> ['05', '06'] (None if absent)."""
    for i, a in enumerate(argv):
        if a.startswith("--chapters="):
            return [c for c in a.split("=", 1)[1].split(",") if c]
        if a == "--chapters" and i + 1 < len(argv):
            return [c for c in argv[i + 1].split(",") if c]
    return None


def _run_strict_parts(argv):
    """Packet gate: checks 6 and 7 FAIL (exit 1) for the named chapters only
    (the default run fails on them for every assembly chapter)."""
    chapters = _chapters_arg(argv)
    if chapters is not None and not _parts_files(chapters):
        print("--strict-parts: no assembly chapter matches %s" % ",".join(chapters))
        return 2
    six, seven, _ = check_parts(chapters)
    try:
        for f in six + seven:
            print(_parts_line(f))
        print("\nstrict parts (%s): check 6 %d, check 7 %d finding(s)" % (
            ",".join(chapters) if chapters else "all chapters", len(six), len(seven)))
    except BrokenPipeError:
        import os

        os.dup2(os.open(os.devnull, os.O_WRONLY), sys.stdout.fileno())
    return 1 if (six or seven) else 0


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if "--budgets-only" in argv:
        return _run_budgets_only("--json" in argv)
    if "--strict-parts" in argv:
        return _run_strict_parts(argv)
    if "--parts-report" in argv:
        return _run_parts_report([a for a in argv if a != "--parts-report"])

    checks = [
        ("Raw callout markers outside admonitions", check_raw_callouts),
        ("Unresolved Step NN.M references", check_step_refs),
        ("STL printed in no batch", check_stl_coverage),
        ("Tables wider than 7 columns", check_table_width),
    ]
    if "--no-budgets" not in argv:
        checks.append(("Steps over word budget",
                       lambda: [_budget_line(f) for f in check_step_budgets()]))

    total = 0
    for name, fn in checks:
        findings = fn()
        print(f"\n== {name}: {len(findings)} finding(s) ==")
        for line in findings:
            print(f"  {line}")
        if findings and not findings[0].startswith("SKIPPED"):
            total += len(findings)

    missing_source = check_missing_source()
    print(f"\n== WARN: Steps missing a `Source:` line: {len(missing_source)} ==")
    for line in missing_source:
        print(f"  WARN: {line}")

    missing_built = check_checkpoint_built()
    label = "" if BUILT_REQUIRED else "WARN: "
    print(f"\n== {label}Checkpoints without a `**Built:**` line: {len(missing_built)} ==")
    for line in missing_built:
        print(f"  {label}{line}")
    if BUILT_REQUIRED:
        total += len(missing_built)

    six, seven, _ = check_parts()
    for n, name, group in ((6, "Parts grammar", six), (7, "Hardware reconciliation", seven)):
        label = "" if PARTS_CHECKS_FAIL else "WARN: "
        print(f"\n== {label}{n} · {name}: {len(group)} finding(s) in "
              f"{len({f['file'] for f in group})} file(s) — "
              "details: python3 scripts/lint_manual.py --parts-report ==")
        if PARTS_CHECKS_FAIL:
            for f in group:
                print(f"  {_parts_line(f)}")
            total += len(group)

    print(f"\n{total} lint finding(s) total.")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
