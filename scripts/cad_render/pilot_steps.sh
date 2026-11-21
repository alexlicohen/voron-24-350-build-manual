#!/usr/bin/env bash
# CLI regression for the CAD step renders (PILOT.md §9): the five pilot steps
# plus 01.15, written as hand-made render.py calls. Each block must match its
# docs/manual/assets/cad/steps.yml entry, so this script and
#   CACHE=<dir> python scripts/cad_render/render_steps.py 01.15 02.10 05.18 05.45 05.46 09.26
# write byte-identical PNGs. render_steps.py is the tool; this script checks
# that the CLI and the manifest still agree. Render into scratch and cmp:
#   CACHE=<dir> PY=venv-cq/bin/python OUT=<scratch> bash scripts/cad_render/pilot_steps.sh
# CACHE is built once by:
#   python scripts/cad_render/step_extract.py Voron_2.4r2_Assembly.step --out CACHE
# Per --select, in order ('' = none): --offset 'dx,dy,dz', --anchor 'x,y,z'
# (CAD mm, before the offset) and --label-y 0..1 = steps.yml offset/anchor/label_y.
# A label with a line break needs bash $'...\n...' quoting; a value that starts
# with '-' needs the --anchor=... form or argparse reads it as an option.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/../.." && pwd)"
PY="${PY:-python3}"
CACHE="${CACHE:?set CACHE=<mesh cache dir>}"
OUT="${OUT:-$REPO/docs/manual/assets/cad}"
R="$PY $HERE/render.py --cache $CACHE"
NOTE="Voron 2.4r2 CAD (VoronDesign, GPL-3.0) @ de7e89d - 250 size; your kit is 350"
mkdir -p "$OUT"

# --- 01.15  frame on the reference surface (anchor / label-y) -----------------
# Long frame rails: the pixel-median leader lands mid-rail, so three groups
# are anchored on the corner the label names and all four labels are placed.
$R --out "$OUT/01-15" --note "$NOTE" --only a \
  --select 'Frame:1/Bottom Extrusions:1/[^/]+/=>' \
    --label 'four bottom corners - all four must stay in contact' \
    --anchor='-78,-38,-48' --label-y 0.90 \
  --select 'Frame:1/Top Extrusions:1/[^/]+/=>' \
    --label $'press each TOP corner in turn;\nrock between diagonals = twist' \
    --anchor '332,372,362' --label-y 0.13 \
  --select 'Frame:1/Verticals Extrusions:1/HFSB5-2020-430-LCP-RCP[^/]*/=>\[' \
    --label 'B verticals x4' \
    --anchor '' --label-y 0.50 \
  --select 'Frame:1/Bed Supports:1/HFSB5[^/]*/=>' \
    --label $'bed extrusions (Step 01.16):\nnot a contact point' \
    --anchor '202,330,-28' --label-y 0.66 \
  --title 'Step 01.15 - the frame on the reference surface' \
  --subtitle-a 'All four bottom corners touch at once, or the frame is twisted. Press the top corners in turn.'

# --- 02.10  LDO rail stops at the top of each Z rail -------------------------
$R --out "$OUT/02-10" --note "$NOTE" \
  --select 'HFSB5-2020-430-LCP-RCP \(3\):1/=>'                 --label '2020 vertical extrusion (rear right)' \
  --select 'HFSB5-2020-430-LCP-RCP \(3\):1/MGN9 - 300mm:1/=>'  --label 'MGN9 Z rail - top end at rail z-max' \
  --select 'Z Joint with Hall Effect:1/MGN9H \(5\):1'          --label 'MGN9H Z carriage (must not run off the top)' \
  --box    '314,343,264.5,330,354,280:z_rail_stop_x4 (LDO, schematic - not in Voron CAD)' \
  --title 'Step 02.10 - LDO rail stop at the top of a Z rail' \
  --subtitle-a 'One of four; top 150 mm of the rail. The stop clips over the free top end.' \
  --frame-a '300,335,175,345,385,290' \
  --subtitle-b 'Same parts in the frame; rest of the machine ghosted at 20%.' \
  --ghost-exclude 'Panels|Skirt' --context-scale 1.25

# --- 05.18  second titanium Y backer ----------------------------------------
# (a) one beam from below: the two faces that matter are both in frame
$R --out "$OUT/05-18" --note "$NOTE" --only a --elev -24 \
  --select 'Gantry Extrusions:1/HFSB5-2020-350:1/=>'                     --label 'C extrusion (Y beam)' \
  --select 'Gantry Extrusions:1/HFSB5-2020-350:1/MGN9 - 300mm[^/]*:1/=>' --label 'MGN9 rail is on THIS face' \
  --box    '313,8,88,331,326,91:titanium Y backer goes on the OPPOSITE face (schematic)' \
  --title 'Step 05.18 - the backer goes on the face opposite the rail' \
  --subtitle-a 'One Y beam seen from below. The backer is drawn schematically: it is not in the Voron CAD.'
# (b) both beams in the gantry, house isometric, panels/skirt out of the ghost
$R --out "$OUT/05-18" --note "$NOTE" --only b --ghost-exclude 'Panels|Skirt|Exhaust' \
  --select 'Gantry Extrusions:1/HFSB5-2020-350[^/]*:1/=>'                        --label 'C extrusion (Y beam) x2' \
  --select 'Gantry Extrusions:1/HFSB5-2020-350[^/]*:1/MGN9 - 300mm[^/]*:1/=>'    --label 'MGN9 rails (underneath)' \
  --box    '313,8,88,331,326,91;-77,8,88,-59,326,91:both Y backers, top faces, mirrored (schematic)' \
  --title 'Step 05.18 - both Y backers, mirrored, on the top faces' \
  --subtitle-b 'Gantry from the house isometric; rest of the machine ghosted at 20%.' \
  --context-scale 1.25

# --- 05.45  X-carriage frame halves -----------------------------------------
$R --out "$OUT/05-45" --note "$NOTE" \
  --select 'X_Carriage_Printed:1/x_carriage_frame_left'   --label 'x_frame_V2TR_MGN12_left' \
  --select 'X_Carriage_Printed:1/x_carriage_frame_right'  --label 'x_frame_V2TR_MGN12_right' \
  --select 'probe_bracket:1/Part38'                       --label 'probe_retainer_bracket' \
  --select 'MGN12H \(1\):1/PRODUCT_NAME_1'                --label 'MGN12H carriage - check the bolt pattern here' \
  --title 'Step 05.45 - stage the X-carriage frame halves' \
  --subtitle-a 'The two halves are handed and are not interchangeable with pre-CW2 carriages.' \
  --subtitle-b 'Where they end up in Ch 07/08; toolhead and X beam ghosted at 20%.' \
  --context-scale 2.6

# --- 05.46  which endstop pod / which cable bridge ---------------------------
# Labels say what each part is AT this step: the pod is already fitted (05.49
# comes first), the joint carries the raised bridge from 05.38, the stock
# 2-hole bridge drawn here is the bagged spare, hall pod and 3-hole bridge were
# never printed. No "BIN": in this manual a bin is a storage bin.
$R --out "$OUT/05-46" --note "$NOTE" --only a \
  --select 'XY Joint - Right:1/D2F Microswitch Pod'   --offset '' \
    --label $'FITTED at Step 05.49: [a]_endstop_pod_D2F_switch\n+ XY endstop board' \
  --select 'XY Joint - Right:1/Hall Effect Endstop'   --offset '0,0,-70' \
    --label $'NOT PRINTED: hall-effect pod\n(this kit has no hall endstops)' \
  --select 'XY Cable Chain Bridge - 2 Hole:1'         --offset '' \
    --label $'2-hole bridge, stock: BAG it as the spare.\nYour joint carries the raised one (Step 05.38)' \
  --select 'XY Cable Chain Bridge - 3 Hole'           --offset '0,0,70' \
    --label $'NOT PRINTED: 3-hole bridge\n(LDO\'s chain ends are 2-hole)' \
  --title 'Step 05.46 - the two Rev D+ variant choices, pulled apart' \
  --subtitle-a 'Both alternates are modelled in the same place in the CAD; separated here along Z.'
$R --out "$OUT/05-46" --note "$NOTE" --only b \
  --select 'XY Joint - Right:1/D2F Microswitch Pod' --label '[a]_endstop_pod_D2F_switch (fitted at Step 05.49)' \
  --select 'XY Cable Chain Bridge - 2 Hole:1' \
    --label $'cable bridge (Step 05.38): yours is the raised\n2-hole one, 3 mm taller than drawn' \
  --title 'Step 05.46 - where the pod and the cable bridge sit' \
  --subtitle-b 'Right XY joint, machine the right way up (on your bench the gantry is upside down); rest ghosted at 20%.' \
  --ghost-exclude 'Panels|Skirt' --context-scale 2.4

# --- 09.26  USB/ESD adapter on the front DIN rail ---------------------------
$R --out "$OUT/09-26" --note "$NOTE" \
  --select 'Electronics:1/DIN3 Rail \(2\):1'  --label 'FRONT DIN rail - adapter clips at its right-hand end' \
  --select 'Electronics:1/DIN3 Rail:1'        --label 'rear DIN rail (PSU / SSR side)' \
  --box    '255,92,-80,300,120,-49.6:LDO USB/ESD adapter (schematic - not in Voron CAD)' \
  --title 'Step 09.26 - clip the USB adapter to the front rail' \
  --subtitle-a 'Both bay rails run left-to-right; front = nearer the door.' \
  --subtitle-b 'Seen through the deck: bay and frame ghosted at 20%.' \
  --ghost-exclude 'Transparent Panels|Skirt' --context-scale 2.2
