# IPCC AR6 WGI Scientific Plotting Skill

High-fidelity scientific plotting distilled from the **IPCC AR6 Working Group I** visual language.

This project is based on the WGI Visual Style Guide, official AR6 colormaps, chapter plotting code, TSU figure-review evidence, and Atlas uncertainty guidance.

> [!IMPORTANT]
> Independent project. Not an official IPCC product and does not imply IPCC endorsement.

## What it preserves

- Arial-first WGI typography and unit conventions
- AR6 report-era and June-2022 SSP colour profiles
- RCP and generic WGI line colours
- Official temperature, precipitation, cryosphere, chemistry, sea-level and wind colormaps
- Scenario time-series and ensemble-band grammar
- Map context, colour-bar and multi-panel conventions
- Separate encodings for model agreement, insufficient data and statistical significance
- A strict fidelity gate that refuses silent non-IPCC fallbacks

## Fidelity modes

**Strict** means IPCC-faithful: correct profile, Arial, official palette assets, explicit map projection and semantic uncertainty encoding.

**Adapted** means IPCC-inspired: substitutions are allowed, but the output must not be described as an exact WGI-style reproduction.

See references/fidelity_checklist.md.

## Install

    python -m venv .venv
    source .venv/bin/activate
    python -m pip install -e ".[qa]"

For climate/map workflows:

    python -m pip install -e ".[climate,qa]"

## Official colormaps

Strict map rendering uses an authorized local checkout of the official WGI colormap repository rather than redistributing its RGB assets here.

    git clone https://github.com/IPCC-WG1/colormaps.git
    export IPCC_WG1_COLORMAPS_DIR=/path/to/colormaps

    from ipcc_sciplot import load_ipcc_colormap
    cmap = load_ipcc_colormap("temp_div")

There is intentionally **no** automatic RdBu, viridis or cmocean fallback in strict mode.

## Quick start

    python examples/quickstart.py

The example uses semantic SSP colours and WGI text conventions.

    from ipcc_sciplot import axis_label, publication_context, scenario_style

    with publication_context(width="double", strict_font=False):
        style = scenario_style("SSP2-4.5", profile="ar6-report")
        ax.plot(year, value, color=style.color)
        ax.set_ylabel(axis_label("Temperature change", "°C"))

Use strict_font=True when the output will be described as IPCC-faithful.

## Evidence, not vibes

The distillation uses this source hierarchy:

1. WGI Visual Style Guide
2. WGI TSU figure-review comments
3. official IPCC-WG1/colormaps
4. AR6 chapter/final-figure plotting code
5. Atlas uncertainty guidance
6. general scientific-visualisation practice only where WGI evidence is silent

See references/SOURCES.md and references/ipcc_visual_grammar.md.

## Project structure

    scripts/ipcc_sciplot/
      tokens.py          WGI semantic colours and design tokens
      colormaps.py       strict loader for official WGI colour assets
      style.py           typography, labels, panels, legends and export
      archetypes.py      recurring figure-family helpers
      maps.py            geographic context and uncertainty layers
      uncertainty.py     ensemble/statistical summaries
      provenance.py      reproducibility metadata

    references/
      SOURCES.md
      ipcc_visual_grammar.md
      figure_archetypes.md
      fidelity_checklist.md
      statistical_rules.md

    templates/
      figure_recipe.yaml

## Validation

    pytest -q

A figure may be called **IPCC AR6 WGI-faithful** only when the applicable checks in references/fidelity_checklist.md pass.

## Scope

The goal is not to reproduce one frozen Matplotlib theme. AR6 WGI contains multiple figure families and chapter-specific implementations.

The project distils the shared visual grammar, preserves documented semantic tokens, and keeps figure-level exceptions explicit.
