#!/usr/bin/env python3
"""Download every STL/3MF the plate plan names, from the pinned commits.

Idempotent: a file whose SHA256 already matches the manifest is not re-fetched.
`slicer/stl/` is gitignored (re-fetchable); `slicer/stl/MANIFEST.sha256` is
committed so a mid-build reprint is provably the same geometry.

    python3 slicer/fetch_stls.py            # fetch what is missing/changed
    python3 slicer/fetch_stls.py --verify   # check only, exit 1 on mismatch
"""
from __future__ import annotations

import argparse
import hashlib
import sys
import urllib.parse
import urllib.request
from pathlib import Path

from plates import REPOS, all_sources, local_path

ROOT = Path(__file__).resolve().parent
STL_DIR = ROOT / "stl"
MANIFEST = STL_DIR / "MANIFEST.sha256"


def raw_url(repo_key: str, path: str) -> str:
    owner_name, _branch, sha = REPOS[repo_key]
    quoted = urllib.parse.quote(path)
    return f"https://raw.githubusercontent.com/{owner_name}/{sha}/{quoted}"


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_manifest() -> dict[str, str]:
    if not MANIFEST.exists():
        return {}
    out = {}
    for line in MANIFEST.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        digest, rel = line.split("  ", 1)
        out[rel] = digest
    return out


def write_manifest(entries: dict[str, str]) -> None:
    lines = [
        "# SHA256 of every STL/3MF used by slicer/build_plates.py.",
        "# Regenerate with: python3 slicer/fetch_stls.py",
        "# Pinned commits:",
    ]
    for key, (owner_name, branch, sha) in sorted(REPOS.items()):
        lines.append(f"#   {key:10s} {owner_name} @ {branch} = {sha}")
    lines.append("")
    lines += [f"{digest}  {rel}" for rel, digest in sorted(entries.items())]
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text("\n".join(lines) + "\n")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify", action="store_true",
                    help="verify local files against the manifest; do not download")
    args = ap.parse_args()

    known = read_manifest()
    entries: dict[str, str] = {}
    fetched = kept = 0
    problems: list[str] = []

    for repo_key, path in all_sources():
        rel = local_path(repo_key, path)
        dest = STL_DIR / rel
        if dest.exists() and known.get(rel) == sha256(dest):
            entries[rel] = known[rel]
            kept += 1
            continue
        if args.verify:
            problems.append(rel)
            continue
        url = raw_url(repo_key, path)
        dest.parent.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(url, timeout=120) as resp:
            data = resp.read()
        dest.write_bytes(data)
        entries[rel] = hashlib.sha256(data).hexdigest()
        fetched += 1
        print(f"fetched {rel} ({len(data)/1024:.0f} KB)")

    if args.verify:
        if problems:
            print(f"MISMATCH/MISSING ({len(problems)}):", file=sys.stderr)
            for p in problems:
                print(f"  {p}", file=sys.stderr)
            return 1
        print(f"verified {kept} files against manifest")
        return 0

    write_manifest(entries)
    print(f"{fetched} fetched, {kept} already current, {len(entries)} total -> {MANIFEST}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
