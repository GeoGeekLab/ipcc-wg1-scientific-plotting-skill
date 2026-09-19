# Visual encoding

The canonical visual-style specification is:

- `ipcc_visual_grammar.md`
- `figure_archetypes.md`
- `fidelity_checklist.md`
- `evidence_matrix.md`

Strict fidelity rules:

- use the correct time/profile (`ar6-report` vs `wgi-guide-2022`);
- use the 90 mm / 180 mm IPCC delivery geometry when preparing print figures;
- use Arial in strict mode;
- keep axes at the 0.5 pt delivery grammar unless a reference figure clearly differs;
- export print raster at 350 ppi;
- use semantic SSP/RCP colours;
- use official WGI colormaps for strict maps;
- keep units in parentheses;
- keep agreement, missing data and statistical significance visually distinct;
- never silently fall back to generic Matplotlib/cmocean palettes.

Scientific-method values such as 17–83%, 80% agreement, median, equal-model weighting or FDR are not visual-style tokens. They belong to the analysis/reference figure and must be declared separately.

General scientific-visualisation advice may fill gaps only where the AR6 WGI source corpus is silent.
