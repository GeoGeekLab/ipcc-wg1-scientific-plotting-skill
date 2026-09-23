# Cross-library IPCC plotting benchmark

This benchmark compares `ar6-sciplot` with libraries that have distilled parts of IPCC climate-figure practice.

The executable comparator is **Figanos 0.7.0**. It is the strongest direct Python comparison here: a mature Xarray-aware plotting library with time series, maps, hatching, automatic scenario colours, faceting, and a wider set of climate-plot types.

## Method

The benchmark has two views of each library:

- **native**: use the library's normal high-level API and defaults where practical;
- **controlled**: hold data, projection, levels, physical figure size, and palette constant.

Three plot families are exercised.

### Scenario time series

Both libraries receive the same official AR6 WGI Chapter 6 methane-emission scenario rows.

Figanos follows its current WGI scenario-colour registry. `ar6-sciplot` renders both the `wgi-guide-2022` and `ar6-report` profiles so the palette-version difference is visible.

### Global change map + model agreement

Both libraries receive the same deterministic 65 × 144 field and the same low-agreement mask.

The controlled map uses:

- Robinson projection;
- identical level boundaries;
- 180 × 100 mm output;
- the same `temp_div` colormap object registered by Figanos.

This isolates map construction, hatching, legends, layout, and audit behavior.

### Three-panel warming-level map

Both libraries receive the same Xarray field at +1.5, +2, and +4 °C warming levels.

Figanos uses native Xarray faceting. `ar6-sciplot` uses its fixed-size panel-grid helper with the same 180 × 72 mm target.

## Pinned inputs

- Figanos: `0.7.0`
- ar6-sciplot: commit under test
- AR6 source repository: `IPCC-WG1/Chapter-6_Fig18`
- source commit: `09d9b43fe935fc81d828147f91b717396a84fca3`
- source file: `ar6-wg1-ch6-emissions-global-data.csv`
- source Git blob: `07162ad5f315cbcfd49bd672f6180c67ad6fc7b3`

## Current comparison

Figanos is ahead on general plotting breadth and Xarray-native ergonomics. Its automatic scenario colours, bundled IPCC colormaps, facet maps, and `gridmap() + hatchmap()` workflow reduce setup code substantially.

ar6-sciplot concentrates on profile-specific AR6/WGI rendering: report-era versus 2022 tokens, physical delivery geometry, provenance, uncertainty encodings, and reference-aware figure checks.

## Run

```bash
python benchmarks/ipcc_plotting/benchmark.py
```

Outputs are written to `benchmarks/ipcc_plotting/out/`:

- PNG renders;
- `results.json`;
- generated `RESULTS.md`.

The workflow `.github/workflows/plotting-benchmark.yml` runs the same benchmark in Python 3.12 and uploads the output directory.

## Comparator inventory

`competitors.yaml` tracks the wider repository set. Projects marked `native_runtime: true` are executed directly by this benchmark; the others remain source/output comparisons.
