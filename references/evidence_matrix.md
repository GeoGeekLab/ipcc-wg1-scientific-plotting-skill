# Evidence matrix

This matrix prevents a chapter-specific habit or a generic publication norm from
being mislabeled as a report-wide IPCC rule.

| Rule / token | Evidence | Scope | Confidence |
| --- | --- | --- | --- |
| Arial / sans serif | WGI visual guide; repeated TSU comments in Chapters 5, 6, 9 | report-wide | high |
| Units in parentheses, not square brackets | visual guide; repeated TSU comments | report-wide | high |
| Prefer °C to K for communicated temperature change | Chapter 9 TSU general comments; Chapter 4 consistency comment | many WGI communication figures, not a physics rule | high |
| 9 cm / 18 cm widths; max 25 cm height | WGI visual guide | IPCC delivery layout | high |
| 9 pt small / 11 pt large figure text | WGI visual guide | IPCC delivery typography | high |
| Black 0.5 pt axes | WGI visual guide | report-wide default | high |
| 350 ppi print raster delivery | WGI visual guide | print delivery | high |
| Legend / colour-bar black 0.5 pt bounding box | WGI visual guide | when a separate legend/bar is used | high |
| Prefer direct labels when clearer | WGI visual guide | report-wide design principle | high |
| RCP semantic colours | visual guide; TSU review; Chapter 9 helper | RCP figures | high |
| SSP report-era colours | Chapter 9 helper; contemporary AR6 usage | `ar6-report` profile | high |
| Updated SSP colours | official `ssp_cat_2.txt`; June-2022 guide | `wgi-guide-2022` profile | high |
| Domain colour families (`temp`, `prec`, etc.) | official IPCC-WG1 colormaps repo | maps/continuous fields | high |
| Short indicative panel titles | repeated TSU review comments | recommended report-wide | high |
| Spell out unfamiliar acronyms | repeated TSU review comments | report-wide communication | high |
| Remove unnecessary grid/frame/clutter | visual guide; Chapter 6 and Chapter 2 TSU comments | report-wide principle | high |
| Grey land/context | Chapter 9 map helper and repeated figure practice | map archetype, not universal | medium |
| One universal map projection | contradicted by chapter diversity | **not a rule** | high |
| 80% sign agreement | used in some AR6 methods/helpers | method-specific, not style-wide | medium |
| Hatching for low agreement | Atlas/chapter implementations | method-specific | medium-high |
| White/blank for missing data | TSU review evidence; figure-specific practice | recommended separation | medium-high |
| Stippling = statistical significance | common convention only when method defines it | method-specific | medium |
| 17–83% interval | appears in some AR6 analyses | scientific choice, not report-wide style | high that it is **not universal** |
| Median / equal-model weighting | analysis-dependent | scientific choice, not visual style | high that it is **not universal** |
| Robinson projection | used in some figures | figure-specific, **not a default** | high |

## Interpretation

A **high-confidence report-wide** rule may become a strict token or audit check.

A **figure-family** rule belongs in an archetype.

A **method-specific** rule must be declared in the figure contract and must not
be activated solely because the user requested "IPCC style".

A **not universal** item must never be hard-coded as an IPCC default.
