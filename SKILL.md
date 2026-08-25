---
name: ipcc-native-plot
description: >-
  IPCC-native climate-assessment figure workflow for Python/xarray/Matplotlib/Cartopy. Use for climate, Earth-system, CMIP, observations/reanalysis, impacts, extremes, regional assessment, uncertainty, scenario and warming-level figures, especially when the user asks for IPCC-quality, assessment-report, policy-facing, or publication-grade plots. Start from an assessment intent and evidence chain, then define the climate estimand, ensemble policy, uncertainty/robustness semantics, spatial/temporal frame, and audience before plotting. Produces reproducible plotted-data artifacts, vector/raster outputs, provenance, and QA notes. This is an independent workflow distilled from public IPCC AR6 WGI practices; it is not an official IPCC product and does not imply IPCC endorsement.
---

# IPCC-native Plot Skill

This skill produces climate-assessment figures as **auditable scientific arguments**, not as decorative charts. The target is the discipline of IPCC-class assessment graphics: explicit estimands, controlled aggregation, transparent uncertainty, consistent scenario semantics, defensible maps, legible multi-panel evidence chains, and FAIR/reproducible delivery.

The current public visual baseline is **IPCC AR6 WGI**. AR7 is underway; before claiming conformance to a current IPCC visual or authoring rule, verify the newest official IPCC guidance. Never present this skill as an official IPCC standard.

## First move: assessment contract before plotting

Before code or styling, establish the assessment contract. If information is missing, infer conservative provisional choices and expose them; do not hide them inside plotting code.

```text
Assessment intent: one sentence stating what the reader should conclude
Audience: chapter author / technical expert / policymaker / public-facing assessment
Evidence role: headline / primary evidence / mechanism / regional detail / robustness / context
Scientific question:
Estimand:
Data sources:
Temporal frame: baseline, target period, season, warming level if applicable
Spatial frame: global / AR6 reference region / custom region / grid
Ensemble policy: model identity, realization policy, weighting, independence assumptions
Uncertainty: what interval/range means and what its sampling unit is
Robustness: exact classification rule and thresholds
Scenario semantics: SSP/RCP/GWL labels and ordering
Figure archetype:
Plotted-data artifact:
Export/QA contract:
Reviewer/assessment risk:
```

Read `references/assessment-contract.md` when translating a scientific request into this contract.

## Non-negotiable scientific rules

1. **Define the estimand before the visual form.** A map of “change” is invalid until baseline, target period, statistic, units, aggregation, and ensemble unit are explicit.
2. **Separate analysis from rendering.** Raw data → harmonized data → analytical result → plotted-data artifact → figure. Plotting functions must not silently change the scientific result.
3. **Models are not automatically independent replicates.** Multiple ensemble members must not be counted as independent models merely to increase `n` or narrow uncertainty.
4. **Calendar, units, grid, masks and missingness are first-class data.** Never infer them only from filenames or plotting defaults.
5. **Area-weight spatial aggregation.** Use true cell area when available. `cos(lat)` is only a documented approximation for regular latitude-longitude grids.
6. **Do not manufacture resolution.** Regridding or interpolation must never visually imply information finer than the source supports.
7. **Uncertainty is semantic, not ornamental.** Every band, whisker, hatch, stipple, opacity or blank region must have one defined meaning.
8. **Robustness classes must be mutually exclusive and exhaustive over valid data.** A reader should never have to guess why one location is hatched, blank or unmarked.
9. **Color encodes the primary scientific quantity. Texture/marker shape encodes secondary evidence status.** Do not overload hue, texture and opacity with competing meanings.
10. **Every final figure ships with plotted data and provenance.** A figure without retraceable plotted data is incomplete.

## Figure archetypes

Classify the figure before implementation. Open `references/ipcc-archetypes.md` for detailed panel logic and design rules.

| Archetype | Best use | Typical evidence structure |
|---|---|---|
| `assessment-map` | Spatial change, climatology, extremes, exposure | central estimate + robustness/sample support |
| `scenario-timeseries` | Historical + future evolution | observations/reanalysis + ensemble center + ranges + scenarios |
| `warming-level-response` | Compare impacts at 1.5/2/3/4 °C | aligned regional/global responses with common baseline |
| `regional-synthesis` | AR6 reference regions or policy regions | compact map/index + regional ranked/interval panels |
| `ensemble-distribution` | Model spread, observational constraint | raw/model distribution + center + interval + sample count |
| `emergence-or-threshold` | ToE, exceedance, threshold crossing | threshold definition + timing/risk distribution |
| `evidence-matrix` | Multi-variable or multi-region synthesis | small multiples with identical scales and semantics |
| `assessment-composite` | SPM/TS/chapter figure | one headline panel + subordinate evidence + restrained annotations |

Avoid defaulting to equal-sized subplot grids. Give the primary assessment statement the clearest visual hierarchy.

## Climate data contract

Use `xarray` as the default labeled-array model. For large data prefer Dask/Zarr. Use CF metadata where possible.

Before analysis validate:

- variable meaning, units and sign convention;
- dimension names and coordinate monotonicity;
- longitude convention and wrap;
- calendar (`standard`, `noleap`, `360_day`, etc.);
- frequency and completeness of baseline/target periods;
- missing/fill values and duplicate timestamps;
- grid type, bounds and cell area;
- land/ocean/ice masks;
- model/source/experiment/member identity;
- whether sample count varies by grid cell;
- whether regridding is scientifically necessary.

Read `references/climate-data-contract.md` for CMIP/reanalysis/observation conventions and anti-patterns.

## Ensemble and uncertainty semantics

Default climate-ensemble behavior is conservative:

- Prefer one clearly declared sampling unit, usually model, not realization.
- If using multiple realizations per model, first aggregate within model unless the study design justifies another hierarchy.
- State whether the center is mean or median.
- State interval endpoints exactly (for example 17–83% model range or 5–95% range).
- Distinguish **ensemble spread**, **confidence interval**, **observational uncertainty**, and **internal variability**. Never call all of them “error”.
- Report `n_valid` when availability varies spatially or across periods.
- If model weighting, performance weighting, independence weighting, emergent constraints, or Bayesian weighting are used, show and record the method explicitly.

Use `scripts/ipcc_sciplot/uncertainty.py` for reproducible summaries; do not substitute a visual convention for a statistical definition.

## Robustness and significance

Read `references/uncertainty-robustness.md` before using stippling or hatching.

Default semantics for climate-change maps:

- **base color**: central estimate/change;
- **no texture**: primary result is considered robust under the declared rule;
- **hatching**: evidence fails the declared agreement/robustness criterion but still has adequate sample support;
- **neutral gray / explicit mask**: insufficient valid data;
- **stippling**: use only when it specifically denotes a statistical significance or confidence criterion that is defined in the caption/metadata.

Never claim a universal “IPCC threshold”. Thresholds depend on the scientific question and source methodology. A value such as sign agreement ≥0.80 is a recipe default only when explicitly chosen and justified.

For field significance or many grid-cell tests, do not present naive pointwise p<0.05 as global evidence. Consider dependence, effective sample size, FDR/field significance, or an assessment-specific robustness framework.

## Scenario, warming-level and regional semantics

Read `references/scenarios-regions.md` when the figure includes SSP/RCP, Global Warming Levels, or AR6 regions.

Rules:

- Preserve canonical scenario labels (`SSP1-2.6`, `SSP2-4.5`, `SSP3-7.0`, `SSP5-8.5`) when those are the actual experiments.
- Do not imply equal probability among scenarios unless the analysis explicitly establishes probabilities.
- Keep scenario colors/line identities stable across all panels in a figure set.
- Treat GWL analysis as a different temporal framing from fixed time slices; state the warming-level definition and window.
- For regional assessment, prefer published AR6 reference regions through `regionmask.defined_regions.ar6` or verified official region geometries rather than hand-drawn boundaries.
- Distinguish land and ocean reference regions when relevant.

## Visual encoding

### Maps

- Use Cartopy or equivalent geospatial axes with an explicit data CRS and map projection.
- Choose projection for the scientific task, not for decoration. Global assessment maps usually need a projection with acceptable global-area/shape tradeoffs; regional plots should minimize distortion over the region of interest.
- Do not draw coastlines/borders thicker than the data need.
- Avoid dense graticules unless geographic coordinates are part of the argument.
- Use `BoundaryNorm` or a declared continuous normalization with explicit breakpoints.
- A zero-centered change field normally requires a diverging color scale centered at the scientifically meaningful neutral value.
- A strictly positive magnitude generally requires a sequential scale.
- Missing data must not share a color with a scientific value.
- Avoid rainbow/jet.

### Time series

- Use a visually dominant central estimate and quieter uncertainty envelopes.
- Separate historical/observational and scenario periods clearly when their epistemic status differs.
- Do not draw every model as an equally salient line in a policy-facing figure unless individual-model structure is itself the evidence.
- If individual members are shown, use thin/light lines behind the summary.
- Direct-label stable scenario lines where practical.

### Distributions and regional comparisons

- Prefer points/intervals, ECDF, box/violin plus raw/summary information over mean-only bars.
- Show sample count where model/source availability differs.
- Align scales across panels that invite direct comparison.

### Multi-panel assessment figures

- One panel should carry the headline evidence whenever possible.
- Reuse units, scenario colors, baseline wording, map projection, region ordering and uncertainty semantics across panels.
- Panel labels `(a)`, `(b)`, … are fixed and unobtrusive.
- Captions must define the scientific transformation, not merely describe the geometry.

## Color policy

Prefer, in order:

1. official/authorized IPCC AR6 colormap files when the user has them available locally;
2. perceptually uniform scientific colormaps (`cmocean`, `cmcrameri`/Scientific Colour Maps, suitable Matplotlib maps);
3. a custom palette only when its perceptual and semantic behavior is checked.

The public `IPCC-WG1/colormaps` repository contains continuous, discrete, categorical and CMIP6 color resources. Do not redistribute upstream files if licensing/provenance is uncertain; load authorized local copies and record their source/version.

Scenario colors are semantic identities, not decoration. Never reorder the legend by incidental plotting order.

## Layout and typography

Use conservative publication/report defaults unless a specific IPCC production template is supplied:

- final width based on the target document rather than arbitrary screen pixels;
- legible text at final rendered size (commonly around 7–9 pt for dense report graphics);
- sans-serif fonts with reliable Unicode/scientific-symbol coverage;
- no chart junk, drop shadows, faux-3D, heavy boxes or decorative gradients;
- thin axes/coastlines; stronger marks reserved for the result;
- direct annotations should explain the assessment message, threshold or event, not narrate obvious axes;
- export PDF/SVG for vector structure where possible; rasterize only dense layers;
- include a 300 dpi PNG preview for review.

Do not copy Nature-specific 89/183 mm widths as an IPCC requirement. Those values are journal conventions, not native IPCC report specifications.

## IPCC-native recipe

Use `templates/ipcc_native_recipe.yaml` as the preferred declarative contract. A valid recipe must define assessment intent, estimand, temporal/spatial frame, ensemble policy, uncertainty/robustness semantics, color meaning and export/provenance targets.

The older `templates/figure_recipe.yaml` remains supported for backward compatibility.

## FAIR and reproducibility contract

A completed figure bundle should contain, where applicable:

```text
figure_XX.pdf                 # vector primary
figure_XX.svg                 # editable vector when appropriate
figure_XX.png                 # review preview
figure_XX_plotted_data.nc     # exact plotted numerical fields
figure_XX_provenance.json     # inputs, hashes, params, environment, git state
figure_XX_recipe.yaml         # declarative scientific/visual contract
figure_XX_qa.md               # checks, assumptions, known limitations
```

The AR6 WGI Atlas explicitly emphasizes traceability, reproducibility, reusable products, reference grids, reference regions, warming levels, reproducibility scripts and environment capture. This skill treats those as core figure-production requirements, not optional extras.

## Quality assurance

Before delivery, read `references/qa-contract.md` and verify at minimum:

### Scientific QA
- estimand matches code and caption;
- units and baseline are correct;
- time/calendar handling is explicit;
- ensemble sample unit and weighting are correct;
- uncertainty definition matches plotted interval/texture;
- `n_valid` handling matches the robustness mask;
- area weighting/regridding/masking are documented;
- scenario/GWL labels are not misleading.

### Visual QA
- color scale matches variable semantics;
- zero/reference value is visually correct;
- no clipped labels/colorbars;
- no false precision from interpolation;
- hatch/stipple density remains legible at final size;
- missing data are visually distinct;
- panel scales/legends are consistent;
- grayscale/color-vision interpretation remains adequate for critical categories.

### Reproducibility QA
- plotted-data artifact can regenerate the figure without raw-data analysis;
- recipe and provenance sidecars exist;
- random seeds are fixed where stochastic methods are used;
- source file hashes or stable identifiers are recorded;
- environment and Git revision are captured.

## Required corrections / refusal to misrepresent

Correct or flag these practices rather than silently producing them:

- rainbow/jet for continuous climate fields;
- treating ensemble members as independent models to inflate sample size;
- calling ensemble spread a confidence interval without justification;
- hiding low agreement or low sample support behind smooth interpolation;
- using a diverging palette whose center is not the scientific neutral value;
- using scenario colors inconsistently across panels;
- presenting SSPs as probabilistic forecasts without probability evidence;
- pointwise significance stippling over thousands of cells without multiplicity/dependence consideration;
- hand-drawn “IPCC regions” when official/reference geometries are available;
- non-area-weighted global/regional means on latitude-longitude grids without justification;
- figure-only delivery with no plotted data/provenance for reproducible assessment work;
- claiming “IPCC compliant” based solely on visual similarity.

## Related files

| File | Open when |
|---|---|
| `references/assessment-contract.md` | Convert a request into assessment intent, evidence hierarchy and risks |
| `references/ipcc-archetypes.md` | Choose map/timeseries/GWL/regional/composite figure architecture |
| `references/climate-data-contract.md` | Validate CMIP, observations, reanalysis, calendars, grids, units and masks |
| `references/uncertainty-robustness.md` | Define intervals, agreement, significance, hatching and stippling |
| `references/scenarios-regions.md` | SSP/RCP, GWL and AR6 regional semantics |
| `references/qa-contract.md` | Final scientific, visual and FAIR audit |
| `references/ipcc_wg1_distillation.md` | Existing upstream AR6 repository distillation |
| `references/SOURCES.md` | Upstream source inventory |
| `scripts/ipcc_sciplot/` | Reusable Python helpers |
| `templates/ipcc_native_recipe.yaml` | Preferred IPCC-native recipe |
| `templates/figure_recipe.yaml` | Legacy compact recipe |
