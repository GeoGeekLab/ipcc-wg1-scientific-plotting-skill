# Fidelity checklist

Use this checklist for strict AR6 WGI reproductions.

## Profile and provenance

- [ ] Correct profile selected: `ar6-report` or `wgi-guide-2022`
- [ ] Chapter / figure / reference identified for reproductions
- [ ] Report-era and post-report tokens are kept distinct

## Delivery geometry and typography

- [ ] Figure width is 90 mm or 180 mm
- [ ] Figure height is no more than 250 mm
- [ ] Arial resolved for strict output
- [ ] Text remains legible at final size
- [ ] Axes follow the 0.5 pt delivery grammar unless the reference differs
- [ ] Units use parentheses
- [ ] Short title / panel title supports first-glance reading
- [ ] Acronyms are understandable from figure or caption
- [ ] Grid, frame and decoration are limited to useful elements
- [ ] Raster master is 350 ppi when raster output is required

## Colour

- [ ] SSP/RCP series use semantic scenario colours
- [ ] Non-semantic lines use WGI generic colours where appropriate
- [ ] Map uses an official variable-matched WGI colormap
- [ ] Diverging scale has a meaningful centre
- [ ] Comparable panels share scale where appropriate
- [ ] Extra colours are identified in the legend or caption

## Legends and annotations

- [ ] Direct labels used where clearer than a legend
- [ ] Legend order follows scientific semantics
- [ ] Legend / colour bar stays close to data
- [ ] Colour bar includes units
- [ ] Shading, hatch and stipple meanings are visible

## Maps

- [ ] Projection is explicit and reference-matched where applicable
- [ ] Geographic context is subordinate to data
- [ ] Missing data, agreement and significance use separate encodings
- [ ] Robust signal remains readable beneath uncertainty layers

## Uncertainty

- [ ] Interval type is named
- [ ] Valid sample / model-count policy is defined
- [ ] Agreement threshold is defined when used
- [ ] Thresholds and intervals match the analysis method or source figure
- [ ] Ensemble construction and weighting are documented

## Reproduction geometry

- [ ] Width and height match the target figure
- [ ] Panel count matches
- [ ] Projection matches
- [ ] Extent, line weights and panel geometry have been compared
- [ ] Colour levels and normalization match
- [ ] Annotation and legend placement match

The machine audit can check size, panel count and projection when reference values are supplied.
