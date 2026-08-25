from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator, Mapping, Sequence

import matplotlib as mpl
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np

_MM_PER_INCH = 25.4
_WIDTHS_MM = {"single": 89.0, "double": 183.0}


def figure_width_inches(width: str | float = "single") -> float:
    """Return figure width in inches from a journal-like width or millimetres.

    `single`/`double` are retained for backward compatibility with the original
    toolkit. They are not asserted to be official IPCC report dimensions.
    """
    if isinstance(width, str):
        if width not in _WIDTHS_MM:
            raise ValueError(f"width must be one of {sorted(_WIDTHS_MM)} or millimetres")
        width_mm = _WIDTHS_MM[width]
    else:
        width_mm = float(width)
        if width_mm <= 0:
            raise ValueError("width in millimetres must be positive")
    return width_mm / _MM_PER_INCH


@contextmanager
def publication_context(
    *,
    width: str | float = "single",
    font_scale: float = 1.0,
    base_font_pt: float = 8.0,
) -> Iterator[None]:
    """Temporary conservative Matplotlib settings for publication figures."""
    if font_scale <= 0:
        raise ValueError("font_scale must be positive")
    w = figure_width_inches(width)
    base = base_font_pt * font_scale
    params = _base_rcparams(base)
    params.update({"figure.figsize": (w, w * 0.62)})
    with mpl.rc_context(params):
        yield


@contextmanager
def assessment_context(
    *,
    width_mm: float = 180.0,
    height_mm: float | None = None,
    aspect: float = 0.62,
    base_font_pt: float = 8.0,
    font_scale: float = 1.0,
) -> Iterator[None]:
    """Temporary context for report/assessment graphics with explicit dimensions.

    Unlike `publication_context`, callers provide the target report size directly.
    This avoids treating journal dimensions as native IPCC requirements.
    """
    if width_mm <= 0:
        raise ValueError("width_mm must be positive")
    if height_mm is not None and height_mm <= 0:
        raise ValueError("height_mm must be positive")
    if aspect <= 0 or font_scale <= 0 or base_font_pt <= 0:
        raise ValueError("aspect, font_scale and base_font_pt must be positive")

    width_in = width_mm / _MM_PER_INCH
    height_in = (height_mm / _MM_PER_INCH) if height_mm is not None else width_in * aspect
    params = _base_rcparams(base_font_pt * font_scale)
    params.update({"figure.figsize": (width_in, height_in)})
    with mpl.rc_context(params):
        yield


def make_norm(
    kind: str,
    *,
    vmin: float | None = None,
    vmax: float | None = None,
    vcenter: float | None = None,
    levels: Sequence[float] | None = None,
    clip: bool = False,
) -> mcolors.Normalize:
    """Build a normalization from declarative recipe semantics."""
    kind = kind.lower().replace("_", "-")
    if kind == "linear":
        return mcolors.Normalize(vmin=vmin, vmax=vmax, clip=clip)
    if kind in {"two-slope", "twoslope", "diverging"}:
        if vmin is None or vcenter is None or vmax is None:
            raise ValueError("two-slope normalization requires vmin, vcenter and vmax")
        if not vmin < vcenter < vmax:
            raise ValueError("require vmin < vcenter < vmax")
        return mcolors.TwoSlopeNorm(vmin=vmin, vcenter=vcenter, vmax=vmax)
    if kind == "boundary":
        if levels is None or len(levels) < 2:
            raise ValueError("boundary normalization requires at least two levels")
        boundaries = np.asarray(levels, dtype=float)
        if not np.all(np.diff(boundaries) > 0):
            raise ValueError("boundary levels must be strictly increasing")
        return mcolors.BoundaryNorm(boundaries, ncolors=256, clip=clip)
    if kind == "log":
        if vmin is not None and vmin <= 0:
            raise ValueError("log normalization requires vmin > 0")
        return mcolors.LogNorm(vmin=vmin, vmax=vmax, clip=clip)
    raise ValueError("kind must be linear, two-slope, boundary, or log")


def add_panel_label(
    ax: Any,
    label: str,
    *,
    x: float = 0.0,
    y: float = 1.02,
    weight: str = "bold",
    fontsize: float | None = None,
) -> Any:
    """Add a consistent panel label in axes coordinates."""
    return ax.text(
        x,
        y,
        label,
        transform=ax.transAxes,
        ha="left",
        va="bottom",
        fontweight=weight,
        fontsize=fontsize,
        clip_on=False,
    )


def register_rgb_colormap(
    path: str | Path,
    *,
    name: str | None = None,
    rgb_scale: int | float | None = None,
    reverse: bool = False,
) -> mcolors.Colormap:
    """Register a colormap from a whitespace/comma separated RGB text file.

    The function intentionally loads local files only. This allows users to use an
    authorized checkout of the IPCC colormap repository without redistributing it.
    """
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(path)
    data = np.loadtxt(path, delimiter="," if path.suffix.lower() == ".csv" else None)
    if data.ndim != 2 or data.shape[1] not in (3, 4):
        raise ValueError("RGB file must contain 3 or 4 numeric columns")
    if not np.isfinite(data).all():
        raise ValueError("RGB file contains non-finite values")
    if rgb_scale is None:
        rgb_scale = 255.0 if float(data.max()) > 1.0 else 1.0
    data = data / float(rgb_scale)
    if (data < 0).any() or (data > 1).any():
        raise ValueError("RGB values must be within [0, scale]")
    if reverse:
        data = data[::-1]
    cmap_name = name or path.stem
    cmap = mcolors.LinearSegmentedColormap.from_list(cmap_name, data)
    try:
        mpl.colormaps.register(cmap, name=cmap_name, force=True)
    except TypeError:  # Matplotlib versions without force=
        if cmap_name not in mpl.colormaps:
            mpl.colormaps.register(cmap, name=cmap_name)
    return cmap


def save_figure(
    fig: mpl.figure.Figure,
    stem: str | Path,
    *,
    metadata: Mapping[str, Any] | None = None,
    formats: tuple[str, ...] = ("pdf", "png"),
    dpi: int = 300,
    close: bool = False,
) -> list[Path]:
    """Save vector/raster figure outputs with deterministic metadata."""
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
            if fmt == "png":
                kwargs["metadata"] = clean_metadata
        elif fmt == "pdf":
            pdf_meta = {
                key: value
                for key, value in clean_metadata.items()
                if key in {"Title", "Author", "Subject", "Keywords", "Creator", "Producer"}
            }
            kwargs["metadata"] = pdf_meta
        fig.savefig(out, **kwargs)
        outputs.append(out)
    if close:
        plt.close(fig)
    return outputs


def _base_rcparams(base: float) -> dict[str, Any]:
    return {
        "figure.dpi": 120,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.02,
        "font.family": "sans-serif",
        "font.size": base,
        "axes.titlesize": base * 1.05,
        "axes.labelsize": base,
        "xtick.labelsize": base * 0.9,
        "ytick.labelsize": base * 0.9,
        "legend.fontsize": base * 0.85,
        "axes.linewidth": 0.7,
        "lines.linewidth": 1.4,
        "lines.markersize": 4.0,
        "xtick.major.width": 0.7,
        "ytick.major.width": 0.7,
        "xtick.minor.width": 0.5,
        "ytick.minor.width": 0.5,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "legend.frameon": False,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "none",
        "axes.unicode_minus": True,
    }
