#!/usr/bin/env python3
"""Map the Steve Builds "LDO Voron 2.4 Kit Build" playlist onto the manual's steps.

Two modes:

  python3 scripts/video_map.py --refresh   # re-fetch playlist metadata + captions
  python3 scripts/video_map.py             # regenerate MANIFEST.md from the YAML

--refresh needs yt-dlp. It is deliberately NOT a project dependency: point
--ytdlp at a scratch venv, e.g.

    uv venv /tmp/ytdl && uv pip install --python /tmp/ytdl/bin/python yt-dlp
    python3 scripts/video_map.py --refresh --ytdlp /tmp/ytdl/bin/yt-dlp

Nothing is downloaded but metadata and subtitle tracks. Captions are cached
OUTSIDE the repo (~/.cache/voron-video-map by default) because they are 4 MB of
re-fetchable auto-generated text; only playlist.json is committed.

The mapping itself lives in docs/manual/assets/video/video_map.yml: one entry
per contiguous video segment (video id, time range, which manual chapter and
step range it covers), plus per-step keyword phrases. Timestamps are resolved by
searching the caption word-timeline inside the segment for those phrases, so a
re-run after a caption refresh re-derives them rather than trusting stale text.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
VIDEO_DIR = REPO / "docs" / "manual" / "assets" / "video"
MAP_YML = VIDEO_DIR / "video_map.yml"
PLAYLIST_JSON = VIDEO_DIR / "playlist.json"
MANIFEST = VIDEO_DIR / "MANIFEST.md"
MANUAL = REPO / "docs" / "manual"
DEFAULT_CACHE = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache")) / "voron-video-map"

# Fields kept from yt-dlp's per-video info JSON. The rest (formats, thumbnails,
# heatmap, live chat) is hundreds of KB of noise we never read.
KEEP = (
    "id title duration upload_date channel channel_id channel_url uploader "
    "webpage_url description chapters license availability view_count"
).split()

STEP_RE = re.compile(r"^### Step ([0-9a-zA-Z]+\.[0-9]+) — (.+)$", re.M)
VTT_CUE = re.compile(r"^(\d\d):(\d\d):(\d\d)\.(\d\d\d) --> ")
VTT_TAG = re.compile(r"<(\d\d):(\d\d):(\d\d)\.(\d\d\d)><c>(.*?)</c>")


# ---------------------------------------------------------------- fetch

def refresh(cfg, ytdlp, cache):
    if not shutil.which(ytdlp) and not Path(ytdlp).exists():
        sys.exit(f"yt-dlp not found at {ytdlp!r} — see the module docstring for a scratch venv")
    cache.mkdir(parents=True, exist_ok=True)
    url = cfg["playlist"]["url"]

    flat = json.loads(subprocess.run(
        [ytdlp, "--flat-playlist", "-J", url],
        check=True, capture_output=True, text=True).stdout)

    subprocess.run([
        ytdlp, "--skip-download", "--write-auto-subs", "--write-subs",
        "--sub-lang", "en.*", "--sub-format", "vtt", "--write-info-json",
        "--no-write-playlist-metafiles", "--ignore-errors",
        "-o", str(cache / "%(playlist_index)02d-%(id)s.%(ext)s"), url,
    ], check=False)

    videos = []
    for entry in flat.get("entries", []):
        vid = entry["id"]
        info = next(iter(sorted(cache.glob(f"*-{vid}.info.json"))), None)
        if info is None:
            print(f"  ! no info.json for {vid} — re-run --refresh (YouTube rate-limits)")
            continue
        d = json.loads(info.read_text())
        rec = {k: d.get(k) for k in KEEP}
        rec["subtitles"] = sorted((d.get("subtitles") or {}).keys())
        rec["automatic_captions_en"] = [
            k for k in (d.get("automatic_captions") or {}) if k.startswith("en")]
        videos.append(rec)

    out = {
        "_note": "Raw yt-dlp metadata, pruned to the fields video_map.py reads "
                 "(formats/thumbnails/heatmap/live-chat dropped). Regenerate: "
                 "python3 scripts/video_map.py --refresh",
        "playlist": {k: flat.get(k) for k in
                     ("id", "title", "channel", "uploader", "channel_url",
                      "webpage_url", "playlist_count")},
        "videos": videos,
    }
    PLAYLIST_JSON.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    total = sum(v["duration"] or 0 for v in videos)
    print(f"playlist.json: {len(videos)} videos, {total // 3600}h{total % 3600 // 60:02d}m")


# ---------------------------------------------------------------- captions

def load_captions(cache):
    """{video_id: [(seconds, word), ...]} from cached auto-caption VTTs."""
    out = {}
    for path in sorted(cache.glob("*.en.vtt")):
        vid = path.name.split("-", 1)[1][: -len(".en.vtt")]
        words, cue = [], 0.0
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            m = VTT_CUE.match(line)
            if m:
                h, mi, s, ms = m.groups()
                cue = int(h) * 3600 + int(mi) * 60 + int(s) + int(ms) / 1000
                continue
            if "<c>" not in line:
                continue
            # A rolling auto-caption cue repeats the previous line then adds the
            # new, word-timed one. Only the tagged half is fresh.
            head = line.split("<", 1)[0].strip()
            if head:
                words.append((cue, head))
            for h, mi, s, ms, w in VTT_TAG.findall(line):
                w = w.strip()
                if w:
                    words.append((int(h) * 3600 + int(mi) * 60 + int(s) + int(ms) / 1000, w))
        out[vid] = [(int(t), w.lower().strip(".,!?\"'();:")) for t, w in words]
    return out


# A YouTube chapter marker fires a little after the topic actually starts, and
# Steve often says the thing before he picks the part up. Allow a keyword to
# match this far before the segment's nominal start.
SLACK = 150


def find(tokens, phrases, lo, hi, slack=SLACK):
    """Earliest window in [lo-slack, hi) containing the most distinct phrases.

    Returns (start_seconds, n_distinct_phrases_matched) or (None, 0).
    """
    lo = max(0, lo - slack)
    events = []
    for phrase in phrases:
        ws = phrase.lower().split()
        n = len(ws)
        for i in range(len(tokens) - n + 1):
            t = tokens[i][0]
            if not (lo <= t < hi):
                continue
            if all(tokens[i + j][1] == ws[j] for j in range(n)):
                events.append((t, phrase))
    if not events:
        return None, 0
    events.sort()
    best = (events[0][0], 1)
    for i, (t0, _) in enumerate(events):
        seen = {p for t, p in events[i:] if t < t0 + 90}
        if len(seen) > best[1]:
            best = (t0, len(seen))
    return best


# ---------------------------------------------------------------- manual

def manual_steps():
    """{chapter_file: [step_id, ...]} in document order."""
    out = {}
    for path in sorted(MANUAL.glob("*.md")) + sorted((MANUAL / "print").glob("*.md")):
        ids = [m.group(1) for m in STEP_RE.finditer(path.read_text())]
        if ids:
            key = path.name if path.parent == MANUAL else f"print/{path.name}"
            out[key] = ids
    return out


def expand(spec, ids):
    """'01.4-01.9' or '01.4, 01.9' -> concrete step ids, in chapter order."""
    if isinstance(spec, list):
        wanted = spec
    else:
        wanted = []
        for part in str(spec).split(","):
            part = part.strip()
            if "-" in part:
                a, b = (p.strip() for p in part.split("-", 1))
                if a not in ids or b not in ids:
                    raise SystemExit(f"step range {part!r}: {a if a not in ids else b} not in chapter")
                wanted += ids[ids.index(a): ids.index(b) + 1]
            elif part:
                wanted.append(part)
    for s in wanted:
        if s not in ids:
            raise SystemExit(f"step {s!r} is not a heading in that chapter")
    return sorted(set(wanted), key=ids.index)


# ---------------------------------------------------------------- build

RANK = {"low": 0, "med": 1, "high": 2}


def build(cfg, captions):
    ids_by_chapter = manual_steps()
    playlist_id = cfg["playlist"]["list_id"]
    pl_videos = json.loads(PLAYLIST_JSON.read_text())["videos"]
    titles = {v["id"]: v["title"] for v in pl_videos}
    pl_order = {v["id"]: i for i, v in enumerate(pl_videos)}
    differs = cfg.get("differs", {})
    rows, unresolved = [], 0

    for seg in cfg["segments"]:
        chapter = seg["chapter"]
        if chapter not in ids_by_chapter:
            raise SystemExit(f"segment {seg['id']}: unknown chapter {chapter}")
        ids = ids_by_chapter[chapter]
        vid = seg["video"]
        if vid not in titles:
            raise SystemExit(f"segment {seg['id']}: {vid} is not in playlist.json")
        tokens = captions.get(vid)
        cap = RANK[seg.get("max_confidence", "high")]
        base = seg.get("confidence", "low")
        kw = seg.get("keywords") or {}
        note = " · ".join(differs[k] for k in seg.get("differs", []))

        for sid in expand(seg["steps"], ids):
            t, conf = seg["start"], base
            phrases = kw.get(sid)
            if phrases and tokens:
                hit, n = find(tokens, phrases, seg["start"], seg["end"])
                if hit is not None:
                    t = max(0, hit - 6)
                    conf = "high" if n >= 2 else "med"
                else:
                    unresolved += 1
            elif phrases and not tokens:
                unresolved += 1
            conf = min(RANK[conf], cap)
            conf = [k for k, v in RANK.items() if v == conf][0]
            rows.append({
                "chapter": chapter, "step": sid, "video": vid,
                "title": titles[vid], "t": int(t),
                "url": f"https://www.youtube.com/watch?v={vid}&list={playlist_id}&t={int(t)}s",
                "covers": seg["covers"], "confidence": conf, "differs": note,
                "seg_end": seg["end"],
                "order": (ids.index(sid), pl_order[vid], int(t)),
            })

    rows.sort(key=lambda r: (list(ids_by_chapter).index(r["chapter"]), r["order"]))
    return rows, unresolved


def write_manifest(cfg, rows):
    pl = json.loads(PLAYLIST_JSON.read_text())
    total = sum(v["duration"] or 0 for v in pl["videos"])
    per_chapter = {}
    for r in rows:
        per_chapter.setdefault(r["chapter"], set()).add(r["step"])
    ids_by_chapter = manual_steps()

    L = []
    A = L.append
    A("# Build-video manifest — Steve Builds, *LDO Voron 2.4 Kit Build*")
    A("")
    A(cfg["manifest"]["intro"].strip())
    A("")
    A("## The series")
    A("")
    A(f"| # | Part | Length | Uploaded | Chapters it covers |")
    A("|---|---|---|---|---|")
    covered = {}
    for r in rows:
        covered.setdefault(r["video"], set()).add(r["chapter"].split("-")[0])
    for i, v in enumerate(pl["videos"], 1):
        d = v["duration"] or 0
        ch = ", ".join(sorted(covered.get(v["id"], {"—"})))
        up = v["upload_date"]
        A(f"| {i} | [{v['title']}]({v['webpage_url']}) | {d // 3600}:{d % 3600 // 60:02d}:{d % 60:02d} "
          f"| {up[:4]}-{up[4:6]}-{up[6:]} | {ch} |")
    A("")
    A(f"**{len(pl['videos'])} videos · {total // 3600} h {total % 3600 // 60:02d} m total · "
      f"{len(rows)} step links · {len({r['step'] for r in rows})} distinct manual steps.**")
    A("")
    A("## Coverage per chapter")
    A("")
    A("| Chapter | Steps in chapter | Steps with a link | Coverage |")
    A("|---|---|---|---|")
    for chap, ids in ids_by_chapter.items():
        got = per_chapter.get(chap)
        if not got:
            continue
        A(f"| `{chap}` | {len(ids)} | {len(got)} | {100 * len(got) // len(ids)} % |")
    A("")
    A("## Step → video")
    A("")
    A("| Chapter | Step | Video | Link | Covers | Conf. | Differs from this kit |")
    A("|---|---|---|---|---|---|---|")
    for r in rows:
        short = r["title"].replace("LDO Voron 2.4 Kit Hangout and Build ", "").strip("()")
        t = r["t"]
        stamp = f"{t // 3600}:{t % 3600 // 60:02d}:{t % 60:02d}"
        if r["confidence"] == "low":
            # No phrase matched, so the link is the start of the whole segment.
            # Say how far past it the step can be, rather than implying precision.
            stamp += f" +{max(1, (r['seg_end'] - t + 59) // 60)}m"
        A(f"| `{r['chapter'].split('-')[0]}` | {r['step']} | {short} | [{stamp}]({r['url']}) "
          f"| {r['covers']} | {r['confidence']} | {r['differs'] or '—'} |")
    A("")
    A(cfg["manifest"]["outro"].strip())
    A("")
    MANIFEST.write_text("\n".join(L))


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--refresh", action="store_true", help="re-fetch metadata and captions with yt-dlp")
    ap.add_argument("--ytdlp", default="yt-dlp", help="path to a yt-dlp binary (scratch venv, not a project dep)")
    ap.add_argument("--cache", type=Path, default=DEFAULT_CACHE, help=f"caption cache dir (default {DEFAULT_CACHE})")
    args = ap.parse_args()

    cfg = yaml.safe_load(MAP_YML.read_text())
    if args.refresh:
        refresh(cfg, args.ytdlp, args.cache)
    if not PLAYLIST_JSON.exists():
        sys.exit("playlist.json missing — run with --refresh first")

    captions = load_captions(args.cache)
    if not captions:
        print(f"! no captions in {args.cache} — timestamps fall back to segment starts", file=sys.stderr)
    else:
        # A partial --refresh (YouTube answers 429 partway through a playlist)
        # leaves a video with no captions, and every one of its rows silently
        # drops to `low`. Say so rather than quietly losing precision.
        missing = [v["id"] for v in json.loads(PLAYLIST_JSON.read_text())["videos"]
                   if v["id"] not in captions]
        if missing:
            print(f"! no cached captions for {', '.join(missing)} — those rows fall back to "
                  f"segment starts; re-run --refresh", file=sys.stderr)
    rows, unresolved = build(cfg, captions)
    write_manifest(cfg, rows)
    print(f"MANIFEST.md: {len(rows)} rows, "
          f"{sum(r['confidence'] == 'high' for r in rows)} high / "
          f"{sum(r['confidence'] == 'med' for r in rows)} med / "
          f"{sum(r['confidence'] == 'low' for r in rows)} low"
          + (f", {unresolved} keyword sets found no caption hit" if unresolved else ""))


if __name__ == "__main__":
    main()
