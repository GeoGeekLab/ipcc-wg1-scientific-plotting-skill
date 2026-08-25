import numpy as np
import pandas as pd
import pytest
import xarray as xr

from ipcc_sciplot.validation import (
    infer_longitude_convention,
    inspect_climate_data,
    normalize_longitude,
    require_climate_ready,
)


def test_inspect_climate_data_happy_path() -> None:
    da = xr.DataArray(
        np.ones((2, 2, 3)),
        dims=("time", "lat", "lon"),
        coords={
            "time": pd.date_range("2000-01-01", periods=2, freq="YS"),
            "lat": [-10.0, 10.0],
            "lon": [0.0, 120.0, 240.0],
        },
        attrs={"units": "K"},
    )
    report = inspect_climate_data(da, expected_unit="K")
    assert report.longitude_convention == "0..360"
    assert report.n_missing == 0
    assert report.warnings == ()
    assert require_climate_ready(da, expected_unit="K").ok


def test_inspect_climate_data_detects_unit_problem() -> None:
    da = xr.DataArray(
        np.ones((2, 2)),
        dims=("lat", "lon"),
        coords={"lat": [-10.0, 10.0], "lon": [-20.0, 20.0]},
        attrs={"units": "degC"},
    )
    report = inspect_climate_data(da, expected_unit="K")
    assert any("unit mismatch" in warning for warning in report.warnings)
    with pytest.raises(ValueError, match="preflight failed"):
        require_climate_ready(da, expected_unit="K")


def test_normalize_longitude_does_not_interpolate() -> None:
    da = xr.DataArray(
        [1, 2, 3],
        dims="lon",
        coords={"lon": [0.0, 180.0, 300.0]},
        attrs={"units": "1"},
    )
    out = normalize_longitude(da, convention="-180..180")
    assert infer_longitude_convention(out.lon) == "-180..180"
    assert sorted(out.values.tolist()) == [1, 2, 3]
