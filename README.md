# IPCC-native Plot Skill

An independent Agent Skill and Python toolkit for **IPCC-class climate-assessment visualization**: assessment intent, climate estimands, ensemble semantics, uncertainty/robustness, scenario/GWL/region consistency, cartographic discipline, FAIR plotted-data delivery and reproducible QA.

> [!IMPORTANT]
> This is not an official IPCC product and does not imply IPCC endorsement. The current public baseline used by this project is IPCC AR6 WGI. AR7 is underway; verify new official guidance before claiming current IPCC conformance.

## Why this is different from an “IPCC style” theme

The Skill does not define quality as matching colors or fonts. It enforces a production chain:

```text
Assessment intent
→ evidence chain
→ climate estimand
→ data/calendar/grid contract
→ ensemble sampling policy
→ uncertainty & robustness semantics
→ scenario/GWL/region semantics
→ figure archetype
→ visual encoding
→ plotted-data artifact
→ PDF/SVG/PNG + provenance + QA
```

The core `SKILL.md` follows a contract-first method inspired by high-end scientific figure skills, but the scientific/visual rules are independently derived from public IPCC AR6 WGI resources and climate-data practice.

## Capabilities

- assessment-map, scenario-time-series, warming-level, regional-synthesis, ensemble-distribution, emergence/threshold, evidence-matrix and assessment-composite archetypes;
- model-equal ensemble summaries with explicit quantile ranges;
- cell-specific valid-model counts and sign-agreement diagnostics;
- configurable mutually exclusive robustness classes;
- Benjamini–Hochberg FDR helper;
- area-aware spatial aggregation;
- Cartopy-compatible hatching and insufficient-data masks;
- canonical CMIP6 SSP labels/order without implying scenario probability;
- xarray climate-data preflight for units, coordinates, calendars, duplicates and longitude conventions;
- local loading of authorized IPCC RGB colormap resources;
- report-size Matplotlib context, declarative normalization and panel labels;
- nested IPCC-native YAML recipe with validation;
- exact plotted-data NetCDF, input/environment/Git provenance and QA notes;
- tests and synthetic end-to-end examples.

## Install as an Agent Skill

Clone the repository into the skill directory used by your Agent, for example:

```bash
git clone https://github.com/GeoGeekLab/ipcc-wg1-scientific-plotting-skill \
  ~/.claude/skills/ipcc-native-plot
```

For Codex, use the corresponding skills directory, e.g. `~/.codex/skills/ipcc-native-plot`.

The skill entry point is [`SKILL.md`](SKILL.md).

## Python installation

Python 3.11+:

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
python -m pip install -e ".[qa]"
```

Climate/geospatial stack:

```bash
python -m pip install -e ".[climate,qa,workflow]"
```

## Start from the IPCC-native recipe

Use [`templates/ipcc_native_recipe.yaml`](templates/ipcc_native_recipe.yaml). It records:

- assessment intent and audience;
- question/estimand/variable/unit;
- baseline, target period or GWL;
- spatial domain, region set and regridding;
- ensemble sampling/realization/weighting policy;
- uncertainty quantiles and robustness thresholds;
- scenario identities and ordering;
- colormap/normalization/projection semantics;
- caption decoding;
- output/plotted-data/provenance/QA paths.

Validate it in Python:

```python
from ipcc_sciplot import load_ipcc_native_recipe

recipe = load_ipcc_native_recipe("templates/ipcc_native_recipe.yaml")
print(recipe.assessment["intent"])
```

The older [`templates/figure_recipe.yaml`](templates/figure_recipe.yaml) and `load_recipe()` remain available for backward compatibility.

## Minimal scientific API

```python
import xarray as xr

from ipcc_sciplot import ensemble_summary, classify_robustness

ensemble = xr.open_dataarray("model_level_change.nc")

summary = ensemble_summary(
    ensemble,
    dim="model",
    center="median",
    lower_q=0.17,
    upper_q=0.83,
    sign_agreement=0.80,
    min_count=5,
)

classes = classify_robustness(
    n_valid=summary["n_valid"],
    agreement=summary["sign_agreement"],
    min_count=5,
    agreement_threshold=0.80,
)
```

`0.80` and `5` are example recipe parameters, not universal IPCC thresholds.

## Climate-data preflight

```python
from ipcc_sciplot import inspect_climate_data, normalize_longitude

report = inspect_climate_data(da, expected_unit="K")
if report.warnings:
    print(report.warnings)

da = normalize_longitude(da, convention="-180..180")
```

The Skill expects calendar, units, masks, grid and ensemble identity to be handled as scientific data, not as plotting convenience.

## End-to-end synthetic demo

The original compact demo remains:

```bash
python examples/quickstart.py
```

The IPCC-native assessment-map demo requires the climate extras:

```bash
python examples/ipcc_native_workflow.py
```

It demonstrates central estimate + model sign agreement + insufficient sample support and writes figure, plotted NetCDF, recipe copy, provenance and QA notes. The example uses synthetic data and is not a climate projection.

## Reference modules

| Reference | Purpose |
|---|---|
| `references/assessment-contract.md` | intent, evidence hierarchy, estimand and reviewer risk |
| `references/ipcc-archetypes.md` | map/time-series/GWL/regional/distribution/composite architectures |
| `references/climate-data-contract.md` | units, calendars, grids, masks, regridding and ensemble identity |
| `references/uncertainty-robustness.md` | ensemble spread, confidence, agreement, significance, texture semantics |
| `references/scenarios-regions.md` | SSP/RCP, GWL and AR6 reference-region semantics |
| `references/visual-style.md` | hierarchy, annotation, color, layout and caption communication |
| `references/qa-contract.md` | final scientific, visual and FAIR audit |
| `references/ipcc_wg1_distillation.md` | earlier AR6 code/repository distillation |
| `references/statistical_rules.md` | compact statistical rules |
| `references/visual_encoding.md` | compact encoding notes |
| `references/SOURCES.md` | public source map and reuse notes |

## Python modules

```text
scripts/ipcc_sciplot/
├── maps.py          # area weighting, robustness masks, hatch/missing overlays
├── provenance.py    # hashes, environment, Git state, sidecar provenance
├── recipe.py        # legacy + nested IPCC-native recipe validation
├── scenarios.py     # canonical SSP labels/order
├── style.py         # assessment context, normalizations, colormaps, export
├── uncertainty.py   # ensemble summaries and FDR
└── validation.py    # climate-data preflight and longitude normalization
```

## Expected figure bundle

For assessment-grade work, aim to deliver:

```text
figure_XX.pdf
figure_XX.svg
figure_XX.png
figure_XX_plotted_data.nc
figure_XX_provenance.json
figure_XX_recipe.yaml
figure_XX_qa.md
```

The plotted-data artifact should be sufficient to redraw the figure without repeating raw-data analysis.

## Validation

```bash
pytest -q

python scripts/check_figure.py \
  outputs/quickstart.pdf \
  --metadata outputs/quickstart.provenance.json
```

For mature assessment projects, add image-regression tests, recipe-schema checks, deterministic data hashes, color-vision checks and tests tying caption thresholds to code parameters.

## Source basis

The public source inventory is in [`references/SOURCES.md`](references/SOURCES.md). Major inputs include the IPCC AR6 WGI Visual Style Guide, AR6 WGI Atlas reproducibility repository, IPCC-WG1 chapter figure repositories, AR6 colormap resources and AR6 reference-region ecosystem.

## Scope boundary

This repository can enforce reproducible climate-figure discipline, but it cannot turn arbitrary model output into an IPCC assessment conclusion. Calibrated IPCC confidence/likelihood language, scenario interpretation, ensemble weighting and assessment judgments require scientific justification and source attribution.