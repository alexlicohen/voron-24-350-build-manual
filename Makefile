# One green gate. Mirrors the build-and-lint job of .github/workflows/check.yml; its plates job
# is `make audit-plates` (CI: --no-brim, the STLs are not in git) and `make test-arrange`.
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

# Plate tooling runs on the interpreter that packs plates (numpy: requirements-arrange.txt,
# pytest for the arranger's tests), not on the docs venv, which has neither.
PLATE_PY ?= python3

# Every committed plate 3MF against the edge, gap and brim rules (plates.AS_PRINTED exempt).
.PHONY: audit-plates
audit-plates:
	$(PLATE_PY) slicer/audit_plates.py

# tools/platearrange's own tests, and the arranger at this build's settings.
.PHONY: test-arrange
test-arrange:
	cd tools/platearrange && $(PLATE_PY) -m pytest -q
