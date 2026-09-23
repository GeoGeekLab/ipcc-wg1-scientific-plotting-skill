from __future__ import annotations

from typing import Any

import matplotlib as mpl
import numpy as np
import xarray as xr
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

from .tokens import COAST_GREY, LAND_GREY, MISSING_DATA


def add_uncertainty_legend(
    ax: mpl.axes.Axes,
    *,
    low_agreement: str | None = None,
    insufficient_data: str | None = None,
    significance: str | None = None,
    hatch: str = "////",
    hatch_color: str = "black",
    missing_color: str = MISSING_DATA,
    significance_color: str = "black",
    loc: str = "lower left",
    ncol: int = 1,
    frameon: bool = False,
    **kwargs: Any,
) -> mpl.legend.Legend:
    """Add legend entries for uncertainty textures used on a map."""
    handles: list[Any] = []
    if low_agreement:
        handles.append(
            Patch(
                facecolor="none",
                edgecolor=hatch_color,
                hatch=hatch,
                linewidth=0.5,
                label=low_agreement,
            )
        )
    if insufficient_data:
        handles.append(
            Patch(
                facecolor=missing_color,
                edgecolor="none",
                label=insufficient_data,
            )
        )
    if significance:
        handles.append(
            Line2D(
                [],
                [],
                linestyle="none",
                marker=".",
                color=significance_color,
                markersize=6,
                label=significance,
            )
        )
    if not handles:
        raise ValueError("provide at least one uncertainty legend label")
    return ax.legend(
        handles=handles,
        loc=loc,
        ncol=ncol,
        frameon=frameon,
        **kwargs,
    )


def cosine_latitude_weights(lat: xr.DataArray) -> xr.DataArray:
    """Approximate area weights for a regular latitude-longitude grid."""
    if lat.ndim != 1:
        raise ValueError("cosine weights require a one-dimensional latitude coordinate")
    values = np.cos(np.deg2rad(lat.astype(float)))
    weights = xr.DataArray(values, coords=lat.coords, dims=lat.dims, name="latitude_weight")
    weights.attrs["note"] = "cos(latitude) approximation for regular lat-lon grid"
    return weights


def weighted_spatial_mean(
    data: xr.DataArray,
    *,
    lat_name: str = "lat",
    lon_name: str = "lon",
    cell_area: xr.DataArray | None = None,
) -> xr.DataArray:
    if lat_name not in data.coords or lon_name not in data.coords:
        raise ValueError("data must include latitude and longitude coordinates")
    if cell_area is None:
        cell_area = cosine_latitude_weights(data[lat_name])
    return data.weighted(cell_area).mean((lat_name, lon_name), skipna=True)


def add_map_context(
    ax: Any,
    *,
    land: bool = True,
    coastlines: bool = True,
    borders: bool = False,
    linewidth: float = 0.4,
    zorder: int = 10,
) -> None:
    """Add restrained geographic context to a Cartopy GeoAxes."""
    try:
        import cartopy.feature as cfeature
    except ImportError as exc:
        raise ImportError("Cartopy is required for map context") from exc

    if land:
        ax.add_feature(cfeature.LAND, facecolor=LAND_GREY, edgecolor="none", zorder=zorder)
    if coastlines:
        ax.coastlines(color=COAST_GREY, linewidth=linewidth, zorder=zorder + 1)
    if borders:
        ax.add_feature(
            cfeature.BORDERS,
            edgecolor=COAST_GREY,
            facecolor="none",
            linewidth=linewidth,
            zorder=zorder + 1,
        )


def _overlay_mask(
    ax: Any,
    lon: np.ndarray,
    lat: np.ndarray,
    mask: np.ndarray,
    *,
    transform: Any = None,
    colors: str = "none",
    hatches: list[str] | None = None,
    zorder: int = 5,
) -> Any:
    mask = np.asarray(mask, dtype=bool)
    field = np.where(mask, 1.0, np.nan)
    kwargs: dict[str, Any] = {
        "levels": [0.5, 1.5],
        "colors": colors,
        "zorder": zorder,
    }
    if hatches is not None:
        kwargs["hatches"] = hatches
    if transform is not None:
        kwargs["transform"] = transform
    return ax.contourf(lon, lat, field, **kwargs)


def add_low_agreement_hatching(
    ax: Any,
    lon: np.ndarray,
    lat: np.ndarray,
    mask: np.ndarray,
    *,
    transform: Any = None,
    hatch: str = "////",
    zorder: int = 5,
) -> Any:
    """Hatch low sign-agreement areas.

    This layer denotes ensemble agreement only. It must not be reused for
    statistical significance or missing data.
    """
    return _overlay_mask(
        ax,
        lon,
        lat,
        mask,
        transform=transform,
        colors="none",
        hatches=[hatch],
        zorder=zorder,
    )


def add_insufficient_data_mask(
    ax: Any,
    lon: np.ndarray,
    lat: np.ndarray,
    mask: np.ndarray,
    *,
    transform: Any = None,
    color: str = MISSING_DATA,
    zorder: int = 6,
) -> Any:
    """Cover cells with insufficient valid samples using a dedicated mask."""
    return _overlay_mask(
        ax,
        lon,
        lat,
        mask,
        transform=transform,
        colors=color,
        zorder=zorder,
    )


def add_significance_stippling(
    ax: Any,
    lon: np.ndarray,
    lat: np.ndarray,
    mask: np.ndarray,
    *,
    transform: Any = None,
    stride: int = 2,
    size: float = 2.0,
    color: str = "black",
    zorder: int = 7,
) -> Any:
    """Stipple cells that explicitly encode a statistical-significance mask."""
    if stride < 1:
        raise ValueError("stride must be >= 1")
    lon = np.asarray(lon)
    lat = np.asarray(lat)
    mask = np.asarray(mask, dtype=bool)

    if lon.ndim == 1 and lat.ndim == 1:
        xx, yy = np.meshgrid(lon, lat)
    elif lon.shape == lat.shape:
        xx, yy = lon, lat
    else:
        raise ValueError("lon/lat must be 1-D coordinates or matching 2-D arrays")
    if mask.shape != xx.shape:
        raise ValueError("mask shape does not match coordinate grid")

    pick = mask.copy()
    thinning = np.zeros_like(pick, dtype=bool)
    thinning[::stride, ::stride] = True
    pick &= thinning

    kwargs: dict[str, Any] = {
        "s": size,
        "c": color,
        "marker": ".",
        "linewidths": 0,
        "zorder": zorder,
    }
    if transform is not None:
        kwargs["transform"] = transform
    return ax.scatter(xx[pick], yy[pick], **kwargs)
