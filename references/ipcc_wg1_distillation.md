# Distillation architecture

Version 0.2 separates visual fidelity from scientific-method and reproducibility concerns.

## Layer 1 — source evidence

Use `SOURCES.md` and `evidence_matrix.md` to classify every rule by source, scope and confidence.

For exact AR6 reproduction, the published figure and contemporaneous AR6 guidance take precedence over later guide updates. For new figures using the June-2022 guide, select the `wgi-guide-2022` profile explicitly.

## Layer 2 — delivery grammar

Machine-readable delivery tokens cover:

- 90 mm / 180 mm figure widths;
- 250 mm maximum height;
- 9 pt / 11 pt text conventions;
- 0.5 pt axes and legend/colour-bar boundaries;
- 350 ppi print-raster output;
- Arial-preferred sans serif typography;
- units in parentheses.

These rules are grounded in the AR6 WGI Visual Style Guide rather than generic journal defaults.

## Layer 3 — semantic colour tokens

`tokens.py` stores:

- generic WGI line colours;
- generic shading colours;
- report-era SSP/RCP semantics;
- June-2022 SSP semantics;
- restrained map-context colours.

Official continuous/discrete/categorical RGB tables remain upstream and are loaded by semantic filename through `colormaps.py`.

## Layer 4 — visual grammar

`ipcc_visual_grammar.md` defines the report-wide rules that can legitimately be called IPCC visual style.

## Layer 5 — figure archetypes

`figure_archetypes.md` captures recurring families rather than pretending one universal theme exists.

## Layer 6 — scientific method

`statistical_rules.md` intentionally separates analysis choices from visual style. Median vs mean, interval quantiles, sign-agreement thresholds, weighting, FDR and projection are not promoted into IPCC-wide defaults.

## Layer 7 — fidelity QA

`fidelity.py` checks what can be automated. `fidelity_checklist.md` covers reference-specific geometry, projection, colour normalization, annotations and method choices that still require human comparison.

## Layer 8 — reproducibility

Plotted-data, provenance, environment capture and tests remain important, but they cannot substitute for visual fidelity.
