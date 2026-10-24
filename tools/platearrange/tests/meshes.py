"""Closed test meshes built from axis-aligned boxes."""
import numpy as np

_FACES = [(0, 2, 1), (0, 3, 2), (4, 5, 6), (4, 6, 7), (0, 1, 5), (0, 5, 4),
          (1, 2, 6), (1, 6, 5), (2, 3, 7), (2, 7, 6), (3, 0, 4), (3, 4, 7)]


def boxes(*specs):
    """Union of boxes (x0, y0, x1, y1[, z0, z1]) as one mesh: (vertices, triangles)."""
    vs, ts = [], []
    for s in specs:
        x0, y0, x1, y1 = s[:4]
        z0, z1 = (s[4], s[5]) if len(s) > 4 else (0.0, 10.0)
        base = len(vs)
        vs += [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
               (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
        ts += [(a + base, b + base, c + base) for a, b, c in _FACES]
    return np.array(vs, dtype=float), np.array(ts, dtype=int)


def box(w, h, x0=0.0, y0=0.0, z=10.0):
    return boxes((x0, y0, x0 + w, y0 + h, 0.0, z))


def ell(w=80, h=80, t=20):
    return boxes((0, 0, w, t), (0, 0, t, h))


def cee(w=100, h=100, t=20):
    """C open to +x: left bar, bottom bar, top bar."""
    return boxes((0, 0, t, h), (0, 0, w, t), (0, h - t, w, h))
