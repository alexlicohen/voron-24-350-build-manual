#!/usr/bin/env python3
"""Print the bench-photo checklist: every step whose image line is still
`(no image — see text)`, plus the ten specific shots Ch 00 Step 00.30 asks
for (which aren't tied to a single step heading).

Not wired as an mkdocs hook — it's a checklist for Alex to carry, not build
output. Run manually and read it, or redirect it into
docs/manual/assets/photos/WANTED.md:

    python3 scripts/photo_wanted.py > docs/manual/assets/photos/WANTED.md
"""

import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
MANUAL = REPO / "docs" / "manual"
_EXCLUDED = {"00-index.md", "00-tonight.md", "CONVENTIONS.md"}

STEP_HEADING_RE = re.compile(r"^###\s*Step\s+([A-Za-z]?\d+\.\d+)\s*—\s*(.+?)\s*$")
NO_IMAGE_RE = re.compile(r"^\s*\*?\(no image[^)]*\)\*?\s*$", re.IGNORECASE)

STEP_00_30_SHOTS = [
    "Every LDO deviation next to the part it replaces (precision spacer beside a shim, "
    "the second-hole rail mounting, the M3×20 bed screw, the deck support you chose next "
    "to the caliper reading)",
    "Nitehawk-SB V2 both faces with PH2.0 connectors seated",
    "The V2 fan-adapter header mated in its keyed orientation",
    "The USB-adapter grounding wire as installed",
    "Titanium backers on both axes before the XY joints are torqued",
    "The electronics bay at each checkpoint",
    "The gantry-squaring setup",
    "The belt-tension measurement with the 150 mm span marked and the phone showing the peak",
    "The good and bad heat-set inserts on the practice coupon",
    "The finished cable runs before the ducts are covered",
]


def chapter_files():
    files = list(MANUAL.glob("*.md")) + list((MANUAL / "print").glob("*.md"))
    return sorted(f for f in files if f.name not in _EXCLUDED)


def find_missing_steps():
    missing = []
    for f in chapter_files():
        lines = f.read_text(encoding="utf-8").splitlines()
        step_id = step_title = None
        for line in lines:
            m = STEP_HEADING_RE.match(line)
            if m:
                step_id, step_title = m.group(1), m.group(2)
                continue
            if step_id and line.strip() == "":
                continue
            if step_id and NO_IMAGE_RE.match(line):
                missing.append((f.relative_to(MANUAL), step_id, step_title))
                step_id = None  # only the first content line after a heading counts
            elif step_id:
                step_id = None  # this step already has a real image line
    return missing


def render(missing):
    out = ["# Bench photos wanted", ""]
    out.append(
        f"_{len(missing)} step(s) marked `(no image — see text)`, plus the ten shots "
        "Ch 00 Step 00.30 calls for. File each with `scripts/ingest_photos.py`._"
    )
    out.append("")
    out.append("## Steps with no image")
    out.append("")
    for rel, step_id, title in missing:
        out.append(f"- [ ] Step {step_id} — {title} (`{rel}`)")
    out.append("")
    out.append("## Ch 00 Step 00.30 — the ten shots no published source has")
    out.append("")
    for shot in STEP_00_30_SHOTS:
        out.append(f"- [ ] {shot}")
    out.append("")
    return "\n".join(out)


def main():
    missing = find_missing_steps()
    print(render(missing))
    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())
