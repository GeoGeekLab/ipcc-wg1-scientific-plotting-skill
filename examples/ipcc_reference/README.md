# IPCC AR6 WGI source-data reference reproductions

These examples are fidelity tests built from **pinned official IPCC AR6 WGI source repositories**.

They are not synthetic demos. Each script fetches the upstream source data from a fixed Git commit and rebuilds a distinct figure family.

| Output | Figure family | Official source |
| --- | --- | --- |
| `ch03_fig3_2b_scatter.png` | scatter + fitted relationship | IPCC-WG1/Chapter-3_Fig02b |
| `ch02_fig2_3_co2_proxy.png` | multi-panel proxy + uncertainty | IPCC-WG1/Chapter-2_Fig03 |
| `ch10_fig10_20b_stations.png` | projected station map | IPCC WGI Chapter 10 ESMValTool source |
| `ch06_fig6_18_ch4_emissions.png` | historical + scenario time series | IPCC-WG1/Chapter-6_Fig18 |

## Run

```bash
python -m pip install -e .
python -m pip install cartopy
python examples/ipcc_reference/generate_all.py
```

Network access is required because the examples deliberately fetch source data from the pinned upstream repositories instead of vendoring copies.

## Fidelity boundary

The reference data, physical figure dimensions, palette semantics and figure-specific plotting grammar are reproduced from the official source.

Arial is **not redistributed**. In CI, Matplotlib uses the repository's documented sans-serif fallback if Arial is unavailable. Therefore CI artifacts are source-faithful regression references but should not be described as strict typographic reproductions unless Arial is installed locally.

Generated outputs are validated at IPCC delivery width/height and 350 ppi.
