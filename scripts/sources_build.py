#!/usr/bin/env python3
"""One-time/refresh crawl that (re)generates sources.yml from every external
URL cited in docs/**/*.md (R6 V2), plus an add-only mode for new citations.

    python3 scripts/sources_build.py --add-missing [--dry-run] [--fetch] [--today D]
        Add-only (the normal way to keep sources.yml current): appends an entry
        for each cited URL sources.yml lacks and leaves every existing entry,
        the header and `generated:` byte-for-byte as they are. New entries are
        merged into the file's id order. Offline by default: title = the first
        markdown link text (else the URL), kind and pinned_ref from the URL,
        first_seen = --today, cited_in = the doc files and Step ids citing it;
        no last_verified or sha until `sources_verify.py` (or --fetch) checks
        them. --fetch also GETs each NEW URL (page title, status) and resolves
        GitHub default-branch shas, as the crawl does.

    python3 scripts/sources_build.py            # full crawl: rewrite sources.yml
    python3 scripts/sources_build.py --dry-run   # full crawl, print a summary, don't write

Does not touch chapter links — this only inventories what's already cited.
The full crawl regenerates the whole file: it fetches every URL (YouTube answers
a crawl with 429s), re-derives ids and titles and drops hand-added fields; only
first_seen and `printables:` pins carry over. Prefer --add-missing.
"""

import argparse
import datetime
import sys

import yaml

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
import sources_common as sc

FIRST_SEEN_DEFAULT = "2026-09-05"

# Sources that don't appear as a plain URL in the docs but are named in the
# brief explicitly: the manual PDF (pinned by commit in README) and the LDO
# config file Ch 12 is written against.
EXTRA_SOURCES = [
    {
        "id": "voron-manual-assembly-pdf",
        "url": "https://raw.githubusercontent.com/VoronDesign/Voron-2/de7e89d/Manual/Assembly_Manual_2.4r2.pdf",
        "kind": "voron-manual",
        "title": "Voron 2.4r2 Assembly Manual (PDF)",
        "pinned_ref": "de7e89d",
    },
    {
        "id": "ldo-leviathan-rev-d-sbv2-cfg",
        "url": "https://raw.githubusercontent.com/MotorDynamicsLab/LDOVoron2/main/Firmware/leviathan-printer-rev-d-sbv2.cfg",
        "kind": "ldo-repo",
        "title": "leviathan-printer-rev-d-sbv2.cfg",
    },
    # Not cited by URL anywhere in docs/, but a git-tracked repo per R6 V3 —
    # give the weekly drift job a sources.yml entry (and sha) to check.
    # Printables answers plain fetches with 403; this entry's `printables:` pin (file ids,
    # sizes, macro hash) is checked through the GraphQL API by sources_verify.py.
    {
        "id": "printables-502306-cable-duct-remix",
        "url": "https://www.printables.com/model/502306",
        "kind": "community",
        "title": "Remix of RyanDam's Cable Management Duct for Voron Printers Version 3.2",
    },
    {
        "id": "printables-796563-nozzle-scrubber",
        "url": "https://www.printables.com/model/796563",
        "kind": "community",
        "title": "Voron 2.4 Silicone Nozzle Scrubber w/ Sheet Stops (Beacon / Carto Compatible)",
    },
    # The Ch 11 Part C add-ons (pinned by file id, size and sha256 like 796563).
    {
        "id": "printables-608769-voron-side-spool",
        "url": "https://www.printables.com/model/608769",
        "kind": "community",
        "title": "Voron 2.4 (350 bed) Side mounted spool",
    },
    {
        "id": "printables-1605113-prusa-uss-drybox-accessories",
        "url": "https://www.printables.com/model/1605113",
        "kind": "prusa",
        "title": "Prusa USS Drybox printable accessories",
    },
    {
        "id": "printables-488020-happycam-ov5640",
        "url": "https://www.printables.com/model/488020",
        "kind": "community",
        "title": "HappyCam, Voron 2.4 OV5640 camera mount",
    },
    {
        "id": "prusa-prusaslicer-settings-prusa-fff",
        "url": "https://github.com/prusa3d/PrusaSlicer-settings-prusa-fff",
        "kind": "prusa",
        "title": "PrusaSlicer-settings-prusa-fff",
    },
]


def build(today):
    existing_by_url = {s["url"]: s for s in sc.load_yaml_sources()}

    entries = []
    seen_urls = set()

    for extra in EXTRA_SOURCES:
        seen_urls.add(extra["url"])
        prior = existing_by_url.get(extra["url"], {})
        entry = dict(extra)
        entry["first_seen"] = prior.get("first_seen", FIRST_SEEN_DEFAULT)
        entry["last_verified"] = today
        if "printables" in prior:
            entry["printables"] = prior["printables"]   # the pin; sources_verify.py refreshes it
        repo = sc.github_repo_slug(extra["url"])
        if repo:
            try:
                entry["sha"] = sc.default_branch_sha(repo)
            except RuntimeError as e:
                print(f"WARN: {extra['id']}: {e}", file=sys.stderr)
        entries.append(entry)

    urls = [u for u in sc.extract_urls() if u not in seen_urls]

    used_ids = {e["id"] for e in entries}
    for url in urls:
        kind = sc.classify_kind(url)
        prior = existing_by_url.get(url, {})

        status, fetched_title = sc.fetch_status_and_title(url)
        title = fetched_title
        if not title:
            texts = sc.link_texts(url)
            title = texts[0] if texts else url

        base_id = sc.id_for(url)
        entry_id = base_id
        n = 2
        while entry_id in used_ids:
            entry_id = f"{base_id}-{n}"
            n += 1
        used_ids.add(entry_id)

        entry = {
            "id": entry_id,
            "url": url,
            "kind": kind,
            "title": title,
            "first_seen": prior.get("first_seen", FIRST_SEEN_DEFAULT),
            "last_verified": today,
        }

        ref = sc.pinned_ref(url)
        if ref:
            entry["pinned_ref"] = ref

        repo = sc.github_repo_slug(url)
        if repo:
            try:
                entry["sha"] = sc.default_branch_sha(repo)
            except RuntimeError as e:
                print(f"WARN: {entry_id}: {e}", file=sys.stderr)

        if status is not None and status != 200:
            entry["last_status"] = status

        entries.append(entry)

    entries.sort(key=lambda e: e["id"])
    return entries


def _split_blocks(text):
    """sources.yml text -> (head, [entry block text, ...], tail). head runs through the
    `sources:` line; each block is one top-level `- ` list item, verbatim."""
    lines = text.splitlines(keepends=True)
    start = next(i for i, l in enumerate(lines) if l.rstrip("\n") == "sources:") + 1
    head, blocks, tail = "".join(lines[:start]), [], ""
    for i, line in enumerate(lines[start:], start):
        if line.startswith("- "):
            blocks.append(line)
        elif blocks and (line.startswith("  ") or not line.strip()):
            blocks[-1] += line
        else:  # a new top-level key after the list: keep it and everything below
            tail = "".join(lines[i:])
            break
    return head, blocks, tail


def add_missing(today, path=None, fetch=False):
    """(new file text, [new entries]) for sources.yml with an entry appended for every
    cited URL it lacks. Existing text is never re-serialised: the old file is the new
    one with the new blocks removed, byte for byte (asserted)."""
    path = path or sc.SOURCES_YML
    old_text = path.read_text(encoding="utf-8")
    existing = (yaml.safe_load(old_text) or {}).get("sources") or []
    head, blocks, tail = _split_blocks(old_text)
    assert len(blocks) == len(existing), (
        f"{path}: {len(blocks)} `- ` blocks but {len(existing)} entries; is it still "
        "in safe_dump's layout?")
    have = {s["url"] for s in existing}
    used_ids = {s["id"] for s in existing}
    index = sc.citation_index()

    new = []
    for url in sc.extract_urls():
        if url in have:
            continue
        base_id = sc.id_for(url)
        entry_id, n = base_id, 2
        while entry_id in used_ids:
            entry_id, n = f"{base_id}-{n}", n + 1
        used_ids.add(entry_id)
        cite = index.get(url, {"texts": [], "cited_in": {}})
        entry = {
            "id": entry_id,
            "url": url,
            "kind": sc.classify_kind(url),
            "title": next((t for t in cite["texts"] if t.strip()), url),
            "first_seen": today,
        }
        ref = sc.pinned_ref(url)
        if ref:
            entry["pinned_ref"] = ref
        if fetch:
            status, fetched_title = sc.fetch_status_and_title(url)
            if fetched_title:
                entry["title"] = fetched_title
            if status == 200:
                entry["last_verified"] = today
            repo = sc.github_repo_slug(url)
            if repo:
                try:
                    entry["sha"] = sc.default_branch_sha(repo)
                except RuntimeError as e:
                    print(f"WARN: {entry_id}: {e}", file=sys.stderr)
            if status is not None and status != 200:
                entry["last_status"] = status
        entry["cited_in"] = [f"{f} ({', '.join(steps)})" if steps else f
                             for f, steps in cite["cited_in"].items()]
        new.append(entry)

    new.sort(key=lambda e: e["id"])
    new_blocks = [yaml.safe_dump([e], sort_keys=False, allow_unicode=True, width=100)
                  for e in new]

    # Merge into the file's id order without moving any existing block: each new
    # block goes before the first existing block whose id sorts after it.
    out, j = [head], 0
    for block, s in zip(blocks, existing):
        while j < len(new) and new[j]["id"] < s["id"]:
            out.append(new_blocks[j])
            j += 1
        out.append(block)
    out.extend(new_blocks[j:])
    out.append(tail)
    new_text = "".join(out)

    # Proof that nothing existing changed: drop the new blocks again -> the old file.
    added = set(new_blocks)
    _, got_blocks, got_tail = _split_blocks(new_text)
    kept = "".join(b for b in got_blocks if b not in added)
    assert head + kept + got_tail == old_text, "existing sources.yml text would change"
    reloaded = yaml.safe_load(new_text)["sources"]
    assert [s for s in reloaded if s["url"] in have] == existing
    assert len(reloaded) == len(existing) + len(new)
    return new_text, new


def main_add_missing(args):
    new_text, new = add_missing(args.today, fetch=args.fetch)
    by_kind = {}
    for e in new:
        by_kind[e["kind"]] = by_kind.get(e["kind"], 0) + 1
    print(f"{len(new)} cited URLs missing from {sc.SOURCES_YML.name}")
    for kind, count in sorted(by_kind.items()):
        print(f"  {kind}: {count}")
    if args.dry_run:
        for e in new:
            print(f"  + {e['id']}  {e['url']}")
        return
    if new:
        sc.SOURCES_YML.write_text(new_text, encoding="utf-8")
        print(f"\nadded {len(new)} entries to {sc.SOURCES_YML}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--today", default=datetime.date.today().isoformat())
    ap.add_argument("--add-missing", action="store_true",
                    help="add-only: append entries for cited URLs sources.yml lacks, offline")
    ap.add_argument("--fetch", action="store_true",
                    help="with --add-missing: fetch title/status and GitHub sha for the new URLs")
    args = ap.parse_args()
    if args.fetch and not args.add_missing:
        ap.error("--fetch only applies with --add-missing (the full crawl always fetches)")
    if args.add_missing:
        return main_add_missing(args)

    entries = build(args.today)

    by_kind = {}
    non200 = []
    for e in entries:
        by_kind[e["kind"]] = by_kind.get(e["kind"], 0) + 1
        if e.get("last_status"):
            non200.append((e["id"], e["url"], e["last_status"]))

    print(f"{len(entries)} sources")
    for kind, count in sorted(by_kind.items()):
        print(f"  {kind}: {count}")
    if non200:
        print(f"{len(non200)} not returning 200:")
        for entry_id, url, status in non200:
            print(f"  {entry_id} [{status}] {url}")

    if args.dry_run:
        return

    with open(sc.SOURCES_YML, "w", encoding="utf-8") as f:
        f.write(f"# Pinned-source inventory (R6 V2).\n")
        f.write(f"# Rebuild: python3 scripts/sources_build.py\n")
        f.write(f"# Re-verify: python3 scripts/sources_verify.py\n")
        f.write(f"# Do not hand-edit URLs here without also fixing the citing chapter.\n\n")
        f.write(f"generated: {args.today!r}\n\n")
        yaml.safe_dump({"sources": entries}, f, sort_keys=False, allow_unicode=True, width=100)

    print(f"\nwrote {sc.SOURCES_YML}")


if __name__ == "__main__":
    main()
