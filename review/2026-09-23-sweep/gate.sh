#!/bin/bash
# Serialised gate: parallel workers share site/, so only one runs the gate at a time.
L=${TMPDIR:-/tmp}/voron-manual-gate.lock
until mkdir "$L" 2>/dev/null; do sleep 3; done
trap 'rmdir "$L"' EXIT
cd /Users/alex/projects/3d-printing
.venv/bin/mkdocs build --strict 2>&1 | grep -E 'WARNING|ERROR|built in' ; b=${PIPESTATUS[0]}
python3 scripts/lint_manual.py | tail -3; l=${PIPESTATUS[0]}
python3 slicer/check_docs.py | tail -2 | cut -c1-200; c=${PIPESTATUS[0]}
python3 hooks/mascot.py >/dev/null 2>&1; m=$?
echo "build=$b lint=$l check_docs=$c mascot=$m"
[ $b -eq 0 ] && [ $l -eq 0 ] && [ $c -eq 0 ] && [ $m -eq 0 ]
