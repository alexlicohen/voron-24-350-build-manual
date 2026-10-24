# Safety rulings 2026-10-23: implementation log

Files: `docs/manual/00a-mains-safety.md`, `docs/manual/12-software.md`, `docs/manual/13-initial-startup.md`, `hooks/mascot.py`. Line numbers are post-edit, at the 056b8e8a base plus this change.

## Ruling 1: Ch 13 live bay checks, "ok to look, don't touch, while on" (G6-01, G5-5)

Evidence: Ch 11.21 bottom panel = opaque 4 mm acrylic door, rear hinges, front clips, "swings down". LDO `VS9_Final.jpg` (00a.6) shows the bay from below: the PSU, SSR and Pi LEDs face the bottom panel. Klipper `stepper_enable.py` @ f0892d8: `is_enabled = False` until the first move. So no motor holds current at 13.3.

Design: one bounded eyes-only window, 13.3 to 13.8. The door is swung down and the machine is put on its side at 13.2, dead and proven 0 V. 13.8 ends the window: Pi shutdown, unplug, 0 V held, door closed, machine stood upright. 13.9 is a closed-bay power-on.

- 13: :21 prereq note; :54 Read-first re-power → 13.9; :86 13.1 Check drops bay/PSU; :102–107 13.2 Do (cord out, on its side, door down, 0 V) + PSU row in table; :113 Check; :121 Pause; :137 13.3 Do 3 "Look into the bay"; :143 new ⚠ eyes-only, she out of the room; :145 Tip rewritten (no touching; motors are disabled at idle); 13.3 Source + 00a.11 + Klipper link; Helper lines removed from 13.5 and 13.6 (inside the window); :259–265 13.8 Do/Check/⚠ (window close-out, door shut after 0 V); :281 13.9 Do power-on, door shut; :653 and What-if "wrong motor" re-power → 13.9; :1726–1727 SSR-LED What-if rows → finish 13.8's shut-down to 0 V first, mains side = 00a.1 person; :1769 Checkpoint line; :1251/:1255 13.43 → Mainsail-loses-printer + one minute (Pi LED is behind the closed door).
- 00a: :83 adult-only list adds 12.15 press and 13.3→13.8; :84 power-ons add 13.9 and later; :323 why-paragraph; :327 Do = three windows; :329 Check; :332 Ritual 2 adds 13.9 (closed-bay observations); :333 eyes-only rule bullet; :336 ⚠; :379, :387 Checkpoint lines.
- `hooks/mascot.py:116` mains list `13.2 13.3 13.8` → `13.2-13.9` (+ comment :106).

## Ruling 2: Leviathan flashing, "keep with whatever LDO typically does" (G5-2)

Primary sources, fetched 2026-10-23:
- LDO Rev D wiring guide § Mainboard Firmware Setup: "The Leviathan board is pre-programmed when you receive it. If you need to update Klipper firmware, follow [the Leviathan V1.3 guide]".
- LDO Leviathan V1.3 guide (ldomotion.com/guides/voron-leviathan-v1-3): "Leviathan boards ship out already flashed with USB firmware." § Flashing Klipper: "if not, press the SW1 button twice quickly to activate the bootloader". § DFU: "The device should be wired as shown and powered on … Press BOTH the SW2 and SW1 button … release SW1 first followed by SW2"; "highly recommended to have ONLY the Leviathan connected to the RPI". The V1.2 guide has the same text.
- Photo `frontsw1sw2_V1.3.webp`: SW2 Boot and SW1 Reset are small tact switches beside the STM32 processor. The only screw terminal near them is the board's 24 V input.
- Leviathan repo README: the setup guide link only; no flashing procedure.

Finding: LDO's flash method needs SW1, or SW2+SW1, pressed on the powered board. `flashtool.py -r` is not LDO's method. Kept LDO's method and wrote the bounded exception:
- Buttons: SW1 and SW2.
- Location: beside the processor, on the front rail. The PSU, SSR and mains WAGO are on the rear rail and rear frame (09.2).
- Position: 12.11 now puts the machine on its side before plug-in.
- Hand: one fingertip, the other hand behind the back, nothing else touched, hand out right after the press.
- Unplugging USB leads from the Pi for DFU is done dead.

Changes:
- 00a :334 exception bullet; :336 ⚠; Source adds the LDO V1.3 guide and § Mainboard Firmware Setup.
- 12: :314–315 12.11 Do (on its side, dead, before plug-in); :333 table row (no touching); :348 new eyes-only ⚠ naming the exception; :477 12.15 Do; :496 ⚠; :498 Source cites LDO V1.3 + Rev D; :510–512 12.16 Do (dead before unplugging USB, then the press); :530 re-plug the leads dead before 12.17.

Open for Alex: LDO treats flashing as optional ("pre-programmed"). Ch 12 always flashes, to match the host version. If the factory firmware connects without a protocol error, skipping 12.14–12.15 would remove the only live touch. That is not decided here.

## Ruling 3: "switch off at the wall" → "unplug at the wall"

- 00a :354 (00a.12 row 1). The phrase occurred nowhere else in 00a, 12 or 13. Grep covered "at the wall", "off at the" and "wall".

## Gate

- `.venv/bin/python scripts/lint_manual.py --strict-parts --chapters 00a,12,13` → exit 0 (check 6: 0, check 7: 0).
- Default `lint_manual.py` → 0 findings, budgets included.
- `.venv/bin/python hooks/mascot.py` → "All self-tests passed".
- `make verify` and `mkdocs build` were not run (orchestrator).

## Needs sync outside my files

- `11-skirts-panels-door.md:235` (11.67 ⚠): "13.3, with the bay closed". It is now door-open, eyes only.
- `11-skirts-panels-door.md:219` (11.67): "tips the printer on its side". 12.11 now leaves it on its side.
- `10-wiring.md` 10.23: "Printer upright" is fine under the eyes-only rule.
- `15-troubleshooting.md:445–446`: the SSR-LED rows should say "unplug, 0 V first" as Ch 13 now does.
- `docs/print/checklists.md` (generated) picks up the 00a/12/13 checkpoint lines at build.

## Ruling 4 (Alex 2026-10-23): flash the Leviathan only when needed; buttons for recovery only

Closes Ruling 2's open item. Line numbers are post-edit.

### Evidence (fetched 2026-10-23)

- LDO Rev D wiring guide § Mainboard Firmware Setup: "The Leviathan board is pre-programmed when you receive it. If you need to update Klipper firmware, follow …".
- LDO Leviathan V1.3 guide, intro: "Leviathan boards ship out already flashed with USB firmware. Run ls /dev/serial/by-id/* to confirn you have a klipper ID. If you need to update firmware … two major steps … in order: Flashing the Leviatan with the Katapult Bootloader … Flashing the Leviatan with the Klipper Firmware". The V1.2 guide has the two steps but not the "ship out" sentence.
- **Katapult on the factory board: not stated by any LDO source.** The guides, the Rev D page and the Leviathan repo (README, no firmware folder) are silent; LDO's update path starts by installing Katapult over DFU. The old 12.15 claim "The board ships with Katapult" was unsourced and is gone. The board answers it at 12.15 itself (below). Web search and Klipper Discourse found no factory-state statement.
- Klipper f0892d8, how a mismatch is reported: `klippy.py:140–146` turns a `msgproto.error` into state "Protocol error"; `extras/error_mcu.py:96–122` rewrites it as "MCU Protocol error / This is frequently caused by running an older version of the firmware on the MCU(s)… / Your Klipper version is: … / MCU(s) which should be updated: … / Up-to-date MCU(s): …" and ends with the raw error. `msgproto.py:314–331` + `serialhdl.py:20`: the raw error is `mcu 'mcu': Command format mismatch: … vs …` or `mcu 'mcu': Unknown command: …`. `mcu.py:835` logs `Loaded MCU 'mcu' N commands (<version> / …)`. There is no separate version warning: a differing version is only listed inside a protocol error. Commands are checked as they are looked up, so a minimal config tests a subset; the full config at 12.37 is the real test.
- Klipper Config Reference § None Kinematics: `kinematics: none` + `max_velocity: 1` + `max_accel: 1` is a valid `[printer]`.
- No-button flash: Klipper `usb_cdc.c:450–459` treats a 1200-baud line coding as a bootloader request; `armcm_reset.c` resets into Katapult if its signature is present, else `stm32h7.c:200–204` / `dfu_reboot.c` reboot into the chip's ROM DFU (`STM32_DFU_ROM_ADDRESS` set for F4 and H7, `stm32/Kconfig:276–283`; `HAVE_BOOTLOADER_REQUEST` selected for all STM32). Katapult 3b973a4 README § Uploading Klipper: "flashtool.py will command USB … devices to enter the bootloader"; `flashtool.py:962–1007`: after the request it flashes only if the new device is Katapult, else prints "Device is not Katapult, exiting..." and writes nothing. README: Katapult enters the bootloader on its own when the application area is empty.
- Rejected: Klipper's `make flash` for the Leviathan. `flash_usb.py:143–157,306–313` falls through to `dfu-util` at the build's offset when no Katapult answers, which on an F446 overwrites the factory image's sector 2 while leaving its start: a dead board. `flashtool.py` refuses instead.

### Changes

- `12-software.md`
  - :3, :5 intro; :53 Read-first bullet (pre-programmed, test first, no-button flash, buttons for recovery); :64 Sources adds Katapult 3b973a4 and `error_mcu.py`.
  - :219 12.7 "Every MCU firmware you build comes from this exact working copy" (was "Both MCUs must be flashed").
  - :346 12.11 prose: a Leviathan on `1d50:6177` (Katapult) is a firmware state, not a Ch 10 fault. :350 ⚠ "The one exception, for recovery only".
  - :380 12.12: a `usb-katapult_` Leviathan line is noted for 12.15. Also removed "unplug one board's USB, re-run" (a live USB pull in the open bay, against 00a.11): the MCU families always differ, so the table settles it.
  - 12.14 :421 description, :425 Do (six-line test `printer.cfg`, restart, klippy.log grep), :440–444 outcome table (Ready → skip to 12.17; `MCU Protocol error` / `Unable to connect` / no `usb-Klipper_` line → build), :446 `printer.cfg` replaced at 12.21, :484 Check (skip branch), :486 ⚠ recovery at 12.15, Source adds Rev D, V1.3 quotes, `error_mcu.py`, `msgproto.py`, None Kinematics.
  - 12.15 :496 description, :500 Do = `flashtool.py -d /dev/serial/by-id/usb-Klipper_…` (no button), :512 Check, :514–518 outcome table (`Device is not Katapult` → board in ROM DFU → 12.16, no button; `timed out` / no line → recovery), :520 wrong-clock case is now recovery, :522 **Recovery, LDO's method, live** (SW1 double-click, wording kept), :524 ⚠ "LDO's buttons: recovery only, the build's only live touch", Source adds Katapult README/flashtool and Klipper usb_cdc/armcm_reset/dfu_reboot.
  - 12.16 :534 description; :538 Do: in DFU from 12.15 → build, no button; recovery → dead, other USB leads out, power on, SW2+SW1 (LDO wording kept); :543 one DFU device, LDO's only-the-Leviathan advice; :558 start Katapult by Pi shutdown + rocker cycle instead of SW1, then flash with 12.15's line; :560 Check; Source adds V1.3 § Katapult and the Katapult README.
  - :566 Pause after 12.16; :607 12.17 Check; :621, :634 12.18.
  - :1495 12.37 table adds `MCU Protocol error`; :1509 ⚠ wording corrected to the source ("MCU Protocol error" ending "mcu 'nhk': Command format mismatch"; the old "MCU 'nhk' shutdown:" is not Klipper's text); :1511 new ⚠ backstop: `mcu 'mcu': …` after the kept factory firmware → build and flash at 12.14–12.15.
  - Checkpoint 12 :1524 (Nitehawk flashed; Leviathan flashed or passed 12.14 + 12.37), :1527 (`config.leviathan` only if built).
- `00a-mains-safety.md`: :83 "recovery-only button press"; :329 Check "SW1 and SW2, recovery only"; :334 exception bullet now says why the buttons are recovery only (pre-programmed, flash only on a protocol error, `flashtool.py` needs no button; buttons only when no Klipper runs on the board); the rest of the bounded-exception wording is unchanged; :336 ⚠; :338 Source adds the Katapult README; :387 Checkpoint line.
- `hooks/mascot.py`: unchanged. 12.11–12.37 stay mains (the machine is still live, bay open).

### Judgment calls for Alex

- 12.16's no-button DFU path keeps the Nitehawk plugged in. LDO says only the Leviathan should be on the Pi for DFU. `dfu-util -d 0483:df11` addresses DFU devices only, and the step checks that exactly one is present. Following LDO literally would mean a dead machine, the leads out and a power cycle, which brings the factory Klipper back up and loses the DFU state.
- 12.16 starts Katapult with a Pi shutdown and a rocker cycle instead of LDO's single SW1 press. `dfu-util … :leave` would avoid the cycle, but it is not LDO's command and is untested here.
- The 12.14 test only checks the commands a six-line config uses. The 12.37 ⚠ catches what it misses.

### Gate

- `.venv/bin/python scripts/lint_manual.py --strict-parts --chapters 00a,12` → exit 0 (check 6: 0, check 7: 0).
- Default `lint_manual.py` → 0 findings, budgets included.
- `.venv/bin/python hooks/mascot.py` → "All self-tests passed".
- `make verify` and `mkdocs build` were not run (orchestrator).

### Needs sync outside my files

- `16-glossary.md:190` Katapult "on both MCUs": unproven for the Leviathan. `:92` DFU "entered with the RESET/BOOT0 buttons": a Klipper USB request also enters it. `:221` fine.
- `15-troubleshooting.md:556`: still right; it could add "a running Klipper reaches DFU with no button".
- `00-tonight.md:331` and `docs/assets/tonight.json`: the 12.14→12.16 leave-state comes from the changed Pause line. Regenerated at build.
- `docs/print/checklists.md` (generated): Checkpoint 12 lines.
- Not in this ruling: the 12.19 Nitehawk fallback presses RESET/BOOT0 on the live toolboard (24 V, outside the bay). 00a.11 names SW1/SW2 as the only live touch.
