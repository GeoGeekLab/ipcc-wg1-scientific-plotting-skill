from __future__ import annotations

from typing import Any

import numpy as np
import xarray as xr


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
    """Area-aware spatial mean with validity-aware weight normalization."""
    if lat_name not in data.coords or lon_name not in data.coords:
        raise ValueError("data must include latitude and longitude coordinates")
    if cell_area is None:
        cell_area = cosine_latitude_weights(data[lat_name])
    if not isinstance(cell_area, xr.DataArray):
        raise TypeError("cell_area must be an xarray.DataArray")
    if (cell_area < 0).any():
        raise ValueError("cell_area/weights must be non-negative")
    return data.weighted(cell_area).mean((lat_name, lon_name), skipna=True)


def classify_robustness(
    *,
    n_valid: xr.DataArray,
    agreement: xr.DataArray,
    min_count: int = 5,
    agreement_threshold: float = 0.80,
) -> xr.Dataset:
    """Create mutually exclusive map robustness classes.

    The thresholds are analytical recipe parameters, not universal IPCC rules.
    Returned classes are boolean masks: `robust`, `low_agreement`, and
    `insufficient_data`.
    """
    if min_count < 1:
        raise ValueError("min_count must be >= 1")
    if not 0.5 <= agreement_threshold <= 1:
        raise ValueError("agreement_threshold must be in [0.5, 1]")
    n_valid, agreement = xr.align(n_valid, agreement, join="exact")

    insufficient = n_valid < min_count
    low = (~insufficient) & (agreement < agreement_threshold)
    robust = (~insufficient) & (agreement >= agreement_threshold)

    result = xr.Dataset(
        {
            "robust": robust.rename("robust"),
            "low_agreement": low.rename("low_agreement"),
            "insufficient_data": insufficient.rename("insufficient_data"),
        }
    )
    result.attrs.update(
        {
            "minimum_valid_count": int(min_count),
            "agreement_threshold": float(agreement_threshold),
            "semantics": "mutually exclusive classes over all cells with finite diagnostics",
        }
    )
    return result


def add_mask_hatching(
    ax: Any,
    lon: np.ndarray,
    lat: np.ndarray,
    mask: np.ndarray | xr.DataArray,
    *,
    transform: Any = None,
    hatch: str = "////",
    zorder: int = 5,
) -> Any:
    """Overlay transparent hatching where `mask` is true.

    Works with ordinary Matplotlib axes and Cartopy GeoAxes. Pass an explicit
    Cartopy transform for geographic coordinates.
    """
    mask_values = np.asarray(mask, dtype=bool)
    field = np.where(mask_values, 1.0, np.nan)
    kwargs = {"levels": [0.5, 1.5], "colors": "none", "hatches": [hatch], "zorder": zorder}
    if transform is not None:
        kwargs["transform"] = transform
    return ax.contourf(lon, lat, field, **kwargs)


def add_low_agreement_hatching(
    ax: Any,
    lon: np.ndarray,
    lat: np.ndarray,
    mask: np.ndarray | xr.DataArray,
    *,
    transform: Any = None,
    hatch: str = "////",
    zorder: int = 5,
) -> Any:
    """Backward-compatible alias for low-agreement hatching."""
    return add_mask_hatching(
        ax,
        lon,
        lat,
        mask,
        transform=transform,
        hatch=hatch,
        zorder=zorder,
    )


def add_insufficient_data_mask(
    ax: Any,
    lon: np.ndarray,
    lat: np.ndarray,
    mask: np.ndarray | xr.DataArray,
    *,
    transform: Any = None,
    color: str = "0.85",
    zorder: int = 6,
) -> Any:
    """Overlay a neutral fill where sample support is insufficient."""
    mask_values = np.asarray(mask, dtype=bool)
    field = np.where(mask_values, 1.0, np.nan)
    kwargs = {"levels": [0.5, 1.5], "colors": [color], "zorder": zorder}
    if transform is not None:
        kwargs["transform"] = transform
    return ax.contourf(lon, lat, field, **kwargs)
