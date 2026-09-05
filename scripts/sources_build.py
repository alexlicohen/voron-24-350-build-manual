#!/usr/bin/env python3
"""One-time/refresh crawl that (re)generates sources.yml from every external
URL cited in docs/**/*.md (R6 V2).

    python3 scripts/sources_build.py            # write sources.yml
    python3 scripts/sources_build.py --dry-run   # print a summary, don't write

Does not touch chapter links — this only inventories what's already cited.
Re-running regenerates the whole file (first_seen for URLs already present
is preserved from the existing sources.yml; new URLs get today via --today).
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--today", default=datetime.date.today().isoformat())
    args = ap.parse_args()

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
