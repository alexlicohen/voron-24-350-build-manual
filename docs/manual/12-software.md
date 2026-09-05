# Chapter 12 — Software: Pi OS image, Klipper/Moonraker/Mainsail, firmware, printer.cfg

Images the Raspberry Pi, flashes Klipper onto both MCUs, and installs a `printer.cfg` that is correct for a **350 mm Rev D+** — so that Ch 13 can power up a machine that already knows its own geometry.

**Time:** 2.0–3.0 h hands-on, first build (survey §7.2). Add ~30 min if you have to reinstall Katapult on either board.

**Prerequisites:**
- **Ch 10 — Electronics bay wiring**, complete, with **LDO Checkpoint #1 passed** (multimeter, unplugged) and the bay powered on once successfully. Both MCUs must be powered and connected to the Pi over USB before Steps 12.11 onward.
- The Pi-side half (Steps 12.1–12.10) has **no hardware prerequisite** and can be bench-done on day one — power the Pi from its own USB-C supply instead of the Leviathan's Pi rail (survey §5.1, P12: "the whole flash+install can be bench-done on day one").
- **Printed parts: none.** No print batch gates this chapter.
- Do **not** start Ch 13 until Checkpoint 12 below passes.

**Tools**
- Laptop with an SD card reader
- Raspberry Pi Imager (download from [raspberrypi.com/software](https://www.raspberrypi.com/software/))
- Ethernet cable (use wired for the flashing session; Wi-Fi is the fallback)
- USB cable, Pi ↔ Leviathan (supplied with the kit; connector type `(verify on bench)`)
- A USB-C 5 V/3 A supply if you are bench-doing the Pi half before the bay is live

**Consumables:** the supplied 32 GB microSD card. Nothing else.

**Printed parts**

| STL | Qty | Colour |
|---|---|---|
| — none — | 0 | — |

**Hardware** (chapter totals)

| Fastener / part | Qty | Note |
|---|---|---|
| — none — | 0 | Software only. The DSI ribbon and the Pi were fitted in Ch 09/Ch 11 |

**Read first**
- **Use `leviathan-printer-rev-d-sbv2.cfg`, never `leviathan-printer-rev-d.cfg`.** The Rev D wiring guide links the wrong one. Every `nhk:` pin differs because the toolboard MCU changed family; loading the V1 config mis-drives the heater, thermistor, probe, both fans and the accelerometer at once (survey §4.1 ①).
- **The toolboard is an STM32G0B1, not an RP2040.** The wiring guide's sentence *"The Nitehawk uses an RP2040 MCU"* is stale. Its USB ID will read `usb-Klipper_stm32g0b1xx_…`. Match on that string, not on `rp2040` (survey §4.1 ②).
- **The stock config ships with every build-size option commented out and no `[bed_mesh]` at all.** Six separate places need the 350 mm lines uncommented, and the mesh section has to be written from scratch (survey §4.4 #15).
- **Confirm which Leviathan you have before you run `make menuconfig`.** LDO shipped an **STM32F446** Leviathan (V1.1/V1.2) and later an **STM32H743** one (V1.3). Processor model, clock reference and bootloader offset all differ; the wrong combination produces firmware that will not run. Step 12.13 settles it from the board itself.
- **Nothing moves and nothing heats in this chapter.** The chapter ends at "Klipper reports Ready with both MCUs connected". Homing, heaters, fans and motion are Ch 13.

---

### Step 12.1 — Decide where you are doing the Pi half

(no image — see text)

**Parts:** none — Pi 4B, supplied 32 GB microSD, laptop, card reader.

**Do:** Steps 12.1–12.10 need only the Pi, the SD card and the network. If the electronics bay is not yet wired, take the Pi off the Leviathan mount, feed it from a USB-C 5 V/3 A supply on the bench, and do this half now. If Ch 10 is done and Checkpoint #1 has passed, leave the Pi on the board and power the bay instead. Plug the Ethernet cable in either way — a wired link makes the flashing steps deterministic.

**Check:** You can identify the Pi's SD slot and its Ethernet port, and you have a way to power it that is not the printer's mains.

⚠ **Rev D+ / LDO:** the Leviathan supplies the Pi from its own dedicated Pi rail, so on the assembled machine "power the Pi" means "switch on the printer". That is why this chapter is gated on Checkpoint #1 (survey §4.4 #8). [src](https://github.com/MotorDynamicsLab/Leviathan)

---

### Step 12.2 — Write MainsailOS with Raspberry Pi Imager

(no image — see text)

**Parts:** microSD 32 GB ×1, card reader ×1.

**Do:** Insert the card and launch Raspberry Pi Imager. **Choose Device** → your Pi model (Raspberry Pi 4). **Choose OS** → scroll to **Other specific-purpose OS** → **3D printing** → **MainsailOS** → pick the **64-bit** version (the 32-bit entry is marked deprecated and is only for pre-Zero-2 hardware). **Choose Storage** → the SD card, and read the drive description twice before you continue.

**Check:** The summary line names your Pi model, MainsailOS 64-bit, and the correct removable drive.

⚠ **Rev D+ / LDO:** LDO's wiring guide tells you to install **Raspberry Pi OS Lite (32-bit)** and then add Klipper/Moonraker/Mainsail with KIAUH. MainsailOS ships Klipper, Moonraker, Mainsail, Crowsnest, Sonar, Timelapse and the input-shaper Python dependencies pre-installed and pre-wired — same end state, four fewer install passes. Take the MainsailOS path; you still need KIAUH in Step 12.8 for KlipperScreen, which MainsailOS does **not** include. [src](https://docs-os.mainsail.xyz/getting-started/raspberry-pi/) · [src](https://docs.ldomotors.com/en/voron/voron2/wiring_guide_rev_d#software-setup)

---

### Step 12.3 — Fill in the Imager customisation

(no image — see text)

**Parts:** none.

**Do:** Work through the customisation pages: **Hostname** — set it to something you will type a lot; `voron` gives you `http://voron.local`. **Localisation** — set your timezone (log timestamps and timelapse depend on it). **User** — set a username and a real password; do not leave the `pi`/`raspberry` default. **Wi-Fi** — SSID and password (the Wi-Fi country comes from your localisation setting). **Remote access** — enable SSH. Then write, confirming the erase prompt.

**Check:** Imager reports a successful write and verify. Eject the card.

Tip: set both Wi-Fi *and* plug in Ethernet. Wi-Fi is the long-term link; Ethernet is what you fall back to when Wi-Fi is the thing that broke. [src](https://docs-os.mainsail.xyz/getting-started/raspberry-pi/)

---

### Step 12.4 — First boot

(no image — see text)

**Parts:** none.

**Do:** Put the card in the Pi, connect Ethernet, power on and leave it alone. The first boot expands the filesystem and can take up to five minutes. Watch the green activity LED — when it settles to occasional flickers the expansion is done.

**Check:** `ping voron.local` answers (substitute your hostname). If the `.local` name does not resolve, find the Pi's IP in your router's DHCP table and use that instead.

**Check:** Give the Pi a DHCP reservation in your router now, before you paste its address into anything.

[src](https://docs-os.mainsail.xyz/getting-started/first-boot/)

---

### Step 12.5 — Reach Mainsail and open an SSH session

![LDO: Mainsail Machine page](https://raw.githubusercontent.com/MotorDynamicsLab/LDOVoron2/main/Images/WiringGuide/RevD/mainsail_machine.png)

**Parts:** none.

**Do:** Open `http://voron.local` in a browser. Mainsail loads and immediately reports a Klipper error — *"Unable to open config file printer.cfg"*. That is expected and correct; MainsailOS ships no `printer.cfg`. In a terminal, `ssh <youruser>@voron.local`.

**Check:** Mainsail's UI renders, the error names the missing `printer.cfg`, and your SSH session lands at a shell prompt.

[src](https://docs-os.mainsail.xyz/getting-started/first-boot/)

---

### Step 12.6 — Update everything before you touch anything else

(no image — see text)

**Parts:** none.

**Do:** In Mainsail go to **Machine** → **Update Manager** (bottom right) and click **Update all components**. Let it finish, including the system packages. Reboot if it asks.

**Check:** Every row in the Update Manager reads up to date.

**Why now:** the version of Klipper you end up with here is the version you must build MCU firmware from in Steps 12.14 and 12.17. Update first, then flash — do it the other way round and you will re-flash both boards after the first update. [src](https://docs-os.mainsail.xyz/getting-started/first-boot/)

---

### Step 12.7 — Record the Klipper version you are building against

(no image — see text)

**Parts:** none.

**Do:** In SSH:

```bash
cd ~/klipper && git describe --tags --always --dirty
```

Write the string down (or paste it into your build notes). Both MCUs must be flashed from this exact working copy.

**Check:** You have one version string, and `ls ~/printer_data/config/` shows `mainsail.cfg` and `moonraker.conf` but no `printer.cfg`.

**Why:** if the host Klipper and an MCU's firmware were built from different commits, Klipper aborts at connect with a *Command format mismatch* error naming the offending MCU. [src](https://docs.mainsail.xyz/faq/klipper_errors/command-format-mismatch/)

---

### Step 12.8 — Install KIAUH

(no image — see text)

**Parts:** none.

**Do:** In SSH:

```bash
sudo apt-get update && sudo apt-get install git -y
cd ~ && git clone https://github.com/dw-0/kiauh.git
./kiauh/kiauh.sh
```

You land in KIAUH's main menu. Do **not** use it to install Klipper, Moonraker or Mainsail — MainsailOS already has them, and a second install will fight the first.

**Check:** KIAUH's status panel shows Klipper, Moonraker and Mainsail as already installed, and KlipperScreen as not installed.

[src](https://github.com/dw-0/kiauh)

---

### Step 12.9 — Install KlipperScreen

(no image — see text)

**Parts:** none.

**Do:** From KIAUH's main menu choose **Install** → **KlipperScreen** and let it run. It builds a Python venv at `~/.KlipperScreen-env`, pulls the graphics packages and installs a systemd unit. When it finishes, confirm Moonraker gained an `[update_manager KlipperScreen]` block in `~/printer_data/config/moonraker.conf`; if not, add it by hand from the KlipperScreen install docs and restart Moonraker.

**Check:** `systemctl status KlipperScreen` shows the unit loaded. It will not display anything useful yet — there is no `printer.cfg`.

[src](https://klipperscreen.dev/Installation.html) · [src](https://docs.ldomotors.com/en/guides/btt_43_rotate_guide)

---

### Step 12.10 — Bring up the DSI panel and rotate it

(no image — see text)

**Parts:** 4.3" DSI touchscreen ×1, Pi FFC ribbon ×1 — both already fitted in Ch 11.

**Do:** With the panel connected, confirm the kernel sees it:

```bash
grep -H . /sys/class/drm/card*-*/status | grep :connected
```

You should get a line containing `DSI-1`. If the panel is upside down for how it is mounted, rotate it in the kernel command line — `sudo nano /boot/firmware/cmdline.txt` — and append to the single existing line (no line breaks):

```
video=DSI-1:800x480@60,rotate=180
```

Reboot. Valid rotations are 0, 90, 180, 270.

**Check:** `/sys/class/drm/...DSI-1/status:connected` is present, the console appears the right way up, and the touch point follows your finger.

⚠ **Rev D+ / LDO:** LDO's touchscreen guide tells you to edit `/boot/config.txt`, comment out `dtoverlay=vc4-fkms-v3d` and set `display_lcd_rotate=2`. That is the **legacy fake-KMS path**. MainsailOS 3.x is built on a current Raspberry Pi OS: the boot partition is mounted at **`/boot/firmware/`**, and the display stack is full KMS (`vc4-kms-v3d`), where `display_lcd_rotate` does nothing. Use the `cmdline.txt` method above. [src](https://klipperscreen.dev/Troubleshooting/Rotation.html) · [src](https://docs.ldomotors.com/en/guides/btt_43_rotate_guide)

Tip: if the touch axes end up rotated relative to the picture, that is a separate fix — see KlipperScreen's touch-rotation matrix page, not the display rotation above. [src](https://klipperscreen.dev/Troubleshooting/Touch_issues.html)

---

### Step 12.11 — Gate: power the bay and confirm both MCUs enumerate

(no image — see text)

**Parts:** none.

**Do:** **Stop here unless LDO Checkpoint #1 has passed** (Ch 10: multimeter, unplugged — continuity within each colour group, no continuity between L/N/PE, PSU 115/230 V selector confirmed). With that done, switch the inlet on. The PSU LED lights. Then, over SSH:

```bash
lsusb
```

**Check:** `lsusb` lists two devices whose descriptors mention Klipper — the Leviathan and the Nitehawk-SB V2. The Nitehawk's onboard USB hub also appears as a separate hub device; that is normal on V2 and is the "+" feature.

⚠ **Rev D+ / LDO:** the Nitehawk-SB V2 adds a **USB hub and a secondary USB port** that the V1 board does not have, so expect one more device in `lsusb` than any Rev D photo shows. [src](https://github.com/MotorDynamicsLab/Nitehawk-SB-V2)

---

### Step 12.12 — Read the two serial IDs and work out which is which

![LDO: ls /dev/serial/by-id output](https://raw.githubusercontent.com/MotorDynamicsLab/LDOVoron2/main/Images/WiringGuide/RevD/serial_by_id_output.png)

**Parts:** none.

**Do:**

```bash
ls -l /dev/serial/by-id/
```

Copy both lines into a scratch file. Identify them by MCU family, not by order:

| Board | Expected ID substring |
|---|---|
| Leviathan V1.1 / V1.2 mainboard | `usb-Klipper_stm32f446xx_…-if00` |
| Leviathan V1.3 mainboard | `usb-Klipper_stm32h743xx_…-if00` |
| **Nitehawk-SB V2 toolboard** | **`usb-Klipper_stm32g0b1xx_…-if00`** |

If you are unsure, unplug one board's USB, re-run the command, and see which line disappears. Mainsail's **Machine** → open a config file → **DEVICES** → **SERIAL** → **REFRESH** shows the same list under *Path by ID*.

**Check:** Exactly two Klipper devices, one toolboard `stm32g0b1xx` and one mainboard `stm32f446xx` or `stm32h743xx`, and you know which physical board each belongs to.

⚠ **Rev D+ / LDO:** the wiring guide states the toolboard ID will look like `usb-Klipper_rp2040_…`. **It will not.** Rev D+ ships the STM32G0B1 Nitehawk-SB V2. Matching on the documented `rp2040` string assigns the *mainboard's* ID to `[mcu nhk]` or finds nothing at all (survey §4.1 ②). Note also that the guide writes the mainboard string as `stmf446xx`; the actual Klipper string is `stm32f446xx`. [src](https://docs.ldomotors.com/en/voron/voron2/wiring_guide_rev_d#software-setup) · [src](https://docs.ldomotors.com/guides/klipper_id) · [src](https://ldomotion.com/p/guide/VORON-Leviathan-V12)

---

### Step 12.13 — Identify your Leviathan revision before you build anything

(no image — see text)

**Parts:** none.

**Do:** Read the revision printed on the mainboard silkscreen, and cross-check it against the ID you just read. They must agree:

| Silkscreen | MCU | Klipper/Katapult clock | Bootloader offset | Serial ID |
|---|---|---|---|---|
| Leviathan **V1.1 / V1.2** | STM32F446 | 12 MHz crystal | **32 KiB** | `stm32f446xx` |
| Leviathan **V1.3** | STM32H743 | 25 MHz crystal | **128 KiB** | `stm32h743xx` |

Use the row that matches *your* board in Step 12.14. If the silkscreen and the serial ID disagree, trust the serial ID and stop to ask in `#ldo_motors`.

**Check:** You have written down one MCU model, one clock reference and one offset, and you are not going to look at the other row again.

⚠ **Rev D+ / LDO:** LDO's own documents conflict here, so do not resolve it from paperwork. The Rev D wiring guide and the kit config header both say **STM32F446 / Leviathan V1.1**; the Leviathan repo README was changed on 2025-10-30 from *"STM32F446"* to *"STM32H743"*, and LDO publishes two setup guides with different menuconfig values. The board itself is the only authority. [src](https://github.com/MotorDynamicsLab/Leviathan) · [src](https://ldomotion.com/p/guide/VORON-Leviathan-V12) · [src](https://ldomotion.com/guides/voron-leviathan-v1-3)

---

### Step 12.14 — Build Klipper firmware for the Leviathan

(no image — see text)

**Parts:** none.

**Do:** Stop Klipper so it releases the serial ports, then configure:

```bash
sudo systemctl stop klipper
cd ~/klipper
make menuconfig
```

Set, for an **F446 (V1.1/V1.2)** board:

```
Micro-controller Architecture: STMicroelectronics STM32
Processor model:               STM32F446
Bootloader offset:             32KiB bootloader
Clock Reference:               12 MHz crystal
Communication interface:       USB (on PA11/PA12)
```

or, for an **H743 (V1.3)** board:

```
Micro-controller Architecture: STMicroelectronics STM32
Processor model:               STM32H743
Bootloader offset:             128KiB bootloader
Clock Reference:               25 MHz crystal
Communication interface:       USB (on PA11/PA12)
```

`Q` to quit, `Y` to save. Then:

```bash
make clean
make
```

**Check:** the build ends with `Creating hex file out/klipper.bin`, and `out/klipper.bin` exists.

⚠ **Rev D+ / LDO:** the bootloader offset is the dangerous field. Building with **no** bootloader offset and flashing over Katapult will overwrite the bootloader, after which the board can only be recovered through DFU (Step 12.16). [src](https://ldomotion.com/p/guide/VORON-Leviathan-V12) · [src](https://ldomotion.com/guides/voron-leviathan-v1-3)

---

### Step 12.15 — Flash the Leviathan through Katapult

(no image — see text)

**Parts:** none.

**Do:** The Leviathan ships with Katapult and Klipper already installed, so you normally never touch DFU. Put it into the bootloader by **double-clicking SW1 (RESET) quickly**, then confirm and flash:

```bash
ls /dev/serial/by-id/*
# expect a line containing:  usb-katapult_stm32f446xx_<id>-if00   (or stm32h743xx)

virtualenv -p python3 ~/katapult-env
~/katapult-env/bin/pip3 install pyserial greenlet cffi python-can aenum
test -e ~/katapult && (cd ~/katapult && git pull) || (cd ~ && git clone https://github.com/Arksine/katapult)

~/katapult-env/bin/python3 ~/katapult/scripts/flashtool.py \
  -d /dev/serial/by-id/usb-katapult_stm32f446xx_<id>-if00 \
  -f ~/klipper/out/klipper.bin
```

**Check:** the tool ends with `Verification Complete: SHA = <id>` then `Flash Success`, the bootloader status LED goes out, and `ls /dev/serial/by-id/*` shows `usb-Klipper_stm32f446xx_<id>-if00` again (same `<id>` as before — the ID is the MCU's, not the firmware's). Restart Klipper with `sudo systemctl start klipper`.

[src](https://ldomotion.com/p/guide/VORON-Leviathan-V12)

---

### Step 12.16 — Recovery only: reinstall Katapult on the Leviathan over DFU

(no image — see text)

**Parts:** none.

**Do:** Skip this step unless Step 12.15 found no `usb-katapult_…` device after a double-click of SW1. If you have to: disconnect every other USB device from the Pi, then press **SW2 and SW1 together, release SW1 first, then SW2**. Confirm with `lsusb` — you want `ID 0483:df11 STMicroelectronics STM Device in DFU Mode`. Then build Katapult with the same processor/clock/offset row from Step 12.13, plus `Communication interface: USB (on PA11/PA12)`, *Support bootloader entry on rapid double click of reset button*, *Enable Status LED*, `Status LED GPIO Pin: PE1`. Flash it:

```bash
cd ~/katapult && make clean && make
sudo dfu-util -d 0483:df11 -a 0 -s 0x08000000:mass-erase:force -D out/katapult.bin
```

Then go back to Step 12.14.

**Check:** after a press of SW1, `lsusb` shows `ID 1d50:6177 OpenMoko, Inc. stm32f446xx` and `/dev/serial/by-id/` gains a `usb-katapult_…` entry.

⚠ **`mass-erase:force` wipes the board.** It removes Klipper too, so you must complete Steps 12.14–12.15 afterwards or the mainboard will not enumerate as a Klipper device at all. [src](https://ldomotion.com/p/guide/VORON-Leviathan-V12)

---

### Step 12.17 — Build Klipper firmware for the Nitehawk-SB V2

(no image — see text)

**Parts:** none.

**Do:**

```bash
sudo systemctl stop klipper
cd ~/klipper
make menuconfig
```

Set exactly:

```
[*] Enable extra low-level configuration options
    Micro-controller Architecture: STMicroelectronics STM32
    Processor model:               STM32G0B1
    Bootloader offset:             8KiB bootloader
    Clock Reference:               12 MHz crystal
    Communication interface:       USB (on PA11/PA12)
[*] Optimize stepper code for 'step on both edges'
    (!PC6) GPIO pins to set at micro-controller startup
```

`Q`, `Y`, then `make clean && make`.

**Check:** `~/klipper/out/klipper.bin` exists and is newer than the Leviathan build you just flashed. (You are reusing one build tree for two boards — flash immediately, do not batch the builds.)

⚠ **Rev D+ / LDO:** this is the deviation that defines Rev D+. The Nitehawk-SB **V1** is an RP2040 and takes an entirely different menuconfig; the **V2** is an STM32G0B1. Choosing RP2040 here produces a binary the board cannot run. The **8 KiB bootloader offset is mandatory** — build with no offset and the Katapult flash will erase the bootloader. `!PC6` lights the ACT LED at startup, which is your at-a-glance "Klipper is running" indicator on the toolhead. [src](https://docs.ldomotors.com/en/Toolboard/nitehawk-sb-v2) · [menuconfig screenshot](https://github.com/MotorDynamicsLab/Nitehawk-SB-V2/blob/master/Images/make_menuconfig.png)

---

### Step 12.18 — Flash the Nitehawk with `make flash`

(no image — see text)

**Parts:** none.

**Do:** The recommended path needs no buttons at all:

```bash
cd ~/klipper
sudo service klipper stop
make flash FLASH_DEVICE=/dev/serial/by-id/usb-Klipper_stm32g0b1xx_<id>-if00
sudo service klipper start
```

Use the `stm32g0b1xx` ID you recorded in Step 12.12.

**Check:** the flash completes without error, and `ls /dev/serial/by-id/` still shows `usb-Klipper_stm32g0b1xx_<id>-if00`. If the board does not come back, reboot the printer before assuming anything is broken.

[src](https://docs.ldomotors.com/en/Toolboard/nitehawk-sb-v2)

---

### Step 12.19 — Fallback: flash the Nitehawk through Katapult

(no image — see text)

**Parts:** none.

**Do:** Only if Step 12.18 failed. Move the toolhead to the front and open the toolhead cover so you can reach **RESET** and **BOOT0** and see the five LEDs (3V3, 24V, HE0, ACT, HUB — ACT is the fourth from the left). **Double-click RESET quickly**; the ACT LED starts blinking slowly. Then:

```bash
ls /dev/serial/by-id/
# expect: usb-katapult_stm32g0b1xx_<id>-if00

~/katapult-env/bin/python3 ~/katapult/scripts/flashtool.py \
  -d /dev/serial/by-id/usb-katapult_stm32g0b1xx_<id>-if00
```

If there is no `usb-katapult_…` line, Katapult itself is missing: hold **RESET and BOOT0** together, release **RESET** first then **BOOT0**, confirm `lsusb` shows `ID 0483:df11 … STM Device in DFU mode`, then build Katapult with `Processor model STM32G0B1 / Clock Reference 12 MHz crystal / Communication interface USB (on PA11/PA12) / Application start offset 8KiB offset / Support bootloader entry on rapid double click of reset button / Enable Status LED / Status LED GPIO Pin (PC6)` and:

```bash
sudo apt install dfu-util
sudo dfu-util -a 0 -s 0x08000000:leave -D ~/katapult/out/katapult.bin
```

Then repeat Steps 12.17–12.18.

**Check:** ACT blinks slowly in Katapult, and `usb-Klipper_stm32g0b1xx_<id>-if00` is back after flashing.

⚠ Installing Katapult this way **erases the Klipper firmware**. You must re-flash Klipper afterwards. [src](https://docs.ldomotors.com/en/Toolboard/nitehawk-sb-v2) · [button/LED photo](https://github.com/MotorDynamicsLab/Nitehawk-SB-V2/blob/master/Images/reset_boot_buttons.jpg) · [katapult menuconfig screenshot](https://github.com/MotorDynamicsLab/Nitehawk-SB-V2/blob/master/Images/katapult_menuconfig.png)

---

### Step 12.20 — Re-read and record both serial paths

(no image — see text)

**Parts:** none.

**Do:**

```bash
ls /dev/serial/by-id/
```

Copy both full paths — including the `-if00` suffix — somewhere you can paste from. You need them twice in the next few steps.

**Check:** Exactly two lines, both containing `usb-Klipper_`, one `stm32g0b1xx` and one `stm32f446xx`/`stm32h743xx`. No `katapult` entries left.

⚠ If `ls /dev/serial/by-id/*` comes back empty on a machine that was working a moment ago, that is the first thing to investigate — a known `udev` failure mode on older Pi OS releases. On MainsailOS 3.x you should not hit it; if you do, check `dmesg | tail` for USB enumeration errors before touching the config (survey §4.3). [src](https://docs.ldomotors.com/guides/klipper_id)

---

### Step 12.21 — Download the correct config file

![LDO: Mainsail config devices panel](https://raw.githubusercontent.com/MotorDynamicsLab/LDOVoron2/main/Images/WiringGuide/RevD/mainsail_cfg_devices.png)

**Parts:** none.

**Do:** Download **[`leviathan-printer-rev-d-sbv2.cfg`](https://github.com/MotorDynamicsLab/LDOVoron2/blob/main/Firmware/leviathan-printer-rev-d-sbv2.cfg)** from LDO's kit repo.

**Check:** Open it in a text editor and search for `nhk:PB8`. If you find it, you have the right file. If you find `gpio23` instead, you downloaded the Rev D file — delete it and start again.

⚠ **Rev D+ / LDO:** the Rev D wiring guide's "pre-made configuration file" link points at `leviathan-printer-rev-d.cfg`, which is the **RP2040** toolboard config. Every `nhk:` pin in it is wrong for your board — extruder step/dir/enable, heater, thermistor, probe, both fans, PCB LED, neopixel, all four ADXL pins and the chamber thermistor. It also defines a `[temperature_sensor nh_temp]` on a pin that does not exist on the V2; do not add that section back (survey §4.1 ①, §4.3). [src](https://github.com/MotorDynamicsLab/LDOVoron2/blob/main/Firmware/README.md)

---

### Step 12.22 — Upload it as `printer.cfg` and add the Mainsail include

(no image — see text)

**Parts:** none.

**Do:** In Mainsail, **Machine** → drag the file into the config panel (or use the upload button). Rename it to exactly **`printer.cfg`** — no other name is recognised. Open it in Mainsail's editor and add one line at the very top, above the header comments:

```ini
[include mainsail.cfg]
```

**Check:** `printer.cfg` sits next to `mainsail.cfg` and `moonraker.conf` in the config list, and line 1 is the include.

**Why:** Mainsail needs `[virtual_sdcard]`, `[display_status]`, `[pause_resume]` and the `PAUSE`/`RESUME`/`CANCEL_PRINT` macros. `mainsail.cfg` is already on the SD card and bundles all six. Do not edit `mainsail.cfg` itself — it is a read-only include; override it later with a `_CLIENT_VARIABLE` macro in `printer.cfg` if you need to. [src](https://docs.mainsail.xyz/configuration/mainsail-cfg/)

---

### Step 12.23 — Paste the two serial paths

(no image — see text)

**Parts:** none.

**Do:** Replace both `{REPLACE WITH YOUR SERIAL}` placeholders. `[mcu]` is the **mainboard**; `[mcu nhk]` is the **toolboard**.

```ini
[mcu]
##  Obtain definition by "ls -l /dev/serial/by-id/" then unplug to verify
##--------------------------------------------------------------------
serial: /dev/serial/by-id/usb-Klipper_stm32f446xx_XXXXXXXXXXXX-if00   # CHANGED — Leviathan; stm32h743xx if V1.3
restart_method: command
##--------------------------------------------------------------------

[mcu nhk]
##  Obtain definition by "ls -l /dev/serial/by-id/" then unplug to verify
##--------------------------------------------------------------------
serial: /dev/serial/by-id/usb-Klipper_stm32g0b1xx_XXXXXXXXXXXX-if00   # CHANGED — Nitehawk-SB V2, NOT rp2040
restart_method: command
##--------------------------------------------------------------------
```

**Check:** the two paths are different from each other, both start `/dev/serial/by-id/usb-Klipper_`, and both end `-if00`.

⚠ **Rev D+ / LDO:** swapping these two is the single most common Rev D+ mistake, because the guide primes you to look for `rp2040` and there isn't one. `[mcu nhk]` gets the **`stm32g0b1xx`** path. [src](https://docs.ldomotors.com/en/voron/voron2/wiring_guide_rev_d#software-setup)

---

### Step 12.24 — 350 mm: `[stepper_x]` and `[stepper_y]`

(no image — see text)

**Parts:** none.

**Do:** In **both** `[stepper_x]` and `[stepper_y]`, uncomment the 350 pair and leave the 250 and 300 pairs commented. `[stepper_x]` after editing (`[stepper_y]` is identical below the header):

```ini
##  B Stepper - Left
##  Connected to HV STEPPER 0
##  Endstop connected to X-ENDSTOP
[stepper_x]
step_pin: PB10
dir_pin: !PB11
enable_pin: !PG0
rotation_distance: 40
microsteps: 32
full_steps_per_rotation:400  #set to 200 for 1.8 degree stepper
endstop_pin: PC1
position_min: 0
##--------------------------------------------------------------------

##  Uncomment below for 250mm build
#position_endstop: 250
#position_max: 250

##  Uncomment for 300mm build
#position_endstop: 300
#position_max: 300

##  Uncomment for 350mm build
position_endstop: 350        # CHANGED — uncommented for 350
position_max: 350            # CHANGED — uncommented for 350

##--------------------------------------------------------------------
homing_speed: 25   #Max 100
homing_retract_dist: 5
homing_positive_dir: true
```

**Check:** exactly two live `position_endstop`/`position_max` pairs in the whole file's X/Y sections — one per stepper. Klipper's parser is non-strict: a second live `position_max` in the same section will be silently accepted and the *last* one wins.

⚠ **Rev D+ / LDO:** the kit config ships with **every** build size commented out. This is the first of six places that need the 350 lines uncommented (survey §4.4 #15). [src](https://github.com/MotorDynamicsLab/LDOVoron2/blob/main/Firmware/leviathan-printer-rev-d-sbv2.cfg)

---

### Step 12.25 — 350 mm: `[stepper_z]`

(no image — see text)

**Parts:** none.

**Do:** Uncomment the 350 line only. Note that Z max is **330**, not 350 — the gantry cannot reach the last 20 mm.

```ini
position_endstop: -0.5
##--------------------------------------------------------------------

##  Uncomment below for 250mm build
#position_max: 230

##  Uncomment below for 300mm build
#position_max: 280

##  Uncomment below for 350mm build
position_max: 330            # CHANGED — uncommented for 350

##--------------------------------------------------------------------
position_min: -5
homing_speed: 8
second_homing_speed: 3
homing_retract_dist: 3
```

**Check:** `position_max: 330` is live; `position_endstop: -0.5` is untouched — it is a placeholder that `Z_ENDSTOP_CALIBRATE` overwrites in Ch 13 via `SAVE_CONFIG`.

[src](https://github.com/MotorDynamicsLab/LDOVoron2/blob/main/Firmware/leviathan-printer-rev-d-sbv2.cfg)

---

### Step 12.26 — 350 mm: `[quad_gantry_level]`

(no image — see text)

**Parts:** none.

**Do:** Uncomment the 350 `gantry_corners` and `points` blocks. Both keys need their continuation lines uncommented too, and the indentation must survive.

```ini
[quad_gantry_level]

#--------------------------------------------------------------------
##  Gantry Corners for 250mm Build
##  Uncomment for 250mm build
#gantry_corners:
#   -60,-10
#   310, 320
##  Probe points
#points:
#   50,25
#   50,175
#   200,175
#   200,25

##  Gantry Corners for 300mm Build
##  Uncomment for 300mm build
#gantry_corners:
#   -60,-10
#   360,370
##  Probe points
#points:
#   50,25
#   50,225
#   250,225
#   250,25

##  Gantry Corners for 350mm Build
##  Uncomment for 350mm build
gantry_corners:              # CHANGED — uncommented for 350
   -60,-10                   # CHANGED
   410,420                   # CHANGED
##  Probe points
points:                      # CHANGED — uncommented for 350
   50,25                     # CHANGED
   50,275                    # CHANGED
   300,275                   # CHANGED
   300,25                    # CHANGED

#--------------------------------------------------------------------
speed: 100
horizontal_move_z: 10
retries: 5
retry_tolerance: 0.0075
max_adjust: 10
```

**Check:** `gantry_corners` has exactly two coordinate lines and `points` exactly four, all indented by three spaces. Klipper errors loudly if a continuation line loses its indent, so a bad edit here fails at Step 12.37 rather than silently.

[src](https://github.com/MotorDynamicsLab/LDOVoron2/blob/main/Firmware/leviathan-printer-rev-d-sbv2.cfg)

---

### Step 12.27 — 350 mm: resonance probe point and the G32 homing end position

(no image — see text)

**Parts:** none.

**Do:** Two more 350 blocks that the survey's checklist does not mention. In `[resonance_tester]`:

```ini
[resonance_tester]
accel_chip: adxl345
accel_per_hz: 100
sweeping_accel: 400
sweeping_period: 0
##--------------------------------------------------------------------
## Uncomment below for 350mm build
probe_points:                # CHANGED — uncommented for 350
    175, 175, 20             # CHANGED
##--------------------------------------------------------------------
```

and in `[gcode_macro G32]`:

```ini
[gcode_macro G32]
gcode:
    SAVE_GCODE_STATE NAME=STATE_G32
    G90
    G28
    QUAD_GANTRY_LEVEL
    G28
    ##  Uncomment for for your size printer:
    #--------------------------------------------------------------------
    ##  Uncomment for 350mm build
    G0 X175 Y175 Z30 F3600   ; CHANGED — uncommented for 350
    #--------------------------------------------------------------------
    RESTORE_GCODE_STATE NAME=STATE_G32
```

**Check:** `grep -n '^#position_max: 350\|^#points:\|^#probe_points:' printer.cfg` returns nothing for the 350 variants.

**Naming note:** the config header calls this *"Homing end position — `[gcode_macro G32]` section"*. This kit does **not** use a `[homing_override]` block; homing behaviour lives in `[safe_z_home]` (Step 12.33) and this G32 macro. Do not add a `[homing_override]` — an incorrect one drives the nozzle into the bed. [src](https://github.com/MotorDynamicsLab/LDOVoron2/blob/main/Firmware/leviathan-printer-rev-d-sbv2.cfg)

---

### Step 12.28 — Verify the 0.9° A/B motor setting

(no image — see text)

**Parts:** none.

**Do:** Confirm — do not change — that `[stepper_x]` and `[stepper_y]` both read:

```ini
full_steps_per_rotation:400  #set to 200 for 1.8 degree stepper
```

and that `[extruder]` reads `full_steps_per_rotation: 200`.

**Check:** X/Y = 400, extruder = 200, and none of the four `[stepper_z*]` sections has a `full_steps_per_rotation` line at all (they inherit the 200 default).

**Why:** the Rev D+ A/B motors are `LDO-42STH48-2004MAH(VRN)`, **0.9°** — 400 full steps per revolution. The Z motors (`LDO-42STH48-2004AC(VRN)`) and the extruder motor (`LDO-36STH20-1004AHG(VRN)`) are 1.8°. LDO already sets this correctly in the `-sbv2` config; the value is on this checklist only because it is the one thing that will silently halve or double every X/Y dimension if someone "fixes" it. [src](https://docs.ldomotors.com/en/voron/voron2/350_BOM/Rev_D)

---

### Step 12.29 — Probe: Omron active, Klicky written but commented

(no image — see text)

**Parts:** none.

**Do:** The kit ships both probes. Build stock — Omron inductive for QGL only, LDO nozzle probe for Z0 — and leave the Klicky parts bagged. Replace the `[probe]` section with the following, which keeps LDO's live values and parks a Klicky block beside them:

```ini
[probe]
##  Inductive Probe (Omron) — ACTIVE
##  Connected to Z-PROBE on the Nitehawk-SB V2
##  This probe is not used for Z height, only Quad Gantry Leveling
pin: nhk:PC15
x_offset: 0
y_offset: 25.0
z_offset: 0
speed: 10.0
samples: 3
samples_result: median
sample_retract_dist: 3.0
samples_tolerance: 0.006
samples_tolerance_retries: 3

##  ---- Klicky alternative — NOT ACTIVE ----------------------------------
##  Comment out the [probe] block above before uncommenting this one.
##  Klicky also needs the klicky-probe macro set, a printed dock, and its own
##  attach/dock sequence inside QUAD_GANTRY_LEVEL. On the toolhead PCB the
##  Klicky cable goes to the same PROBE port, but the 24V pin is not connected.
##  Confirm the sense of the switch with QUERY_PROBE before ANY Z move: if it
##  reports TRIGGERED with the probe off the dock, add a leading "!" to the pin.
#[probe]
#pin: ^nhk:PC15             # (verify on bench) — microswitch needs a pull-up
#x_offset: 0                # (verify on bench) — depends on your dock/mount
#y_offset: 19.75            # (verify on bench) — klicky default, measure yours
#z_offset: 6.42             # (verify on bench) — set by PROBE_CALIBRATE
#speed: 10.0
#samples: 3
#samples_result: median
#sample_retract_dist: 3.0
#samples_tolerance: 0.006
#samples_tolerance_retries: 3
```

**Check:** exactly one live `[probe]` section. `grep -c '^\[probe\]' printer.cfg` returns 1.

⚠ **Rev D+ / LDO:** the PROBE port on the Nitehawk-SB **V2** is **JST-PH2.0**, not the JST-XH2.5 the wiring guide describes. A spare probe pigtail crimped to the documented XH2.5 will not fit, and a PH2.0 housing can be forced into the wrong header (survey §4.1 ③). Also: the fibreglass tape goes on the **front and sides** of the Omron only — never the back or the bottom, or it will not sense. [src](https://docs.ldomotors.com/en/voron/voron2/wiring_guide_rev_d) · [src](https://github.com/MotorDynamicsLab/Nitehawk-SB-V2)

---

### Step 12.30 — Hotend: E3D Revo HF

(no image — see text)

**Parts:** none.

**Do:** Confirm the `[extruder]` heater and sensor block matches your hotend. For the kit's Revo HF, LDO's shipped values are already correct — verify rather than edit:

```ini
heater_pin: nhk:PA7
## Check what thermistor type you have.
sensor_type: ATC Semitec 104NT-4-R025H42G   # correct for the Revo 60 W 104NT HeaterCore
sensor_pin: nhk:PB12
pullup_resistor: 2200                        # Nitehawk TH0 port has 2k2 pull-ups
min_temp: 10
max_temp: 270                                # Revo HF core is rated 300 C; 270 is LDO's cap
max_power: 1.0
min_extrude_temp: 170
control = pid
pid_kp = 26.213
pid_ki = 1.304
pid_kd = 131.721
```

**Check:** `sensor_type` reads `ATC Semitec 104NT-4-R025H42G` and `pullup_resistor: 2200` is present. Leave the PID values alone — `PID_CALIBRATE HEATER=extruder TARGET=245` in Ch 13 replaces them.

**Sourcing:** E3D publishes the Revo 60 W 104NT HeaterCore as *Thermistor Type: Semitec 104NT-4-R025H42G*, *Klipper Setting: "ATC Semitec 104NT-4-R025H42G"*, *60W*, *Max Printing Temperature: 300°C*. Use the Revo's **integrated** thermistor lead into TH0; the loose Semitec 104NT in the kit bag is a spare. [src](https://e3d-online.com/pages/revo-support-60w-104nt-heatercore)

⚠ **Rev D+ / LDO:** the wiring guide says the TH0 connector is *"JST-XH2.5 two pin"*. On the V2 board it is **JST-PH2.0** (survey §4.1 ③). The heater screw terminal and the E0508 ferrule spec are unchanged. If you fitted a Rapido HF instead of the Revo, its thermistor is a different part — re-check `sensor_type` against its datasheet before power-up. [src](https://docs.ldomotors.com/en/voron/voron2/wiring_guide_rev_d)

---

### Step 12.31 — Bed heater and chamber sensor

(no image — see text)

**Parts:** none.

**Do:** Verify, do not edit:

```ini
[heater_bed]
##  SSR Pin - HEATBED
##  Thermistor - TH1
heater_pin: PG11
sensor_type: ATC Semitec 104NT-4-R025H42G
sensor_pin: PA2
pullup_resistor: 2200                  # Leviathan thermistor ports are 2k2
max_power: 0.6
min_temp: 0
max_temp: 120
control: pid
pid_kp: 58.437
pid_ki: 2.347
pid_kd: 363.769

[temperature_sensor chamber_temp]
## Chamber Temperature — plugs into the CT port on the toolhead PCB
sensor_type: ATC Semitec 104NT-4-R025H42G
sensor_pin: nhk:PB2
min_temp: 0
max_temp: 100
gcode_id: chamber_th
```

**Check:** after Step 12.37, Mainsail's temperature panel shows **bed** and **chamber** within ~2 °C of room temperature. If the chamber reads obviously wrong while the bed and hotend read correctly, the CT port's pull-up is the suspect — LDO's board-level config for that port specifies `pullup_resistor: 4700` (Klipper's default, which is why the kit config omits the line); add an explicit value only if the reading is wrong.

**Note:** `max_power: 0.6` on the bed is deliberate — a 355×355 heatpad at full power warps the plate. Do not raise it. The Leviathan README specifies *"4x Thermistor ports with 2k2 ohm pullup resistors"*, which is where the bed's `2200` comes from. [src](https://github.com/MotorDynamicsLab/Leviathan) · [src](https://github.com/MotorDynamicsLab/Nitehawk-SB-V2/blob/master/Configs/nitehawk-sbv2.cfg)

---

### Step 12.32 — Fans and lighting: Nevermore, COB strips, bay fans

![LDO Rev D: fan and LED strip connections](https://raw.githubusercontent.com/MotorDynamicsLab/LDOVoron2/main/Images/WiringGuide/RevD/S7_fan.jpg)

**Parts:** none.

**Do:** The kit's mainboard fan/LED mapping, per the wiring guide's own table, is: **PCB Fan → FAN2/PF7**, **LED Strip → LED-Strip/PE6**, **Filter Fan → FAN3/PF9**. Note what LDO's config calls FAN3 and what is actually plugged into it. Edit as follows:

```ini
[fan]
##  Print Cooling Fan - FAN0 (toolhead, 5015 blower on fan adapter P4)
pin: nhk:PA15
##tachometer_pin: nhk:PD2
kick_start_time: 0.5
off_below: 0.10

[heater_fan hotend_fan]
##  Hotend Fan - FAN1 (toolhead, 4010 axial on fan adapter P2)
pin: nhk:PD0
#tachometer_pin: nhk:PD1
max_power: 1.0
kick_start_time: 0.5
heater: extruder
heater_temp: 50.0

[controller_fan controller_fan]
##  Electronics bay fans — 2x 6020 joined by the 3x2 splicer PCB. FAN2 / "PCB FAN"
pin: PF7
##tachometer_pin: PF6
kick_start_time: 0.5
heater: heater_bed

##  ---- REPLACES LDO's [heater_fan exhaust_fan] ---------------------------
##  FAN3 is labelled "FILTER FAN" in the harness and feeds the Nevermore
##  Micro V5 Duo. LDO's stock config declares it as a [heater_fan] slaved to
##  the bed at 60 C, which cannot be commanded from the slicer or a macro.
##  fan_generic lets PRINT_START run it during the print and leave it running
##  afterwards, which is the whole point of a recirculating filter.
[fan_generic nevermore]                # CHANGED — was [heater_fan exhaust_fan]
pin: PF9
max_power: 1.0
shutdown_speed: 0.0
kick_start_time: 5.0

##  ---- LDO stock, kept for reference — NOT ACTIVE -----------------------
#[heater_fan exhaust_fan]
#pin: PF9
#max_power: 1.0
#shutdown_speed: 0.0
#kick_start_time: 5.0
#heater: heater_bed
#heater_temp: 60
#fan_speed: 1.0

## Chamber Lighting — 2x COB strips joined by the 2x3 splitter PCB, LED-STRIP port
[output_pin caselight]
pin: PE6
pwm: true
hardware_pwm: False
value: 0.20                   # startup brightness
shutdown_value: 0
#value:1                      # CHANGED — commented out; see note below
cycle_time: 0.00025
```

**Check:** `grep -c '^\[heater_fan exhaust_fan\]' printer.cfg` returns 0, `grep -c '^\[fan_generic nevermore\]' printer.cfg` returns 1, and `[output_pin caselight]` contains exactly one live `value:` line.

**Why the caselight edit:** LDO's stanza declares `value` **twice** — `value: 0.20` and then `value:1`. Klipper builds its parser with `RawConfigParser(strict=False)`, so duplicate keys are accepted silently and the **last one wins**: the COB strips come up at full brightness on every boot, and the 0.20 you thought you set is dead text. The same duplicate is present in LDO's Leviathan-repo configs, so it is not a transcription error in your file. [src](https://github.com/Klipper3d/klipper/blob/master/klippy/configfile.py)

⚠ **Rev D+ / LDO:** the stock exhaust-filter fan is **not included** in the Rev D kit, so nothing else wants FAN3. The Nevermore Micro V5 Duo is built in Ch 11 and is the only thing on that port. [src](https://docs.ldomotors.com/en/voron/voron2/wiring_guide_rev_d)

---

### Step 12.33 — Z endstop: leave `safe_z_home` deliberately unreachable

(no image — see text)

**Parts:** none.

**Do:** Do **not** guess the nozzle-probe coordinates. Leave the section as LDO ships it and add a marker:

```ini
[safe_z_home]
##  XY Location of the Z Endstop Switch
##  Update -10,-10 to the XY coordinates of your endstop pin
##  after going through the "Z Endstop Pin Location Definition" step.
home_xy_position:-10,-10      # TODO Ch 13 — measured on the machine, NOT a 350 preset
speed:100
z_hop:10
```

**Check:** `home_xy_position` is still `-10,-10`, and you understand that `G28 Z` will fail in Ch 13 with **"Move out of range"** until you replace it.

**Why leave it broken:** `-10,-10` is outside `position_min: 0` for both X and Y, so Klipper refuses the move rather than attempting it. That refusal *is* the safety interlock. Substituting a plausible-looking value — bed centre, say — makes `G28 Z` drive the nozzle down at a spot where there is no pin, into the build plate. The LDO nozzle probe's real XY location is read off the machine during the startup wizard's *Z Endstop* page in Ch 13. [src](https://docs.vorondesign.com/build/startup/) · [src](https://docs.ldomotors.com/en/voron/voron2/wiring_guide_rev_d)

---

### Step 12.34 — Add a `[bed_mesh]` section

(no image — see text)

**Parts:** none.

**Do:** There is **no `[bed_mesh]` anywhere in the LDO config**. Add this block (anywhere above the macros; next to `[quad_gantry_level]` reads well):

```ini
#####################################################################
#   Bed Mesh  — ADDED, not present in the LDO config
#####################################################################

[bed_mesh]
speed: 300
horizontal_move_z: 10
##  mesh_min / mesh_max are PROBE coordinates, not nozzle coordinates.
##  The Omron sits at y_offset +25, so the toolhead goes to (X, Y-25):
##  mesh_min Y 30 -> toolhead Y 5;  mesh_max Y 320 -> toolhead Y 295. Both legal.
mesh_min: 30, 30
mesh_max: 320, 320
probe_count: 7, 7
algorithm: bicubic
##  Z0 comes from the nozzle-probe endstop, and [probe] z_offset is 0 because
##  the Omron is a QGL-only probe. Without a zero reference the whole mesh
##  would be offset by the Omron's trigger height. Pin it to bed centre:
zero_reference_position: 175, 175
fade_start: 1.0
fade_end: 10.0
fade_target: 0
adaptive_margin: 5
```

**Check:** `mesh_max` minus the probe's `y_offset` (25) is ≤ `position_max` (350) on Y, and `mesh_min` Y (30) minus 25 is ≥ `position_min` (0). Both hold. Klipper will reject the section at restart if they do not.

**Why `zero_reference_position` is not optional here:** `[probe] z_offset: 0` — LDO's own comment says *"This probe is not used for Z height, only Quad Gantry Leveling"*. A mesh built with an uncalibrated probe carries the probe's trigger height as a constant offset on every point. `zero_reference_position` subtracts the mesh value at the named point from the whole mesh, making it purely relative and safe to apply on top of a nozzle-probe Z0. [src](https://www.klipper3d.org/Config_Reference.html#bed_mesh)

**Note:** 7×7 with `[probe] samples: 3` is 147 probes and takes a while. Use `BED_MESH_CALIBRATE SAMPLES=2` for routine meshes, and `ADAPTIVE=1` (as PRINT_START does below) to mesh only the area the print actually covers — which is what makes a per-print mesh practical on a 350 (survey §4.4 #15). [src](https://www.klipper3d.org/G-Codes.html#bed_mesh_calibrate)

---

### Step 12.35 — Add `[input_shaper]` and `[exclude_object]`

(no image — see text)

**Parts:** none.

**Do:** Add both. `[input_shaper]` goes in as a disabled placeholder so Ch 14 has somewhere to write:

```ini
#####################################################################
#   Input shaper  — ADDED, placeholder. Values come from Ch 14.
#####################################################################

[input_shaper]
##  Leave both frequencies commented until you have run SHAPER_CALIBRATE
##  on a machine that has already produced a good first print (survey §3.3).
##  The ADXL345 is on the toolboard; [resonance_tester] is already configured.
#shaper_freq_x: 0
#shaper_freq_y: 0
#shaper_type: mzv

#####################################################################
#   Object exclusion  — ADDED
#####################################################################

[exclude_object]
```

**Check:** Klipper accepts a bare `[input_shaper]` with no frequencies — that is a valid "shaping disabled" state, not an error. `[exclude_object]` takes no parameters at all.

**Also:** for cancel-object to actually work, the G-code needs object labels. Either turn on PrusaSlicer's **Output options → Label objects → Firmware-specific**, or set `enable_object_processing: True` under `[file_manager]` in `moonraker.conf` and let Moonraker inject them. Slicer-side is cheaper — Moonraker's preprocessor is file-I/O heavy. Decide this in the slicer chapter, not here. [src](https://www.klipper3d.org/Config_Reference.html#input_shaper) · [src](https://moonraker.readthedocs.io/en/latest/configuration/)

---

### Step 12.36 — Replace `PRINT_START` with a skeleton that waits on the chamber

(no image — see text)

**Parts:** none.

**Do:** LDO's stock `PRINT_START` is three lines and takes no parameters. Replace it. Leave `PRINT_END` alone — it already ends with `BED_MESH_CLEAR`, which pairs correctly with the mesh you just added.

```ini
[gcode_macro PRINT_START]
#   Slicer start G-code:  PRINT_START EXTRUDER={first_layer_temperature[0]} BED={first_layer_bed_temperature[0]} CHAMBER=45
#   CHAMBER=0 (the default) skips the chamber wait entirely and does a timed soak instead.
gcode:
    {% set bed      = params.BED|default(100)|float %}
    {% set extruder = params.EXTRUDER|default(240)|float %}
    {% set chamber  = params.CHAMBER|default(0)|float %}
    {% set soak     = params.SOAK|default(8)|int %}

    CLEAR_PAUSE
    BED_MESH_CLEAR
    SET_GCODE_OFFSET Z=0

    SET_DISPLAY_TEXT MSG="Homing"
    G28                                    ; cold home; Z on the nozzle-probe pin
    G90
    G0 X175 Y175 Z30 F3600                 ; park over centre  <-- 350 only

    SET_DISPLAY_TEXT MSG="Bed {bed}C"
    SET_FAN_SPEED FAN=nevermore SPEED=1    ; filter runs from the start of the soak
    M140 S{bed}
    M190 S{bed}                            ; wait for the bed

    {% if chamber > 0 %}
      SET_DISPLAY_TEXT MSG="Chamber {chamber}C"
      M106 S255                            ; part fan stirs the chamber while soaking
      TEMPERATURE_WAIT SENSOR="temperature_sensor chamber_temp" MINIMUM={chamber}
      M107
    {% else %}
      SET_DISPLAY_TEXT MSG="Soak {soak} min"
      G4 P{soak * 60000}
    {% endif %}

    SET_DISPLAY_TEXT MSG="QGL"
    M104 S150                              ; 150C for QGL: hot enough to be dimensionally
    TEMPERATURE_WAIT SENSOR=extruder MINIMUM=145   ; honest, cold enough not to ooze
    QUAD_GANTRY_LEVEL
    G28 Z                                  ; re-home Z hot; this is the Z0 that counts

    SET_DISPLAY_TEXT MSG="Meshing"
    BED_MESH_CALIBRATE ADAPTIVE=1

    SET_DISPLAY_TEXT MSG="Hotend {extruder}C"
    G0 X175 Y175 Z10 F3600                 ; <-- 350 only
    M109 S{extruder}

    ##  TODO Ch 14: purge / prime line goes here, once the nozzle is calibrated.

    G21
    G90
    M83                                    ; relative extrusion
    G92 E0
    SET_DISPLAY_TEXT MSG="Printing"
```

**Check:** the macro parses at Step 12.37. Do not run it — `G28` will fail until Step 12.33's TODO is closed in Ch 13.

⚠ **`TEMPERATURE_WAIT` has no timeout.** If the chamber never reaches `CHAMBER`, the macro blocks forever and the only way out is cancelling the print. Keep `CHAMBER=0` (timed soak) until you have measured what your chamber actually reaches with the door shut and the bed at your print temperature. [src](https://www.klipper3d.org/G-Codes.html#temperature_wait)

**Ordering note:** bed heat and soak come first, then QGL hot, then the mesh — matching the Voron wizard's own order and the rule that a thermally unstable machine will not QGL repeatably (survey §3.3, §4.4 #16). `SET_DISPLAY_TEXT` needs `[display_status]`, which arrived with `[include mainsail.cfg]` in Step 12.22. [src](https://docs.vorondesign.com/build/startup/)

---

### Step 12.37 — The config-compiles check

(no image — see text)

**Parts:** none.

**Do:** In Mainsail's editor press **SAVE & RESTART**. Then, if anything at all looks wrong, run `FIRMWARE_RESTART` from the console — that restarts the MCUs as well as the host. Read the whole console output, not just the last line.

**Check:** all four of these, and nothing less:

1. Mainsail's status reads **Ready**. No red banner, no orange "missing configuration" panel.
2. `STATUS` in the console returns without an error.
3. The console startup block lists **two** MCUs — `mcu` and `mcu nhk` — and no `Unable to connect` or `Command format mismatch`.
4. The temperature panel shows **extruder**, **heater_bed** and **chamber** all reading within a couple of degrees of room temperature.

**Do not** home, jog, heat or run a fan. Every one of those is a Ch 13 step with its own safety check in front of it.

⚠ If you get *"MCU 'nhk' shutdown: Command format mismatch"*, the toolboard firmware and the host Klipper were built from different commits — go back to Step 12.17 and rebuild from the current `~/klipper`. [src](https://docs.mainsail.xyz/faq/klipper_errors/command-format-mismatch/)

---

## Checkpoint 12

- [ ] MainsailOS boots, is reachable at your hostname, and every component in the Update Manager is up to date.
- [ ] The Klipper version string from Step 12.7 is written down, and **both** MCUs were flashed from that same working copy.
- [ ] `ls /dev/serial/by-id/` shows exactly two Klipper devices: one `stm32g0b1xx` (Nitehawk-SB V2) and one `stm32f446xx` **or** `stm32h743xx` (Leviathan). No `katapult` entries.
- [ ] `printer.cfg` is the **`-sbv2`** file — `grep -c 'nhk:PB8' printer.cfg` returns 1 and `grep -c gpio2 printer.cfg` returns 0.
- [ ] Line 1 is `[include mainsail.cfg]`, and Mainsail shows no missing-configuration panel.
- [ ] All six 350 mm sites are uncommented: `[stepper_x]`, `[stepper_y]`, `[stepper_z]`, `[quad_gantry_level]`, `[resonance_tester]`, `[gcode_macro G32]`.
- [ ] `[bed_mesh]` exists and carries `zero_reference_position: 175, 175`.
- [ ] `[input_shaper]` and `[exclude_object]` exist; exactly one live `[probe]` section.
- [ ] `[fan_generic nevermore]` on PF9; `[output_pin caselight]` has one live `value:`.
- [ ] `safe_z_home` still reads `-10,-10` with the Ch 13 TODO next to it.
- [ ] `STATUS` is clean after `RESTART`, both MCUs connected, three sensors reading room temperature.
- [ ] KlipperScreen is running and the DSI panel shows the right way up.
- [ ] Nothing has been homed, heated or jogged.

## Common mistakes

- **Downloading `leviathan-printer-rev-d.cfg`.** The wiring guide links it and it looks right. Every `nhk:` pin in it belongs to an RP2040. Grep for `nhk:PB8` before you upload anything.
- **Hunting for `rp2040` in `/dev/serial/by-id/`.** There is no RP2040 in a Rev D+ kit. The toolboard is `stm32g0b1xx`. The guide is wrong; the board is not.
- **Building MCU firmware before running the Update Manager.** You will flash both boards twice. Update the host first, then flash.
- **Omitting the bootloader offset in `make menuconfig`.** 8 KiB for the Nitehawk, 32 KiB (F446) or 128 KiB (H743) for the Leviathan. Flash with no offset and Katapult is gone, and the only way back is DFU with the board buttons.
- **Following the V1.3 Leviathan guide on a V1.2 board.** STM32H743/25 MHz/128 KiB against STM32F446/12 MHz/32 KiB. Read the silkscreen and the serial ID before menuconfig, not after.
- **Filling in `home_xy_position` with a guess.** `-10,-10` failing is the interlock working. A plausible wrong value drives the nozzle into the plate.
- **Adding `[bed_mesh]` without `zero_reference_position`.** The Omron's `z_offset` is 0 by design, so the raw mesh carries its whole trigger height as a constant offset.

## Next

**Ch 13 — First power-up and initial startup**: work the Voron startup wizard in its own order (temperatures → heaters → fans → `STEPPER_BUZZ` → XY endstop → homing → bed locating → 0,0 → Z endstop → probe → PID → QGL → Z-offset), which closes the `safe_z_home` TODO from Step 12.33.
