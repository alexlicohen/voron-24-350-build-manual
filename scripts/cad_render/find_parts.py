#!/usr/bin/env python3
"""Query the mesh cache index: `find_parts.py CACHE REGEX [-t] [-n N]`.
-t groups by assembly path prefix instead of listing leaves."""
import json, re, sys, argparse, collections
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("cache"); ap.add_argument("pattern")
ap.add_argument("-n", type=int, default=40)
ap.add_argument("-t", action="store_true", help="group by path prefix")
ap.add_argument("-d", type=int, default=4, help="prefix depth for -t")
ap.add_argument("-b", action="store_true", help="show bbox + size")
a = ap.parse_args()

d = json.load(open(f"{a.cache}/index.json"))
rx = re.compile(a.pattern, re.I)
hits = [r for r in d if rx.search(r["path"])]
print(f"{len(hits)} hit(s) for /{a.pattern}/")
if a.t:
    g = collections.Counter("/".join(r["path"].split("/")[:a.d]) for r in hits)
    for k, v in sorted(g.items()):
        print(f"{v:5d}  {k}")
else:
    for r in hits[:a.n]:
        s = ""
        if a.b:
            b = np.array(r["bbox"]); s = f"  size={np.round(b[3:]-b[:3],1)} at {np.round(b[:3],1)}"
        print(f"{r['id']:5d} {r['tris']:6d}  {r['path']}{s}")
    if len(hits) > a.n:
        print(f"... {len(hits)-a.n} more")
