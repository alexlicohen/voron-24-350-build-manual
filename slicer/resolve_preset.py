#!/usr/bin/env python3
"""Resolve a PrusaSlicer vendor-bundle preset (following `inherits`) to a flat dict.

Reads the PrusaResearch.ini that ships with the installed PrusaSlicer so the
values are the ones this machine will actually slice with, not recalled ones.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

BUNDLE = Path(
    "/Applications/PrusaSlicer.app/Contents/Resources/profiles/PrusaResearch.ini"
)

_SECTION_RE = re.compile(r"^\[([^\]]+)\]\s*$")


def load_bundle(path: Path = BUNDLE) -> dict[str, dict[str, str]]:
    """Parse the vendor bundle into {section_name: {key: value}}.

    Hand-rolled rather than configparser: vendor sections repeat keys across
    kinds and values contain '=' and escaped newlines.
    """
    sections: dict[str, dict[str, str]] = {}
    cur: dict[str, str] | None = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.rstrip("\n")
        m = _SECTION_RE.match(line.strip())
        if m:
            cur = sections.setdefault(m.group(1), {})
            continue
        if cur is None or not line.strip() or line.lstrip().startswith("#"):
            continue
        if "=" not in line:
            continue
        k, v = line.split("=", 1)
        cur[k.strip()] = v.strip()
    return sections


def resolve(sections: dict[str, dict[str, str]], kind: str, name: str) -> dict[str, str]:
    """Flatten `[kind:name]` by applying its `inherits` chain left to right."""
    key = f"{kind}:{name}"
    if key not in sections:
        raise KeyError(f"no section [{key}] in bundle")
    node = sections[key]
    out: dict[str, str] = {}
    inherits = node.get("inherits", "").strip()
    if inherits:
        for parent in [p.strip() for p in inherits.split(";") if p.strip()]:
            out.update(resolve(sections, kind, parent))
    for k, v in node.items():
        if k == "inherits":
            continue
        out[k] = v
    return out


if __name__ == "__main__":
    kind, name = sys.argv[1], sys.argv[2]
    s = load_bundle()
    for k, v in sorted(resolve(s, kind, name).items()):
        print(f"{k} = {v}")
