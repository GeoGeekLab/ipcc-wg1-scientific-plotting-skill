# Statistical and uncertainty rules

This file is intentionally separate from the visual-style specification.

**There is no report-wide IPCC default for median vs mean, 17–83% vs 5–95%,
80% sign agreement, minimum model count, model weighting, FDR, or projection.**
Those are scientific/method choices and must come from the target analysis or
the specific AR6 reference figure.

Package defaults are convenience values for generic calculations only. They are
not evidence of IPCC visual fidelity.

## Ensemble statistics

For model changes `x_m` at a grid cell or time point, a figure contract may define:

- centre: mean, median, or another declared estimator;
- interval: declared quantiles/CI/model range;
- valid count: `n_valid = sum(isfinite(x_m))`;
- sign agreement relative to a declared reference.

A common sign-agreement calculation is:

```text
p_pos = count(x_m > reference) / n_valid
p_neg = count(x_m < reference) / n_valid
agreement = max(p_pos, p_neg)
```

If a threshold is used, it must be recorded as a method parameter. Some AR6
figures use an 80% criterion; that does **not** make 80% an IPCC-wide style token.

Zero handling must be explicit. A tolerance may be scientifically appropriate
for quantities where numerical noise around zero is not meaningful.

## Models and realizations

Do not infer the ensemble policy from visual style.

Possible choices include:

- one realization per model;
- model-first aggregation across realizations;
- equal-model mean/median;
- performance or independence weighting.

Whatever policy is used must match the study/reference and be disclosed. Scenario
spread is not automatically a probability distribution.

## Time series

- State smoothing/window/bandwidth.
- Account for autocorrelation when uncertainty depends on effective sample size.
- Keep the raw/central signal interpretable beneath uncertainty shading.
- Name intervals precisely rather than calling everything "error".

## Spatial significance

Significance and ensemble agreement are distinct concepts.

If a statistical test is part of the analysis:

1. define effect size and test;
2. check assumptions;
3. address multiplicity where scientifically appropriate;
4. account for spatial/temporal dependence as needed;
5. encode significance separately from model agreement.

The provided `fdr_bh_mask` is a standard BH helper, not an IPCC style rule.

## Area aggregation

Use actual grid-cell area when available. For a regular latitude/longitude grid,
`cos(latitude)` is a documented approximation, not a universal substitute.

## Missing data

- missing is not zero;
- report/track valid sample count;
- do not encode missingness with the same texture as disagreement or significance;
- make changes in sample composition visible in provenance/methods.

## Fidelity rule

When reproducing a published AR6 figure, the original figure's method and plotted
data take precedence over this package's calculation defaults.
