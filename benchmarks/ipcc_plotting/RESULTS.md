# Cross-library benchmark result

CI run: https://github.com/GeoGeekLab/ipcc-wg1-scientific-plotting-skill/actions/runs/35832746975  
Benchmark commit: `ffe805d9bebb57ef63554e731f49399b15092c23`  
Artifact digest: `sha256:3aea7dd8406450d85af9badba2c0e413468cc5a41485511bb9bc36c4f21caba5`

Environment: Python 3.12.14, Matplotlib 3.11.2, Xarray 2026.7.0, Figanos 0.7.0.

The workflow also verified all 43 official RGB assets against
`IPCC-WG1/colormaps@b7d3849d4fa521d2583b91360e875e38f191d209`.

## Summary

Figanos remains the stronger general-purpose climate plotting library: broader plot
coverage, deeper Xarray integration, native faceting, automatic scenario colours, and
bundled IPCC colormaps.

ar6-sciplot now adds fixed-size panel grids, uncertainty legends, collision-aware
line-end labels, pinned upstream colour assets, and reference geometry checks to its
AR6/WGI profile and provenance layer.

## Scenario time series

The benchmark uses the ten years populated in all five pinned AR6 Chapter 6 SSP rows:

`2015, 2020, 2030, 2040, 2050, 2060, 2070, 2080, 2090, 2100`.

| Scenario | Figanos 0.7.0 | ar6-sciplot WGI-2022 | ar6-sciplot report-era |
| --- | --- | --- | --- |
| SSP1-1.9 | `#00ADCF` | `#00ADCF` | `#1E9684` |
| SSP1-2.6 | `#173C66` | `#173C66` | `#1D3354` |
| SSP2-4.5 | `#F79420` | `#F79420` | `#EADD3D` |
| SSP3-7.0 | `#E71D25` | `#E71D25` | `#F21111` |
| SSP5-8.5 | `#951B1E` | `#951B1E` | `#840B22` |

Figanos matches the WGI-2022 scenario palette exactly. The report-era profile keeps
the final-report-era colours.

Both renders use line-end labels. Display-space collision detection reports:

- Figanos: `SSP1-1.9` overlaps `SSP1-2.6`;
- ar6-sciplot: no SSP label overlap.

The ar6-sciplot helper moves nearby labels vertically and adds a short connector when
the label leaves the line endpoint.

## Controlled change map + agreement

Both renders use the same 65 x 144 field, low-agreement mask, Robinson projection,
`temp_div` colormap, -4 to +4 level boundaries, and 180 x 100 mm canvas.

Figanos still has the shorter `gridmap() + hatchmap()` path. ar6-sciplot provides
separate agreement hatching and uncertainty legend helpers. The reference audit passes
width, height, panel count, and Robinson projection for the controlled render.

## Warming-level multipanel

Both renders use three Robinson panels on a 180 x 72 mm canvas.

The panel layouts are comparable at final size. Figanos remains simpler at the
data-to-layout step because it facets directly from the Xarray `warming` dimension.
ar6-sciplot handles fixed physical geometry with `map_panel_grid()` and checks the
resulting size, panel count, and projection.

## Official colour assets

`load_ipcc_colormap()` verifies the requested local RGB table before loading it.
The manifest records the Git blob SHA for each official continuous, discrete, and
categorical file at the pinned 2021-06-17 commit.

Verified colormaps carry the source commit and asset blob on the Matplotlib colormap
object. The strict map audit checks that metadata rather than accepting any colormap
whose name merely starts with `ipcc_`.
