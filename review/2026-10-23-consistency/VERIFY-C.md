# VERIFY-C — Ch 11 / Ch 13 (agent C, 2026-10-23)

Files edited: docs/manual/11-skirts-panels-door.md, docs/manual/13-initial-startup.md. Held items (13.1–13.3 bay/LED checks, 13.8, SSR-LED What-if rows 1722–1723, Checkpoint 13 SSR line) and 13.24 untouched.
Lint: `lint_manual.py --strict-parts --chapters 11,13` exit 0 (check 6 0, check 7 0); `--budgets-only` shows nothing in Ch 11/13 (only the existing 00.8 cross-ref finding); `--no-budgets` 0 findings. No mkdocs build run (brief).

## G6-03 — 13.39 "still hot" after SAVE_CONFIG — CONFIRMED
- Source: Klipper @ f0892d8 (the chapter's pinned commit). `klippy/configfile.py:403` `cmd_SAVE_CONFIG` → `gcode.request_restart('restart')`; `klippy/gcode.py:352-361` `request_restart` sends `gcode:request_restart`; `klippy/extras/heaters.py:253-254` registers `turn_off_all_heaters` on that event; the new host's `Heater` starts `target_temp = 0.` (heaters.py:46). docs/G-Codes.md:277 "SAVE_CONFIG … restart the host software". `FIRMWARE_RESTART` (13.38 Do) takes the same `request_restart` path.
- Second cause the report missed: 13.38 itself ends with `FIRMWARE_RESTART`, so 13.39 is cold even without 13.36.
- Changes: 13-initial-startup.md:1075–1079 (13.39 Do → 3 items: both restarts turned heaters off; `SET_IDLE_TIMEOUT TIMEOUT=7200`, bed 100 / hotend 150; soak the 13.32 time; `G28`, QGL, `G28`, `BED_MESH_CALIBRATE`). :972 (13.35 Tip → "Stay hot through 13.36; its `SAVE_CONFIG` turns the heaters off, and 13.39 re-heats."). Checkpoint 13 "mesh taken hot" now true as written; not edited.

## G6-02 — 11.52 opens the bay without unplug / 0 V — CONFIRMED
- Source: 00a-mains-safety.md 00a.11 ⚠ "To look or touch: power off, unplug, read 0 V held ten seconds, as at 10.73". 13.43 Do 2 ends "switch the machine off at the inlet" and 13.54 "shut down as before": cord stays in. 11.21 makes the bottom panel the bay door; 11.67 and 14-calibration.md 14.30 do the full ritual before opening it.
- Changes: 11-skirts-panels-door.md:1538–1542 (11.52 Do 1 "Unplug wall, then inlet. On its side, open the bottom panel; meter +V to −V."; items 2–3 compressed to fit 40 words; Check leads "Meter held 0 V for ten seconds first."); Source line gains 11.67 and 00a.11 links; **Helper line removed** (a confirm-dead step is a mains step: 11.67, 10.73, 14.30 are all in NO_MASCOT "mains").
- **Needed from the orchestrator (not my file):** hooks/mascot.py `NO_MASCOT_STEPS["mains"]`: add `11.52`, e.g. `"10.73 10.77 10.78 10.80 11.52 11.67 12.11 13.2 13.3 13.8 14.30-14.32"`. Not adding it does not break the build (no Helper remains), but the badges would stay on a mains step.
- Not done: optional Checkpoint 11 Part B line (reviewer marked optional).

## G1-05 — "power down" before connector swaps at the board — CONFIRMED
- Source: 00a.11 ⚠ touch rule (above); 00a.2 "not in the room … while the machine is plugged in with the bay open"; 11.67 ⚠ says the next plug-in is 13.3 "with the bay closed", so any swap at the Leviathan in Ch 13 reopens the bay. 14.30 is the project's own template.
- Changes, 13-initial-startup.md: :54 Read first defines it once (Pi shut down, rocker off, unplug wall then inlet, cord out; on its side, open the panel, meter +V to −V 0 V held 10 s as at 11.67; swap, close, power on as at 13.3, one adult). Rows :451, :649, :1721, :1729 point at 11.67's 0 V ritual. Same-finding siblings with the same wording, also fixed: :452 (13.16 "Power the machine down"), :1727 (What-if "Power off first"), Common mistakes ~:1789 ("Power down for every connector change"). SSR-LED rows untouched (held).
- Optional for the orchestrator: 13.16 and 13.23 now include the unplug-and-meter ritual as a conditional fix; neither carries a Helper, so NO_MASCOT is unaffected; listing them as "mains" is a judgement call.

## G1-03 (13.3 part) — "two people" at power-on — CONFIRMED
- Source: 00a.2 "She is not beside the machine at any power-on — 10.23, 12.11 and 13.3. One adult, standing to the side, hand on the switch — nobody else within reach of the machine."
- Change: 13-initial-startup.md:135 Do 1 → "One adult at the switch; nobody else within reach." Check, ⚠ and LED checks untouched (held).
- Seen, not in scope: 13.22 Do 1 "Two people: one owns the stop, one watches, hands out." 13.22 is not a power-on, so 00a.2's power-on line does not forbid it; no edit.
