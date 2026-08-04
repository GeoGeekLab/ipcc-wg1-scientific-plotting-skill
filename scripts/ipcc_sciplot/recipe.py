from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping

import yaml


@dataclass(frozen=True)
class FigureRecipe:
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
