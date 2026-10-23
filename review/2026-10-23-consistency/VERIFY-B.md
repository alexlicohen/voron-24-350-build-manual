# VERIFY-B: mains, wiring and software findings (2026-10-23)

Agent B. Files edited: `docs/manual/00a-mains-safety.md`, `docs/manual/10-wiring.md`,
`docs/manual/12-software.md`, `hooks/mascot.py`. Nothing staged or committed. G5-2 (Leviathan SW1/SW2)
not touched.

Gates: `.venv/bin/python scripts/lint_manual.py --strict-parts --chapters 00a,10,12`: check 6 0, check 7 0.
Default lint run: 0 findings (budgets included). `.venv/bin/python hooks/mascot.py`: all self-tests passed.
Not run: `mkdocs build` / `make verify` (brief), so there is no iPad render check yet. The orchestrator's
`make verify` regenerates `00-tonight.md` and the step pages.

---

## G1-03 = G5-1: Helper lines and "two people" inside 00a.2's adult-only window

**Verdict: CONFIRMED.**

**What 00a says.** 00a.2, bullet 2: she is not in the room "while the machine is plugged in with the
bay open", naming "the firmware gate at 12.11 through Checkpoint 12, and the shut-down at 11.67. Those are
adult-only." Bullet 3: "One adult, standing to the side, hand on the switch, nobody else within reach"
at 10.23, 12.11 and 13.3. Bullet 4: she owns the record "only with the printer **unplugged**".
Checkpoint 00a repeats "Ch 12 Step 12.11 through Checkpoint 12".

**Is the machine live for the whole window?** Yes. 12.11 ⚠ says "The machine now stays powered with the
bay open through the flashing steps". 12.37 runs `FIRMWARE_RESTART` with both MCUs connected. Checkpoint 12
says "The machine is still live with the bay open … until Step 11.67". By 00a's own wording, 12.11–12.37
and Checkpoint 12 are all adult-only.

**The conflict.** 12.12, 12.27 and 12.37 had Helper lines that read the screen. 12.11 Do 2 said "two
people". 12.11 had no Who-is-in-the-room ⚠, unlike 10.1, 10.17, 10.23, 11.67 and 14.30. `mascot.py`'s
`mains` list held only `12.11`, so the build let the three Helper lines through.

**Changes:**
- `12-software.md` 12.11 Do 2: "two people" → "one adult only".
- 12.11: added the standard ⚠ Who-is-in-the-room callout after the Rev D+ ⚠: one adult, nobody else
  within reach, and she stays out of the room through Checkpoint 12 until 11.67 has proved the machine
  dead.
- Deleted the Helper lines in 12.12, 12.27 and 12.37. The 12.7 Helper stays: it is bench work on the Pi
  alone, before 12.11.
- `hooks/mascot.py` `mains`: `12.11` → `12.11-12.37`. The list comment now names the live open-bay window.
  Self-test ids `12.12` and `12.37` added.
- Side effect for the orchestrator: the Check, Tip and Pause badges are now stripped on 12.12–12.37, the
  same treatment as every other mains step. This keeps one classifying list and keeps CONVENTIONS § Helper
  steps true as written. If Alex wants the birds back on those software steps, the alternative is a
  helper-only list in `mascot.py` plus a CONVENTIONS edit.
- **Ch 13 (agent C):** 13.3 Do 1 in the current tree already reads "One adult at the switch; nobody else
  within reach." No change needed from me.

## G1-04: "Switch off at the wall, not the rocker" vs rocker-first in the steps

**Verdict: CONFIRMED.** 00a contradicts itself and the steps: row 2 of the 00a.12 table vs Ritual 2,
10.23 and 13.3.

**Sources:**
- LDO wiring guide § Checkpoint 1 (curl, 2026-10-23): "plug in the power cable and switch on the
  inlet … **Switch off the inlet and remove the plug**". The rocker comes first, then the plug.
- 00a.10: the rocker switches both L and N, so it isolates everything downstream of the inlet.
- Every ritual already has the hand on the rocker (00a.11 Ritual 2, 10.23, 12.11, 13.3), so the rocker is
  the fastest way to remove energy. Reaching the wall plug means reaching behind a smoking machine.
- The rocker does not isolate the C14 pins, the fuse drawer or the cord. For smoke at the inlet or cord
  itself, the safe action is the breaker labelled in 00a.5, which exists "so the circuit can be killed from
  outside the room".

**Changes:**
- `00a-mains-safety.md` 00a.12, row "Smoke, a hot smell, buzzing or click-cycling": now reads "**Rocker
  off** at once, your hand is already on it, then unplug at the wall." For smoke at the inlet or cord
  itself, it sends you to the 00a.5 breaker.
- 00a.11 Ritual 2: "Anything wrong: switch off at once" → "rocker off at once, then unplug at the wall".

**Not changed:**
- 00a.12 row 1 (breaker or RCD trips): "Switch off at the wall, unplug" was left alone. The supply is
  already dead there, so it does not contradict the steps. It is still a UK idiom, because US receptacles
  have no switch. Alex's call whether it should read "rocker off, unplug at the wall".

**Proposed for agent C (13-initial-startup.md, 13.3 ⚠):**
"⚠ If any of that is wrong, rocker off at once, then unplug at the wall, and go back to Ch 10."
The current "switch off at the inlet immediately" is consistent with the rocker but drops the unplug.

## G5-3: 12.1 option 2 powers the bay before 12.11; Part 1's order assumptions

**Verdict: CONFIRMED.**

**Evidence:**
- 12.1 Do 2 said "Checkpoint #1 passed: leave the Pi on the board and power the bay". That contradicts
  00a.11, which says the machine is energised at exactly two steps before the bay closes, 10.23 and 12.11.
  It also contradicts Ch 12 Prereqs, which call 12.11 "the first time the Leviathan, the Pi and the
  toolboard are energised".
- Index row 15 runs Ch 12 Part 1 with "no hardware gate", before Ch 01. 12.1 ⚠ said the chapter "is gated
  on Checkpoint #1".
- 12.10 said "Ch 10 connected the panel", but in index order Ch 10 has not happened yet. 12.10's own Pause
  says "there is no screen on the bench yet".

**Changes:**
- `12-software.md` 12.1 Do: (1) work on the Pi alone, on the bench, not on the Leviathan; (2) feed it from
  a USB-C 5 V/3 A supply; (3) plug in Ethernet. The bay-power option is gone. "Not on the Leviathan" also
  covers a late builder whose Pi is already mounted: its HAT adapter puts the Pi on the Leviathan's +5P
  rail (schematic, see G5-6), and USB-C power would back-feed that rail.
- 12.1 ⚠: "power the Pi" means switching on the printer, which first happens at Step 12.11, after
  Checkpoint #1. 12.1 to 12.10 never power the printer.
- 12.10 Do: "Nothing plugs in yet; Ch 10 latches the panel."
- Tools: the USB-C supply is now required for the Pi half (12.1–12.10), no longer "if".

**00-index:** no change needed. Row 15 already says "the Pi … only, no hardware gate".

## G5-4: 00a.6 says +24 V → PE reads OL; 00a.3 quotes stale Ch 10 text

**Verdict: CONFIRMED (both parts).** Ch 10 is the right side.

**+24 V → PE:**
- Nitehawk-SB V2 doc § ESD Hardening (curl, 2026-10-23): "connecting the extruder motor body to the
  toolboard ground, and the USB adapter ground to the printer frame, creating a continuous discharge path
  … through to the toolboard, umbilical cable, USB adapter, and finally frame/earth".
- So DC −V sits on PE through 10.58's cable. 00a.6 itself says "−V / GND reads a few Ω on purpose".
- With −V on PE, +V → PE = (+V → −V through the loads) + a few Ω. That is finite and about the 10.74
  figure, exactly as 10.74, 10.77 and Checkpoint 10 say. An `OL` there would mean the rail is open or the
  ESD bond is missing.

**00a.3 quotes:** the current Ch 10 Tools text is "a 2 MΩ or 20 MΩ resistance range you can select by
hand", and 10.13 now reads "`OL` on your meter's highest Ω range". 00a.3 still quoted "at least 2 MΩ" and
"well above 10 MΩ". Its claim that a 20 MΩ meter "turns a pass into a number" no longer matches 10.13.

**Changes:**
- `00a-mains-safety.md` 00a.6: L and N read `OL`. A new sentence says that, because −V sits on PE, the
  +24 V side reads about the 10.74 +V → −V figure to earth, through the loads and the bond, never 0 Ω.
- 00a.3 Resistance range: now quotes Ch 10's current Tools text. It also cites 10.19 and 10.78 (L↔N is a
  number on the 2 MΩ range, ≥100 kΩ, PSU input bridge), 10.13 (`OL` on the highest range) and 10.76
  (≤162 kΩ). The stale 20 MΩ claim is removed. Added one line: a meter that only autoranges may not let
  you hold the 2 MΩ range. This is inferred from Ch 10's "select by hand".

## G5-6: 10.75 measures 5 V on GPIO pins the HAT adapter covers

**Verdict: CONFIRMED.**

**Sources:**
- LDO `assets/remote/09-electronics-bay/rpi4_installed_V1.3.jpg` (embedded at 09.23), cropped at 3×. The
  black 3/4 adapter (P1/P3/F1/C1) covers the first 12 columns of the header, pins 1–24, at the end away
  from USB/Ethernet. That is the microSD end. Pins 2, 4 and 6 are under it. Its top shows a 2×12 array of
  exposed pads, square at the edge-row corner.
- Leviathan schematics V1.2 and V1.3 (MotorDynamicsLab/Leviathan `Schematic/`, repo head 878c3c4):
  - J9 "PWR/UART": pins 1–2 = **+5P**, pins 3 and 6 = GND, 4/5 = UART.
  - +5P comes from its own regulator, PS1 K7805-3AR3.
  - The board **+5V** comes from PS3 K7805-2000R3 through D20. That rail feeds EXP1.
  - So G5's EXP1_10/EXP1_9 suggestion would meter the wrong rail. Refuted for that sub-point.
- Leviathan V1.3 manual p.5: "Dedicated power supply for Raspberry Pi". No physical pin-1 marking for J9
  is published.

**Changes:**
- `10-wiring.md` 10.75 Do: the adapter covers pins 2, 4 and 6, so leave it seated. Probe its top pads
  instead: over pin 2 (5 V) to over pin 6 (GND), the edge row's first and third at the microSD end,
  `(verify on bench)`. "Verify on bench" is there because the photo cannot prove the pads are the socket's
  solder joints.
- New Tip: the same rail is on J9, pins 1–2 = 5 V and pin 6 = GND, and EXP1's 5 V is a separate regulator.
  It cites the schematic.
- Source line: added the LDO photo and the schematic.

---

## For other agents / Alex

1. **Agent C, 13.3 ⚠:** "rocker off at once, then unplug at the wall" (see G1-04). 13.3 Do 1 already reads
   one adult.
2. **Alex:** 00a.12 row 1 still says "Switch off at the wall". There is no switch on a US outlet; consider
   "rocker off, unplug at the wall".
3. **Alex/orchestrator:** the `12.11-12.37` mains listing strips the mascot badges on those software steps
   (see G1-03). Say if a helper-only list is preferred.
4. **Observations, not edited (out of scope):**
   - 12.11 Do 2 plugs in without "rocker off" first. Ritual 1 and 10.23 both have it, and 10.23 leaves the
     rocker off.
   - The Pause lines inside 12.11–12.37 do not say whether the builder may walk away from the live,
     open bay.
