"""High-fidelity helpers distilled from IPCC AR6 WGI visual practice."""

from .colormaps import load_ipcc_colormap, official_colormap_root
from .fidelity import audit_figure
from .provenance import build_provenance, sha256_file, write_provenance
from .recipe import FigureRecipe, load_recipe
from .style import (
    audit_text_conventions,
    axis_label,
    ipcc_legend,
    panel_label,
    publication_context,
    require_arial,
    save_figure,
)
from .tokens import (
    AR6_REPORT_RCP,
    AR6_REPORT_SSP,
    GENERIC_LINE_COLORS,
    GENERIC_SHADE_COLORS,
    WGI_GUIDE_2022_SSP,
    scenario_style,
)
from .uncertainty import ensemble_summary, fdr_bh_mask

__all__ = [
    "AR6_REPORT_RCP",
    "AR6_REPORT_SSP",
    "FigureRecipe",
    "GENERIC_LINE_COLORS",
    "GENERIC_SHADE_COLORS",
    "WGI_GUIDE_2022_SSP",
    "audit_figure",
    "audit_text_conventions",
    "axis_label",
    "build_provenance",
    "ensemble_summary",
    "fdr_bh_mask",
    "ipcc_legend",
    "load_ipcc_colormap",
    "load_recipe",
    "official_colormap_root",
    "panel_label",
    "publication_context",
    "require_arial",
    "save_figure",
    "scenario_style",
    "sha256_file",
    "write_provenance",
]
