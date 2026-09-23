# Distillation architecture

The project separates source evidence, visual tokens, figure layout, scientific method, and reproducibility.

## Layer 1 — source evidence

`SOURCES.md` and `evidence_matrix.md` classify rules by source, scope and confidence.

For AR6 reproductions, the published figure and contemporaneous guidance take precedence. New figures can select the June-2022 `wgi-guide-2022` profile.

## Layer 2 — delivery grammar

Machine-readable tokens cover:

- 90 mm / 180 mm figure widths;
- 250 mm maximum height;
- 9 pt / 11 pt text conventions;
- 0.5 pt axes and legend/colour-bar boundaries;
- 350 ppi print raster;
- Arial-preferred typography;
- units in parentheses.

## Layer 3 — semantic colour tokens

`tokens.py` stores:

- generic WGI line colours;
- generic shading colours;
- report-era SSP/RCP semantics;
- June-2022 SSP semantics;
- restrained map-context colours.

Official continuous/discrete RGB tables remain upstream and are loaded through `colormaps.py`.

## Layer 4 — visual grammar

`ipcc_visual_grammar.md` contains report-wide visual rules.

## Layer 5 — figure archetypes

`figure_archetypes.md` covers recurring figure families and multi-panel layout.

## Layer 6 — scientific method

`statistical_rules.md` records analysis choices such as center statistic, interval quantiles, agreement thresholds, weighting and FDR.

## Layer 7 — fidelity QA

`fidelity.py` checks delivery, semantic colours, official colormap use, and supplied reference geometry. `fidelity_checklist.md` covers the remaining visual comparison.

## Layer 8 — reproducibility

Plotted data, provenance, environment capture and regression tests support repeatable figure production.
