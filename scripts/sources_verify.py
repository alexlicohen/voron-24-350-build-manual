#!/usr/bin/env python3
"""Re-verify sources.yml (R6 V2/V3).

    python3 scripts/sources_verify.py --dry-run
        Re-checks every source (HEAD/GET, expect 200) and, for GitHub
        entries, compares the stored `sha` to the current default-branch
        HEAD. Prints a summary; does not write sources.yml.

    python3 scripts/sources_verify.py
        Same checks, then rewrites sources.yml with refreshed
        `last_verified` and `sha` values.

    python3 scripts/sources_verify.py --git-only
        Drift-job mode (R6 V3, git-backed only per the 2026-09-05 ruling):
        checks only the git-tracked repos in
        sources_common.GIT_TRACKED_REPOS, one line per repo, and prints
        `CHANGED <repo> <old_sha> -> <new_sha>` for any that moved plus
        `DOWN <url> [<status>]` for any pinned URL that stopped 200'ing.
        Exit code is 1 if anything changed or went down (drift.yml uses
        this to decide whether to open an issue).
"""

import argparse
import datetime
import sys

import yaml

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
import sources_common as sc


def verify_git_only():
    sources = sc.load_yaml_sources()
    by_repo = {}
    for s in sources:
        repo = sc.github_repo_slug(s["url"])
        if repo in sc.GIT_TRACKED_REPOS and "sha" in s:
            by_repo.setdefault(repo, []).append(s)

    changed = False
    for repo in sorted(sc.GIT_TRACKED_REPOS):
        entries = by_repo.get(repo, [])
        if not entries:
            print(f"SKIP {repo}: no sources.yml entry with a stored sha")
            continue
        try:
            current = sc.default_branch_sha(repo)
        except RuntimeError as e:
            print(f"ERROR {repo}: {e}")
            changed = True
            continue
        stored_shas = {e["sha"] for e in entries}
        if current in stored_shas:
            print(f"OK {repo} {current}")
        else:
            old = sorted(stored_shas)[0]
            print(f"CHANGED {repo} {old} -> {current} "
                  f"(compare: https://github.com/{repo}/compare/{old}...{current})")
            changed = True

        for s in entries:
            status, _ = sc.fetch_status_and_title(s["url"])
            if status != 200:
                print(f"DOWN {s['url']} [{status}]")
                changed = True

    return 1 if changed else 0


def verify_all(write, today):
    sources = sc.load_yaml_sources()
    non200 = []
    sha_changes = []

    for s in sources:
        status, _ = sc.fetch_status_and_title(s["url"])
        if status != 200:
            non200.append((s["id"], s["url"], status))
        else:
            s["last_verified"] = today

        repo = sc.github_repo_slug(s["url"])
        if repo and "sha" in s:
            try:
                current = sc.default_branch_sha(repo)
            except RuntimeError as e:
                print(f"WARN: {s['id']}: {e}", file=sys.stderr)
                continue
            if current != s["sha"]:
                sha_changes.append((s["id"], repo, s["sha"], current))
                s["sha"] = current

    print(f"{len(sources)} sources checked")
    if non200:
        print(f"{len(non200)} not returning 200:")
        for entry_id, url, status in non200:
            print(f"  {entry_id} [{status}] {url}")
    if sha_changes:
        print(f"{len(sha_changes)} CHANGED (sha moved):")
        for entry_id, repo, old, new in sha_changes:
            print(f"  CHANGED {entry_id} ({repo}) {old} -> {new}")

    if write:
        with open(sc.SOURCES_YML, "w", encoding="utf-8") as f:
            f.write("# Pinned-source inventory (R6 V2).\n")
            f.write("# Rebuild: python3 scripts/sources_build.py\n")
            f.write("# Re-verify: python3 scripts/sources_verify.py\n")
            f.write("# Do not hand-edit URLs here without also fixing the citing chapter.\n\n")
            f.write(f"generated: {today!r}\n\n")
            yaml.safe_dump({"sources": sources}, f, sort_keys=False, allow_unicode=True, width=100)
        print(f"\nwrote {sc.SOURCES_YML}")

    return 1 if (non200 or sha_changes) else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="check only, don't rewrite sources.yml")
    ap.add_argument("--git-only", action="store_true",
                     help="drift-job mode: check only the git-tracked repos in GIT_TRACKED_REPOS")
    ap.add_argument("--today", default=datetime.date.today().isoformat())
    args = ap.parse_args()

    if args.git_only:
        sys.exit(verify_git_only())
    sys.exit(verify_all(write=not args.dry_run, today=args.today))


if __name__ == "__main__":
    main()
