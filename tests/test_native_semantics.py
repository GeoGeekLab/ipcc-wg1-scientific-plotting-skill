import numpy as np
import xarray as xr

from ipcc_sciplot.maps import classify_robustness
from ipcc_sciplot.scenarios import canonical_scenario_label, canonical_scenario_order


def test_canonical_scenario_order() -> None:
    labels = ["ssp585", "historical", "ssp126", "SSP2-4.5"]
    assert canonical_scenario_order(labels) == [
        "historical",
        "SSP1-2.6",
        "SSP2-4.5",
        "SSP5-8.5",
    ]
    assert canonical_scenario_label("ssp370") == "SSP3-7.0"


def test_robustness_classes_are_mutually_exclusive() -> None:
    n = xr.DataArray([4, 5, 8], dims="cell")
    agreement = xr.DataArray([0.9, 0.7, 0.9], dims="cell")
    classes = classify_robustness(
        n_valid=n,
        agreement=agreement,
        min_count=5,
        agreement_threshold=0.8,
    )
    stacked = np.vstack(
        [
            classes["robust"].values,
            classes["low_agreement"].values,
            classes["insufficient_data"].values,
        ]
    )
    assert np.all(stacked.sum(axis=0) == 1)
    assert classes["insufficient_data"].values.tolist() == [True, False, False]
    assert classes["low_agreement"].values.tolist() == [False, True, False]
    assert classes["robust"].values.tolist() == [False, False, True]
