from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

import matplotlib as mpl

from .style import axis_label, ipcc_legend
from .tokens import GENERIC_LINE_COLORS, scenario_style


def plot_scenario_timeseries(
    ax: mpl.axes.Axes,
    x: Sequence[float],
    series: Mapping[str, Sequence[float]],
    *,
    profile: str = "ar6-report",
    linewidth: float = 1.6,
    legend: bool = True,
    legend_loc: str = "best",
) -> dict[str, mpl.lines.Line2D]:
    """Plot SSP/RCP lines with semantic WGI colours."""
    lines: dict[str, mpl.lines.Line2D] = {}
    for name, values in series.items():
        token = scenario_style(name, profile=profile)
        (line,) = ax.plot(
            x,
            values,
            color=token.color,
            linestyle=token.linestyle,
            linewidth=linewidth,
            label=name,
        )
        lines[name] = line
    if legend:
        ipcc_legend(ax, loc=legend_loc)
    return lines


def plot_generic_lines(
    ax: mpl.axes.Axes,
    x: Sequence[float],
    series: Mapping[str, Sequence[float]],
    *,
    linewidth: float = 1.4,
) -> dict[str, mpl.lines.Line2D]:
    """Plot non-semantic series using the WGI generic line-colour order."""
    if len(series) > 24:
        raise ValueError("generic line grammar supports at most 24 distinguishable series")
    line_styles = ("-", "--", ":", "-.")
    lines: dict[str, mpl.lines.Line2D] = {}
    for index, (name, values) in enumerate(series.items()):
        color = GENERIC_LINE_COLORS[index % len(GENERIC_LINE_COLORS)]
        linestyle = line_styles[index // len(GENERIC_LINE_COLORS)]
        (line,) = ax.plot(
            x,
            values,
            color=color,
            linestyle=linestyle,
            linewidth=linewidth,
            label=name,
        )
        lines[name] = line
    return lines


def plot_ensemble_band(
    ax: mpl.axes.Axes,
    x: Sequence[float],
    center: Sequence[float],
    lower: Sequence[float],
    upper: Sequence[float],
    *,
    color: str = "#000000",
    shade_color: str = "#808080",
    alpha: float = 0.25,
    label: str | None = None,
    interval_label: str | None = None,
) -> tuple[mpl.lines.Line2D, mpl.collections.PolyCollection]:
    band = ax.fill_between(
        x,
        lower,
        upper,
        color=shade_color,
        alpha=alpha,
        linewidth=0,
        label=interval_label,
    )
    (line,) = ax.plot(x, center, color=color, label=label)
    return line, band


def add_ipcc_colorbar(
    fig: mpl.figure.Figure,
    mappable: mpl.cm.ScalarMappable,
    *,
    ax: Any,
    label: str,
    unit: str | None = None,
    orientation: str = "horizontal",
    pad: float = 0.08,
    fraction: float = 0.05,
) -> mpl.colorbar.Colorbar:
    """Add a compact colour bar with units in parentheses."""
    cbar = fig.colorbar(
        mappable,
        ax=ax,
        orientation=orientation,
        pad=pad,
        fraction=fraction,
    )
    cbar.set_label(axis_label(label, unit))
    cbar.outline.set_linewidth(0.5)
    cbar.outline.set_edgecolor("black")
    return cbar


def short_panel_title(ax: mpl.axes.Axes, text: str) -> None:
    ax.set_title(text, loc="left", pad=4)
