# IPCC-native Assessment Contract

Use this reference before writing plotting code. The figure must support an assessment statement, not merely display a dataset.

## Required contract

```text
Assessment intent:
Audience:
Evidence role:
Scientific question:
Core conclusion or provisional conclusion:
Estimand:
Data sources:
Temporal frame:
Spatial frame:
Ensemble policy:
Uncertainty definition:
Robustness definition:
Scenario/GWL semantics:
Figure archetype:
Panel map:
  a:
  b:
  c:
Plotted-data artifact:
Export contract:
Assessment/reviewer risk:
```

## 1. Assessment intent

Write one sentence with a conclusion verb. Good examples:

- "Heavy precipitation increases across most assessed land regions at 2 °C global warming, with lower agreement in selected subtropical regions."
- "Projected warming rises with emissions scenario after mid-century while observational and model uncertainty overlap strongly in the historical period."

Avoid topic labels such as "Temperature projections" or "CMIP6 results".

If the evidence is not yet sufficient to support a directional conclusion, state the intent as a question and label the eventual result provisional.

## 2. Audience

Choose one dominant reader:

- `chapter-author`: technically dense, assumes domain fluency;
- `technical-summary`: compact synthesis with explicit uncertainty;
- `policymaker`: low legend burden, headline-first, conservative annotation;
- `public-assessment`: strongest explanatory hierarchy and direct labels.

The scientific content does not change with audience; hierarchy and explanatory burden do.

## 3. Evidence role

Every panel has one role:

- `headline`: the single view that carries the main assessment statement;
- `primary-evidence`: central quantitative support;
- `mechanism`: process/context needed to interpret the result;
- `regional-detail`: spatial disaggregation;
- `robustness`: sensitivity, model spread, observational comparison or methodological stability;
- `context`: baseline, historical framing or definitions.

If covering a panel would not weaken the assessment argument, remove or merge it.

## 4. Estimand

An estimand must identify at least:

```text
variable/index:
transformation: absolute / anomaly / percent change / ratio / exceedance
reference or baseline:
time aggregation:
space aggregation:
ensemble sampling unit:
center statistic:
```

Example:

```text
Annual maximum 1-day precipitation (Rx1day), percent change in each model's
20-year mean at the 2 °C GWL relative to 1995–2014, summarized by the
model-equal median across models.
```

"Projected change" alone is not an estimand.

## 5. Temporal frame

Record explicitly:

- baseline/reference period;
- target period or Global Warming Level;
- season and season-year convention (for example DJF assigned to January year);
- historical/scenario transition handling;
- calendar treatment;
- smoothing or running-window method;
- GWL window definition, if used.

Do not silently mix fixed time slices and warming-level windows in the same comparison.

## 6. Spatial frame

Specify:

- global, regional, gridded or point/site analysis;
- land/ocean/ice masks;
- AR6 reference region or verified custom geometry;
- area-weighting method;
- source and target grid if regridded;
- projection used only for rendering, not analysis.

## 7. Ensemble policy

Capture:

```text
models included:
experiments/scenarios:
realizations per model:
within-model aggregation:
model weighting:
independence assumptions:
minimum valid sample:
```

A common conservative policy is one model-level value per model followed by equal-model summary. This is not universally correct; document deviations.

## 8. Uncertainty and robustness

Separate the concepts:

- ensemble spread;
- confidence/credible interval;
- observational uncertainty;
- internal variability;
- structural/model uncertainty;
- scenario uncertainty;
- robustness/agreement class.

For each visual encoding, write a sentence that can be copied into a caption. Example:

> Shading shows the 17–83% range across model-level estimates; hatching marks grid cells where fewer than 80% of valid models agree on the sign of change; gray indicates fewer than five valid models.

If such a sentence cannot be written precisely, the visual encoding is not ready.

## 9. Assessment risk

Before final styling, ask what a skeptical chapter author/reviewer could challenge:

- Does the baseline match the scientific claim?
- Are models and ensemble members conflated?
- Does the map exaggerate resolution?
- Is a robustness threshold arbitrary or undocumented?
- Are scenario labels likely to be interpreted as probabilities?
- Does the color center match the scientific neutral point?
- Does missing data look like zero change?
- Are regional means area weighted?
- Is the interval described with the correct sampling unit?
- Can the plotted-data artifact regenerate the figure exactly?
