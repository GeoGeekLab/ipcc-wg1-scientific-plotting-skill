import numpy as np
import xarray as xr

from ipcc_sciplot.uncertainty import ensemble_summary, fdr_bh_mask


def test_ensemble_summary_masks():
    da = xr.DataArray(
        [[1.0, 1.0, np.nan], [2.0, -1.0, np.nan], [3.0, 2.0, 1.0], [4.0, -2.0, 2.0]],
        dims=("model", "point"),
    )
    out = ensemble_summary(da, min_count=3, sign_agreement=0.75)
    assert out.n_valid.values.tolist() == [4, 4, 2]
    assert out.high_agreement.values.tolist() == [True, False, False]
    assert out.low_agreement.values.tolist() == [False, True, False]
    assert out.insufficient_data.values.tolist() == [False, False, True]


def test_fdr_bh_mask():
    p = xr.DataArray([0.001, 0.01, 0.04, 0.20, np.nan], dims="test")
    result = fdr_bh_mask(p, alpha=0.05)
    assert result.values.tolist() == [True, True, False, False, False]
