# Figure archetypes

AR6 WGI figures recur in several visual families. The shared tokens below are combined with figure-specific geometry and scientific method.

## A. Scenario time series

Use for historical/projected evolution across SSPs or RCPs.

- scenario colours are semantic and profile-specific;
- historical/observed series are neutral unless the reference specifies otherwise;
- uncertainty bands use a related shade of the corresponding series;
- direct labels or legends stay close to the lines;
- interval meaning is explicit;
- units use parentheses;
- titles state the quantity or comparison.

## B. Ensemble centre + interval

Use for a central estimate with model or observational spread.

- central estimate visually dominates the interval;
- interval label states its statistic;
- individual ensemble members remain secondary unless trajectories are the message;
- neutral black/grey works for non-scenario series.

## C. Global or regional change map

- use an official variable-matched WGI colormap;
- set explicit levels and a meaningful centre for diverging data;
- set projection, central longitude and extent;
- keep geographic context subdued;
- colour bar carries units;
- low agreement, insufficient data and significance use separate encodings.

Projection follows the target figure or scientific context.

## D. Map matrix / small multiples

Use for period × scenario, variable × warming level, or comparable spatial panels.

- comparable panels share limits and palette;
- use one shared colour bar when units and scales match;
- row/column headings carry the comparison logic;
- panel labels stay in fixed positions;
- keep maps readable at final size;
- apply uncertainty overlays consistently.

`map_panel_grid()` provides fixed physical figure dimensions and compact panel allocation.

## E. Multi-series line comparison

For non-scenario series:

- use the WGI generic colour order;
- after six colours, add line-style variation;
- direct-label lines when practical;
- otherwise use a semantically ordered legend.

## F. Categorical / point comparison

Use report-wide grammar with figure-specific layout:

- Arial;
- semantic or generic WGI colours;
- minimal decoration;
- direct labels where useful;
- units in parentheses;
- meaningful ordering;
- explicitly identified uncertainty intervals.

## Profiles

### Strict

Use for AR6/WGI style reproduction.

- Arial
- selected style profile
- official WGI palette assets for maps
- explicit map projection
- semantic scenario colours
- fidelity audit

### Adapted

Use the same visual grammar with documented substitutions for font, palette or layout.
