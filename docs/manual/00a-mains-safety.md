# Chapter 00a — Mains safety: read before Chapter 09

Everything you must decide, buy and agree *before* the electronics bay exists: who is allowed to do the mains work, who is allowed in the room, what meter you need, where the protective earth runs in this machine, and what to do when it goes wrong. Nothing is built here — this chapter exists so that Ch 09 and Ch 10 never stop to ask a question that should already have an answer.

**Time:** 0.75–1.0 h hands-on, first build — reading, one shopping decision, one outlet check. No kit parts are touched.

**Sessions:** 2 × ~30 min

**Prerequisites:**

- **Ch 00 — Before you start**, at least through [Step 00.8](00-before-you-start.md#step-008-settle-the-tool-list-owned-vs-buy) (the tool table, where the multimeter is a "Buy if not owned" row) and [Step 00.30](00-before-you-start.md#step-0030-start-the-build-log) (the build log and your daughter's assigned jobs). This chapter turns both of those into rules.
- **Print batches: none.** Nothing here is printed, mounted or wired.
- Read this **before Ch 09**, not before Ch 10. Ch 09 already puts the inlet, the PSU and the SSR into the machine; by the time you open Ch 10 the decisions below are already spent.

**Tools**

- Digital multimeter — see [Step 00a.3](#step-00a3-buy-a-meter-that-is-rated-for-the-job) for the minimum spec. This is the one tool in the build with a safety rating, not just a tolerance.
- The multimeter's own test leads, rated at or above the meter's category
- A known-live wall outlet you can reach (for the meter self-test)

**Consumables:** none.

**Printed parts:** none. No print batch gates this chapter.

**Hardware**


| Fastener / part | Qty | Note |
|---|---|---|
| — nothing is consumed in this chapter — | 0 | every mains part stays in its box until [Ch 09](09-electronics-bay.md) |

**Read first**

- **Mains is the only irreversible hazard in this build.** Every other safety fact in this manual is stated at the step that needs it. This one cannot be, because the decisions — who wires it, what meter, which outlet — are made weeks earlier. [src](https://docs.vorondesign.com/build/electrical/)
- **There is no step in this manual where a 13-year-old touches mains wiring.** [Step 00a.2](#step-00a2-write-the-who-is-in-the-room-rule-and-post-it-on-the-wall) names the exact stretches she is not present for, and what she does instead.
- **The meter is not optional and it is not a formality.** Ch 10's Checkpoint #1 is seven meter measurements on an unplugged machine, and it is the hard gate before the bay closes (survey §5.2 W8).
- **If your local rules say a certified person must make the mains connections, that is the whole of Ch 10 Section 1.** Decide it now, not with the printer on its back and the WAGOs half-populated.
- **Nothing in this chapter overrides a step.** Where this chapter and a step disagree, the step wins and the disagreement is a bug — log it in the corrections table in [00-index.md](00-index.md).

---

## Before the kit arrives

### Step 00a.1 — Decide who is doing the mains work

(no image — see text)

**What you're looking at:** No parts — a decision about one stretch of the build. The conductors in question are the ones that carry wall voltage: the C14 inlet where the power cord plugs in, the WAGO lever blocks that fan it out, the PSU's AC terminal block, the solid-state relay that switches the bed heater, and the heater's own live lead. Everything else in this machine runs on 24 V and is not this conversation.

**Parts:** none.

**Do:** This build has exactly one region that can kill you: **Ch 10 Section 1, Steps [10.1](10-wiring.md#step-101-empty-the-bay-and-set-the-end-state)–[10.16](10-wiring.md#step-1016-frame-pe)** — the C14 inlet, the three-way WAGO bus, the Meanwell LRS-200-24's AC terminal block, the Omron SSR's LOAD pair, and the bed heater's live lead. Read your local rules for who may make those connections in a dwelling. If the answer is "not you", the Voron community's standard advice applies: build the machine, mount every part, and *"install the parts and then find a qualified electrician to do the connecting up."* Ch 10's own **Read first** says the same thing and names the stopping line — get to [Step 10.4](10-wiring.md#step-104-fit-the-ac-inlet-into-the-printed-plug-panel) and hand over. Write the decision down today; it changes nothing else in the build order.

**Check:** One line in the build log naming who lands the mains conductors, dated before the kit ships.

Source: [Ch 10 — Read first](10-wiring.md) · [Voron forum — Mains Wiring Safety](https://forum.vorondesign.com/threads/mains-wiring-safety.1998/) · [Voron docs — Electrical Wiring](https://docs.vorondesign.com/build/electrical/)

---

### Step 00a.2 — Write the "who is in the room" rule and post it on the wall

(no image — see text)

**What you're looking at:** No parts — a written rule for the two people building this printer. It names the exact step ranges where only one person is at the machine, and what the other person does instead, so the rule is decided in daylight rather than at the bench.

**Parts:** none.

**Do:** [Step 00.30](00-before-you-start.md#step-0030-start-the-build-log) gives your daughter the camera and the measurement log — *"the diagonals in Ch 01 are hers to read out"*. That assignment has no carve-out for mains, so write one, in these words:

- She does not strip, land, tighten or unplug any conductor that is or has been connected to the wall.
- She is not in the room while the mains conductors are being worked on — **Ch 10 Section 1 ([10.1](10-wiring.md#step-101-empty-the-bay-and-set-the-end-state)–[10.16](10-wiring.md#step-1016-frame-pe))** and **Ch 10 Section 2 ([10.17](10-wiring.md#step-1017-de-energise-and-set-up)–[10.23](10-wiring.md#step-1023-first-power-on-then-off-again))**.
- She is not beside the machine at the two power-ons: [Step 10.23](10-wiring.md#step-1023-first-power-on-then-off-again) and [Step 13.3](13-initial-startup.md#step-133-first-power-on-hand-on-the-switch). One adult, standing to the side, hand on the switch — nobody else within reach of the machine.
- What she *does* own on those days: she photographs the finished bay once the cord is out of the room ([Step 10.72](10-wiring.md#step-1072-photograph-the-bay)), and she reads out the meter values while you hold the probes. Reading numbers out loud is a real job — it is how you catch a row you skipped.

Post it where you both see it. Say it out loud once, before Ch 09.

**Check:** The rule is written, posted, and has been read aloud. Neither of you has to reconstruct it at 22:00 with the printer on its back.

⚠ This rule is not about competence. It is about there being only one pair of hands near a live conductor, and about that pair belonging to the person who can also reach the breaker.

Source: [Ch 00 Step 00.30](00-before-you-start.md#step-0030-start-the-build-log) · [Ch 10 Sections 1–2](10-wiring.md#section-1-mains-inlet-switch-psu-ssr-bed-heater) · [Ch 13 Step 13.3](13-initial-startup.md#step-133-first-power-on-hand-on-the-switch)

---

### Step 00a.3 — Buy a meter that is rated for the job

(no image — see text)

**What you're looking at:** No parts — the meter you will buy. A digital multimeter measures continuity, resistance, DC volts and AC volts; the **CAT rating** printed on its face says how large an electrical surge the meter can survive at the place you are using it, which is a different question from what voltage it can display ([glossary](16-glossary.md#c)). The four functions in the table are the ones Ch 10's Checkpoint #1 asks for.

**Parts:** none.

**Do:** [Step 00.8](00-before-you-start.md#step-008-settle-the-tool-list-owned-vs-buy) lists the multimeter as one row in a thirteen-row table. This is that row expanded. A meter's **CAT rating** says what size transient it can survive where you are using it, not what voltage it can display — a meter with no category rating, or the wrong one, can fail violently. Fluke's definitions: **CAT II** is *"Single-phase receptacle-connected loads such as appliances and portable tools"*; **CAT III** is *"3-phase distribution including single-phase commercial lighting and equipment in fixed locations such as switchgear and polyphase motors."* This printer is a receptacle-connected appliance, so CAT II is the category — buy **CAT III 600 V** anyway, because it is the common rating on decent meters and it leaves you margin if you ever probe at a panel.

| Function | Why this build needs it | Used at |
|---|---|---|
| Continuity / beeper | every Checkpoint #1 measurement | [10.17](10-wiring.md#step-1017-de-energise-and-set-up)–[10.21](10-wiring.md#step-1021-the-ssr-is-open-when-unpowered) |
| Resistance (Ω) | bed heater, thermistors, PE bonding, 24 V shorts | [10.13](10-wiring.md#step-1013-measure-the-bed-heater-before-you-connect-it), [10.74](10-wiring.md#step-1074-24-v-rails), [10.76](10-wiring.md#step-1076-thermistors-at-room-temperature), [10.77](10-wiring.md#step-1077-protective-earth-bonding) |
| DC volts | the 24 V rail at first power-on | [10.23](10-wiring.md#step-1023-first-power-on-then-off-again), [10.73](10-wiring.md#step-1073-confirm-dead) |
| AC volts, 600 V range | the meter self-test in [00a.4](#step-00a4-test-the-meter-before-you-trust-it-and-again-after); never used inside the machine | this chapter only |

Two details worth getting right. **Resistance range:** Ch 10's tool list asks for "at least 2 MΩ", but [Step 10.13](10-wiring.md#step-1013-measure-the-bed-heater-before-you-connect-it) wants to see the bed heater read *"well above 10 MΩ"* to earth, and [Step 10.76](10-wiring.md#step-1076-thermistors-at-room-temperature) reads thermistors up to 162 kΩ. A 2 MΩ meter answers the pass/fail (anything higher shows `OL`, which is the pass), but a meter that ranges to 20 MΩ or more turns a pass into a number you can write in the log. **Leads:** they carry their own CAT rating and it is the *lower* of meter and lead that governs. Do not put unrated leads on a rated meter.

**Check:** Meter on the bench with a category rating printed on its face, leads rated to at least the same category, fresh battery, and the four functions above found and tried once.

Source: [Fluke — IEC category ratings](https://www.fluke.com/en-us/learn/blog/safety/iec-category-ratings-use-the-right-tools-for-the-job) · [Ch 00 Step 00.8](00-before-you-start.md#step-008-settle-the-tool-list-owned-vs-buy) · [Ch 10 — Tools](10-wiring.md)

---

### Step 00a.4 — Test the meter before you trust it, and again after

(no image — see text)

**What you're looking at:** The meter, its two test leads, and a wall outlet you know is live. **Live–dead–live** is the practice of proving the meter works immediately before and immediately after the measurement that matters ([glossary](16-glossary.md#l)) — a meter with a flat battery or a broken lead reads "no voltage" on a live conductor, which is the one wrong answer that gets someone hurt.

**Parts:** multimeter, a known-live wall outlet.

**Do:** A meter that has quietly died reads "no voltage" on a live conductor, which is the most dangerous reading in electrical work. The standard defence is **live–dead–live**: prove the meter on a known-live source, take your measurement, then prove the meter again on the same known-live source — if it failed in between, you find out before you act on the reading. Do it in this order the first time you use the meter, and every time you are about to touch something you have declared dead:

1. **Live** — AC volts on a wall outlet you know is on. It should read your nominal mains voltage.
2. **Dead** — the measurement you actually care about.
3. **Live** — back to the same outlet. Same reading as step 1.

Then the bench self-tests you will use constantly: on continuity, short the two probes tip to tip — it must beep and read near 0 Ω. Clip one probe to the other's tip along each lead in turn to prove neither lead is broken internally. Confirm the battery symbol is not showing. If the meter has a fused current jack, check the fuse now rather than discovering it during a measurement.

**Check:** Live–dead–live done once end to end. Probes shorted → beep, near 0 Ω. Both leads continuous. No low-battery symbol.

⚠ [Step 10.17](10-wiring.md#step-1017-de-energise-and-set-up) opens Checkpoint #1 by shorting the probes for exactly this reason. That is the short version of this step; this is the long one, and it is the one to use before you conclude anything is dead.

Source: [NFPA 70E live–dead–live practice](https://www.70econsultants.com/live-dead-live-test-comprehensive-guide-rozel/) · [Ch 10 Step 10.17](10-wiring.md#step-1017-de-energise-and-set-up)

---

### Step 00a.5 — Put the printer on an RCD/GFCI outlet you can reach

(no image — see text)

**What you're looking at:** The wall outlet the printer will live on, and the breaker that feeds it. An **RCD** (a GFCI receptacle or GFCI breaker in a US house) compares the current flowing out on live with the current returning on neutral and cuts the supply when they differ, because a difference means current is leaving by some other path — through the frame, or through a person ([glossary](16-glossary.md#g)).

**Parts:** none.

**Do:** A residual-current device compares live and neutral current and cuts the supply when they differ — which is what happens when current is leaving through a person or through the frame. RepRap's safety page is blunt about it: *"If not compulsory in your country, a 20mA resident current device (RCD) shall be installed on your electrical installation."* In a US house that is a **GFCI receptacle or a GFCI breaker**. Choose the outlet now, before the machine has a place to live:

- Press the outlet's **TEST** button and confirm it cuts power, then **RESET**. Repeat monthly for the life of the printer. A GFCI that does not trip on its own test button is a dead GFCI.
- Find the breaker that feeds it and label it. You need to be able to kill the circuit from outside the room.
- Give the printer a circuit that is not also feeding a space heater or a microwave. The PSU alone draws about **4 A at 115 VAC**, and the AC bed heater is a much larger load again — the Omron SSR that switches it is rated **10 A**.

**Check:** Outlet trips on TEST and resets. Breaker identified and labelled. You can reach that breaker without passing the machine.

Source: [RepRap — Safety](https://reprap.org/wiki/Safety) · [Mean Well LRS-200 spec sheet](https://www.meanwell.com/Upload/PDF/LRS-200/LRS-200-SPEC.PDF) · [Ch 09 Step 09.17](09-electronics-bay.md#step-0917-fit-the-ssr-to-its-metal-din-bracket)

---

Pause: ~30 min since the last pause — this is the chapter's first segment. Decisions made and written down, meter ordered or found and self-tested, outlet chosen and labelled. Nothing is open, nothing is wired, and no kit box has been touched. Do not start Ch 09 before finishing the rest of this chapter; the earth chain below is what Ch 09's placement decisions assume.

---

## The earth chain, the fuse and the terminals

### Step 00a.6 — Learn the protective-earth chain in this build

(no image — see [LDO Rev D bay, wiring complete](https://raw.githubusercontent.com/MotorDynamicsLab/LDOVoron2/main/Images/WiringGuide/RevD/VS9_Final.jpg))

**What you're looking at:** LDO's photo of a finished Rev D electronics bay. Every branch of the **protective earth** chain is in this one frame: the inlet at the back wall, the yellow/green WAGO block that fans it out, the PSU's earth screw, the ring terminal bolted to a frame extrusion, and the lead that runs up to the build plate ([glossary](16-glossary.md#p)). PE is the conductor that makes the machine safe to *touch* — it gives a stray live current a path of far lower resistance than you.

**Parts:** none.

**Do:** Protective earth (PE) is the conductor that makes the machine safe to *touch*: if a live conductor ever reaches the frame, the bed or a motor can, PE gives that current a path with far less resistance than you, and the fault current trips the breaker or the RCD. Voron's electrical page is explicit that this is not optional on an AC-bed machine — *"If using an AC powered bed, be sure to ground the bed regardless of if the assembly manual specifies it or not"*, and *"Grounding the frame is recommended."* RepRap adds the constraint people get wrong: *"Earth shall be connected to a valid earth, never on plumbing."* Learn the five branches before you see them:

| Branch | Runs from → to | Made at |
|---|---|---|
| Supply | wall socket earth → C14 **E** pin, through the C13 cord. Never switched, never fused | [10.5](10-wiring.md#step-105-verify-the-pre-wired-inlet-before-you-trust-it) |
| Bus | C14 **E** → the yellow **PE** WAGO (one of three 5-way blocks) | [10.7](10-wiring.md#step-107-populate-and-label-the-wago-bus), [10.8](10-wiring.md#step-108-inlet-wago-bus) |
| PSU | PE WAGO → the Meanwell's **⏚** terminal, the outermost of its three AC screws (⏚, N, L) | [10.9](10-wiring.md#step-109-wago-bus-psu) |
| Frame | PE WAGO → a frame extrusion, ring terminal sandwiched between two M5 locking washers on **bare** metal | [10.16](10-wiring.md#step-1016-frame-pe) |
| Bed | build plate → PE WAGO, ring terminal on the plate's own **M4×6 BHCS + serrated washer** | [03.6](03-build-plate.md#step-036-verify-the-pe-screw-and-identify-the-three-cables), [10.12](10-wiring.md#step-1012-bed-harness-into-the-bed-wago-breakout), [10.15](10-wiring.md#step-1015-bed-neutral-and-bed-pe-the-wago-bus) |

A sixth path is not protective earth but shares the same bus at the far end: the **ESD ground** from the extruder motor body to the toolboard, fitted at [Step 10.58](10-wiring.md#step-1058-fit-the-esd-grounding-path). It is why the extruder can appears in the earth-bonding table.

The whole chain is proved in one sweep at [Step 10.77](10-wiring.md#step-1077-protective-earth-bonding): from the C14 earth pin, the PE WAGO and PSU ⏚ read **< 1 Ω**, and the frame, bare plate aluminium and extruder motor body read **a few Ω or less** — while the bed heater's L and N, and every 24 V node, read `OL`.

**Check:** You can draw the five branches from memory and say where each is verified. That is the whole of the reason the bay is not allowed to close before Checkpoint #1.

⚠ **Rev D+ / LDO:** the bed's PE screw is **already fitted to the plate** and is an **M4×6 BHCS**, not the M3×6 the official manual asks you to supply. Verify it is tight at [Step 03.6](03-build-plate.md#step-036-verify-the-pe-screw-and-identify-the-three-cables); do not remove it and refit it. Its serrated washer is what bites through the surface to make the bond. [src](https://docs.ldomotors.com/voron/voron2/build-faq)

Source: [Voron docs — Electrical Wiring](https://docs.vorondesign.com/build/electrical/) · [RepRap — Safety](https://reprap.org/wiki/Safety) · [LDO wiring guide § Frame PE](https://docs.ldomotors.com/en/voron/voron2/wiring_guide_rev_d#connecting-the-ffc-cable-ethernet-cable-usb-cable-and-fame-pe) · [Ch 10 Step 10.77](10-wiring.md#step-1077-protective-earth-bonding)

---

### Step 00a.7 — The SSR is marked "earth the mounting rail" and this build does not

(no image — see [LDO S4 mapping](https://raw.githubusercontent.com/MotorDynamicsLab/LDOVoron2/main/Images/WiringGuide/RevD/S4_mapping.jpg))

**What you're looking at:** The **solid-state relay** on its metal bracket, with the wording on its body legible: *1 LOAD 2*, *3 + INPUT 4 −*, and the line this step is about — *EARTH THE MOUNTING RAIL*. An SSR is a semiconductor switch with no moving contacts; here it switches mains to the bed heater on a low-voltage signal from the mainboard ([glossary](16-glossary.md#s)). The photo is from LDO's Rev C guide, so the relay in it is the 20 A G3NB-220B-1 and the bus behind it is DIN terminal blocks; your Rev D kit ships the 10 A G3NB-210B-1 and WAGO 221 blocks, and carries the same marking.

**Parts:** none.

**Do:** [Step 10.10](10-wiring.md#step-1010-read-the-ssr-terminal-numbers-before-you-wire-it) records something you will read on the SSR body itself: *EARTH THE MOUNTING RAIL*. LDO's build does not run a PE conductor to the DIN rail. Understand the gap before you are standing in front of it:

- The SSR is an **Omron G3NB-210B-1** — 24–220 VAC 10 A on the **1 / 2 LOAD** pair, 5–24 VDC on the **3 + / 4 − INPUT** pair ([09.17](09-electronics-bay.md#step-0917-fit-the-ssr-to-its-metal-din-bracket)). It bolts to a stamped metal bracket which clips to a DIN rail, and that rail bolts to a frame extrusion at [Step 09.5](09-electronics-bay.md#step-095-fit-the-two-din-rails-running-left-to-right).
- So the rail *is* bonded to the frame, and the frame *is* earthed at [Step 10.16](10-wiring.md#step-1016-frame-pe) — but through anodised aluminium and steel screws, incidentally. Ch 10.16 tells you to scrape the anodising under the frame PE washer precisely because anodising is an insulator. An incidental bond through two more anodised interfaces is not the same thing as a PE conductor, and it is not a compliance argument.
- Ch 10 states the consequence plainly: if your local rules require an earthed rail, **that is a mains change** and it belongs to whoever signs off your mains work — not to a decision you make at the bench.

Two more facts from Omron's own datasheet that change how you handle this part. The standard G3NB **has no terminal cover** — Omron's note is that *"If you need a terminal cover, please use the G3NA-240B or similar product"* — so four mains-carrying screw terminals sit exposed in your bay until Ch 11 closes it. And the relay's internal snubber leaks: *"A leakage current flows through a snubber circuit in the G3NB even when there is no power input. Therefore, always turn OFF the power to the input or load and check that it is safe before replacing or wiring the G3NB."*

**Check:** You can state, before Ch 09, what the marking asks for, what this build actually does, and who decides if that is acceptable where you live.

⚠ Omron's caution for this relay family is *"Be sure to conduct wiring with the power supply turned OFF"* and *"Do not touch the G3NB's main circuit terminals immediately after the power is turned OFF."* Both are already how Ch 10 sequences the work — every mains connection is made with the cord in another room, and [Step 10.73](10-wiring.md#step-1073-confirm-dead) measures 0 V for ten seconds before anything is touched again.

Source: [Omron — Solid State Relays G3NB datasheet (J164-E1)](https://www.omron-ap.com/data_pdf/cat/g3nb-1_j164-e1_4_3_csm1013815.pdf) · [Ch 10 Step 10.10](10-wiring.md#step-1010-read-the-ssr-terminal-numbers-before-you-wire-it) · [Ch 09 Step 09.17](09-electronics-bay.md#step-0917-fit-the-ssr-to-its-metal-din-bracket)

---

### Step 00a.8 — Ferrules and the no-whisker rule

(no image — see text)

**What you're looking at:** The two kinds of mains terminal, side by side in LDO's Rev D bay. Above: the Meanwell PSU's three **screw terminals** (⏚, N, L), each taking a stranded core that has been crimped into a red **ferrule** — a metal sleeve that turns loose strands into one solid tube the screw can clamp ([glossary](16-glossary.md#f)). Below: the orange **WAGO 221** lever blocks, which clamp the core themselves and need no ferrule.

**Parts:** none — the kit supplies the ferrules.

**Do:** Two kinds of terminal carry mains in this machine and they want opposite things. **Screw terminals** — the Meanwell's ⏚/N/L block and the SSR's LOAD 1 / LOAD 2 — clamp a stranded core against a metal plate; strands splay, one escapes the clamp, and you are left with a reduced contact area that heats. Crimp a **ferrule** onto the core so the screw clamps a solid ferrule instead of loose strands. The kit ships **VE0508** ferrules for exactly this, counted in Ch 09 and used in Ch 10. **WAGO 221 lever terminals** — the three 5-way N / L / PE blocks — take bare stranded or ferruled core to the stop; the failure there is not splaying but *escaping*, and [Step 10.8](10-wiring.md#step-108-inlet-wago-bus) gives the test: tug each core hard, and confirm **no copper is visible outside any port**. A whisker of exposed strand next to a live terminal is the failure mode.

On conductor size, Voron's electrical page sets the floor: *"Use at least 18 AWG (0.75 mm²) for mains AC wiring, even better would be 16 AWG (1.25 mm²)."* Every mains conductor in this kit arrives pre-made; the number matters if you ever lengthen or replace one.

**Check:** Ferrules found in the kit before Ch 10 starts (Ch 09's hardware table counts five). You know which terminals get a ferrule and which get bare stranded core, and you know the pull-and-look test.

Source: [Voron docs — Electrical Wiring](https://docs.vorondesign.com/build/electrical/) · [Ch 09 — Hardware](09-electronics-bay.md) · [Ch 10 Step 10.8](10-wiring.md#step-108-inlet-wago-bus), [Step 10.9](10-wiring.md#step-109-wago-bus-psu)

---

### Step 00a.9 — Strain relief: nothing may pull on a terminal

(no image — see text)

**What you're looking at:** No parts — a routing rule. Everything here is about keeping load off a termination: the wire ducts that carry the mains run below deck, the anchor at the deck opening, and the zip ties at both ends of every drag chain, so it is the duct or the chain that takes the pull, not the screw terminal at the end of the wire.

**Parts:** none.

**Do:** A terminal is a connection, not an anchor. RepRap's rule is the one to hold: *"all wires ends of moving wires and static power wires shall be secured just aside the connection, in order to release any load on connexion."* In this build that means the mains run goes **inside a wire duct**, not across open deck ([10.8](10-wiring.md#step-108-inlet-wago-bus)), the deck opening is strain-relieved ([10.69](10-wiring.md#step-1069-strain-relieve-the-deck-opening)), and every drag chain is zip-tied at both ends so the chain — not the connector — takes the motion ([10.66](10-wiring.md#step-1066-zip-tie-both-ends-of-every-chain)). Ch 10's own warning is that cables pulled tight *"will survive assembly and fail in three months"*.

The same page sets the end state for the whole electronics bay: *"All connections of mains (110/230V) shall be physically protected and you shall not be capable to access them even if you try."* That is what the bottom panel, the skirts and the duct covers in **Ch 11** are for. Closing the machine is a safety step, not a cosmetic one — which is exactly why Ch 11 is not allowed to start until Checkpoint #1 has passed.

**Check:** You can name the three places this manual anchors a cable near its termination, and you understand that Ch 11 is the step that makes the mains inaccessible.

Source: [RepRap — Safety](https://reprap.org/wiki/Safety) · [Ch 10 Step 10.69](10-wiring.md#step-1069-strain-relieve-the-deck-opening) · [Ch 11 — Read first](11-skirts-panels-door.md)

---

### Step 00a.10 — The fuse in the inlet, and what it does not protect

(no image — see [LDO inlet layout diagram](https://docs.ldomotors.com/v01_wire_guide/inlet_layout.png))

**What you're looking at:** LDO's diagram of the combined AC inlet — one moulded body carrying the C14 socket where the cord plugs in, the illuminated double-pole rocker switch, and a pull-out fuse drawer. **C14** is the male inlet on the machine and **C13** the socket on the cord ([glossary](16-glossary.md#i)). The three properties below — fuse on live only, rocker on both poles, earth straight through — are what Step 10.5 proves with the meter.

**Parts:** none.

**Do:** The kit's AC inlet is a **single module** — C14 socket, illuminated rocker switch and fuse drawer in one body — not the official manual's separate filtered inlet plus rocker ([09.11](09-electronics-bay.md#step-0911-fit-the-combined-iec-inlet-module), [10.4](10-wiring.md#step-104-fit-the-ac-inlet-into-the-printed-plug-panel)). Learn its three properties now, because [Step 10.5](10-wiring.md#step-105-verify-the-pre-wired-inlet-before-you-trust-it) asks you to prove all three with the meter:

- **The fuse is in series with Live only.** Pull it and the L path opens even with the rocker on.
- **The rocker switches both L and N.** RepRap's requirement — *"You always shall be capable to unpower totally the printer, so the printer power switch shall be on the mains"* — is met by this module, and only because both poles are switched.
- **The Earth spade is neither switched nor fused.** It goes straight through. That is correct and it is what makes PE a protective conductor rather than a circuit.

What the fuse is for: Omron's datasheet for your SSR says *"The G3NB may rupture if a short-circuit is applied to it. To protect against short-circuit accidents, install a protective device, such as a quick-burning fuse, on the power supply line."* The inlet fuse is that device. What it is **not** for: it does not protect a person. A fault current small enough to kill will not blow a mains fuse — that is the RCD's job ([00a.5](#step-00a5-put-the-printer-on-an-rcdgfci-outlet-you-can-reach)) and the PE chain's ([00a.6](#step-00a6-learn-the-protective-earth-chain-in-this-build)). Keep the fuse at the rating supplied and never fit a larger one to stop nuisance blowing; a fuse that keeps blowing is reporting a fault.

**Check:** You can find the fuse drawer with the machine upright, and the rating printed on the fuse or its holder is written in the build log **(verify on bench — LDO does not publish the value)**.

Source: [Omron — G3NB datasheet (J164-E1)](https://www.omron-ap.com/data_pdf/cat/g3nb-1_j164-e1_4_3_csm1013815.pdf) · [RepRap — Safety](https://reprap.org/wiki/Safety) · [LDO wiring guide § Preparing the inlet](https://docs.ldomotors.com/en/voron/voron2/wiring_guide_rev_d#preparing-the-inlet)

---

## The two rituals, and the bad day

### Step 00a.11 — Know the two power-on rituals before either one arrives

(no image — see text)

**What you're looking at:** No parts — two scripted sequences, read now so neither is improvised. Checkpoint #1 is a set of meter measurements on a completely unplugged machine followed by one deliberate plug-in; the first real power-on in Ch 13 is a ten-second hand-on-the-switch listen with the chamber cleared.

**Parts:** none.

**Do:** This machine is deliberately powered on only three times before it is closed, and two of those are scripted rituals. Read both now so neither is improvised.

**Ritual 1 — Checkpoint #1, [Ch 10 Steps 10.17](10-wiring.md#step-1017-de-energise-and-set-up)–[10.23](10-wiring.md#step-1023-first-power-on-then-off-again).** Meter first, cord out of the room: colour groups shorted, L / N / PE mutually isolated, the switch actually switching, the SSR open when unpowered, the voltage selector re-read. Only then one deliberate plug-in — cord to inlet, then to wall, then rocker — hands clear of the terminal block, looking for the rocker to illuminate, the PSU LED to light green, **24 V ± 0.5 V** on the meter, and no noise or smell. Then off, unplug, and the cord goes back out of the room. LDO's framing of the whole section: *"Incorrect wiring of AC/mains can be dangerous — therefore, always double check your work, and then triple check it once more."*

**Ritual 2 — first real power-on, [Ch 13 Step 13.3](13-initial-startup.md#step-133-first-power-on-hand-on-the-switch).** [Step 13.1](13-initial-startup.md#step-131-clear-the-machine-and-stage-the-bench) clears the chamber and puts a fire extinguisher within arm's reach. Then: stand to the **side** of the machine, hand on the inlet rocker, switch on, and keep your hand there for a full ten seconds while you listen and smell. Anything wrong — switch off immediately.

The third powered moment is [Step 12.11](12-software.md#step-1211-gate-power-the-bay-and-confirm-both-mcus-enumerate), the firmware gate. Between Checkpoint #1 and Ch 11 the bay is open **by design** — [Step 10.71](10-wiring.md#step-1071-leave-the-duct-covers-off) leaves the duct covers off on purpose. So the rule is: the machine is energised with the bay open **only** at those three steps, and only with hands out of the bay. If you want to look at something, power off, look, power on. Voron's page states the general form: *"Never plug or unplug any device while the printer is powered"*, and *"Always double check to make sure your printer is unplugged and the capacitors in the power supplies have discharged before touching any wire or terminal"* — which is what [Step 10.73](10-wiring.md#step-1073-confirm-dead) measures, 0 V held for ten seconds.

**Check:** You can recite both rituals in order, and you know the three step numbers at which this machine is allowed to be live with the bay open.

Source: [LDO wiring guide § Checkpoint 1](https://docs.ldomotors.com/en/voron/voron2/wiring_guide_rev_d#checkpoint-1) · [Voron docs — Electrical Wiring](https://docs.vorondesign.com/build/electrical/) · [Ch 13 Step 13.3](13-initial-startup.md#step-133-first-power-on-hand-on-the-switch)

---

### Step 00a.12 — Decide now what you do when it smokes, trips or bites

(no image — see text)

**What you're looking at:** No parts — five agreed responses. Each row's *Do this first* is the action that removes energy from the machine; the *Then* column points at the existing step that owns the diagnosis, so nothing here is improvised in the moment.

**Parts:** none.

**Do:** Agree these five responses before you need one. Every fix below is the branch an existing step already owns; none of them is improvised here.

| What happens | Do this first | Then |
|---|---|---|
| Breaker or RCD trips the moment you switch on | Switch off at the **wall**, unplug, leave it off | RCD tripping is an L-or-N-to-earth fault; a breaker is L-to-N. Redo [10.18](10-wiring.md#step-1018-colour-groups-are-shorted)–[10.19](10-wiring.md#step-1019-l-n-and-pe-are-isolated-from-each-other) |
| Smoke, a hot smell, buzzing or click-cycling | Switch off at the **wall**, not the rocker, and unplug | Do not open the bay until [10.73](10-wiring.md#step-1073-confirm-dead) reads 0 V held ten seconds. Suspect a strand outside a terminal, or the PSU selector ([10.2](10-wiring.md#step-102-set-the-psu-input-voltage-selector), [10.22](10-wiring.md#step-1022-re-check-the-voltage-selector)) |
| A temperature climbs with nothing commanded | Cut power at the switch | Ch 13's what-if table calls this a heater energised through a wiring fault — back to Ch 10, do not *"just watch it"* |
| SSR reads short **LOAD 1 → LOAD 2** unpowered | Do not energise the machine | A solid-state relay that reads short is dead and the bed would be permanently live. Replace it ([10.21](10-wiring.md#step-1021-the-ssr-is-open-when-unpowered), [10.78](10-wiring.md#step-1078-ssr-polarity-and-isolation-one-last-time)) |
| Someone is shocked or stuck to the machine | **Do not touch them.** Kill the circuit at the breaker you labelled in [00a.5](#step-00a5-put-the-printer-on-an-rcdgfci-outlet-you-can-reach) | Then emergency services. Any shock, however small, ends the session — the machine stays unplugged until the PE sweep at [10.77](10-wiring.md#step-1077-protective-earth-bonding) has been redone |

Two standing rules on top of the table. **Never re-energise a circuit that tripped without finding out why** — a second trip is not new information and it is not a test. And keep the extinguisher from [Step 13.1](13-initial-startup.md#step-131-clear-the-machine-and-stage-the-bench) permanently by the machine, not just on startup day: RepRap's position on unattended printing is that *"No printer shall remain unattended"*, and this one runs multi-hour ASA prints in a hot chamber. No Voron or LDO source specifies an extinguisher class — buy one rated for electrical fires and read its label once **(verify on bench)**.

**Check:** All five responses agreed out loud with whoever else is in the house, the breaker is labelled, and the extinguisher is in reach of the machine rather than in a cupboard.

Source: [RepRap — Safety](https://reprap.org/wiki/Safety) · [Ch 13 — What if](13-initial-startup.md#what-if-first-start-failures-and-what-they-actually-mean) · [Ch 10 Steps 10.19](10-wiring.md#step-1019-l-n-and-pe-are-isolated-from-each-other), [10.21](10-wiring.md#step-1021-the-ssr-is-open-when-unpowered), [10.73](10-wiring.md#step-1073-confirm-dead)

---

Pause: ~25 min since the last pause — the chapter is read and nothing is half-done, because nothing was started. The only durable outputs are the posted room rule, the labelled breaker, a tested meter and five agreed responses. Do not carry on into Ch 09 in the same session if you are tired; Ch 09 ends with the machine on its back and the bay open.

---

## Checkpoint 00a

Do not open Ch 09 until every line is ticked.

- [ ] Decided and written down who lands the mains conductors in Ch 10 Section 1, and whether that is a certified person.
- [ ] The "who is in the room" rule is written and posted, naming Ch 10 Steps 10.1–10.16, Steps 10.17–10.23, and Ch 13 Step 13.3.
- [ ] Multimeter on the bench with a printed CAT rating (CAT III 600 V or better), matching leads, continuity, Ω, DC V and AC V all found.
- [ ] Meter proved live–dead–live once, probes shorted to a beep, both leads continuous, battery good.
- [ ] Printer's outlet is RCD/GFCI protected, trips on its TEST button, and its breaker is identified and labelled.
- [ ] The five PE branches can be named from memory, and the M4×6 bed PE screw was confirmed present at Ch 03 Step 03.6.
- [ ] The SSR "earth the mounting rail" gap is understood and, if local rules require an earthed rail, it has been raised with whoever signs off the mains work.
- [ ] VE0508 ferrules located in the kit; the pull-and-look test at Ch 10 Step 10.8 is understood.
- [ ] Both power-on rituals read end to end, and the three steps where the machine may be live with the bay open are known.
- [ ] The five failure responses are agreed out loud; extinguisher in reach; nobody re-energises a tripped circuit without a cause.

## Common mistakes

- **Reading this chapter after Ch 09.** By then the inlet, PSU and SSR are already mounted and the only decisions left are the ones you should have made first. Ch 09 is where the mains parts enter the machine; Ch 10 is only where they get connected.
- **Buying a meter on price and range instead of on category.** Display range tells you what it can show; the CAT rating tells you what it can survive. An unrated meter on a receptacle circuit is the wrong tool, not a cheap one.
- **Trusting a "no voltage" reading from a meter you have not just proved.** A flat battery, a broken lead or a blown internal fuse all read as *dead*. Live–dead–live costs fifteen seconds.
- **Treating the frame PE bond as automatic.** Anodising is an insulator. Ch 10 Step 10.16 says to scrape it under the washer for a reason, and the same logic is why the DIN rail's incidental bond is not a substitute for an earthed rail.
- **Enlarging the inlet fuse because it blew.** The fuse is reporting a short. Fitting a bigger one removes the report and leaves the short.
- **Letting the "who is in the room" rule become implicit.** An unwritten rule gets bent at 22:00 by whoever is holding the camera. Write it, post it, say it once.

## Next

[**Ch 09 — Electronics bay**](09-electronics-bay.md): mount the DIN rails, ducts, PSU, SSR, Leviathan, Pi and mains inlet — everything placed, nothing wired. Then [Ch 10](10-wiring.md), where the decisions above get spent.
