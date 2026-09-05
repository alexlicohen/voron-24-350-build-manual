#!/usr/bin/env python3
"""Fetch LDO Motors images (GitHub repos + docs.ldomotors.com pages) into
docs/manual/assets/ldo/ for embedding in the Voron manual.

Alex's ruling 2026-09-05 (see docs/manual/CONVENTIONS.md "Image licensing"):
LDO documentation images and the Nitehawk-SB V2 / Leviathan / LDOVoron2 repo
images may be mirrored for this non-commercial, attributed manual.

Usage: python3 scripts/fetch_ldo_images.py
Requires: `gh` CLI authenticated, `curl`, Pillow (for optional downscale pass).
"""
import csv
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse, quote

ROOT = Path(__file__).resolve().parent.parent
MANUAL = ROOT / "docs" / "manual"
ASSETS = MANUAL / "assets" / "ldo"
IMG_EXT = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".bmp"}
MIN_BYTES = 10 * 1024  # skip logos/icons under 10 KB
MAX_TOTAL_MB = 60

REPOS = [
    ("MotorDynamicsLab/LDOVoron2", ["Images", "Firmware"], True),
    ("MotorDynamicsLab/Leviathan", [""], True),
    ("MotorDynamicsLab/Nitehawk-SB-V2", ["Images"], False),
]


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, errors="ignore")
    if r.returncode != 0:
        return None
    return r.stdout


def gh_api(path):
    out = run(["gh", "api", path])
    if out is None:
        return None
    return json.loads(out)


def default_branch(repo):
    data = gh_api(f"repos/{repo}")
    return data["default_branch"]


def branch_sha(repo, branch):
    data = gh_api(f"repos/{repo}/git/refs/heads/{branch}")
    return data["object"]["sha"]


def list_tree(repo, sha):
    """Full recursive tree at sha."""
    data = gh_api(f"repos/{repo}/git/trees/{sha}?recursive=1")
    if data is None:
        return []
    return data.get("tree", [])


def fetch_repo_images(repo, subdirs, also_root_readme):
    branch = default_branch(repo)
    sha = branch_sha(repo, branch)
    tree = list_tree(repo, sha)
    records = []
    for entry in tree:
        if entry.get("type") != "blob":
            continue
        path = entry["path"]
        ext = Path(path).suffix.lower()
        if ext not in IMG_EXT:
            continue
        in_scope = any(
            sd == "" or path.startswith(sd + "/") or path == sd for sd in subdirs
        )
        if not in_scope and not also_root_readme:
            continue
        if not in_scope:
            # allow root-level images referenced from README
            if "/" in path:
                continue
        raw_url = f"https://raw.githubusercontent.com/{repo}/{sha}/{quote(path)}"
        dest_dir = ASSETS / repo.split("/")[1] / Path(path).parent
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / Path(path).name
        ok = run(["curl", "-sL", "-f", "-o", str(dest), raw_url])
        if ok is None or not dest.exists() or dest.stat().st_size == 0:
            print(f"  FAILED download: {raw_url}", file=sys.stderr)
            if dest.exists():
                dest.unlink()
            continue
        records.append(
            {
                "file": str(dest.relative_to(ROOT)),
                "repo": repo,
                "path": path,
                "sha": sha,
                "url": raw_url,
                "source_page": raw_url,
            }
        )
    return records


def find_docs_urls():
    urls = set()
    pattern = re.compile(r"https?://docs\.ldomotors\.com[^\s)\"'\]]*")
    for md in MANUAL.glob("*.md"):
        for m in pattern.findall(md.read_text(errors="ignore")):
            # normalize: strip fragment, ensure scheme
            base = m.split("#")[0].rstrip("/.,")
            urls.add(base)
    return sorted(urls)


def page_slug(url):
    path = urlparse(url).path.strip("/")
    return re.sub(r"[^a-zA-Z0-9_-]+", "-", path).strip("-") or "index"


def fetch_docs_page_images(url):
    """Fetch a docs.ldomotors.com page and pull <img src> URLs, downloading
    each into assets/ldo/docs/<slug>--<name>."""
    slug = page_slug(url)
    records = []
    failed = None

    # Some manual citations are direct image URLs, not HTML pages.
    if Path(urlparse(url).path).suffix.lower() in IMG_EXT:
        dest_dir = ASSETS / "docs"
        dest_dir.mkdir(parents=True, exist_ok=True)
        name = Path(urlparse(url).path).name
        dest = dest_dir / f"{slug}"
        # slug already encodes the path incl. filename; keep original ext
        if not dest.suffix:
            dest = dest_dir / f"{slug}{Path(name).suffix}"
        ok = run(["curl", "-sL", "-f", "-o", str(dest), url])
        if ok is None or not dest.exists() or dest.stat().st_size < MIN_BYTES:
            if dest.exists():
                dest.unlink()
            return [], url
        return [
            {
                "file": str(dest.relative_to(ROOT)),
                "repo": "docs.ldomotors.com",
                "path": url,
                "sha": "",
                "url": url,
                "source_page": url,
            }
        ], None

    html = run(["curl", "-sL", "-A", "Mozilla/5.0", url])
    if not html:
        return [], url
    # Try to find img src attributes
    srcs = set(re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', html, re.I))
    # Also catch data-src (lazy-loaded) and background-image url()
    srcs |= set(re.findall(r'data-src=["\']([^"\']+)["\']', html, re.I))
    if not srcs:
        failed = url
        return [], failed
    dest_dir = ASSETS / "docs"
    dest_dir.mkdir(parents=True, exist_ok=True)
    seen_names = set()
    got_any = False
    for src in srcs:
        if src.startswith("//"):
            src = "https:" + src
        elif src.startswith("/"):
            parsed = urlparse(url)
            src = f"{parsed.scheme}://{parsed.netloc}{src}"
        elif not src.startswith("http"):
            continue
        ext = Path(urlparse(src).path).suffix.lower()
        if ext not in IMG_EXT:
            continue
        name = Path(urlparse(src).path).name
        if re.search(r"logo|icon|favicon|avatar", name, re.I):
            continue
        fname = f"{slug}--{name}"
        if fname in seen_names:
            continue
        seen_names.add(fname)
        dest = dest_dir / fname
        ok = run(["curl", "-sL", "-f", "-o", str(dest), src])
        if ok is None or not dest.exists():
            if dest.exists():
                dest.unlink()
            continue
        if dest.stat().st_size < MIN_BYTES:
            dest.unlink()
            continue
        got_any = True
        records.append(
            {
                "file": str(dest.relative_to(ROOT)),
                "repo": "docs.ldomotors.com",
                "path": src,
                "sha": "",
                "url": src,
                "source_page": url,
            }
        )
    if not got_any:
        failed = url
    return records, failed


def sha256(path):
    h = hashlib.sha256()
    h.update(Path(path).read_bytes())
    return h.hexdigest()


def dedupe(records):
    seen = {}
    kept = []
    removed = 0
    for r in records:
        p = ROOT / r["file"]
        if not p.exists():
            continue
        h = sha256(p)
        if h in seen:
            p.unlink()
            removed += 1
            continue
        seen[h] = r["file"]
        kept.append(r)
    return kept, removed


def guess_chapter(source):
    s = source.lower()
    if "wiring" in s or "nozzle-probe" in s or "endstop" in s or "cable" in s or "wago" in s:
        return "10-wiring.md"
    if "nitehawk" in s:
        return "08-toolhead.md / 10-wiring.md / 12-software.md"
    if "leviathan" in s:
        return "09-electronics-bay.md / 12-software.md"
    if "printed_part" in s or "heatset" in s or "rail_grease" in s:
        return "docs/manual/print/"
    if "build-faq" in s or "bom" in s:
        return "01-frame.md .. 07-ab-belts.md"
    return "TBD"


def main():
    ASSETS.mkdir(parents=True, exist_ok=True)
    all_records = []
    per_source_counts = {}

    for repo, subdirs, also_root in REPOS:
        print(f"Fetching {repo} ...", file=sys.stderr)
        recs = fetch_repo_images(repo, subdirs, also_root)
        per_source_counts[repo] = len(recs)
        all_records.extend(recs)

    docs_urls = find_docs_urls()
    failed_pages = []
    for url in docs_urls:
        recs, failed = fetch_docs_page_images(url)
        all_records.extend(recs)
        if failed:
            failed_pages.append(failed)
    per_source_counts["docs.ldomotors.com"] = sum(
        1 for r in all_records if r["repo"] == "docs.ldomotors.com"
    )

    kept, dup_removed = dedupe(all_records)

    total_bytes = sum((ROOT / r["file"]).stat().st_size for r in kept)
    total_mb = total_bytes / (1024 * 1024)
    downscaled = False
    if total_mb > MAX_TOTAL_MB:
        downscaled = True
        try:
            from PIL import Image

            for r in kept:
                p = ROOT / r["file"]
                if p.suffix.lower() == ".svg":
                    continue  # vector, not downscalable
                try:
                    with Image.open(p) as im:
                        fmt = im.format
                        if max(im.size) > 1600:
                            im.thumbnail((1600, 1600))
                        if fmt == "JPEG":
                            im.convert("RGB").save(p, "JPEG", quality=82, optimize=True)
                        elif fmt == "PNG":
                            im.save(p, "PNG", optimize=True)
                        else:
                            im.save(p)
                except Exception as e:
                    print(f"  downscale failed {p}: {e}", file=sys.stderr)
        except ImportError:
            print("Pillow not available; skipping downscale", file=sys.stderr)
        total_bytes = sum((ROOT / r["file"]).stat().st_size for r in kept)
        total_mb = total_bytes / (1024 * 1024)

    # SOURCES.txt
    today = "2026-09-05"
    with open(ASSETS / "SOURCES.txt", "w") as f:
        for r in kept:
            f.write(
                f"{r['file']} -> {r['url']} -> © LDO Motors, used with attribution, non-commercial -> {today}\n"
            )

    # MANIFEST.csv
    with open(ASSETS / "MANIFEST.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["file", "source_page", "alt_text_guess", "suggested_chapter"])
        for r in kept:
            name = Path(r["file"]).stem.replace("_", " ").replace("-", " ")
            w.writerow([r["file"], r["source_page"], name, guess_chapter(r["source_page"])])

    print("\n--- Summary ---")
    for src, n in per_source_counts.items():
        print(f"{src}: {n} images")
    print(f"Duplicates removed: {dup_removed}")
    print(f"Total size: {total_mb:.1f} MB" + (" (downscaled to fit)" if downscaled else ""))
    if total_mb > MAX_TOTAL_MB:
        print(f"WARNING: still over {MAX_TOTAL_MB} MB after downscale")
    if failed_pages:
        print("Pages with no extractable images:")
        for p in failed_pages:
            print(f"  {p}")
    print(f"Manifest: {ASSETS / 'MANIFEST.csv'}")
    print(f"Sources: {ASSETS / 'SOURCES.txt'}")


if __name__ == "__main__":
    main()
