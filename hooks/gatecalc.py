"""Build-time fence conversion for the two bench widgets (R7).

Runs as an mkdocs `on_page_markdown` hook on **every** page, so a fence written
in a chapter also works in the step page `scripts/build_steps.py` copies it
into (`docs/manual/steps/**`, which reproduces step bodies verbatim).

Two fences, both authored in the chapter markdown:

    ```gate-calc
    id: gate-a
    title: Gate A — the 30 mm cube
    inputs:
      - key: x
        label: X width (mm)
        nominal: 30.0
        tol: 0.15
        low: <advice when measured < nominal - tol>
        high: <advice when measured > nominal + tol>
      - key: fl
        label: First layer vs mid height, X (mm)
        max: 0.15
        high: <advice>
      - key: snap
        label: Corner snap tears across the layers
        kind: yesno
        no: <advice shown when the answer is no>
        why: <one sentence on what this row protects, behind a "why?" toggle>
    pass: <text shown when every row passes>
    derive:                     # optional, one derived number in the badge line
      expr: start + step * line
      label: Pressure advance to save
      digits: 3
    ```

  -> `<div class="gate-calc" data-gate-calc="<json>">`, filled in by
     `docs/javascripts/gatecalc.js`. The JSON is the whole spec, normalised to
     one shape (`min`/`max`/`advice`), so the JS carries no per-gate knowledge.

     Row semantics: `nominal` + `tol` is a band; `max` / `min` is a one-sided
     limit; `kind: yesno` is a toggle whose failing side is whichever of `no:` /
     `yes:` carries the advice. `optional: true` means an unanswered row does
     not hold up the verdict (it still fails it when answered and failing).
     `why:` is one sentence on what the row protects, rendered as a collapsed
     `why?` disclosure under it; it never affects the verdict.

     `derive:` is an arithmetic expression over the fence's own **number**
     keys, shown beside the badge (`14.18`: the PA value the chosen line of
     Ellis' pattern works out to). It is validated here — only input keys,
     digits, `+ - * / ( ) .` — so the JS can hand it to `new Function` on a
     string it did not have to trust.

    ```tap-tree
    - Phase
        - Symptom
            - What you see

                One paragraph and the step link. [12.3](12-software.md#step-123)
    ```

  -> `<div class="tap-tree" markdown="1">` around the untouched list, so
     Python-Markdown renders it (and mkdocs rewrites and validates every
     relative link) exactly as it would anywhere else on the page;
     `docs/javascripts/taptree.js` then turns the nested `<ul>` into tappable
     cards and hides the list. With JS off the reader still gets the list.

Bad YAML, a missing key or an unreadable row is a build error, not a silently
empty widget.
"""

import html
import json
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mascot  # noqa: E402  (hooks/mascot.py — the raven's markup and asset paths)

_FENCE_RE = re.compile(r"^(\s{0,3})(`{3,}|~{3,})\s*([A-Za-z0-9_-]*)\s*$")

_WIDGETS = ("gate-calc", "tap-tree")

# PyYAML resolves the bare keys `no` / `yes` (and `on` / `off`) to booleans, so
# `no:` in an input row arrives as the key False. Map them back.
_BOOL_KEYS = {True: "yes", False: "no"}


class GateCalcError(Exception):
    """Raised for a malformed fence — fails the build with the page name."""


def _num(value, where, field):
    try:
        return float(value)
    except (TypeError, ValueError):
        raise GateCalcError(f"{where}: `{field}` must be a number, got {value!r}")


def _fmt(value):
    """0.15 -> '0.15', 30.0 -> '30', 16.3 -> '16.3' — hints read like the chapter."""
    text = f"{value:.4f}".rstrip("0").rstrip(".")
    return text or "0"


def _normalise_input(raw, where):
    if not isinstance(raw, dict):
        raise GateCalcError(f"{where}: every entry under `inputs:` must be a mapping")
    row = {}
    for key, value in raw.items():
        row[_BOOL_KEYS.get(key, key) if isinstance(key, bool) else str(key)] = value

    key = row.get("key")
    label = row.get("label")
    if not key or not label:
        raise GateCalcError(f"{where}: an input needs both `key:` and `label:`")
    where = f"{where} input {key!r}"

    out = {
        "key": str(key),
        "label": str(label),
        "optional": bool(row.get("optional", False)),
    }

    why = row.get("why")
    if why is not None:
        if not isinstance(why, str) or not why.strip():
            raise GateCalcError(f"{where}: `why:` must be one sentence of text, got {why!r}")
        out["why"] = why.strip()

    if str(row.get("kind", "")).lower() == "yesno":
        fail_on = "no" if "no" in row else ("yes" if "yes" in row else None)
        if fail_on is None:
            raise GateCalcError(f"{where}: a `kind: yesno` row needs a `no:` or `yes:` advice line")
        out["kind"] = "yesno"
        out["fail_on"] = fail_on
        out["advice"] = str(row[fail_on])
        out["hint"] = str(row.get("hint") or ("yes passes" if fail_on == "no" else "no passes"))
        return out

    out["kind"] = "number"
    if "nominal" in row:
        if "tol" not in row:
            raise GateCalcError(f"{where}: `nominal:` needs a `tol:` beside it")
        nominal = _num(row["nominal"], where, "nominal")
        tol = _num(row["tol"], where, "tol")
        out["min"] = round(nominal - tol, 6)
        out["max"] = round(nominal + tol, 6)
        default_hint = f"{_fmt(nominal)} ±{_fmt(tol)}"
    elif "max" in row or "min" in row:
        parts = []
        if "min" in row:
            out["min"] = _num(row["min"], where, "min")
            parts.append(f"≥ {_fmt(out['min'])}")
        if "max" in row:
            out["max"] = _num(row["max"], where, "max")
            parts.append(f"≤ {_fmt(out['max'])}")
        default_hint = " and ".join(parts)
    else:
        raise GateCalcError(
            f"{where}: a number row needs `nominal:` + `tol:`, or `min:` / `max:`"
        )

    low = row.get("low")
    high = row.get("high")
    if "min" in out and not low and not high:
        raise GateCalcError(f"{where}: needs a `low:` advice line")
    if "max" in out and not high and not low:
        raise GateCalcError(f"{where}: needs a `high:` advice line")
    out["low"] = str(low or high)
    out["high"] = str(high or low)
    out["hint"] = str(row.get("hint") or default_hint)
    return out


_DERIVE_CHARS_RE = re.compile(r"^[A-Za-z0-9_+\-*/(). ]+$")
_DERIVE_IDENT_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")


def _normalise_derive(raw, inputs, where):
    """`derive:` -> {expr, keys, label, digits}, with the expression whitelisted."""
    if not isinstance(raw, dict):
        raise GateCalcError(f"{where}: `derive:` must be a mapping with an `expr:`")
    expr = raw.get("expr")
    if not isinstance(expr, str) or not expr.strip():
        raise GateCalcError(f"{where}: `derive:` needs an `expr:` string")
    expr = expr.strip()
    if not _DERIVE_CHARS_RE.match(expr):
        raise GateCalcError(
            f"{where}: `derive.expr` may only use input keys, numbers, `+ - * / ( ) .` — got {expr!r}"
        )
    numbers = [row["key"] for row in inputs if row["kind"] == "number"]
    keys = []
    for ident in _DERIVE_IDENT_RE.findall(expr):
        if ident not in numbers:
            raise GateCalcError(
                f"{where}: `derive.expr` names {ident!r}, which is not a number input on this fence"
            )
        if ident not in keys:
            keys.append(ident)
    if not keys:
        raise GateCalcError(f"{where}: `derive.expr` uses no input of this fence")
    try:
        digits = int(raw.get("digits", 3))
    except (TypeError, ValueError):
        raise GateCalcError(f"{where}: `derive.digits` must be a whole number")
    if not 0 <= digits <= 6:
        raise GateCalcError(f"{where}: `derive.digits` must be between 0 and 6, got {digits}")
    return {
        "expr": expr,
        "keys": keys,
        "label": str(raw.get("label") or "Result"),
        "digits": digits,
    }


def _gate_calc_html(body, where, bird=True):
    try:
        spec = yaml.safe_load("\n".join(body))
    except yaml.YAMLError as exc:
        raise GateCalcError(f"{where}: gate-calc YAML did not parse — {exc}")
    if not isinstance(spec, dict):
        raise GateCalcError(f"{where}: a gate-calc fence must be a YAML mapping")
    if not spec.get("id"):
        raise GateCalcError(f"{where}: a gate-calc fence needs an `id:` (its storage key)")
    if not isinstance(spec.get("inputs"), list) or not spec["inputs"]:
        raise GateCalcError(f"{where}: a gate-calc fence needs a non-empty `inputs:` list")

    out = {
        "id": str(spec["id"]),
        "title": str(spec.get("title") or "Gate check"),
        "pass": str(spec.get("pass") or "Every row passes."),
        "inputs": [_normalise_input(row, where) for row in spec["inputs"]],
    }
    seen = set()
    for row in out["inputs"]:
        if row["key"] in seen:
            raise GateCalcError(f"{where}: duplicate input key {row['key']!r}")
        seen.add(row["key"])
    if spec.get("derive") is not None:
        out["derive"] = _normalise_derive(spec["derive"], out["inputs"], where)

    payload = html.escape(json.dumps(out, ensure_ascii=False, separators=(",", ":")), quote=True)
    # The two verdict birds ride as page-relative asset paths (hooks/mascot.py
    # resolves the `@mascot/` sentinel per page), so gatecalc.js stays
    # spec-agnostic: it reads an attribute and never knows where the art lives.
    # Inside a NO_MASCOT_STEPS step (B00.7 is an iron step) the attributes are
    # left off; gatecalc.js then makes no bird element and shows only the text.
    birds = (
        f' data-mascot-pass="{mascot.asset("pass")}"'
        f' data-mascot-fail="{mascot.asset("fail")}"'
        f' data-mascot-pass-alt="{html.escape(mascot.title_of("pass"), quote=True)}"'
        f' data-mascot-fail-alt="{html.escape(mascot.title_of("fail"), quote=True)}"'
    ) if bird else ""
    return (
        f'<div class="gate-calc" data-gate-calc="{payload}"{birds}>'
        f'<p class="gate-calc__nojs">{html.escape(out["title"])} — '
        f"the calculator needs JavaScript; the limits are in the table on this page.</p></div>"
    )


def _tap_tree_markdown(body, indent, where):
    lines = [line[len(indent):] if line.startswith(indent) else line for line in body]
    if not any(line.lstrip().startswith(("-", "*", "+")) for line in lines):
        raise GateCalcError(f"{where}: a tap-tree fence must hold a nested markdown list")
    return ['<div class="tap-tree" markdown="1">', ""] + lines + ["", "</div>"]


def _convert(markdown, where):
    lines = markdown.split("\n")
    out = []
    # hooks/mascot.py's step scope (the humour rule's one classifier): which
    # NO_MASCOT_STEPS step, if any, the current line sits in.
    scope = mascot._StepScope()
    i, n = 0, len(lines)
    while i < n:
        m = _FENCE_RE.match(lines[i])
        if not m:
            h = mascot._MD_HEADING_RE.match(lines[i])
            if h:
                scope.heading(len(h.group(1)), h.group(2))
            out.append(lines[i])
            i += 1
            continue
        indent, token, info = m.group(1), m.group(2)[0] * 3, m.group(3)
        j = i + 1
        while j < n and not lines[j].strip().startswith(token):
            j += 1
        body = lines[i + 1:j]
        close = min(j + 1, n)
        if info not in _WIDGETS:
            out.extend(lines[i:close])          # somebody else's fence, untouched
        elif info == "gate-calc":
            out += ["", _gate_calc_html(body, where, bird=not scope.step), ""]
        else:
            out += [""] + _tap_tree_markdown(body, indent, where) + [""]
        i = close
    return "\n".join(out)


def on_page_markdown(markdown, page, config, files):
    if "```gate-calc" not in markdown and "```tap-tree" not in markdown:
        return markdown
    where = getattr(getattr(page, "file", None), "src_uri", None) or "page"
    return _convert(markdown, where)


if __name__ == "__main__":
    fixtures = {
        "gate band + limit + yesno": (
            "```gate-calc\n"
            "id: gate-a\n"
            "title: Gate A — the cube\n"
            "inputs:\n"
            "  - key: x\n"
            "    label: X width (mm)\n"
            "    nominal: 30.0\n"
            "    tol: 0.15\n"
            "    low: under advice\n"
            "    high: over advice\n"
            "  - key: fl\n"
            "    label: First layer delta (mm)\n"
            "    max: 0.15\n"
            "    high: elephant foot\n"
            "  - key: snap\n"
            "    label: Corner snap tears across the layers\n"
            "    kind: yesno\n"
            "    no: chamber too cold\n"
            "  - key: rail\n"
            "    label: Rail guide slides on\n"
            "    kind: yesno\n"
            "    optional: true\n"
            "    no: reprint it\n"
            "    why: the rail row gates nothing but a reprint\n"
            "pass: all good\n"
            "```\n"
        ),
        "derive": (
            "```gate-calc\n"
            "id: tune-pa\n"
            "inputs:\n"
            "  - key: start\n"
            "    label: Sweep start\n"
            "    min: 0\n"
            "    max: 0.1\n"
            "    low: widen it\n"
            "    high: widen it\n"
            "  - key: stepv\n"
            "    label: Increment\n"
            "    min: 0.001\n"
            "    max: 0.005\n"
            "    low: too fine\n"
            "    high: too coarse\n"
            "  - key: line\n"
            "    label: Lines above the start\n"
            "    min: 0\n"
            "    max: 20\n"
            "    low: widen it\n"
            "    high: widen it\n"
            "  - key: clean\n"
            "    label: One corner is sharpest\n"
            "    kind: yesno\n"
            "    no: check the extruder\n"
            "derive:\n"
            "  expr: start + stepv * line\n"
            "  label: PA to save\n"
            "  digits: 3\n"
            "```\n"
        ),
        "tap tree": (
            "```tap-tree\n"
            "- Printing a plate\n"
            "    - The cube is oversize\n"
            "\n"
            "        Bring the multiplier down. [B00.5](print/B00-calibration-and-jigs.md)\n"
            "```\n"
        ),
        "a plain fence is untouched": ("```python\nid: not-a-gate\n```\n"),
    }

    fail = False
    gate = _convert(fixtures["gate band + limit + yesno"], "fixture")
    print(gate)
    spec = json.loads(html.unescape(re.search(r'data-gate-calc="([^"]*)"', gate).group(1)))
    rows = {r["key"]: r for r in spec["inputs"]}
    if (rows["x"]["min"], rows["x"]["max"]) != (29.85, 30.15):
        print("FAIL: nominal/tol did not become a band:", rows["x"])
        fail = True
    if rows["fl"].get("min") is not None or rows["fl"]["max"] != 0.15:
        print("FAIL: `max:` became something other than a one-sided limit:", rows["fl"])
        fail = True
    if rows["snap"]["fail_on"] != "no" or rows["snap"]["advice"] != "chamber too cold":
        print("FAIL: PyYAML's boolean `no:` key was not mapped back:", rows["snap"])
        fail = True
    if not rows["rail"]["optional"]:
        print("FAIL: optional row lost its flag:", rows["rail"])
        fail = True
    if rows["x"]["hint"] != "30 ±0.15":
        print("FAIL: hint:", rows["x"]["hint"])
        fail = True
    if rows["rail"].get("why") != "the rail row gates nothing but a reprint":
        print("FAIL: `why:` did not reach the JSON:", rows["rail"])
        fail = True
    if "why" in rows["x"]:
        print("FAIL: a row with no `why:` invented one:", rows["x"])
        fail = True

    derived = _convert(fixtures["derive"], "fixture")
    dspec = json.loads(html.unescape(re.search(r'data-gate-calc="([^"]*)"', derived).group(1)))
    if dspec.get("derive") != {
        "expr": "start + stepv * line",
        "keys": ["start", "stepv", "line"],
        "label": "PA to save",
        "digits": 3,
    }:
        print("FAIL: derive did not normalise:", dspec.get("derive"))
        fail = True

    tree = _convert(fixtures["tap tree"], "fixture")
    print(tree)
    if '<div class="tap-tree" markdown="1">' not in tree or "- Printing a plate" not in tree:
        print("FAIL: tap-tree did not wrap the list verbatim")
        fail = True

    # The humour rule: no verdict bird inside a NO_MASCOT_STEPS step (B00.7 is
    # an iron step), on the step page (h1) and the chapter page (h2) alike; the
    # next step heading closes the scope.
    small = "```gate-calc\nid: g\ninputs:\n  - key: a\n    label: A\n    max: 1\n    high: x\n```\n"
    if "data-mascot-pass" not in gate:
        print("FAIL: a gate outside any listed step lost its verdict bird")
        fail = True
    for doc, want, what in (
        ("# Step B00.7 — Gate B\n\n" + small, False, "step page of a listed step"),
        ("## Step B00.7 — Gate B\n\n#### Row\n\n" + small, False, "sub-heading inside a listed step"),
        ("## Step B00.7 — Gate B\n\n## Step B00.8 — Next\n\n" + small, True, "step after a listed one"),
        ("# Step B00.2 — Gate A\n\n" + small, True, "unlisted step"),
    ):
        got = _convert(doc, "fixture")
        if ("data-mascot-pass" in got) != want or 'class="gate-calc"' not in got:
            print("FAIL: verdict bird on the", what, "- want bird:", want)
            fail = True

    untouched = _convert(fixtures["a plain fence is untouched"], "fixture")
    if untouched.strip() != fixtures["a plain fence is untouched"].strip():
        print("FAIL: a non-widget fence was rewritten:", untouched)
        fail = True

    for bad, why in (
        ("```gate-calc\ntitle: no id\ninputs:\n  - key: a\n    label: A\n    max: 1\n    high: x\n```\n",
         "missing id"),
        ("```gate-calc\nid: x\ninputs:\n  - key: a\n    label: A\n```\n", "row with no limit"),
        ("```gate-calc\nid: x\ninputs:\n  - key: a\n    label: A\n    kind: yesno\n```\n",
         "yesno with no advice"),
        ("```gate-calc\nid: x\ninputs:\n  - key: a\n    label: A\n    max: 1\n    high: x\n"
         "    why:\n      - not a sentence\n```\n", "`why:` that is not a string"),
        ("```gate-calc\nid: x\ninputs:\n  - key: a\n    label: A\n    max: 1\n    high: x\n"
         "derive:\n  expr: a + b\n```\n", "derive naming an unknown key"),
        ("```gate-calc\nid: x\ninputs:\n  - key: a\n    label: A\n    max: 1\n    high: x\n"
         "derive:\n  expr: fetch(a)\n```\n", "derive with a call in it"),
        ("```gate-calc\nid: x\ninputs:\n  - key: a\n    label: A\n    kind: yesno\n    no: x\n"
         "derive:\n  expr: a * 2\n```\n", "derive over a yes/no row"),
        ("```tap-tree\nnot a list\n```\n", "tap-tree with no list"),
    ):
        try:
            _convert(bad, "fixture")
        except GateCalcError:
            continue
        print(f"FAIL: {why} did not raise")
        fail = True

    if fail:
        raise SystemExit(1)
    print("All self-tests passed.")
