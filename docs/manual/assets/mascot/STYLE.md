# Mascot — construction and style

*Voron* is Russian for raven, so the manual's mascot is a raven (*Corvus corax*), drawn from real
bird anatomy rather than from a circle-and-oval cartoon. Twenty files in **three views**, generated
by `scripts/gen_mascot.py` — edit the script, not the SVGs.

| View | When | Constructions |
|---|---|---|
| **Profile** | the bird is looking at something; the page is about that thing | `bird()` |
| **Three-quarter** | the bird is *doing* something and wants you to see it | `bird_3q()` |
| **Front** | the bird is addressing the reader directly | `bird_front()` |

All three share the palette, the halo pass, the feather-row helper, the friendly expression
(`eyelid` / gape hook / cheek catch), the `.m-*` animation classes and the reduced-motion gate.
`spread_wing` works in every view; a fan seen from the front is just a mirrored pair.

## Construction

The bird is built from feather **rows**, not blobs. `row(n, base0, base1, angle0, angle1, len0,
len1, w0, w1)` shingles `n` lanceolate feathers along a baseline, interpolating direction and
length; every plumage group in every pose comes out of that one call.

| Group | What it is | Note |
|---|---|---|
| Skull | rounded wedge, flat crown, x 300–398 | crown sheen runs crown → nape |
| Bill | heavy, hooked at the tip, as long as the skull | upper mandible `K1`, lower `K0`, gape line between |
| Nasal bristles | six tapers over the base of the culmen | the detail that says raven and not crow |
| Throat hackles | five pointed feathers that **project past** the throat line | the front silhouette is serrated, never smooth |
| Folded wing | envelope filled `K0`, then five rows: primaries → secondaries → greater → median → lesser coverts | sheen rides the median and lesser coverts only |
| Spread wing | a fan, not the folded wing rotated — see below | one construction, every extended-wing pose |
| Tail | five rectrices, alternating tones, graduated | wedge tail, longest feathers central |
| Legs | tarsus with four scale bands, three toes forward + hallux, claws | far leg `K0`, near leg `K1` |
| Breast | two faint scallop rows at 0.2 opacity | texture, never a bib |

### Plumage detail

Detail is spent where it survives 256 px, and nowhere else:

- **`long_feather()`** draws a flight feather or rectrix, then `plume()` adds a **rachis** line and
  **three barb strokes** on the wide side. A few strokes, never a hatch — a hatch turns to noise at
  256 px. Primaries and rectrices get three barbs, secondaries two.
- **`shingle()`** draws a covert row twice: the full shape in a lighter rim tone, then an inner copy
  at 0.84 scale in the base tone. The pale fringe that leaves is what makes a covert row read as
  feathers instead of scales.
- **`jitter(i)`** wobbles ruff and hackle lengths deterministically. A smooth length interpolation
  gives a row of lozenges; the wobble gives a shaggy mass.
- **Eye** carries a thin pale ring (`#5A6780` at 0.55) outside the disc, inside the socket.
- **Feet** are three toes plus the hallux in every view, each with three scute bands and a claw. The
  three-quarter near foot has its toes separated rather than fanned as one mass.

### Juvenile

`bird_3q(juv=True)` is the fledgling, used by `helper`:

| | Adult | Fledgling |
|---|---|---|
| Head | scale 1.0 | **1.16** about the neck pivot, halo included |
| Bill | `BILL_3Q`, hooked | `BILL_3Q_JUV`, stubby, no hook |
| Gape | closed, hooked up at the hinge | **slightly open**, with a pale `#6B7689` flange |
| Eye | r 19 / 11 | **×1.2** — larger relative to the head |
| Ruff | pointed, jitter 0.24 | **×1.22, blunter**, fluffier |
| Tail | `TAIL_3Q` | `TAIL_3Q_JUV`, shorter |
| Legs | full tarsus | stubbier, shorter toes |

Feather rows must **tile**, not stack: a row whose bases sit closer together than its feather width
collapses into one smooth mass. The hackles use alternating lengths for the same reason — a smooth
length lerp gives a teardrop, not a fringe.

### The three-quarter view

`bird_3q()`. The body is angled toward the reader and the **head is turned further than the body**,
so both eyes read:

- **Near eye** r 19 at (300, 142), full, with the catchlight. **Far eye** r 11 at (222, 148), near
  the head's edge, with the base of the bill across its lower corner. Equal-sized eyes read as an
  owl, not a turned head — the size difference is what sells the turn.
- **Bill** foreshortened to ~0.8 of the profile length and given a **culmen ridge** line with a lit
  far facet on one side of it. The ridge is the single strongest cue that the head is turned.
- **Wings** are seen near edge-on, so they are a dark mass: primaries at the tip and a short covert
  patch at the shoulder. The full profile rows compress into vertical stripes in this view and read
  as suspenders — that was the first thing to go wrong.
- **Ruff** of five long hackle points across the throat in `#3B465C` / `K2`, much shaggier than the
  profile's serration, because in this view the throat faces the reader.
- Head and shoulders **merge** — no neck pinch. A pinch makes a ball-headed penguin.

### The front view

`bird_front()`. **Not quite symmetric** — about ten degrees of yaw toward the reader's right, so the
bird stops being a blob while still reading as facing you. The far (right) side of the face is
compressed, the far eye is r 17 against the near eye's r 20, the bill and its ridge sit ~7 units
right of centre, and the bird's left shoulder is marginally forward. `warn` keeps symmetric shoulder
origins and equal spans so its spread wings still read as a stop sign.

- **Bill** is the identity here and is drawn large — a wedge from y 142 to 254 with a vertical
  culmen ridge, one darker facet, and a hooked tip. A small front bill reads as a chick.
- **Both eyes** r 19 at (206, 134) and (306, 134), each with its own lid.
- **Bristles** as a tuft spraying down both sides from the top of the bill.
- **Gape** is two short lines under the bill whose outer ends rise — the smile, mirrored.
- **Folded wings** hang at the flanks with the **primaries crossing low over the tail**, which is
  what a perched corvid looks like head-on.
- **Feet** splayed, three toes each, short because they are foreshortened.
- Idle head motion is a slow **sway** (`mascot-sway`, ±1.8°) rather than the profile's look.

### One wing per side — the wing state

Each view's constructor takes a **per-side wing state**, and draws that side either folded or
spread, never both:

```python
bird(near=SP(24, 146), far=FOLDED)          # profile:  near/far
bird_3q(near=SP(-52, 150), far=FOLDED)      # 3Q:       near/far
bird_front(left=SP(186, 172), right=SP(-6, 172))   # front: left/right
```

`FOLDED` draws that side's folded wing, `SP(angle, span, droop, origin)` draws a spread one from the
same shoulder, and `None` omits the side entirely. The halo pass switches with it, so a spread wing
takes its side's envelope out of the silhouette too.

**Why this exists.** The first version of the three-quarter and front views drew the folded wings
unconditionally and added the spread ones on top, so `pass`, `warn`, `fail`, `kitday` and every
action pose had *four* wings — a raised pair and a folded pair. Routing all of it through one
per-side state is what makes that unrepresentable.

The spread wing's shoulder matches the folded one's (profile (296, 232); 3Q (338, 218) / (198, 234);
front (192, 230) / (320, 230)) and its halo deliberately excludes the arm bar, so the limb reads as
the same wing moved rather than a second one stuck on.

In the **profile** view a folded `far` is only the sliver that clears the body — the envelope
redrawn behind the torso, offset up and back — never a second full wing. The strict-profile poses
(`base`, `pause`, `print`, `screen`) leave `far=None`: from the side the other wing is genuinely
hidden, and poking a sliver out would be wrong.

The tally's markers are **derived from the wing path constants**, not retyped: hand-copied prefixes
went stale the moment an envelope was re-drawn, and the guard silently passed a wingless front view.

`gen_mascot.py` **tallies the wings of every file it writes** and exits non-zero if a pose has more
than two, or has a spread wing without exactly two in total. `helper` (two birds) and `badge` (a
head crop) are the two declared exceptions.

### The spread wing

`spread_wing(angle, span, flip, origin, droop)` builds an **extended** wing, and every pose that
holds, raises or spreads a wing calls it. Rotating the folded wing was the earlier approach and it
read as a striped sleeve: covert stripes running along a constant-width tube.

- **Arm bar** from shoulder → elbow → wrist, tapering, at the leading edge.
- **Primaries** fan out of the *wrist* over ~75°, with the angular spacing wider than the feather
  width so the tips have **visible gaps**. The fan is what makes the wing broaden toward the tip.
- **Secondaries** fill the inner trailing edge between elbow and wrist, blunt-tipped, behind the
  primaries.
- **Coverts** are a short shingled band on the **leading edge only** — three rows, greater → median
  → lesser. The sheen rides the median and lesser band and nothing else.
- **Alula** at the wrist on the leading edge, a small `K3` lobe.
- `flip` puts the trailing edge on whichever side points downward; it is derived from the angle
  (`cos(angle) >= 0`) unless overridden. `droop` adds degrees to the primaries so the tips hang —
  that is what makes the `fail` shrug rueful.
- The fan's halo is the **thin** width (6) and covers primaries, secondaries and alula but **not**
  the arm bar: the bar has to merge into the shoulder, and a halo around it makes the wing look
  detached.
- `origin` moves the shoulder. `fail` uses it to set the far wing back and up so both wings read in
  a side profile, where a truly symmetric shrug would hide one behind the body.

`wing_tip(angle, span)` returns where the outermost primary lands, for hanging a prop on it.

### Expression

The bird is friendly, not stern. Four pieces, all in `head_art` / `eyelid`:

- **Gape** — the mouth line runs back along the jaw and **hooks up** at the hinge (`M326 202 … 392
  181`), so the bill reads as a slight smile rather than a straight slot.
- **Upper lid** — a shallow `K1` crescent crops the top ~20 % of the eye disc. Enough to soften the
  stare; any deeper and the bird looks sleepy. No rim line on it — a stroke there reads as a monocle.
- **Cheek catch** — a small `#3A4559` lozenge behind the gape at 0.5 opacity. Small: at illustration
  size a larger one reads as a bruise.
- **Head tilt** — `bird(tilt=N)` rotates the head N degrees bill-up about the neck pivot (300, 200),
  and rotates the head's **halo shapes with it** so the rim stays aligned. Positive is up.

| Tilt | Poses |
|---|---|
| +1 … +7 up | base, gather, check, print, screen, base-3q, pass, tip, helper, hexkey, caliper, point, carry, cable, badge |
| 0 | warn (serious), pause (asleep), the front view (no tilt hook — it sways instead) |
| −5 down | fail (rueful) |

### Halo

The bird has no dark outline. A `halo` pass draws the outer silhouette shapes (torso, skull, bill,
wing envelope, primaries, tail, hackle points, legs) filled and stroked in `#EDF0F4` **before** the
art, so the union reads as a pale rim on Material's slate (`#1e2129`). Stroke is 10.5 for the body,
6 for the legs — wider and the bird looks like a sticker, narrower and it vanishes on dark.

Only groups that move relative to the halo may rotate, and only by a degree or two, otherwise the
art slides off its own rim.

## Layers and their animation roles

Every animated group carries an invisible full-viewBox `<rect>` first. That fixes its `fill-box`
bounding box to the viewBox, which is what makes `transform-origin` px values mean user-space
coordinates. Remove the rect and the origin silently moves.

| Class | Holds | Idle motion |
|---|---|---|
| `.m-body` | everything | breathe, `scaleY` 1.013 over 4.2 s, origin at the feet |
| `.m-head` | skull, bill, bristles, eye | slow look, ±2.2° over 9 s |
| `.m-eye` | eye disc and highlights | blink, `scaleY` .08 for ~70 ms every 5.4 s |
| `.m-tail` | rectrices | tail-set, 1.4° over 11 s |
| `.m-wing` | folded wing rows | static when idle; the `.wave` one-shot rotates it |
| (spread wings) | `spread_wing` fans | static — they sit outside `.m-wing` so the fan never slides off its rim |
| `.m-leg-lift` | near leg, `pass` only | foot lift every 7.6 s |
| `.m-prop` | tray, magnifier, caliper, reprint arrow | per-pose bob / raise / turn |
| `.m-zz` | the three sleep marks | drift up and fade, 4.6 s |
| `.m-bulb` | the `tip` bulb | flicker |
| `.m-chick` | the fledgling | hop |
| `.m-layer` | the printer's first layer | `scaleX` .04 → 1 |
| `.m-tick`, `.m-flap` | PASS tick, carton flaps | pop, wobble |

All of it is inside `@media (prefers-reduced-motion: no-preference)`; with motion off every file is
static and complete. `.still` on the root kills animation regardless. `.wave` is a one-shot greeting
(wing + head) for a page that wants the bird to say hello on load.

**Never put an animated class and a `transform` attribute on the same element.** A CSS transform
animation overrides the attribute outright and the element jumps to the origin. `place()` exists to
keep positioning on an outer group and animation on an inner one.

## Palette

| Role | Hex | Used for |
|---|---|---|
| `K0` | `#0E1116` | primaries, lower mandible, far leg, deepest separations |
| `K1` | `#161A21` | body base, skull, near leg |
| `K2` | `#222A38` | mantle, greater coverts, hackles |
| `K3` | `#30394B` | nape, crown, median and lesser coverts, breast edge |
| Edge | `#2B3341` / `#3C465A` | feather separation strokes — the brighter one only in the dark tail/primary mass |
| Sheen | `#4C7FD3` → `#2A6FB5` | **the one permitted gradient**, id `sheen`, crown and wing coverts only |
| Halo | `#EDF0F4` | the silhouette rim, closed eyelid |
| Eye | `#0E1116` + `#FFFFFF` | dark eye, white highlight — the brightest thing in the file |
| Prop blue | `#2A6FB5` / `#DCE9F6` | spool band, lens, nightcap, printer window, bulb |
| Hardware | `#5C6675` / `#E7E9EC` / `#B6BDC6` | tray, caliper, carton, magnifier ring, bulb base |
| Feather rim | `#333D50` / `#46536C` | the lighter fringe on a covert, drawn by `shingle()` |
| Barb / rachis | `#3C465A` | `plume()` strokes on flight feathers, at 0.5 opacity |
| Gape flange | `#6B7689` | the fledgling's pale gape, nothing else |
| Amber | `#D98324` / `#FBEBD3` | hard hat and the reprint arrow. **Warn and fail only.** |
| Green | `#2E7D32` | the PASS tick, nothing else |

No other colour, no second gradient, no filters, no raster, no fonts, no scripts. Props carry
finish but stay flat: hex drives on the screw heads, a tick scale on the caliper beam, a bevel ring
and a knurled grip on the magnifier, and **brand-neutral** labels on the bin and carton — bars and
blocks, never lettering, since the files carry no fonts.

Per-file budget is **80 KB**; the set currently peaks at 56 KB (`helper`, which holds two birds).

## Sizing

| Size | Use | Rule |
|---|---|---|
| ≥ 160 px | page illustration | the detailed poses in all three views; feather rows and props resolve here |
| 40–48 px | inline badge | `mascot-badge.svg` **only** — head and shoulders, three hackle scallops, one big eye |

The detailed poses do not survive 48 px: the feather rows mush and the props become grey specks.
That is what the badge file is for. Keep the square viewBox; scale with `width`/`height`, never
crop, never re-colour with a CSS filter.

## Humour rule

Dry and kind, and rationed.

- **The bird never makes the mistake.** It watches, checks, shrugs alongside you, points at a
  lightbulb. It never breaks a part, never drops a screw, and is never the butt of the joke.
- **Never funny on `⚠`.** Mains, hot end, blade, magnets, anything that can hurt a person or scrap a
  part: the hard-hat pose only — no smile, no gag prop, no tilt. If a page's warning is serious
  enough to need the bird, the bird is serious too.
- **FAIL is sympathetic.** A shrug and a spool to print again. No tears, no facepalm, no red, no
  "oops". The gate failed, not the builder.
- **No speech.** No bubbles, no captions, no puns in `<title>`. The manual's words carry the
  meaning; the bird is punctuation.
- One mascot per page maximum, and no mascot at all on a page whose job is a number.

## File naming

`mascot-<pose>.svg`, lowercase, pose in one word. Previews are `preview/mascot-<pose>-light.png` and
`-dark.png` at 512 px, plus `preview/mascot-badge-48.png`. A new meaning is a new file — never
repurpose an existing pose, because the map below is how the next pass will place them.

---

## Where each pose belongs

A proposal for the next pass. Nothing in the manual references these files yet. `VIEW_OF` in the
generator is the authority on which view a pose is in, and it asserts against `POSES` at build time.

| File | View | The moment | Proposed placement |
|---|---|---|---|
| `mascot-base.svg` | profile | the manual itself | Home, beside the title |
| `mascot-badge.svg` | 3Q head | the manual speaking, inline | 48 px in the site header and beside field labels |
| `mascot-check.svg` | profile | verifying before moving on | the Check field's badge, and a chapter that ends in a measurement |
| `mascot-gather.svg` | profile | staging parts before a run of steps | the generated **Gather for this segment** block |
| `mascot-pause.svg` | profile | stopping for the night | `Pause:` boxes, the Tonight planner, overnight plates |
| `mascot-print.svg` | profile | watching a first layer | print-batch overview headers, slicer setup |
| `mascot-screen.svg` | profile | firmware and software | Ch 12 flashing, Ch 13 first startup |
| `mascot-base-3q.svg` | 3Q | the bird, turned to you | any page about the two of you rather than the machine |
| `mascot-pass.svg` | 3Q | a gate clears | the gate-calculator PASS verdict panel |
| `mascot-fail.svg` | 3Q | a gate does not clear | the same panel's FAIL state |
| `mascot-tip.svg` | 3Q | a shortcut worth knowing | `Tip:` boxes, one per chapter at most |
| `mascot-helper.svg` | 3Q | a step that wants two pairs of hands | the `**Helper:**` badge, the "With a helper" section |
| `mascot-hexkey.svg` | 3Q | tightening a fastener | Ch 01 squaring, and any step whose verb is *tighten* |
| `mascot-caliper.svg` | 3Q | reading a measurement | test cubes, belt spacing, gate numbers |
| `mascot-point.svg` | 3Q | "look at this one" | Do lines that single out a part, diagram callouts |
| `mascot-carry.svg` | 3Q | sorting | the bin-label page, per-chapter sorting diagrams |
| `mascot-cable.svg` | 3Q | low-voltage wiring | Ch 10. Signal connectors only |
| `mascot-base-front.svg` | front | the bird greeting you | Home; carries the `.wave` one-shot |
| `mascot-warn.svg` | front | safety, not caution | Ch 00a mains safety, and the one or two `⚠` boxes that can hurt someone |
| `mascot-kitday.svg` | front | the day a carton lands | Home's kit-day step, the B00 Gen-2-first note, Ch 00 unpacking |

**Deliberately absent.** There is no pose for mains, soldering iron, blade or hot chamber. Those
steps get no mascot at all — see the humour rule. `mascot-cable.svg` is low-voltage signal wiring
only: a connector and its tail, never a stripped conductor, never a mains lead.

**How to place them, when that pass happens.** Step pages under `docs/manual/steps/` are generated
by `scripts/build_steps.py`; never edit them. Art goes into the chapter markdown, or into the hook
that renders the block it belongs to (`hooks/callouts.py` for the callout badges,
`hooks/gatecalc.py` for the verdict panels) so every generated copy inherits it. Placement must not
touch step ids, and a mascot image line must stay outside the budgeted fields — it is not part of a
Do or Check run. Add one `.mascot` / `.mascot--badge` rule to `docs/stylesheets/extra.css` rather
than sizing each image inline.

Reference the SVG, not the preview PNG: CSS animations inside an SVG do run when it is loaded
through `<img>`, which is how a Markdown image line loads it.

## Regenerating

```sh
python3 scripts/gen_mascot.py docs/manual/assets/mascot --preview
```

Rewrites all twelve SVGs and re-renders the preview PNGs (512 px light and dark, plus the badge at
48 px) with `rsvg-convert`. `#1e2129` is Material's slate page colour. Check a new pose at 48 px on
both backgrounds before committing it; that is the size that fails first.
