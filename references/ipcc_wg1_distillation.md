# Distillation architecture

Version 0.2 separates reproducible climate workflow practice from visual fidelity.

## Layer 1 — evidence

Use the hierarchy in SOURCES.md:

Visual Style Guide → TSU review evidence → official colour assets → repeated chapter implementations → Atlas uncertainty guidance → general best practice.

## Layer 2 — design tokens

Machine-readable tokens live in scripts/ipcc_sciplot/tokens.py:

- generic WGI line colours;
- generic shading colours;
- report-era SSP/RCP semantics;
- June-2022 SSP semantics;
- typography and line-weight tokens;
- map context colours.

Official continuous/discrete/categorical RGB tables remain upstream and are loaded by semantic filename through colormaps.py.

## Layer 3 — visual grammar

ipcc_visual_grammar.md defines report-wide constraints:

- Arial in strict mode;
- units in parentheses;
- scenario-semantic colour;
- official variable-specific map palettes;
- restrained axes/context;
- colour-bar/legend rules;
- separate uncertainty semantics.

## Layer 4 — figure archetypes

figure_archetypes.md defines families rather than a single theme:

- scenario time series;
- ensemble centre + interval;
- global/regional map;
- map matrix;
- generic multi-series line;
- categorical/point comparison.

## Layer 5 — render helpers

Reusable helpers apply tokens but do not choose the scientific method silently.

## Layer 6 — fidelity QA

fidelity_checklist.md determines whether a render can be described as IPCC-faithful. Failing strict requirements downgrades the label to IPCC-inspired/adapted.

## Layer 7 — reproducibility

Plotted-data, provenance, environment capture and statistical tests remain important, but they no longer substitute for style fidelity.
