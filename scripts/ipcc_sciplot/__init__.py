"""Reusable helpers for reproducible IPCC-native climate-assessment figures."""

from .maps import (
    add_insufficient_data_mask,
    add_low_agreement_hatching,
    add_mask_hatching,
    classify_robustness,
    cosine_latitude_weights,
    weighted_spatial_mean,
)
from .provenance import build_provenance, sha256_file, write_provenance
from .recipe import (
    FigureRecipe,
    IPCCNativeRecipe,
    load_any_recipe,
    load_ipcc_native_recipe,
    load_recipe,
)
from .scenarios import (
    canonical_scenario_label,
    canonical_scenario_order,
    known_ssp_labels,
    validate_scenario_order,
)
from .style import (
    add_panel_label,
    assessment_context,
    make_norm,
    publication_context,
    register_rgb_colormap,
    save_figure,
)
from .uncertainty import ensemble_summary, fdr_bh_mask
from .validation import (
    ClimateDataReport,
    infer_longitude_convention,
    inspect_climate_data,
    normalize_longitude,
    require_climate_ready,
)

__all__ = [
    "ClimateDataReport",
    "FigureRecipe",
    "IPCCNativeRecipe",
    "add_insufficient_data_mask",
    "add_low_agreement_hatching",
    "add_mask_hatching",
    "add_panel_label",
    "assessment_context",
    "build_provenance",
    "canonical_scenario_label",
    "canonical_scenario_order",
    "classify_robustness",
    "cosine_latitude_weights",
    "ensemble_summary",
    "fdr_bh_mask",
    "infer_longitude_convention",
    "inspect_climate_data",
    "known_ssp_labels",
    "load_any_recipe",
    "load_ipcc_native_recipe",
    "load_recipe",
    "make_norm",
    "normalize_longitude",
    "publication_context",
    "register_rgb_colormap",
    "require_climate_ready",
    "save_figure",
    "sha256_file",
    "validate_scenario_order",
    "weighted_spatial_mean",
    "write_provenance",
]
