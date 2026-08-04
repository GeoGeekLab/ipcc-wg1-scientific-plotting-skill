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
    if lat_name not in data.coords or lon_name not in data.coords:
        raise ValueError("data must include latitude and longitude coordinates")
    if cell_area is None:
        cell_area = cosine_latitude_weights(data[lat_name])
    return data.weighted(cell_area).mean((lat_name, lon_name), skipna=True)


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
    """Overlay transparent hatching where mask is true.

    Works with ordinary Matplotlib axes and Cartopy GeoAxes. Pass an explicit
    Cartopy transform for geographic coordinates.
    """
    mask = np.asarray(mask, dtype=bool)
    field = np.where(mask, 1.0, np.nan)
    kwargs = {"levels": [0.5, 1.5], "colors": "none", "hatches": [hatch], "zorder": zorder}
    if transform is not None:
        kwargs["transform"] = transform
    return ax.contourf(lon, lat, field, **kwargs)
