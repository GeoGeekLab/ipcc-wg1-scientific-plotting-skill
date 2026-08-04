"""Small, dependency-light helpers for reproducible scientific figures."""

from .provenance import build_provenance, sha256_file, write_provenance
from .recipe import FigureRecipe, load_recipe
from .style import publication_context, register_rgb_colormap, save_figure
from .uncertainty import ensemble_summary, fdr_bh_mask

__all__ = [
    "FigureRecipe",
    "build_provenance",
    "ensemble_summary",
    "fdr_bh_mask",
    "load_recipe",
    "publication_context",
    "register_rgb_colormap",
    "save_figure",
    "sha256_file",
    "write_provenance",
]
