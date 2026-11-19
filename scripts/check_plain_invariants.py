#!/usr/bin/env python3
"""A plain-style rewrite must not touch what other files key on.

Compares chapters in the working tree with the same files at a base commit and fails when a step
heading, a Parts block, a Helper line, a Source line or a Pause line's minutes changed.

    python3 scripts/check_plain_invariants.py --base <commit> --chapters 02,03
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANUAL = ROOT / "docs" / "manual"

_STEP_RE = re.compile(r"^###\s*Step\s+(\S+)")
_FIELD_RE = re.compile(r"^\*\*[^*]+:\*\*")
_PAUSE_RE = re.compile(r"^Pause: ~\d+ min since the last pause")


def facts(text):
    """{step id: {heading, parts, helper, source, pause}} plus the heading order."""
    order, steps, cur, in_parts = [], {}, None, False
    for raw in text.splitlines():
        line = raw.rstrip()
        m = _STEP_RE.match(line)
        if m:
            cur = {"heading": line, "parts": [], "helper": [], "source": [], "pause": []}
            steps[m.group(1)] = cur
            order.append(line)
            in_parts = False
            continue
        if line.startswith("## "):
            cur, in_parts = None, False
        if cur is None:
            continue
        if line.startswith("**Parts:**"):
            in_parts = True
            cur["parts"].append(line)
            continue
        if in_parts:
            if _FIELD_RE.match(line) or line.startswith(("#", "!", "Source:", "Pause:", "⚠")):
                in_parts = False
            elif line and not line.startswith(("-", " ", "\t")):
                in_parts = False
            elif line:
                cur["parts"].append(line)
                continue
            else:
                continue
        if line.startswith("**Helper:**"):
            cur["helper"].append(line)
        elif line.startswith("Source:"):
            cur["source"].append(line)
        else:
            p = _PAUSE_RE.match(line)
            if p:
                cur["pause"].append(p.group(0))
    return order, steps


def compare(path, base):
    rel = path.relative_to(ROOT).as_posix()
    old = subprocess.run(["git", "-C", str(ROOT), "show", f"{base}:{rel}"],
                         capture_output=True, text=True, check=True).stdout
    old_order, old_steps = facts(old)
    new_order, new_steps = facts(path.read_text())
    out = []
    if old_order != new_order:
        gone = [h for h in old_order if h not in new_order]
        added = [h for h in new_order if h not in old_order]
        out.append(f"{rel}: step headings changed (order, id or title)")
        out += [f"  - {h}" for h in gone] + [f"  + {h}" for h in added]
    for sid, o in old_steps.items():
        n = new_steps.get(sid)
        if n is None:
            continue
        for key in ("parts", "helper", "source", "pause"):
            if o[key] != n[key]:
                out.append(f"{rel}: Step {sid}: {key} changed")
                out += [f"  - {x}" for x in o[key] if x not in n[key]]
                out += [f"  + {x}" for x in n[key] if x not in o[key]]
    return out


def main():
    ap = argparse.ArgumentParser(description="A plain-style rewrite must not touch what other files key on.")
    ap.add_argument("--base", required=True, help="commit that holds the chapters before the rewrite")
    ap.add_argument("--chapters", required=True, help="comma-separated chapter numbers, e.g. 02,03")
    args = ap.parse_args()
    findings = []
    for num in args.chapters.split(","):
        paths = sorted(MANUAL.glob(f"{num.strip()}-*.md"))
        if not paths:
            findings.append(f"no chapter file for {num}")
        for path in paths:
            findings += compare(path, args.base)
    print("\n".join(findings) if findings else f"OK: invariants hold for {args.chapters} against {args.base}")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
