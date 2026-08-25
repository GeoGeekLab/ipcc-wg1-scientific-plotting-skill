# Uncertainty and Robustness Contract

Use this reference before drawing any band, whisker, hatch, stipple, confidence symbol, probability label or model-agreement mask.

The central rule is: **an uncertainty visual is valid only when its statistical object, sampling unit and interpretation can be stated in one precise sentence.**

## 1. Name the uncertainty source

Choose one or more, but do not collapse them into the word `error`:

- internal variability;
- observational/reanalysis uncertainty;
- measurement uncertainty;
- model structural spread;
- parametric uncertainty;
- scenario uncertainty;
- sampling uncertainty;
- confidence interval;
- credible interval;
- assessed likelihood range;
- method/sensitivity spread.

For each source record:

```text
object:
sampling unit:
calculation:
coverage/probability meaning:
visual encoding:
```

## 2. Ensemble ranges are not automatically confidence intervals

A 17–83% or 5–95% range across model values is an ensemble quantile range unless a probabilistic framework justifies stronger language.

Preferred wording:

> Shading shows the 17–83% range across model-level estimates.

Avoid:

> 66% confidence interval

unless it is actually a confidence/credible interval under a defined statistical model.

## 3. Ensemble hierarchy

A multi-model ensemble may have nested structure:

```text
model/source
  └─ realization/member
      └─ time/event samples
```

Default conservative handling when the assessment unit is model:

1. compute the target statistic within each realization;
2. combine realizations to one model-level estimate according to the study design;
3. summarize across models.

Do not treat 50 realizations from one model as 50 independent models.

If weighting is used, record:

- performance criterion;
- independence criterion;
- normalization;
- whether weights vary by variable/region/season;
- sensitivity to equal weighting.

## 4. Agreement is not significance

Model sign agreement, inter-product agreement and statistical significance answer different questions.

Examples:

- `sign_agreement = 0.8`: 80% of valid model-level changes share the dominant sign;
- `p < 0.05`: a test-statistic criterion under a stated null model;
- `confidence = high`: an assessment judgment integrating evidence and agreement.

Never use stippling/hatching for one concept and call it another in the caption.

## 5. Robustness classification

A useful map robustness scheme must be:

- pre-declared;
- mutually exclusive;
- exhaustive over valid cells;
- based on cell-specific valid sample count when availability varies.

Example recipe, not universal IPCC law:

```text
insufficient: n_valid < 5
low_agreement: n_valid >= 5 and dominant-sign fraction < 0.80
robust: n_valid >= 5 and dominant-sign fraction >= 0.80
```

This is a configurable analytical choice. The caption must report the thresholds.

Recommended visual semantics:

- base color = central estimate;
- no texture = robust under declared rule;
- hatch = low agreement / low robustness;
- neutral mask = insufficient data;
- stipple = statistical significance only when explicitly defined.

Do not use the same texture convention in two panels with different meanings.

## 6. Zero and near-zero changes

Sign agreement is unstable when many values lie near zero. Consider a scientifically meaningful `zero_tolerance` when measurement precision or practical relevance warrants it.

If used, state it explicitly:

```text
values in [-tol, +tol] are treated as neutral and support neither sign
```

Do not choose `tol` post hoc to make agreement look stronger.

## 7. Pointwise significance and multiplicity

For thousands of grid cells, naive pointwise testing can create a visually dense field of false positives.

Before stippling a map, consider:

- spatial/temporal autocorrelation;
- effective sample size;
- multiple-testing correction such as Benjamini–Hochberg FDR;
- field significance;
- resampling/block bootstrap;
- whether a model-agreement criterion is more appropriate to the scientific question.

`fdr_bh_mask` in `scripts/ipcc_sciplot/uncertainty.py` controls the Benjamini–Hochberg false discovery rate under its assumptions; it does not solve spatial dependence by itself.

## 8. Confidence and likelihood language

IPCC calibrated language is assessment language, not a plotting style token. Do not attach `likely`, `very likely`, `high confidence`, etc. merely because a numerical interval looks similar.

When a figure reproduces an assessed likelihood/confidence statement:

- preserve the exact assessed term;
- identify the assessment source;
- visually distinguish assessed ranges from raw model ensemble spread;
- do not derive confidence terminology solely from model counts.

## 9. Time-series uncertainty

Preferred order:

1. central estimate line;
2. inner interval if needed;
3. outer interval if needed;
4. individual model/member lines only as quiet context.

If showing two nested bands, the caption must define both, e.g. 17–83% and 5–95% model ranges.

Avoid opaque overlapping scenario bands. Where several scenarios overlap, consider line emphasis, direct labels and lower-alpha bands.

## 10. Map texture density

Texture can destroy the map if overused.

Rules:

- use one texture family for one evidence-status variable;
- choose hatch spacing that remains legible at final size;
- avoid simultaneously dense hatching + stippling + administrative borders + graticules;
- mask insufficient data before drawing agreement texture;
- use vector hatch for moderate complexity, but rasterize dense texture layers if PDF size becomes excessive;
- test at final printed/report scale, not only on a large monitor.

## 11. Regional interval plots

For regional or GWL comparisons show:

- central estimate;
- declared spread/interval;
- sample count when variable;
- observational/assessed range as a distinct object if present.

If intervals overlap strongly, avoid visually overclaiming rank differences.

## 12. Caption sentence test

Every uncertainty encoding should pass this test:

> [Visual mark] shows [statistical object] calculated across [sampling unit] using [method/interval]; [texture/mask] marks [robustness/significance condition] with threshold [value], and [gray/blank] indicates [missing/insufficient condition].

If the sentence is ambiguous, revise the analysis or encoding before finalizing the figure.