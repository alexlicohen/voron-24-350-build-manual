"""platearrange: centre-packing 2D arranger for FDM build plates (PrusaSlicer projects).

    from platearrange import Item, arrange
    placements = arrange(items, bed=(250, 220), gap=6.0, rot_step=5.0)
"""
from .core import (NoFit, Item, Placement, Result, arrange, arrange_detailed,  # noqa: F401
                      clear_cache)
from .io3mf import Project, ProjectItem, read_3mf, write_3mf  # noqa: F401

__version__ = "0.1.0"
