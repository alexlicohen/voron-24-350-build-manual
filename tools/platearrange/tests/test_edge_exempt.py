"""The edge-rule exemption (slicer/plates.py EDGE_EXEMPT), through the two places that honour it:
slicer/audit_plates.py lists the break with its reason and fails nothing else, and
slicer/build_plates.platearrange_pack places an exempt plate with no edge margin.

Needs no PrusaSlicer and no fetched STLs: the audit reads the committed B12 projects with the brim
rule off (as CI does), and the packer test writes its own box STL.
"""
import struct
import sys
from pathlib import Path

import pytest

from meshes import box

SLICER = Path(__file__).resolve().parents[3] / "slicer"
sys.path.insert(0, str(SLICER))

import audit_plates  # noqa: E402
import build_plates  # noqa: E402
import plates  # noqa: E402
from geom import Piece, convex_hull  # noqa: E402


def test_only_b12_p1_is_edge_exempt_and_it_says_why():
    # B12 integration 2026-11-12: one plate, with its reason. A new entry needs his ruling; change this then.
    assert set(plates.EDGE_EXEMPT) == {"B12-P1"}
    assert "212" in plates.EDGE_EXEMPT["B12-P1"]
    assert not set(plates.EDGE_EXEMPT) & plates.AS_PRINTED


def test_audit_lists_the_exempt_edge_break_and_passes(capsys):
    assert audit_plates.run(["B12-P1"], brim=False) == 0
    out = capsys.readouterr().out
    assert "edge exempt" in out
    assert plates.EDGE_EXEMPT["B12-P1"] in out
    assert "(exempt) edge: side_spool_frame_puck.stl" in out


def test_audit_fails_the_same_plate_without_the_exemption(monkeypatch, capsys):
    monkeypatch.setattr(audit_plates, "EDGE_EXEMPT", {})
    assert audit_plates.run(["B12-P1"], brim=False) == 1
    assert "FAIL" in capsys.readouterr().out


def test_exemption_covers_the_edge_rule_only(monkeypatch, capsys):
    # B12-P2 passes every rule; exempt it from the edge rule and break its gap rule.
    monkeypatch.setattr(audit_plates, "EDGE_EXEMPT", {"B12-P2": "test"})
    monkeypatch.setattr(build_plates, "PA_GAP", 50.0)
    assert audit_plates.run(["B12-P2"], brim=False) == 1
    out = capsys.readouterr().out
    assert "FAIL" in out and "gap:" in out and "(exempt) gap:" not in out


def _write_stl(path: Path, v, t) -> None:
    out = bytearray(b"\0" * 80) + struct.pack("<I", len(t))
    for a, b, c in t:
        out += struct.pack("<12fH", 0.0, 0.0, 0.0, *v[a], *v[b], *v[c], 0)
    path.write_bytes(bytes(out))


def _frame_piece(tmp_path, monkeypatch) -> Piece:
    v, t = box(212.0, 212.0, z=21.5)            # the side spool frame's footprint
    _write_stl(tmp_path / "frame.stl", v, t)
    monkeypatch.setattr(build_plates, "STL", tmp_path)
    return Piece("frame.stl", "frame.stl", convex_hull([(x, y) for x, y, _z in v]), 3.0, 0.0)


def test_pack_refuses_the_frame_under_the_edge_rule(tmp_path, monkeypatch):
    fits, overflow = build_plates.platearrange_pack([_frame_piece(tmp_path, monkeypatch)],
                                                    build_plates.INI["black"])
    assert not fits and overflow


def test_pack_centres_the_frame_when_exempt(tmp_path, monkeypatch):
    p = _frame_piece(tmp_path, monkeypatch)
    fits, _ = build_plates.platearrange_pack([p], build_plates.INI["black"], edge_exempt=True)
    assert fits
    x0, y0, x1, y1 = p.extent()
    w, h = x1 - x0, y1 - y0
    cx, cy = p.x + w / 2, p.y + h / 2
    assert abs(cx - build_plates.BED_X / 2) < 1.0 and abs(cy - build_plates.BED_Y / 2) < 1.0
    reach = 3.0 + 0.3                             # brim + the ini's brim_separation
    assert p.y - reach >= -1e-6 and p.y + h + reach <= build_plates.BED_Y + 1e-6
