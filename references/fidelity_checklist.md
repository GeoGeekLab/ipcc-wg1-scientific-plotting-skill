# Fidelity checklist

A render may be described as **IPCC AR6 WGI-faithful** only when the applicable
checks pass.

## Global

- [ ] Correct profile selected: `ar6-report` or `wgi-guide-2022`
- [ ] Arial resolved with no silent font fallback
- [ ] Units use parentheses
- [ ] Short title/panel title supports first-glance reading
- [ ] Acronyms are understandable from figure/caption
- [ ] No unnecessary grid, frame or decorative element
- [ ] Final physical size is known and text remains legible

## Colour

- [ ] SSP/RCP series use semantic scenario colours
- [ ] Non-semantic lines use WGI generic colour order
- [ ] Map uses an official variable-matched WGI colormap
- [ ] Diverging scale has a scientifically meaningful centre
- [ ] Comparable panels share scale where appropriate
- [ ] No rainbow/jet
- [ ] No unlabelled colour outside the colour bar/legend

## Legends and annotations

- [ ] Direct labels used where clearer than a legend
- [ ] Legend order follows scientific semantics
- [ ] Legend/colour bar is close to data
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
- [ ] Categories are non-overlapping where the method requires them
- [ ] Ensemble construction/weighting is documented

## Reproduction-specific

- [ ] Reference figure/chapter identified
- [ ] Report-era vs 2022-guide palette difference checked
- [ ] Projection, extent, line weights, labels and panel geometry compared
- [ ] No chapter-specific convention generalized beyond this reproduction

If any strict item fails, describe the result as **IPCC-inspired/adapted**, not
IPCC-faithful.
