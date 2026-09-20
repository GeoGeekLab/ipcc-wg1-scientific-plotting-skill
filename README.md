<div align="center">

# ipcc-wg1-scientific-plotting-skill

**Evidence-backed visual grammar and fidelity checks for IPCC AR6 WGI scientific figures.**

<code>source → profile → render → audit → reproduce</code>

[![CI](https://github.com/GeoGeekLab/ipcc-wg1-scientific-plotting-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/GeoGeekLab/ipcc-wg1-scientific-plotting-skill/actions/workflows/ci.yml)
[![Reference reproductions](https://github.com/GeoGeekLab/ipcc-wg1-scientific-plotting-skill/actions/workflows/reference-reproductions.yml/badge.svg)](https://github.com/GeoGeekLab/ipcc-wg1-scientific-plotting-skill/actions/workflows/reference-reproductions.yml)
[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12-3776AB?style=flat-square&logo=python&logoColor=white)](pyproject.toml)
[![AR6 WGI](https://img.shields.io/badge/IPCC-AR6%20WGI-111111?style=flat-square)](references/SOURCES.md)
[![Fidelity](https://img.shields.io/badge/fidelity-strict%20%7C%20adapted-2ea44f?style=flat-square)](references/fidelity_checklist.md)

**Not a Matplotlib theme.** The project encodes AR6/WGI visual semantics, delivery geometry,
official colour assets, uncertainty grammar, provenance, and machine-checkable fidelity.

</div>

> [!IMPORTANT]
> Independent project. Not an official IPCC product and does not imply IPCC endorsement.

## See the reference reproductions first

These figures are regenerated from **pinned official IPCC AR6 WGI source repositories**,
not synthetic demo data. Source commits, physical dimensions, and SHA256 checksums are
recorded in the [reference gallery](examples/ipcc_reference/README.md) and
[manifest](examples/ipcc_reference/outputs/manifest.json).

<table>
<tr>
<td width="50%" valign="top">
<strong>Chapter 3 — Figure 3.2b</strong><br>
Scatter + fitted relationship.<br><br>
<img src="examples/ipcc_reference/outputs/ch03_fig3_2b_scatter.png" alt="Chapter 3 Figure 3.2b reproduction">
</td>
<td width="50%" valign="top">
<strong>Chapter 10 — Figure 10.20b</strong><br>
Mediterranean station map.<br><br>
<img src="examples/ipcc_reference/outputs/ch10_fig10_20b_stations.png" alt="Chapter 10 Figure 10.20b reproduction">
</td>
</tr>
<tr>
<td width="50%" valign="top">
<strong>Chapter 2 — Figure 2.3</strong><br>
Paleo CO₂ proxies + uncertainty.<br><br>
<img src="examples/ipcc_reference/outputs/ch02_fig2_3_co2_proxy.png" alt="Chapter 2 Figure 2.3 reproduction">
</td>
<td width="50%" valign="top">
<strong>Chapter 6 — Figure 6.18 source</strong><br>
Historical + scenario CH₄ emissions.<br><br>
<img src="examples/ipcc_reference/outputs/ch06_fig6_18_ch4_emissions.png" alt="Chapter 6 Figure 6.18 source reproduction">
</td>
</tr>
</table>

## Why this is different

A lot of “IPCC-style” plotting stops at a diverging palette, a sans-serif font,
and some hatching. This repository treats AR6 WGI as a **visual system with evidence
and failure conditions**, not a theme.

- **Evidence-backed rules** — WGI guides, TSU review comments, official colormaps,
  chapter code, Atlas guidance, and published reference figures are kept distinct.
- **Semantic colour** — SSP/RCP colours and variable-specific map palettes carry
  meaning; they are not a decorative colour cycle.
- **Explicit fidelity modes** — strict/IPCC-faithful and adapted/IPCC-inspired are
  separate claims.
- **Fail-closed strict mode** — no silent fallback to <code>viridis</code>, <code>RdBu</code>,
  cmocean, or an arbitrary font while still claiming fidelity.
- **Method ≠ style** — median, 17–83%, 80% agreement, FDR, weighting, and projection
  remain analysis/reference choices unless evidence says otherwise.
- **Auditable outputs** — physical dimensions, typography, semantic colours,
  official-colormap use, provenance, and reference regressions can be checked.

The goal is not to make a plot look vaguely IPCC-ish. The goal is to make the
**fidelity claim inspectable**.

## Quick start

Requires Python 3.11+.

~~~bash
git clone https://github.com/GeoGeekLab/ipcc-wg1-scientific-plotting-skill.git
cd ipcc-wg1-scientific-plotting-skill
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[qa]"
~~~

Run a minimal, copy-pasteable example:

~~~python
import matplotlib.pyplot as plt
import numpy as np

from ipcc_sciplot import audit_figure, axis_label, publication_context, scenario_style

year = np.arange(2015, 2101)
warming = np.linspace(1.1, 2.7, year.size)
style = scenario_style("SSP2-4.5", profile="ar6-report")

with publication_context(width="double", strict_font=False):
    fig, ax = plt.subplots()
    ax.plot(year, warming, color=style.color, label="SSP2-4.5")
    ax.set_xlabel("Year")
    ax.set_ylabel(axis_label("Temperature change", "°C"))
    ax.legend()

issues = audit_figure(
    fig,
    profile="ar6-report",
    strict_font=False,
    strict_dimensions=True,
)

print("fidelity audit:", issues or "passed")
plt.show()
~~~

This first run deliberately allows a font substitution. A figure should only be
called **strictly IPCC-faithful** when all strict requirements are satisfied,
including Arial where required.

For map/climate workflows:

~~~bash
python -m pip install -e ".[climate,qa]"
git clone https://github.com/IPCC-WG1/colormaps.git
export IPCC_WG1_COLORMAPS_DIR=/path/to/colormaps
~~~

Strict maps load the official WGI colormap assets directly and intentionally have
**no generic palette fallback**.

## Choose the fidelity contract

| Goal | Profile / mode | Contract |
| --- | --- | --- |
| Reproduce a published AR6 figure | <code>ar6-report</code> + strict | Match the published figure first, then contemporaneous AR6 guidance and source code. |
| Create a new figure using the updated WGI guidance | <code>wgi-guide-2022</code> + strict | Use the June-2022 guide explicitly rather than silently rewriting final-report semantics. |
| Use the visual language with documented substitutions | adapted / IPCC-inspired | Substitutions are allowed, but the result must not be labelled exact or faithful. |

Two style profiles are explicit and are never silently mixed:

~~~text
ar6-report       → final-report-era AR6 semantics
wgi-guide-2022   → June-2022 WGI guide update
~~~

## Execution model

~~~text
SOURCE → PROFILE → FIGURE CONTRACT → RENDER → AUDIT → REFERENCE
~~~

| Stage | Question |
| --- | --- |
| **Source** | Which WGI evidence or published figure defines the rule? |
| **Profile** | Are we reproducing final-report AR6 or using the 2022 guide? |
| **Figure contract** | What quantity, geometry, uncertainty method, palette, projection, and output size are required? |
| **Render** | Which archetype and semantic tokens apply? |
| **Audit** | What can be machine-checked, and what still needs visual comparison? |
| **Reference** | Can the output be regenerated from pinned source data and verified by SHA256? |

## What is encoded

~~~text
delivery
  ├── 90 / 180 mm print widths
  ├── ≤ 250 mm height
  ├── 9 / 11 pt WGI typography
  ├── 0.5 pt axis grammar
  └── 350 ppi raster master

semantics
  ├── SSP / RCP colours
  ├── WGI generic line colours
  ├── variable-specific official colormaps
  └── report-era vs 2022 profiles

uncertainty
  ├── model agreement
  ├── insufficient data
  └── statistical significance

qa
  ├── text + unit conventions
  ├── semantic colour audit
  ├── physical-size audit
  ├── official-colormap audit
  └── source-data regression gallery
~~~

## Repository map

```text
ipcc-wg1-scientific-plotting-skill/
├── SKILL.md                         # skill contract + routing
├── scripts/ipcc_sciplot/
│   ├── tokens.py                    # semantic WGI colours + design tokens
│   ├── colormaps.py                 # official WGI asset loader
│   ├── style.py                     # delivery geometry + typography
│   ├── archetypes.py                # recurring figure families
│   ├── maps.py                      # map context + uncertainty layers
│   ├── fidelity.py                  # machine-checkable fidelity audit
│   ├── uncertainty.py               # statistical helpers, not style defaults
│   └── provenance.py                # reproducibility metadata
├── references/
│   ├── SOURCES.md                   # source hierarchy
│   ├── evidence_matrix.md           # rule → evidence → scope → confidence
│   ├── ipcc_visual_grammar.md        # canonical visual grammar
│   ├── figure_archetypes.md          # figure-family rules
│   ├── fidelity_checklist.md         # strict gate
│   └── statistical_rules.md          # method/style separation
├── examples/
│   ├── quickstart.py
│   └── ipcc_reference/              # pinned source-data regressions
├── templates/
│   └── figure_recipe.yaml
└── tests/
```

## Verification

Run the local contract:

```bash
ruff check .
pytest -q
python examples/quickstart.py
python scripts/check_figure.py   outputs/quickstart.pdf   --metadata outputs/quickstart.provenance.json
```

Rebuild the pinned IPCC reference gallery:

```bash
python -m pip install cartopy
python examples/ipcc_reference/generate_all.py
git diff --exit-code -- examples/ipcc_reference/outputs
```

CI covers Python 3.11 and 3.12. The reference workflow regenerates the four official-source cases and fails if the committed gallery drifts.

## Evidence model

The source hierarchy is deliberately explicit:

```text
published reference figure
        ↓
WGI visual guidance + TSU review evidence
        ↓
official IPCC-WG1 colour assets
        ↓
chapter / final-figure implementation code
        ↓
Atlas uncertainty guidance
        ↓
general scientific-visualisation practice
```

Start with:

- [source corpus](references/SOURCES.md)
- [evidence matrix](references/evidence_matrix.md)
- [visual grammar](references/ipcc_visual_grammar.md)
- [figure archetypes](references/figure_archetypes.md)
- [fidelity checklist](references/fidelity_checklist.md)

## The boundary

This repository does **not** claim that one Matplotlib theme can represent all of AR6 WGI.

It also does not turn scientific-method choices into fake visual defaults.

```text
17–83% range       ≠ IPCC style
80% agreement      ≠ IPCC style
median             ≠ IPCC style
equal-model weight ≠ IPCC style
Robinson           ≠ universal IPCC projection
```

Those choices belong to the analysis or the published reference figure.

## License and third-party material

Original project code and documentation are licensed under the [MIT License](LICENSE).

That license does **not** relicense IPCC figures, source data, colour assets,
chapter code, fonts, or other third-party material referenced or fetched by the
reproducibility workflows. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)
and [the source corpus](references/SOURCES.md) before redistributing upstream
material.

This is an independent project. It is not an official IPCC product and does not
imply IPCC endorsement.

---

<div align="center">

**Source it. Encode it. Render it. Prove it.**

</div>
