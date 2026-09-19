from __future__ import annotations

from dataclasses import dataclass
from typing import Final

RGB = tuple[int, int, int]


def _hex(rgb: RGB) -> str:
    return "#" + "".join(f"{v:02X}" for v in rgb)


@dataclass(frozen=True)
class ScenarioStyle:
    color: str
    linestyle: str = "-"
    linewidth: float = 1.6


GENERIC_LINE_RGB: Final[tuple[RGB, ...]] = (
    (0, 0, 0),
    (112, 160, 205),
    (196, 121, 0),
    (178, 178, 178),
    (0, 52, 102),
    (0, 79, 0),
)
GENERIC_LINE_COLORS: Final[tuple[str, ...]] = tuple(_hex(v) for v in GENERIC_LINE_RGB)

GENERIC_SHADE_RGB: Final[tuple[RGB, ...]] = (
    (128, 128, 128),
    (91, 174, 178),
    (204, 174, 113),
    (191, 191, 191),
    (67, 147, 195),
    (223, 237, 195),
)
GENERIC_SHADE_COLORS: Final[tuple[str, ...]] = tuple(_hex(v) for v in GENERIC_SHADE_RGB)

AR6_REPORT_SSP: Final[dict[str, ScenarioStyle]] = {
    "ssp119": ScenarioStyle("#1E9684"),
    "ssp126": ScenarioStyle("#1D3354"),
    "ssp245": ScenarioStyle("#EADD3D"),
    "ssp370": ScenarioStyle("#F21111"),
    "ssp585": ScenarioStyle("#840B22"),
}
AR6_REPORT_RCP: Final[dict[str, ScenarioStyle]] = {
    "rcp26": ScenarioStyle("#003466"),
    "rcp45": ScenarioStyle("#70A0CD"),
    "rcp60": ScenarioStyle("#C47900"),
    "rcp85": ScenarioStyle("#990002"),
}

WGI_GUIDE_2022_SSP: Final[dict[str, ScenarioStyle]] = {
    "ssp119": ScenarioStyle("#00ADCF"),
    "ssp126": ScenarioStyle("#173C66"),
    "ssp245": ScenarioStyle("#F79420"),
    "ssp370": ScenarioStyle("#E71D25"),
    "ssp585": ScenarioStyle("#951B1E"),
}

LAND_GREY: Final[str] = "#B2B2B2"
COAST_GREY: Final[str] = "#999999"
MISSING_DATA: Final[str] = "#FFFFFF"
TEXT_COLOR: Final[str] = "#000000"

PANEL_LABEL_WEIGHT: Final[str] = "bold"
LEGEND_EDGE_COLOR: Final[str] = "#000000"
LEGEND_EDGE_WIDTH_PT: Final[float] = 0.5

DEFAULT_LINEWIDTH_PT: Final[float] = 1.4
DEFAULT_AXIS_WIDTH_PT: Final[float] = 0.7
DEFAULT_TICK_WIDTH_PT: Final[float] = 0.7

FONT_PRIMARY: Final[str] = "Arial"
FONT_FALLBACKS: Final[tuple[str, ...]] = ("Arial", "Liberation Sans", "DejaVu Sans")


def _scenario_key(value: str) -> str:
    return (
        value.strip()
        .lower()
        .replace("-", "")
        .replace(".", "")
        .replace(" ", "")
        .replace("_", "")
    )


def scenario_style(
    scenario: str,
    *,
    profile: str = "ar6-report",
) -> ScenarioStyle:
    key = _scenario_key(scenario)
    if profile == "ar6-report":
        table = {**AR6_REPORT_SSP, **AR6_REPORT_RCP}
    elif profile == "wgi-guide-2022":
        table = {**WGI_GUIDE_2022_SSP, **AR6_REPORT_RCP}
    else:
        raise ValueError("profile must be 'ar6-report' or 'wgi-guide-2022'")
    try:
        return table[key]
    except KeyError as exc:
        raise KeyError(f"no IPCC semantic colour registered for {scenario!r}") from exc
