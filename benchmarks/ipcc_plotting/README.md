# Cross-library IPCC plotting benchmark

This benchmark compares `ar6-sciplot` with other projects that have distilled parts of IPCC climate-figure practice.

The first executable comparison is intentionally focused on **Figanos**, because it is the strongest direct Python comparator we found: it is a mature Xarray-aware climate plotting library with time series, maps, hatching, automatic IPCC variable/scenario colours, faceting, and several plot families that `ar6-sciplot` does not currently provide.

## What this benchmark is — and is not

It is not a scorecard and it does not declare an overall winner. The projects optimize for different goals:

- **Figanos** is currently the stronger general-purpose climate plotting library. It has broader plot coverage, deeper Xarray integration, automatic faceting, convenient ensemble handling, and bundled/registered IPCC colour assets.
- **ar6-sciplot** is intentionally narrower. Its differentiator is evidence-backed AR6/WGI profiles, physical delivery constraints, provenance, and machine-checkable fidelity rules.
- A plot looking closer to an IPCC figure does not prove that its underlying science is correct.
- A fidelity audit does not replace reference-specific review of projection, panel geometry, levels, annotations, or scientific method.

The benchmark therefore separates **native usability** from **controlled fidelity**.

## Pinned comparator

The executable benchmark pins:

- Figanos: `0.7.0`
- ar6-sciplot: the commit under test
- AR6 time-series source: `IPCC-WG1/Chapter-6_Fig18` at commit
  `09d9b43fe935fc81d828147f91b717396a84fca3`
- source file: `ar6-wg1-ch6-emissions-global-data.csv` (Git blob `07162ad5f315cbcfd49bd672f6180c67ad6fc7b3`)

## Three benchmark archetypes

### 1. Scenario time series

Both libraries receive the same official AR6 Chapter 6 methane-emission scenario rows.

This test is deliberately expected to expose a real semantic difference:

- Figanos 0.7.0 follows the updated IPCC WGI scenario colours used by its current categorical colour registry.
- `ar6-sciplot(profile="wgi-guide-2022")` should converge on those colours.
- `ar6-sciplot(profile="ar6-report")` intentionally retains final-report-era SSP colours where they differ.

That difference is not treated as an error in Figanos.

### 2. Global change map + model-agreement texture

A deterministic synthetic global field is used so that both libraries receive exactly the same raster and the same low-agreement mask.

For this benchmark, both renderers share Figanos' registered `temp_div` IPCC colormap and the same Robinson projection and level boundaries. This deliberately removes palette and projection as confounders. The test then exposes differences in map API, hatching, colour-bar treatment, physical geometry, and auditability.

Using Figanos' registered colour asset here is intentional: automatic bundled registration is a genuine Figanos strength.

### 3. Three-panel warming-level map

Both libraries receive the same three-dimensional Xarray object for +1.5, +2 and +4 °C warming levels.

This test makes a major Figanos advantage visible: it can construct Xarray facet maps directly. `ar6-sciplot` currently needs explicit Matplotlib/Cartopy panel construction, although it provides the publication tokens and panel helpers.

## Outputs

Running:

```bash
python benchmarks/ipcc_plotting/benchmark.py
```

creates `benchmarks/ipcc_plotting/out/` containing PNG renders, `results.json`, and `RESULTS.md`.

The GitHub Actions workflow `.github/workflows/plotting-benchmark.yml` runs the same benchmark in a clean Python 3.12 environment and uploads the output directory as an artifact.

## Comparator inventory

The broader inventory is tracked in `competitors.yaml`. Only projects marked `native_runtime: true` should be used for direct executable claims. R-based or workflow-specific projects are kept in the inventory but must not be presented as if their native renderer was executed by this Python benchmark.
