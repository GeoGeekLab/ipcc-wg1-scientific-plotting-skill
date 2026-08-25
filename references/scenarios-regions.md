# Scenario, Warming-Level and Region Semantics

Use this reference whenever a figure contains SSP/RCP experiments, Global Warming Levels (GWLs), AR6 reference regions, or policy/geographic aggregation.

## 1. Scenario identity

Preserve canonical labels when they are the actual experiments:

```text
SSP1-1.9
SSP1-2.6
SSP2-4.5
SSP3-7.0
SSP5-8.5
```

Other experiments such as historical, piControl, abrupt-4xCO2, 1pctCO2 or idealized runs must not inherit SSP visual semantics unless explicitly compared.

Rules:

- Do not shorten labels so aggressively that forcing level or pathway identity becomes ambiguous.
- Do not call SSPs forecasts unless the scientific context explicitly defines a forecast product.
- Do not imply equal probability among scenarios.
- Do not convert scenario order into a probability ranking.
- If only a subset of scenarios is shown, state that subset rather than visually implying exhaustiveness.

## 2. Scenario ordering

For forcing-pathway comparisons, a common semantic order is low to high forcing:

```text
SSP1-1.9
SSP1-2.6
SSP2-4.5
SSP3-7.0
SSP5-8.5
```

Use the same order in legends, facets and tables unless the assessment question requires another order.

Do not sort by incidental plotting order, alphabetical order or final-year values unless stated.

## 3. Scenario color identity

Scenario colors are stable identities across a figure set.

Preferred policy:

1. use an official/authorized IPCC/CMIP6 color resource when available and provenance is clear;
2. otherwise choose a perceptually separable ordered palette and record it in the recipe;
3. use line style/marker redundancy for critical categories where grayscale or color-vision accessibility matters.

Never change a scenario's color between panels merely to increase local contrast.

## 4. Historical-to-scenario transition

A figure that joins historical and SSP experiments must define:

- transition year/date;
- whether historical and scenario segments are concatenated or independently processed;
- overlap/duplicate handling;
- whether the historical line is shared before scenario divergence;
- whether uncertainty bands use the same ensemble membership through the transition.

Avoid drawing five differently colored copies of an identical historical trajectory when one shared historical representation is clearer.

## 5. Global Warming Levels

GWL-conditioned analyses require a separate contract from fixed calendar slices.

Record:

```text
warming metric: GMST/GST definition
reference period:
GWL target: 1.5 / 2 / 3 / 4 °C or custom
crossing algorithm:
running-mean/window length:
window around crossing used for local variables:
scenario pooling policy:
non-reaching models/scenarios:
minimum sample count:
```

Rules:

- A `2 °C GWL` value is not synonymous with `2081–2100 under SSPx-y`.
- A model/scenario that never reaches the target GWL within available data is not missing at random; record its exclusion/non-reaching status.
- Sample composition can differ by GWL. Show or save `n_valid`.
- If pooling scenarios at a common GWL, explain the rationale and check whether pathway dependence matters.
- Do not interpolate a GWL response beyond analyzed levels without explicitly modeling that relationship.

## 6. AR6 reference regions

The AR6 WGI Atlas introduced subcontinental reference regions designed for regional climate assessment. The maintained `regionmask` implementation exposes:

```python
regionmask.defined_regions.ar6.all
regionmask.defined_regions.ar6.land
regionmask.defined_regions.ar6.ocean
```

Current regionmask documentation describes 58 regions in `ar6.all`, with land and ocean subsets. Some named areas can occur in both land and ocean categories; preserve the intended domain.

When using them:

- record `regionmask` version;
- record whether `.all`, `.land`, or `.ocean` is used;
- retain canonical abbreviations in plotted data;
- use area-weighted aggregation within the actual region mask;
- document treatment of fractional coastal cells;
- do not redraw approximate polygons by hand for publication analysis.

## 7. Region ordering

Choose one ordering and state it:

- official/canonical region numbering;
- geographic grouping/order;
- latitude/longitude centroid order;
- assessed category;
- estimate ranking.

If ranking by estimate, uncertainty remains visible and the order should not imply statistically distinct ranks where intervals overlap.

Keep region order stable across related panels unless a panel explicitly changes the comparison objective.

## 8. Custom regions

A custom region must have a retraceable geometry.

Record:

```text
name:
geometry source:
version/date:
CRS:
file hash or stable URI/DOI:
land/ocean handling:
aggregation weights:
```

If the region is a political boundary, record the boundary source and avoid presenting it as an IPCC reference region.

## 9. Spatial synthesis and scale

For policy-facing regional plots:

- a locator map may establish geography;
- an aligned point-interval plot usually communicates magnitude differences more precisely than choropleth colors alone;
- a matrix can compare region × variable or region × GWL if scales are compatible;
- do not place tiny labels in every polygon when a structured regional list is clearer.

## 10. Scenario/GWL anti-patterns

Correct these before rendering:

- `SSP1-2.6 = likely future`, `SSP5-8.5 = worst-case probability` without an explicit probabilistic framework;
- using RCP and SSP labels interchangeably;
- mixing a 20-year fixed period with a 20-year GWL window and calling both `mid-century`;
- using different scenario colors in map and time-series panels;
- pooling model realizations differently at each GWL without recording the policy;
- comparing regional values aggregated with different masks/area weighting;
- labeling a custom administrative region as an `IPCC AR6 region`.

## 11. Caption minimum

A scenario/GWL/regional figure caption should state enough to reconstruct the comparison:

```text
experiments/scenarios shown
baseline/reference period
future period or GWL definition
ensemble sampling/weighting
region set/domain
central statistic and interval
sample support/robustness rule where relevant
```

Keep scenario likelihood interpretation out of the caption unless it is genuinely part of the assessment evidence.