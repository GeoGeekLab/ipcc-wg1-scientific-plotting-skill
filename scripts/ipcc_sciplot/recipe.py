from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping

import yaml


@dataclass(frozen=True)
class FigureRecipe:
    """Legacy compact figure recipe retained for backward compatibility."""

    figure_id: str
    question: str
    estimand: str
    plot_type: str
    variable: str
    unit: str
    baseline: str | None = None
    center: str = "median"
    lower_quantile: float = 0.17
    upper_quantile: float = 0.83
    sign_agreement: float = 0.80
    min_valid_count: int = 5
    colormap: str = "RdBu_r"
    output_stem: str = "outputs/figure"
    extras: Mapping[str, Any] = field(default_factory=dict)

    def validate(self) -> None:
        if not self.figure_id.strip():
            raise ValueError("figure_id is required")
        if not self.question.strip() or not self.estimand.strip():
            raise ValueError("question and estimand are required")
        if not 0 <= self.lower_quantile < self.upper_quantile <= 1:
            raise ValueError("invalid quantile interval")
        if not 0.5 <= self.sign_agreement <= 1:
            raise ValueError("sign_agreement must be in [0.5, 1]")
        if self.min_valid_count < 1:
            raise ValueError("min_valid_count must be >= 1")


@dataclass(frozen=True)
class IPCCNativeRecipe:
    """Validated nested recipe for assessment-grade climate figures.

    The object deliberately keeps nested sections as mappings. Scientific projects
    often need project-specific keys; strict validation is applied to the core
    semantics while unknown fields remain available for provenance and extensions.
    """

    schema_version: str
    figure_id: str
    assessment: Mapping[str, Any]
    science: Mapping[str, Any]
    sources: Mapping[str, Any]
    temporal: Mapping[str, Any]
    spatial: Mapping[str, Any]
    ensemble: Mapping[str, Any]
    robustness: Mapping[str, Any]
    scenario: Mapping[str, Any]
    visual: Mapping[str, Any]
    caption: Mapping[str, Any]
    outputs: Mapping[str, Any]
    provenance: Mapping[str, Any]
    extras: Mapping[str, Any] = field(default_factory=dict)

    def validate(self) -> None:
        if not str(self.schema_version).strip():
            raise ValueError("schema_version is required")
        if not self.figure_id.strip():
            raise ValueError("figure_id is required")

        _require_text(self.assessment, "intent", "assessment")
        _require_text(self.assessment, "audience", "assessment")
        _require_text(self.assessment, "archetype", "assessment")
        _require_text(self.science, "question", "science")
        _require_text(self.science, "estimand", "science")
        _require_text(self.science, "variable", "science")
        _require_text(self.science, "unit", "science")

        audience = self.assessment.get("audience")
        allowed_audiences = {
            "chapter-author",
            "technical-summary",
            "policymaker",
            "public-assessment",
        }
        if audience not in allowed_audiences:
            raise ValueError(
                f"assessment.audience must be one of {sorted(allowed_audiences)}"
            )

        center = self.ensemble.get("center", "median")
        if center not in {"median", "mean"}:
            raise ValueError("ensemble.center must be 'median' or 'mean'")

        lower = _as_float(self.ensemble.get("lower_quantile", 0.17), "ensemble.lower_quantile")
        upper = _as_float(self.ensemble.get("upper_quantile", 0.83), "ensemble.upper_quantile")
        if not 0 <= lower < upper <= 1:
            raise ValueError("ensemble quantiles must satisfy 0 <= lower < upper <= 1")

        min_count = _as_int(self.ensemble.get("min_valid_count", 1), "ensemble.min_valid_count")
        if min_count < 1:
            raise ValueError("ensemble.min_valid_count must be >= 1")

        if bool(self.robustness.get("enabled", False)):
            method = str(self.robustness.get("method", "")).strip()
            if not method:
                raise ValueError("robustness.method is required when robustness is enabled")
            if method == "sign-agreement":
                threshold = _as_float(
                    self.robustness.get("sign_agreement_threshold", 0.80),
                    "robustness.sign_agreement_threshold",
                )
                if not 0.5 <= threshold <= 1:
                    raise ValueError(
                        "robustness.sign_agreement_threshold must be in [0.5, 1]"
                    )
                zero_tolerance = _as_float(
                    self.robustness.get("zero_tolerance", 0.0),
                    "robustness.zero_tolerance",
                )
                if zero_tolerance < 0:
                    raise ValueError("robustness.zero_tolerance must be non-negative")

        transformation = self.science.get("transformation")
        if transformation == "percent_change" and self.science.get("reference_value") is None:
            # Percent-change denominators normally live in baseline data, but a
            # missing reference-value field is a useful signal that the recipe
            # should explicitly document denominator handling.
            raise ValueError(
                "science.reference_value must document denominator/neutral handling for percent_change"
            )

        formats = self.outputs.get("formats", [])
        if not isinstance(formats, list) or not formats:
            raise ValueError("outputs.formats must be a non-empty list")
        unsupported = {str(x).lower() for x in formats} - {"pdf", "svg", "png", "tif", "tiff"}
        if unsupported:
            raise ValueError(f"unsupported output formats: {sorted(unsupported)}")

        normalization = self.visual.get("normalization", {})
        if isinstance(normalization, Mapping) and normalization.get("type") == "two-slope":
            vmin = _as_float(normalization.get("vmin"), "visual.normalization.vmin")
            vcenter = _as_float(normalization.get("vcenter"), "visual.normalization.vcenter")
            vmax = _as_float(normalization.get("vmax"), "visual.normalization.vmax")
            if not vmin < vcenter < vmax:
                raise ValueError("two-slope normalization requires vmin < vcenter < vmax")

        warming = self.temporal.get("warming_level", {})
        if isinstance(warming, Mapping) and bool(warming.get("enabled", False)):
            target = warming.get("target_degC")
            if target is None or _as_float(target, "temporal.warming_level.target_degC") <= 0:
                raise ValueError("enabled warming-level analysis requires positive target_degC")
            if not str(warming.get("reference_period", "")).strip():
                raise ValueError("warming-level analysis requires reference_period")

    @property
    def output_stem(self) -> str:
        return str(self.outputs.get("stem", "outputs/figure"))


def load_recipe(path: str | Path) -> FigureRecipe:
    """Load the legacy compact recipe."""

    payload = _read_yaml_mapping(path)
    known = {
        "figure_id",
        "question",
        "estimand",
        "plot_type",
        "variable",
        "unit",
        "baseline",
        "center",
        "lower_quantile",
        "upper_quantile",
        "sign_agreement",
        "min_valid_count",
        "colormap",
        "output_stem",
    }
    args = {k: payload[k] for k in known if k in payload}
    args["extras"] = {k: v for k, v in payload.items() if k not in known}
    recipe = FigureRecipe(**args)
    recipe.validate()
    return recipe


def load_ipcc_native_recipe(path: str | Path) -> IPCCNativeRecipe:
    """Load and validate a nested IPCC-native recipe."""

    payload = _read_yaml_mapping(path)
    required_sections = {
        "assessment",
        "science",
        "sources",
        "temporal",
        "spatial",
        "ensemble",
        "robustness",
        "scenario",
        "visual",
        "caption",
        "outputs",
        "provenance",
    }
    missing = sorted(required_sections - payload.keys())
    if missing:
        raise ValueError(f"IPCC-native recipe missing sections: {missing}")

    for section in required_sections:
        if not isinstance(payload[section], Mapping):
            raise ValueError(f"recipe section {section!r} must be a mapping")

    known = {"schema_version", "figure_id", *required_sections}
    recipe = IPCCNativeRecipe(
        schema_version=str(payload.get("schema_version", "1.0")),
        figure_id=str(payload.get("figure_id", "")),
        assessment=payload["assessment"],
        science=payload["science"],
        sources=payload["sources"],
        temporal=payload["temporal"],
        spatial=payload["spatial"],
        ensemble=payload["ensemble"],
        robustness=payload["robustness"],
        scenario=payload["scenario"],
        visual=payload["visual"],
        caption=payload["caption"],
        outputs=payload["outputs"],
        provenance=payload["provenance"],
        extras={k: v for k, v in payload.items() if k not in known},
    )
    recipe.validate()
    return recipe


def load_any_recipe(path: str | Path) -> FigureRecipe | IPCCNativeRecipe:
    """Auto-detect legacy versus IPCC-native recipe format."""

    payload = _read_yaml_mapping(path)
    if "assessment" in payload and "science" in payload:
        return load_ipcc_native_recipe(path)
    return load_recipe(path)


def _read_yaml_mapping(path: str | Path) -> dict[str, Any]:
    payload = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("recipe root must be a mapping")
    return payload


def _require_text(mapping: Mapping[str, Any], key: str, section: str) -> str:
    value = str(mapping.get(key, "")).strip()
    if not value:
        raise ValueError(f"{section}.{key} is required")
    return value


def _as_float(value: Any, name: str) -> float:
    if value is None:
        raise ValueError(f"{name} is required")
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be numeric") from exc


def _as_int(value: Any, name: str) -> int:
    if isinstance(value, bool):
        raise ValueError(f"{name} must be an integer")
    try:
        result = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be an integer") from exc
    if float(result) != float(value):
        raise ValueError(f"{name} must be an integer")
    return result
