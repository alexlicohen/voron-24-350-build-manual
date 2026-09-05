#!/usr/bin/env python3
"""Render every entry in docs/manual/assets/cad/steps.yml.

    CACHE=<mesh cache> python3 scripts/cad_render/render_steps.py [STEP ...]

Replaces pilot_steps.sh (PILOT.md §7.2): the YAML manifest is the reviewable
artefact, the PNGs are derived. One Scene is loaded for the whole run, so the
64 MB mesh cache is mmapped once instead of once per image.

Deterministic: same cache + same steps.yml -> byte-identical PNGs.
"""
import argparse, os, re, sys, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import yaml

import render as R

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
YML = os.path.join(REPO, "docs/manual/assets/cad/steps.yml")
OUT = os.path.join(REPO, "docs/manual/assets/cad")


def entry_opt(e, d, key, mode=None):
    """`key_a` / `key_b` beat `key`, which beats the file-level default."""
    if mode and f"{key}_{mode}" in e:
        return e[f"{key}_{mode}"]
    if key in e:
        return e[key]
    return d.get(key)


def build_selection(scene, e):
    """(selections, shift) in manifest order; boxes last, as main() does."""
    pats, labels, offsets = [], [], []
    for s in e.get("select", []):
        if "ids" in s:
            pats.append("ids:" + ",".join(str(i) for i in s["ids"]))
        else:
            pats.append(s["resolve"])
        labels.append(s.get("label", pats[-1]))
        offsets.append(s.get("offset", ""))
    sel = scene.select(pats)
    shift = {}
    for k, off in enumerate(offsets):
        if off:
            d = [float(x) for x in off.split(",")]
            for i in sel[k][1]:
                shift[i] = d
    sel = [(labels[i], ids) for i, (_, ids) in enumerate(sel)]
    for b in e.get("boxes", []):
        pids = [scene.add_box(g) for g in b["geom"].split(";") if g.strip()]
        sel.append((b["label"], pids))
    return sel, shift


def reset_boxes(scene):
    """Schematic boxes get negative pseudo-ids counted from -1, so they have to
    be cleared between entries or the ids drift and the render stops being a
    function of the entry alone."""
    for pid in list(scene.by_id):
        if pid < 0:
            del scene.by_id[pid]
    scene.boxes.clear()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("steps", nargs="*", help="step ids to render (default: all)")
    ap.add_argument("--cache", default=os.environ.get("CACHE"))
    ap.add_argument("--yml", default=YML)
    ap.add_argument("--out", default=OUT)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--check-ids", action="store_true",
                    help="re-resolve every `resolve:` regex against the cache "
                         "and report drift from the pinned `ids:`")
    a = ap.parse_args()
    if not a.cache:
        sys.exit("set CACHE=<mesh cache dir> (built by step_extract.py)")

    doc = yaml.safe_load(open(a.yml))
    d = doc.get("defaults", {})
    entries = doc["steps"]
    if a.steps:
        want = set(a.steps)
        entries = [e for e in entries if e["step"] in want or e["out"] in want]
        if not entries:
            sys.exit(f"no entry matches {sorted(want)}")

    scene = R.Scene(a.cache)
    print(f"cache: {len(scene.index)} parts", flush=True)

    if a.check_ids:
        bad = 0
        for e in entries:
            for s in e.get("select", []):
                if "ids" not in s or "resolve" not in s:
                    continue
                rx = re.compile(s["resolve"], re.I)
                got = [r["id"] for r in scene.index if rx.search(r["path"])]
                if got != list(s["ids"]):
                    bad += 1
                    print(f"DRIFT {e['step']:8s} {s['label'][:44]!r}\n"
                          f"      pinned  {list(s['ids'])}\n"
                          f"      resolve {got}")
        print(f"\n{'FAIL' if bad else 'OK'}: {bad} selection(s) drifted")
        return 1 if bad else 0

    t0, n = time.time(), 0
    for e in entries:
        stem = os.path.join(a.out, e["out"])
        reset_boxes(scene)
        sel, shift = build_selection(scene, e)
        print(f"\n== {e['step']}  -> {e['out']}", flush=True)
        for label, ids in sel:
            print(f"   {label}: {len(ids)} part(s)", flush=True)
        if a.dry_run:
            continue
        for mode in e.get("modes", ["a", "b"]):
            ge = entry_opt(e, d, "ghost_exclude", mode)
            frame = entry_opt(e, d, "frame", mode)
            R.render(
                scene, sel, f"{stem}-{mode}.png", mode,
                float(entry_opt(e, d, "azim", mode)),
                float(entry_opt(e, d, "elev", mode)),
                int(entry_opt(e, d, "width", mode)),
                int(entry_opt(e, d, "height", mode)),
                int(entry_opt(e, d, "ss", mode)),
                float(entry_opt(e, d, "context_scale", mode)),
                title=entry_opt(e, d, "title", mode),
                subtitle=entry_opt(e, d, "subtitle", mode),
                note=entry_opt(e, d, "note", mode),
                shift=shift,
                ghost_exclude=re.compile(ge, re.I) if ge else None,
                frame=(np.array([float(x) for x in frame.split(",")])
                       if frame else None),
            )
            n += 1
    print(f"\n{n} image(s) in {time.time()-t0:.1f}s", flush=True)


if __name__ == "__main__":
    sys.exit(main() or 0)
