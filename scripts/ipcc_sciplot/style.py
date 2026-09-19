from __future__ import annotations

import re
from collections.abc import Iterator, Mapping, Sequence
from contextlib import contextmanager
from pathlib import Path
from typing import Any

import matplotlib as mpl
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt

from .tokens import (
    DEFAULT_AXIS_WIDTH_PT,
    DEFAULT_DATA_LINEWIDTH_PT,
    DEFAULT_TICK_WIDTH_PT,
    FONT_FALLBACKS,
    FONT_PRIMARY,
    LEGEND_EDGE_COLOR,
    LEGEND_EDGE_WIDTH_PT,
    PANEL_LABEL_WEIGHT,
)

_MM_PER_INCH = 25.4
_WIDTHS_MM = {"single": 90.0, "double": 180.0}
_DEFAULT_FONTS_PT = {"single": 9.0, "double": 11.0}
_MAX_HEIGHT_MM = 250.0
_PRINT_RASTER_DPI = 350
_BRACKET_UNIT_RE = re.compile(r"\[[^\]]+\]")


def figure_width_inches(width: str | float = "single") -> float:
    if isinstance(width, str):
        if width not in _WIDTHS_MM:
            raise ValueError(f"width must be one of {sorted(_WIDTHS_MM)} or millimetres")
        width_mm = _WIDTHS_MM[width]
    else:
        width_mm = float(width)
        if width_mm <= 0:
            raise ValueError("width in millimetres must be positive")
    return width_mm / _MM_PER_INCH


def figure_size_inches(
    width: str | float = "single",
    *,
    height_mm: float | None = None,
    aspect: float = 0.62,
) -> tuple[float, float]:
    width_in = figure_width_inches(width)
    if height_mm is None:
        height_in = width_in * aspect
    else:
        if not 0 < height_mm <= _MAX_HEIGHT_MM:
            raise ValueError("height_mm must be in (0, 250] for IPCC figure delivery")
        height_in = height_mm / _MM_PER_INCH
    return width_in, height_in


def require_arial() -> str:
    """Return the resolved Arial path or fail."""
    try:
        return fm.findfont(FONT_PRIMARY, fallback_to_default=False)
    except ValueError as exc:
        raise RuntimeError(
            "Arial is required for strict IPCC WGI fidelity but is not installed. "
            "Install Arial or use strict_font=False and disclose the substitution."
        ) from exc


def _default_font_size(width: str | float) -> float:
    if isinstance(width, str):
        return _DEFAULT_FONTS_PT[width]
    return 9.0


@contextmanager
def publication_context(
    *,
    width: str | float = "single",
    height_mm: float | None = None,
    font_scale: float = 1.0,
    base_font_pt: float | None = None,
    strict_font: bool = False,
) -> Iterator[None]:
    """Apply AR6-WGI-oriented print-figure defaults.

    The WGI guide specifies 9 cm / 18 cm widths, a maximum 25 cm height,
    9 pt text on smaller figures and 11 pt on larger figures, with 0.5 pt axes.
    Figure-specific line weights and geometry should still follow the reference
    figure when performing exact reproduction.
    """
    if font_scale <= 0:
        raise ValueError("font_scale must be positive")
    if strict_font:
        require_arial()

    base = (base_font_pt or _default_font_size(width)) * font_scale
    params = {
        "figure.figsize": figure_size_inches(width, height_mm=height_mm),
        "figure.dpi": 120,
        "savefig.dpi": _PRINT_RASTER_DPI,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.02,
        "font.family": "sans-serif",
        "font.sans-serif": list(FONT_FALLBACKS),
        "font.size": base,
        "axes.titlesize": base,
        "axes.titleweight": "normal",
        "axes.labelsize": base,
        "xtick.labelsize": base,
        "ytick.labelsize": base,
        "legend.fontsize": base,
        "axes.linewidth": DEFAULT_AXIS_WIDTH_PT,
        "lines.linewidth": DEFAULT_DATA_LINEWIDTH_PT,
        "lines.markersize": 4.0,
        "xtick.major.width": DEFAULT_TICK_WIDTH_PT,
        "ytick.major.width": DEFAULT_TICK_WIDTH_PT,
        "axes.grid": False,
        "legend.frameon": True,
        "legend.fancybox": False,
        "legend.framealpha": 1.0,
        "legend.edgecolor": LEGEND_EDGE_COLOR,
        "legend.borderaxespad": 0.5,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "none",
        "axes.unicode_minus": True,
    }
    with mpl.rc_context(params):
        yield


def axis_label(name: str, unit: str | None = None) -> str:
    """Format a WGI-style axis label using parentheses for units."""
    name = name.strip()
    if not unit:
        return name
    return f"{name} ({unit.strip()})"


def panel_label(
    ax: mpl.axes.Axes,
    letter: str,
    *,
    title: str | None = None,
    x: float = 0.0,
    y: float = 1.02,
) -> mpl.text.Text:
    text = f"({letter.strip().strip('()')})"
    if title:
        text += f" {title}"
    return ax.text(
        x,
        y,
        text,
        transform=ax.transAxes,
        ha="left",
        va="bottom",
        fontweight=PANEL_LABEL_WEIGHT,
    )


def ipcc_legend(
    ax: mpl.axes.Axes,
    *,
    loc: str = "best",
    ncol: int = 1,
    **kwargs: Any,
) -> mpl.legend.Legend:
    legend = ax.legend(loc=loc, ncol=ncol, frameon=True, fancybox=False, framealpha=1.0, **kwargs)
    frame = legend.get_frame()
    frame.set_edgecolor(LEGEND_EDGE_COLOR)
    frame.set_linewidth(LEGEND_EDGE_WIDTH_PT)
    return legend


def audit_text_conventions(fig: mpl.figure.Figure) -> list[str]:
    """Return fidelity warnings for text conventions that can be audited safely."""
    warnings: list[str] = []
    for ax in fig.axes:
        for value, role in (
            (ax.get_xlabel(), "x-axis label"),
            (ax.get_ylabel(), "y-axis label"),
            (ax.get_title(), "title"),
        ):
            if value and _BRACKET_UNIT_RE.search(value):
                warnings.append(f"{role} uses square brackets for units: {value!r}")
        for text in ax.texts:
            value = text.get_text()
            if value and _BRACKET_UNIT_RE.search(value):
                warnings.append(f"annotation uses square brackets for units: {value!r}")
    return warnings


def save_figure(
    fig: mpl.figure.Figure,
    stem: str | Path,
    *,
    metadata: Mapping[str, Any] | None = None,
    formats: Sequence[str] = ("pdf", "png"),
    dpi: int = _PRINT_RASTER_DPI,
    close: bool = False,
) -> list[Path]:
    stem = Path(stem)
    stem.parent.mkdir(parents=True, exist_ok=True)
    clean_metadata = {str(k): str(v) for k, v in (metadata or {}).items()}
    outputs: list[Path] = []
    for fmt in formats:
        fmt = fmt.lower().lstrip(".")
        out = stem.with_suffix(f".{fmt}")
        kwargs: dict[str, Any] = {"bbox_inches": "tight", "pad_inches": 0.02}
        if fmt in {"png", "jpg", "jpeg", "tif", "tiff"}:
            kwargs["dpi"] = dpi
            kwargs["metadata"] = clean_metadata
        elif fmt == "pdf":
            kwargs["metadata"] = {
                key: value
                for key, value in clean_metadata.items()
                if key in {"Title", "Author", "Subject", "Keywords", "Creator", "Producer"}
            }
        fig.savefig(out, **kwargs)
        outputs.append(out)
    if close:
        plt.close(fig)
    return outputs
