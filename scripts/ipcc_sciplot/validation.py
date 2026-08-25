from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import xarray as xr


@dataclass(frozen=True)
class ClimateDataReport:
    """Compact preflight report for a climate DataArray."""

    dims: tuple[str, ...]
    shape: tuple[int, ...]
    unit: str | None
    calendar: str | None
    longitude_convention: str | None
    n_missing: int
    n_nonfinite: int
    duplicate_time_count: int
    warnings: tuple[str, ...]

    @property
    def ok(self) -> bool:
        return not self.warnings


def inspect_climate_data(
    data: xr.DataArray,
    *,
    lat_name: str = "lat",
    lon_name: str = "lon",
    time_name: str = "time",
    expected_unit: str | None = None,
    require_time_monotonic: bool = True,
) -> ClimateDataReport:
    """Inspect common failure modes before climate analysis or plotting.

    The function deliberately does not guess coordinate names. Callers should pass
    names resolved from CF metadata or a project contract when non-standard names
    are used.
    """

    if not isinstance(data, xr.DataArray):
        raise TypeError("data must be an xarray.DataArray")

    warnings: list[str] = []
    unit = _optional_text(data.attrs.get("units"))
    if expected_unit is not None and unit != expected_unit:
        warnings.append(f"unit mismatch: expected {expected_unit!r}, found {unit!r}")
    if unit is None:
        warnings.append("units attribute is missing")

    for coord_name in (lat_name, lon_name):
        if coord_name not in data.coords:
            warnings.append(f"coordinate {coord_name!r} is missing")

    longitude_convention: str | None = None
    if lon_name in data.coords:
        lon = np.asarray(data[lon_name].values, dtype=float)
        if not np.isfinite(lon).all():
            warnings.append("longitude coordinate contains non-finite values")
        else:
            longitude_convention = infer_longitude_convention(lon)
        if lon.ndim == 1 and lon.size > 1:
            diff = np.diff(lon)
            if not (np.all(diff > 0) or np.all(diff < 0)):
                warnings.append("1-D longitude coordinate is not monotonic")

    if lat_name in data.coords:
        lat = np.asarray(data[lat_name].values, dtype=float)
        if not np.isfinite(lat).all():
            warnings.append("latitude coordinate contains non-finite values")
        if np.nanmin(lat) < -90 or np.nanmax(lat) > 90:
            warnings.append("latitude coordinate lies outside [-90, 90]")
        if lat.ndim == 1 and lat.size > 1:
            diff = np.diff(lat)
            if not (np.all(diff > 0) or np.all(diff < 0)):
                warnings.append("1-D latitude coordinate is not monotonic")

    calendar: str | None = None
    duplicate_time_count = 0
    if time_name in data.coords:
        time = data[time_name]
        calendar = _calendar_name(time)
        index = time.to_index()
        duplicate_time_count = int(index.duplicated().sum())
        if duplicate_time_count:
            warnings.append(f"time coordinate contains {duplicate_time_count} duplicate values")
        if require_time_monotonic and not index.is_monotonic_increasing:
            warnings.append("time coordinate is not monotonically increasing")

    values = np.asarray(data.values)
    if np.issubdtype(values.dtype, np.number):
        n_missing = int(np.isnan(values).sum()) if np.issubdtype(values.dtype, np.floating) else 0
        n_nonfinite = int((~np.isfinite(values)).sum())
    else:
        n_missing = int(data.isnull().sum().item())
        n_nonfinite = n_missing

    return ClimateDataReport(
        dims=tuple(data.dims),
        shape=tuple(int(x) for x in data.shape),
        unit=unit,
        calendar=calendar,
        longitude_convention=longitude_convention,
        n_missing=n_missing,
        n_nonfinite=n_nonfinite,
        duplicate_time_count=duplicate_time_count,
        warnings=tuple(warnings),
    )


def require_climate_ready(
    data: xr.DataArray,
    **kwargs: Any,
) -> ClimateDataReport:
    """Run :func:`inspect_climate_data` and raise if preflight warnings remain."""

    report = inspect_climate_data(data, **kwargs)
    if report.warnings:
        joined = "; ".join(report.warnings)
        raise ValueError(f"climate-data preflight failed: {joined}")
    return report


def infer_longitude_convention(lon: np.ndarray | xr.DataArray) -> str:
    values = np.asarray(lon, dtype=float)
    if values.size == 0 or not np.isfinite(values).all():
        raise ValueError("longitude values must be finite and non-empty")
    lo = float(values.min())
    hi = float(values.max())
    if lo >= 0 and hi <= 360:
        return "0..360"
    if lo >= -180 and hi <= 180:
        return "-180..180"
    return "other"


def normalize_longitude(
    data: xr.DataArray | xr.Dataset,
    *,
    lon_name: str = "lon",
    convention: str = "-180..180",
    sort: bool = True,
) -> xr.DataArray | xr.Dataset:
    """Normalize 1-D longitude coordinates without interpolating data."""

    if lon_name not in data.coords:
        raise ValueError(f"longitude coordinate {lon_name!r} not found")
    lon = data[lon_name]
    if lon.ndim != 1:
        raise ValueError("normalize_longitude currently supports 1-D longitude coordinates")

    if convention == "-180..180":
        new_lon = ((lon + 180) % 360) - 180
    elif convention == "0..360":
        new_lon = lon % 360
    else:
        raise ValueError("convention must be '-180..180' or '0..360'")

    out = data.assign_coords({lon_name: new_lon})
    if sort:
        out = out.sortby(lon_name)
    return out


def _calendar_name(time: xr.DataArray) -> str | None:
    try:
        calendar = getattr(time.dt, "calendar", None)
        if calendar is not None:
            return str(calendar)
    except (AttributeError, TypeError, ValueError):
        pass
    encoding = time.encoding.get("calendar") if hasattr(time, "encoding") else None
    return _optional_text(encoding)


def _optional_text(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None
