# Source corpus and evidence hierarchy

This project distils the visual grammar of **IPCC AR6 Working Group I**. It is
independent and is not an official IPCC product.

## Evidence hierarchy

When sources disagree, use this order:

1. **WGI Visual Style Guide (June 2022 update)** — normative visual guidance.
2. **WGI TSU figure-review comments** — evidence of rules actually enforced during AR6.
3. **Official AR6 WGI colormap repository** — canonical palette assets.
4. **Final-figure / chapter plotting code** — implementation evidence and figure-family conventions.
5. **Atlas uncertainty guidance** — uncertainty/robustness semantics.
6. **General scientific-visualisation practice** — only when AR6 evidence is silent.

Do not promote a single chapter's local implementation into a report-wide rule
unless it is supported by a higher-level source or appears repeatedly across chapters.

## Primary sources

### Visual Style Guide

- IPCC WGI Visual Style Guide, updated June 2022  
  https://www.ipcc.ch/site/assets/uploads/2022/09/IPCC_AR6_WGI_VisualStyleGuide_2022.pdf
- WGI resources page listing the guide  
  https://www.ipcc.ch/working-group/wg1/

The guide covers message-first design, chart choice, colours, typography and axes,
legends/colour bars, sizing, labels/annotations, visual cues, uncertainty,
captions, testing, metadata/code and file delivery.

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

These are used to identify recurring implementation patterns, not to claim that
every chapter used identical code.

### WGI TSU review evidence

The First Order Draft review records contain repeated TSU requests that were
taken into account during figure revision. Particularly useful examples:

- Chapter 4 review:
  https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_FOD_CommentsResponses_Chapter04.pdf
- Chapter 5 review:
  https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_FOD_CommentsResponses_Chapter05.pdf
- Chapter 6 review:
  https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_FOD_CommentsResponses_Chapter06.pdf
- Chapter 7 review:
  https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_FOD_CommentsResponses_Chapter07.pdf
- Chapter 9 review:
  https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_FOD_CommentsResponses_Chapter09.pdf

Repeated enforced conventions include Arial, units in parentheses, use of
prescribed RCP/temperature colours, short panel titles, reduced clutter,
colour-blind-safe choices, explicit explanation of shading and missing data,
and clearer in-figure legends/annotations.

### Uncertainty and robustness

- AR6 WGI Atlas chapter:
  https://www.ipcc.ch/report/ar6/wg1/chapter/atlas/

The Atlas framework is the primary source for map robustness principles:
uncertainty categories must be interpretable, mutually exclusive where defined,
and must not visually suppress the robust signal.

## Two style profiles

The repository intentionally distinguishes:

- `ar6-report` — reproduce final-report-era semantics when matching an AR6 figure.
- `wgi-guide-2022` — apply the June-2022 updated WGI visual-style tokens.

Do not silently mix the two. Some SSP colours changed between report-era helper
code and the 2022 guide update.

## Copyright and redistribution

IPCC figures and upstream assets have their own copyright and licensing terms.
This repository stores original helper code, source references, semantic tokens
needed for interoperability, and filenames for upstream colour assets. Consult
each upstream source before redistributing its code, data or graphics.
