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


STEP_HEAD = re.compile(r"^### Step (\S+) — (.*)$", re.M)


def chapter_state(repo, chapter, step_id):
    """(step title, what the step's image line currently is) from the chapter.

    Read-only. Chapters are owned by another pass and are being written
    concurrently, so the manifest records what was true when it was generated
    rather than assuming (no image - see text).
    """
    f = os.path.join(repo, "docs/manual", chapter)
    if not os.path.exists(f):
        return "(chapter not found)", "?"
    text = open(f, encoding="utf-8").read()
    heads = list(STEP_HEAD.finditer(text))
    for i, m in enumerate(heads):
        if m.group(1) != step_id:
            continue
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        block = text[m.start():end]
        imgs = re.findall(r"^!\[[^\]]*\]\(([^)]+)\)", block, re.M)
        if imgs:
            return m.group(2), " + ".join(imgs)
        if re.search(r"no image\s*—\s*see text", block):
            return m.group(2), "(no image — see text)"
        return m.group(2), "(no image line found)"
    return "(step heading not found)", "?"


def alt_of(title, mode, pair):
    """Alt text for one image. Where an entry produces both views, `b` says so —
    two identical alt texts on adjacent images help nobody."""
    tail = re.sub(r"^Step \S+ - ", "", (title or "")).strip()
    return f"CAD render — {tail}" + (", in place" if pair and mode == "b" else "")


def write_manifest(doc, out_dir, repo):
    d, byout = doc.get("defaults", {}), {}
    for e in doc["steps"]:
        byout.setdefault(e["out"], []).append(e)

    ROLE = {"a": "parts alone", "b": "in place, rest of the machine ghosted"}
    rows, blocks = [], []
    for out, es in byout.items():
        e0 = es[0]
        title, cur = chapter_state(repo, e0["chapter"], e0["step"])
        modes = [(e, m) for e in es for m in e.get("modes", ["a", "b"])]
        ready = "yes" if all(e.get("insert") for e in es) else "**no**"
        rows.append(f"| {e0['step']} | `{e0['chapter']}` "
                    f"| {', '.join(f'{out}-{m}.png' for _, m in modes)} "
                    f"| {cur} | {ready} |")

        lines = [f"### {e0['step']} — {title}", "",
                 f"Chapter `{e0['chapter']}` · currently shows: {cur}", ""]
        for e in es:
            ms = e.get("modes", ["a", "b"])
            names = " and ".join(f"**`{out}-{m}.png`** ({ROLE[m]})" for m in ms)
            lines += [f"{names} — {e.get('caption', '(no caption)')}", ""]

        n350 = next((e.get("note_350") for e in es if e.get("note_350")), None)
        lines += [f"**350 caveat:** {n350 or 'none - nothing in this image is size-dependent.'}", ""]

        have = [(e, m) for e, m in modes if f"assets/cad/{out}-{m}.png" in cur]
        todo = [(e, m) for e, m in modes if (e, m) not in have]
        if have:
            lines += ["Already in the chapter, do not add again: "
                      + ", ".join(f"`{out}-{m}.png`" for _, m in have), ""]
        if todo:
            lines += ["Image line(s) to add, immediately after the step heading:",
                      "", "```markdown"]
            for e, m in todo:
                lines.append(f"![{alt_of(entry_opt(e, d, 'title', m), m, len(e.get('modes', ['a','b'])) > 1)}]"
                             f"(assets/cad/{out}-{m}.png)")
            lines += ["```", ""]

        seen, look = set(), []
        for e in es:                      # a and b of one step often each say
            t = e.get("looking_at")       # something the other does not
            if t and t not in seen:
                seen.add(t); look.append(t)
        lines += ["**What you're looking at:** " + (" ".join(look) or "(none)"), ""]
        for e in es:
            if e.get("insert_note"):
                lines += [f"> {' '.join(e['insert_note'].split())}", ""]
        blocks.append("\n".join(lines))

    head = f"""# CAD render manifest

{len(byout)} manual steps illustrated from the official Voron 2.4r2 STEP
({len(doc['steps'])} manifest entries, {sum(len(e.get('modes', ['a', 'b'])) for e in doc['steps'])} PNGs).
Generated from `steps.yml` by `scripts/cad_render/render_steps.py --manifest` —
edit that file, not this one.

Two standing caveats apply to every image and are printed in every footer:

1. **The published CAD is the 250 machine.** Part identity, handedness, mounting
   faces and assembly relationships transfer to this 350 build; extrusion, rail
   and belt **lengths do not**. Per-image detail is in the *350 caveat* line below.
2. Anything labelled **(schematic)** is a box drawn by the renderer, not Voron
   geometry — the LDO Rev D+ and mod hardware (rail stops, titanium backers,
   the USB/ESD adapter) is absent from the Voron CAD.

## For the pass that inserts these

- `a` = the selected parts alone; `b` = the same parts in place with the rest of
  the machine ghosted. Where only one is listed, the other was judged to add
  nothing.
- Put the image line(s) directly under the `### Step` heading, replacing
  `(no image — see text)` where that is what the step still shows. Where the
  step already carries a manual page, a parts render or a bench photo, **add**
  these after it — do not replace the existing image.
- Every one of these steps already has a `**What you're looking at:**` line
  written by the chapter author. Fold the sentence below into it; do not add a
  second one.
- The *currently shows* column and the *already in the chapter* lines record the
  chapters as they stood when this file was generated, while they were still
  being written. Re-run `--manifest` and re-check before inserting.

## Index

| Step | Chapter | Images | Currently shows | Ready |
|---|---|---|---|---|
"""
    body = head + "\n".join(rows) + "\n\n## Per-step detail\n\n" + "\n".join(blocks)
    path = os.path.join(out_dir, "MANIFEST.md")
    open(path, "w", encoding="utf-8").write(body.rstrip() + "\n")
    print(f"wrote {path}  ({len(byout)} steps)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("steps", nargs="*", help="step ids to render (default: all)")
    ap.add_argument("--cache", default=os.environ.get("CACHE"))
    ap.add_argument("--yml", default=YML)
    ap.add_argument("--out", default=OUT)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--manifest", action="store_true",
                    help="regenerate MANIFEST.md from steps.yml and exit")
    ap.add_argument("--check-ids", action="store_true",
                    help="re-resolve every `resolve:` regex against the cache "
                         "and report drift from the pinned `ids:`")
    a = ap.parse_args()
    if not a.cache and not a.manifest:
        sys.exit("set CACHE=<mesh cache dir> (built by step_extract.py)")

    doc = yaml.safe_load(open(a.yml))
    d = doc.get("defaults", {})
    entries = doc["steps"]
    if a.steps:
        want = set(a.steps)
        entries = [e for e in entries if e["step"] in want or e["out"] in want]
        if not entries:
            sys.exit(f"no entry matches {sorted(want)}")

    if a.manifest:
        write_manifest(doc, a.out, REPO)
        return 0

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
