#!/usr/bin/env bash
# Re-render the five pilot step illustrations.
#   CACHE=<dir> PY=<python> bash scripts/cad_render/pilot_steps.sh
# CACHE is built once by:
#   python scripts/cad_render/step_extract.py Voron_2.4r2_Assembly.step --out CACHE
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/../.." && pwd)"
PY="${PY:-python3}"
CACHE="${CACHE:?set CACHE=<mesh cache dir>}"
OUT="${OUT:-$REPO/docs/manual/assets/cad}"
R="$PY $HERE/render.py --cache $CACHE"
NOTE="Voron 2.4r2 CAD (VoronDesign, GPL-3.0) @ de7e89d - 250 size; your kit is 350"
mkdir -p "$OUT"

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
$R --out "$OUT/05-46" --note "$NOTE" --only a \
  --select 'XY Joint - Right:1/D2F Microswitch Pod'   --offset ''         --label 'PRINT: [a]_endstop_pod_D2F_switch + XY PCB' \
  --select 'XY Joint - Right:1/Hall Effect Endstop'   --offset '0,0,-70'  --label 'SKIP: hall-effect pod (no hall endstops in this kit)' \
  --select 'XY Cable Chain Bridge - 2 Hole:1'         --offset ''         --label 'KEEP: xy_joint_cable_bridge_2hole' \
  --select 'XY Cable Chain Bridge - 3 Hole'           --offset '0,0,70'   --label 'BIN: 3-hole bridge' \
  --title 'Step 05.46 - the two Rev D+ variant choices, pulled apart' \
  --subtitle-a 'Both alternates are modelled in the same place in the CAD; separated here along Z.'
$R --out "$OUT/05-46" --note "$NOTE" --only b \
  --select 'XY Joint - Right:1/D2F Microswitch Pod' --label '[a]_endstop_pod_D2F_switch (bag for Ch 06)' \
  --select 'XY Cable Chain Bridge - 2 Hole:1'       --label 'xy_joint_cable_bridge_2hole' \
  --title 'Step 05.46 - where the two parts you keep end up' \
  --subtitle-b 'Right XY joint; rest of the gantry ghosted at 20%.' \
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
