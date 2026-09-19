# IPCC AR6 WGI Scientific Plotting Skill

High-fidelity scientific plotting distilled from the **IPCC AR6 Working Group I** visual language.

This project is based on WGI visual-style guidance, official AR6 colormaps, chapter plotting code, TSU figure-review evidence, and Atlas uncertainty guidance.

> [!IMPORTANT]
> Independent project. Not an official IPCC product and does not imply IPCC endorsement.

## What it preserves

- 9 cm / 18 cm IPCC print geometry and 25 cm maximum height
- Arial-first WGI typography, 9/11 pt sizing and 0.5 pt axis grammar
- 350 ppi print-raster delivery
- AR6 report-era and June-2022 SSP colour profiles
- RCP and generic WGI line colours
- Official temperature, precipitation, cryosphere, chemistry, sea-level and wind colormaps
- Scenario time-series and ensemble-band grammar
- Map context, colour-bar and multi-panel conventions
- Separate encodings for model agreement, insufficient data and statistical significance
- A strict fidelity gate that refuses silent non-IPCC fallbacks

## Fidelity modes

**Strict** means IPCC-faithful: correct temporal profile, Arial, IPCC delivery geometry, semantic colours, official palette assets and explicit map projection.

**Adapted** means IPCC-inspired: substitutions are allowed, but the output must not be described as an exact WGI-style reproduction.

See `references/fidelity_checklist.md`.

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

There is intentionally **no** automatic `RdBu`, `viridis` or cmocean fallback in strict mode.

## Quick start

    python examples/quickstart.py

The example uses semantic SSP colours, WGI text conventions and the print-delivery context.

    from ipcc_sciplot import axis_label, publication_context, scenario_style

    with publication_context(width="double", strict_font=False):
        style = scenario_style("SSP2-4.5", profile="ar6-report")
        ax.plot(year, value, color=style.color)
        ax.set_ylabel(axis_label("Temperature change", "°C"))

Use `strict_font=True` when the output will be described as IPCC-faithful.

## Evidence, not vibes

The distillation is auditable rather than aesthetic guesswork.

- `references/SOURCES.md` — source hierarchy
- `references/evidence_matrix.md` — rule-by-rule scope/confidence
- `references/ipcc_visual_grammar.md` — shared visual grammar
- `references/figure_archetypes.md` — figure-family rules
- `references/fidelity_checklist.md` — strict gate

A key rule: analysis choices such as median vs mean, 17–83% ranges, 80% sign agreement or equal-model weighting are **not** promoted into visual-style tokens.

## Project structure

    scripts/ipcc_sciplot/
      tokens.py          WGI semantic colours and design tokens
      colormaps.py       strict loader for official WGI colour assets
      style.py           delivery geometry, typography, labels and export
      archetypes.py      recurring figure-family helpers
      maps.py            geographic context and uncertainty layers
      fidelity.py        machine-checkable fidelity audit
      uncertainty.py     statistical helpers (not style defaults)
      provenance.py      reproducibility metadata

    references/
      SOURCES.md
      evidence_matrix.md
      ipcc_visual_grammar.md
      figure_archetypes.md
      fidelity_checklist.md
      statistical_rules.md

## Validation

    pytest -q
    python examples/quickstart.py
    python scripts/check_figure.py outputs/quickstart.pdf --metadata outputs/quickstart.provenance.json

CI runs Ruff, tests and the end-to-end example on Python 3.11 and 3.12.

A figure may be called **IPCC AR6 WGI-faithful** only when the applicable fidelity checks pass.

## Scope

The goal is not one frozen Matplotlib theme. AR6 WGI contains multiple figure families and chapter-specific implementations.

The project distils the shared visual grammar, preserves documented semantic tokens, makes time/profile differences explicit, and refuses to turn method-specific choices into fake report-wide defaults.
