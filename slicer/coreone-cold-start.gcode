M17 ; enable steppers
M862.1 P[nozzle_diameter] A{(filament_abrasive[0] ? 1 : 0)} F{(nozzle_high_flow[0] ? 1 : 0)} ; nozzle check
M862.3 P "COREONE" ; printer model check
M862.5 P2 ; g-code level check
M862.6 P"Input shaper" ; FW feature check
M115 U6.8.1+16182

M555 X{(min(print_bed_max[0], first_layer_print_min[0] + 32) - 32)} Y{(max(0, first_layer_print_min[1]) - 4)} W{((min(print_bed_max[0], max(first_layer_print_min[0] + 32, first_layer_print_max[0])))) - ((min(print_bed_max[0], first_layer_print_min[0] + 32) - 32))} H{((first_layer_print_max[1])) - ((max(0, first_layer_print_min[1]) - 4))}

G90 ; use absolute coordinates
M83 ; extruder relative mode

{if chamber_minimal_temperature[initial_tool]!=0}
M140 S115 ; set bed temp for chamber heating
{else}
M140 S[first_layer_bed_temperature] ; set bed temp
{endif}

M104 S0 ; cold nozzle for homing and probing (loadcell noise workaround)

M84 E ; turn off E motor

G28 ; home all without mesh bed level

{if chamber_minimal_temperature[initial_tool]!=0}
; Min chamber temp section
M104 S0 ; keep nozzle cold
G1 Z10 F720 ; set bed position
G1 X242 Y-9 F4800 ; set print head position
M191 S{chamber_minimal_temperature[initial_tool]} ; wait for minimal chamber temp
M141 S{chamber_temperature[initial_tool]} ; set nominal chamber temp
M107
M140 S[first_layer_bed_temperature] ; set bed temp
{else}
M141 S{chamber_temperature[initial_tool]} ; set nominal chamber temp
{endif}

{if first_layer_bed_temperature[initial_tool]<=60}M106 S70{endif}
G0 Z40 F10000
M104 T{initial_tool} S0 ; keep nozzle cold
M190 R[first_layer_bed_temperature] ; wait for bed temp
M107

G29 G ; absorb heat

M104 S0 ; cold nozzle for MBL

M84 E ; turn off E motor

; nozzle cleaning (G29 P9) removed: nozzle is cold here, clean the tip by hand while hot

;
; MBL
;
M84 E ; turn off E motor
G29 P1 ; invalidate mbl & probe print area
G29 P1 X150 Y0 W100 H20 C ; probe near purge place
G29 P3.2 ; interpolate mbl probes
G29 P3.13 ; extrapolate mbl outside probe area
G29 A ; activate mbl

; prepare for purge
M104 S{first_layer_temperature[0]}
G0 X249 Y-2.5 Z15 F4800 ; move away and ready for the purge
M109 S{first_layer_temperature[0]}

G92 E0
M569 S0 E ; set spreadcycle mode for extruder

M591 S0 ; disable stuck detection

;
; Extrude purge line
;
G92 E0 ; reset extruder position
G0 E5 X235 Z0.2 F500 ; purge
G0 X225 E4 F500 ; purge
G0 X215 E4 F650 ; purge
G0 X205 E4 F800 ; purge
G0 X202 Z0.05 F8000 ; wipe, move close to the bed
G0 X199 Z0.2 F8000 ; wipe, move quickly away from the bed

M591 R ; restore stuck detection

G92 E0
M221 S100 ; set flow to 100%
