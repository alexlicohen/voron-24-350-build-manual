# platearrange

Arranges 3D-printing parts on FDM build plates, packing them tightly around the bed centre.
It reads and writes PrusaSlicer `.3mf` projects. Self-contained: Python ≥ 3.9 and numpy; scipy
is optional and makes it about 2× faster (multi-threaded float32 FFTs).

```
python3 -m platearrange project.3mf -o arranged.3mf [--gap 6 --rot-step 5 --edge-margin 0
                                                     --res 0.5 --exclude X0,Y0,X1,Y1
                                                     --report report.json]
```

Run it from this directory, or `pip install .` first. The output is a copy of the project
in which only each build item's `transform` attribute changes. When the parts need more
than one bed, nothing is written. The report and stderr list which part goes on which bed,
and the exit status is 3. Splitting a project across beds is out of scope for v1.

If the project prints a skirt, set `--edge-margin` to at least `skirt_distance` plus the
skirt width. The CLI prints a note when it is too small.

## API

```python
from platearrange import Item, arrange, arrange_detailed, read_3mf, write_3mf

items = [Item(id="bracket", vertices=V, triangles=T, brim=3.1)]   # V (n,3), T (m,3)
placements = arrange(items, bed=(250, 220), gap=6.0, rot_step=5.0, edge_margin=0.0,
                     exclusions=[(100, 0, 150, 20)], res=0.5)
# Placement(item_id, bed, rot_deg, x, y): world XY = Rz(rot_deg) @ item XY + (x, y)

res = arrange_detailed(items, ...)      # + .beds, .strategy, .piles (part+brim bbox per bed)
pr = read_3mf("p.3mf")                  # items, bed polygon, config; pr.to_items()
write_3mf("p.3mf", "out.3mf", res.placements)
```

- `bed` is `(w, h)` for `[0, w] × [0, h]`, or a polygon in bed coordinates. A 3MF's
  `bed_shape` is such a polygon, and an axis-aligned one is treated as a rectangle.
- `brim` is the brim's reach from the part. For PrusaSlicer that is `brim_width +
  brim_separation`, and `read_3mf` works it out per object.
- Parts with identical meshes share their footprints, wherever they sit on the bed.
- `NoFit` is raised when a part does not fit an empty bed in any rotation, or when
  `max_beds` is too small.

## How it works

**Footprint.** A part's footprint is the top-down silhouette of its mesh: the union of every
projected triangle, not only the bottom face, so overhangs count. It is rasterised
conservatively at `res` mm: every cell the closed silhouette overlaps is set, so a
measured clearance is never optimistic. The first layer (the mesh below `zmin +
first_layer`, clipped exactly) is rasterised separately, because the brim grows from the
first layer and not from an overhang.

**Rotation.** Parts turn about Z only, never onto another face. Candidate rotations are
every multiple of `rot_step`, and 0/90/180/270 are always included and exact. Each
rotation rotates the mesh vertices and rasterises again; the raster is never rotated, so
no error accumulates. Each rotated silhouette is snapped so that its bounding-box corner
falls on a cell corner, which means a part costs `ceil(width/res)` cells and never one
more.

**Clearance.** Each part's clearance raster is

    silhouette ⊕ E(gap/2)  ∪  first layer ⊕ E(gap/2 + brim)

`E(ρ)` holds the cells whose squares are closer than ρ to a set cell. If two parts were
closer than ρa + ρb, some patch of bed would lie inside both dilations. So two clearance
rasters that share no cell prove that the parts are ≥ `gap` apart, and the brims are too.
The brim's footprint (silhouette ∪ first layer ⊕ brim) has to fit inside the bed less
`edge_margin`, and that test uses the exact rotated extents, not the raster. The gap/2
halo may hang over the edge. Exclusion zones are occupied cells, so parts keep `gap/2`
away from them.

**Feasibility.** For one part on one bed, every collision-free position for every
rotation comes out of a single batched FFT cross-correlation: the occupied raster
correlated with the part's clearance raster. A count below 0.5 means free. The chosen
cell is re-checked with an exact boolean AND before the part is committed.

**Beds.** Parts are placed largest first. Each one goes on the first bed where it fits
(first-fit-decreasing), and a new bed opens only when it fits on none. The result
reports each part's bed and the number of beds.

**Deterministic.** The same input always gives the same output: there is no randomness,
and ties go to the lowest rotation index, then the lowest row and column.

## Objective

At each step every feasible (rotation, position) gets a score, and the lowest score wins.
All terms are normalised to the usable bed (`uw × uh`, half diagonal `hd`):

    score = 1.0 · W·H / (uw·uh)               W, H: bbox of the pile including this part
          + 0.5 · max(W/uw, H/uh)             (keeps the pile in the bed's proportions)
          + 0.1 · |part centre − sink| / diag
          + ρ   · max(pile radius, |farthest part corner − sink|) / hd

ρ is 0 for the `box` objective and 0.5 for `round`. The sink is the bed centre (`centre`)
or the usable bed's front-left corner (`corner`). The pile bbox includes brims. When a part
fits inside the current pile's bbox, the first two terms do not change, so the centre
term places it in the hole nearest the sink, such as the notch of a C-shaped part.

There are 8 strategies: objective {box, round} × order {area-descending, longest side
descending} × sink {centre, corner}. All 8 run, and the one kept is ranked first by bed
count, then by the translation-invariant pile metric

    W·H/(uw·uh) + 0.5·max(W/uw, H/uh) + 0.1·mean d/diag + 0.5·max d/hd

where d is each part's bbox-centre distance from the pile's bbox centre. Each bed's pile
is then moved so its bbox centre sits on the bed centre, clamped to the bed. With
exclusions or a polygon bed it moves in whole cells and is re-checked.

If the best result needs more beds than the parts' total area requires, the 8 strategies
run again with rotations limited to {0, 180}, then to {0, 90, 180, 270}. A greedy that may
turn every part can wall off the slot a later part needed. Four 120 × 100 boxes on a
250 × 220 bed are the test case for this.

`improve=N` adds N passes that lift each part and re-place it on the rest of the pile,
keeping a move only when the pile metric improves. It is off by default: on the repo
plates it gained under 1 % for twice the time.

### Why this approximates PrusaSlicer

These points were checked against the PrusaSlicer 2.9.6 source
(`src/slic3r-arrange/include/arrange/NFP/Kernels/TMArrangeKernel.hpp`,
`src/slic3r-arrange-wrapper/src/ArrangeImpl.hpp`, `include/arrange-wrapper/Scene.hpp`,
`src/SceneBuilder.cpp`):

| PrusaSlicer 2.9.6 arrange | platearrange |
|---|---|
| Parts are sorted by priority, then by convex-hull area, largest first | Area-descending (silhouette) or longest-side-descending order |
| First-fit over beds | First-fit-decreasing over beds |
| `TMArrangeKernel` for a big part (> 2 % of the bed): `0.6·d + 0.1·a + (1−R)·0.3·d + R·0.3·a`, where d is the distance from the part's centroid to the centre of the pile bbox (seeded at the bed centre) / √bed area, a is alignment with same-area neighbours, and R is the share of parts left. A small part scores its distance to the big-items bbox centre | Pile bbox area and larger side, plus the distance to the sink. Both pull each part into the pile around the centre; platearrange scores the bbox directly, so piles come out rectangular, where PrusaSlicer's come out round |
| Rectangular bed: the pile is packed on an unbounded bed with a penalty for overfitting it (`RectangleOverfitKernelWrapper`), then translated so its bbox centre sits on the bed centre and clamped to the bed | Placement is limited to the bed, then the pile bbox is centred on the bed and clamped |
| Spacing: each object outline is inflated by `d_obj/2` (default `d_obj` = 6 mm). The bed is inset by `max(d_bed, skirt + max brim)`, and brims are **not** added between objects | Each part is inflated by `gap/2 + its own brim`, so the bare bed between two brims is ≥ `gap`. This is stricter than PrusaSlicer, whose 3 mm brims can meet across a 6 mm gap |
| Brim reach = `brim_width + brim_separation` for outer brims | The same (`read_3mf`) |
| Rotations, when enabled: the min-area-bbox angle, that angle + 45°, 90°, 135° and 180°, the original angle, and a fit-into-bed angle | Every `rot_step` degrees, plus exact 0/90/180/270 |
| NFP (no-fit polygons) from convex or concave outlines | Raster cross-correlation, conservative to about one cell per part |

## Tests

```
python3 -m pytest -q tools/platearrange/tests
```

The tests check overlap and on-bed placement independently of the packer's raster, in two
ways: pure-Python rotated-rectangle polygon distances, and `platearrange.measure`, which
uses exact vector geometry on the projected outline segments. They also cover exact 90°
rotation, a small part placed in a C-shaped part's notch, a single part centred,
determinism, overflow to a second bed, exclusions, a polygon bed, a brim that grows from
the first layer only, and a 3MF round trip with every non-transform member byte-identical.
