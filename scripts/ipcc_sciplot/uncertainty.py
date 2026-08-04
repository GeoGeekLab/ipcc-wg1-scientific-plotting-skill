from __future__ import annotations

from typing import Literal

import numpy as np
import xarray as xr

Center = Literal["median", "mean"]


def ensemble_summary(
    data: xr.DataArray,
    *,
    dim: str = "model",
    center: Center = "median",
    lower_q: float = 0.17,
    upper_q: float = 0.83,
    reference: float = 0.0,
    sign_agreement: float = 0.80,
    min_count: int = 5,
    zero_tolerance: float = 0.0,
) -> xr.Dataset:
    """Summarize an ensemble and classify sign agreement.

    Zero values count as valid observations but support neither sign. A positive
    `zero_tolerance` treats values in [-tol, tol] as zero.
    """
    if dim not in data.dims:
        raise ValueError(f"dimension {dim!r} not found in {data.dims}")
    if not 0 <= lower_q < upper_q <= 1:
        raise ValueError("require 0 <= lower_q < upper_q <= 1")
    if not 0.5 <= sign_agreement <= 1:
        raise ValueError("sign_agreement must be in [0.5, 1]")
    if min_count < 1:
        raise ValueError("min_count must be >= 1")
    if zero_tolerance < 0:
        raise ValueError("zero_tolerance must be non-negative")

    valid = data.notnull()
    n_valid = valid.sum(dim=dim)
    delta = data - reference
    positive = (delta > zero_tolerance).sum(dim=dim)
    negative = (delta < -zero_tolerance).sum(dim=dim)
    agreement = xr.where(n_valid > 0, xr.apply_ufunc(np.maximum, positive, negative) / n_valid, np.nan)

    if center == "median":
        center_da = data.median(dim=dim, skipna=True)
    elif center == "mean":
        center_da = data.mean(dim=dim, skipna=True)
    else:
        raise ValueError("center must be 'median' or 'mean'")

    quantiles = data.quantile([lower_q, upper_q], dim=dim, skipna=True)
    lower = quantiles.sel(quantile=lower_q, drop=True)
    upper = quantiles.sel(quantile=upper_q, drop=True)
    insufficient = n_valid < min_count
    low_agreement = (agreement < sign_agreement) & ~insufficient
    high_agreement = (agreement >= sign_agreement) & ~insufficient

    ds = xr.Dataset(
        {
            "center": center_da,
            "lower": lower,
            "upper": upper,
            "n_valid": n_valid,
            "sign_agreement": agreement,
            "high_agreement": high_agreement,
            "low_agreement": low_agreement,
            "insufficient_data": insufficient,
        }
    )
    ds.attrs.update(
        {
            "ensemble_dimension": dim,
            "center_statistic": center,
            "lower_quantile": lower_q,
            "upper_quantile": upper_q,
            "reference": reference,
            "sign_agreement_threshold": sign_agreement,
            "minimum_valid_count": min_count,
            "zero_tolerance": zero_tolerance,
        }
    )
    return ds


def fdr_bh_mask(pvalues: xr.DataArray, *, alpha: float = 0.05) -> xr.DataArray:
    """Benjamini-Hochberg false-discovery-rate rejection mask.

    NaNs are ignored. This controls FDR under the usual BH assumptions; it does
    not itself account for spatial or temporal dependence.
    """
    if not 0 < alpha < 1:
        raise ValueError("alpha must be between 0 and 1")
    values = np.asarray(pvalues.values, dtype=float)
    finite = np.isfinite(values)
    flat = values[finite]
    reject = np.zeros(values.shape, dtype=bool)
    if flat.size:
        order = np.argsort(flat)
        ranked = flat[order]
        thresholds = alpha * np.arange(1, flat.size + 1) / flat.size
        passing = np.flatnonzero(ranked <= thresholds)
        if passing.size:
            cutoff = ranked[passing[-1]]
            reject[finite] = flat <= cutoff
    out = xr.DataArray(reject, coords=pvalues.coords, dims=pvalues.dims, name="fdr_reject")
    out.attrs.update({"method": "Benjamini-Hochberg", "alpha": alpha})
    return out
