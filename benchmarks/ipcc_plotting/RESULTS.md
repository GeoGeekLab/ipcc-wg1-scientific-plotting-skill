# Cross-library benchmark result

CI run: https://github.com/GeoGeekLab/ipcc-wg1-scientific-plotting-skill/actions/runs/35830722862  
Benchmark commit: `2b2e2d2a0a839f22a7060633cd93d12df004d8f9`  
Artifact digest: `sha256:877920f323472faa1a5c345ffb9a2a4e9a376883b7d199a8bbfeb0ba99f4f4b0`

Environment: Python 3.12.14, Matplotlib 3.11.2, Xarray 2026.7.0, Figanos 0.7.0.

## Summary

Figanos remains the stronger general-purpose climate plotting library: broader plot coverage, deeper Xarray integration, native faceting, automatic scenario colours, and bundled IPCC colormaps.

ar6-sciplot focuses on AR6/WGI profile versioning, print geometry, provenance, uncertainty semantics, and figure checks. This iteration adds fixed-size panel grids, uncertainty legends, and reference geometry checks.

## Scenario time series

The benchmark uses the common populated years in the pinned AR6 Chapter 6 source rows:

`2015, 2020, 2030, 2040, 2050, 2060, 2070, 2080, 2090, 2100`.

| Scenario | Figanos 0.7.0 | ar6-sciplot WGI-2022 | ar6-sciplot report-era |
| --- | --- | --- | --- |
| SSP1-1.9 | `#00ADCF` | `#00ADCF` | `#1E9684` |
| SSP1-2.6 | `#173C66` | `#173C66` | `#1D3354` |
| SSP2-4.5 | `#F79420` | `#F79420` | `#EADD3D` |
| SSP3-7.0 | `#E71D25` | `#E71D25` | `#F21111` |
| SSP5-8.5 | `#951B1E` | `#951B1E` | `#840B22` |

Figanos matches the WGI-2022 scenario palette exactly. The report-era profile keeps the colours used by final-report-era material.

Figanos' edge labels save plotting space, but SSP1-1.9 and SSP1-2.6 overlap at the 2100 endpoint in this dataset. The ar6-report render uses a boxed legend.

## Controlled change map + agreement

Both renders use the same 65 x 144 field, low-agreement mask, Robinson projection, `temp_div` colormap, -4 to +4 level boundaries, and 180 x 100 mm canvas.

Figanos still has the shorter `gridmap() + hatchmap()` path. ar6-sciplot now provides the agreement hatch and matching legend through dedicated helpers. The reference audit passes width, height, panel count, and Robinson projection for the controlled render.

## Warming-level multipanel

Both renders use three Robinson panels on a 180 x 72 mm canvas.

The panel layouts are now comparable at final size. Figanos remains simpler at the data-to-layout step because it facets directly from the Xarray `warming` dimension. ar6-sciplot now handles the physical panel grid with `map_panel_grid()` and checks the resulting size, panel count, and projection.

## Current split

Use Figanos for broad climate-plotting coverage and Xarray-native plotting workflows.

ar6-sciplot adds AR6/WGI profile selection, report-era semantics, fixed print geometry, uncertainty-specific encodings, provenance, and reference-aware checks.
