# Contributing

This is a build manual for one specific kit (LDO Voron 2.4 R2, Rev D+, 350 mm). If your kit differs, corrections are the most valuable thing you can contribute.

## Reporting a correction or a question

Use the issue templates: **Correction** (the manual says one thing, your kit or an updated source says another — needs a chapter/step, what the doc says, what you found, and your kit revision/batch) or **Question** (something about how the manual itself is written). General Voron/LDO build help belongs in the [Voron Discord](https://discord.gg/voron), not here.

## Running the site locally

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
./scripts/serve.sh        # prints the LAN URL
```

Before opening a PR:

```bash
mkdocs build --strict
python3 scripts/lint_manual.py
```

## Conventions

Chapter and print-batch format (header block, `### Step NN.M`, Parts / Do / Check, `⚠ Rev D+ / LDO:` callouts, Checkpoint, Common mistakes) is fixed by [`docs/manual/CONVENTIONS.md`](docs/manual/CONVENTIONS.md) — follow it exactly.

## How a correction flows through the manual

A factual change goes in **three** places, per `docs/manual/00-index.md`'s "How to update this manual": the corrections-log row, an inline `⚠ Rev D+ / LDO:` callout at the affected step, and (if the fact was sourced from them) `docs/voron-print-plan.md` or `docs/voron-build-instructions-survey.md` first. Cite what backs the change with a `Source:` line, and add its URL to [`sources.yml`](sources.yml) if it isn't already tracked (`python3 scripts/sources_build.py` regenerates the inventory; don't hand-edit URLs there without also fixing the citing chapter).
