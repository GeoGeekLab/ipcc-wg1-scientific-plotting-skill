from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator, Mapping

import matplotlib as mpl
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np

_MM_PER_INCH = 25.4
_WIDTHS_MM = {"single": 89.0, "double": 183.0}


def figure_width_inches(width: str | float = "single") -> float:
    """Return figure width in inches from an IPCC-like publication width."""
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
    """Temporary, conservative Matplotlib settings for publication figures."""
    if font_scale <= 0:
        raise ValueError("font_scale must be positive")
    w = figure_width_inches(width)
    base = base_font_pt * font_scale
    params = {
        "figure.figsize": (w, w * 0.62),
        "figure.dpi": 120,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.02,
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
    with mpl.rc_context(params):
        yield


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
    """Save vector PDF and raster preview with deterministic metadata."""
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
            # PDF backend supports a restricted metadata vocabulary. Put detailed
            # provenance in the JSON sidecar instead of forcing arbitrary keys.
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
