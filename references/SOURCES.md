# Source corpus and evidence hierarchy

This project distils the visual grammar of **IPCC AR6 Working Group I**. It is
independent and is not an official IPCC product.

## Evidence hierarchy

There is no single timeless "IPCC theme". Rules must be interpreted against the
target profile.

### Reproducing a specific AR6 final figure

Use this order:

1. **The published reference figure itself** — geometry, projection, panel order,
   labels, levels and other figure-specific decisions.
2. **Contemporaneous AR6 WGI visual guidance and TSU review evidence** — report-wide
   conventions actually enforced during production.
3. **Official AR6 WGI colour assets and final/chapter plotting code** — semantic
   colour and implementation evidence.
4. **Atlas uncertainty guidance** — uncertainty/robustness semantics where relevant.
5. **General scientific-visualisation practice** — only where AR6 evidence is silent.

### Creating a new figure with the updated WGI guide

Use the **June 2022 WGI Visual Style Guide** as the normative visual profile,
together with official WGI colour assets and the same uncertainty principles.

Do not let the post-report 2022 SSP palette silently overwrite colours when the
goal is to reproduce a 2021 final-report figure.

## Primary sources

### Visual Style Guides

- IPCC Visual Style Guide for Authors, WGI TSU, 2018 / AR6 production baseline  
  https://www.ipcc.ch/site/assets/uploads/2019/04/IPCC-visual-style-guide.pdf
- IPCC WGI Visual Style Guide, updated June 2022  
  https://www.ipcc.ch/site/assets/uploads/2022/09/IPCC_AR6_WGI_VisualStyleGuide_2022.pdf
- WGI resources page listing the updated guide  
  https://www.ipcc.ch/working-group/wg1/

The AR6 production guide establishes the physical delivery grammar used by this
project: 9 cm or 18 cm figure width, maximum 25 cm height, approximately 9 pt
text on smaller figures and 11 pt on larger figures, black 0.5 pt axes,
parenthesised units, Arial-preferred sans serif typography, restrained legends
and colour bars, and 350 ppi raster delivery for print.

The June-2022 update is retained as a separate style profile rather than being
treated as retroactive evidence for every 2021 final-report figure.

### Official AR6 WGI colour assets

- https://github.com/IPCC-WG1/colormaps

The official repository includes continuous, discrete and categorical colour
tables, including semantic families for temperature, precipitation, cryosphere,
chemistry, sea level and wind.

This project does **not** vendor the upstream RGB tables. Faithful mode loads an
authorized local checkout through `IPCC_WG1_COLORMAPS_DIR`.

### WGI plotting implementations

- Chapter 9: https://github.com/IPCC-WG1/Chapter-9
  - `Functions/IPCC_Get_LineColors.m`
  - `Functions/IPCC_Get_SSPColors.m`
  - `Functions/IPCC_Plot_Map.m`
  - `Functions/IPCC_Get_Colorbar.m`
- Chapter 11: https://github.com/IPCC-WG1/Chapter-11
- Chapter 6 Figure 19: https://github.com/IPCC-WG1/Chapter-6_Fig19
- Chapter 2 Figure 31: https://github.com/IPCC-WG1/Chapter-2_Fig31
- Atlas: https://github.com/IPCC-WG1/Atlas

These are implementation evidence and figure-family examples. A local helper in
one chapter is not automatically a report-wide rule.

### WGI TSU review evidence

The First Order Draft review records are especially valuable because they show
which visual conventions the TSU asked authors to change during AR6 production.

- Chapter 2:
  https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_FOD_CommentsResponses_Chapter02.pdf
- Chapter 4:
  https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_FOD_CommentsResponses_Chapter04.pdf
- Chapter 5:
  https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_FOD_CommentsResponses_Chapter05.pdf
- Chapter 6:
  https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_FOD_CommentsResponses_Chapter06.pdf
- Chapter 7:
  https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_FOD_CommentsResponses_Chapter07.pdf
- Chapter 9:
  https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_FOD_CommentsResponses_Chapter09.pdf
- Chapter 10:
  https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_FOD_CommentsResponses_Chapter10.pdf

Repeated enforced conventions include Arial, units in parentheses, semantic RCP
and temperature/precipitation palettes, short indicative titles, spelled-out
acronyms, reduced visual clutter, explicit legends and colour-bar units, and
clear separation of missing data from uncertainty textures.

### Uncertainty and robustness

- AR6 WGI Atlas chapter:
  https://www.ipcc.ch/report/ar6/wg1/chapter/atlas/

The Atlas framework is the main source for map robustness principles:
uncertainty categories must remain interpretable and should not suppress the
robust central signal.

## Style profiles

- `ar6-report` — reproduce final-report-era semantics and contemporaneous code.
- `wgi-guide-2022` — use the June-2022 updated WGI visual-style tokens.

The profile is part of provenance and must never be inferred silently.

## Evidence matrix

See `evidence_matrix.md` for a rule-by-rule record of source strength and scope.

## Copyright and redistribution

Original project code and documentation are licensed under the repository's
[MIT License](../LICENSE), except where a file states otherwise.

The MIT License does **not** relicense IPCC figures, source data, colour assets,
chapter code, fonts, or other third-party material. Those upstream materials
retain their own copyright, licensing, attribution, and reuse terms.

This repository stores original helper code, source references, semantic tokens
needed for interoperability, and filenames for upstream colour assets. It does
not vendor the official WGI RGB tables. Consult each upstream source before
redistributing its code, data or graphics, and see
[THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md) for the project-wide
boundary.
