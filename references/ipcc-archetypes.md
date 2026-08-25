# IPCC-native Figure Archetypes

These archetypes are production patterns, not templates to copy mechanically. Select the minimum architecture that supports the assessment statement.

## 1. `assessment-map`

Use for climatology, anomalies, projected change, extremes, exposure or spatially varying evidence.

### Preferred panel logic

- headline map: central estimate or assessed state;
- optional compact secondary map: robustness, sample support, observational comparison or another variable;
- optional regional summary: intervals/ranking for policy-relevant regions.

### Rules

- Map color encodes the primary quantity.
- Robustness uses a secondary channel such as hatch/stipple/mask.
- Missing or insufficient data must be visually distinct from zero/no change.
- Report colorbar units and transformation.
- Avoid tiny multipanel maps unless the reader must compare the same field across scenarios/periods.
- If comparing maps, share projection, extent, normalization and color breaks whenever scientifically defensible.

## 2. `scenario-timeseries`

Use for historical-to-future evolution, scenario divergence, observations vs simulations, or global/regional means.

### Preferred hierarchy

1. observations/reanalysis or historical evidence;
2. central modeled estimate;
3. uncertainty envelopes;
4. scenario identities;
5. direct annotation of reference periods or policy thresholds.

### Rules

- Historical and scenario periods may have different epistemic status; communicate this visually if needed.
- Do not render dozens of models as equally salient lines in a synthesis figure.
- If individual models are important, place them as low-salience context behind the summary.
- Keep SSP identities stable across all panels and figures in the same product.
- Separate scenario uncertainty from model spread when both are shown.

## 3. `warming-level-response`

Use when the scientific framing is 1.5, 2, 3 or 4 °C Global Warming Levels rather than fixed calendar windows.

### Preferred structures

- aligned point/interval plots by GWL;
- small-multiple maps with identical color normalization;
- regional response matrix;
- response-vs-global-warming curve.

### Rules

- State how GWL crossing years/windows are defined.
- Do not mix GWL values with fixed calendar time slices without explicit explanation.
- For scenario-combined GWL analyses, explain how scenario/model samples contribute at each level.
- Sample size may change with GWL; show or record it.

## 4. `regional-synthesis`

Use for AR6 reference regions, continents, basins or policy-relevant geographic units.

### Preferred composition

- small locator/reference-region map;
- ranked or geographically ordered interval plot;
- optional matrix of variables/seasons/levels.

### Rules

- Use verified region geometries.
- Preserve a stable region ordering across panels.
- If using AR6 reference regions, distinguish land/ocean regions where relevant.
- Regional aggregation must be area weighted and mask-aware.
- Avoid map-only regional comparisons when exact differences between regions matter; add interval/ranked panels.

## 5. `ensemble-distribution`

Use when spread, constraint, disagreement or source comparison is itself the evidence.

### Preferred structures

- dot + interval summaries;
- ECDF;
- violin/box plus model-level points;
- ridge/small multiples only when several comparable distributions are necessary.

### Rules

- The sampling unit must be explicit.
- Do not hide model multiplicity or weighting behind a smooth violin.
- Show center and interval definitions.
- If observations are used to constrain/evaluate models, visually separate observational uncertainty from ensemble spread.

## 6. `emergence-or-threshold`

Use for time of emergence, exceedance probabilities, return-period shifts, threshold crossing or hazard classification.

### Preferred structures

- threshold crossing timeline;
- map of crossing year/level with sample-support mask;
- exceedance probability curve with uncertainty;
- distribution of first-crossing times.

### Rules

- Define the threshold and reference variability explicitly.
- Distinguish "not emerged by end of period" from missing data.
- If censoring occurs, treat it statistically and visually as censoring, not as an arbitrary terminal year.

## 7. `evidence-matrix`

Use for a compact synthesis across variables, seasons, regions or observational products.

### Rules

- Every cell must share a clearly defined scale/legend or use direct numeric/ordinal encoding.
- Do not use color to encode two incompatible quantities.
- If rows/columns have a natural order (latitude, warming level, scenario forcing), preserve it.
- Avoid decorative heatmaps where precise interval information is necessary.

## 8. `assessment-composite`

Use for Summary-for-Policymakers, Technical Summary or chapter synthesis figures that combine multiple evidence modes.

### Structure

- one headline panel carrying the primary assessment statement;
- 2–4 subordinate panels that explain regional detail, temporal evolution or robustness;
- concise annotations that connect panels semantically;
- one shared legend/semantic key when possible.

### Rules

- Unequal panel sizes are encouraged when evidence importance is unequal.
- Reuse color/line/marker semantics across all panels.
- Do not combine panels merely because they use the same dataset.
- If a panel requires a new legend grammar, ask whether it belongs in another figure.

## Panel selection test

For each planned panel answer:

```text
Unique question answered:
Evidence role:
What conclusion becomes weaker if removed:
What uncertainty it communicates:
What semantic vocabulary it reuses:
```

Remove panels that cannot answer these questions.
