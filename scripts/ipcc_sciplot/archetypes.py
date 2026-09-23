from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from typing import Any

import matplotlib as mpl
import matplotlib.pyplot as plt

from .style import axis_label, figure_size_inches, ipcc_legend
from .tokens import DEFAULT_DATA_LINEWIDTH_PT, GENERIC_LINE_COLORS, scenario_style


def map_panel_grid(
    n_panels: int,
    *,
    projection: Any = None,
    ncols: int | None = None,
    width: str | float = "double",
    height_mm: float | None = None,
    panel_aspect: float = 0.55,
    wspace: float = 0.03,
    hspace: float = 0.08,
) -> tuple[mpl.figure.Figure, tuple[mpl.axes.Axes, ...]]:
    """Create a compact fixed-size panel grid for map or spatial figures."""
    if n_panels < 1:
        raise ValueError("n_panels must be >= 1")
    if ncols is None:
        ncols = min(3, n_panels)
    if ncols < 1:
        raise ValueError("ncols must be >= 1")
    if panel_aspect <= 0:
        raise ValueError("panel_aspect must be positive")

    nrows = math.ceil(n_panels / ncols)
    if height_mm is None:
        width_in, _ = figure_size_inches(width)
        panel_width_in = width_in / ncols
        height_mm = panel_width_in * panel_aspect * nrows * 25.4

    subplot_kw = {} if projection is None else {"projection": projection}
    fig, grid = plt.subplots(
        nrows,
        ncols,
        squeeze=False,
        figsize=figure_size_inches(width, height_mm=height_mm),
        subplot_kw=subplot_kw,
        gridspec_kw={"wspace": wspace, "hspace": hspace},
    )
    axes = list(grid.flat)
    for extra_ax in axes[n_panels:]:
        extra_ax.remove()
    return fig, tuple(axes[:n_panels])


def label_line_ends(
    ax: mpl.axes.Axes,
    lines: Mapping[str, mpl.lines.Line2D],
    *,
    min_gap_points: float = 2.0,
    x_pad_points: float = 4.0,
    connector_threshold_points: float = 2.0,
    fontsize: float | None = None,
) -> dict[str, mpl.text.Annotation]:
    """Label line endpoints while separating labels that would overlap."""
    if min_gap_points < 0:
        raise ValueError("min_gap_points must be >= 0")

    endpoints: list[tuple[str, mpl.lines.Line2D, float, float]] = []
    for label, line in lines.items():
        x = line.get_xdata(orig=False)
        y = line.get_ydata(orig=False)
        finite = [
            index
            for index, (x_value, y_value) in enumerate(zip(x, y, strict=False))
            if math.isfinite(float(x_value)) and math.isfinite(float(y_value))
        ]
        if not finite:
            continue
        index = finite[-1]
        endpoints.append((label, line, float(x[index]), float(y[index])))

    if not endpoints:
        return {}

    ax.relim()
    ax.autoscale_view()
    ax.figure.canvas.draw()

    endpoint_y_px = [
        float(ax.transData.transform((x_value, y_value))[1])
        for _, _, x_value, y_value in endpoints
    ]
    ordered = sorted(
        zip(endpoints, endpoint_y_px, strict=True),
        key=lambda item: item[1],
    )

    low = float(ax.bbox.y0)
    high = float(ax.bbox.y1)
    font_points = float(fontsize if fontsize is not None else mpl.rcParams["font.size"])
    requested_gap = (font_points + min_gap_points) * ax.figure.dpi / 72.0
    if len(ordered) > 1:
        gap = min(requested_gap, max(0.0, (high - low) / (len(ordered) - 1)))
    else:
        gap = 0.0

    adjusted_y_px: list[float] = []
    for _, original_y_px in ordered:
        candidate = max(original_y_px, low)
        if adjusted_y_px:
            candidate = max(candidate, adjusted_y_px[-1] + gap)
        adjusted_y_px.append(candidate)

    overflow = adjusted_y_px[-1] - high
    if overflow > 0:
        adjusted_y_px = [value - overflow for value in adjusted_y_px]
    if adjusted_y_px[0] < low:
        adjusted_y_px = [low + index * gap for index in range(len(adjusted_y_px))]

    x_pad_px = x_pad_points * ax.figure.dpi / 72.0
    x_axes = 1.0 + x_pad_px / float(ax.bbox.width)
    label_transform = mpl.transforms.blended_transform_factory(ax.transAxes, ax.transData)
    threshold_px = connector_threshold_points * ax.figure.dpi / 72.0

    annotations: dict[str, mpl.text.Annotation] = {}
    for ((label, line, x_value, y_value), original_y_px), target_y_px in zip(
        ordered,
        adjusted_y_px,
        strict=True,
    ):
        target_data_y = float(
            ax.transData.inverted().transform((float(ax.bbox.x1), target_y_px))[1]
        )
        arrowprops = None
        if abs(target_y_px - original_y_px) > threshold_px:
            arrowprops = {
                "arrowstyle": "-",
                "color": line.get_color(),
                "linewidth": 0.5,
                "shrinkA": 0,
                "shrinkB": 0,
            }

        annotations[label] = ax.annotate(
            label,
            xy=(x_value, y_value),
            xycoords="data",
            xytext=(x_axes, target_data_y),
            textcoords=label_transform,
            ha="left",
            va="center",
            color=line.get_color(),
            fontsize=fontsize,
            annotation_clip=False,
            arrowprops=arrowprops,
        )

    return annotations

def plot_scenario_timeseries(
    ax: mpl.axes.Axes,
    x: Sequence[float],
    series: Mapping[str, Sequence[float]],
    *,
    profile: str = "ar6-report",
    linewidth: float = DEFAULT_DATA_LINEWIDTH_PT,
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
    linewidth: float = DEFAULT_DATA_LINEWIDTH_PT,
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
