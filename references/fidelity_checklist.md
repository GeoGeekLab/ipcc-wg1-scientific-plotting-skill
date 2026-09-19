# Fidelity checklist

A render may be described as **IPCC AR6 WGI-faithful** only when the applicable
checks pass.

## Profile and provenance

- [ ] Correct profile selected: `ar6-report` or `wgi-guide-2022`
- [ ] If reproducing a figure, chapter/figure/reference is identified
- [ ] Post-report 2022 tokens have not silently replaced report-era tokens

## Delivery geometry and typography

- [ ] Figure width is 90 mm or 180 mm for IPCC print delivery
- [ ] Figure height is no more than 250 mm
- [ ] Arial resolved with no silent font fallback
- [ ] Text remains legible at final size (about 9 pt small / 11 pt large)
- [ ] Axes are restrained and use the 0.5 pt delivery grammar unless reference-specific
- [ ] Units use parentheses
- [ ] Short title/panel title supports first-glance reading
- [ ] Acronyms are understandable from figure/caption
- [ ] No unnecessary grid, frame or decorative element
- [ ] Print raster master is exported at 350 ppi when raster output is required

## Colour

- [ ] SSP/RCP series use semantic scenario colours
- [ ] Non-semantic lines use WGI generic colour order where appropriate
- [ ] Map uses an official variable-matched WGI colormap
- [ ] Diverging scale has a scientifically meaningful centre
- [ ] Comparable panels share scale where appropriate
- [ ] No rainbow/jet
- [ ] No unlabelled colour outside the colour bar/legend

## Legends and annotations

- [ ] Direct labels used where clearer than a legend
- [ ] Legend order follows scientific semantics
- [ ] Legend/colour bar is close to data
- [ ] Separate legend/colour bar uses restrained black 0.5 pt boundary where applicable
- [ ] Colour bar includes units
- [ ] Shaded areas/texture meaning is visible in figure or caption

## Maps

- [ ] Projection is explicit and justified/reference-matched
- [ ] Geographic context is subordinate to data
- [ ] Missing data is not encoded as model disagreement
- [ ] Low agreement is not encoded as statistical significance
- [ ] Significance stippling is used only for an explicit significance test
- [ ] Robust signal remains visually readable beneath uncertainty layers

## Uncertainty

- [ ] Interval type is named
- [ ] Valid sample/model count policy is defined
- [ ] Agreement threshold is defined if used
- [ ] Threshold/interval values come from the scientific method or reference figure, not "IPCC style"
- [ ] Categories are non-overlapping where the method requires them
- [ ] Ensemble construction/weighting is documented

## Reproduction-specific

- [ ] Projection, extent, line weights, labels and panel geometry compared
- [ ] Colour levels and normalization compared
- [ ] Annotation/legend placement compared
- [ ] No chapter-specific convention generalized beyond this reproduction

If any strict item fails, describe the result as **IPCC-inspired/adapted**, not
IPCC-faithful.
