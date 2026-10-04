# One green gate. Mirrors .github/workflows/check.yml, plus slicer/check_docs.py (local only).
# The build regenerates the tracked docs/assets/tonight.json; commit it if it changes.
VENV ?= .venv/bin
PY := $(VENV)/python

.PHONY: verify
verify:
	$(VENV)/mkdocs build --strict
	$(PY) scripts/build_tonight.py --self-test
	node scripts/check_tonight.mjs
	$(PY) hooks/callouts.py
	$(PY) scripts/lint_manual.py
	$(PY) slicer/check_docs.py
