<div align="center">

# ipcc-wg1-scientific-plotting-skill

**IPCC AR6 WGI visual grammar, distilled into Python.**

Profiles · official colour assets · publication geometry · uncertainty encodings · figure audit · source-backed regression

[![CI](https://github.com/GeoGeekLab/ipcc-wg1-scientific-plotting-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/GeoGeekLab/ipcc-wg1-scientific-plotting-skill/actions/workflows/ci.yml)
[![Reference reproductions](https://github.com/GeoGeekLab/ipcc-wg1-scientific-plotting-skill/actions/workflows/reference-reproductions.yml/badge.svg)](https://github.com/GeoGeekLab/ipcc-wg1-scientific-plotting-skill/actions/workflows/reference-reproductions.yml)
[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12-3776AB?style=flat-square&logo=python&logoColor=white)](pyproject.toml)
[![PyPI](https://img.shields.io/pypi/v/ar6-sciplot?style=flat-square)](https://pypi.org/project/ar6-sciplot/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](LICENSE)

</div>

```text
evidence → profile → tokens → render → audit → reference regression
```

## Install

```bash
python -m pip install ar6-sciplot
```

Climate/map stack:

```bash
python -m pip install "ar6-sciplot[climate]"
git clone https://github.com/IPCC-WG1/colormaps.git
git -C colormaps checkout b7d3849d4fa521d2583b91360e875e38f191d209
export IPCC_WG1_COLORMAPS_DIR=/path/to/colormaps
```

Distribution: `ar6-sciplot`  
Import: `ipcc_sciplot`  
CLI: `ar6plot`

## What ships

| Surface | Implementation |
| --- | --- |
| AR6 profiles | `ar6-report`, `wgi-guide-2022` |
| SSP / RCP | semantic scenario colours |
| Official WGI colour assets | pinned commit + Git blob verification |
| Print geometry | 90 / 180 mm widths, ≤250 mm height |
| Raster delivery | 350 ppi reference output |
| Typography | Arial-first publication context |
| Direct labels | collision-aware line-end labels |
| Map panels | fixed-size Cartopy panel grids |
| Uncertainty | agreement hatch, missing-data mask, significance stipple |
| Figure QA | structured Python audit + `ar6plot` CLI |
| Reference QA | source-backed contracts + exact PNG regression |
| Provenance | input hashes, Git state, dependency metadata |

## 30-second plot

```python
import matplotlib.pyplot as plt

from ipcc_sciplot import (
    audit_figure_report,
    axis_label,
    label_line_ends,
    publication_context,
    scenario_style,
)

series = {
    "SSP1-2.6": [1.1, 1.25, 1.35, 1.42, 1.48],
    "SSP2-4.5": [1.1, 1.35, 1.65, 1.95, 2.20],
    "SSP5-8.5": [1.1, 1.55, 2.15, 2.90, 3.75],
}
years = [2020, 2040, 2060, 2080, 2100]

with publication_context(width="double", height_mm=92, strict_font=False):
    fig, ax = plt.subplots()
    lines = {}

    for scenario, values in series.items():
        style = scenario_style(scenario, profile="ar6-report")
        (line,) = ax.plot(years, values, color=style.color, label=scenario)
        lines[scenario] = line

    label_line_ends(ax, lines)
    ax.set_xlabel("Year")
    ax.set_ylabel(axis_label("Temperature change", "°C"))

report = audit_figure_report(
    fig,
    profile="ar6-report",
    strict_dimensions=True,
    reference_size_mm=(180, 92),
)

print(report.render_text())
```

## AR6 source-data comparison

<img src="examples/visual_comparison/ar6-source-fidelity.svg" alt="AR6 Chapter 6 methane-emissions source data rendered with four plotting treatments">

Same data, four rendering treatments. Source: AR6 WGI Chapter 6 Figure 6.18 methane-emissions data, pinned at:

```text
IPCC-WG1/Chapter-6_Fig18
09d9b43fe935fc81d828147f91b717396a84fca3
```

Rebuild:

```bash
python examples/visual_comparison.py
python examples/visual_comparison.py --check
```

## Cross-library benchmark

Figanos 0.7.0 and `ar6-sciplot` are executed against shared scenario data and controlled map inputs.

| Check | Figanos 0.7.0 | ar6-sciplot |
| --- | --- | --- |
| Xarray-native faceting | native | explicit panel grid |
| SSP WGI-2022 colours | exact match | exact match |
| Report-era SSP profile | — | `ar6-report` |
| IPCC colormap delivery | bundled / registered | external, pinned, blob-verified |
| Direct labels, benchmark case | SSP1-1.9 / SSP1-2.6 collision | no SSP label collision |
| Controlled 3-panel size | 180 × 72 mm | 180 × 72 mm |
| Reference geometry audit | — | size / panels / projection |
| Plotting surface | broad climate plotting API | AR6-focused helpers + QA |

Benchmark code and recorded output:

- [method](benchmarks/ipcc_plotting/README.md)
- [results](benchmarks/ipcc_plotting/RESULTS.md)
- [workflow](.github/workflows/plotting-benchmark.yml)

## Reference regression

Four AR6 WGI source-data reproductions live in the repository. Three carry structured contracts in addition to exact committed-PNG regression.

### Chapter 6 — Figure 6.18 source

<p align="center">
  <img width="100%" src="examples/ipcc_reference/outputs/ch06_fig6_18_ch4_emissions.png" alt="AR6 WGI Chapter 6 Figure 6.18 methane-emissions reproduction">
</p>

```text
source       IPCC-WG1/Chapter-6_Fig18 @ 09d9b43f…
canvas       180 × 92 mm
profile      ar6-report
contract     x-range · labels · SSP legend · SSP colours
raster       350 ppi
regression   exact PNG + SHA256 + image metrics
```

<table>
<tr>
<td width="50%" valign="top">
<strong>Chapter 3 — Figure 3.2b</strong><br>
90 × 120 mm · limits · labels · title · panel bbox · legend contract<br><br>
<img width="100%" src="examples/ipcc_reference/outputs/ch03_fig3_2b_scatter.png" alt="AR6 WGI Chapter 3 Figure 3.2b reproduction">
</td>
<td width="50%" valign="top">
<strong>Chapter 10 — Figure 10.20b</strong><br>
90 × 72 mm · Lambert Conformal · projected viewport · legend order<br><br>
<img width="100%" src="examples/ipcc_reference/outputs/ch10_fig10_20b_stations.png" alt="AR6 WGI Chapter 10 Figure 10.20b reproduction">
</td>
</tr>
</table>

<details>
<summary><strong>Chapter 2 — Figure 2.3 paleo CO₂ reconstruction</strong></summary>

<br>

<img width="70%" src="examples/ipcc_reference/outputs/ch02_fig2_3_co2_proxy.png" alt="AR6 WGI Chapter 2 Figure 2.3 paleo CO2 reproduction">

</details>

Reference regression reports:

```text
physical canvas
panel geometry
axis limits
projection / viewport
legend content
scenario colours
pixel dimensions
mean absolute pixel error
changed-pixel fraction
64 × 64 thumbnail error
SHA256
```

Current committed references reproduce at zero pixel error in CI.

Source commits and output hashes:

- [reference gallery](examples/ipcc_reference/README.md)
- [manifest](examples/ipcc_reference/outputs/manifest.json)
- [contracts](examples/ipcc_reference/contracts.py)
- [regression workflow](.github/workflows/reference-reproductions.yml)

## Figure audit

CLI:

```bash
ar6plot audit figure.py   --strict-dimensions   --reference-size-mm 180 92   --reference-panel-count 3   --reference-projection Robinson
```

JSON for CI:

```bash
ar6plot audit figure.py   --strict-dimensions   --format json   --output outputs/audit.json
```

Typical output:

```text
AR6 fidelity audit — PASS
Profile: ar6-report

PASS  text.unit-convention
PASS  delivery.width
PASS  delivery.height
PASS  reference.width
PASS  reference.height
PASS  reference.panel-count

Summary: 6 passed, 0 failed
```

Python:

```python
from ipcc_sciplot import audit_figure_report

report = audit_figure_report(
    fig,
    profile="ar6-report",
    strict_dimensions=True,
    reference_size_mm=(180, 92),
    reference_panel_count=3,
    reference_projection="Robinson",
)

assert report.passed
print(report.to_dict())
```

## Profiles

| Profile | Tokens |
| --- | --- |
| `ar6-report` | final-report-era AR6 colours and conventions |
| `wgi-guide-2022` | June 2022 WGI visual guidance |

Example: SSP2-4.5

```text
ar6-report       #EADD3D
wgi-guide-2022   #F79420
```

```python
from ipcc_sciplot import scenario_style

scenario_style("SSP2-4.5", profile="ar6-report")
scenario_style("SSP2-4.5", profile="wgi-guide-2022")
```

## Official WGI colormaps

The manifest is pinned to:

```text
IPCC-WG1/colormaps
b7d3849d4fa521d2583b91360e875e38f191d209
```

All 43 continuous, discrete, and categorical RGB assets are verified by Git blob SHA in CI.

```python
from ipcc_sciplot import (
    OFFICIAL_COLORMAP_COMMIT,
    load_ipcc_colormap,
    verify_official_colormap_checkout,
)

print(OFFICIAL_COLORMAP_COMMIT)
verify_official_colormap_checkout()
cmap = load_ipcc_colormap("temp_div")
```

Verified Matplotlib colormaps carry asset name, blob SHA, and source commit metadata. The strict map audit reads that metadata.

## Layout + uncertainty

Fixed-size map panels:

```python
from cartopy import crs as ccrs
from ipcc_sciplot import map_panel_grid

fig, axes = map_panel_grid(
    3,
    projection=ccrs.Robinson(),
    width="double",
    height_mm=72,
)
```

Uncertainty legend:

```python
from ipcc_sciplot import add_uncertainty_legend

add_uncertainty_legend(
    ax,
    low_agreement="Low agreement",
    insufficient_data="Insufficient data",
    significance="Statistically significant",
)
```

Line-end labels:

```python
from ipcc_sciplot import label_line_ends

label_line_ends(ax, scenario_lines, min_gap_points=2)
```

## v2.3.0

```text
+ Figanos cross-library benchmark
+ collision-aware direct labels
+ fixed-size map panel grids
+ uncertainty legends
+ reference size / panel / projection audit
+ pinned + blob-verified official WGI colormaps
+ source-backed structured figure contracts
+ image regression metrics
+ quieter audit output
```

## Repository map

```text
scripts/ipcc_sciplot/
├── tokens.py          # profiles, scenario colours, delivery tokens
├── colormaps.py       # official asset loading + blob verification
├── style.py           # publication context, labels, typography
├── archetypes.py      # scenario plots, panel grids, direct labels
├── maps.py            # map context + uncertainty encodings
├── fidelity.py        # structured figure audit
├── uncertainty.py     # statistical masks
├── provenance.py      # hashes + environment metadata
├── recipe.py
└── cli.py

benchmarks/ipcc_plotting/
├── benchmark.py
├── competitors.yaml
├── README.md
└── RESULTS.md

examples/ipcc_reference/
├── contracts.py
├── compare_regressions.py
├── reproduce_ch02_fig2_3.py
├── reproduce_ch03_fig3_2b.py
├── reproduce_ch06_fig6_18_ch4.py
├── reproduce_ch10_fig10_20b.py
└── outputs/
```

## Development

```bash
git clone https://github.com/GeoGeekLab/ipcc-wg1-scientific-plotting-skill.git
cd ipcc-wg1-scientific-plotting-skill

python -m pip install -e ".[qa]"
ruff check .
pytest -q

python examples/quickstart.py
python examples/visual_comparison.py --check
python examples/ipcc_reference/generate_all.py
```

CI matrix:

```text
Python 3.11
Python 3.12
package build + twine check
reference reproductions
reference contracts
exact PNG regression
cross-library plotting benchmark
official colormap manifest verification
```

## Sources

- [source corpus](references/SOURCES.md)
- [evidence matrix](references/evidence_matrix.md)
- [visual grammar](references/ipcc_visual_grammar.md)
- [figure archetypes](references/figure_archetypes.md)
- [fidelity checklist](references/fidelity_checklist.md)
- [statistical rules](references/statistical_rules.md)

## License

Project code and documentation: [MIT](LICENSE).

Upstream IPCC figures, datasets, colour assets, chapter code, fonts, and other third-party material retain their source terms. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

Independent implementation.
