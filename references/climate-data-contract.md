# Climate Data Contract

Use this reference whenever the figure depends on climate-model, reanalysis, observational, remote-sensing or gridded Earth-system data. The objective is to make the analytical support of the figure explicit before rendering.

## Required preflight

Record or validate:

```text
variable/index:
standard_name / long_name:
units and sign convention:
data source and version:
experiment/scenario:
model/source identifiers:
member/realization identifiers:
frequency:
calendar:
coverage period:
grid type and nominal resolution:
longitude convention:
cell bounds/area:
mask(s):
missing-value convention:
regridding:
spatial aggregation:
temporal aggregation:
```

## 1. Variable identity and units

- Prefer CF metadata (`standard_name`, `units`, coordinate attributes) over filename inference.
- Verify the sign convention of fluxes, transport, vertical velocity, radiative quantities and anomalies.
- Convert units before statistical aggregation when conversion is linear and valid.
- For nonlinear transformations or derived indices, compute with a documented scientific definition rather than merely relabeling units.
- Preserve original units in provenance even when the plotted unit is converted.
- A percent change must define the denominator and behavior where the baseline is zero or near zero.

## 2. Time and calendars

Climate data may use `standard`, `gregorian`, `proleptic_gregorian`, `noleap`, `all_leap`, `360_day` and other calendars.

Rules:

- Do not coerce model calendars to pandas datetimes merely for convenience.
- Use `cftime`/xarray calendar-aware operations where necessary.
- Verify monthly/seasonal completeness before aggregation.
- Define DJF year convention explicitly; a common convention assigns December to the following January/February year.
- For annual extremes, confirm the index definition and annual boundary.
- If a running mean or smoothing window is used, state centering, window length and edge treatment.
- Historical/scenario concatenation must verify continuity and avoid duplicate transition dates.

## 3. Baselines and anomalies

A baseline is part of the estimand.

Record:

```text
baseline period:
baseline computed per model/source or from common reference:
minimum years required:
seasonal baseline policy:
anomaly type: absolute / standardized / percent / ratio
```

For model anomalies, per-model baselines are often appropriate because models have different climatological biases. Do not switch between per-model and common baselines silently.

## 4. Grids and coordinates

Validate:

- latitude/longitude coordinate identity;
- monotonicity and orientation;
- 0–360 versus -180–180 longitude;
- regular, curvilinear, rotated-pole, cubed-sphere or unstructured grid;
- coordinate bounds;
- cell area if supplied.

Rendering projection is separate from analytical grid. Never calculate regional statistics in screen/projected coordinates unless the method explicitly requires it.

## 5. Area weighting

For regional/global means:

1. prefer supplied cell-area variables such as `areacella` / `areacello` when valid;
2. otherwise derive spherical/ellipsoidal cell area from bounds where feasible;
3. use `cos(lat)` only as a documented approximation for regular latitude-longitude grids.

Weights must be masked consistently with valid data. If a field has varying missingness, normalize weights over valid cells for each aggregation unless the scientific definition requires a fixed denominator.

## 6. Regridding

Regrid only when needed for comparison, aggregation, visualization consistency or a defined workflow.

Record:

```text
source grid:
target grid:
method: conservative / bilinear / nearest / other
periodic longitude:
mask handling:
weight file/version:
```

Guidance:

- extensive quantities and area-integrated fields often require conservative methods;
- smooth intensive fields may support bilinear interpolation;
- categorical masks generally require nearest-neighbor or dedicated categorical treatment;
- conservative regridding requires trustworthy cell bounds;
- never use visual interpolation to claim physical information below source resolution.

If using xESMF, save or hash the weight file when reproducibility matters.

## 7. Masks

Land, ocean, sea-ice, glacier and validity masks are scientific transformations, not cosmetic clipping.

- Record the mask source and threshold.
- Avoid mixing model-specific land masks without defining how common cells are selected.
- For coastal regional means, explain whether fractional land area is used.
- If a region includes both land and ocean but the variable only exists over one surface type, state the effective domain.

## 8. Ensemble identity

For CMIP-like data keep model/source, institution, experiment, member and grid identity distinct.

Do not deduplicate merely by filename. A typical CMIP6 identity includes:

```text
source_id
experiment_id
member_id (r<i>i<p>f<f>)
grid_label
variable_id
frequency/table
version where available
```

Before ensemble statistics, construct an explicit table of included models and realizations.

## 9. Observations and reanalysis

Do not treat observational/reanalysis products as truth without qualification.

Record:

- dataset/product version;
- native resolution and temporal coverage;
- known coverage masks;
- whether uncertainty estimates are provided;
- homogenization/bias correction where relevant;
- whether several products are independent enough to be treated as separate evidence sources.

A spread across observational products is not automatically a calibrated observational uncertainty interval.

## 10. Extremes and derived indices

For ETCCDI/xclim or custom extremes:

- cite the index definition;
- state wet-day thresholds, percentile baseline and bootstrap treatment where applicable;
- verify units before/after resampling;
- preserve calendar-aware event counts;
- do not average a nonlinear extreme index before computing it unless the definition permits this.

## 11. Regional aggregation

For AR6 reference regions use verified geometries, preferably the maintained `regionmask` implementation:

```python
regionmask.defined_regions.ar6.all
regionmask.defined_regions.ar6.land
regionmask.defined_regions.ar6.ocean
```

The current regionmask documentation describes 58 AR6 reference regions in `ar6.all`, with land and ocean subsets. Record the library version and region set used.

For custom regions, save the geometry or stable identifier and its CRS.

## 12. Data-quality failure conditions

Stop or explicitly flag the analysis when:

- units are unknown or contradictory;
- required baseline/target coverage is insufficient;
- time duplicates or calendar conversion change the sample silently;
- model identities cannot be reconstructed;
- grid coordinates are malformed;
- regridding method is incompatible with the variable;
- regional masks cannot be verified;
- valid sample size is too small for the stated uncertainty/robustness rule.

Do not repair these conditions purely in the plotting layer.