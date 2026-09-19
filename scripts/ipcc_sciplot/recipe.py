from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True)
class FigureRecipe:
    figure_id: str
    question: str
    estimand: str
    plot_type: str
    variable: str
    unit: str
    style_profile: str = "ar6-report"
    fidelity: str = "strict"
    archetype: str | None = None
    baseline: str | None = None
    center: str | None = None
    lower_quantile: float | None = None
    upper_quantile: float | None = None
    sign_agreement: float | None = None
    min_valid_count: int | None = None
    colormap: str | None = None
    projection: str | None = None
    output_stem: str = "outputs/figure"
    extras: Mapping[str, Any] = field(default_factory=dict)

    def validate(self) -> None:
        if not self.figure_id.strip():
            raise ValueError("figure_id is required")
        if not self.question.strip() or not self.estimand.strip():
            raise ValueError("question and estimand are required")
        if self.style_profile not in {"ar6-report", "wgi-guide-2022"}:
            raise ValueError("unsupported style_profile")
        if self.fidelity not in {"strict", "adapted"}:
            raise ValueError("fidelity must be 'strict' or 'adapted'")

        quantiles = (self.lower_quantile, self.upper_quantile)
        if (quantiles[0] is None) != (quantiles[1] is None):
            raise ValueError("lower_quantile and upper_quantile must be set together")
        if (
            quantiles[0] is not None
            and quantiles[1] is not None
            and not 0 <= quantiles[0] < quantiles[1] <= 1
        ):
            raise ValueError("invalid quantile interval")

        if self.sign_agreement is not None and not 0.5 <= self.sign_agreement <= 1:
            raise ValueError("sign_agreement must be in [0.5, 1]")
        if self.min_valid_count is not None and self.min_valid_count < 1:
            raise ValueError("min_valid_count must be >= 1")

        if self.plot_type == "map" and self.fidelity == "strict":
            if not self.colormap:
                raise ValueError("strict map recipes require an official IPCC colormap name")
            if not self.projection:
                raise ValueError("strict map recipes require an explicit projection")

    @property
    def is_strict(self) -> bool:
        return self.fidelity == "strict"


def load_recipe(path: str | Path) -> FigureRecipe:
    payload = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("recipe root must be a mapping")
    known = {
        "figure_id",
        "question",
        "estimand",
        "plot_type",
        "variable",
        "unit",
        "style_profile",
        "fidelity",
        "archetype",
        "baseline",
        "center",
        "lower_quantile",
        "upper_quantile",
        "sign_agreement",
        "min_valid_count",
        "colormap",
        "projection",
        "output_stem",
    }
    args = {k: payload[k] for k in known if k in payload}
    args["extras"] = {k: v for k, v in payload.items() if k not in known}
    recipe = FigureRecipe(**args)
    recipe.validate()
    return recipe
