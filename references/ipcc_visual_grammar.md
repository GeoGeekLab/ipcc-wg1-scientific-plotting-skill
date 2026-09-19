# AR6 WGI visual grammar

This document defines what this project means by **IPCC AR6 WGI style**.

It separates high-confidence report-wide rules from figure-family conventions
and chapter-specific details. A figure should not be called "IPCC-faithful"
merely because it uses a blue-red palette or a sans-serif font.

## 1. Delivery geometry and typography

### Physical size

For IPCC print delivery:

- single-column width: **9 cm**;
- double-column width: **18 cm**;
- maximum figure height: **25 cm**;
- design and inspect the figure at its final physical size.

The helper's automatic aspect ratio is only a convenience. Exact reproduction
must match the reference figure's geometry.

### Text and axes

- Use **Arial** for strict fidelity.
- Smaller figures use about **9 pt** text; larger figures about **11 pt**.
- Keep axes black at **0.5 pt**.
- Avoid decorative bold/italic/underline text unless the reference figure
  clearly requires emphasis.
- Put units in **parentheses**, e.g. `Temperature change (°C)`, not
  `Temperature change [K]`.
- Prefer °C rather than K when communicating temperature change to the general
  WGI readership unless the scientific context requires K.
- Spell out unfamiliar acronyms on first use where space permits.

### Raster delivery

- print raster output: **350 ppi**;
- web derivatives may use lower resolution, but they are not the print master.

### Titles and panel labels

- Give panels short, indicative titles when they improve first-glance reading.
- Use conventional `(a)`, `(b)`, ... labels consistently.
- A title should communicate the panel's subject, not repeat the full caption.

## 2. Colour semantics

Colour is semantic, not decorative.

### Scenario colours

If a line represents an SSP or RCP, use the matching scenario token. Never
assign scenarios from Matplotlib's default cycle.

The project keeps report-era and June-2022 profiles separate because the SSP
palette changed.

### Generic line colours

For non-semantic multi-series line charts, use the WGI generic colour order.
When more than six series are required, reuse colour with a secondary linestyle
encoding rather than introducing arbitrary new colours.

Line width is **not** a universal IPCC constant beyond the delivery minimum.
Match the reference/archetype; the package's 1 pt data line is a convenience
default, not a fidelity claim.

### Continuous fields

Use an official AR6 WGI colour family matched to the physical variable:

- `temp_*` — temperature
- `prec_*` — precipitation
- `cryo_*` — cryosphere
- `chem_*` — chemistry
- `slev_*` — sea level
- `wind_*` — wind
- `misc_*` — only when no domain-specific family applies

Use sequential palettes for ordered one-direction fields and diverging palettes
for anomalies/change around a meaningful centre.

**Strict mode has no generic fallback.** If the official palette asset is not
available, the renderer must fail rather than substitute `RdBu`, `viridis`,
`cmocean` or another palette while still claiming IPCC fidelity.

## 3. Axes, frames and grids

- Keep axes visually subordinate to the data.
- Do not add grid lines by default.
- Remove frames or secondary decoration when they add clutter without aiding
  interpretation.
- Tick density should support reading at final publication size.
- Do not use a truncated axis in a way that exaggerates magnitude.
- Avoid dual y axes unless the scientific relationship genuinely requires them
  and the encoding remains unambiguous.

## 4. Legends and direct labels

Prefer direct annotation when it reduces eye travel and remains uncluttered.

When a separate legend or colour bar is needed:

- place it close to the encoded data;
- use available white space before consuming an extra margin;
- use a restrained black **0.5 pt** bounding box;
- order items by scientific/semantic meaning, not plotting-call order;
- explain every colour or texture that appears outside the main colour scale.

## 5. Colour bars

- Always show the relevant unit.
- Use a common colour scale across panels that are meant to be compared.
- Do not vary limits silently across adjacent panels.
- Keep the bar large enough for ticks and labels to remain legible at final size.
- For diverging data, centre the scale on the scientifically meaningful
  reference value when appropriate; symmetry is not required merely for visual balance.

## 6. Maps

There is no single universal "IPCC map projection".

Projection, extent, central longitude and land treatment are part of a
**figure archetype** and must be chosen from the scientific task or the
reference figure being reproduced.

Recurring WGI traits include:

- subdued geographic context;
- grey land/context when land is not the plotted variable in relevant archetypes;
- thin coastlines/boundaries;
- strong data layer, weak base map;
- explicit colour-bar units;
- no decorative basemap;
- missing data represented distinctly from uncertainty/robustness.

A Robinson projection may be appropriate for some global display figures but is
not an IPCC-wide default.

## 7. Uncertainty, agreement and significance

Do not collapse distinct statistical concepts into a single hatch/stipple layer.

### Ensemble agreement

Low sign agreement may be shown with hatching when that is the declared method.
The threshold belongs to the scientific method and must appear in the caption or
metadata. **80% is not a universal IPCC style default.**

### Insufficient data

Insufficient model/sample count is a separate category. Use a mask/blank/neutral
treatment, not the same texture used for low agreement.

### Statistical significance

Stippling may be used when it genuinely represents a significance criterion.
It must not be used as a synonym for model agreement.

### Robust information first

Texture must not obscure the central field. If most of a map is robust, prefer
leaving robust areas visually clean and marking the exceptional/low-confidence
areas.

## 8. Shading and uncertainty bands

- Shading is subordinate to the central estimate.
- Keep the centre line readable over the interval.
- Label the interval explicitly: e.g. 5–95%, 17–83%, 95% CI.
- No one interval is globally prescribed by the visual style.
- Do not call different uncertainty quantities generically "error".
- Scenario-specific uncertainty bands should retain scenario semantics rather
  than using unrelated colours.

## 9. Multi-panel composition

- Arrange panels according to scientific logic, not merely loop order.
- Use shared axes/colour bars only when quantities and scales are genuinely common.
- Maintain readable panel size; do not shrink maps until labels or spatial
  structure are no longer legible.
- Keep panel-label and title positions consistent.

## 10. Message-first design

The WGI guide is not a theme sheet. It treats each figure as communication.

Before rendering, state:

- what the reader should learn;
- the scientific estimand;
- comparison/reference period;
- uncertainty definition;
- semantic colour mapping;
- target figure family;
- final physical size;
- style profile.

The visual grammar follows those decisions.

## 11. What is not IPCC fidelity

The following are useful scientific-plotting practices but are not, by
themselves, evidence of WGI visual fidelity:

- xarray/Dask/Zarr;
- provenance JSON;
- FAIR metadata;
- FDR correction;
- model-equal weighting;
- a 17–83% range;
- an 80% agreement threshold;
- using a perceptually uniform generic colormap;
- removing top/right spines.

Keep workflow reproducibility and scientific methodology separate from the
visual style.
