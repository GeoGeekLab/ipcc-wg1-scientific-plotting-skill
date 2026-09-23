# Cross-library benchmark — CI result

Run: https://github.com/GeoGeekLab/ipcc-wg1-scientific-plotting-skill/actions/runs/35822060746

Artifact: `ipcc-plotting-benchmark`  
Artifact digest: `sha256:0ffa6bf3883277f5b2f830e8417362e0ca2c3f30db0299b902ceb1e126fe997e`

Environment:

- Python 3.12.14
- Matplotlib 3.11.2
- Xarray 2026.7.0
- Figanos 0.7.0
- ar6-sciplot commit under test: `73272f5df9f25303d5f1bdcfdcca2cc452d1ea4f`

The native benchmark completed successfully. Seven PNG renders plus machine-readable results were uploaded by CI.

## Result that should be stated plainly

**Figanos is currently the stronger general-purpose climate plotting library.**

That is visible both in its API and in this benchmark. It has broader plot coverage, deeper Xarray integration, native facet construction, automatic scenario-colour recognition, automatically registered IPCC colormaps, and a more complete map/hatching workflow. ar6-sciplot should not claim to beat Figanos on plotting breadth or convenience.

The defensible distinction for ar6-sciplot is narrower: explicit AR6 report-era versus WGI-2022 profiles, physical IPCC delivery geometry, evidence/provenance, separation of uncertainty semantics, and machine-checkable fidelity diagnostics.

## 1. Scenario time series

The benchmark uses official AR6 WGI Chapter 6 Figure 6.18 methane-emission source data pinned to commit `09d9b43fe935fc81d828147f91b717396a84fca3`.

Figanos 0.7.0 automatically produced these SSP colours:

| Scenario | Figanos 0.7.0 | ar6-sciplot WGI-2022 | ar6-sciplot report-era |
| --- | --- | --- | --- |
| SSP1-1.9 | `#00ADCF` | `#00ADCF` | `#1E9684` |
| SSP1-2.6 | `#173C66` | `#173C66` | `#1D3354` |
| SSP2-4.5 | `#F79420` | `#F79420` | `#EADD3D` |
| SSP3-7.0 | `#E71D25` | `#E71D25` | `#F21111` |
| SSP5-8.5 | `#951B1E` | `#951B1E` | `#840B22` |

So Figanos matches the updated WGI-2022 profile exactly in this test. Its mismatch with the report-era palette is **not a defect**; it reflects a different target profile.

The native Figanos figure was 162.56 × 121.92 mm. The ar6-sciplot report render was explicitly constrained to 180 × 100 mm.

Visual inspection also shows a practical Figanos advantage: its edge/direct scenario labels use plotting space efficiently, whereas the current ar6-sciplot example uses a conventional boxed legend.

## 2. Controlled change map + low agreement

To avoid a biased comparison, both renderers were forced to use:

- the same deterministic 65 × 144 field;
- the same low-agreement mask;
- the same Robinson projection;
- the same `temp_div` colormap object registered by Figanos;
- the same level boundaries from -4 to +4;
- the same 180 × 100 mm figure size.

Under those controls, Figanos' `gridmap() + hatchmap()` route is materially more concise and more turnkey. It also creates the hatching legend directly.

The current ar6-sciplot route needs explicit Matplotlib/Cartopy construction and does not yet provide an equally convenient legend abstraction for the uncertainty texture. Its advantage is semantic separation: low agreement, insufficient data, and statistical significance are different helpers rather than interchangeable pattern layers.

The benchmark deliberately uses Figanos' registered IPCC colormap for both sides. This gives Figanos full credit for a real usability advantage: official colour assets are bundled and registered automatically.

## 3. Three warming-level panels

Both outputs were constrained to 180 × 72 mm and three Robinson panels.

Figanos creates the panels directly from the Xarray `warming` dimension. This is a **clear Figanos advantage**.

ar6-sciplot currently has no equivalent native facet abstraction; the benchmark has to construct three Cartopy axes manually. In the first benchmark render, the longer manual panel labels are visibly tighter than Figanos' automatically managed facet headings. That exposes a real layout/API gap rather than something that should be hidden by the comparison.

## What this benchmark does not prove

It does not establish a universal winner and it does not test scientific correctness. It also does not claim that passing the ar6-sciplot audit proves exact reproduction: projection, panel geometry, annotations and scientific method still require reference-specific review.

The practical conclusion is narrower:

- choose **Figanos** when the main requirement is a mature, flexible climate plotting library with strong Xarray ergonomics;
- use **ar6-sciplot** when the additional requirement is explicit AR6/WGI profile provenance, report-era semantics, delivery constraints, and auditable fidelity rules.

The benchmark should be maintained as evidence for that distinction rather than as marketing intended to make ar6-sciplot win.
